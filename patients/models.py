from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    age = models.IntegerField()

    gender = models.CharField(max_length=20)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    def __str__(self):

        return self.name