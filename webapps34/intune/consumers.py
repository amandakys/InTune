from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
import json

from django.contrib.auth.models import User

from .models import ChatMessage, Composition, Profile, Comment, Notification

# TODO: Check user permissions


# Connected to websocket.connect
def ws_chat_add(message, comp):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    Group("chat-%s" % comp).add(message.reply_channel)


# Connected to websocket.receive
def ws_chat_message(message):
    text = json.loads(message.content['text'])
    room_id = text['room']
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
def ws_chat_disconnect(message):
    text = json.loads(message.content['text'])
    group_postfix = text["room"]
    Group("chat-%s" % group_postfix).discard(message.reply_channel)


def ws_comment_add(message, comp):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    Group("comment-%s" % comp).add(message.reply_channel)


def ws_comment_message(message):
    text = json.loads(message.content['text'])
    room_id = text['room']
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


def ws_comment_disconnect(message):
    text = json.loads(message.content['text'])
    group_postfix = text["room"]
    Group("comment-%s" % group_postfix).discard(message.reply_channel)



class Selection:
    compositions = {}
    # Each { comp_id: { user: bar } }

    @classmethod
    def select(cls, composition, bar, user):
        Selection.deselect(composition, user)
        cls.compositions[composition][user.id] = bar
        Group("comp-%s" % composition).send({
            "text": json.dumps({
                "bar_mod": "select",
                "bar_id": bar,
                "user": user.id,
            }),
        })

    @classmethod
    def deselect(cls, composition, user):
        if composition in cls.compositions:
            bar = cls.compositions[composition].pop(user.id, None)
            Group("comp-%s" % composition).send({
                "text": json.dumps({
                    "bar_mod": "deselect",
                    "bar_id": bar,
                    "user": user.id,
                }),
            })
        else:
            cls.compositions[composition] = {}

    @classmethod
    def get_selection(cls, composition, user):
        Selection.deselect(composition, user)
        return cls.compositions[composition]


class Selection:
    compositions = {}
    # Each { comp_id: { user: bar } }

    @classmethod
    def select(cls, composition, bar, user):
        Selection.deselect(composition, user)
        cls.compositions[composition][user.id] = bar
        Group("comp-%s" % composition).send({
            "text": json.dumps({
                "bar_mod": "select",
                "bar_id": bar,
                "user": user.id,
            }),
        })

    @classmethod
    def deselect(cls, composition, user):
        if composition in cls.compositions:
            bar = cls.compositions[composition].pop(user.id, None)
            Group("comp-%s" % composition).send({
                "text": json.dumps({
                    "bar_mod": "deselect",
                    "bar_id": bar,
                    "user": user.id,
                }),
            })
        else:
            cls.compositions[composition] = {}

    @classmethod
    def get_selection(cls, composition, user):
        Selection.deselect(composition, user)
        return cls.compositions[composition]


@channel_session_user_from_http
def ws_bar_connect(message, comp):
    message.reply_channel.send({"accept": True})
    Group("comp-%s" % comp).add(message.reply_channel)
    message.reply_channel.send({
        "text": json.dumps({
            "bar_mod": "fresh_selects",
            "selection": Selection.get_selection(comp, message.user),
        }),
    })


@channel_session_user
def ws_bar_receive(message, comp):
    contents = json.loads(message.content['text'])
    composition = Composition.objects.get(pk=comp)
    #message.reply_channel.send({"text": json.dumps({"msg": "hello"})})

    if composition.has_access(message.user):
        if contents['action'] == "update":
            bar_contents = contents['bar_contents']
            bar_id = int(contents['bar_id'])

            composition.set_bar(bar_id, bar_contents)
            Group("comp-%s" % comp).send({
                "text": json.dumps({
                    "bar_mod": "update",
                    "bar_id": bar_id,
                    "bar_contents": bar_contents,
                }),
            })
        elif contents['action'] == "append":
            bar_contents = contents['bar_contents']

            composition.append_bar(bar_contents)
            Group("comp-%s" % comp).send({
                "text": json.dumps({
                    "bar_mod": "append",
                    "bar_contents": bar_contents,
                }),
            })
        elif contents['action'] == "select":
            Selection.select(comp, contents['bar_id'], message.user)
        elif contents['action'] == "deselect":
            Selection.select(comp, message.user)
        elif contents['action'] == "delete_last":
            if composition.delete_last_bar() >=0:
                Group("comp-%s" % comp).send({
                    "text": json.dumps({
                        "bar_mod": "delete_last",
                    }),
                })
        else:
            print("Invalid WebSocket composition request")


@channel_session_user
def ws_bar_disconnect(message, comp):
    Group("comp-%s" % comp).discard(message.reply_channel)
    Selection.deselect(comp, message.user)


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
    Group("notif-%s" % user).discard(message.reply_channel);
