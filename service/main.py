#!/usr/bin/env python3

from paho.mqtt.client import Client
from spotipy.oauth2 import SpotifyClientCredentials
import json
import time
import config
import hashlib
import sqlite3
import spotipy
import config

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

conn = sqlite3.connect(config.DB_PATH)
print(conn)
conn.set_trace_callback(print)
c = conn.cursor()

last_song = {
    'data': {},
    'timestamps': {
        'lastsong_start' : time.time(),
        'lastsong_current' : 0
    }
}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(config.GENERAL_TOPIC)

def handle_song(data, timestamp, lastsong):
    if lastsong['data'] == {}:
        lastsong['data'] = data
    else:
        if data == lastsong['data']:
            lastsong['timestamps']['lastsong_current'] = timestamp
        else:
            print(lastsong['data'])
            songdict = {
                'songid': str(lastsong['data']['id']),
                'artistid': str(lastsong['data']['artistid']),
                'songname': str(lastsong['data']['title']),
                'albumid': str(lastsong['data']['albumid']),
                'player_specific_id': lastsong['data']['content_id'],
                'image': str(lastsong['data']['image']),
            }

            playdict = {
                'songid': lastsong['data']['id'],
                'timefrom': float(lastsong['timestamps']['lastsong_start']),
                'timeto': float(lastsong['timestamps']['lastsong_current']),
            }

            albumdict = {
                'albumid': lastsong['data']['albumid'],
                'albumname': lastsong['data']['album'],
                'artistid': lastsong['data']['artistid'],
                'cover': lastsong['data']['image'],
                'popularity': None,
                'release_date': None,
                'total_tracks': None
            }

            artistdict = {
                'artistid': lastsong['data']['artistid'],
                'artistname': lastsong['data']['artist'],
                'image': None,
                'popularity':None,
            }

            if 'discovered_client' in lastsong['data']:
                if lastsong['data']['discovered_client'] == 'spotify':
                    spotify_trackdata = sp.track(lastsong['data']['content_id'])
                    spotify_albumdata = sp.album(spotify_trackdata['album']['id'])
                    spotify_artistdata = sp.artist(spotify_trackdata['artists'][0]['id'])
                    print(spotify_artistdata)
                    spotify_featuredata = sp.audio_features(lastsong['data']['content_id'])
                    spotifydict = {
                        'songid': lastsong['data']['id'],
                        'popularity': spotify_trackdata['popularity'],
                        'track_number': spotify_trackdata['track_number'],
                        'key': spotify_featuredata[0]['key'],
                        'mode': spotify_featuredata[0]['mode'],
                        'acousticness': spotify_featuredata[0]['acousticness'],
                        'danceability': spotify_featuredata[0]['danceability'],
                        'energy': spotify_featuredata[0]['energy'],
                        'instrumentalness': spotify_featuredata[0]['instrumentalness'],
                        'liveness': spotify_featuredata[0]['liveness'],
                        'loudness': spotify_featuredata[0]['loudness'],
                        'speechiness': spotify_featuredata[0]['speechiness'],
                        'valence': spotify_featuredata[0]['valence'],
                        'tempo': spotify_featuredata[0]['tempo']
                    }
                    artistdict['image'] = spotify_artistdata['images'][0]['url']
                    artistdict['popularity'] = spotify_artistdata['popularity']
                    albumdict['popularity'] = spotify_albumdata['popularity']
                    albumdict['release_date'] = spotify_albumdata['release_date']
                    albumdict['total_tracks'] = spotify_albumdata['total_tracks']
                else:
                    spotifydict = None
            else: lastsong['data']['discovered_client'] = ''

            # print(lastsong['timestamps'])
            # print(float(lastsong['timestamps']['lastsong_current']) - float(lastsong['timestamps']['lastsong_start']))
            print('-------------')
            # print(lastsong)

            c.execute("SELECT * FROM song WHERE songid=:songid", songdict)
            songquery = c.fetchone()
            if songquery is None:
                pass
                c.execute("INSERT or REPLACE INTO song(songid, artistid, songname, albumid, player_specific_id) VALUES (:songid, :artistid, :songname, :albumid, :player_specific_id);", songdict)
            else:
                print('song in db, no insert')
                pass

            if lastsong['data']['discovered_client'] == 'spotify' and spotifydict is not None:
                c.execute("SELECT * FROM spotify_song_data WHERE songid=:songid", songdict)
                songspotquery = c.fetchone()
                if songspotquery is None:
                    c.execute("INSERT or REPLACE INTO spotify_song_data(songid, popularity, track_number, key, mode, acousticness, loudness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo) VALUES (:songid, :popularity, :track_number, :key, :mode, :acousticness, :loudness, :danceability, :energy, :instrumentalness, :liveness, :speechiness, :valence, :tempo);", spotifydict)
                else:
                    print('songspotifydata in db, no insert')
                    pass

            c.execute("SELECT * FROM album WHERE albumid=:albumid", albumdict)
            albumquery = c.fetchone()
            if albumquery is None:
                c.execute("INSERT or REPLACE INTO album(albumid, albumname, artistid, cover, popularity, release_date, total_tracks) VALUES (:albumid, :albumname, :artistid, :cover, :popularity, :release_date, :total_tracks);", albumdict)
            else:
                print('album in db, no insert')
                pass

            c.execute("SELECT * FROM artist WHERE artistid=:artistid", artistdict)
            artistquery = c.fetchone()
            if artistquery is None:
                c.execute("INSERT or REPLACE INTO artist(artistid, artistname, image, popularity) VALUES (:artistid, :artistname, :image, :popularity);", artistdict)
            else:
                print('artist in db, no insert')
                pass

            if(playdict['timefrom'] != 0):
                if(playdict['timeto']- playdict['timefrom'] > 1):
                    c.execute("INSERT INTO play(songid, timefrom, timeto) VALUES (:songid, :timefrom, :timeto);", playdict)
                else:
                    print('play too short to save, probably skipping through playlist')
            else:
                print('invalid timefrom')
            conn.commit()
            # print('Artysta: ' + data['artist'] + ', Tytuł: ' + data['title'] + ', Album: ' + data['album'])
            # print('contentID: ' + data['content_id'] + ', Adres miniaturki: ' + data['images'][64]+ ', Adres obrazka: ' + data['images'][300])
            # print('ID: ' + data['id'])
            print(songdict)
            print(playdict)
            lastsong['data'] = data
            lastsong['timestamps']['lastsong_start'] = lastsong['timestamps']['lastsong_current'] = timestamp
        pass


