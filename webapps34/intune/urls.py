from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$',
        login_required(views.CompositionList.as_view()),
        name="index"),

    url(r'^composition/(?P<pk>[0-9]+)/$',
        login_required(views.CompositionDetail.as_view()),
        name="song"),

    url(r'^composition/create/$',
        login_required(views.CompositionCreate.as_view()),
        name="song_create"),

    url(r'^register/$',
        views.InTuneRegister.as_view(),
        name="register"),

    url(r'^profile/$',
        views.ProfileDetail.as_view(),
        name="profile"),

    url(r'^composition/(?P<pk>[0-9]+)/edit/$',
        login_required(views.CompositionEdit.as_view()),
        name="song_edit"),

    url(r'^composition/(?P<pk>[0-9]+)/delete/$',
        login_required(views.CompositionDelete.as_view()),
        name="song_delete"),

    url(r'^composition/bar_change/$',
        login_required(views.composition_bar_edit_ajax),
        name="bar_edit"),

    url(r'^comments/$',
        login_required(views.comment_get),
        name="comments"),

    url(r'^comments/create/$',
        login_required(views.comment_create_ajax),
        name="comment_create"),

    # (auxillary url used for django-autocomplete)
    url(
        r'^profile-autocomplete/$',
        login_required(views.ProfileAutocomplete.as_view()),
        name='profile-autocomplete',
    ),

    url(r'^composition/(?P<pk>[0-9]+)/chat/$',
        login_required(views.Chat.as_view()),
        name="chats"),

    # Retrieve Composition Attributes as JSON
    url(r'^composition/attribute/(?P<pk>[0-9]+)/$',
        login_required(views.get_composition_attribute),
        name="composition_attribute"
        ),

    url(r'^notifications/$',
        views.NotificationList.as_view(),
        name='notifications'),

    url(r'^notifications/count/$',
        views.notification_count,
        name='notification_count'),
]
