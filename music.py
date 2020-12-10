'''
The required docstring
'''
import sqlite3
from flask import Flask, render_template, g, request

app = Flask(__name__)



'''
The database section of the site
'''


DATABASE = 'music.db'
MIXCLOUD = 'https://www.mixcloud.com/'
YOUTUBE = 'https://www.youtube.com/'

# The database get request
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# closing the db connection after use
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
#  Initialising the db schema
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#  initialising the db on the cli
@app.cli.command('init-db')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialised the database...')



'''
The actual app
'''

# The home route of the project
@app.route('/')
def index():
    res = get_db()
    aud = []
    vid = []
    # for i in res:
    #     out = video_or_audio(i)
    #     if out == YOUTUBE and out != None:
    #         vid.append(a)
    #     elif out == MIXCLOUD and out != None:
    #         aud.append(a)
    return render_template('index.html', title='Romoz', res=res)

@app.route('/admin/add')
def add():
    msg= 'nthing'
    try:
        link = request.form['link']
        with sql.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO links link VALUES ? ",link )
            
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
    
    finally:
        return render_template("admin.html",msg = msg, title='Admin')
        close_connection()
@app.route('/admin')
def admin():
    rows = get_db()
    return render_template("admin.html",rows=rows,title='Admin')


@app.route('/videos')
def video():
    res = get_db()
    videos = []
    # for i in res:
    #     out = video_or_audio(i)
    #     if out == YOUTUBE:
    #         videos.append(out)
    return render_template('videos.html', title='Videos', videos=videos)

@app.route('/audios')
def audio():
    res = get_db()
    audios = []
    # for i in res:
    #     out = video_or_audio(i)
    #     if out == MIXCLOUD and out != None:
    #         audios.append(out)
    return render_template('audios.html', title='Audios', audios=audios)


#  The function that decides whether the link is a video or an audio

def video_or_audio(d):
    if d[:len(YOUTUBE)] == YOUTUBE:
        return d[len(YOUTUBE):]
    elif d[:len(MIXCLOUD)] == MIXCLOUD:
        return d[len(MIXCLOUD):]
    return None