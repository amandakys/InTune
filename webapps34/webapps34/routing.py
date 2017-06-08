from channels import route
from channels.staticfiles import StaticFilesConsumer

# This function will display all messages received in the console
def message_handler(message):
    print(message['text'])


channel_routing = [
    route("websocket.receive", message_handler),
    route("http.request", StaticFilesConsumer())
]
