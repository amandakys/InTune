from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Composition


class user_home_view(TemplateView):
    def get(self, request, user_id):
        composition_list = Composition.objects.filter(owner = user_id)
        context = {'composition_list': composition_list}
        return render(request, 'core/user_home.html', context)


