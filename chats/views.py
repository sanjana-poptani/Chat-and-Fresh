# from django.contrib.auth.models import User
from django import conf
from django.contrib import messages
from .models import *
from django.shortcuts import redirect, render, HttpResponseRedirect, reverse
from django.http.response import JsonResponse
import uuid
from django.conf import settings
from django.core.mail import message, send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
# from django.contrib.auth import authenticate,SESSION_KEY
# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password,check_password
import datetime
Session.objects.all().delete()
from .helpers import send_forget_pwd_mail
from .serializers import *

# Create your views here.
# @login_required(login_url="/")
def home(request):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email=request.session['email'])
        # for user in users:
        #     print("Got users: ",user.username)
        usr = Profile.objects.exclude(username = users.username)
        for i in usr:
            print("Got users: ",i.username)
        return render(request,'home1.html',{'users':usr,'curruser':users})
    else:
        return redirect('/')
    # return render(request,'home.html')

def message_view(request, sender, receiver):
    if not 'email' in request.session and 'id' in request.session:
        return redirect('/')
    if request.method == "GET":
        users = Profile.objects.get(email=request.session['email'])
        usr = Profile.objects.exclude(username = users.username)
        for i in usr:
            print("Got users: ",i.username)
        return render(request, "home.html",
                      {'users': usr,
                       'receiver': Profile.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender=sender, receiver=receiver) |
                                   Message.objects.filter(sender=receiver, receiver=sender),
                                   'curruser':users})


def home1(request):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email=request.session['email'])
        # for user in users:
        #     print("Got users: ",user.username)
        usr = Profile.objects.exclude(username = users.username)
        for i in usr:
            print("Got users: ",i.username)
        return render(request,'home1.html',{'users':usr,'curruser':users})
    else:
        return redirect('/')


def msge_view(request, sender, receiver):
    
    if not 'email' in request.session and 'id' in request.session:
        return redirect('/')
    if request.method == "GET":
        print("Rreached here")
        users = Profile.objects.get(email=request.session['email'])
        usr = Profile.objects.exclude(username = users.username)
        for i in usr:
            print("Got users: ",i.username)
        
        rec = Profile.objects.get(id=receiver)
        print(rec.username,rec.firstname,rec.lastname)

        msges = Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
        for i in msges:
            print("File: ",i.file)

        return render(request, "home1.html",
                      {'users': usr,
                       'receiver': Profile.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender=sender, receiver=receiver) |
                                   Message.objects.filter(sender=receiver, receiver=sender),
                                   'curruser':users})
    else:
        print("reached here")
        users = Profile.objects.get(email=request.session['email'])
        usr = Profile.objects.exclude(username = users.username)
        msge = request.POST.get('message')
        filee = request.FILES.get('file1')
        print(msge)
        if msge == None:
            msge = ''
        Message.objects.create(sender_id=sender,receiver_id=receiver,message=msge,file = filee,timestamp = datetime.datetime.now(),is_read=False)
        # return render(request, "home1.html",
        #               {'users': usr,
        #                'receiver': Profile.objects.get(id=receiver),
        #                'messages': Message.objects.filter(sender=sender, receiver=receiver) |
        #                            Message.objects.filter(sender=receiver, receiver=sender),
        #                            'curruser':users})
        return redirect("rooms1",sender,receiver)


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def login(request):
    print("Reached inside login")
    if request.method == 'POST':
        print("Reached inside if condition")
        username = request.POST.get('username')
        password = request.POST.get('password')
        pwd = make_password(password)
        try:
            user = Profile.objects.get(username = username)
            
            print("Found user: ",user.username)
            
            
            if not user.is_verified:
                return render(request,'login.html',{'message':'Profile is not verified, check your mail!'})

            elif not check_password(password,user.password):
                print("Pwd: " + pwd + " and password: " + user.password)
                return render(request,'login.html',{'message':'Password is invalid!'}) 

            else:
                print('Reached here')
                user.is_active=True
                user.last_login = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                print("Current time is ",datetime.datetime.now())
                user.save()
                request.session['email'] = user.email
                request.session['username'] = user.username
                request.session['id'] = user.id
                print("Reached here with ",request.session['email'])
                # request.session['profile_pic'] = user.userprofile
                # return redirect('')
                return redirect('home')
        # if authenticate()
        except:
            return render(request,'login.html',{'message':'Username is invalid!'}) 
    return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        profile = request.FILES.get('profile')
        print("Got profile pic" + str(request.FILES.get('profile')))
        print("Got profile pic" + str(profile))
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
            pwd = make_password(password)
            user_obj = Profile.objects.create(username = username,userprofile = profile,firstname = fname,lastname = lname,email = email,password = pwd,auth_token = auth_token)
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
                return render(request,'changed_pwd.html',{'message':'Your account has been already verified!'})
            profile_obj.is_verified = True
            profile_obj.save()
            return render(request,'changed_pwd.html',{'message':'Your account has been verified successfully!'})
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


def forgot_pwd(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not Profile.objects.filter(username = username).first():
                message = "No such user found!!"
                return render(request,'forgot_pwd.html',{'message':message})

            user_obj = Profile.objects.get(username = username)
            print("User found ",user_obj.username)
            token = str(uuid.uuid4())
            # profile_obj = ForgotPwd.objects.filter(user = user_obj).first()
            user_obj.auth_token = token
            print("Token set to ",user_obj.auth_token)
            user_obj.save()
            # profile_obj = ForgotPwd.objects.all()
            # for i in profile_obj:
            #     print("Profile obj: ",i)
            print("Got token ",token)
            print("Inside fn",send_forget_pwd_mail(user_obj.email,token))
            message = "An email has been sent"
            return render(request,'forgot_pwd.html',{'message':message})


    except Exception as e:
        print(e)
    return render(request,'forgot_pwd.html')


def change_pwd(request,token):
    context = {}
    try:
        print("came inside")
        profile_obj = Profile.objects.filter(auth_token = token).first()
        print("Got profile ",profile_obj.username)
        # print(profile_obj)

        context = {'user_id':profile_obj.id}      
        print("Set context to ",context)  
        if request.method == 'POST':
            new_pwd = request.POST.get('password1')
            confirm_pwd = request.POST.get('password2')
            user_id = request.POST.get('user_id')
            if user_id is None:
                message = "No such user found!!"
                return render(request,'change_pwd.html',{'message':message})

            user_obj = Profile.objects.get(id = user_id)
            if check_password(confirm_pwd,user_obj.password):
                message = "Password and confirm password doesn't match"
                return render(request,'change_pwd.html',{'message':message})

            print("User id is ",user_id)
            user_obj = Profile.objects.get(id = user_id)
            user_obj.password = make_password(new_pwd)
            user_obj.save()
            message = "Password changed successfully"
            return render(request,'changed_pwd.html',{'message':message})

    except Exception as e:
        print(e)

    return render(request,'change_pwd.html',context)


def logout(request):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email=request.session['email'])
        users.is_active=False
        last_login = datetime.datetime.now()
        hrs = 5
        mins = 31
        hours_added = datetime.timedelta(hours = hrs,minutes = mins)
        print(hours_added)
        curr_date = last_login + hours_added
        users.last_login = curr_date
        users.save()
    del request.session['email']
    del request.session['username']
    del request.session['id']
    return redirect('/')


