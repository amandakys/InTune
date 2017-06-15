from channels import Group
from channels.generic.websockets import WebsocketConsumer
from django.contrib.auth.models import User
import json

from .models import ChatMessage, Composition, Profile, Comment


class CompositionChannel:
    def __init__(self, composition_id: int, user: User):
        comp = Composition.objects.get(id=composition_id)
        self.user = user
        self.composition = comp if comp.has_access(user) else None

class CommentHandler(CompositionChannel):
    def receive(self, bar: int, message: str):
        Comment.objects.create(
            composition=self.composition,
            comment=message,
            bar=bar,
            commenter=self.user.profile,
        )
        Group("comment-%s" % self.composition.id).send({
            "text": json.dumps({
                "user": str(self.user),
                "msg": message,
                "bar": bar,
            })
        })


class ChatHandler(CompositionChannel):
    def receive(self, message: str):
        ChatMessage.objects.create(
            room=self.composition,
            msg=message,
            sender=self.user.profile,
        )
        Group("chat-%s" % self.composition.id).send({
            "text": json.dumps({
                "user": str(self.user),
                "msg": message,
            })
        })


class Editor(CompositionChannel):
    # Each { Composition: { user_id: bar_id } }
    compositions = {}   # Static, access with Editor.compositions

    class Action:
        UPDATE = "update"
        APPEND = "append"
        DELETE = "delete_last"
        SELECT = "select"
        DESELECT = "deselect"

    def send(self, bar, action, contents=None):
        if bar >= 0:
            Group("comp-%s" % self.composition.id).send({
                "text": json.dumps({
                    "bar_mod": action,
                    "bar_id": bar,
                    "user": self.user.id,   # TODO: change to username
                    "bar_contents": contents,
                }),
            })

    def delete_last(self, **kwargs):
        bar = self.composition.delete_last_bar()
        if bar >= 0:
            self.send(bar, Editor.Action.DELETE)

    def update(self, bar: int, contents: str, **kwargs):
        self.composition.set_bar(bar, contents)
        self.send(bar, Editor.Action.UPDATE, contents)

    def append(self, contents: str, **kwargs):
        bar = self.composition.append_bar(contents)
        self.send(bar, Editor.Action.APPEND, contents)

    def select(self, bar: int, **kwargs):
        self.deselect()
        Editor.compositions[self.composition][self.user.id] = bar
        self.send(bar, Editor.Action.SELECT)

    def deselect(self, **kwargs):
        if self.composition in Editor.compositions:
            bar = Editor.compositions[self.composition].pop(self.user.id, -1)
            self.send(bar, Editor.Action.DESELECT)
        else:
            Editor.compositions[self.composition] = {}

    def get_selection(self):
        # For newly connected users
        self.deselect()
        return Editor.compositions[self.composition]


class CommentConsumer(WebsocketConsumer):
    http_user = True

    def connection_groups(self, **kwargs):
        # Enforce permissions
        CommentHandler(kwargs.get("comp"), self.message.user)
        return ["comment-%s" % kwargs.get("comp")]

    def receive(self, text=None, bytes=None, **kwargs):
        contents = json.loads(text)
        CommentHandler(kwargs.get("comp"), self.message.user)\
            .receive(contents['bar'], contents['msg'])


class ChatConsumer(WebsocketConsumer):
    http_user = True

    def connection_groups(self, **kwargs):
        # Enforce permissions
        ChatHandler(kwargs.get("comp"), self.message.user)
        return ["chat-%s" % kwargs.get("comp")]

    def receive(self, text=None, bytes=None, **kwargs):
        contents = json.loads(text)
        ChatHandler(kwargs.get("comp"), self.message.user)\
            .receive(contents['msg'])


class EditorConsumer(WebsocketConsumer):
    http_user = True

    def connection_groups(self, **kwargs):
        return ["comp-%s" % kwargs.get("comp")]

    def connect(self, message, **kwargs):
        # This enforces Composition.has_access
        selection = Editor(kwargs.get("comp"), message.user).get_selection()
        self.message.reply_channel.send({"accept": True})
        self.message.reply_channel.send({
            "text": json.dumps({
                "bar_mod": "fresh_selects",
                "selection": selection,
            }),
        })

    def receive(self, text=None, bytes=None, **kwargs):
        contents = json.loads(text)
        comp_editor = Editor(kwargs.get("comp"), self.message.user)

        action = contents.get('action', None)
        bar_id = contents.get('bar_id', -1)
        bar_contents = contents.get('bar_contents', "")

        {
            Editor.Action.UPDATE: comp_editor.update,
            Editor.Action.APPEND: comp_editor.append,
            Editor.Action.DELETE: comp_editor.delete_last,
            Editor.Action.SELECT: comp_editor.select,
            Editor.Action.DESELECT: comp_editor.deselect,
        }[action](bar=bar_id, contents=bar_contents)

    def disconnect(self, message, **kwargs):
        Editor(kwargs.get("comp"), message.user).deselect()


class NotificationConsumer(WebsocketConsumer):
    http_user = True

    def connection_groups(self, **kwargs):
        return ["notify-%s" % self.message.user.id]

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})
        self.message.reply_channel.send({
            "text": json.dumps({
                "action": "unread_count",
                "unread": self.message.user.profile.unread_notifications,
                "notification_list": [notification.formatDict()
                    for notification in self.message.user.profile.get_recent()]
            }),
        })

    def receive(self, text=None, bytes=None, **kwargs):
        # There is only one message
        self.message.user.profile.mark_unread()
        Group("notify-%d" % self.message.user.id).send({
            "text": json.dumps({
                "action": "unread_count",
                "unread": 0,
                "notification_list": [],
            })
        })
