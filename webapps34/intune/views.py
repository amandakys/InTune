from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import generic
from .models import Composition



class UserHomeView(generic.ListView):
    def get_queryset(self):
        return self.request.user.profile.composition_set.all()

    def get_context_data(self, **kwargs):
        context = super(UserHomeView, self).get_context_data(**kwargs)
        return context


class MusicScoreOverview(TemplateView):
    @staticmethod
    def can_view(user, composition):
        shared = (shared_u == user for shared_u in composition.users.all())
        return composition.owner == user or any(shared)

    def get(self, request, composition_id, **kwargs):
        try:
            composition = Composition.objects.get(id=composition_id)
            context = {'composition': composition}
        except Composition.DoesNotExist:
            raise Http404("Composition does not exit")
        if self.can_view(request.user, composition):
            return render(request, 'intune/music_score.html', context)
        else:
            return render(request, 'intune/unauthorised_view.html')
