from flask import render_template, url_for, flash, redirect, request, Response, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from flask_security import SQLAlchemyUserDatastore, Security, utils

from app import app, db, admin, bcrypt, mail
from app.forms import LoginForm, MedicionForm, RequestResetForm, ResetPasswordForm, RecomendacionForm
from app.admin import UserAdmin
from app.models import Usuario, Rol, Medicion, Recomendacion
from flask_mail import Message

import keras
import numpy as np
import pandas as pd
from keras.models import model_from_json
import os
from tensorflow.keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from numpy import array


# main = Blueprint('main', __name__)
cont = 0


from fpdf import FPDF
from app.funciones_adicionales import serialize
from json import dumps
import ast

#main = Blueprint('main', __name__)
cont=0
def get_model():
    global model
    model = load_model('recomendador.h5')
    print('*Modelo cargado!')


# get_model()

def guardar_medicion(ph, densidad, cond_elec, fecha, Cant_arr, pro_arr, cant_arv, pro_arv, cant_gar, pro_gar, cant_len, cant_pintcolor, pro_pintcolor, cant_raycolor, pro_raycolor, cant_colordef, pro_colordef, pro_len):
    medicion = Medicion(ph=ph, densidad=densidad, cond_elec=cond_elec,
                        fecha=fecha, Cant_arro=Cant_arr, pro_arr=pro_arr, cant_arv=cant_arv,
                        pro_arv=pro_arv, cant_gar=cant_gar, pro_gar=pro_gar, cant_len=cant_len,
                        cant_pintcolor=cant_pintcolor, pro_pintcolor=pro_pintcolor,
                        cant_raycolor=cant_raycolor, pro_raycolor=pro_raycolor, cant_colordef=cant_colordef, pro_colordef=pro_colordef,prolent=pro_len)
    db.session.add(medicion)
    db.session.commit()
    return True

# @app.route('/')
# def index():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     return render_template('index.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/parcela')
@login_required
def inicio():
    return render_template("parcela.html")


@app.route('/procesar', methods=['POST'])
@login_required
def procesar():
    arroz = request.form.get("arroz")
    arveja = request.form.get("arveja")
    garbanzo = request.form.get("garbanzo")
    lenteja = request.form.get("lenteja")
    pcolor = request.form.get("pcolor")
    rcolor = request.form.get("rcolor")
    colord = request.form.get("colord")


    return redirect(url_for('predict', a=arroz,ar=arveja,g=garbanzo,l=lenteja,pc=pcolor,rc=rcolor,c=colord))


@app.route("/medicion", methods=['GET', 'POST'])
@login_required
def ingresar_datos():
    ar = (int)(request.args.get("a"))
    arv = (int)(request.args.get("ar"))
    ga = (int)(request.args.get("g"))
    len = (int)(request.args.get("l"))
    pco = (int)(request.args.get("pc"))
    rco = (int)(request.args.get("rc"))
    co = (int)(request.args.get("c"))
    form = MedicionForm()
    if form.validate_on_submit():
        p1 = request.form.get("pr1")
        p2 = request.form.get("pr2")
        p3 = request.form.get("pr3")
        p4 = request.form.get("pr4")
        p5 = request.form.get("pr5")
        p6 = request.form.get("pr6")
        p7 = request.form.get("pr7")


        ph = form.ph.data
        densidad = form.densidad.data
        cond_elec = form.cond_elect.data
        fecha = form.fecha.data
        medicion = Medicion(ph=ph, densidad=densidad, cond_elec=cond_elec,
                            fecha=fecha)
        db.session.add(medicion)
        db.session.commit()
        id = medicion.id
        session['id_med'] = id
        print('MEDICION',medicion.id)
        return redirect(url_for('get_recomendacion'))
    return render_template('ingreso_datos.html', form=form,es1=ar,es2=arv,es3=ga,es4=len,es5=pco,es6=rco,es7=co)


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and utils.verify_password(form.password.data, user.password):
            login_user(user, remember=form.remember.data)
            # next_page = request.args.get('next')
            if user.has_role('admin'):
                return redirect(url_for('admin.home_admin'))
            elif user.has_role('tecnico'):
                return redirect(url_for('home'))
                # return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Error al acceder. Por favor verifique su email y/o contraseña', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    session.pop('id_med', None)
    session.pop('busqueda_recomendaciones', None)
    session.pop('fecha_inicio', None)
    session.pop('fecha_fin', None)
    return redirect(url_for('login'))


