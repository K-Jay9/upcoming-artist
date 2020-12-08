'''
The required docstring
'''

from flask import Flask, render_template


app = Flask(__name__)

# The home route of the project


@app.route('/')
def index():
    return render_template('base.html', title='Romoz')
