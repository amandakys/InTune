from channels import include
from channels.routing import route, route_class
from channels.staticfiles import StaticFilesConsumer

from intune import consumers

http_routing = [
    route("http.request", StaticFilesConsumer()),
]

chat_routing = [
    route("websocket.connect",
          consumers.ws_chat_add,
          path=r"^/(?P<comp>\d+)/$"),

    route("websocket.receive",
          consumers.ws_chat_message,
          path=r"^/(?P<comp>\d+)/$"),

    route("websocket.disconnect",
          consumers.ws_chat_disconnect,
          path=r"^/(?P<comp>\d+)/$"),
]

channel_routing = [
    include(chat_routing, path=r"^/chat"),
    route_class(consumers.EditorConsumer, path=r"^/ws_comp/(?P<comp>\d+)/$"),
    route_class(consumers.CommentConsumer, path=r"^/comment/(?P<comp>\d+)/$"),
    route_class(consumers.NotificationConsumer, path=r"^/notif/$"),
    include(http_routing),
]
