from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import response
from requests import Request, post
from django.http import HttpResponseRedirect
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from .extras import *


# Create your views here.

class AuthenticationURL(APIView):
    def get(self, request, format  =None):
        #Pick a required scope for the user from spotify documentation
        scopes = "playlist-modify-public"
        url = request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url
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
    redirect_url = ""
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