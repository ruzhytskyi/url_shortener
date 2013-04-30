from url_shortener import db
from datetime import datetime

class Hash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    url_hash = db.Column(db.String(8), unique=True)
    full_url = db.Column(db.String(1000))
    redirects = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                           backref=db.backref('hashes', lazy='dynamic'))

    def __init__(self, url_hash, full_url, redirects=0, creation_date=None):
        if creation_date == None:
            self.creation_date = datetime.utcnow()
        self.url_hash = url_hash
        self.full_url = full_url 
        self.redirects = redirects

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, login, password):
        self.login = login
        self.password = password
