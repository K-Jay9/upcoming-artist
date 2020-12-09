'''
The required docstring
'''

from flask import Flask, render_template


app = Flask(__name__)

# The home route of the project


@app.route('/')
def index():
    return render_template('base.html', title='Romoz')

@app.route('/admin')
def admin():
    return render_template('admin.html', title='Admin')

@app.route('/videos')
def video():
    return render_template('videos.html', title='Videos')

@app.route('/audios')
def audio():
    return render_template('audios.html', title='Audios')

