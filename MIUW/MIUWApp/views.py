import os
import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Api.models import *
from django.contrib.auth.models import User


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def chat(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")

        if user_input:

            user=request.user
            SUARIO=usuario.objects.get(id=user)
            artistas_fav = SUARIO.Artistas_FAV  # Cadena con los artistas favoritos
            generos = SUARIO.MusicalPreference
            Hystory=SUARIO.Hystorial

            Salida3=f"soy {user.username} Mi historial de artistas favoritos es: {artistas_fav}.Los géneros musicales que más me gustan son: {generos}que estan oredenados segun mis sentimientos: Happy,Sad,Calm,Angry,Euphoria,Love,Motivation,Homesickness,Melancoly,Frustration. entonces:   {user_input}   aqui te añado nuestro historial:  {Hystory}"
            #print(Salida3)# de Esta manera se puede cargar el historial a la IA

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(Salida3)

            SUARIO.Hystorial = ', '.join(response)
            SUARIO.save()

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


def perfil(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            name = request.POST.get('name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            fav_artists = [request.POST.get(f'fav_artist_{i}') for i in range(10)]
            happy_genre = request.POST.get('happy')
            SAD_genre = request.POST.get('sad')
            Calm_genre = request.POST.get('calm')
            Angry_genre = request.POST.get('angry')
            Euphoria_genre = request.POST.get('euphoria')
            love_genre = request.POST.get('love')
            Motivation_genre = request.POST.get('motivation')
            Homesicknes_genre = request.POST.get('homesickness')
            Melancoly_genre = request.POST.get('melancholy')
            Frustration_genre = request.POST.get('frustration')

            #print(f"Form data received: {name}, {last_name}, {email}, {fav_artists}, {happy_genre}, {SAD_genre}, {Calm_genre}, {Angry_genre}, {Euphoria_genre}, {love_genre}, {Motivation_genre}, {Homesicknes_genre}, {Melancoly_genre}, {Frustration_genre}")

            Generos = [happy_genre, SAD_genre, Calm_genre, Angry_genre, Euphoria_genre,
                       love_genre, Motivation_genre, Homesicknes_genre, Melancoly_genre, Frustration_genre]

            #print(f"Genres list: {Generos}")

        
            user = request.user
            
            usuario_obj = usuario.objects.get(id=user)

            
            usuario_obj.Nombre = name
            usuario_obj.Apellido = last_name
            usuario_obj.Email = email
            

            
            usuario_obj.Artistas_FAV = ', '.join(fav_artists)

            usuario_obj.MusicalPreference = ', '.join(Generos)

            usuario_obj.save()  
            user.email = email
            user.save() 

        return render(request, 'profile.html')
    else:
        # Si el usuario no está autenticado, redirigir al login
        return redirect('loginaccount')