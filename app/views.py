from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.forms import EditProfileForm, EmptyForm
from app.models import User


def user_write_db(user):
    db.session.add(user)
    db.session.commit()

def user_del_db(user):
    db.session.delete(user)
    db.session.commit()

def not_current_user(user):
    if user != current_user:
        return user

def get_first_post(user):
    try:
        get_first_post = user.posts.first().body
        post = get_first_post
    except:
        post = None
    return post

def view_user_posts(users):
    user_posts = [{'author': {'username': user.username, 'avatar': user.avatar},
                   'body': get_first_post(user)} for user in users if get_first_post(user)]
    return user_posts

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index/')
@app.route('/index')
@login_required
def index():
    users = list(filter(not_current_user, User.query.all()))
    posts = view_user_posts(users)

    return render_template('index.html', title='INDEX', posts=posts)


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
    now_time = datetime.now()
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
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
            {'author': user, 'body': 'Test post_1'},
            {'author': user, 'body': 'Test post_2'}
            ]
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username} not found')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))