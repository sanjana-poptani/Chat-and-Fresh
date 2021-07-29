# from django.contrib.auth.models import User
import re
from django import conf
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models.aggregates import Count
from django.db.models.fields import EmailField
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
from django.utils import timezone
import pytz

# Create your views here.
# @login_required(login_url="/")

def find_frnds(curruser):
    friends = Friends.objects.filter(sender = curruser)
    frnds = []
    if friends:
        for i in friends:
            if i.is_friend == True or i.is_req == True:
                frnds.append(i.receiver)
    friends1 = Friends.objects.filter(receiver = curruser)
    if friends1:
        for i in friends1:
            if i.is_friend == True or i.is_req == True:
                frnds.append(i.sender)
    return frnds

def find_grps(user):
    try:
        print("Reached in find grps with user id ",user)
        fetch_user = UserGroups.objects.filter(userRef = user)
        print("Found user groups ",fetch_user)
        fetch_all_grps = []
        for i in fetch_user:
            fetch_grp = groupModel.objects.filter(id = i.group.id)
            print("Found group",fetch_grp)
            fetch_all_grps.append(fetch_grp)
        print("Found groups", fetch_all_grps)
        fetch_all_users = []
        for i in fetch_all_grps:
            fetch_usr = UserGroups.objects.filter(group = i)
            fetch_all_users.append(fetch_usr)
        grp_details = [fetch_all_grps,fetch_all_users]
        return grp_details
    except:
        return []

def fetch_grps(user):
    grps = find_grps(user)
    groups = []
    if grps:
        grpss = grps[0]
        for i in grpss:
            groups.append(i[0])
        print("Groups are ",groups)
    return groups

def home(request):
    if not 'email' in request.session:
        return redirect("/")
    if request.session['email'] == "sanjupoptani17@gmail.com" and request.session['username'] == "admin":
        return render(request,'adminHome.html')
    elif 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email=request.session['email'])
        usr = Profile.objects.exclude(username = users.username)
        frnds = find_frnds(users)
        if frnds:
            print("Found frnds: ",frnds[0])
            groups = fetch_grps(users)
            pending_msges = []
            for i in frnds:
                check_reads = Message.objects.filter(sender = i,receiver = users)
                for msge in check_reads:
                    if msge.is_read == False:
                        pending_msges.append(i)
            set_pending_msges = set(pending_msges)
            for i in set_pending_msges:
                print(i)
            return render(request,'home1.html',{'users':usr,'curruser':users,'friends':frnds,'pend_reads':set_pending_msges,'grps':groups})
        else:
            return render(request,'home1.html',{'users':usr,'curruser':users})
    else:
        return redirect("/")
    # return render(request,'home.html')

# def adminHome(request):


def add_edit_status(request):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email=request.session['email'])
        # for user in users:
        #     print("Got users: ",user.username)
        if request.method == "POST":
            status = request.POST.get("status")
            users.status = status
            users.save()
        return redirect('home')
    else:
        return redirect('/')

def change_grp_desc(request,grp_id):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email=request.session['email'])
        grp_obj = groupModel.objects.get(id = grp_id)
        # for user in users:
        #     print("Got users: ",user.username)
        if request.method == "POST":
            grpNm = request.POST.get("grpNm")
            grpDesc = request.POST.get("status")
            if grpNm != None:
                grp_obj.groupName = grpNm
                grp_obj.save()
            if grpDesc != None:
                grp_obj.groupDesc = grpDesc
                grp_obj.save()
        return redirect('rooms2',users.id,grp_id)
    else:
        return redirect('/')


def add_change_grp_icn(request,grp_id):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email=request.session['email'])
        grp_obj = groupModel.objects.get(id = grp_id)
        # for user in users:
        #     print("Got users: ",user.username)
        if request.method == "POST":
            print("Reached here with ",request.FILES.get("grpIcn")," and grp ",grp_obj.groupName)
            grpImg = request.FILES.get("grpIcn")
            grp_obj.groupImg = grpImg
            # print("going to change img ",grp_obj.groupImg)
            grp_obj.save()
            # print("saved now, so image is ",grp_obj.groupImg)
        return redirect('rooms2',users.id,grp_id)
    else:
        return redirect('/')

