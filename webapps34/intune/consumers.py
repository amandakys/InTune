import json

from channels import Group
from .models import ChatMessage, Composition, Profile


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
    user_id = text['user']
    msg = text['msg']
    sender_name = Profile.objects.get(id=user_id).user.username

    ChatMessage.objects.create(
        room=Composition.objects.get(id=room_id),
        msg=msg,
        sender=Profile.objects.get(id=user_id),
    )
    Group("chat-%s" % room_id).send({
        "text": json.dumps({
            "user": str(sender_name),
            "msg": str(msg),
        })
    })


# Connected to websocket.disconnect
def ws_disconnect(message):
    text = json.loads(message.content['text'])
    room_id = text['room']
    Group("chat-%s" % room_id).discard(message.reply_channel)
