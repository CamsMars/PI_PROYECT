from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from requests import get
from django.http import HttpResponseRedirect
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from .extras import *


# Create your views here.

class AuthenticationURL(APIView):
    def get(self, request, format=None):
        scopes = "playlist-modify-public playlist-modify-private"
        url = f"https://accounts.spotify.com/authorize?scope={scopes}&response_type=code&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}"
        return HttpResponseRedirect(url)

def spotify_redirect(request, format = None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        return error

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    authKey = request.session.session_key
    if not request.session.exists(authKey):
        request.session.create()
        authKey = request.session.session_key

    update_or_create_tokens(authKey, access_token, refresh_token, expires_in, token_type)

    #Create a redirect url for the required response
    redirect_url = "http://localhost:8000/chat"
    return HttpResponseRedirect(redirect_url)

class CheckAuthentication(APIView):
    def get(self, request, format=None):
        key = self.request.session.session_key
        if not self.request.session.exists(key):
            self.request.session.create()
            key = self.request.session.session_key

        auth_status = is_spotify_authenticated(key)

        if auth_status:
            #will be redirect to the credentials
            redirect_url = ""
            return HttpResponseRedirect(redirect_url)
        else:
            #redirect to AuthenticationURL
            redirect_url = ""
            return HttpResponseRedirect(redirect_url)

class CreatePlaylist(APIView):
    def post(self, request, format=None):
        session_id = request.session.session_key
        if not is_spotify_authenticated(session_id):
            return HttpResponseRedirect('/spotify/login')

        tokens = get_user_tokens(session_id)
        access_token = tokens.access_token

        playlist_name = request.data.get('name')
        playlist_description = request.data.get('description', '')

        user_id = "your_spotify_user_id"  # Replace with the actual user ID

        try:
            create_playlist_response = post(
                f'https://api.spotify.com/v1/users/{user_id}/playlists',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                },
                json={
                    'name': playlist_name,
                    'description': playlist_description,
                    'public': False
                }
            )
            create_playlist_response.raise_for_status()  # Raise an error for bad status codes
            create_playlist_data = create_playlist_response.json()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(create_playlist_data, status=status.HTTP_201_CREATED)

class ModifyPlaylist(APIView):
    def post(self, request, playlist_id, format=None):
        session_id = request.session.session_key
        if not is_spotify_authenticated(session_id):
            return HttpResponseRedirect('/spotify/login')

        tokens = get_user_tokens(session_id)
        access_token = tokens.access_token

        playlist_name = request.data.get('name')
        playlist_description = request.data.get('description')

        modify_playlist_response = post(
            f'https://api.spotify.com/v1/playlists/{playlist_id}',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            json={
                'name': playlist_name,
                'description': playlist_description,
                'public': False
            }
        ).json()

        return Response(modify_playlist_response, status=status.HTTP_200_OK)

class ListPlaylists(APIView):
    def get(self, request, format=None):
        session_id = request.session.session_key
        if not is_spotify_authenticated(session_id):
            return HttpResponseRedirect('/spotify/login')

        tokens = get_user_tokens(session_id)
        access_token = tokens.access_token

        try:
            playlists_response = get(
                'https://api.spotify.com/v1/me/playlists',
                headers={
                    'Authorization': f'Bearer {access_token}'
                }
            )
            playlists_response.raise_for_status()  # Raise an error for bad status codes
            playlists_data = playlists_response.json()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(playlists_data, status=status.HTTP_200_OK)