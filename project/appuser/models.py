from django.db import models
from appadmin.models import Category,CustomUser
from appdonor.models import Pet

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    pet_id = models.IntegerField(null=True)  
    pet_name = models.CharField(max_length=255, null=True)
    adoptor = models.CharField(max_length=255, null=True)
    donor = models.CharField(max_length=255, null=True)
    donor_email = models.EmailField()
    adoptor_email = models.EmailField(null=True)
    donor_contact = models.CharField(max_length=10,null=True)
    adoptor_contact = models.CharField(max_length=10,null=True)  
    pet_breed = models.CharField(max_length=255, null=True)
    pet_age = models.IntegerField(null=True)
    donor_id=models.IntegerField(null=True)
    visited = models.BooleanField(default=False)  
    visited2=models.BooleanField(default=False)
    


class Adoption(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)






