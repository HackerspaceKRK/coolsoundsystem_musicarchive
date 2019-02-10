from app import db

class Song(db.Model):
    songid = db.Column(db.String(64), primary_key=True)
    artist = db.Column(db.String(64))
    songname = db.Column(db.String(64))
    album = db.Column(db.String(64))
    player_specific_id = db.Column(db.String(64), index=True, unique=True)
    thumb = db.Column(db.String(64))
    image = db.Column(db.String(64))

    def __repr__(self):
        return '<Song {}>'.format(self.songid)

class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songid = db.Column(db.String(64), db.ForeignKey('song.songid'), nullable=False, index=True)
    timefrom = db.Column(db.String(64), index=True)
    timeto = db.Column(db.String(64), index=True)


    def __repr__(self):
        return '<Play {}>'.format(self.id)

    # songs = [
    #     {
    #     'artist': 'Dubioza kolektiv',
    #     'songname': 'Himna generacije',
    #     'album': 'Pjesmice za djecu i odrasle',
    #     'id':'2mZYQC01utmvwynQZVvplL',
    #     'address': 'https://open.spotify.com/track/2mZYQC01utmvwynQZVvplL',
    #     'thumb': 'https://i.scdn.co/image/762af66d1a31d1d68221e3721116ae71a6a339e4',
    #     'image': 'https://i.scdn.co/image/8c54f79bbed8ac4af7a270786888c26bca930c42',
    #     'timefrom':'13:37',
    #     'timeto': '21:37'
    #     }
    # ]
