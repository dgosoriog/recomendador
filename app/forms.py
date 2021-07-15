from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import date
from app.models import Usuario


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordar')
    submit = SubmitField('Entrar')

class MedicionForm(FlaskForm):
    ph = FloatField('Ph',validators=[DataRequired()])
    densidad = FloatField('Densidad', validators=[DataRequired()])
    cond_elect = FloatField('Conductividad Eléctrica',validators=[DataRequired()])
    fecha = DateField('Fecha', default=date.today(), validators=[DataRequired()])
    cargar = SubmitField('Cargar')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Solicitar cambio de contraseña')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No existe una cuenta con ese email. Solicite su registro al administrador.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cambiar Contraseña')