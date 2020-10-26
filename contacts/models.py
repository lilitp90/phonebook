from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30)
    email_address = models.EmailField()
    created = models.DateTimeField()

    def __str__(self):
        return self.name
