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

def get_data():
    con = sqlite3.connect(DATABASE)
    db = con.cursor()
    res = db.execute('select * from links')
    return res

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
    res = get_data()
    aud = []
    vid = []
    for i in res:
        out = video_or_audio(i[1])
        if out == 'video' and out != None:
            vid.append(i[1])
        elif out == 'audio' and out != None:
            aud.append(i[1])
    return render_template('index.html', title='Romoz', aud=aud, vid=vid)

@app.route('/admin/add', methods=['POST', 'GET'])
def add():
    msg= 'nthing'
    if request.method == 'POST':
        try:
            link = request.form['link']
            with sql.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO links link VALUES ? ",link )
                
                con.commit()
                msg = "Record successfully added"
                print(msg)
        except:
            con.rollback()
            msg = "error in insert operation"
        
        finally:
            return render_template("add.html",msg = msg, title='Add')
            close_connection()
    else:
        print(msg)
        return render_template('add.html', msg=msg, title='Add')

@app.route('/admin')
def admin():
    rows = get_data()
    return render_template("admin.html",rows=rows,title='Admin')


@app.route('/videos')
def video():
    res = get_data()
    videos = []
    for i in res:
        out = video_or_audio(i[1])
        if out == 'video':
            videos.append(i[1])
    return render_template('videos.html', title='Videos', videos=videos)

@app.route('/audios')
def audio():
    res = get_data()
    audios = []
    for i in res:
        out = video_or_audio(i[1])
        if out == 'audio' and out != None:
            audios.append(i[1])
    return render_template('audios.html', title='Audios', audios=audios)


#  The function that decides whether the link is a video or an audio

def video_or_audio(d):
    if d[:len(YOUTUBE)] == YOUTUBE:
        return 'video'
    elif d[:len(MIXCLOUD)] == MIXCLOUD:
        return 'audio'
    return None