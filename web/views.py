from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from .models import Category,Item, UserProfile,ProductKey
from django.contrib.auth.models import User, auth
from django.contrib import messages
import secrets




# homepage
def home(request):
    items=Item.objects.filter(is_sold=False)[0:6]
    categories=Category.objects.all()
    return render(request, 'index.html', {'items':items, 'categories':categories})



# signin Up
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
       
        if password==password1:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect('register')
            else:
                user=User.objects.create_user(username,email,password)
                UserProfile.objects.create(user=user,balance=100)
                user.first_name=first_name
                user.last_name=last_name
                
                user.save();
                
                return redirect('login')
        else:
            messages.info(request, "Passwords doesn't march")
            return redirect('register')
    else:
        return render(request, 'register.html')

# Logging Out
def logout(request):
    auth.logout(request)
    return redirect('home')

#Loging In
def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            messages.info(request, "you have succefully logged in ")
            return redirect('home')
        else:
            messages.info(request, "enter correct credentials")
            return redirect('login')

    else:
        return render(request, 'login.html')


# getting the items or products and storing the unique and deducting from the free token when buy is initiated
def getting(request,pk):
        product=Item.objects.filter(is_sold=False)[0:1]
        user_keys = ProductKey.objects.filter(user=request.user)
        items=get_object_or_404(Item, pk=pk)
        user_profile = UserProfile.objects.filter(user=request.user).first()

        if user_profile:
           user_profile.deduct_balance(items.price)
           key_number = generate_key()
           user = request.user

        # Checking if the key is unique 
           while ProductKey.objects.filter(key_number=key_number).exists():
               key_number = generate_key()

           ProductKey.objects.create(key_number=key_number, user=user)
        
         
           return render(request,'purchase.html', {'product': product, 'user_keys':user_keys})
        
        else:
            
            return render(request,'insufficience.html')
   #generating the keys     
def generate_key():
    return secrets.token_hex(16)

#desplaying the key on the template
def user_keys(request):
    user_keys = ProductKey.objects.filter(user=request.user)
    return render(request, 'key.html', {'user_keys': user_keys})
