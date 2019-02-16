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
    image = db.Column(db.String(64), index=True)
    popularity = db.Column(db.Integer())

    def __repr__(self):
        return '<Artist {}>'.format(self.artistid)

    def data(self):
        return {
                    'artistid': self.artistid,
                    'artistname': self.artistname,
                    'image': self.image,
                    'popularity': self.popularity
                }

class Album(db.Model):
    albumid = db.Column(db.String(64), primary_key=True)
    albumname = db.Column(db.String(64), index=True, unique=True)
    artistid = db.Column(db.String(64), db.ForeignKey('artist.artistid'), nullable=False, index=True) # one artist to many albums
    cover = db.Column(db.String(64), index=True)
    songs = db.relationship('Song', backref='album', lazy='dynamic') # many songs to one album
    popularity = db.Column(db.Integer())
    release_date = db.Column(db.String(64))
    total_tracks = db.Column(db.Integer())

    def __repr__(self):
        return '<Album {}>'.format(self.albumid)

    def data(self):
        return {
                    'albumid': self.albumid,
                    'albumname': self.albumname,
                    'artistid': self.artistid,
                    'cover': self.cover,
                    'popularity': self.popularity,
                    'release_date': self.release_date,
                    'total_tracks': self.total_tracks
                }

class SpotifySongData(db.Model):
    songid = db.Column(db.String(64), primary_key=True)
    popularity = db.Column(db.Integer())
    track_number = db.Column(db.Integer())
    key = db.Column(db.Integer())
    mode = db.Column(db.Integer())
    acousticness = db.Column(db.Integer())
    danceability = db.Column(db.Integer())
    energy = db.Column(db.Integer())
    instrumentalness = db.Column(db.Integer())
    liveness = db.Column(db.Integer())
    loudness = db.Column(db.Integer())
    speechiness = db.Column(db.Integer())
    valence = db.Column(db.Integer())
    tempo = db.Column(db.Integer())

    def __repr__(self):
        return '<SpotifySongData {}>'.format(self.songid)

    def data(self):
        return {
                'songid': self.songid,
                'popularity': self.popularity,
                'track_number': self.track_number,
                'key': self.key,
                'mode': self.mode,
                'acousticness': self.acousticness,
                'danceability': self.danceability,
                'energy': self.energy,
                'instrumentalness': self.instrumentalness,
                'liveness': self.liveness,
                'loudness': self.loudness,
                'speechiness': self.speechiness,
                'valence': self.valence,
                'tempo': self.tempo
    }
