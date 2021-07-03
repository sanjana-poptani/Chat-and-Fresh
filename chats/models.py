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
    userprofile = models.ImageField(upload_to='image/',default='')
    firstname = models.CharField(max_length=100,default='')
    lastname = models.CharField(max_length=100,default='xyz')
    is_active = models.BooleanField(auto_created=True,default=False)
    email = models.EmailField(max_length=150,unique=True,default='')
    password = models.CharField(max_length=100,default='')
    last_login = models.DateTimeField(default=datetime.datetime.now().tzinfo)
    auth_token = models.CharField(max_length=100,default='')
    is_verified = models.BooleanField(default=False)
    created_At = models.DateTimeField(default=datetime.datetime.now().tzinfo)

    def __str__(self):
        return self.user.username

class UserGroups(models.Model):
    userRef = models.ForeignKey(Profile,on_delete=CASCADE)
    group = models.ForeignKey(groupModel,on_delete=CASCADE)

class ForgotPwd(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    forget_pwd_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.datetime.now().tzinfo)

    def __str__(self) -> str:
        return self

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200,default='')
    file = models.FileField(upload_to='file/',default='')
    timestamp = models.DateTimeField(default=datetime.datetime.now().tzinfo)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)