def viewNotifications(request):
    if 'email' in request.session and 'id' in request.session:
        if request.method == "GET":
            print("Reached here ")
            users = Profile.objects.get(email=request.session['email'])
            usr = Profile.objects.exclude(username = users.username)
            notifications = Broadcast.objects.all()
            for n in notifications:
                print(n.notification)
            frnds = find_frnds(users)
            groups = fetch_grps(users)
            return render(request, "home1.html",{'users': usr,'curruser':users,'notices':notifications,'friends':frnds,'grps':groups})
    else:
        return redirect("/")



def fetchUsers(request):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.all()
        months = []
        for month in range(12):
            months.append(0)
        for user in users:
            month = user.created_At.month
            months[month - 1] += 1
        monthLabel = ['January','February','March','April','May','June','July','August','September','October','November','December']
        return render(request,"adminReport.html",{'data':months,'label':monthLabel})
    else:
        return redirect("/")

def createGrp(request):
    if 'email' in request.session and 'id' in request.session:
        if request.method == "POST":
            print("Reached here in post")
            GroupName = request.POST.get('grpnm')
            GroupImg = request.FILES.get('grpimg')
            GroupDesc = request.POST.get('grpdesc')
            if GroupDesc == None:
                GroupDesc = "Add group description..."
            usr = Profile.objects.get(email = request.session['email'])
            grp_id = groupModel.objects.create(Admin = usr,groupName = GroupName,groupDesc = GroupDesc,groupImg = GroupImg)
            return redirect("newGrp2",grp_id.id)
        else:
            return render(request,"new_group.html")
    else:
        return redirect("/")

def createGrp2(request,grp_id):
    if 'email' in request.session and 'id' in request.session:
        if request.method == "POST":
            curr_user = Profile.objects.get(email = request.session['email'])
            print("Reached here in post")
            ppls = request.POST.getlist('frnds[]')
            grp = groupModel.objects.get(id = grp_id)
            for i in ppls:
                print("Got ",i)
                user = Profile.objects.get(id = i)
                UserGroups.objects.create(userRef = user,group = grp)
            UserGroups.objects.create(userRef = curr_user,group = grp)
            return redirect("home")
        else:
            usr = Profile.objects.get(email = request.session['email'])
            frnds = find_frnds(usr)
            print(frnds)
            return render(request,"new_group2.html",{'friends':frnds,'grp':grp_id})
    else:
        return redirect("/")

def msge_view(request, sender, receiver):
    if 'email' in request.session and 'id' in request.session:
        if request.method == "GET":
            print("Rreached here in msge_view")
            users = Profile.objects.get(email=request.session['email'])
            usr = Profile.objects.exclude(username = users.username)
            for i in usr:
                print("Got users: ",i.username)
            frnds = find_frnds(users)
            print("Found friends of ",users," are ",frnds)
            rec = Profile.objects.get(id=receiver)
            print(rec.username,rec.firstname,rec.lastname)
            groups = fetch_grps(users)
            check_friend = Friends.objects.filter(sender=sender,receiver=receiver) | Friends.objects.filter(sender = receiver,receiver = sender)
            if check_friend:
                print("Found friend",check_friend[0])
                is_friends = []
                for i in check_friend:
                    if i.is_friend == True and (i.sender == users or i.receiver == users):
                        is_friends.append(True)
                    else:
                        is_friends.append(False)

                if is_friends[0] == True:
                    print("Reached here with friends",is_friends[0])
                    msges = Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
                    msg_objs = msges.order_by("id")
                    for i in msg_objs:
                        print("message: ",i.message)
                        i.is_read = True
                        i.save()
                        # print("File: ",i.file)

                    
                    for i in usr:
                        print("Got users: ",i.username)
                    
                    return render(request, "home1.html",
                            {'users': usr,
                            'receiver': Profile.objects.get(id=receiver),
                            'messages': msg_objs, 'curruser':users,'friends':frnds,'grps':groups})
                else:
                    if check_friend[0].is_req == True:
                        if check_friend[0].receiver == users:
                            val1 = 'Accept'
                            val2 = 'Reject'
                            return render(request, "home1.html",
                                {'users': usr,
                                'receiver': Profile.objects.get(id=receiver),
                                'val1':val1,'val2':val2,'curruser':users,'friends':frnds,'grps':groups})
                        else:
                            val = 'Request sent!'
                            bl = True
                            return render(request, "home1.html",
                                {'users': usr,'bl':bl,
                                'receiver': Profile.objects.get(id=receiver),
                                'val':val,'curruser':users,'friends':frnds,'grps':groups})
            else:
                print("Friend not found of ",users)
                val = 'Send request'
                return render(request, "home1.html",
                    {'users': usr,
                    'receiver': Profile.objects.get(id=receiver),
                    'val':val,'curruser':users,'friends':frnds,'grps':groups})
            
        else:
            print("reached here with file")
            users = Profile.objects.get(email=request.session['email'])
            usr = Profile.objects.exclude(username = users.username)
            msge = request.POST.get('message')
            filee = request.FILES.get('file1')
            print("Reached here atleast")
            print("got file",filee)
            print(msge)
            if msge == None:
                msge = ''
            Message.objects.create(sender_id=sender,receiver_id=receiver,message=msge,file = filee,is_read=False)
            return redirect("rooms1",sender,receiver)
    else:
        return redirect("/")


