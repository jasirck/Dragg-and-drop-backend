from rest_framework import serializers
from .models import UrlsFiles

class UrlsFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlsFiles
        fields = '__all__'
