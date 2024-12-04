from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    user_type=models.CharField(default=1, max_length=10)
    email = models.EmailField(unique=True)
    address=models.CharField(max_length=255,null=True)
    contact=models.CharField(max_length=10,null=True)
    

class Category(models.Model):
    Category_name=models.CharField(max_length=255,unique=True)

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField(null=True)
    visited = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    
class Donor_message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_doner = models.TextField(null=True, default="")
    visited = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)


class Admin_message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_admin = models.TextField(null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
class Donation_message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    donate = models.TextField(null=True, default="")
    visited = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)


    