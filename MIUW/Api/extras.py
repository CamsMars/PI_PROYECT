from datetime import timedelta

from django.utils import timezone
from requests import post

from .credentials import CLIENT_ID, CLIENT_SECRET
from .models import Token

BASE_URL = 'https://api.spotify.com/v1/me/'

def check_tokens(session_id):
    tokens = Token.objects.filter(user=session_id)
    if tokens:
        return tokens[0]
    else:
        return None

def update_or_create_tokens(session_id, access_token, refresh_token, expires_in, token_type):
    tokens = check_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = Token(
            user = session_id,
            access_token = access_token,
            refresh_token = refresh_token,
            expires_in = expires_in,
            token_type = token_type
        )
        tokens.save()

def is_spotify_authenticated(session_id):
    tokens = check_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
        return True
    return False

def refresh_spotify_token(session_id):
    tokens = get_user_tokens(session_id)
    refresh_token = tokens.refresh_token

    response = post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    )

    response_data = response.json()  # Convert response to dictionary

    access_token = response_data.get('access_token')
    token_type = response_data.get('token_type')
    expires_in = response_data.get('expires_in')

    update_or_create_tokens(session_id, access_token, refresh_token, expires_in, token_type)

def get_user_tokens(session_id):
    tokens = Token.objects.filter(user=session_id)
    if tokens.exists():
        return tokens.first()
    return None