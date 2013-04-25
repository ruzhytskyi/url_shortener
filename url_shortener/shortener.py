from flask import Flask, render_template, request, url_for, redirect
from wtforms import Form, TextField, validators
from wtforms.validators import ValidationError
from urllib2 import urlopen, URLError
from hashlib import md5 
from flask.ext.sqlalchemy import SQLAlchemy

# configuration
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return url_for('static', filename='favicon.ico')
@app.route('/<hash_str>', methods=['GET'])
def redirection(hash_str):
    if hash_str != 'favicon.ico':
        url = "http://localhost:5000/%s" % hash_str
        full_url = ShortUrl.query.filter_by(short_url=url).first().full_url
        return redirect(full_url) 

@app.route('/shortener', methods=['GET', 'POST'])
def shortener():
    shortener_form = ShortenerForm(request.form)
    short_url = ''
    if request.method == 'POST' and shortener_form.validate():
        short_url = convert_url(shortener_form.full_url.data) 
        entry = ShortUrl(shortener_form.full_url.data, short_url)
        db.session.add(entry)
        db.session.commit()
    return render_template('shortener.html', short_url=short_url, form=shortener_form)

def is_valid_url(form, field):
    url = field.data
    try:
        urlopen(url)
    except ValueError, URLError:
        raise ValidationError('Not a valid url, paste another one')

class ShortUrl(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    full_url = db.Column(db.String(1000), unique = True)
    short_url = db.Column(db.String(8), unique = True)
    
    def __init__(self, full_url, short_url):
        self.full_url = full_url
        self.short_url = short_url

class ShortenerForm(Form):
    full_url = TextField('Full url', [is_valid_url, validators.InputRequired(message='Paste an url and try again')]) 

def convert_url(full_url):
    """
    Returns shortened url
    """
    path = md5(full_url).hexdigest()[:8]
    short_url = "http://localhost:5000/%s" % path
    return short_url 

if __name__ == '__main__':
    app.run()
