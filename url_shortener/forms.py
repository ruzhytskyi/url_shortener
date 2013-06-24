from wtforms import Form, TextField, PasswordField, validators
from wtforms.validators import ValidationError
from urllib2 import urlopen, URLError, HTTPError
from models import User
from tools import get_service_url

class ShortenerForm(Form):
    no_input_message = 'Paste url and try again'
    full_url = TextField('Full url',
                         [validators.InputRequired(message=no_input_message)])

    def validate_full_url(form, field):
        url = field.data
        try:
            if not url.strip() == get_service_url() + '/shortener':
                urlopen(url)
        except HTTPError:
            raise ValidationError('Provided url results in http error, paste another one') 
        except URLError:
            raise ValidationError('Not a valid url, paste another one')
        except ValueError:
            raise ValidationError('Not a valid url, paste another one')
            
class SignUpForm(Form):
    no_login = 'Please, provide your login'
    no_pass = 'Please, provide your password'
    no_conf = 'Please, repeat your password'
    login = TextField('Login',
                      [validators.InputRequired(message=no_login)])
    password = PasswordField('Password',
                             [validators.InputRequired(message=no_pass)])
    confirmation = PasswordField('Confirmation',
                                 [validators.InputRequired(message=no_conf)])

    def validate_login(form, field):
        if User.query.filter_by(login=field.data).first():
            raise ValidationError("User with login '%s' already exists"
                                  % field.data)

    def validate_confirmation(form, field):
        if field.data != form.password.data:
            raise ValidationError("Confirmation doesn't match password")
        
class SignInForm(Form):
    no_login = 'Please, provide your login'
    no_pass = 'Please, provide your password'
    login = TextField('Login',
                      [validators.InputRequired(message=no_login)])
    password = PasswordField('Password',
                             [validators.InputRequired(message=no_pass)])

    def validate_login(form, field):
        if User.query.filter_by(login=field.data).first() == None:
            raise ValidationError("User with login '%s' doesn't exist"
                                 % field.data)

    def validate_password(form, field):
        if form.login.errors == []:
            password = User.query.filter_by(login=form.login.data).first().password
            if password != field.data:
                raise ValidationError("Wrong password")
