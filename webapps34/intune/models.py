import select2.fields
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Composition(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(Profile, related_name='owner', on_delete=models.CASCADE)
    users = models.ManyToManyField(Profile, blank=True)

    # users = select2.fields.ManyToManyField(Profile,
    #     ajax=True,
    #     search_field=lambda q: Q(user__icontains=q),
    #     sort_field='position',
    #     js_options={'quiet_millis': 200})

    # users = select2.fields.ManyToManyField(Profile, through='SharedUsers', limit_choices_to=models.Q(active=True),
    #                                ajax=True, search_field='name', overlay="Choose shared users...",
    #                                js_options={'quiet_millis': 200, },
    #                                on_delete=models.CASCADE)
    # data = models.BinaryField()
    data = models.CharField(max_length=10000, blank=True)
    lastEdit = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def get_default_string(self):
        return 'options space=20 tab-stems=true stave-distance=40 tab-stem-direction=down\n' \
               'tabstave notation=true key=C time=4/4 tablature=false'

    def __str__(self):
        return self.title
