from django.test import SimpleTestCase, Client


class ViewTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_get_composition_title(self):
        pass

