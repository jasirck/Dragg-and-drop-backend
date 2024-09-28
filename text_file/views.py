from django.http import JsonResponse
from rest_framework.views import APIView
from bs4 import BeautifulSoup
import requests
from .serializer import UrlsFilesSerializer
from .models import UrlsFiles
import re
from django.views.decorators.csrf import csrf_exempt


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
        saved_entries = []

        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                data = soup.get_text()
            except requests.RequestException as e:
                data = str(e)
                data = data.split("Error:")[-1].strip()
                # data = f"Error fetching content: {str(e)}"

            # Whether we successfully fetched content or not, we try to save the URL
            serializer = UrlsFilesSerializer(data={'urls': url, 'content': data})
            if serializer.is_valid():
                serializer.save()
                saved_entries.append({"url": url, "status": "success", "content": data})
            else:
                saved_entries.append({"url": url, "status": "error", "error": serializer.errors})

        return JsonResponse({'saved_entries': saved_entries}, status=201)


class UrlsGet(APIView):
    def get(self, request):
        all_entries = UrlsFiles.objects.all()
        serializer = UrlsFilesSerializer(all_entries, many=True)
        print(UrlsFiles.objects.all().count())
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def delete_all(request):
    UrlsFiles.objects.all().delete()
    return JsonResponse({"message": "All URLs deleted successfully."}, status=200)