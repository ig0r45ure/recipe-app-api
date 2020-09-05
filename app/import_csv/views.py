from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UploadFileForm
from .apps import handle_uploaded_file

from core.models import OrgUnit

def select_upload_file(request):
    uploaded_data = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        uploaded_data.update({'Request method': request.method})
        if form.is_valid():
            uploaded_data.update({'Check': form.is_valid()})
            handle_uploaded_file(request.FILES['file'], uploaded_data)
    else:
        form = UploadFileForm()
        uploaded_data.update({'Select File': 'Nie powinno mnie tu być'})
    return render(
            request,
            'import_csv/upload_data.html',
            {'form': form, 'uploaded_data': uploaded_data}
            )

"""
def org_unit_upload(request)
    # declaring template
    template = "org_unit_upload.html"
    data = OrgUnit.objects.all()
# prompt is a context variable that can have different values      depending on their context
    prompt = {
        'filenames':'Order of the CSV should be name, acronym, is_HQUnit',
        'org_units': data
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Profile.objects.update_or_create(
        name=column[0],
        email=column[1],
        address=column[2],
        phone=column[3],
        profile=column[4]
    )
    context = {}
return render(request, template, context)
"""
