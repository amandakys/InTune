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
    # data = models.BinaryField()
    lastEdit = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def output_to_json(self):
        return \
            '''{
              clef: "treble",
              voices: [
                { time: "4/4", notes: [
                  { duration: "h", keys: ["C", "Eb", "F", "A"] },
                  { duration: "h", keys: ["Bb", "D", "F", "A"] },
                  { barnote: true },
                  { duration: "q", keys: ["C", "Eb", "G", "Bb"] },
                  { duration: "q", keys: ["C", "Eb", "F", "A"] },
                  { duration: "h", keys: ["Bb", "D", "F", "A"] },
                  { barnote: true },
                  { duration: "q", keys: ["C", "Eb", "G", "Bb"] },
                  { duration: "q", keys: ["C", "Eb", "F", "A"] },
                  { duration: "h", keys: ["Bb", "D", "F", "A"] },
                  { barnote: true },
                  { duration: "q", keys: ["C", "Eb", "G", "Bb"] },
                  { duration: "q", keys: ["C", "Eb", "F", "A"] },
                  { duration: "h", keys: ["Bb", "D", "F", "A"] }
                ]}
              ]
            }'''

    def __str__(self):
        return self.title

