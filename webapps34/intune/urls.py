from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', login_required(views.UserHomeView.as_view()), name="index"),
    url(r'^composition/(?P<pk>[0-9]+)/$', login_required(views.MusicScore.as_view()), name="song"),
    url(r'^composition/create/$',
        login_required(views.CompositionCreate.as_view()),
        name="song_create"),

    url(r'^register/$',
        views.InTuneRegister.as_view(),
        name="register"),

    url(r'^profile/$',
        views.ProfileDetail.as_view(),
        name="profile"),


]
