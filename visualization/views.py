from django.shortcuts import render, redirect 
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import os
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_url = 'http://127.0.0.1:8000/visualization/callback'
username = '1177903028'
scope = 'playlist-read-private'

# Create your views here.
oauth = SpotifyOAuth(client_id, client_secret, redirect_url)

def index(request):
	return render(request, 'index.html')

def test(request):
	auth_url = oauth.get_authorize_url()
	return redirect(auth_url)

def callback(request):
	code = request.GET['code']
	#code = js['code']
	access_token = oauth.get_access_token(code)
	if access_token:
		return render(request, 'test_page.html')
	else:
		return render(request, 'index.html')