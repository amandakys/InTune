from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from hamcrest import assert_that, has_entries

from .models import Composition, Profile


class CompositionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="TestUser")
        self.profile = Profile.objects.create(user=self.user)
        self.composition = Composition.objects.create(
            title="Test Composition",
            owner=self.profile)

    def test_get_composition_attribute(self):
        expected = {'title': "Test Composition",
                    'owner': "TestUser",
                    'users': []}

        self.client.force_login(self.user)
        pk = self.composition.id
        response = self.client.get(
            reverse('intune:composition_attribute', args=[pk]))
        test = response.json()

        assert_that(test, has_entries(expected))
