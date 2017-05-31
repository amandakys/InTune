from django.db.models import Q
from django.views import generic
from .models import Composition


class UserHomeView(generic.ListView):
    def get_queryset(self):
        return Composition.objects.filter(Q(owner__user=self.request.user) |
                                          Q(users__user=self.request.user))


class MusicScore(generic.DetailView):
    # TODO: consider redirect if composition not found

    def get_queryset(self):
        return Composition.objects.filter(Q(owner__user=self.request.user) |
                                          Q(users__user=self.request.user))
