import os
import re

import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render, redirect
from requests import get

from Api.Api_utilities import create_playlist, search_song, add_song_to_playlist, get_playlist_id_by_name
from Api.extras import *
from Api.models import *

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

            Salida = (
                f"Rol: Eres MIUW un asistente virtual que ayuda a los usuarios a recibir recomendaciones musicales dependiendo de sus gustos y emociones actuales, cuando un usuario te diga como se sienta actua de manera apropiada y recomiendale una lista de 10 canciones para acompañar su estado de animo"
                f"Información del usuario:\n"
                f"Usuario: {context['username']}\n"
                f"Nombre: {context['name']}\n"
                f"Apellido: {context['last_name']}\n"
                f"Email: {context['email']}\n"
                f"Artistas favoritos: {', '.join(context['fav_artists'])}\n"
                f"Géneros musicales preferidos: {', '.join(context['happy_genre'])}, {', '.join(context['SAD_genre'])}, {', '.join(context['Calm_genre'])}, {', '.join(context['Angry_genre'])}, {', '.join(context['Euphoria_genre'])}, {', '.join(context['love_genre'])}, {', '.join(context['Motivation_genre'])}, {', '.join(context['Homesicknes_genre'])}, {', '.join(context['Melancoly_genre'])}, {', '.join(context['Frustration_genre'])}\n"
                f"Última interacción: {context['History']}\n"
                f"Determina la intencion del usuario:\n"
                f"En caso de agregar o buscar canciones ten presente que maximo debes agregar 10\n"
                f"Consulta del Usuario: {user_input}\n"
                f"Responde '1' si el usuario desea crear una playlist, junto con el nombre de la playlist y la descripcion si se especifican, antes de usar esta respuesta, verifica que el usuario no te este pidiendo canciones o musica, si es asi usa la respuesta 4 de manera acorde.\n"
                f"Si no se especifica un nombre y una descripcion inventa unos y responde con esos.\n"
                f"Escribe tu respuesta como:\n"
                f"'1 - Nombre: <nombre_playlist>, Descripcion: <descripcion>'\n"
                f"Responde '2' si el usuario desea buscar una cancion, junto con el nombre de la cancion o las canciones si se especifican.\n"
                f"Si no se especifica una cancion pero si un artista busca canciones de ese artista.\n"
                f"Escribe tu respuesta como:\n"
                f"'2 - Canciones: <cancion1>, <cancion2>, <cancion3>, ...'\n"
                f"Responde '3' si el usuario desea agregar una cancion a una playlist, junto con el nombre de la cancion y el nombre de la playlist si se especifican.\n"
                f"Escribe tu respuesta como:\n"
                f"'3 - Cancion: <nombre_cancion>, Playlist: <nombre_playlist>'\n"
                f"Responde '4' si el usuario desea crear una playlist con multiples canciones, junto con el nombre de la playlist y las canciones si se especifican.\n"
                f"Si no se especifica un nombre y canciones inventa unos y responde con esos y busca canciones que vayan acorde a la playlist, puedes usar la informacion de los gustos del usuario para esto.\n"
                f"No incluyas el nombre del artista solo de la cancion"
                f"Escribe tu respuesta como:\n"
                f"'4 - Nombre: <nombre_playlist>, Descripcion: <descripcion_playlist>, Canciones: <cancion1>, <cancion2>, <cancion3>, ...'\n"
                f"De otra forma, Responde 'No'."
            )

            model = genai.GenerativeModel("gemini-1.5-flash")
            ai_response = model.generate_content(Salida)

            response_text = ai_response.text

            tokens = get_user_tokens(request.session.session_key)
            access_token = tokens.access_token

            print(response_text)

            if "No" not in user_input:
                regular_expression_call(response_text, user, access_token)

            Salida3 = (
                f"Rol: Eres MIUW un asistente virtual que ayuda a los usuarios a recibir recomendaciones musicales dependiendo de sus gustos y emociones actuales, cuando un usuario te diga como se sienta actua de manera apropiada y recomiendale una lista de 10 canciones para acompañar su estado de animo"
                f"Información del usuario:\n"
                f"Usuario: {context['username']}\n"
                f"Nombre: {context['name']}\n"
                f"Apellido: {context['last_name']}\n"
                f"Email: {context['email']}\n"
                f"Artistas favoritos: {', '.join(context['fav_artists'])}\n"
                f"Géneros musicales preferidos: {', '.join(context['happy_genre'])}, {', '.join(context['SAD_genre'])}, {', '.join(context['Calm_genre'])}, {', '.join(context['Angry_genre'])}, {', '.join(context['Euphoria_genre'])}, {', '.join(context['love_genre'])}, {', '.join(context['Motivation_genre'])}, {', '.join(context['Homesicknes_genre'])}, {', '.join(context['Melancoly_genre'])}, {', '.join(context['Frustration_genre'])}\n"
                f"Última interacción: {context['History']}\n"
                f"Entrada del usuario: {user_input}"
                f"Esta es tu respuesta anterior, en caso de que el usuario te haya pedido que crearas una playlist con canciones, los nombres de las caciones que agregaste a la playlist, el nombre o el nombre y la descripcion de la playlist puede estar ahi, para que lo tengas presente en la respuesta que le daras al usuario.\n"
                f"Respuesta anterior: {response_text}\n"
                f"Si en la respuesta anterior hay un nombre de playlist, descripcion o canciones, mencionales esos al usuario diciendole que es la playlist que le has creado con las canciones, de otra manera genera una respuesta acorde al contexto de la entrada del usuario"
            )

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(Salida3)

            if response and hasattr(response, 'text'):
                user.Hystorial = response.text
                user.save()
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

            Generos = [happy_genre, SAD_genre, Calm_genre, Angry_genre, Euphoria_genre,
                       love_genre, Motivation_genre, Homesicknes_genre, Melancoly_genre, Frustration_genre]
        
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


