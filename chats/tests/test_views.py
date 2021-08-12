from django.http import response
from django.test import TestCase, Client, client
from django.urls import reverse
from chats.views import *
from chats.models import Profile
from django.contrib.auth.hashers import make_password,check_password
import unittest

class TestViews(TestCase):
    def test_project_login_GET(self):
        client = Client()
        response = client.get(reverse('login'))
        self.assertEquals(response.status_code,200)
    
    def setUP(self):
        client = Client()
        username = 'testuser'
        firstname = 'test'
        lastname = 'user'
        email = 'teest@gmail.com'
        password = 'test'
        pwd = make_password(password)
        is_verified = True
        user = Profile.objects.create(username = username,firstname = firstname,lastname = lastname,email = email,password = pwd,is_verified = is_verified)
        user.save()
        login = client.login(username = username,password = pwd)
        self.assertEqual(login,True)

    # def test_project_home_GET(self):
    #     response = self.client.get('home/')
    #     self.assertEquals(response.status_code,200)

    def test_project_register_GET(self):
        client = Client()
        response = client.get(reverse('register'))
        self.assertEquals(response.status_code,200)

    