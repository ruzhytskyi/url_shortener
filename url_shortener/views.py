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
        logged_in = session.has_key('login') and session['login']
        if logged_in:
            url_hash = make_hash(full_url+session['login']) 
        else:
            url_hash = make_hash(full_url)
        short_url = make_short_url(app.config['HOST'],
                                   app.config['PORT'],
                                   url_hash)
        if Hash.query.filter_by(url_hash=url_hash).first() == None:
            if logged_in:
                user = User.query.filter_by(login=session['login']).first()
                hash_obj = Hash(url_hash, full_url)
                user.hashes.append(hash_obj)
                db.session.commit()
            else:
                user = User.query.filter_by(login='not_registered').first()
                if not user:
                    user = User('not_registered', 'pass')
                    db.session.add(user)
                hash_obj = Hash(url_hash, full_url)
                user.hashes.append(hash_obj)
                db.session.commit()
               
    return render_template('shortener.html', short_url=short_url, form=shortener_form)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    sign_up_form = SignUpForm(request.form)
    if request.method == 'POST':
        if sign_up_form.validate():
            login = sign_up_form.login.data
            password = sign_up_form.password.data
            session['login'] = login
            user = User(login, password)
            db.session.add(user)
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
        login = sign_in_form.login.data
        password = sign_in_form.password.data
        session['login'] = login 
        return redirect(url_for('shortener'))
    else:
        errors = sign_in_form.login.errors +\
                 sign_in_form.password.errors 
        return render_template('errors.html', errors=errors)

@app.route('/sign_out', methods=['GET'])
def sign_out():
    session['login'] = None
    return redirect(url_for('shortener'))

@app.route('/<url_hash>', methods=['GET'])
def redirection(url_hash):
    hash_obj = Hash.query.filter_by(url_hash=url_hash).first()
    hash_obj.redirects += 1
    db.session.commit()
    full_url = hash_obj.full_url
    return redirect(full_url) 

@app.route('/statistics', methods=['GET'])
def statistics():
    logged_in = session.has_key('login') and session['login']
    if logged_in:
        user_id = User.query.filter_by(login=session['login']).first().id
        hashes = Hash.query.filter_by(user_id=user_id)
        for hash_obj in hashes:
            short_url = make_short_url(app.config['HOST'],
                                       app.config['PORT'],
                                       hash_obj.url_hash)
            hash_obj.url_hash = short_url 
        return render_template('statistics.html', hashes=enumerate(hashes))
    else:
        errors = ['You should log in first']
        return render_template('errors.html', errors=errors)

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return url_for('static', filename='favicon.ico')
