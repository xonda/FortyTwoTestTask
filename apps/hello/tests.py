from django.test import TestCase

from django.core.urlresolvers import reverse
from django.test import Client
from .models import Contacts

# Create your tests here.

client = Client()

class SomeTests(TestCase):
    def test_math(self):
        "put docstrings in your tests"
        assert(2 + 2 == 4)

class MainPageTest(TestCase):
    def test_home_page(self):
        """
        test if home page returns 200 ok
        """
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
