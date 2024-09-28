
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.FileUpload.as_view(), name='file-upload'),
    path('urls/', views.UrlsGet.as_view(), name='file-upload'),
    path('clear/', views.delete_all, name='delete_all'),
]
