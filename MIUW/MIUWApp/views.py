from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'Musictampl.html')

def about(request):
    return render(request, 'about2.html')

# Create your views here.
