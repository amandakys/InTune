from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', views.UserHomeView.as_view()),
    url(r'^song(?P<composition_id>[0-9]+)$', views.MusicScoreOverview.as_view(), name='song')
]