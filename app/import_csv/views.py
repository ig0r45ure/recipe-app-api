from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UploadFileForm
from .apps import handle_uploaded_file


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('app_name:upload'))
    else:
        form = UploadFileForm()
    return render(request, 'import_csv/upload.html', {'form': form})
