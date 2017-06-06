from django.test import Client, TestCase, RequestFactory
from django.urls import reverse

from intune import views
from intune.models import Composition, User, Profile


class ViewTests(TestCase):
    u_names = ['u1', 'u2', 'u3']
    pw = 'password123'
    client = Client()
    users = []
    profiles = []

    def setUp(self):
        for i in range(3):
            self.users.append(User.objects.create(username=self.u_names[i]))
            self.users[i].set_password(self.pw)
            self.users[i].save()
            self.profiles.append(Profile.objects.create(user=self.users[i]))

        self.composition = Composition.objects.create(owner=self.profiles[1],
                                                      title="song")
        self.composition.users.add(self.profiles[0])
        self.composition.users.add(self.profiles[2])
        self.user0_composition = Composition.objects.create(owner=self.profiles[0],
                                                            title="song1")

    def test_can_view_owned_compositions(self):
        login = self.client.login(username=self.u_names[0], password=self.pw)
        self.assertTrue(login)
        pk = self.composition.id
        response = self.client.get(reverse('intune:song', args=[pk]))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_cannot_view_compositions_not_owned_or_shared(self):
        login = self.client.login(username=self.u_names[1], password=self.pw)
        self.assertTrue(login)
        pk = self.user0_composition.id
        response = self.client.get(reverse('intune:song', args=[pk]))
        self.assertEqual(response.status_code, 404)
        self.client.logout()
