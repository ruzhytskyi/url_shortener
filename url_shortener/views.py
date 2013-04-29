from flask import request, render_template, redirect, url_for, session, g
from url_shortener import app, db
from forms import ShortenerForm, SignUpForm, SignInForm
from tools import make_hash, make_short_url
from models import Hash, User

@app.before_request
def before_request():
    g.si_form = SignInForm()

@app.route('/shortener', methods=['GET', 'POST'])
def shortener():
    shortener_form = ShortenerForm(request.form)
    short_url = ''
    if request.method == 'POST' and shortener_form.validate():
        full_url = shortener_form.full_url.data
        url_hash = make_hash(full_url) 
        short_url = make_short_url(app.config['HOST'],
                                   app.config['PORT'],
                                   url_hash)
        entry = Hash(url_hash, full_url)
        db.session.add(entry)
        try:
            db.session.commit()
        except:
            pass
    return render_template('shortener.html', short_url=short_url, form=shortener_form)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    sign_up_form = SignUpForm(request.form)
    if request.method == 'POST':
        if sign_up_form.validate():
            login = sign_up_form.login.data
            password = sign_up_form.password.data
            session['login'] = login
            entry = User(login, password)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('shortener')) 
        else:
            return render_template('sign_up.html', form=sign_up_form)
    elif request.method == 'GET':
        return render_template('sign_up.html', form=sign_up_form)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    sign_in_form = SignInForm(request.form)
    if sign_in_form.validate():
        session['login'] = sign_in_form.login.data
        return redirect(url_for('shortener'))
    else:
        return render_template('sign_in_errors.html', form=sign_in_form)

@app.route('/sign_out', methods=['GET'])
def sign_out():
    session['login'] = None
    return redirect(url_for('shortener'))

@app.route('/<url_hash>', methods=['GET'])
def redirection(url_hash):
    full_url = Hash.query.filter_by(url_hash=url_hash).first().full_url
    return redirect(full_url) 

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return url_for('static', filename='favicon.ico')
