from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils import encoding
from loginsystem import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes , force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from . tokens import generate_token
from email.message import EmailMessage
from django.core.mail import EmailMessage  

# Create your views here.

def home(request):
    return render(request,'index.html')
    # return HttpResponse("hello")


def signup(request):
    if request.method == "POST" :
            username = request.POST.get('username')
            first = request.POST.get('firstname')
            last  = request.POST.get('lastname')
            email  = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
 

            if User.objects.filter(username=username):
                messages.error(request,"Username already exists! Please try some other username.")
                return redirect('home')
 
            if User.objects.filter(email=email):
                messages.error(request,"Email already registered! Please try other email.")
                return redirect('home')
 
            if len(username)>10:
                messages.error(request,"Username must be in 10 characters.")

            if pass1!=pass2:
                messages.error(request,"Password didn't match!")

            if not username.isalnum():
                messages.error(request,"Username must be Alpha-numeric!")
                return redirect('home')


 
            xyz = User.objects.create_user(username, email,pass1)
            xyz.first_name= first
            xyz.last_name = last

            xyz.is_active = False
            xyz.save()

            messages.success(request, "Your account is successfully created. We have sent you a confirmation email, please confirm your email address in order to activate your account. ")
          
            # Welcome Email
           
            subject = "Welcome to Test Project - Django Login!!"
            message = "Hello  " +  xyz.first_name + "!! \n " + "Welcome to Test Project!! \n Thankyou for visiting my project \n We have also send you a confirmation email, please confirm your email address in order to activate your account. \n \n Thanking You! \n Rashi Jain"
            from_email =settings.EMAIL_HOST_USER
            to_list = [xyz.email]
            send_mail(subject , message , from_email, to_list,  fail_silently=True)
    

            #  Email Address Confirmation EWmail

            current_site = get_current_site(request)
            email_subject = "Confirm your email @ test-project - Django Login!!" 
            message2 = render_to_string('email_confimation.html',{
                'name' : xyz.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(xyz.pk)),
                'token': generate_token.make_token(xyz),
            })  


            email= EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [xyz.email],
            )

            email.fail_silently = True
            email.send()


            return redirect('/signin/')

    else:
        pass
    return render(request,'signup.html')
    # return HttpResponse("hello signup")
  
def signin(request):
    if request.method == "POST" :
            username = request.POST.get('username')
            pass1 = request.POST.get('pass1')
            
            user = authenticate(username=username , password=pass1)

            if user is not None:
                login(request, user)
                fname = user.first_name
                return render(request ,"index.html", {'fname': fname})


            else:
                messages.error(request,"Bad Creadentials")
                return redirect('home')

    return render(request,'signin.html')
    # return HttpResponse("hello signin")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')

    # return render(request,'signout.html')
    # return HttpResponse("hello signout")



# creating a function "activate" in order to activate the account of user 
# force_text is like encoding the special tokens and checking that wheather this token was given to particular user or not.
# pk = primary key
# xyz is our user object

def activate(request, uidb64, token):
    try:
        uid= force_text(urlsafe_base64_decode(uidb64))
        xyz = User.objects.get(pk=uid)

    except(TypeError , ValueError, OverflowError , User.DoesNotExist):
        xyz = None


    if xyz is not None and generate_token.check_token(xyz, token):
        xyz.is_active = True
        xyz.save()
        login(request, xyz)
        return redirect('signin')

    else:
        return render(request,'activation_failed.html')