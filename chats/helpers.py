from django.core.mail import message, send_mail
import uuid
from django.conf import settings

def send_forget_pwd_mail(email,token):
    # token = str(uuid.uuid4())
    subject = "Your forget password link"
    message = f'Hi, click on the link to reset your password http://127.0.0.1:8000/change_pwd/{token}'
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_form,recipient_list)
    return True