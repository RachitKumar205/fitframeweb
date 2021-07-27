from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# Create your views here.
@login_required
def index(request):

    return render(request, 'main/index.html',{
        "poses": Pose.objects.all()
    })


def signin(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(request,'Nigga u signed in')
    return render(request, 'registration/login.html')

@login_required()
def pose(request, pose_id):
    try:
        ch = Choice.objects.get(name=User.username)
        ch.number = pose_id
    except:
        ch = Choice(name=User.username, number=pose_id)
        ch.save()

    return render(request, 'main/pose.html')