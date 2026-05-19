from django.db import models

# Create your models here.
from django.db import models

class Doctor(models.Model):

    name = models.CharField(max_length=100)

    specialization = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    def __str__(self):

        return self.name