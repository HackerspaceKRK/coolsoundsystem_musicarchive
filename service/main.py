#!/usr/bin/env python3

from paho.mqtt.client import Client
import json
import time
import config
import hashlib

idhasher = hashlib.sha1()
last_song = {
    'data': {},
    'timestamps': {
        'lastsong_start' : 0,
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
            songdict = {
                'songid': data['id'],
                'artist': data['artist'],
                'songname': data['title'],
                'album': data['album'],
                'player_specific_id': data['content_id'],
                'thumb': data['images'][64],
                'image': data['images'][300] if 300 in data['images'] else data['images'][64]
            }

            playdict = {
                'songid': data['id'],
                'timefrom': float(lastsong['timestamps']['lastsong_start']),
                'timeto': float(lastsong['timestamps']['lastsong_current']),
            }
            # print(lastsong['timestamps'])
            # print(float(lastsong['timestamps']['lastsong_current']) - float(lastsong['timestamps']['lastsong_start']))
            print('-------------')
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
#        kek = json.loads(msg.payload)
        print(json.dumps(kek, indent=4, sort_keys=True))
    except:
        pass

def acquire_data(dataToAcquire, noDataComm):
    try:
        result = dataToAcquire()
    except:
        result = noDataComm
    return result


def on_message_music(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        data = {}

        data.update(acquire_data(lambda: {'title': payload['data']['media_metadata']['title']}, {'title': 'Brak danych'}))
        data.update(acquire_data(lambda: {'artist': payload['data']['media_metadata']['artist']}, {'artist': 'Brak danych'}))
        data.update(acquire_data(lambda: {'album': payload['data']['media_metadata']['albumName']}, {'album': 'Brak danych'}))
        data.update(acquire_data(lambda: {'content_id': payload['data']['content_id']}, {'content_id': 'Brak danych'}))
        data.update(acquire_data(lambda: {'images': payload['data']['media_metadata']['images']}, {'images': []}))

        imagearray = data['images']
        imagedict = {}
        if len(imagearray) != 0:
            for image in imagearray:
                    imagedict.update({image['height']: image['url']})

            data['images'] = imagedict

        if data['content_id'] is not None:
            data.update({'id': hashlib.sha1(data['content_id'].encode('utf-8')).hexdigest()})

        handle_song(data, time.time(), last_song)
    except Exception as e:
        print("Exception: " + str(e))
        pass

client = Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add(config.SPECIFIC_TOPIC, on_message_music)

client.connect(config.SERVER_ADDRESS, 1883, 60)

client.loop_forever()
