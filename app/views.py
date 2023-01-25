import datetime

from flask import render_template, flash, redirect, url_for

from app import app
from app.forms import LoginForm


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
def index():
    user = {'username': 'Towareesh'}
    posts = [{'author': {'username': 'Vlad'},
              'body': 'Beautiful day in Portland!'},

             {'author': {'username': 'Tony'},
              'body': 'Nice mother'},

             {'author': {'username': 'Mark'},
              'body': 'Bullshit!'}]

    return render_template('index.html', title='INDEX', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Войти', form=form)