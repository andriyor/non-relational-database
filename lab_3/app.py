from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'app-transportation',
}
app.config['SECRET_KEY'] = 'hard to guess string'
Bootstrap(app)


app.debug = True

db = MongoEngine(app)

