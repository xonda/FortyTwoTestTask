from django.test import TestCase
from selenium import webdriver


class RequestsPageTests(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_requests_page_content(self):
        """
        Test requests page contents
        """
        self.driver.get("http://127.0.0.1:8000/requests")
        self.assertIn('Requests', self.driver.title)
        tbody = self.driver.find_element_by_tag_name("tbody")
        self.assertIn(' /requests ', tbody.text)
        self.assertIn(' GET ', tbody.text)
        self.assertIn(' {} ', tbody.text)

    def tearDown(self):
        self.driver.close()
