from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UrlsFiles

class FileUploadTestCase(APITestCase):
    
    def setUp(self):
        # Creating a sample text file for testing
        self.test_file_content = "https://example.com\nhttps://another-example.com\nhttps://github.com"
        self.test_file = {
            'file': ('urls.txt', self.test_file_content, 'text/plain')
        }
        self.upload_url = reverse('file-upload')
        self.urls_get_url = reverse('file-upload')

    def test_upload_file(self):
        """Test that the file can be uploaded and URLs extracted."""
        # Post the file
        response = self.client.post(self.upload_url, self.test_file, format='multipart')
        
        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Assert that 3 URLs were saved
        self.assertEqual(UrlsFiles.objects.count(), 3)
        
        # Assert that the URLs match what we uploaded
        expected_urls = ["https://example.com", "https://another-example.com", "https://github.com"]
        saved_urls = UrlsFiles.objects.values_list('urls', flat=True)
        self.assertListEqual(list(saved_urls), expected_urls)

    def test_get_urls(self):
        """Test retrieving URLs after uploading."""
        # First, upload the file to populate the database
        self.client.post(self.upload_url, self.test_file, format='multipart')
        
        # Now test the GET request to retrieve URLs
        response = self.client.get(self.urls_get_url)
        
        # Assert that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert that the returned data matches the saved URLs
        expected_data = [
            {"urls": "https://example.com"},
            {"urls": "https://another-example.com"},
            {"urls": "https://github.com"}
        ]
        self.assertEqual(response.json(), expected_data)

    def test_upload_empty_file(self):
        """Test that an error is raised if no file is uploaded."""
        response = self.client.post(self.upload_url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'No file provided')
