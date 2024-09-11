from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'chattest.html')

def chat(request):
    return render(request, 'chat.html')

# Create your views here.
