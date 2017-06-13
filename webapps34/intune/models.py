from django.db import models
from django.contrib.auth.models import User
from json import dumps, loads


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Composition Attributes
# -> data: JSON String
#       {'bars':
#           < List of bars in the following format:
#               {'options': <string for options>,
#                'tabstave': <string for tabstave>,
#                'clef': <"treble", "bass" or "none">,
#                'time_sig': <string of form: "<num>/<num>">,
#                'notes': <string containing notes>
#               }
#           >
#       }
class Composition(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(Profile, related_name='owner',
                              on_delete=models.CASCADE)
    users = models.ManyToManyField(Profile, blank=True)
    # data = models.BinaryField()
    data = models.CharField(max_length=10000, blank=True)
    lastEdit = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def get_full_attributes(self):
        attributes = {'title': self.title,
                      'owner': self.owner.user.username,
                      'users': [str(p) for p in self.users.all()]}
        attributes.update(self.get_data())
        return attributes

    def get_bar_list(self):
        return self.get_data()['bars']

    def get_data(self):
        try:
            return loads(self.data)
        except ValueError:
            return {'bars': []}

    def has_access(self, user):
        return self.owner.user == user or user.profile in self.users.all()

    def append_bar(self, contents):
        data = self.get_data()
        data['bars'].append(contents)
        self.data = dumps(data)
        self.save()

    def set_bar(self, bar_id, contents):
        data = self.get_data()
        data['bars'][bar_id] = contents
        self.data = dumps(data)
        self.save()

    def delete_last_bar(self):
        data = self.get_data()
        bar_count = len(data['bars'])
        if bar_count > 0:
            del data['bars'][-1]
            self.data = dumps(data)
            self.save()
            Comment.objects.filter(composition=self, bar=bar_count-1).delete()
        return bar_count - 1

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    room = models.ForeignKey(Composition, related_name='room', on_delete=models.CASCADE)
    msg = models.CharField(max_length=200)
    sender = models.ForeignKey(Profile, related_name='sender', default=1)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.msg


class Comment(models.Model):
    commenter = models.ForeignKey(Profile)
    time = models.DateTimeField(auto_now_add=True)
    composition = models.ForeignKey(Composition)
    bar = models.PositiveIntegerField()
    comment = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.comment


class Notification(models.Model):
    recipients = models.ManyToManyField(Profile, blank=False)
    msg = models.CharField(max_length=10000)
    sent_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    composition = models.ForeignKey(Composition)

    def __str__(self):
        return self.msg
