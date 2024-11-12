import os
import re
import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Api.models import *
from django.contrib.auth.models import User
from Api.Api_utilities import create_playlist, search_song, add_song_to_playlist
from Api.extras import *


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def getUserContext(user):
    profile = usuario.objects.get(id=user)
    context = {
        "username": profile.USR,
        "name": profile.Nombre,
        "last_name": profile.Apellido,
        "email": profile.Email,
        "fav_artists": profile.Artistas_FAV.split(","),
        "happy_genre": profile.MusicalPreference.split(",")[0],
        "SAD_genre": profile.MusicalPreference.split(",")[1],
        "Calm_genre": profile.MusicalPreference.split(",")[2],
        "Angry_genre": profile.MusicalPreference.split(",")[3],
        "Euphoria_genre": profile.MusicalPreference.split(",")[4],
        "love_genre": profile.MusicalPreference.split(",")[5],
        "Motivation_genre": profile.MusicalPreference.split(",")[6],
        "Homesicknes_genre": profile.MusicalPreference.split(",")[7],
        "Melancoly_genre": profile.MusicalPreference.split(",")[8],
        "Frustration_genre": profile.MusicalPreference.split(",")[9],
        "History": profile.Hystorial
    }
    return context

def chat(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")

        if user_input:
            user = request.user
            context = getUserContext(user)

            Salida3 = (
                f"Información del usuario:\n"
                f"Usuario: {context['username']}\n"
                f"Nombre: {context['name']}\n"
                f"Apellido: {context['last_name']}\n"
                f"Email: {context['email']}\n"
                f"Artistas favoritos: {', '.join(context['fav_artists'])}\n"
                f"Géneros musicales preferidos: {', '.join(context['happy_genre'])}, {', '.join(context['SAD_genre'])}, {', '.join(context['Calm_genre'])}, {', '.join(context['Angry_genre'])}, {', '.join(context['Euphoria_genre'])}, {', '.join(context['love_genre'])}, {', '.join(context['Motivation_genre'])}, {', '.join(context['Homesicknes_genre'])}, {', '.join(context['Melancoly_genre'])}, {', '.join(context['Frustration_genre'])}\n"
                f"Última interacción: {context['History']}\n"
                f"Entrada del usuario: {user_input}"
            )

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(Salida3)

            if response and hasattr(response, 'text'):
                response_text = response.text 
                user.Hystorial = response_text
                user.save()
                return JsonResponse({"generated_text": response_text})
            else:
                return JsonResponse({"error": "No se pudo generar contenido."}, status=500)
        else:
            return JsonResponse({"error": "El input del usuario está vacío."}, status=400)
    return render(request, 'chat.html')


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'chattest.html')

def perfil(request):
    if request.user.is_authenticated:
        user = request.user
        usuario_obj = usuario.objects.get(id=user.id)  
        
        if request.method == "POST":
            name = request.POST.get('name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            fav_artists = [request.POST.get(f'fav_artist_{i}') for i in range(9) if request.POST.get(f'fav_artist_{i}')]  # Lista de artistas
            happy_genre = request.POST.get('happy')
            sad_genre = request.POST.get('sad')
            calm_genre = request.POST.get('calm')
            angry_genre = request.POST.get('angry')
            euphoria_genre = request.POST.get('euphoria')
            love_genre = request.POST.get('love')
            motivation_genre = request.POST.get('motivation')
            homesickness_genre = request.POST.get('homesickness')
            melancholy_genre = request.POST.get('melancholy')
            frustration_genre = request.POST.get('frustration')

            genres = [happy_genre, sad_genre, calm_genre, angry_genre, euphoria_genre,
                      love_genre, motivation_genre, homesickness_genre, melancholy_genre, frustration_genre]

            
            usuario_obj.Nombre = name
            usuario_obj.Apellido = last_name
            usuario_obj.Email = email
            usuario_obj.Artistas_FAV = ', '.join(fav_artists)  
            usuario_obj.MusicalPreference = ', '.join(genres)  
            usuario_obj.save()

            
            user.email = email
            user.save()

       
        fav_artists = usuario_obj.Artistas_FAV.split(', ') if isinstance(usuario_obj.Artistas_FAV, str) else usuario_obj.Artistas_FAV
        genres = usuario_obj.MusicalPreference.split(', ') if isinstance(usuario_obj.MusicalPreference, str) else usuario_obj.MusicalPreference

        context = {
            'name': usuario_obj.Nombre,
            'last_name': usuario_obj.Apellido,
            'email': usuario_obj.Email,
            'fav_artists': fav_artists,  
            'genres': genres, 
        }

        return render(request, 'profile.html', context)
    
    else:
        
        return redirect('loginaccount')