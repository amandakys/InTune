import datetime
from django.test import Client, TestCase, RequestFactory
from django.urls import reverse

from intune import views
from intune.models import Composition, User, Profile


class ViewTests(TestCase):
    u_names = ['u1', 'u2', 'u3']
    client = Client()
    users = []
    profiles = []

    def setUp(self):
        for i in range(3):
            self.users.append(User.objects.create(username=self.u_names[i]))
            self.users[i].save()
            self.profiles.append(Profile.objects.create(user=self.users[i]))

        self.composition = Composition.objects.create(owner=self.profiles[1],
                                                      title="song")
        self.composition.users.add(self.profiles[0])
        self.composition.users.add(self.profiles[2])
        self.user0_composition = Composition.objects.create(owner=self.profiles[0],
                                                            title="song1")

    def test_can_view_owned_compositions(self):
        login = self.client.force_login(self.users[0])
        pk = self.composition.id
        response = self.client.get(reverse('intune:song', args=[pk]))
        self.assertEqual(response.context['composition'], self.composition)
        self.client.logout()

    def test_cannot_view_compositions_not_owned_or_shared(self):
        login = self.client.force_login(self.users[1])
        pk = self.user0_composition.id
        response = self.client.get(reverse('intune:song', args=[pk]))
        if response.context:
            self.assertIsNone(response.context['composition'])
        else:
            self.assertFalse("song1" in str(response.content))
        self.client.logout()

    def test_composition_list_no_duplicates(self):
        login = self.client.force_login(self.users[1])
        response = self.client.get(reverse('intune:index'))
        cl = response.context['composition_list']
        self.assertEqual(len(cl), len(cl.distinct()))
        self.client.logout()

    def test_composition_list_ordered(self):
        login = self.client.force_login(self.users[1])
        response = self.client.get(reverse('intune:index'))
        cl = response.context['composition_list']
        self.assertEqual(len(cl), len(cl.order_by("-lastEdit")))
        self.client.logout()

    def test_composition_last_edit_no_future(self):
        login = self.client.force_login(self.users[1])
        response = self.client.get(reverse('intune:index'))
        composition = response.context['composition_list'][0]
        self.assertTrue(composition.lastEdit <=
                        datetime.datetime.now(tz=composition.lastEdit.tzinfo))
        self.client.logout()
