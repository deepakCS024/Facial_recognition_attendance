from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# to activate the user accounts
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
# getting token from utils.py
from .utils import TokenGenerator,generate_token

from arkauth.models import Register
# emails 
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.mail import BadHeaderError,send_mail
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMessage

# resetpasword generators

from django.contrib.auth.tokens import PasswordResetTokenGenerator
# threading
import threading

class EmailThread(threading.Thread):

    def __init__(self,email_message):
        self.email_message=email_message
        threading.Thread.__init__(self) 

    def run(self):
        self.email_message.send()
    
def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'auth/signup.html')
                   
        try:
            if User.objects.get(username=email):
                messages.warning(request,"Email is Taken")
                return render(request,'auth/signup.html')

        except Exception as identifier:
            pass

        user = User.objects.create_user(email,email,password)
        user.is_active=False
        user.save()
        current_site=get_current_site(request)
        email_subject="Activate Your Account"
        message=render_to_string('auth/activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)

        })

        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)

        EmailThread(email_message).start()
        messages.info(request," Activate Your Account by clicking link on your email ")
        return redirect('/arkauth/login')

    return render(request,'auth/signup.html')


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('/arkauth/login')
        return render(request,'auth/activatefail.html')

def handlelogin(request):
    if request.method=="POST":

        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/arkauth/login')

    return render(request,'auth/login.html')  


def handlelogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('/arkauth/login')


class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'auth/request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('auth/reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            EmailThread(email_message).start()

            messages.info(request,"WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET THE PASSWORD")
            return render(request,'auth/request-reset-email.html')

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'auth/request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'auth/set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'auth/set-new-password.html',context)
        
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success Please Login with NewPassword")
            return redirect('/arkauth/login/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'auth/set-new-password.html',context)

        return render(request,'auth/set-new-password.html',context)


def AddIa(request):
    if request.method=="POST":
        usn = request.POST.get('usn')
        gender = request.POST.get('gender')
        sem = request.POST.get('sem')
        ia = request.POST.get('ia')
        marks=request.POST.get('marks')
        subject=request.POST.get('subject')
        query=Register(usn=usn,gender=gender,sem=sem,ia=ia,marks=marks,subject=subject)
        query.save()
        messages.success(request,"Added Marks")
        return redirect('/addstudent')
    return redirect('/addstudent')   