def grp_msge_view(request, sender, grpid):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email=request.session['email'])
        usr = Profile.objects.exclude(username = users.username)
        grp_obj = groupModel.objects.get(id = grpid)
        frnds = find_frnds(users)
        grp_receivers = UserGroups.objects.filter(group = grp_obj)
        receivers = []
        print("Group receivers are ",grp_receivers)
        
        for i in grp_receivers:
            if i.userRef != users:
                receivers.append(i)
        total_receivers = len(receivers)
        print("Got receivers",receivers," and length ",total_receivers)
        if request.method == "GET":
            print("Rreached here in msge_view")
            groups = fetch_grps(users)
            msges = GrpMsges.objects.filter(group=grp_obj)
            for i in msges:
                print("File: ",i.file)
                    
            for i in usr:
                print("Got users: ",i.username)
                    
            return render(request, "grphome.html",
            {'users': usr,
            'grp_receivers': receivers,
            'total_receivers':total_receivers,
            'curr_grp':grp_obj,
            'msges': msges,
            'curruser':users,'friends':frnds,'grps':groups})
        else:
            print("reached here with file")
            msge = request.POST.get('message')
            filee = request.FILES.get('file1')
            print("Reached here atleast")
            print("got file",filee)
            print(msge)
            if msge == None:
                msge = ''
            GrpMsges.objects.create(sender=users,group=grp_obj,message=msge,file = filee)
            return redirect("rooms2",sender,grpid)
    else:
        return redirect("/")


