from app import app
from flask import render_template
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
@app.route('/index')
def index():
    p = Play.query.order_by(Play.timefrom.desc()).all()

    return render_template('index.html', plays=p, bl=idblacklist, tf=getnormaltime)
