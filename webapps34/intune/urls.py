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

    url(r'^composition/bar_change/$',
        login_required(views.composition_bar_edit_ajax),
        name="bar_edit"),

    url(r'^composition/bar_append/(?P<pk>[0-9]+)/$',
        login_required(views.composition_add_bar),
        name="bar_add"),

    # (auxillary url used for django-autocomplete)
    # TODO: make this url not visible?
    url(
        r'^profile-autocomplete/$',
        login_required(views.ProfileAutocomplete.as_view()),
        name='profile-autocomplete',
    ),
]
