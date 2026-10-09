from django.urls import path

from .views import handle_file_upload
app_name = 'requestdataapp'

urlpatterns = [
    path("upload_file", handle_file_upload, name="upload"),
]
