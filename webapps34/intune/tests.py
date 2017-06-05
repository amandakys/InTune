from django.test import Client, TestCase, RequestFactory
from django.urls import reverse

from intune import views
from intune.models import Composition, User, Profile


class ViewTests(TestCase):
    u_name1 = 'my_username1'
    u_name2 = 'my_username2'
    pw = 'password123'
    client = Client()

    def setUp(self):
        self.factory = RequestFactory()
        self.test_user1 = User.objects.create(username=self.u_name1, password=self.pw)
        self.test_user2 = User.objects.create(username=self.u_name2, password=self.pw)
        test_profile1 = Profile.objects.create(user=self.test_user1)
        test_profile2 = Profile.objects.create(user=self.test_user2)
        self.composition = Composition.objects.create(owner=test_profile2, title="song")
        self.composition.users.add(test_profile1)
        self.user1_composition = Composition.objects.create(owner=test_profile1, title="song1")

    def test_can_view_owned_compositions(self):
        pk = self.composition.id
        request = self.factory.get(reverse('intune:song', args=[pk]))
        request.user = self.test_user1
        response = views.MusicScore.as_view()(request, pk=pk)
        self.assertEqual(response.status_code, 200)


