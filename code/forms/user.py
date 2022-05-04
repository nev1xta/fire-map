from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    fio = StringField('Укажите ФИО', validators=[DataRequired()])
    login = StringField('Придумайте логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class PositionForm(FlaskForm):
    # position = SelectField('Укажите должность', choices=[('Сержант', 'Сержант'), ('Лейтинант', 'Лейтинант'),
    #                                                      ('Капитан', 'Капитан')])
    fio = StringField('Укажите ФИО', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить')