admin.add_view(UserAdmin(Usuario, db.session))
@app.route("/recomendacion")
def get_recomendacion():
    form = RecomendacionForm()
    dgarbanzo = request.args.get("d")
    print("ddd", dgarbanzo)
    ph=db.session.query(Medicion.ph).all();
    ph= pd.DataFrame(ph, columns = ['Name'])
    datosph=ph.values.astype('float32')
    den=db.session.query(Medicion.densidad).all();
    den=pd.DataFrame(den, columns = ['Name'])
    datosden = den.values.astype('float32')
    CE = db.session.query(Medicion.cond_elec).all();
    CE = pd.DataFrame(CE, columns=['Name'])
    datosce = CE.values.astype('float32')

    # df = pd.read_csv("C:/Users/Amanda/Downloads/Tesis_Zambrano_Meza-main/conjunto_datos/datos_clasificados.csv",
    #                  names=["dia", "CE", "PH", "D", "C"])
    # df_nan = df[df.isna().any(axis=1)]
    # df['C'] = df['C'].replace(np.nan, 0)
    # df_nan = df[df.isna().any(axis=1)]
    # datos = df.values.astype('float32')
    # cargar json y crear el modelo
    json_file = open("app/static/modelo/model.json", 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # cargar pesos al nuevo modelo
    loaded_model.load_weights("app/static/modelo/recomendador.h5")
    print("Cargado modelo desde disco.")

    # Compilar modelo cargado y listo para usar.
    loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['binary_accuracy'])
    suma_CE = 0;
    suma_PH = 0;
    suma_D = 0;

    # training_data = np.empty(shape=[0, 3])
    # target_data = np.empty(shape=[0])
    # print("se7", sum(list(map(float,ph))));
    # print("xd",ph);

    if (len(ph) <= 10):
        a = 0
        b = 10
        # print("entro aqui")
        for j in range(a, b):
            suma_CE = suma_CE + datosce[j];
            suma_PH = suma_PH + datosph[j];
            suma_D = suma_D + datosden[j];

    a = 0
    b = 10

    if (len(ph) > 10):
        b = len(ph) - 1
        a = len(ph) - 10
        # print("entro aca")
        for j in range(a, b):
            suma_CE = suma_CE + datosce[j];
            suma_PH = suma_PH + datosph[j];
            suma_D = suma_D + datosden[j];
        print("Datos de ", a, " hasta ", b);

    # print("Datos de ", a, " hasta ", b);
    pro_CE = float(suma_CE / 10);

    pro_PH = float(suma_PH / 10);
    # print(pro_PH);
    pro_D = float(suma_D / 10);
    # print(pro_D);

    suma_CE = 0;
    suma_PH = 0;
    suma_D = 0;
    c = array([[pro_CE, pro_PH, pro_D]])
    print(c)
    pre = loaded_model.predict(c)
    result = pre[0]
    print(result)
    answer = np.argmax(result)
    print(answer)

    if answer == 1:
        print("Se Recomienda: Incorporar Composto o Cambio de lugar")
        recomen = "Incorporar Composto o Cambio de lugar"
    elif answer == 2:
        print("Se Recomienda: Drenchado,Trinchar camas o Levantar camas")
        recomen = "Drenchado,Trinchar camas o Levantar camas"
    elif answer == 3:
        print("Se Recomienda: Aplicar sulfato de calcio o Aplicar nitrato de calcio")
        recomen = "Aplicar sulfato de calcio o Aplicar nitrato de calcio"
    elif answer == 4:
        print("Se Recomienda: Aplicar sulfato de amonio o Aplicar nitrato de amonio")
        recomen = "Aplicar sulfato de amonio o Aplicar nitrato de amonio"
    form.descrip.data = recomen
    return render_template('recomendacion.html',form= form)

