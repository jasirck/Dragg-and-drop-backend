from django.db import models

class UrlsFiles(models.Model):
    # file = models.FileField(upload_to='uploads/')
    urls = models.TextField(default="default_url")
    content = models.TextField(default="No data")
    uploaded_at = models.DateTimeField(auto_now_add=True)
