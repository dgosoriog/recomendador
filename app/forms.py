from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, SelectField, \
    RadioField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from datetime import date
from app.models import Usuario
from app.models import MyEnum


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

class RecomendacionForm(FlaskForm):
    descrip = TextAreaField('',validators=[DataRequired()], render_kw={'readonly': True})
    otra_sugerencia = SelectField('Escoja una recomendación más adecuada',choices = [("", "Seleccione una opción"),
                                                                (0,'No hacer nada'),
                                                                (1,'Incorporar Composto o Cambio de lugar'),
                                                                (2,'Drenchado,Trinchar camas o Levantar camas'),
                                                                (3,'Aplicar sulfato de calcio o Aplicar nitrato de calcio'),
                                                                (4,'Aplicar sulfato de amonio o Aplicar nitrato de amonio'),
                                                                 ],validators=[Optional()],default="")
    de_acuerdo = RadioField('¿Está de acuerdo con esta recomendación?', choices=[(1,'Si'),(0,'No')], validators=[DataRequired()])
    guardar = SubmitField('Guardar')

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