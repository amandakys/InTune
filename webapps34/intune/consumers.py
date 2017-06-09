import json

from channels import Group
from .models import ChatMessage, Composition, Profile, Comment


# Connected to websocket.connect
# def ws_add(message, room):
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    path = message.content['path'].strip("/")
    print("connected to ", path)
    Group("%s" % path).add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    print("ws message ", message.content)
    text = json.loads(message.content['text'])
    room_id = text['room']
    user_id = text['user']
    msg = text['msg']
    sender_name = Profile.objects.get(id=user_id).user.username
    type = text['type']
    if type == "chatmsg":
        bar_id = 0
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

    group_postfix = get_group_postfix(type, room_id, bar_id)
    print("group postfix", group_postfix)
    Group("chat-%s" % group_postfix).send({
        "text": json.dumps({
            "user": str(sender_name),
            "msg": str(msg),
        })
    })


def ws_disconnect(message):
    # check that disconnect is called by chatbox
    if 'text' in message.content.keys():
        text = json.loads(message.content['text'])
        room_id = text['room']
        type = text['type']
        bar_id = get_bar_id(text)
        group_postfix = get_group_postfix(type, room_id, bar_id)
        Group("chat-%s" % group_postfix).discard(message.reply_channel)
    else:
        print("Unexpected disconnect, message: ", message)


def get_group_postfix(type, room_id, bar_id):
    if type == "chatmsg":
        return room_id
    elif type == "comment":
        return str(room_id) + "-" + str(bar_id)
    else:
        print("error: unexpected msg type ", type)
        return


def get_bar_id(text):
    type = text["text"]
    if type == "chatmsg":
        # return default bar number for composition wide channels
        return 0
    elif type == "comment":
        return text["bar"]
    else:
        print("error: unexpected msg type ", type)
        return