def regular_expression_call(response_text, user, access_token):
    if "1" in response_text:
        # Extract the playlist name and description from the response text
        name_match = re.search(r'Nombre: ([^,]+)', response_text)
        description_match = re.search(r'Descripcion: (.+)', response_text)

        # Default values if name or description is not provided
        playlist_name = name_match.group(1).strip() if name_match else f"My Playlist {user.id}"
        description = description_match.group(1).strip() if description_match else "User-generated playlist"

        user_response = get(
            'https://api.spotify.com/v1/me',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        user_response.raise_for_status()  # Raise an error for bad status codes
        user_data = user_response.json()
        user_id = user_data['id']

        # Call the create_playlist function
        try:
            result = create_playlist(access_token, playlist_name, description, user_id, user)
            if result:
                return 0
            else:
                return JsonResponse({"error": "Failed to create playlist."}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif "2" in response_text:
        songs = []
        name_match = re.search(r'Canciones: (.+)', response_text)

        if name_match:
            songs_string = name_match.group(1).strip()
            songs = [song.strip() for song in songs_string.split(",")]

        query = []

        for song in songs:
            track_id = search_song(access_token, song)
            query.append(track_id)

        return 0

    elif "3" in response_text:
        cancion_match = re.search(r'Cancion: ([^,]+)', response_text)
        playlist_match = re.search(r'Playlist: (.+)', response_text)

        profile = usuario.objects.get(id=user)

        if playlist_match:
            playlist_name = playlist_match.group(1).strip().strip("'")

        print(playlist_name)

        playlist_id = get_playlist_id_by_name(profile, playlist_name)

        track_id = search_song(access_token, cancion_match.group(1))

        print(playlist_id)

        add_song_to_playlist(access_token, playlist_id, track_id)

        return 0

    elif "4" in response_text:
        name_match = re.search(r'Nombre: ([^,]+)', response_text)
        description_match = re.search(r'Descripcion: (.+)', response_text)
        songs_match = re.search(r'Canciones: (.+)', response_text)

        playlist_name = name_match.group(1).strip() if name_match else f"My Playlist {user.id}"
        description = description_match.group(1).strip() if description_match else "User-generated playlist"
        songs = [song.strip() for song in songs_match.group(1).split(",")]

        user_response = get(
            'https://api.spotify.com/v1/me',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        user_response.raise_for_status()
        user_data = user_response.json()
        user_id = user_data['id']

        try:
            result = create_playlist(access_token, playlist_name, description, user_id, user)
            if result:
                for song in songs:
                    print(song)
                    track_id = search_song(access_token, song)
                    add_song_to_playlist(access_token, result['id'], track_id)
                return 0
            else:
                return JsonResponse({"error": "Failed to create playlist."}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)