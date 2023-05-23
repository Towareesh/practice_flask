from flask import (current_app, flash, redirect, render_template, request,
                   url_for)
from flask_babel import _
from flask_login import current_user, login_required

from app import db
from app.handler import UserHandler
from app.models import Post, User
from app.user import user_bp
from app.user.forms import EditProfileForm, EmptyForm


handler = UserHandler(current_app, current_user, db)

@user_bp.route('/user/<username>')
@login_required
def user(username):
    form  = EmptyForm()
    user  = User.query.filter_by(username=username).first_or_404()
    query = user.posts.order_by(Post.timestamp.desc())
    posts, prev_url, next_url = handler.pagination_user_posts(query, user, 'user.user')

    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        handler.user_edit_profile(form)
        flash(_('Your changes have been saved.'))
        return redirect(url_for('user.edit_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.gender.data   = current_user.gender
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@user_bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_(f'User {username} not found'))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot follow yourself!'))
            return redirect(url_for('user.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user.user', username=username))
    else:
        return redirect(url_for('main.index'))


@user_bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_(f'User {username} not found'))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot unfollow yourself!'))
            return redirect(url_for('user.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user.user', username=username))
    else:
        return redirect(url_for('main.index'))