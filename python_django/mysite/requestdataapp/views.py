from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    MAX_FILE_SIZE = 1 * 1024 * 1024

    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]
        if myfile.size > MAX_FILE_SIZE:
            raise Exception("You cant load file that more than 1 MB")

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print("Saved file:", filename)

    return render(request, "requestdataapp/file_upload.html")