from app import app
from flask import render_template
from app import db
from app.models import Song, Play

@app.route('/')
@app.route('/index')
def index():
    s = Song.query.all()
    p = Play.query.all()

    print(s)
    songs = [
        {
        'artist': 'Dubioza kolektiv',
        'songname': 'Himna generacije',
        'album': 'Pjesmice za djecu i odrasle',
        'id':'2mZYQC01utmvwynQZVvplL',
        'address': 'https://open.spotify.com/track/2mZYQC01utmvwynQZVvplL',
        'thumb': 'https://i.scdn.co/image/762af66d1a31d1d68221e3721116ae71a6a339e4',
        'image': 'https://i.scdn.co/image/8c54f79bbed8ac4af7a270786888c26bca930c42',
        'timefrom':'13:37',
        'timeto': '21:37'
        }
    ]
    return render_template('index.html', plays=p)
