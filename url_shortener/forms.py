from wtforms import Form, TextField, validators
from wtforms.validators import ValidationError
from urllib2 import urlopen, URLError, HTTPError

class ShortenerForm(Form):
    no_input_message = 'Paste url and try again'
    full_url = TextField('Full url',
                         [validators.InputRequired(message=no_input_message)])

    def validate_full_url(form, field):
        url = field.data
        try:
            urlopen(url)
        except HTTPError:
            raise ValidationError('Provided url results in http error, paste another one') 
        except URLError:
            raise ValidationError('Not a valid url, paste another one')
        except ValueError:
            raise ValidationError('Not a valid url, paste another one')
            
