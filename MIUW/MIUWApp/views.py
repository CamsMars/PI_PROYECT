from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth. forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'chattest.html')

def chat(request):
    return render(request, 'chat.html')

def menu(request):
    return render(request, 'sign_up.html')

def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html',{'form':UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user.save()
                user =user.objects.create_user(request.POST['username'], password=request.POST['password'])
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signupaccount.html',{'form':UserCreationForm, 'error':'usuario ya exixte'})
        else :
            return render(request, 'signupaccount.html', {'form':UserCreationForm, 'error':'password no coincide'})

def LogOUT(request):
    logout(request)
    return redirect('home')

def LogIN(request):
    if request.method == 'GET':
        return render(request, 'log_in.html', {'form':AuthenticationForm})
    else :
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'log_in.html', {'form': AuthenticationForm(), 'error': 'algunp de los 2 no coincide'})
        else :
            login(request, user)
            return redirect('home')
# Create your views here.
