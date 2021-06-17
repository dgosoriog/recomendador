from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import date

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