def on_message(client, userdata, msg):
    try:
        kek = json.loads(msg.payload)
        # print(json.dumps(kek, indent=4, sort_keys=True))
    except:
        pass

def acquire_data(dataToAcquire, noDataComm):
    try:
        result = dataToAcquire()
    except:
        result = noDataComm
    return result


def on_message_music(client, userdata, msg):
    # try:
        payload = json.loads(msg.payload.decode('utf-8'))
        data = {}


        data.update(acquire_data(lambda: {'title': payload['data']['media_metadata']['title']}, {'title': 'Brak danych'}))
        data.update(acquire_data(lambda: {'artist': payload['data']['media_metadata']['artist']}, {'artist': 'Brak danych'}))
        data.update(acquire_data(lambda: {'album': payload['data']['media_metadata']['albumName']}, {'album': 'Brak danych'}))
        data.update(acquire_data(lambda: {'content_id': payload['data']['content_id']}, {'content_id': 'Brak danych'}))
        data.update(acquire_data(lambda: {'image': payload['data']['media_metadata']['images'][0]['url']}, {'image': config.SILENT_IMAGE_SMALL}))

        if data['content_id'] is not None:
            data.update({'id': hashlib.sha1(data['content_id'].encode('utf-8')).hexdigest()})
            if 'spotify' in str(data['content_id']):
                data['discovered_client'] = 'spotify'
            elif 'soundcloud' in str(data['content_id']):
                data['discovered_client'] = 'soundcloud'
            else:
                data.update({'discovered_client': ''})
        else:
            data.update({'id': 'noid'})

        if data['artist'] is not None:
            data.update({'artistid': hashlib.sha1(data['artist'].encode('utf-8')).hexdigest()})
        else:
            data.update({'artistid': 'noid'})

        if data['album'] is not None:
            data.update({'albumid': hashlib.sha1(data['album'].encode('utf-8')).hexdigest()})
        else:
            data.update({'albumid': 'noid'})

        handle_song(data, time.time(), last_song)


    # except Exception as e:
    #     print("Exception: " + str(e))
    #     pass

client = Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add(config.SPECIFIC_TOPIC, on_message_music)

client.connect(config.SERVER_ADDRESS, 1883, 60)

client.loop_forever()
