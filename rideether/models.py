from django.db import models

class driver(models.Model):
    driver_name = models.CharField(max_length=100)
    vehical_name = models.CharField(max_length=100)
    vehical_number = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=100)