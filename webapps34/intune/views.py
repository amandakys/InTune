from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Composition


class UserHomeView(TemplateView):
    def get(self, request, user_id, **kwargs):
        composition_list = Composition.objects.filter(owner=user_id)
        context = {'composition_list': composition_list}
        return render(request, 'core/user_home.html', context)


class MusicScoreOverview(TemplateView):
    def get(self, request, composition_id, **kwargs):

        try:
            composition = Composition.objects.get(id=composition_id)
            context = {'composition': composition}
        except Composition.DoesNotExist:
            raise Http404("Composition does not exit")
        return render(request, 'core/music_score.html', context)