@app.route("/guardar_recomendacion", methods=['GET', 'POST'])
@login_required
def guardar_recomendacion():
    form = RecomendacionForm()
    if form.validate_on_submit():
        descrip = form.descrip.data
        de_acuerdo = form.de_acuerdo.data
        otra_sugerencia = form.otra_sugerencia.data
        recomendacion = Recomendacion(descrip=descrip, de_acuerdo=de_acuerdo, otra_sugerencia=otra_sugerencia,
                                      medicion_id=session.get('id_med'))
        db.session.add(recomendacion)
        db.session.commit()
        print('ID-------->', session.get('id_med'))
        return redirect(url_for('ingresar_datos'))
    return render_template('recomendacion.html',form=form)

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
    recs = []
    fecha_inicio = request.args.get('desde')
    fecha_fin = request.args.get('hasta')
    if fecha_inicio and fecha_fin:
        if fecha_inicio > fecha_fin:
            flash('La fecha de inicio no puede ser mayor a la fecha fin', 'warning')
        else:
            recs = db.session.query(Recomendacion).join(Medicion).filter(Medicion.fecha <= fecha_fin,
                                                                         Medicion.fecha >= fecha_inicio).all()
        #print('RECs',recs)
        serialized_labels = [
            serialize(row)
            for row in db.session.query(Recomendacion).join(Medicion).filter(Medicion.fecha <= fecha_fin,
                                                                         Medicion.fecha >= fecha_inicio).all()
        ]
        recomendaciones = dumps(serialized_labels)
        print('RECOMENDACIONES',recomendaciones)
        session['busqueda_recomendaciones'] = recomendaciones
        session['fecha_inicio'] = fecha_inicio
        session['fecha_fin'] = fecha_fin
        #session.pop('logged_in', None)
        #recs = Recomendacion.query.filter(Recomendacion.medicion.fecha <= fecha_fin, Recomendacion.medicion_id.fecha >= fecha_inicio).all()
    return render_template('historial.html',recs=recs)

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('app/static/images/hoja.png', 10, 8, 20)
        # helvetica bold 15
        self.set_font('helvetica', 'B', 15)
        self.page_width = self.w - 2 * self.l_margin
        # Title
        self.cell(self.page_width, 0.0,'Reporte de Recomendaciones', align='C')
        # Line break
        # self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # helvetica italic 8
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

@app.route('/imprimir')
@login_required
def imprimir_reporte():
    document= PDF()
    document.alias_nb_pages()
    document.add_page()
    document.set_font('Times', '', 12)
    th = document.font_size
    col_width = document.page_width / 4
    document.ln(6 * th)
    document.cell(col_width/2, th, 'Desde:', border=0)
    document.cell(col_width/2, th,  str(session.get('fecha_inicio')), border=0)
    document.cell(col_width/2, th, 'Hasta:', border=0)
    document.cell(col_width/2, th,  str(session.get('fecha_fin')), border=0)
    document.ln(2 * th)
    document.cell(col_width, th, 'N°', border=1)
    document.cell(col_width, th, 'Descripción', border=1)
    document.ln(th)
    recos = ast.literal_eval(session.get('busqueda_recomendaciones'))
    for i in recos:
        document.cell(col_width, th, str(i['id']), border=1)
        document.cell(col_width, th, i['descrip'], border=1)
        document.ln(th)
    return Response(document.output(dest='S'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=recomendaciones.pdf'})

# def get_recomendaciones(fecha_desde,fecha_hasta):
#     recs = db.session.query(Recomendacion).join(Medicion).filter(Medicion.fecha <= fecha_hasta,
#                                                                  Medicion.fecha >= fecha_desde).all()
#     return recs
