from django.http import JsonResponse
from rest_framework.views import APIView
from .serializer import UrlsFilesSerializer
from .models import UrlsFiles
import re

class FileUpload(APIView):
    def extract_urls(self, text):
        url_pattern = r'https?://[^\s]+'
        return re.findall(url_pattern, text) 

    def post(self, request):
        if 'file' not in request.data:
            return JsonResponse({"error": "No file provided"}, status=400)

        uploaded_file = request.data['file']
        UrlsFiles.objects.all().delete()

        try:
            file_contents = uploaded_file.read().decode('utf-8')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        urls = self.extract_urls(file_contents)

        for url in urls:
            serializer = UrlsFilesSerializer(data={'urls': url})
            if serializer.is_valid():
                serializer.save()
            else:
                return JsonResponse(serializer.errors, status=400)

        # all_entries = UrlsFiles.objects.all()
        # all_entries_list = [{"id": entry.id, "urls": entry.urls, "uploaded_at": entry.uploaded_at} for entry in all_entries]

        return JsonResponse(status=201)

class UrlsGet(APIView):
    def get(self, request):
        all_entries = UrlsFiles.objects.all()
        serializer = UrlsFilesSerializer(all_entries, many=True)
        return JsonResponse(serializer.data, safe=False) 