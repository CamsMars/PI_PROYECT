from django.shortcuts import render
from .forms import UserCreateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from Api.models import usuario as US

from django.contrib.auth.decorators import login_required


def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html', {'form': UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            if User.objects.filter(username=request.POST['username']).exists():
                return render(request, 'signupaccount.html', {'form': UserCreateForm, 'error': 'Username already taken. Choose a new username.'})
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                US.objects.create(id=user, USR=user.username)
                login(request, user)
                return redirect('home')
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                return render(request, 'signupaccount.html', {'form': UserCreateForm, 'error': 'Username already taken. Choose a new username.'})
            except Exception as e:
                print(f"Unexpected error: {e}")
                return render(request, 'signupaccount.html', {'form': UserCreateForm, 'error': 'An unexpected error occurred. Please try again.'})
        else:
            print("Passwords do not match.")
            return render(request, 'signupaccount.html', {'form': UserCreateForm, 'error': 'Passwords do not match'})


@login_required
def logoutaccount(request):
    logout(request)
    return redirect('home')


def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html',
                      {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'loginaccount.html',
                          {'form': AuthenticationForm(),
                           'error': 'username and password do not match'})
        else:
            login(request, user)
            return redirect('home')
