from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask_mail import Message

from app import app, db, mail
from app.forms import (LoginForm,
                       RegistrationForm,
                       EditProfileForm,
                       EmptyForm,
                       PostForm,
                       ResetPasswordRequestForm,
                       ResetPasswordForm)
from app.models import User, Post
from app.email import send_password_reset_email


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

<<<<<<< HEAD
=======
@app.route('/test_mail')
def test_mail():
    msg = Message('hello world',
                  sender='towareesh41@gmail.com',
                  recipients=['anitaulitka@gmail.com'])
    
    msg.body = "hello everybody my name is TALIBAN"
    mail.send(msg)
    return 'MAIL SEND'

>>>>>>> 7c91e0cc3f2f7fa64497c4d9c0897f00556dbb15

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    
    page  = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page=page,
                                                   per_page=app.config['POSTS_PER_PAGE'],
                                                   error_out=False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None

    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/explore')
@login_required
def explore():
    page  = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page,
                                                                per_page=app.config['POSTS_PER_PAGE'],
                                                                error_out=False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)
    

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
    form = EmptyForm()
    user  = User.query.filter_by(username=username).first_or_404()
    page  = request.args.get('page', 1, type=int)
    
    #### later add: per_page=app.config['POSTS_PER_PAGE']
    posts = user.posts.paginate(page=page,
                                error_out=False)
    return render_template('user.html', user=user,
                           form=form, posts=posts.items)


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


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
    