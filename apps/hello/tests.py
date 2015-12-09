# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Info, WebRequest

client = Client()


class MainPageTest(TestCase):
    def test_home_page_alive(self):
        """
        Test if home page returns 200 ok
        """
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)

    def test_home_page_content(self):
        """
        Test if home page shows content
        """
        response = client.get(reverse('home'))
        self.assertIn('<div class="block">', response.content)
        self.assertIn('"/static/css/main.css"', response.content)
        self.assertIn('<p>Contacts</p>', response.content)

    def test_home_empty_db(self):
        """
        Test home page when the db is empty
        """
        Info.objects.all().delete()
        response = client.get(reverse('home'))
        self.assertIn('<div class="block">', response.content)
        self.assertIn('id="nodata"', response.content)
        self.assertIn('id="nodata"', response.content)

    def test_unicode(self):
        """
        Test page when db record has Unicode
        """
        Info.objects.filter(pk__in=[1, 4]).delete()
        response = client.get(reverse('home'))
        self.assertIn('Иван', response.content)

    def test_1_db_record(self):
        """
        Test page when there is one db record
        """
        Info.objects.filter(pk__in=[1, 3]).delete()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Name', response.content)
        self.assertNotIn('id="nodata', response.content)

    def test_2_or_more_db_records(self):
        """
        Test home page when there are 2 or more db records
        """
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('id="nodata', response.content)
        self.assertContains(response, 'Viktor')


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
        self.assertIn('No records in database', response.content)

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


class EditInfoPageTests(TestCase):
    fixtures = ['username.json']

    def test_edit_page_available(self):
        """
        Test if edit info page redirects to login
        """
        response = client.get(reverse('edit_info'))
        self.assertEqual(response.status_code, 302)

    def test_edit_page_available_logged_in(self):
        """
        Test if edit info page returns 200 ok when logged in
        """
        client.login(username='admin', password='admin')
        response = client.get(reverse('edit_info'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)

    def test_edit_info_empty_db(self):
        """
        Test edit page when the db is empty
        """
        Info.objects.all().delete()
        client.login(username='admin', password='admin')
        response = client.get(reverse('edit_info'))
        self.assertEqual(response.content, 'No records in database')

    def test_first_object_data_loaded(self):
        """
        Test if first object data is loaded to form
        """
        record = Info.objects.all()[0]
        client.login(username='admin', password='admin')
        response = client.get(reverse('edit_info'))
        self.assertIn(record.name, response.content)
        self.assertIn(record.skype, response.content)
        self.assertIn(record.email, response.content)

    def test_unicode(self):
        """
        Test edit info page when db record has Unicode
        """
        Info.objects.filter(pk__in=[1, 4]).delete()
        client.login(username='admin', password='admin')
        response = client.get(reverse('edit_info'))
        self.assertIn('Иван', response.content)

    def test_edit_with_1_db_record(self):
        """
        Test edit page when there is one db record
        """
        Info.objects.filter(pk__in=[1, 3]).delete()
        record = Info.objects.all()[0]
        client.login(username='admin', password='admin')
        response = client.get(reverse('edit_info'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(record.name, response.content)
        self.assertNotIn('No records in database', response.content)
