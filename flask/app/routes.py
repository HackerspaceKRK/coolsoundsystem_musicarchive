from app import app
from flask import render_template, url_for, request
from app import db
from app.models import Song, Play

# clumsy import
from datetime import datetime

# more clumsiness with global variables ahead
idblacklist=[None, 'spotify:music:content', 'Brak danych']

# even clumsier function to pass to jinja template
def getnormaltime(t):
    return datetime.fromtimestamp(int(float(t)))

@app.route('/')
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
    return render_template('song.html', songdata=songdata)

@app.route('/artist/<artistid>')
def artist(artistid):
    return render_template('artist.html')

@app.route('/album/<albumid>')
def album(albumid):
    return render_template('album.html')
