from django.test import TestCase
from selenium import webdriver


class RequestsPageTests(TestCase):
    def test_requests_page_content(self):
        """
        Test content added with ajax
        """
        driver = webdriver.Chrome()
        driver.get("http://127.0.0.1:8000/requests")
        self.assertIn('Requests', driver.title)
        tbody = driver.find_element_by_tag_name("tbody")
        self.assertIn(' /requests ', tbody.text)
        self.assertIn(' GET ', tbody.text)
        self.assertIn(' {} ', tbody.text)
        driver.close()
