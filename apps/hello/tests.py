from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
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
        self.assertIn('<p>Name:', response.content)

    def test_home_page_empty_db(self):
        """
        test home page when the db is empty
        """
        Info.objects.all().delete()
        response = client.get(reverse('home'))
        self.assertIn('<div class="block">', response.content)
        self.assertIn('id="nodata"', response.content)


class InfoModelTest(TestCase):
    fixtures = ['initial_data.json']

    def test_model(self):
        """
        test info model
        """
        info = Info.objects.get()
        self.assertEqual(info.surname, 'Lykov')
        self.assertEqual(info.skype, 'testerotuco')


class AdminSiteTests(TestCase):
    fixtures = ['username.json']

    def test_adminsite_login_redirect(self):
        """
        test if admin page redirects to login if logged out
        """
        response = client.get('/admin')
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, '/admin/', status_code=301)

    def test_admin_logged_in(self):
        """
        test login to admin page
        """
        self.user = User.objects.get()
        self.assertEqual(str(self.user), 'admin')
        client.login(username='admin', password='admin')
        self.response = client.get('/admin/')
        self.assertIn("Site administration", self.response.content)
        self.assertIn('<a href="/admin/hello/info/">Infos</a>',
                      self.response.content)

    def test_admin_Info_registered(self):
        """
        test if Info class registered on admin site
        """
        self.user = User.objects.get()
        self.assertEqual(str(self.user), 'admin')
        client.login(username='admin',
                     password='admin')
        self.response = client.get('/admin/')
        self.assertIn('<a href="/admin/hello/info/">Infos</a>',
                      self.response.content)


class RequestsPageTests(TestCase):
    def test_page_is_available(self):
        response = client.get('/requests')
        self.assertEqual(response.status_code, 200)

    def test_upd_request_not_ajax(self):
        response = client.get('/upd_requests')
        self.assertEqual(response.content, 'Not ajax request')

    def test_upd_requests_ajax(self):
        response = client.get('/upd_requests', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('hello.webrequest', response.content)

    def test_upd_request_db_empty(self):
        WebRequest.objects.all().delete()
        response = client.get('/upd_requests', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content, 'No records in database')






class RequestsMiddlewareTest(TestCase):
    def test_middleware_saves_requests(self):
        client.get('/')
        query = WebRequest.objects.get(pk=1)
        self.assertTrue(query)
        self.assertEqual(query.path, '/')















