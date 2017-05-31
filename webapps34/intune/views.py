from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import generic
from .models import Composition


class UserHomeView(generic.ListView):
    model = Composition

    def get_context_data(self, **kwargs):
        context = super(UserHomeView, self).get_context_data(**kwargs)
        return context


class MusicScoreOverview(TemplateView):
    def get(self, request, composition_id, **kwargs):

        try:
            composition = Composition.objects.get(id=composition_id)
            context = {'composition': composition}
        except Composition.DoesNotExist:
            raise Http404("Composition does not exit")
        return render(request, 'intune/music_score.html', context)
