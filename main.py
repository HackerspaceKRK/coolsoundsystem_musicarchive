#!/usr/bin/env python3

from paho.mqtt.client import Client
import json
import time

last_song = {
    'data': {},
    'timestamps': {
        'lastsong_start' : 0,
        'lastsong_current' : 0
    }
}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("music/#")

def handle_song(data, timestamp, lastsong):
    if lastsong['data'] == {}:
        lastsong['data'] = data
    else:
        if data == lastsong['data']:
            lastsong['timestamps']['lastsong_current'] = timestamp
        else:
            print(lastsong['timestamps'])
            print(float(lastsong['timestamps']['lastsong_current']) - float(lastsong['timestamps']['lastsong_start']))
            print('Artysta: ' + data['artist'] + ', Tytuł: ' + data['title'] + ', Album: ' + data['album'])
            print('ID: ' + data['content_id'] + ', Adres obrazka: ' + data['image'])
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
        data.update(acquire_data(lambda: {'image': payload['data']['media_metadata']['images'][0]['url']}, {'image': 'https://sound.at.hskrk.pl/img/silence.jpg'}))

        handle_song(data, time.time(), last_song)
    except:
#       print(payload)
        pass

client = Client()
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add('music/chromecast/playing', on_message_music)

client.connect("rudy.at.hskrk.pl", 1883, 60)

client.loop_forever()
