from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth. forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from Api.models import Usuario
import os
import google.generativeai as genai
from django.http import JsonResponse

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def chat(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")

        if user_input:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)

            if response and hasattr(response, 'text'):
                return JsonResponse({"generated_text": response.text})
            else:
                return JsonResponse({"error": "No se pudo generar contenido."}, status=500)
        else:
            return JsonResponse({"error": "El input del usuario está vacío."}, status=400)
    
    return render(request, 'chat.html')  

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'chattest.html')

def menu(request):
    return render(request, 'Menu.html')

def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html',{'form':UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try: 
                user =User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()

                n=request.POST['username']
                ts=Usuario.objects.create(USR=n)
                ts.save()

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
        
def perfil(request):
    return render(request, 'profile.html')