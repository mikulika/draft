from django.contrib.auth.decorators import login_required
from courses.models import Klasa
from users.forms import profileUpdateForm, userUpdateForm
from django.views.generic import TemplateView
from users.models import Profile as Pro
from users.models import Requests
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from project import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage

# Create your views here.
def HomeView(request):
    return render(request, "home.html")
    
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def grades(request):
    return render(request, "grades.html")

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username already exists' )
                return redirect(register)
            
            if User.objects.filter(email=email):
                messages.error(request, "Email already registered!")
                return redirect('home')
            
            if len(username)>10:
                messages.error(request, "Username must be under 10 caharacters")

            if password != confirm_password:
                messages.error(request, "Passwords didn't match!")
            
            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric")
                return redirect('home')
            
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            #user.is_staff=True
            user.save()

            messages.success(request, "Your Account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account")

            # Welcome Email

            subject = "Welcome to Maktab Login!!"
            message = f"Hello {first_name}!! \nWelcome to Maktab!! \nThank you for visiting our website.\nWe have also sent you a confirmation email, please confirm your email address in order to activate your account.\n\nThanking You\nMaktab"
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            return redirect('login')
    else:
        return render(request, "register.html")
    
def login_user(request):

    if request.method == 'POST':
        username =request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            first_name = user.first_name
            return render(request, 'profile/profile.html', {'first_name': first_name})
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('home')
     
    return render(request,"login.html")

@login_required
def Profile(request):
    user = request.user
    if request.method == 'POST':
        u_form = userUpdateForm(request.POST,instance=request.user)
        p_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account was successfully updated!')
            return redirect('users:Profile')
    else:
        u_form = userUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)

    context= {
        'u_form':u_form,
        'p_form':p_form,
        'user:':user
    }
    return render(request,'profile/profile.html',context)

@login_required
def edit_profile(request):
    print("edit_profile view called")  # Debug statement
    if request.method == 'POST':
        print("POST request detected")  # Debug statement
        u_form = userUpdateForm(request.POST, instance=request.user)
        p_form = profileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            print("Forms are valid")  # Debug statement
            u_form.save()
            p_form.save()
            return redirect('users:profile')
    else:
        print("GET request detected")  # Debug statement
        u_form = userUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    print(context) 
    return render(request, 'profile/edit_profile.html', context)


def teacher_request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('e-mail')
        phone = request.POST.get('phone')
        prof = request.user.profile

        # Create the teacher request
        teacher_request = Requests(profile=prof, name=name, email=email, phone=phone)
        teacher_request.save()

        # Update profile to mark as teacher
        prof.is_teacher = True
        prof.save()
        
    
def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')

def sign_up(request):
    return render(request, "register.html")
