from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Plant
from django.urls import reverse
from .forms import PlantForm
import re

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# pylint: disable=no-member

def index(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {
    'plants' : Plant.objects.all().order_by('-created_at')
    }

    return render(request, "index.html", context)

def mylistings(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
    'plants' : Plant.objects.all().order_by('-created_at')
    }

    return render(request, "mylistings.html", context)


def delete(request, id):
    delete = Plant.objects.get(pk = id)
    delete.delete()
    return redirect('mylistings')


def create_profile(request):
    form = PlantForm()
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user = request.user
            user_pr.uploader = user
            user_pr.display_picture = request.FILES['display_picture']
            file_type = user_pr.display_picture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                return render(request, 'error.html')
            user_pr.save()
            return HttpResponseRedirect(reverse('index'))
    context = {"form": form,}
    return render(request, 'add.html', context)

def add(request):
    if request.method == 'GET':
        return render(request, 'add.html', {"message": None})

    user = request.user
    print(user)
    title = request.POST['title']
    document = request.File['document']
    description = request.POST['description']
    plant_type = request.POST['plant_type']
    plant_shape = request.POST['plant_shape']

    if not title:
        return render(request, 'add.html', {"message": "Enter a title."})
    elif len(title) < 3:
        return render(request, 'add.html', {"message": "Title should be longer than 3 characters."})
    elif not description:
        return render(request, 'add.html', {"message": "Enter a description."})
    elif len(title) < 10:
        return render(request, 'add.html', {"message": "Description should be longer than 10 characters."})
    if not plant_type:
        return render(request, 'add.html', {"message": "Enter a plant type i.e. indoor or outdoor."})
    elif len(plant_type) < 3:
        return render(request, 'add.html', {"message": "Plant type should be longer than 3 characters."})
    if not plant_shape:
        return render(request, 'add.html', {"message": "Enter a plant shape i.e seed cutting, full plant, etc.."})
    elif len(plant_shape) < 4:
        return render(request, 'add.html', {"message": "Username should be longer than 4 characters."})
    else:
        try:
            Plant.objects.create(title=title, document=document, description=description, plant_type=plant_type, plant_shape=plant_shape, uploader=user)
        except:
            return render(request, 'add.html', {"message": "Plant addition failed."})
    return HttpResponseRedirect(reverse('index'))


def info(request, id):
    context = {
        'plant': Plant.objects.get(pk = id),
    }
    return render(request, 'info.html', context)

def faq(request):
    if request.method == 'GET':
        return render(request, 'faq.html', {"message": None})


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
    elif len(username) < 3:
        return render(request, 'login.html', {"message": "Username should be longer than 3 characters."})
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
    elif len(username) < 3:
        return render(request, 'register.html', {"message": "Username should be longer than 3 characters."})
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