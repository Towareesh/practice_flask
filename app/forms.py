from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     BooleanField,
                     SubmitField,
                     TextAreaField)
from wtforms.validators import (DataRequired,
                                ValidationError,
                                Email,
                                EqualTo,
                                Length)
from app.models import User


class LoginForm(FlaskForm):
    username    = StringField('Имя', validators=[DataRequired()])
    password    = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit      = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username   = StringField('Имя', validators=[DataRequired()])
    password   = PasswordField('Пароль', validators=[DataRequired()])
    password2  = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    email      = StringField('Email', validators=[DataRequired(), Email()])
    submit     = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другую почту.')


class EditProfileForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=140)])
    submit   = SubmitField('Применить')

    def __init__(self, original_name, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
    
    def validate_username(self, username):
        if username.data != self.original_name:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Пожалуйста, используйте другое имя.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post   = TextAreaField('Скажите что-то', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    email  = StringField('Email', validators=[DataRequired(), Email()] )
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password  = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Requset Password Reset')