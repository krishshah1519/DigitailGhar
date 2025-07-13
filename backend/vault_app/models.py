from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    dob = models.DateField()
    gender_choices = (('male','Male'),('female','Female'))
    gender = models.CharField(choices= gender_choices)
    phone_number = models.CharField(max_length= 10)

    def __str__(self):
        return self.username