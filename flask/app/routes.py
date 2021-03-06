from app import app
from flask import render_template, url_for, request, redirect
from app import db
from app.models import Song, Play, Album, Artist, SpotifySongData

# clumsy import
from datetime import datetime

# more clumsiness with global variables ahead
idblacklist=[None, 'spotify:music:content', 'Brak danych', u'']

# even clumsier function to pass to jinja template
def getnormaltime(t):
    return datetime.fromtimestamp(int(float(t)))

def getranks(data):
    result = []
    for item in data:
        songdata = Song.query.get(item.songid)
        albumdata = Album.query.get(songdata.albumid)
        artistdata = Artist.query.get(songdata.artistid)
        result.append({'songdata': songdata, 'artistdata': artistdata, 'albumdata': albumdata, 'data': item})
    return result

@app.route('/')
def main():
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    debug = request.args.get('debug', 0, type=int)
    idcount = {}
    lastplay = {}

    p = Play.query.order_by(Play.timefrom.desc()).paginate(page, app.config['PLAYS_ON_INDEX_PER_PAGE'], False)

    for item in p.items:
        count = Play.query.filter_by(songid=item.songid).order_by(Play.timefrom.desc()).all()
        idcount.update({item.songid: len(count)})
        lastplay.update({item.songid: count[0].data()})

    next_url = url_for('index', page=p.next_num, debug=debug) if p.has_next else None
    prev_url = url_for('index', page=p.prev_num, debug=debug) if p.has_prev else None

    return render_template('index.html',
                           plays=p.items,
                           counts=idcount,
                           lastplay=lastplay,
                           playsobj=p,
                           bl=idblacklist,
                           tf=getnormaltime,
                           debug=debug,
                           next_url=next_url,
                           prev_url=prev_url)

@app.route('/song/<songid>')
def song(songid):
    songdata = Song.query.get(songid)
    spotifysongdata = SpotifySongData.query.get(songid)
    albumdata = Album.query.get(songdata.albumid)
    artistdata = Artist.query.get(songdata.artistid)
    songplays = Play.query.filter_by(songid=songid).all()
    return render_template('song.html', tf=getnormaltime, songdata=songdata, spotifysongdata=spotifysongdata, albumdata=albumdata, artistdata=artistdata, songplays=songplays)

@app.route('/album/<albumid>')
def album(albumid):
    albumdata = Album.query.get(albumid)
    artistdata = Artist.query.get(albumdata.artistid)
    songsofalbum = Song.query.filter_by(albumid=albumid).all()

    lastplay = {}
    for item in songsofalbum:
            count = Play.query.filter_by(songid=item.songid).order_by(Play.timefrom.desc()).all()
            lastplay.update({item.songid: count[0].data()})

    return render_template('album.html', tf=getnormaltime, albumdata=albumdata, artistdata=artistdata, songsofalbum=songsofalbum, lastplay=lastplay)

@app.route('/artist/<artistid>')
def artist(artistid):
    artistdata = Artist.query.get(artistid)
    albumsofartist = Album.query.filter_by(artistid=artistid).all()
    songsofartist = Song.query.filter_by(artistid=artistid).all()

    lastplay = {}
    for item in songsofartist:
            count = Play.query.filter_by(songid=item.songid).order_by(Play.timefrom.desc()).all()
            lastplay.update({item.songid: count[0].data()})

    return render_template('artist.html', artistdata=artistdata, albumsofartist=albumsofartist, songsofartist=songsofartist, tf=getnormaltime, lastplay=lastplay)

@app.route('/nope/<songid>')
def nope(songid):
    songdata = Song.query.get(songid)
    spotifysongdata = SpotifySongData.query.get(songid)
    albumdata = Album.query.get(songdata.albumid)
    artistdata = Artist.query.get(songdata.artistid)
    songplays = Play.query.filter_by(songid=songid).all()
    return render_template('nope.html', tf=getnormaltime, songdata=songdata, spotifysongdata=spotifysongdata, albumdata=albumdata, artistdata=artistdata, songplays=songplays)

@app.route('/ranking/')
def ranking():
    popularity = SpotifySongData.query.order_by(SpotifySongData.popularity.desc()).limit(5).all()
    populardata = getranks(popularity)

    hipsterity = SpotifySongData.query.order_by(SpotifySongData.popularity.asc()).limit(5).all()
    hipsterdata = getranks(hipsterity)

    speed = SpotifySongData.query.order_by(SpotifySongData.tempo.desc()).limit(5).all()
    speeddata = getranks(speed)

    slow = SpotifySongData.query.order_by(SpotifySongData.tempo.asc()).limit(5).all()
    slowdata = getranks(slow)

    return render_template('ranking.html', popular=populardata, hipster=hipsterdata, speedy=speeddata, slowy=slowdata)
