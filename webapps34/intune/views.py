from dal import autocomplete
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.views import generic

from .models import Composition, Profile, ChatMessage, Comment, Notification


class CompositionList(generic.ListView):
    def get_queryset(self):
        return Composition.objects.filter(Q(owner__user=self.request.user) |
                                          Q(users__user=self.request.user)
                                          ).distinct().order_by("-lastEdit")


class CompositionCreate(generic.edit.CreateView):
    model = Composition
    fields = ["title", "users"]
    success_url = reverse_lazy("intune:index")

    def get_form(self):
        form = super(CompositionCreate, self).get_form()
        form.fields['users'].widget = autocomplete.ModelSelect2Multiple(
            url='intune:profile-autocomplete')
        form.fields['users'].queryset = Profile.objects.exclude(
            user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        form.instance.save()
        return super(CompositionCreate, self).form_valid(form)


class InTuneRegister(generic.edit.CreateView):
    form_class = UserCreationForm
    template_name = "intune/register.html"
    success_url = reverse_lazy("intune:index")

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if not self.request.user.profile:
                Profile(user=self.request.user).save()
            return redirect("intune:index")
        return super(InTuneRegister, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.save()
        Profile(user=form.instance).save()
        return super(InTuneRegister, self).form_valid(form)


class ProfileDetail(generic.DetailView):
    def get_object(self, queryset=None):
        return self.request.user.profile


class CompositionEdit(generic.edit.UpdateView):
    template_name = "intune/composition_edit.html"
    model = Composition
    fields = ['users']

    def get_form(self):
        form = super(CompositionEdit, self).get_form()
        form.fields['users'].widget = autocomplete.ModelSelect2Multiple(
            url='intune:profile-autocomplete')
        form.fields['users'].queryset = Profile.objects.exclude(
            user=self.request.user)
        return form

    def get_queryset(self):
        return Composition.objects.filter(Q(owner__user=self.request.user) |
                                          Q(users__user=self.request.user)
                                          ).distinct()

    def get_success_url(self):
        return reverse_lazy("intune:song_edit", args=[self.kwargs['pk']])


class CompositionDelete(generic.edit.DeleteView):
    model = Composition
    success_url = reverse_lazy("intune:index")

    def get_queryset(self):
        return Composition.objects.filter(Q(owner__user=self.request.user) |
                                          Q(users__user=self.request.user)
                                          ).distinct()


class ProfileAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Profile.objects.none()
        qs = Profile.objects.exclude(user=self.request.user)
        if self.q:
            qs = qs.filter(user__username__istartswith=self.q)
        return qs


def get_composition_attribute(request, pk):
    """
    Returns python dictionary containing composition attributes
    :param request: Http request method
    :type request: django.core.handlers.wsgi.WSGIRequest
    :param pk: Composition id
    :type pk: int
    :return: Dictionary containing composition attributes
    :rtype: dict
    """
    if request.method != "GET":
        return Http404()

    composition = Composition.objects.get(pk=pk)
    if not composition.has_access(request.user):
        return HttpResponseForbidden()

    attributes = composition.get_full_attributes()

    return JsonResponse(attributes)


def comment_get(request):
    if not request.is_ajax() or request.method != "GET":
        return Http404()

    composition = Composition.objects.get(pk=request.GET['composition'])
    if not composition or not composition.has_access(request.user):
        return Http404()

    comments = Comment.objects.filter(composition=composition,
                                      bar=int(request.GET['bar'])).order_by('time')
    comments = [{   "commenter": str(comment.commenter),
                    "time": comment.time.isoformat(),
                    "comment": str(comment.comment),
                } for comment in comments]
    return JsonResponse({'comments': comments})
