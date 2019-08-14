import spotipy

def get_playlists(access_token):
	sp = spotipy.client.Spotify(auth=access_token)
	return sp.current_user_playlists()['items']

def get_song_features(access_token, playlist_id):
	sp = spotipy.client.Spotify(auth=access_token)
	user_id = sp.me()['id']
	playlist = sp.user_playlist(user_id, playlist_id, fields=['tracks'])
	num_tracks = playlist['tracks']['total']
	num_tracks_so_far = 0
	tracks = []
	while num_tracks_so_far < num_tracks:
		tracks += sp.user_playlist_tracks(user_id, playlist_id=playlist_id, offset=num_tracks_so_far)['items']
		num_tracks_so_far += 100
	uris, artists, titles =  [], [], []
	for track in tracks:
		uris.append(track['track']['uri'])
		artists.append(track['track']['artists'][0]['name'])
		titles.append(track['track']['name'])
	return artists, titles, get_audio_features(uris, sp)
def get_audio_features(tracks, sp):
	num_tracks = len(tracks)
	num_extracted = 0
	feature_dict = []
	while num_extracted < num_tracks:
		if (num_tracks - num_extracted) // 50 > 0:
			feature_dict += sp.audio_features(tracks[num_extracted:num_extracted + 50])
			num_extracted += 50
		else:
			feature_dict += sp.audio_features(tracks[num_extracted:])
			num_extracted = num_tracks
	return feature_dict