from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_security import SQLAlchemyUserDatastore, Security, utils

from app import app, db, admin, bcrypt, mail
from app.forms import LoginForm,MedicionForm,RequestResetForm, ResetPasswordForm
from app.admin import UserAdmin
from app.models import Usuario, Rol, Medicion, Recomendacion
from flask_mail import Message

import keras
from tensorflow.keras import backend as K
from keras.models import Sequential
from keras.models import load_model

#main = Blueprint('main', __name__)
def get_model():
    global model
    model = load_model('recomendador.h5')
    print('*Modelo cargado!')

#get_model()

def guardar_medicion(ph,densidad,cond_elec,fecha):
    medicion = Medicion(ph=ph, densidad=densidad, cond_elec=cond_elec,
                        fecha=fecha)
    db.session.add(medicion)
    db.session.commit()
    return True

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/home')
@login_required
def home():
 return render_template('home.html')

@app.route("/predict", methods=['GET', 'POST'])
@login_required
def predict():
    form = MedicionForm()
    if form.validate_on_submit():
        ph = form.ph.data
        densidad = form.densidad.data
        cond_elec = form.cond_elect.data
        fecha = form.fecha.data
        guardar_medicion(ph,densidad,cond_elec,fecha)
        return redirect(url_for('recomendacion'))

    return render_template('ingreso_datos.html',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and utils.verify_password(form.password.data,user.password):
            login_user(user, remember=form.remember.data)
            #next_page = request.args.get('next')
            if user.has_role('admin'):
                return redirect(url_for('admin.home_admin'))
            elif user.has_role('tecnico'):
                return redirect(url_for('home'))
                #return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Error al acceder. Por favor verifique su email y/o contraseña', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

admin.add_view(UserAdmin(Usuario, db.session))
@app.route("/recomendacion")
def recomendacion():
    return render_template('recomendacion.html')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Solicitud para reestablecer contraseña',
                  sender='oso95d@gmail.com',
                  recipients=[user.email])
    msg.body = f'''Para reestablecer tu contraseña, visita el siguiente link:
{url_for('reset_token', token=token, _external=True)}
Si no hiciste esta solicitud simplemente ignora este correo y no se hará ningún cambio.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Se ha enviado un email con instrucciones para reestablecer su contraseña.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Usuario.verify_reset_token(token)
    if user is None:
        flash('El token es inválido o ha expirado', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Su contraseña ha sido cambiada! Ahora puede iniciar sesión', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Usuario, Rol)
security = Security(app, user_datastore)
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        get_url=url_for
    )

@app.before_first_request
def before_first_request():

    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', descripcion='Administrador')
    user_datastore.find_or_create_role(name='tecnico', descripcion='Tecnico Agricola')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password_admin = utils.hash_password('admin')
    encrypted_password_tecnico = utils.hash_password('tecnico')
    if not user_datastore.get_user('tecnico@example.com'):
        user_datastore.create_user(email='tecnico@example.com', password=encrypted_password_tecnico)
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(email='admin@example.com', password=encrypted_password_admin)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('tecnico@example.com', 'tecnico')
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    db.session.commit()

@app.route('/historial', methods=['GET', 'POST'])
@login_required
def buscar_recomendaciones():
    recs=[]
    fecha_inicio = request.args.get('desde')
    fecha_fin = request.args.get('hasta')
    print('fecha inicio',fecha_inicio)
    if fecha_inicio and fecha_fin:
        if fecha_inicio>fecha_fin:
            flash('La fecha de inicio no puede ser mayor a la fecha fin', 'warning')
        else:
            recs = db.session.query(Recomendacion).join(Medicion).filter(Medicion.fecha <= fecha_fin,Medicion.fecha>=fecha_inicio).all()
        print(recs)
        #recs = Recomendacion.query.filter(Recomendacion.medicion.fecha <= fecha_fin, Recomendacion.medicion_id.fecha >= fecha_inicio).all()
    return render_template('historial.html',recs=recs)