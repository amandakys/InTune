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


comment_routing = [
    route("websocket.connect",
          consumers.ws_comment_add,
          path=r"^/(?P<comp>\d+)/$"),

    route("websocket.receive",
          consumers.ws_comment_message,
          path=r"^/(?P<comp>\d+)/$"),

    route("websocket.disconnect",
          consumers.ws_comment_disconnect,
          path=r"^/(?P<comp>\d+)/$"),
]

notif_routing = [
    route("websocket.connect",
          consumers.ws_notif_add),

    route("websocket.disconnect",
          consumers.ws_notif_disconnect),
]

channel_routing = [
    include(chat_routing, path=r"^/chat"),
    route_class(consumers.EditorConsumer, path=r"^/ws_comp/(?P<comp>\d+)/$"),
    include(comment_routing, path=r"^/comment"),
    include(notif_routing, path=r"^/notif"),
    include(http_routing),
]
