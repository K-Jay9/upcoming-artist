from flask import Flask

app = Flask(__name__)

# The home route of the project


@app.route('/')
def hello():
    return 'Hello, World!'
