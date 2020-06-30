from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Plant
from django.urls import reverse
import re

# pylint: disable=no-member

def index(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {
    'plants' : Plant.objects.all().order_by('-created_at')
    }

    return render(request, "index.html", context)

def add(request):
    if request.method == 'GET':
        return render(request, 'add.html', {"message": None})

    user = request.user
    print(user)
    title = request.POST['title']
    plant_type = request.POST['plant_type']
    plant_shape = request.POST['plant_shape']

    if not title:
        return render(request, 'add.html', {"message": "Enter a title."})
    elif len(title) < 4:
        return render(request, 'add.html', {"message": "Title should be longer than 4 characters."})
    if not plant_type:
        return render(request, 'add.html', {"message": "Enter a plant type i.e. indoor or outdoor."})
    elif len(plant_type) < 4:
        return render(request, 'add.html', {"message": "Plant type should be longer than 4 characters."})
    if not plant_shape:
        return render(request, 'add.html', {"message": "Enter a plant shape i.e seed cutting, full plant, etc.."})
    elif len(plant_shape) < 4:
        return render(request, 'add.html', {"message": "Username should be longer than 4 characters."})
    else:
        try:
            Plant.objects.create(title=title, plant_type=plant_type, plant_shape=plant_shape, uploader=user)
        except:
            return render(request, 'add.html', {"message": "Plant addition failed."})
    return HttpResponseRedirect(reverse('index'))


def info(request):
    context = {
        'plant': Plant.objects.get(Plant.id),
    }
    return render(request, 'info.html', context)



def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'GET':
        return render(request, 'login.html', {"message": None})

    username = request.POST['username']
    password = request.POST['password']

    # Server-side form validation
    if not username:
        return render(request, 'login.html', {"message": "Enter your username."})
    elif len(username) < 4:
        return render(request, 'login.html', {"message": "Username should be longer than 4 characters."})
    elif not password:
        return render(request, 'login.html', {"message": "Type your password."})
    else:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {"message": "Login failed."})

def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html', {"message": None})

    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirmation = request.POST['confirmation']

    # Server-side form validation
    if not username:
        return render(request, 'register.html', {"message": "Enter your username."})
    elif len(username) < 4:
        return render(request, 'register.html', {"message": "Username should be longer than 4 characters."})
    elif not email:
        return render(request, 'register.html', {"message": "No Email."})
    # Email validation required.
    elif not password or not confirmation:
        return render(request, 'register.html', {"message": "Type your password."})
    elif len(password) < 8 or len(confirmation) < 8:
        return render(request, 'register.html', {"message": "Password should be longer than 8 characters."})
    elif password != confirmation:
        return render(request, 'register.html', {"message": "Passwords don't match."})
    elif User.objects.filter(email=email):
        return render(request, 'register.html', {"message": "Email is invalid or already taken."})
    else:
        try:
            User.objects.create_user(username, email, password)
        except:
            return render(request, 'register.html', {"message": "Registration failed."})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
    return HttpResponseRedirect(reverse('index'))

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "You're Logged out"})