@csrf_exempt
def grp_message_list(request, sender=None, grpid=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = GrpMsges.objects.filter(sender_id=sender, group_id=grpid, is_read=False)
        serializer = MessageSerializer1(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer1(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def is_accept(request,sender,receiver):
    if 'email' in request.session and 'id' in request.session:
        # users = Profile.objects.get(email = request.session['email'])
        # usr = Profile.objects.exclude(email = request.session['email'])
        sendr = Friends.objects.filter(sender = sender,receiver = receiver) | Friends.objects.filter(sender = receiver,receiver = sender)
        if sendr:
            sendr[0].is_req = True
            sendr[0].is_friend = True
            sendr[0].save()
            return redirect("rooms1",sender,receiver)
    else:
        return redirect("/")


def is_decline(request,sender,receiver):
    if 'email' in request.session and 'id' in request.session:
        user = Friends.objects.filter(sender = sender,receiver = receiver) | Friends.objects.filter(sender = receiver,receiver = sender)
        if user:
            user[0].delete()
            return redirect("rooms1",sender,receiver)
    else:
        return redirect("/")




def reqSent(request,sender,receiver):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email = request.session['email'])
        usr = Profile.objects.exclude(email = request.session['email'])
        sendr = Profile.objects.filter(id = sender).first()
        receivr = Profile.objects.filter(id = receiver).first()
        frnds = find_frnds(users)
        if request.method == "POST":
            print("Reached inside post method")
            get_users = Friends.objects.all()
            if get_users:
                print("Got all users")
                check_user = []
                for i in get_users:
                    if (i.sender == sender and i.receiver == receiver) or (i.sender == receiver and i.receiver == sender):
                        check_user.append(i)
                if check_user:
                    print("Found user ",check_user[0])
                    check_user[0].is_req = True
                    check_user[0].save()
                    print("Saved user")
                else:
                    print(sendr,receivr)
                    Friends.objects.create(sender = sendr,receiver = receivr,is_req = True)
                    print("New obj created")
            else:
                print(sendr,receivr)
                Friends.objects.create(sender = sendr,receiver = receivr,is_req = True)
                print("New obj created")
            val = "Request sent!!"
            blField = True
            groups = fetch_grps(users)
            # return render(request, "home1.html",
            #         {'users': usr,
            #         'receiver': Profile.objects.get(id=receiver),
            #         'val':val,'curruser':users,'bl':blField,'friends':frnds,'grps':groups})
            return redirect("home")
    else:
        return redirect("/")



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
            print("Reached inside try")
            
            if ( username == "admin" or username == "Admin" ) and password == "admin":
                print("Yeah i am an admin!!")
                request.session['email'] = "sanjupoptani17@gmail.com"
                request.session['username'] = "admin"
                request.session['id'] = 1000000
                return redirect('home')
            
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
            print("Password is " + pwd)
            user_obj = Profile.objects.create(username = username,userprofile = profile,firstname = fname,lastname = lname,email = email,password = pwd,auth_token = auth_token)
            user_obj.save()
            print("User obj created successfully")
            send_mail_after_registration(email,auth_token)
            print("Mail sent")
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


def finalLogout(request):
    if 'email' in request.session and 'id' in request.session:
        del request.session['email']
        del request.session['username']
        del request.session['id']
        return redirect('/')

def logout(request):
    if not "email" in request.session:
        return redirect("/")
    # print("Reached at logout with email",request.session['email'],"and username",request.session['username'])
    if request.session['email']=="sanjupoptani17@gmail.com" and request.session['username']=='admin':
        print("Reached at logout if")
        return redirect("finalLogout")
    elif 'email' in request.session and 'id' in request.session:
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
        return redirect("finalLogout")
    else:
        return redirect("/")
    
def submitFeedback(request):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email = request.session['email'])
        usr = Profile.objects.exclude(username = users.username)
        frnds = find_frnds(users)
        if frnds:
            print("Found frnds: ",frnds[0])
            groups = fetch_grps(users)
            return render(request,'home1.html',{'msge':'Thank you for your valuable feedback','users':usr,'curruser':users,'friends':frnds,'grps':groups})
        else:
            return render(request,'home1.html',{'msge':'Thank you for your valuable feedback','users':usr,'curruser':users})
    else:
        return redirect("/")


def feedback(request):
    if 'email' in request.session and 'id' in request.session:
        users = Profile.objects.get(email=request.session['email'])
        if request.method == 'POST':
            feedback = request.POST.get('feedback')
            Feedback.objects.create(feedback = feedback,user = users)
            user = Profile.objects.get(email=request.session['email'])
            usr = Profile.objects.exclude(username = users.username)
            return redirect("submitFeedback")
    else:
        return redirect('/')

def clearChat(request,sender,receiver):
    if 'email' in request.session and 'id' in request.session:
        msges = Message.objects.filter(sender=sender, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
        for i in msges:
            i.delete()
        return redirect("rooms1",sender,receiver)

def openVideo(request):
    if 'email' in request.session and 'id' in request.session:
        usr = Profile.objects.get(email=request.session['email'])
        return render(request,"video.html",{"curruser":usr})
    else:
        return redirect("/")

def loadFeedback(request):
    if 'email' in request.session and 'id' in request.session:
        feedback = Feedback.objects.all()
        return render(request,"adminFeedback.html",{'feedbacks':feedback})
    else:
        return redirect("/")

def view_broadcast(request):
    if 'email' in request.session and 'id' in request.session:
        broadcast = Broadcast.objects.all()
        return render(request,"adminBroadcast.html",{'details':broadcast})
    else:
        return redirect("/")

def broadcast(request):
    if 'email' in request.session and 'id' in request.session:
        if request.method == 'POST':
            message = request.POST.get('msge')
            date = datetime.datetime.now()
            Broadcast.objects.create(notification = message,date = date)
            return redirect("viewBroadcast")
    else:
        return redirect("/")
