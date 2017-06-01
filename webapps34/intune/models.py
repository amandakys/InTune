from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Composition(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(Profile, related_name='owner', on_delete=models.CASCADE)
    users = models.ManyToManyField(Profile, blank=True)
    # data = models.BinaryField()
    lastEdit = timezone.now()
    created = timezone.now()

    def output_to_json(self):
        return \
            '''{
      clef: ["treble", "bass"],
      duration: "w",
      keys: ["C_2", "G_2", "Bb_2", "E_3", "Bb-3", "E-4", "G-4"],
      add_right_double_line: true,
    }'''

    def __str__(self):
        return self.title
