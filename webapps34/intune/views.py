from django.shortcuts import render

# Create your views here.
from .models import Composition


def user_home(request,user_id):
    composition_list = Composition.objects.filter(owner = user_id)
    context = {'composition_list': composition_list}
    return render(request, 'core/user_home.html', context)