from django.core.urlresolvers import reverse
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class RequestsPageTests(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_requests_page_content(self):
        """
        Test requests page contents
        """
        self.driver.get('http://127.0.0.1:8000' + reverse('requests'))
        self.assertIn('Requests', self.driver.title)
        tbody = self.driver.find_element_by_tag_name("tbody")
        self.assertIn(' /requests ', tbody.text)
        self.assertIn(' GET ', tbody.text)
        self.assertIn(' {} ', tbody.text)
        self.assertIn(" AnonymousUser 0", tbody.text)
        req_sort = self.driver.find_element_by_id("req-sort")
        req_sort.click()
        self.assertNotIn(" AnonymousUser 0", tbody.text)

    def tearDown(self):
        self.driver.close()


class HomePageTests(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_edit_link_tag(self):
        """
        Test if edit_link tag drives to poject admin page
        """
        self.driver.get('http://127.0.0.1:8000' + reverse('login'))
        elem = self.driver.find_element_by_name("username")
        elem.send_keys("admin")
        elem = self.driver.find_element_by_name("password")
        elem.send_keys("admin" + Keys.RETURN)

        admin_link = self.driver.find_element_by_link_text("(admin)")
        admin_link.click()

        self.assertIn('Django site admin', self.driver.title)
        admin_body = self.driver.find_element_by_tag_name("body").text
        self.assertIn('Viktor', admin_body)
        self.assertIn('testerotuco@mail.ru', admin_body)
        jabber = self.driver.find_element_by_id('id_jabber')
        self.assertIn('xonda', jabber.get_attribute('value'))

    def tearDown(self):
        self.driver.close()
