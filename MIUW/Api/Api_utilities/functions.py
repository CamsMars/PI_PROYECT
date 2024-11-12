import requests
from Api.credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from Api.models import SpotifyProfile

def create_playlist(access_token, name="My Playlist", description="A new playlist"):
    """Create a playlist for the given Spotify user ID."""
    response = requests.post(
        f'https://api.spotify.com/v1/users/me/playlists',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json={
            'name': name,
            'description': description,
            'public': True
        }
    )
    response.raise_for_status()  # Ensure the request was successful
    return response.json()  # Return playlist data

def search_song(access_token, query):
    """Search for songs on Spotify by query and return a list of track IDs."""
    response = requests.get(
        'https://api.spotify.com/v1/search',
        headers={'Authorization': f'Bearer {access_token}'},
        params={
            'q': query,
            'type': 'track',
            'limit': 10
        }
    )
    response.raise_for_status()
    tracks_data = response.json()['tracks']['items']
    return [track['id'] for track in tracks_data]  # List of track IDs

def add_song_to_playlist(access_token, playlist_id, track_ids):
    """Add a list of track IDs to a specified playlist."""
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {'uris': [f'spotify:track:{track_id}' for track_id in track_ids]}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Ensure the request was successful
    return response.json()  # Return response data if needed
