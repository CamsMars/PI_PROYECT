"""
URL configuration for MIUW project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MIUWApp import views as MIUWApp_views
from Api import views as Api_views
from AcountService import views as ACviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MIUWApp_views.home, name='home'),
    path('about/', MIUWApp_views.about, name='chattest'),

    path('chat/', MIUWApp_views.chat, name='chat'),
    path('profile/',MIUWApp_views.perfil, name='profile'),

    path('signupaccount/', ACviews.signupaccount, name='signupaccount'),
    path('logout/', ACviews.logoutaccount, name='logoutaccount'),
    path('login/', ACviews.loginaccount, name='loginaccount'),

    path('spotify/login', Api_views.AuthenticationURL.as_view(), name='spotify-login'),
    path('spotify/redirect', Api_views.spotify_redirect, name='spotify-redirect'),
    path('spotify/check-auth', Api_views.CheckAuthentication.as_view(), name='spotify-check-auth'),
    path('spotify/create-playlist', Api_views.CreatePlaylist.as_view(), name='create-playlist'),
    path('spotify/modify-playlist/<str:playlist_id>', Api_views.ModifyPlaylist.as_view(), name='modify-playlist'),
    path('spotify/list-playlists', Api_views.ListPlaylists.as_view(), name='list-playlists'),
    path('spotify/search-song/', Api_views.SearchSong.as_view(), name='search-song'),
    path('spotify/add-song-to-playlist/<str:playlist_id>/', Api_views.AddSongToPlaylist.as_view(), name='add-song-to-playlist'),
    path('spotify/get-access-token', Api_views.get_access_token, name='get-access-token'),
    path('spotify/play-track', Api_views.play_track, name='play-track'),
]
