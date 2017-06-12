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

    ChatMessage.objects.create(
        room=Composition.objects.get(id=room_id),
        msg=msg,
        sender=Profile.objects.get(id=user_id),
    )

    group_postfix = room_id
    print("sending msg to ", group_postfix)
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
        group_postfix = text["room"]
        print("disconnecting from ", group_postfix)
        Group("chat-%s" % group_postfix).discard(message.reply_channel)
    else:
        print("Unexpected disconnect, message: ", message)


def ws_comment_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    path = message.content['path'].strip("/")
    print("connected to ", path)
    Group("%s" % path).add(message.reply_channel)


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
    print("sending msg to  comment ", group_postfix)
    Group("comment-%s" % group_postfix).send({
        "text": json.dumps({
            "user": str(sender_name),
            "msg": str(msg),
            "bar": bar_id
        })
    })


def ws_comment_disconnect(message):
    if 'text' in message.content.keys():
        text = json.loads(message.content['text'])
        group_postfix = text["room"]
        print("disconnecting from ", group_postfix)
        Group("comment-%s" % group_postfix).discard(message.reply_channel)
    else:
        print("Unexpected disconnect, message: ", message)


@channel_session_user_from_http
def ws_bar_connect(message, comp):
    message.reply_channel.send({"accept": True})
    Group("comp-%s" % comp).add(message.reply_channel)


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
        else:
            print("Invalid WebSocket composition request")


@channel_session_user
def ws_bar_disconnect(message, comp):
    Group("comp-%s" % comp).discard(message.reply_channel)
