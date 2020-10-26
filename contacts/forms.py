from django import forms
from django.core.validators import FileExtensionValidator


class ContactForm(forms.Form):
    to_be_uploaded = forms.FileField(required=True,
                                     validators=[FileExtensionValidator(
                                         ['xls', 'xlsx'])])
