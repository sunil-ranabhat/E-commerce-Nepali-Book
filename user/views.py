from django.shortcuts import render
from django.shortcuts import render,redirect , HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template, render_to_string
from django.contrib.auth.models import auth

# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        signup_name = request.POST.get('signup_name')
        signup_username = request.POST.get('signup_username')
        signup_email = request.POST.get('signup_email')
        signup_password = request.POST.get('signup_password')
        print(signup_username)
        
        if get_user_model().objects.filter(username=signup_username).exists():
            messages.error(request,'The username has been taken already' , extra_tags='signup')
            return redirect('/auth/signup')
        elif get_user_model().objects.filter(email=signup_email).exists():
            messages.error(request,'The email has been used already' , extra_tags='signup')
            return redirect('/auth/signup') 
        else:
            user=get_user_model().objects.create_user(username = signup_username , password = signup_password , fullname = signup_name , email = signup_email , is_active = True)    
            user.save()
            
            return redirect('/')
        

    else:
        return render(request ,'signup.html')

def signin(request):
    if request.user.is_authenticated:
            return redirect('/')
    if request.method == 'POST':
        login_username = request.POST.get('login_username')
        login_password = request.POST.get('login_password')
        user=auth.authenticate(username=login_username,password=login_password)
        print(user)
        if user is not None:
            auth.login(request,user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('/')
        else:
            messages.error(request , 'Username or password not matching', extra_tags='login')
            return redirect(request.path_info)
    return render(request ,'signin.html')

def logout(request):
    auth.logout(request)
    next = request.GET.get('next')
    if next:
        return redirect(next)
    return redirect('/') 