from django.db import models

class UrlsFiles(models.Model):
    # file = models.FileField(upload_to='uploads/')
    urls = models.TextField(default="default_url")
    uploaded_at = models.DateTimeField(auto_now_add=True)
