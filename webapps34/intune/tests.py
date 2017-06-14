import datetime
from django.test import Client, TestCase
from django.urls import reverse

from .models import Composition, User, Profile


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
        self.client.force_login(self.users[0])
        pk = self.composition.id
        response = self.client.get(reverse('intune:song', args=[pk]))
        self.assertEqual(response.context['composition'], self.composition)
        self.client.logout()

    def test_cannot_view_compositions_not_owned_or_shared(self):
        self.client.force_login(self.users[1])
        pk = self.user0_composition.id
        response = self.client.get(reverse('intune:song', args=[pk]))
        if response.context and 'composition' in response.context:
            self.assertIsNone(response.context['composition'])
        else:
            self.assertFalse("song1" in str(response.content))
        self.client.logout()

    def test_composition_list_no_duplicates(self):
        self.client.force_login(self.users[1])
        response = self.client.get(reverse('intune:index'))
        cl = response.context['composition_list']
        self.assertEqual(len(cl), len(cl.distinct()))
        self.client.logout()

    def test_composition_list_ordered(self):
        self.client.force_login(self.users[1])
        response = self.client.get(reverse('intune:index'))
        cl = response.context['composition_list']
        self.assertEqual(len(cl), len(cl.order_by("-lastEdit")))
        self.client.logout()

    def test_composition_last_edit_no_future(self):
        self.client.force_login(self.users[1])
        response = self.client.get(reverse('intune:index'))
        composition = response.context['composition_list'][0]
        self.assertTrue(composition.lastEdit <=
                        datetime.datetime.now(tz=composition.lastEdit.tzinfo))
        self.client.logout()

    def test_composition_edit_permission(self):
        self.client.force_login(self.users[0])
        pk = self.composition.id
        response = self.client.get(reverse('intune:song_edit', args=[pk]))
        self.assertEqual(response.context['composition'], self.composition)
        pk = self.user0_composition.id
        response = self.client.get(reverse('intune:song_edit', args=[pk]))
        self.assertEqual(response.context['composition'], self.user0_composition)
        self.client.logout()

        self.client.force_login(self.users[2])
        response = self.client.get(reverse('intune:song_edit', args=[pk]))
        if response.context and 'composition' in response.context:
            self.assertIsNone(response.context['composition'])
        else:
            self.assertFalse("song1" in str(response.content))
        self.client.logout()


class CompositionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="TestUser")
        cls.profile = Profile.objects.create(user=cls.user)

        cls.shared_user = User.objects.create(username="Shared")
        cls.shared_profile = Profile.objects.create(user=cls.shared_user)

        cls.non_shared_user = User.objects.create(username="NotShared")
        cls.non_shared_profile = Profile.objects.create(user=cls.non_shared_user)

        cls.composition = Composition.objects.create(title="Test Composition",
                                                     owner=cls.profile)
        cls.composition.users.add(cls.shared_profile)

    def test_has_bar(self):
        self.assertTrue('bars' in self.composition.get_data())

    def test_bar_add_integrity(self):
        bar_list = self.composition.get_bar_list()
        self.composition.append_bar(":w ##")
        self.assertSequenceEqual(bar_list, self.composition.get_bar_list()[:-1])

    def test_has_access(self):
        self.assertTrue(self.composition.has_access(self.user))
        self.assertTrue(self.composition.has_access(self.shared_user))
        self.assertFalse(self.composition.has_access(self.non_shared_user))
