# from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.shortcuts import redirect, render
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login

# Create your views here.
# @login_required(login_url="/")
def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = Profile.objects.filter(username = username,password = password).first()
        if user is None:
            return render(request,'login.html',{'message':'Username or password is invalid!'}) 
        
        if not user.is_verified:
            return render(request,'login.html',{'message':'Profile is not verified, check your mail!'})
        else:
            return redirect('/')
        # if authenticate()

    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        profile = request.POST.get('profile')
        email = request.POST.get('email')
        password1 = request.POST.get('pwd1')
        password2 = request.POST.get('pwd2')
        if password2 == password1:
            password = password1
            print(password)
        else:
            # messages.success('Password and confirm password must be same!')
            return render(request,'register.html',{'message':'Password and confirm password must be same!'})

        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        try:
            if Profile.objects.filter(username = username).first():
                # messages.success('Username is already taken! Please try with another username')
                return render(request,'register.html',{'message':'Username is already taken! Please try with another username'})

            if Profile.objects.filter(email = email).first():
                # messages.success('Email is already taken! Please try with another email')
                return render(request,'register.html',{'message':'Email is already taken! Please try with another email'})
            auth_token = str(uuid.uuid4())
            print("Reached with ",username,password,profile,fname,lname,auth_token,email)
            user_obj = Profile.objects.create(username = username,userprofile = profile,firstname = fname,lastname = lname,email = email,password = password,auth_token = auth_token)
            user_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('/token')
        except Exception as e:
            print(e)
    return render(request,'register.html')

def success(request):
    return render(request,'success.html')

def token_send(request):
    return render(request,'token_send.html')

def verify(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                return render(request,'login.html',{'message':'Your account has been already verified!'})
            profile_obj.is_verified = True
            profile_obj.save()
            return render(request,'login.html',{'message':'Your account has been verified successfully!'})
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def error_page(request):
    return render(request,'error.html')

def send_mail_after_registration(email,token):
    subject = "Your account need to be verified"
    message = f'Hi click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)