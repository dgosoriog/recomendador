from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    usuario = StringField('Usuario',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordar')
    submit = SubmitField('Entrar')