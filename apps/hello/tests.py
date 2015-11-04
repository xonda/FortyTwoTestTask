from django.test import TestCase

from django.core.urlresolvers import reverse
from django.test import Client
from .models import Info

client = Client()


class MainPageTest(TestCase):
    def test_home_page(self):
        """
        test if home page returns 200 ok
        """
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class InfoModelTest(TestCase):
    def setUp(self):
        Info.objects.create(name="John",
                            surname="Doe",
                            dob="1975-05-04",
                            bio="Biography",
                            email="mail@mail.com",
                            jabber="ololo@xmmp.com",
                            skype="johndoe",
                            other="other")

    def test_model(self):
        john = Info.objects.get(name="John")
        self.assertEqual(john.surname, 'Doe')
        self.assertEqual(john.skype, 'johndoe')
        self.assertEqual(john.other, 'other')
