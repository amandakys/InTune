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


class CompositionChannel:
    def __init__(self, composition_id: int, user: User):
        comp = Composition.objects.get(id=composition_id)
        self.user = user
        self.composition = comp if comp.has_access(user) else None


class CommentHandler(CompositionChannel):

    def receive(self, bar: int, message: str):
        Comment.objects.create(
            composition=self.composition,
            comment=message,
            bar=bar,
            commenter=self.user.profile,
        )
        Group("comment-%s" % self.composition.id).send({
            "text": json.dumps({
                "user": str(self.user),
                "msg": message,
                "bar": bar,
            })
        })


@channel_session_user_from_http
def ws_comment_add(message, comp):
    CommentHandler(comp, message.user)  # Check has_access
    message.reply_channel.send({"accept": True})
    Group("comment-%s" % comp).add(message.reply_channel)


@channel_session_user
def ws_comment_message(message, comp):
    text = json.loads(message.content['text'])
    CommentHandler(comp, message.user).receive(text['bar'], text['msg'])


@channel_session_user
def ws_comment_disconnect(message, comp):
    Group("comment-%s" % comp).discard(message.reply_channel)


class Editor(CompositionChannel):
    # Each { Composition: { user_id: bar_id } }
    compositions = {}   # Static, access with Editor.compositions

    class Action:
        UPDATE = "update"
        APPEND = "append"
        DELETE = "delete_last"
        SELECT = "select"
        DESELECT = "deselect"

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

    def delete_last(self, **kwargs):
        bar: int = self.composition.delete_last_bar()
        if bar >= 0:
            self.send(bar, Editor.Action.DELETE)

    def update(self, bar: int, contents: str, **kwargs):
        self.composition.set_bar(bar, contents)
        self.send(bar, Editor.Action.UPDATE, contents)

    def append(self, contents: str, **kwargs):
        bar: int = self.composition.append_bar(contents)
        self.send(bar, Editor.Action.APPEND, contents)

    def select(self, bar: int, **kwargs):
        self.deselect()
        Editor.compositions[self.composition][self.user.id] = bar
        self.send(bar, Editor.Action.SELECT)

    def deselect(self, **kwargs):
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
    # This enforces Composition.has_access
    selection = Editor(comp, message.user).get_selection()

    message.reply_channel.send({"accept": True})
    Group("comp-%s" % comp).add(message.reply_channel)
    message.reply_channel.send({
        "text": json.dumps({
            "bar_mod": "fresh_selects",
            "selection": selection,
        }),
    })


@channel_session_user
def ws_bar_receive(message, comp):
    contents = json.loads(message.content['text'])
    comp_editor = Editor(comp, message.user)

    action: str = contents.get('action', None)
    bar_id: int = contents.get('bar_id', -1)
    bar_contents: str = contents.get('bar_contents', "")

    {
        Editor.Action.UPDATE: comp_editor.update,
        Editor.Action.APPEND: comp_editor.append,
        Editor.Action.DELETE: comp_editor.delete_last,
        Editor.Action.SELECT: comp_editor.select,
        Editor.Action.DESELECT: comp_editor.deselect,
    }[action](bar=bar_id, contents=bar_contents)


@channel_session_user
def ws_bar_disconnect(message, comp):
    Group("comp-%s" % comp).discard(message.reply_channel)
    Editor(comp, message.user).deselect()


@channel_session_user_from_http
def ws_notif_add(message):
    message.reply_channel.send({"accept": True})
    Group("notif-%s" % message.user.id).add(message.reply_channel)


@channel_session_user
def ws_notif_disconnect(message):
    Group("notif-%s" % message.user.id).discard(message.reply_channel)
