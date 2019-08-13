from django.shortcuts import render, redirect 
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import os
from . import spotify
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_url = 'http://127.0.0.1:8000/visualization/callback'
scope = 'playlist-read-private user-read-private'

# Create your views here.
oauth = SpotifyOAuth(client_id, client_secret, redirect_url, scope=scope)

def index(request):
	return render(request, 'index.html')

def login(request):
	auth_url = oauth.get_authorize_url()
	return redirect(auth_url)

def callback(request):
	access_token = request.session.get('access_token', False)
	if not access_token:
		code = request.GET['code']
		access_token = oauth.get_access_token(code)
		request.session['access_token'] = access_token
	playlists = spotify.get_playlist(access_token['access_token'])
	context = {'playlists': playlists}
	if access_token:
		return render(request, 'visualization/callback.html', context=context)
	else:
		return render(request, 'index.html')