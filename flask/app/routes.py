from app import app
from flask import render_template, url_for, request
from app import db
from app.models import Song, Play

# clumsy import
from datetime import datetime

# more clumsiness with global variables ahead
idblacklist=[None, 'spotify:music:content']

# even clumsier function to pass to jinja template
def getnormaltime(t):
    return datetime.fromtimestamp(int(float(t)))

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    print(page)
    p = Play.query.order_by(Play.timefrom.desc()).paginate(page, app.config['PLAYS_ON_INDEX_PER_PAGE'], False)
    next_url = url_for('index', page=p.next_num) if p.has_next else None
    prev_url = url_for('index', page=p.prev_num) if p.has_prev else None

    return render_template('index.html', plays=p.items, playsobj=p, bl=idblacklist, tf=getnormaltime, next_url=next_url, prev_url=prev_url)
