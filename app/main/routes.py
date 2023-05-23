from flask import current_app, flash, g, redirect, render_template, url_for, request
from flask_babel import _, get_locale
from flask_login import current_user, login_required

from app import db
from app.handler import MainHandler
from app.main import main_bp
from app.main.forms import PostForm, SearchForm
from app.models import Post


handler = MainHandler(current_app, current_user, db)

@main_bp.before_request
def before_request():
    handler.last_seen()
    g.search_form = SearchForm()
    g.locale = str(get_locale())


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        handler.create_post(form, Post)
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))

    query = current_user.followed_posts()
    posts, prev_url, next_url = handler.pagination_posts(query, 'main.index')

    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@main_bp.route('/explore')
@login_required
def explore():
    query = Post.query.order_by(Post.timestamp.desc())
    posts, prev_url, next_url = handler.pagination_posts(query, 'main.explore')

    return render_template('index.html', title=_('Explore'), posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


# @main_bp.route('/translate', methods=['POST'])
# @login_required
# def translate_():
#     return jsonify({'text': translate_text(request.form['text'],
#                                            request.form['source_language'],
#                                            request.form['dest_language'])})


@main_bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])

    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) if page > 1 else None

    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)