import spotipy
from sklearn.manifold import TSNE
from numpy import array

def get_playlists(access_token):
	sp = spotipy.client.Spotify(auth=access_token)
	return sp.current_user_playlists()['items']

def get_song_features(access_token, playlist_id):
	sp = spotipy.client.Spotify(auth=access_token)
	user_id = sp.me()['id']
	playlist = sp.user_playlist(user_id, playlist_id)
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
	features = get_audio_features(uris, sp)
	none_idx = [i for i, item in enumerate(features) if item is None]
	for i in sorted(none_idx, reverse=True):
		del features[i]
		del artists[i]
		del titles[i]
	return artists, titles, features, playlist['name']
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

def get_projection(access_token, playlist_id, features=['danceability', 'acousticness', 'energy', 'instrumentalness', 'valence']):
	artists, titles, data, playlist_name = get_song_features(access_token, playlist_id)
	feature_table = []
	for i in range(len(data)):
		feature_table.append([data[i][k] for k in features])
	projection = TSNE(n_components=2, init='pca').fit_transform(array(feature_table))
	return list(projection[:,0]), list(projection[:,1]), titles, artists, playlist_name

