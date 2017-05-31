from . import views
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.UserHomeView.as_view()), name="index"),
    url(r'^composition/(?P<composition_id>[0-9]+)/$', login_required(views.MusicScoreOverview.as_view()), name="song")
]
