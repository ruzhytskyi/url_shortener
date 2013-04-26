from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('url_shortener.config')
db = SQLAlchemy(app)

import url_shortener.views
