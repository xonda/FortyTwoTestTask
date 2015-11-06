from django.test import TestCase

from django.core.urlresolvers import reverse
from django.test import Client
from .models import Info

client = Client()


class MainPageTest(TestCase):
    def test_home_page_alive(self):
        """
        test if home page returns 200 ok
        """
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)

    def test_home_page_content(self):
        """
        test if home page shows content
        """
        response = client.get(reverse('home'))
        self.assertIn('<div class="block">', response.content)
        self.assertIn('"/static/css/main.css"', response.content)
        self.assertIn('<p>Name:', response.content)

    def test_home_page_empty_db(self):
        Info.objects.all().delete()
        response = client.get(reverse('home'))
        self.assertIn('<div class="block">', response.content)
        self.assertIn('id="nodata"', response.content)
        print response.content


class InfoModelTest(TestCase):
    fixtures = ['initial_data.json']

    def test_model(self):
        """
        test info model
        """
        info = Info.objects.get()
        self.assertEqual(info.surname, 'Lykov')
        self.assertEqual(info.skype, 'testerotuco')
