from url_shortener import db

class Hash(db.Model):
    url_hash = db.Column(db.String(8), primary_key=True)
    full_url = db.Column(db.String(1000), unique = True)

    def __init__(self, url_hash, full_url):
        self.url_hash = url_hash
        self.full_url = full_url 