from app import db

class Song(db.Model):
    songid = db.Column(db.String(64), primary_key=True)
    artistid = db.Column(db.String(64), db.ForeignKey('artist.artistid'), nullable=False, index=True) # one artist to many songs
    songname = db.Column(db.String(64))
    albumid = db.Column(db.String(64), db.ForeignKey('album.albumid'), nullable=False, index=True) # one album to many songs
    player_specific_id = db.Column(db.String(64), index=True, unique=True)
    plays = db.relationship('Play', backref='track', lazy='dynamic') # many plays to one song

    def __repr__(self):
        return '<Song {}>'.format(self.songid)

    def data(self):
        return {
                    'songid': self.songid,
                    'artistid': self.artistid,
                    'songname': self.songname,
                    'albumid': self.albumid,
                    'player_specific_id': self.player_specific_id,
                }

class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songid = db.Column(db.String(64), db.ForeignKey('song.songid'), nullable=False, index=True)
    timefrom = db.Column(db.String(64), index=True)
    timeto = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Play {}>'.format(self.id)

    def data(self):
        return {
                    'id': self.id,
                    'songid': self.songid,
                    'timefrom': self.timefrom,
                    'timeto': self.timeto
                }

class Artist(db.Model):
    artistid = db.Column(db.String(64), primary_key=True)
    artistname = db.Column(db.String(64), index=True, unique=True)
    albums = db.relationship('Album', backref='artist', lazy='dynamic') # many albums to one artist
    songs = db.relationship('Song', backref='artist', lazy='dynamic') # many songs to one artist

    def __repr__(self):
        return '<Artist {}>'.format(self.id)

    def data(self):
        return {
                    'artistid': self.artistid,
                    'artistname': self.artistname
                }

class Album(db.Model):
    albumid = db.Column(db.String(64), primary_key=True)
    albumname = db.Column(db.String(64), index=True, unique=True)
    artistid = db.Column(db.String(64), db.ForeignKey('artist.artistid'), nullable=False, index=True) # one artist to many albums
    cover = db.Column(db.String(64), index=True)
    songs = db.relationship('Song', backref='album', lazy='dynamic') # many songs to one album

    def __repr__(self):
        return '<Album {}>'.format(self.id)

    def data(self):
        return {
                    'albumid': self.albumid,
                    'albumname': self.albumname
                    'cover': self.cover
                }



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
