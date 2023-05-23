import detectlanguage
from flask import request, url_for
from datetime import datetime


class BaseHandler:
    """The class allows you to hide piles of business logic in presentation functions.

    In order to avoid duplication code, it implements commonly used methods.
    """

    def __init__(self, current_app, current_user, db) -> None:
        self.current_user = current_user
        self.current_app  = current_app
        self.db = db


    def update_db(self, data=None) -> None:
        """Writes and commits to the database.
        
        If not given data, then nothing will be written
        to the database, it is simply updated.

        Args:
            data (app.models): Instance class of models.
        """
        if data:
            self.db.session.add(data)
        self.db.session.commit()


class MainHandler(BaseHandler):
    
    def last_seen(self) -> None:
        """Updating last seen time user
        """

        if self.current_user.is_authenticated:
            self.current_user.last_seen = datetime.utcnow()
            self.update_db()

    def get_lang(self, text: str) -> str:
        """Func get language a text.

        If connecting to detectlanguageAPI is fall,
        then language is not detect, otherwise an empty string.

        Args:
            text (str): Any string data.

        Returns:
            language (str): Detected language, else an empty string.
        """

        try:
            detectlanguage.configuration.api_key = self.current_app.config['DETECT_LANG_API_KEY']
            language = detectlanguage.simple_detect(text)
        except:
            # issue catch the error then fall detect - 001
            language = ''    
        return language

    def create_post(self, form, Model) -> None:
        """Create user post in data base.

        Args:
            form (PostForm): Instance class PostForm(FlaskForm)
            Model (app.models.Post): Instance Post(UserMixin) class of models.
        """

        lang = self.get_lang(form.post.data)
        post = Model(body=form.post.data, author=self.current_user, language=lang)
        self.update_db(post)

    def pagination_posts(self, query, route_adress: str) -> tuple:
        """Does pagination of the request.

        Args:
            query (query.Query): Generated posts request to the database.
            route_adress (str): Route func name.

        Returns:
            tuple: Contains prev_url and next_url, paginated posts.
        """

        page  = request.args.get('page', 1, type=int)
        posts = query.paginate(page=page, per_page=self.current_app.config['POSTS_PER_PAGE'], error_out=False)

        prev_url = url_for(route_adress, page=posts.prev_num) if posts.has_prev else None
        next_url = url_for(route_adress, page=posts.next_num) if posts.has_next else None

        return posts, prev_url, next_url


class UserHandler(BaseHandler):

    def pagination_user_posts(self, query, user, route_adress: str) -> tuple:
        """Does pagination of the request.

        Args:
            query (query.Query): Generated posts request to the database.
            user (User.user): Generated user  request to the database.
            route_adress (str): Route func name.

        Returns:
            tuple: Contains prev_url and next_url, paginated posts.
        """

        page  = request.args.get('page', 1, type=int)
        posts = query.paginate(page=page, per_page=self.current_app.config['POSTS_PER_PAGE'], error_out=False)

        next_url = url_for(route_adress, username=user.username, page=posts.next_num) if posts.has_next else None
        prev_url = url_for(route_adress, username=user.username, page=posts.prev_num) if posts.has_prev else None

        return posts, prev_url, next_url

    def user_edit_profile(self, form) -> None:
        self.current_user.username = form.username.data
        self.current_user.about_me = form.about_me.data
        self.current_user.gender   = form.gender.data
        self.update_db()
