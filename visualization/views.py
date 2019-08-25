from django.shortcuts import render, redirect 
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import os
from . import spotify
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_url = 'https://playlist-visualizer.herokuapp.com/visualization/callback'
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
	else:
		access_token = oauth.refresh_access_token(request.session['access_token']['refresh_token'])
		request.session['access_token'] = access_token
		request.session.modified = True

	playlists = spotify.get_playlists(access_token['access_token'])
	context = {'playlists': playlists}
	if access_token:
		return render(request, 'visualization/callback.html', context=context)
	else:
		return render(request, 'index.html')

def visualize(request, id):
	access_token = request.session.get('access_token', False)
	if not access_token:
		code = request.GET['code']
		access_token = oauth.get_access_token(code)
		request.session['access_token'] = access_token
	else:
		access_token = oauth.refresh_access_token(request.session['access_token']['refresh_token'])
		request.session['access_token'] = access_token
		request.session.modified = True
	artists, titles, features, _, _ = spotify.get_song_features(access_token['access_token'], id)
	keys = features[0].keys()
	context = {'keys': keys, 'zip_list': zip(features, artists, titles)}
	return render(request, 'visualization/visualize.html', context=context)

def feature_context(request):
	return render(request, 'visualization/feature_context.html')

def plot(request, id):
	access_token = request.session.get('access_token', False)
	if not access_token:
		code = request.GET['code']
		access_token = oauth.get_access_token(code)
		request.session['access_token'] = access_token
	else:
		access_token = oauth.refresh_access_token(request.session['access_token']['refresh_token'])
		request.session['access_token'] = access_token
		request.session.modified = True
	x_projection, y_projection, titles, artists, playlist_name, ids = spotify.get_projection(access_token['access_token'], id)
	for i in range(len(titles)):
	 	titles[i] = artists[i] + ": " + titles[i]
	x_offset = abs(max(x_projection) - min(x_projection))/5
	y_offset = abs(max(y_projection) - min(y_projection))/5
	context = {
	'x_max': max(x_projection) + x_offset,
	'y_max': max(y_projection) + y_offset,
	'x_min': min(x_projection) - x_offset,
	'y_min': min(y_projection) - y_offset,
	'zip_list': zip(titles, x_projection, y_projection, ids),
	'playlist_name': playlist_name,
	}
	return render(request, 'visualization/plot.html', context=context)

