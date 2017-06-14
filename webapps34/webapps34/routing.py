from channels import include
from channels.routing import route
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

bar_routing = [
    route("websocket.connect",
          consumers.ws_bar_connect,
          path=r"^/(?P<comp>\d+)/$"),

    route("websocket.receive",
          consumers.ws_bar_receive,
          path=r"^/(?P<comp>\d+)/$"),

    route("websocket.disconnect",
          consumers.ws_bar_disconnect,
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
          consumers.ws_notif_add,
          path=r"^/(?P<user>\d+)/$"),

    route("websocket.receive",
          consumers.ws_notif_message),

    route("websocket.disconnect",
          consumers.ws_notif_disconnect,
          path=r"^/(?P<user>\d+)/$"),
]

channel_routing = [
    include(chat_routing, path=r"^/chat"),
    include(bar_routing, path=r"^/ws_comp"),
    include(comment_routing, path=r"^/comment"),
    include(notif_routing, path=r"^/notif"),
    include(http_routing),
]
