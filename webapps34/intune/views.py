from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.views import generic

from .models import Composition, Profile
from dal import autocomplete


class CompositionList(generic.ListView):
    def get_queryset(self):
        return Composition.objects.filter(Q(owner__user=self.request.user) |
                                          Q(users__user=self.request.user)
                                          ).distinct().order_by("-lastEdit")


class CompositionDetail(generic.DetailView):
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # TODO: add error message
            return redirect("intune:index")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_queryset(self):
        return Composition.objects.filter(Q(owner__user=self.request.user) |
                                          Q(users__user=self.request.user)
                                          ).distinct()


class CompositionCreate(generic.edit.CreateView):
    model = Composition
    fields = ["title", "users"]
    success_url = reverse_lazy("intune:index")

    def get_form(self):
        form = super(CompositionCreate, self).get_form()
        form.fields['users'].widget = autocomplete.ModelSelect2Multiple(url='intune:profile-autocomplete')
        form.fields['users'].queryset = Profile.objects.exclude(user__id=self.request.user.id)
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
    fields = ['data', 'users']

    def get_form(self):
        form = super(CompositionEdit, self).get_form()
        form.fields['users'].widget = autocomplete.ModelSelect2Multiple(url='intune:profile-autocomplete')
        form.fields['users'].queryset = Profile.objects.exclude(user__id=self.request.user.id)
        return form

    def get_queryset(self):
        return Composition.objects.filter(Q(owner__user=self.request.user) |
                                          Q(users__user=self.request.user)
                                          ).distinct()

    def get_success_url(self):
        return reverse_lazy("intune:song_edit", args=[self.kwargs['pk']])

    def form_valid(self, form):
        composition = form.save(commit=False)
        composition.save()
        users = form.cleaned_data['users']
        composition.users.clear()
        for u in users:
            composition.users.add(u)
        form.save_m2m()
        return super(CompositionEdit, self).form_valid(form)


class ProfileAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Profile.objects.none()
        qs = Profile.objects.exclude(user__id=self.request.user.id)
        if self.q:
            qs = qs.filter(user__username__istartswith=self.q)
        return qs
