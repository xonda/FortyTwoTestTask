# -*- coding: utf-8 -*-

import os.path
import subprocess
from datetime import date
from StringIO import StringIO
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.test import TestCase
from django.test import Client
from .models import Info, WebRequest, DatabaseLog


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
        self.assertIn('<h4>Contacts</h4>', response.content)

    def test_home_empty_db(self):
        """
        Test home page when the db is empty
        """
        Info.objects.all().delete()
        response = client.get(reverse('home'))
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
        self.assertIn('John', response.content)
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
    fixtures = ['webrequest.json']

    def test_page_is_available(self):
        """
        Test if requests page is available
        """
        response = client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)

    def test_upd_request_not_ajax(self):
        """
        Test update request with not ajax request
        """
        response = client.get(reverse('upd_requests'))
        self.assertEqual(response.content, 'Not ajax request')

    def test_upd_requests_ajax_and_not_empty(self):
        """
        Test update requests with ajax request, db not empty
        """
        response = client.get(reverse('upd_requests'),
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('127.0.0.1:8000', response.content)
        self.assertIn('hello.webrequest', response.content)

    def test_upd_requests_ajax_and_empty(self):
        """
        Test update requests with ajax request, db empty
        """
        WebRequest.objects.all().delete()
        response = client.get(reverse('upd_requests'),
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('No records in database', response.content)


class RequestsMiddlewareTest(TestCase):
    def test_middleware_saves_requests(self):
        """
        Test if middleware saves requests in database
        """
        client.get(reverse('home'))
        query = WebRequest.objects.get(pk=1)
        self.assertTrue(query)
        self.assertEqual(query.path, '/')
        self.assertEqual(query.host, 'testserver')


class EditInfoPageTests(TestCase):
    fixtures = ['superuser.json']

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

    def test_post_is_valid(self):
        """
        Test when POST is valid
        """
        client.login(username='admin', password='admin')
        response = client.post(reverse('edit_info'),
               {"bio": "Several words",
                "surname": "Lykov", "name": "Viktor",
                "dob": "1986-01-22", "photo": "",
                "other": "ICQ: 228339308",
                "skype": "testerotuco",
                "csrfmiddlewaretoken": "OjJ63FVRl5o3vnjcLr610rGZ3NgYPiMv",
                "jabber": "xonda@khavr.com",
                "email": "yamabushi@ukr.net"},
               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual('Changes have been saved', response.content)

    def test_post_is_invalid(self):
        """
        Test when POST is Invalid
        """
        client.login(username='admin', password='admin')
        response = client.post(reverse('edit_info'),
               {"bio": "",
                "surname": "Lykov", "name": "Viktor",
                "dob": "1986", "photo": "",
                "other": "ICQ: 228339308",
                "skype": "testerotuco",
                "csrfmiddlewaretoken": "OjJ63FVRl5o3vnjcLr610rGZ3NgYPiMv",
                "jabber": "xonda@khavr.com",
                "email": "yamabushiukr.net"},
               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('This field is required', response.content)
        self.assertIn('Enter a valid email address', response.content)
        self.assertIn('invalid date format', response.content)


class CusotmCommandsTest(TestCase):
    fixtures = ['superuser.json']
    today = date.today().strftime('%d-%m-%Y')
    filename = today + '.dat'
    out = StringIO()
    out_err = StringIO()
    call_command('list_models', stdout=out, stderr=out_err)
    subprocess.call('./list-models.sh')

    def test_list_models_command(self):
        self.assertIn('Info - 3 records', self.out.getvalue())
        self.assertIn('User - 1 records', self.out.getvalue())
        self.assertIn('error: Info - 3 records', self.out_err.getvalue())
        self.assertIn('error: User - 1 records', self.out_err.getvalue())

    def test_list_model_save_file(self):
        self.assertTrue(os.path.isfile(self.filename))

    def test_list_model_file_contents(self):
        with open(self.filename, 'rb') as f:
            file_content = f.read()
            self.assertIn('error: User - 1 records', file_content)
            self.assertIn('error: Info - 3 records', file_content)


class SignalProcessorTest(TestCase):
    def test_delete_object_signal(self):
        Info.objects.all()[0].delete()
        record = DatabaseLog.objects.latest('date')
        self.assertEqual('Info', record.model)
        self.assertEqual('delete', record.action)

    def test_edit_object_signal(self):
        obj = Info.objects.all()[0]
        obj.name = 'Teddy'
        obj.save()
        record = DatabaseLog.objects.latest('date')
        self.assertEqual('Info', record.model)
        self.assertEqual('edit', record.action)

    def test_create_object_signal(self):
        obj = Info(name='Tom', surname='Waits', dob='1986-01-22',
                   bio='BlahBlah', email='tw@mail.com',
                   jabber='tomw', skype='tomw', other='foo')
        obj.save()
        record = DatabaseLog.objects.latest('date')
        self.assertEqual('Info', record.model)
        self.assertEqual('create', record.action)

    def test_edit_signal_not_doubled(self):
        DatabaseLog.objects.all().delete()
        obj = Info.objects.all()[0]
        obj.name = 'Teddy'
        obj.save()
        self.assertNotEqual(2, DatabaseLog.objects.all().count())

    def test_delete_signal_not_doubled(self):
        DatabaseLog.objects.all().delete()
        obj = Info.objects.all()[0]
        obj.name = 'Teddy'
        obj.photo = 'img.png'
        obj.save()
        self.assertNotEqual(2, DatabaseLog.objects.all().count())
