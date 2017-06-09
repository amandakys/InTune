from channels import Group
from .models import ChatMessage, Room


# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    Group("chat").add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    ChatMessage.objects.create(
        # TODO: get correct room
        room=Room.objects.get(id=1),
        msg=message.content['text'],
    )
    Group("chat").send({
        "text": "[user] %s" % message.content['text'],
    })


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)