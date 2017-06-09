import json

from channels import Group
from .models import ChatMessage, Room


# Connected to websocket.connect
# def ws_add(message, room):
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    path = message.content['path'].strip("/")
    Group("%s" % path).add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    text = json.loads(message.content['text'])
    room_id = text['room']
    msg = text['msg']

    ChatMessage.objects.create(
        room=Room.objects.get(id=room_id),
        msg=msg,
    )
    Group("chat-%s" % room_id).send({
        "text": msg,
    })


# Connected to websocket.disconnect
def ws_disconnect(message):
    text = json.loads(message.content['text'])
    room_id = text['room']
    Group("chat-%s" % room_id).discard(message.reply_channel)
