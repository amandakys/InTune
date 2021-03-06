from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$',
        login_required(views.CompositionList.as_view()),
        name="index"),

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

    url(r'^comments/$',
        login_required(views.comment_get),
        name="comments"),

    # (auxillary url used for django-autocomplete)
    url(
        r'^profile-autocomplete/$',
        login_required(views.ProfileAutocomplete.as_view()),
        name='profile-autocomplete',
    ),

    # Retrieve Composition Attributes as JSON
    url(r'^composition/attribute/(?P<pk>[0-9]+)/$',
        login_required(views.get_composition_attribute),
        name="composition_attribute"
        ),
]
