from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import UrlsFiles

class UrlsFilesAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.upload_url = '/upload/'  # Adjust this URL to match your actual endpoint
        self.urls_get_url = '/urls/'   # Adjust this URL to match your actual endpoint

    def test_upload_file_and_extract_urls(self):
        # Create a sample text file with URLs
        test_file_content = "Here are some URLs: https://example.com and http://another-example.com"
        test_file = self.create_text_file(test_file_content)

        # Upload the file
        response = self.client.post(self.upload_url, {'file': test_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if URLs are saved in the database
        urls = UrlsFiles.objects.all()
        self.assertEqual(urls.count(), 2)  # There are 2 URLs in the test file

    def test_get_urls(self):
        # Set up data by uploading a file first
        self.test_upload_file_and_extract_urls()

        # Get the URLs
        response = self.client.get(self.urls_get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Validate the response data
        urls = response.json()
        self.assertEqual(len(urls), 2)  # Should match the number of URLs uploaded

    def create_text_file(self, content):
        """Helper method to create a text file in memory"""
        from io import BytesIO
        return BytesIO(content.encode('utf-8'))

