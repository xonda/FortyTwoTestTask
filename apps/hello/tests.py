from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Info, WebRequest

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
        self.assertIn('<p>Contacts</p>', response.content)

    def test_home_page_empty_db(self):
        """
        test home page when the db is empty
        """
        Info.objects.all().delete()
        response = client.get(reverse('home'))
        self.assertIn('<div class="block">', response.content)
        self.assertIn('id="nodata"', response.content)


class RequestsPageTests(TestCase):
    def test_page_is_available(self):
        """
        Test if requests page is availlable
        """
        response = client.get('/requests')
        self.assertEqual(response.status_code, 200)

    def test_upd_request_not_ajax(self):
        """
        Test update request with not ajax request
        """
        response = client.get('/upd_requests')
        self.assertEqual(response.content, 'Not ajax request')

    def test_upd_requests_ajax(self):
        """
        Test update requests with ajax request
        """
        response = client.get('/upd_requests',
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('hello.webrequest', response.content)
        self.assertIn('"host": "testserver"', response.content)

    def test_requests_content(self):
        """
        Test content served by requests view
        """
        response = client.get('/requests')
        self.assertIn('Host', response.content)
        self.assertIn('User Agent', response.content)
        self.assertIn('Ajax', response.content)
        self.assertIn('Requests | Site Name', response.content)


class RequestsMiddlewareTest(TestCase):
    def test_middleware_saves_requests(self):
        """
        Test if middleware saves requests in database
        """
        client.get('/')
        query = WebRequest.objects.get(pk=1)
        self.assertTrue(query)
        self.assertEqual(query.path, '/')
        self.assertEqual(query.host, 'testserver')
