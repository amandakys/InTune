from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Composition(models.Model):
    title = models.CharField(max_length = 200)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    #users = models.ManyToManyField(Profile)
    # data = models.BinaryField()
    # lastEdit = models.DateTimeField()
    # created = models.DateTimeField()

# class Segment(models.Model):
#     composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
