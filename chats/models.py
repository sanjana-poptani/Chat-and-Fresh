from typing import Callable
from django.db import models
import datetime
from django.db.models.expressions import F
import pytz
# from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField
# Create your models here.



class Profile(models.Model):
    username = models.CharField(max_length=100,unique=True)
    userprofile = models.ImageField(upload_to='image/',default='')
    firstname = models.CharField(max_length=100,default='')
    lastname = models.CharField(max_length=100,default='xyz')
    is_active = models.BooleanField(auto_created=True,default=False)
    email = models.EmailField(max_length=150,unique=True,default='')
    password = models.CharField(max_length=100,default='')
    last_login = models.DateTimeField(default=datetime.datetime.now)
    auth_token = models.CharField(max_length=100,default='')
    is_verified = models.BooleanField(default=False)
    created_At = models.DateTimeField(default=datetime.datetime.now)
    status = models.CharField(max_length=1000,default='')


class groupModel(models.Model):
    Admin = models.ForeignKey(Profile,on_delete=CASCADE)
    groupName = models.CharField(max_length=100,default='')
    groupDesc = models.CharField(max_length=5000,default='Plz change description....')
    groupImg = models.ImageField(upload_to='image/',default='')

class UserGroups(models.Model):
    userRef = models.ForeignKey(Profile,on_delete=CASCADE)
    group = models.ForeignKey(groupModel,on_delete=CASCADE)

class GrpMsges(models.Model):
    message = models.CharField(max_length=1200,default='')
    file = models.FileField(upload_to='file/',default='')
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    sender = models.ForeignKey(Profile,on_delete=CASCADE)
    group = models.ForeignKey(groupModel,on_delete=CASCADE)

class ForgotPwd(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    forget_pwd_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self) -> str:
        return self

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200,default='')
    file = models.FileField(upload_to='file/',default='')
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    is_read = models.BooleanField(default=False)
    # is_friend = models.BooleanField(default=False)
    # is_req = models.BooleanField(default=False)
    def __str__(self):
        return self.message


class Friends(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='send_user')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receive_user')
    is_friend = models.BooleanField(default=False)
    is_req = models.BooleanField(default=False)

class Feedback(models.Model):
    feedback = models.CharField(max_length=5000,default='')
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)


class Broadcast(models.Model):
    notification = models.CharField(max_length=5000,default='')
    date = models.DateTimeField(default=datetime.datetime.now)