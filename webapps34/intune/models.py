from django.db import models
from django.contrib.auth.models import User
from json import dumps, loads


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Composition(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(Profile, related_name='owner', on_delete=models.CASCADE)
    users = models.ManyToManyField(Profile, blank=True)
    # data = models.BinaryField()
    data = models.CharField(max_length=10000, blank=True)
    lastEdit = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def get_bar_list(self):
        return self.get_data()['bars']

    def get_data(self):
        try:
            return loads(self.data)
        except ValueError:
            return {'bars': []}

    def has_access(self, user):
        return self.owner.user == user or user.profile in self.users.all()

    def add_bar(self):
        data = self.get_data()
        data['bars'].append(":w ##")
        self.data = dumps(data)
        self.save()

    def set_bar(self, bar_id, contents):
        data = self.get_data()
        data['bars'][bar_id] = contents
        self.data = dumps(data)
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    commenter = models.ForeignKey(Profile)
    time = models.DateTimeField(auto_now_add=True)
    composition = models.ForeignKey(Composition)
    bar = models.PositiveIntegerField()
    comment = models.CharField(max_length=255)

    def __str__(self):
        return self.comment
