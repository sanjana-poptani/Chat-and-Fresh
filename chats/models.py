from django.db import models
import datetime
# from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField
# Create your models here.


class groupModel(models.Model):
    groupName = models.CharField(max_length=100)
    groupDesc = models.CharField(max_length=1000)

class Profile(models.Model):
    username = models.CharField(max_length=100,unique=True)
    userprofile = models.CharField(max_length=100,default='')
    firstname = models.CharField(max_length=100,default='')
    lastname = models.CharField(max_length=100,default='xyz')
    is_active = models.BooleanField(auto_created=True,default=False)
    email = models.EmailField(max_length=150,unique=True,default='')
    password = models.CharField(max_length=100,default='')
    last_login = models.DateTimeField(auto_now=True)
    auth_token = models.CharField(max_length=100,default='')
    is_verified = models.BooleanField(default=False)
    created_At = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class UserGroups(models.Model):
    userRef = models.ForeignKey(Profile,on_delete=CASCADE)
    group = models.ForeignKey(groupModel,on_delete=CASCADE)