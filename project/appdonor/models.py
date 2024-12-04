from django.db import models
from appadmin.models import Category,CustomUser

# Create your models here.
class Pet(models.Model):
    donor=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    cat=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    pet_name=models.CharField(max_length=255,null=True)
    pet_breed=models.CharField(max_length=255,null=True)
    pet_image=models.ImageField(upload_to="image/",null=True)
    pet_age=models.IntegerField(null=True)
    description = models.TextField(null=True)
    approved=models.BooleanField(default=False)
    disapproved=models.BooleanField(default=False)
    visited=models.BooleanField(default=False)
    

    def __str__(self):
        return self.pet_name
    

