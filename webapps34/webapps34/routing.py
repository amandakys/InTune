from channels.routing import route
from channels.staticfiles import StaticFilesConsumer

from intune.consumers import ws_add, ws_message, ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
    route("http.request", StaticFilesConsumer()),
]
