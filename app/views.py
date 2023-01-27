import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


def user_write_db(user):
    db.session.add(user)
    db.session.commit()

def user_del_db(user):
    db.session.delete(user)
    db.session.commit()

def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return user

@app.route('/test')
@app.route('/test/<data>')
def test(data=None):
    server_gmt_time  = datetime.datetime.now()
    result = server_gmt_time.strftime("%d-%m-%Y %H:%M")
    
    if data is not None:
        result = data
    
    return result

@app.route('/')
@app.route('/index/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Towareesh'}
    posts = [{'author': {'username': 'Vlad'},
              'body': 'Beautiful day in Portland!'},

             {'author': {'username': 'Tony'},
              'body': 'Nice mother'},

             {'author': {'username': 'Mark'},
              'body': 'Bullshit!'}]

    return render_template('index.html', title='INDEX', user=user, posts=posts)

@app.route('/home')
@login_required
def home():
    """ 
    Представление главной страницы.
    Returns:
        str: object render_template
    """

    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Представление страницы с моделью регистации.
    Returns:
        str: object render_template
    """

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    now_time = datetime.datetime.now()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        print(f'user: {form.username.data} - - {now_time.strftime("%d-%m-%Y %H:%M")}')
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        user_write_db(user)

        flash('You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = get_user(username)
    posts = [
            {'author': user, 'body': 'Test post_1'},
            {'author': user, 'body': 'Test post_2'}
            ]
    return render_template('user.html', user=user, posts=posts)