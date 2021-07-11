from django.db import models

# Create your models here.

class user(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100) 