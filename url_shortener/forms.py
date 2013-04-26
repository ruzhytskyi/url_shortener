from wtforms import Form, TextField, validators
from wtforms.validators import ValidationError
from urllib2 import urlopen, URLError

class ShortenerForm(Form):
    no_input_message = 'Paste url and try again'
    full_url = TextField('Full url',
                         [validators.InputRequired(message=no_input_message)])

    def validate_url(form, field):
        url = field.data
        try:
            urlopen(url)
        except ValueError, URLError:
            raise ValidationError('Not a valid url, paste another one')
