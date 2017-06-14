from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.contrib.auth.models import User
import json


from .models import ChatMessage, Composition, Profile, Comment

# TODO: Check user permissions


# Connected to websocket.connect
def ws_chat_add(message, comp):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    Group("chat-%s" % comp).add(message.reply_channel)


# Connected to websocket.receive
def ws_chat_message(message, comp):
    text = json.loads(message.content['text'])
    room_id = comp
    user_id = text['user']
    msg = text['msg']
    sender_name = Profile.objects.get(id=user_id).user.username

    ChatMessage.objects.create(
        room=Composition.objects.get(id=room_id),
        msg=msg,
        sender=Profile.objects.get(id=user_id),
    )

    group_postfix = room_id
    Group("chat-%s" % group_postfix).send({
        "text": json.dumps({
            "user": str(sender_name),
            "msg": str(msg),
        })
    })


# Connected to websocket.disconnect
def ws_chat_disconnect(message, comp):
    Group("chat-%s" % comp).discard(message.reply_channel)


def ws_comment_add(message, comp):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    Group("comment-%s" % comp).add(message.reply_channel)


def ws_comment_message(message, comp):
    text = json.loads(message.content['text'])
    room_id = comp
    user_id = text['user']
    msg = text['msg']
    sender_name = Profile.objects.get(id=user_id).user.username
    bar_id = text['bar']
    Comment.objects.create(
        composition=Composition.objects.get(id=room_id),
        comment=msg,
        bar=bar_id,
        commenter=Profile.objects.get(id=user_id)
    )

    group_postfix = room_id
    Group("comment-%s" % group_postfix).send({
        "text": json.dumps({
            "user": str(sender_name),
            "msg": str(msg),
            "bar": bar_id
        })
    })


def ws_comment_disconnect(message, comp):
    Group("comment-%s" % comp).discard(message.reply_channel)


class Editor:
    # Each { Composition: { user_id: bar_id } }
    compositions = {}   # Static, access with Editor.compositions

    class Action:
        UPDATE = "update"
        APPEND = "append"
        DELETE = "delete_last"
        SELECT = "select"
        DESELECT = "deselect"

    def __init__(self, composition : Composition, user : User):
        if composition.has_access(user):
            self.composition = composition
            self.user = user
        else:
            print("Attempted unauthorised access of composition `%s` by `%s`" %
                  (composition, user))

    def send(self, bar, action, contents=None):
        if bar >= 0:
            Group("comp-%s" % self.composition.id).send({
                "text": json.dumps({
                    "bar_mod": action,
                    "bar_id": bar,
                    "user": self.user.id,   # TODO: change to username
                    "bar_contents": contents,
                }),
            })

    def delete_last(self):
        bar : int = self.composition.delete_last_bar()
        if bar >= 0:
            self.send(bar, Editor.Action.DELETE)

    def update(self, bar : int, contents : str):
        self.composition.set_bar(bar, contents)
        self.send(bar, Editor.Action.UPDATE, contents)

    def append(self, contents : str):
        bar : int= self.composition.append_bar(contents)
        self.send(bar, Editor.Action.APPEND, contents)

    def select(self, bar : int):
        self.deselect()
        Editor.compositions[self.composition][self.user.id] = bar
        self.send(bar, Editor.Action.SELECT)

    def deselect(self):
        if self.composition in Editor.compositions:
            bar = Editor.compositions[self.composition].pop(self.user.id, -1)
            self.send(bar, Editor.Action.DESELECT)
        else:
            Editor.compositions[self.composition] = {}

    def get_selection(self):
        # For newly connected users
        self.deselect()
        return Editor.compositions[self.composition]


@channel_session_user_from_http
def ws_bar_connect(message, comp):
    composition = Composition.objects.get(id=comp)

    message.reply_channel.send({"accept": True})
    Group("comp-%s" % comp).add(message.reply_channel)
    message.reply_channel.send({
        "text": json.dumps({
            "bar_mod": "fresh_selects",
            "selection": Editor(composition, message.user).get_selection(),
        }),
    })


@channel_session_user
def ws_bar_receive(message, comp):
    contents = json.loads(message.content['text'])
    composition = Composition.objects.get(pk=comp)
    comp_editor = Editor(composition, message.user)

    if composition.has_access(message.user):
        if contents['action'] == "update":
            bar_contents = contents['bar_contents']
            bar_id = int(contents['bar_id'])

            comp_editor.update(bar_id, bar_contents)
        elif contents['action'] == "append":
            bar_contents = contents['bar_contents']

            comp_editor.append(bar_contents)
        elif contents['action'] == "select":
            comp_editor.select(contents['bar_id'])
        elif contents['action'] == "deselect":
            comp_editor.deselect()
        elif contents['action'] == "delete_last":
            comp_editor.delete_last()
        else:
            print("Invalid WebSocket composition request")


@channel_session_user
def ws_bar_disconnect(message, comp):
    composition = Composition.objects.get(id=comp)

    Group("comp-%s" % comp).discard(message.reply_channel)
    Editor(composition, message.user).deselect()


def ws_notif_add(message, user):
    message.reply_channel.send({"accept": True})
    Group("notif-%s" % user).add(message.reply_channel)


def ws_notif_message(message):
    text = json.loads(message.content['text'])
    user_id = text["user_id"]
    Group("notif-%s" % user_id).send({
        "text": text
    })


def ws_notif_disconnect(message, user):
    Group("notif-%s" % user).discard(message.reply_channel)
