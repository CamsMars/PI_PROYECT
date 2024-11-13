import requests
from Api.models import PLAYLIST, usuario


def create_playlist(access_token, name, description, user_id, user):
    """Create a playlist for the given Spotify user ID."""
    response = requests.post(
        f'https://api.spotify.com/v1/users/{user_id}/playlists',
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
    response.raise_for_status() # Ensure the request was successful
    playlist_data = response.json()

    playlist_name = playlist_data['name']
    playlist_id = playlist_data['id']
    playlist_url = playlist_data['external_urls']['spotify']

    profile = usuario.objects.get(id=user)

    save_playlist(profile, playlist_name, playlist_id, playlist_url)

    return playlist_data  # Return playlist data

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
    track_id = tracks_data[0]['id'] if tracks_data else None
    return track_id.strip("'") if track_id else None

def add_song_to_playlist(access_token, playlist_id, track_id):
    """Add a list of track IDs to a specified playlist."""
    print(track_id)
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'uris': [f'spotify:track:{track_id}']  # Correct Spotify URI format
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Ensure the request was successful
    return response.json()  # Return response data if needed


def save_playlist(user, playlist_name, playlist_id, playlist_link=None):
    # Check if the playlist already exists for the user
    existing_playlist = PLAYLIST.objects.filter(ID_USER=user, NOMBRE_PLAYLIST=playlist_name).first()
    if not existing_playlist:
        # Create a new playlist entry
        playlist = PLAYLIST(
            ID_USER=user,
            LINK_PLAYLIST=playlist_link,
            NOMBRE_PLAYLIST=playlist_name,
            ID_PLAYLIST=playlist_id,
        )
        playlist.save()
        return playlist
    else:
        return existing_playlist  # Return existing if found


def get_playlist_id_by_name(user, playlist_name):
    try:
        # Look for a playlist with the given name for the specified user
        playlist = PLAYLIST.objects.get(ID_USER=user, NOMBRE_PLAYLIST=playlist_name)
        return playlist.ID_PLAYLIST
    except PLAYLIST.DoesNotExist:
        return None  # No playlist found with that name