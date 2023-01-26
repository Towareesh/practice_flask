from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User



class LoginForm(FlaskForm):
    username    = StringField('Имя', validators=[DataRequired()])
    password    = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit      = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    # username   = LoginForm.username
    # password   = LoginForm.password
    username   = StringField('Имя', validators=[DataRequired()])
    password   = PasswordField('Пароль', validators=[DataRequired()])
    password2  = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    email      = StringField('Почта', validators=[DataRequired(), Email()])
    submit     = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другую почту.')