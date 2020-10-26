import os
import uuid
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.generic import View

from phonebook.settings import MEDIA_ROOT
from .forms import ContactForm
from .tasks import upload_file


class ContactUploadView(View):
    form_class = ContactForm

    def get(self, request):
        form = self.form_class()
        template_name = 'index.html'
        return render(request, template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        template_name = 'upload_done.html'
        if form.is_valid():
            file_name_inmemory = request.FILES['to_be_uploaded']
            t = os.path.splitext(file_name_inmemory.name)
            file_name = f'{t[0]}_{uuid.uuid4().hex}{t[1]}'
            fs = FileSystemStorage()
            f = fs.save(file_name, file_name_inmemory)
            messages.add_message(request, messages.INFO,
                                 'Thanks for uploading, '
                                 'it is underway!')
            upload_file.delay(os.path.join(MEDIA_ROOT, f))
            return render(request, template_name)
        return render(request, template_name, {'form': form})
