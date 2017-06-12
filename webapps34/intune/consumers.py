from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
import json

from channels import Group
from .models import ChatMessage, Composition, Profile, Comment

# TODO: Check user permissions

# Connected to websocket.connect
def ws_chat_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    path = message.content['path'].strip("/")
    print("connected to ", path)
    Group("%s" % path).add(message.reply_channel)


# Connected to websocket.receive
def ws_chat_message(message):
    text = json.loads(message.content['text'])
    room_id = text['room']
    user_id = text['user']
    msg = text['msg']
    sender_name = Profile.objects.get(id=user_id).user.username
    type = text['type']
    if type == "chatmsg":
        ChatMessage.objects.create(
            room=Composition.objects.get(id=room_id),
            msg=msg,
            sender=Profile.objects.get(id=user_id),
        )
    elif type == "comment":
        bar_id = text['bar']
        Comment.objects.create(
            composition=Composition.objects.get(id=room_id),
            comment=msg,
            bar=bar_id,
            commenter=Profile.objects.get(id=user_id)
        )
    else:
        print("wrong type")

    group_postfix = get_group_postfix(text)
    print("group postfix", group_postfix)
    Group("chat-%s" % group_postfix).send({
        "text": json.dumps({
            "user": str(sender_name),
            "msg": str(msg),
        })
    })


# Connected to websocket.disconnect
def ws_chat_disconnect(message):
    # check that disconnect is called by chatbox
    if 'text' in message.content.keys():
        text = json.loads(message.content['text'])
        group_postfix = get_group_postfix(text)
        Group("chat-%s" % group_postfix).discard(message.reply_channel)
    else:
        print("Unexpected disconnect, message: ", message)


def get_group_postfix(text):
    type = text["type"]
    if type == "chatmsg":
        return str(text["room"])
    elif type == "comment":
        return str(text["room"]) + "-" + str(text["bar"])
    else:
        print("error: unexpected msg type ", type)
        return


class Selection:
    compositions = {}
    # Each { comp_id: { user: bar } }

    @classmethod
    def select(cls, composition, bar, user):
        Selection.deselect(composition, user)
        compositions[composition][user] = bar
        Group("comp-%s" % composition).send({
            "text": json.dumps({
                "bar_mod": "select",
                "bar_id": bar,
                "user": str(user),
            }),
        })

    @classmethod
    def deselect(cls, composition, user):
        if composition in compositions:
            bar = compositions[composition].pop(user, None)
            Group("comp-%s" % composition).send({
                "text": json.dumps({
                    "bar_mod": "deselect",
                    "bar_id": bar,
                    "user": str(user),
                }),
            })
        else:
            compositions[composition] = {}

    @classmethod
    def get_selection(cls, composition, user):
        Selection.deselect(composition, user)
        return compositions[composition]


@channel_session_user_from_http
def ws_bar_connect(message, comp):
    message.reply_channel.send({"accept": True})
    Group("comp-%s" % comp).add(message.reply_channel)
    message.reply_channel.send(Selection.get_selection(comp, message.user))


@channel_session_user
def ws_bar_receive(message, comp):
    contents = json.loads(message.content['text'])
    composition = Composition.objects.get(pk=comp)

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
            Selection.select(comp, bar_id, message.user)
        elif contents['action'] == "deselect":
            Selection.select(comp, message.user)
        else:
            print("Invalid WebSocket composition request")


@channel_session_user
def ws_bar_disconnect(message, comp):
    Group("comp-%s" % comp).discard(message.reply_channel)
    Selection.deselect(comp, message.user)
