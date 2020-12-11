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


audios = []
videos = []
result = []
minor = []


#  The function that decides whether the link is a video or an audio

def video_or_audio(d):
    if d[:len(YOUTUBE)] == YOUTUBE:
        return 'video'
    elif d[:len(MIXCLOUD)] == MIXCLOUD:
        return 'audio'
    return None


def decide():
    res = get_data()
    for i in res:
        out = video_or_audio(i[1])
        if out == 'audio' and out != None:
            result.append(i[1])
        elif out == 'video' and out != None:
            minor.append(i[1])
    return

decide()
def trim():
    for i in result:
        users = {}
        x = i.split('/')
        users[x[-3]] = x[-2]
        audios.append(users)
    for i in minor:
        z = i.split('/')
        y = z[-1].split('=')
        videos.append(y[-1])
    return
trim()

'''
The actual app
'''

# The home route of the project
@app.route('/')
def index():
    return render_template('index.html', title='Romoz', videos=videos[:4], audios=audios[:4])


# the only function that doesn't work
@app.route('/admin/add', methods=['POST', 'GET'])
def add():
    msg= 'nthing'
    if request.method == 'POST':
        try:
            link = request.form['link']
            query = ''';
            '''
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                print(query)
                cur.execute("INSERT INTO links(link, artist) VALUES(?, ?)", (link, 'djromoz'))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        
        finally:
            return render_template("add.html",msg = msg, title='Add')
            close_connection()
    else:
        return render_template('add.html', msg=msg, title='Add')

@app.route('/admin')
def admin():
    rows = get_data()
    return render_template("admin.html",rows=rows,title='Admin')


@app.route('/videos')
def video():
    return render_template('videos.html', title='Videos', videos=videos)

@app.route('/audios')
def audio():
    return render_template('audios.html', title='Audios', audios=audios)



