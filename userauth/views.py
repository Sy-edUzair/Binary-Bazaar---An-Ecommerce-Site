from django.shortcuts import render
from django.http import HttpResponseRedirect
from userauth.forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from .models import User


# Create your views here.
@csrf_protect
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #register the user
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Hey{username},your account was created successfully")

            #login the user
            return HttpResponseRedirect(reverse('userauth:login'))
    else:
        form = UserRegisterForm()
    

    return render(request,'userauth/sign-up.html',{
        'registerform':form,
    })

@csrf_protect
def login_view(request):
    #backend of how to login a user
    if request.method == "POST":
        email = request.POST.get("email").strip()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email__iexact=email)# using email since it is a unique field

            auth_user = authenticate(request,username=email,password=password)

            if auth_user is not None:
                login(request,auth_user)
                messages.success(request,"You are logged in")
                return HttpResponseRedirect(reverse('store:store'))
            else:
                messages.warning(request,"Incorrect Password, Please Try Again!")

        except:
            messages.warning(request,f"User with {email} does not exist")


    context={}
    return render(request,"userauth/login.html",context)

@csrf_protect
def logout_view(request):
    logout(request)
    messages.success(request,"You logged out")
    return HttpResponseRedirect(reverse("userauth:sign-up"))
