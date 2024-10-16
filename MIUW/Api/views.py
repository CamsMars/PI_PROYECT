from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from requests import get, put
from django.http import HttpResponseRedirect
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from .extras import *
import logging
import requests
import json
from django.views.decorators.csrf import csrf_exempt


class AuthenticationURL(APIView):
    def get(self, request, format=None):
        scopes = "playlist-modify-public playlist-modify-private user-modify-playback-state user-read-playback-state streaming"
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
    redirect_url = "http://localhost:8000/about/"
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
            redirect_url = "http://localhost:8000/about/"
            return HttpResponseRedirect(redirect_url)
        else:
            #redirect to AuthenticationURL
            redirect_url = "/spotify/login"
            return HttpResponseRedirect(redirect_url)

logger = logging.getLogger(__name__)


class CreatePlaylist(APIView):
    def post(self, request, format=None):
        session_id = request.session.session_key
        if not is_spotify_authenticated(session_id):
            return HttpResponseRedirect('/spotify/login')

        tokens = get_user_tokens(session_id)
        access_token = tokens.access_token

        playlist_name = request.data.get('name')
        playlist_description = request.data.get('description', '')

        try:
            # Get the authenticated user's ID
            user_response = get(
                'https://api.spotify.com/v1/me',
                headers={
                    'Authorization': f'Bearer {access_token}'
                }
            )
            user_response.raise_for_status()  # Raise an error for bad status codes
            user_data = user_response.json()
            user_id = user_data['id']  # Get the user ID

            # Now create the playlist
            create_playlist_response = post(
                f'https://api.spotify.com/v1/users/{user_id}/playlists',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                },
                json={
                    'name': playlist_name,
                    'description': playlist_description,
                    'public': True
                }
            )
            create_playlist_response.raise_for_status()  # Raise an error for bad status codes
            create_playlist_data = create_playlist_response.json()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(create_playlist_data, status=status.HTTP_201_CREATED)


class ModifyPlaylist(APIView):
    def put(self, request, playlist_id, format=None):
        session_id = request.session.session_key
        if not is_spotify_authenticated(session_id):
            return HttpResponseRedirect('/spotify/login')

        tokens = get_user_tokens(session_id)
        access_token = tokens.access_token

        playlist_name = request.data.get('name')
        playlist_description = request.data.get('description')

        try:
            modify_playlist_response = post(
                f'https://api.spotify.com/v1/playlists/{playlist_id}',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                },
                json={
                    'name': playlist_name,
                    'description': playlist_description,
                    'public': True  # Set to True or False based on your need
                }
            )

            # Check for successful response
            if modify_playlist_response.status_code in [200, 204]:
                return Response({'message': 'Playlist modified successfully'}, status=status.HTTP_200_OK)
            else:
                # Log and return error response from Spotify
                logger.error(f"Error modifying playlist: {modify_playlist_response.status_code}, Response: {modify_playlist_response.text}")
                return Response(modify_playlist_response.json(), status=modify_playlist_response.status_code)

        except Exception as e:
            logger.error(f"Unexpected error occurred: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class SearchSong(APIView):
    def get(self, request, format=None):
        session_id = request.session.session_key
        if not is_spotify_authenticated(session_id):
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_user_tokens(session_id)
        access_token = tokens.access_token

        query = request.query_params.get('query')
        if not query:
            return Response({'error': 'No search query provided'}, status=status.HTTP_400_BAD_REQUEST)

        response = get(
            'https://api.spotify.com/v1/search',
            headers={
                'Authorization': f'Bearer {access_token}',
            },
            params={
                'q': query,
                'type': 'track',
                'limit': 10,  # Limit to 10 results for simplicity
            }
        )

        if response.status_code != 200:
            return Response({'error': 'Failed to search for tracks'}, status=response.status_code)

        return Response(response.json(), status=status.HTTP_200_OK)


class AddSongToPlaylist(APIView):
    def post(self, request, playlist_id):
        tokens = get_user_tokens(request.session.session_key)
        access_token = tokens.access_token

        song_id = request.data.get('song_id')  # Make sure song_id is being received
        if not song_id:
            return JsonResponse({'error': 'No song ID provided'}, status=400)

        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'uris': [f'spotify:track:{song_id}']  # Correct Spotify URI format
        }

        response = post(url, headers=headers, json=data)

        if response.status_code != 201:
            return JsonResponse({'error': response.json()}, status=response.status_code)

        return JsonResponse({'message': 'Song added successfully'}, status=201)


def get_access_token(request):
    session_id = request.session.session_key  # Assuming you have user authentication
    tokens = get_user_tokens(session_id)

    if tokens and tokens.access_token:
        return JsonResponse({'access_token': tokens.access_token})

    return JsonResponse({'error': 'No valid token found'}, status=400)


@csrf_exempt
def play_track(request):
    if request.method == 'PUT':
        logger.info('Received request to play track.')

        session_id = request.session.session_key
        tokens = get_user_tokens(session_id)

        if tokens and tokens.access_token:
            access_token = tokens.access_token
            try:
                data = json.loads(request.body)
                track_uris = data.get('uris', [])
            except json.JSONDecodeError:
                logger.error('Invalid JSON received.')
                return JsonResponse({'error': 'Invalid JSON'}, status=400)

            logger.info(f'Track URIs to play: {track_uris}')

            # Making a request to Spotify API to play the track
            response = requests.put(
                'https://api.spotify.com/v1/me/player/play',
                headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
                json={'uris': track_uris}
            )

            if response.status_code == 204:  # Successful response
                logger.info('Successfully started playing track.')
                return JsonResponse({'status': 'Playing track'})
            else:
                error_response = response.json()
                logger.error(f'Error from Spotify API: {error_response}')
                return JsonResponse({'error': error_response}, status=response.status_code)

        logger.warning('No access token found for user.')
        return JsonResponse({'error': 'No access token available'}, status=400)

    logger.error('Invalid request method: %s', request.method)
    return JsonResponse({'error': 'Invalid request'}, status=400)
