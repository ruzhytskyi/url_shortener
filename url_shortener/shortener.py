from flask import Flask, render_template, request, url_for
from wtforms import Form, TextField, validators
from wtforms.validators import ValidationError
from urllib2 import urlopen, URLError
from hashlib import md5 

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/shortener', methods=['GET', 'POST'])
def shortener():
    shortener_form = ShortenerForm(request.form)
    short_url = ''
    if request.method == 'POST' and shortener_form.validate():
        short_url = convert_url(shortener_form.full_url.data) 
    return render_template('shortener.html', short_url=short_url, form=shortener_form)

def is_valid_url(form, field):
    url = field.data
    try:
        urlopen(url)
    except ValueError, URLError:
        raise ValidationError('Not a valid url, paste another one')

class ShortenerForm(Form):
    full_url = TextField('Full url', [is_valid_url, validators.InputRequired(message='Paste an url and try again')]) 

def convert_url(full_url):
    """
    Returns shortened url
    """
    path = md5(full_url).hexdigest()[:8]
    short_url = "http://localhost/%s" % path
    return short_url 

            
        
    

if __name__ == '__main__':
    app.run()
