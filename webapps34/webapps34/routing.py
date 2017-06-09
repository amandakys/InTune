from channels import include
from channels.routing import route
from channels.staticfiles import StaticFilesConsumer

from intune import consumers

http_routing = [
    route("http.request", StaticFilesConsumer()),
]

chat_routing = [
    route("websocket.connect", consumers.ws_chat_add),
    route("websocket.receive", consumers.ws_chat_message),
    route("websocket.disconnect", consumers.ws_chat_disconnect),
]

channel_routing = [
    include(chat_routing, path=r"^/chat"),
    include(http_routing),
]
