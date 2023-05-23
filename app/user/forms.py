from app.models import User
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    gender   = StringField('Gender', validators=[DataRequired()])
    submit   = SubmitField(_l('Submit'))

    def __init__(self, original_name, *args, **kwargs):
        # Username is saved as an instance variable,
        # and checked in validate_username() method.
        # If username entered in form is same as original username,
        # then there is no reason to check database for duplicates.
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
    
    def validate_username(self, username):
        if username.data != self.original_name:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
