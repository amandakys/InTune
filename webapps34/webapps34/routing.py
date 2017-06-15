from channels import include
from channels.routing import route, route_class
from channels.staticfiles import StaticFilesConsumer

from intune import consumers

http_routing = [
    route("http.request", StaticFilesConsumer()),
]

channel_routing = [
    route_class(consumers.ChatConsumer, path=r"^/chat/(?P<comp>\d+)/$"),
    route_class(consumers.EditorConsumer, path=r"^/ws_comp/(?P<comp>\d+)/$"),
    route_class(consumers.CommentConsumer, path=r"^/comment/(?P<comp>\d+)/$"),
    route_class(consumers.NotificationConsumer, path=r"^/notif/$"),
    include(http_routing),
]
