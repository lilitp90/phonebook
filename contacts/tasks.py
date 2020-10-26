import os

from django.db.models import Q
from django.utils import timezone

from phonebook.celery import app
from phonebook.settings import MEDIA_ROOT
from .models import Contact
from .utils import validate_uploaded_file, aws_upload


@app.task
def upload_file(uploaded_file):
    now = timezone.localtime(timezone.now())
    min_threshold = now - timezone.timedelta(minutes=3)
    df = validate_uploaded_file(os.path.join(MEDIA_ROOT, uploaded_file))
    if df is not None:
        if not df.empty:
            for i, j in df.iterrows():
                name = j['Name']
                phone_number = j['Phone Number']
                email_address = j['Email Address']
                recently_added = Contact.objects.filter(Q(
                    email_address=email_address) &
                    Q(phone_number=phone_number)).\
                    filter(created__range=[min_threshold, now])
                if not recently_added:
                    Contact.objects.create(name=name,
                                           phone_number=phone_number,
                                           email_address=email_address,
                                           created=now)
        else:
            print('Invalid file')
    else:
        print('The file does not contain all the necessary columns')
    aws_upload(uploaded_file, os.path.basename(uploaded_file))
    os.remove(uploaded_file)
