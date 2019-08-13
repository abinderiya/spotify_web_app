import spotipy

def get_playlist(access_token):
	sp = spotipy.client.Spotify(auth=access_token)
	return sp.current_user_playlists()['items']