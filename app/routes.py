from datetime import date, datetime
from io import BytesIO

from flask import render_template, url_for, flash, redirect, request, Response, session, jsonify, current_app, send_file
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import and_, or_
from app import app, db, bcrypt, mail
from app.models import Usuario, Rol, Bloque, Medicion, Variedad, Cama, Recomendacion, Permission
from app.utils import send_reset_email, serialize, PDF, MedicionesToExcel
from json import dumps
import keras
import numpy as np
import pandas as pd
from keras.models import model_from_json
from numpy import array
from app.utils import permission_required, admin_required

@app.context_processor
def inject_permissions():
 return dict(Permission=Permission)

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
def crear_usuario():
    roles = db.session.query(Rol).all();
    if request.method == 'POST':
        email = request.form.get("email")
        user = Usuario.query.filter_by(email=email).first()
        if user:
            flash('Ya existe un usuario con ese correo', 'warning')
        else:
            pwd = request.form.get("password")
            if len(pwd) < 8:
                flash('La contraseña debe tener como mínimo 8 caracteres', 'warning')
            else:
                rol = request.form.get("rol")
                password = bcrypt.generate_password_hash(pwd).decode('utf-8')
                usuario = Usuario(email=email, password=password, role_id=rol)
                db.session.add(usuario)
                db.session.commit()
                flash('Usuario creado exitosamente','success')
                return redirect(url_for('ver_usuarios'))
    return render_template('crear_usuario.html',roles=roles)

@app.route('/usuarios',methods=['GET','POST'])
@login_required
@admin_required
def ver_usuarios():
    users = db.session.query(Usuario).join(Rol).all()
    return render_template('usuarios.html', users=users)

@app.route('/usuarios/editar/<id>',methods=['GET','POST'])
@login_required
@admin_required
def editar_usuario(id):
    user = Usuario.query.filter_by(id=id).first()
    roles = db.session.query(Rol).all()
    return render_template('editar_usuario.html',user=user, roles=roles)

@app.route('/usuarios/actualizar/<id>',methods=['GET','POST'])
@login_required
@admin_required
def actualizar_usuario(id):
    if request.method == 'POST':
        email = request.form.get("email")
        rol = request.form.get("rol")
        db.session.query(Usuario).filter(Usuario.id == id).update({Usuario.email: email, Usuario.role_id: rol})
        db.session.commit()
        flash('Usuario modificado correctamente','success')
        return redirect(url_for('ver_usuarios'))

@app.route('/usuarios/eliminar/<id>',methods=['GET','POST'])
@login_required
@admin_required
def eliminar_usuario(id):
    obj = db.session.query(Usuario).filter(Usuario.id == id).first()
    db.session.delete(obj)
    db.session.commit()
    flash('Usuario eliminado','success')
    return redirect(url_for('ver_usuarios'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = Usuario.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Error al acceder. Por favor verifique su email y/o contraseña', 'danger')
    return render_template('login.html')

# user_datastore = SQLAlchemyUserDatastore(db,Usuario,Rol)
# security = Security(app,user_datastore)

@app.route("/logout")
def logout():
    logout_user()
    session.pop('id_med', None)
    session.pop('busqueda_recomendaciones', None)
    session.pop('fecha_inicio', None)
    session.pop('fecha_fin', None)
    if session.get('datos1'):
         session.pop('datos1', None)
    return redirect(url_for('login'))

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get("email")
        user = Usuario.query.filter_by(email=email).first()
        if user is None:
            flash('No existe una cuenta con ese email. Solicite su registro al administrador.','warning')
        else:
            send_reset_email(user)
            flash('Se ha enviado un email con instrucciones para reestablecer su contraseña.', 'info')
            return redirect(url_for('login'))
    return render_template('reset_request.html')

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Usuario.verify_reset_token(token)
    if user is None:
        flash('El token es inválido o ha expirado', 'warning')
        return redirect(url_for('reset_request'))
    if request.method == 'POST':
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            flash('¡Las contraseñas no coinciden!','warning')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Su contraseña ha sido cambiada. Ahora puede iniciar sesión', 'success')
            return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reestablecer Contraseña')


# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin.base_template,
#         admin_view=admin.index_view,
#         get_url=url_for
#     )


# @app.before_first_request
# def before_first_request():
#     # Create any database tables that don't exist yet.
#     db.create_all()
#
#     # Create the Roles "admin" and "end-user" -- unless they already exist
#     user_datastore.find_or_create_role(name='admin', descripcion='Administrador')
#     user_datastore.find_or_create_role(name='tecnico', descripcion='Tecnico Agricola')
#
#     # Create two Users for testing purposes -- unless they already exists.
#     # In each case, use Flask-Security utility function to encrypt the password.
#     encrypted_password_admin = utils.hash_password('admin')
#     encrypted_password_tecnico = utils.hash_password('tecnico')
#     if not user_datastore.get_user('tecnico@example.com'):
#         user_datastore.create_user(email='tecnico@example.com', password=encrypted_password_tecnico)
#     if not user_datastore.get_user('admin@example.com'):
#         user_datastore.create_user(email='admin@example.com', password=encrypted_password_admin)
#
#     # Commit any database changes; the User and Roles must exist before we can add a Role to the User
#     db.session.commit()
#
#     # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
#     # Users already have these Roles.) Again, commit any database changes.
#     user_datastore.add_role_to_user('tecnico@example.com', 'tecnico')
#     user_datastore.add_role_to_user('admin@example.com', 'admin')
#     db.session.commit()

@app.route('/medicionform1')
@login_required
def medicionform1():
    bloques = db.session.query(Bloque).all();
    hoy = date.today()
    return render_template("parcela.html",bloques=bloques, hoy=hoy, Permission=Permission)

@app.route('/getcamas', methods=['POST'])
@login_required
def get_camas():
    req = request.json
    print('REQ',req)
    bloque_id = req['bloque_id']
    serialized_labels = [
        serialize(row)
        for row in db.session.query(Cama).join(Bloque).filter(Bloque.id == int(bloque_id))
    ]
    camas = dumps(serialized_labels)
    print('CAMAS',camas)
    return camas

@app.route('/getvariedad', methods=['POST'])
@login_required
def get_variedad():
    req = request.json
    print('REQ',req)
    cama_id = req['cama_id']
    serialized_labels = [
        serialize(row)
        for row in db.session.query(Variedad).join(Cama).filter(Cama.id == int(cama_id))
    ]
    variedad = dumps(serialized_labels)
    print('VARIEDAD',variedad)
    print('TIPO',type(variedad))
    return variedad

@app.route('/procesarform1', methods=['POST'])
@login_required
def procesarform1():
    #if isinstance(request.form.get("fechamed"), str):
    #    fecha_med = datetime.strptime(request.form.get("fechamed"), "%Y-%m-%d").date()
    fecha_med = datetime.strptime(request.form.get("fechamed"), "%Y-%m-%d")
    if fecha_med.date() > date.today():
        flash('La fecha de la medicion no puede ser mayor a la fecha de hoy', 'warning')
        return redirect(url_for('medicionform1'))
    else:
        cama_id = request.form.get("cama")
        muestreo = request.form.get("muestreo")
        query = db.session.query(Medicion).filter(and_(Medicion.cama_id == int(cama_id),or_(Medicion.muestreo == int(muestreo), Medicion.fecha == fecha_med)))
        print('Q',query.count())
        if query.count() == 0:
            arroz = request.form.get("arroz")
            arveja = request.form.get("arveja")
            garbanzo = request.form.get("garbanzo")
            lenteja = request.form.get("lenteja")
            pcolor = request.form.get("pcolor")
            rcolor = request.form.get("rcolor")
            colord = request.form.get("colord")
            prom_arroz = request.form.get("prom_arroz") if request.form.get("prom_arroz") else None
            prom_arveja = request.form.get("prom_arveja") if request.form.get("prom_arveja") else None
            prom_garbanzo = request.form.get("prom_garb") if request.form.get("prom_garb") else None
            prom_lenteja = request.form.get("prom_lenteja") if request.form.get("prom_lenteja") else None
            prom_pcolor = request.form.get("prom_pcolor") if request.form.get("prom_pcolor") else None
            prom_rcolor = request.form.get("prom_rcolor") if request.form.get("prom_rcolor") else None
            prom_colord = request.form.get("prom_colord") if request.form.get("prom_colord") else None
            session['datos1'] = {'arroz':arroz,"prom_arroz":prom_arroz,"arveja":arveja,"prom_arveja":prom_arveja,
                                "garbanzo":garbanzo,"prom_garbanzo":prom_garbanzo,"lenteja":lenteja,"prom_lenteja":prom_lenteja,
                                "pcolor":pcolor,"prom_pcolor":prom_pcolor,"rcolor":rcolor,"prom_rcolor":prom_rcolor,
                                "colord":colord,"prom_colord":prom_colord,"muestreo":muestreo,"fecha_med":fecha_med,'cama_id':cama_id}
            print(session['datos1'])
            return redirect(url_for('medicionform2'))
        else:
            flash('Ya existe una medición realizada en esa fecha', 'danger')
            return redirect(url_for('medicionform1'))

@app.route("/medicionform2")
@login_required
def medicionform2():
    if session.get('datos1') == None:
        return redirect(url_for('medicionform1'))
    else:
        #fecha = session.get('datos1')['fecha_med']
        fecha = session.get('datos1')['fecha_med'].strftime("%d/%m/%Y")
        #fecha = datetime.strptime(session.get('datos1')['fecha_med'], "%Y-%m-%d").date()
    return render_template('ingreso_datos.html',fecha=fecha)

@app.route("/ingresar_datos", methods=['GET', 'POST'])
@login_required
def ingresar_datos():
    if request.method == 'POST':
        d12 = request.form.get("cec") if request.form.get("cec") else None
        d13 = request.form.get("phc") if request.form.get("phc") else None
        d14 = request.form.get("dec") if request.form.get("dec") else None
        d15 = request.form.get("cet") if request.form.get("cet") else None
        d16 = request.form.get("pht") if request.form.get("pht") else None
        d17 = request.form.get("ceg") if request.form.get("ceg") else None
        d18 = request.form.get("phg") if request.form.get("phg") else None
        d21 = request.form.get("cep") if request.form.get("cep") else None
        d22 = request.form.get("php") if request.form.get("php") else None
        ph = request.form.get("ph")
        densidad = request.form.get("densidad")
        cond_elec = request.form.get("ce")
        datosf1 = session.get('datos1')
        medicion = Medicion(ph=ph, densidad=densidad, cond_elec=cond_elec,
                        fecha=datosf1['fecha_med'], cant_arr=datosf1['arroz'], pro_arr=datosf1['prom_arroz'], cant_arv=datosf1['arveja'],
                        pro_arv=datosf1['prom_arveja'], cant_gar=datosf1['garbanzo'], pro_gar=datosf1['prom_garbanzo'], cant_len=datosf1['lenteja'],
                        prolent=datosf1['prom_lenteja'],cant_pintcolor=datosf1['pcolor'], pro_pintcolor=datosf1['prom_pcolor'],
                        cant_raycolor=datosf1['rcolor'], pro_raycolor=datosf1['prom_rcolor'], cant_colordef=datosf1['colord'],
                        pro_colordef=datosf1['prom_colord'],muestreo=datosf1['muestreo'],ce_compost=d12,ph_compost=d13,de_compost=d14,
                        ce_tanque=d15,ph_tanque=d16,ce_goteo=d17,ph_goteo=d18,ce_programac=d21,ph_programac=d22,cama_id=datosf1['cama_id'])
        db.session.add(medicion)
        db.session.commit()
        count_med = db.session.query(Medicion).count()
        session.pop('datos1', None)
        if count_med <= 10:
            flash('La medicion fue guardada exitosamente. Por favor ingrese %2d mediciones para obtener una recomendacion'%(11-count_med),'success')
            return redirect(url_for('medicionform1'))
        else:
            session['id_med'] = medicion.id
            return redirect(url_for('get_recomendacion'))
    return render_template('ingreso_datos.html')

@app.route("/get_recomendacion")
@login_required
def get_recomendacion():
    ph = db.session.query(Medicion.ph).all();
    ph = pd.DataFrame(ph, columns=['Name'])
    datosph = ph.values.astype('float32')
    den = db.session.query(Medicion.densidad).all();
    den = pd.DataFrame(den, columns=['Name'])
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
    loaded_model.load_weights("app/static/modelo/app.h5")
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
        print("Se Recomienda: Incorporar Compost o Cambio de lugar")
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
    return render_template('recomendacion.html',rec=recomen)


@app.route("/guardar_recomendacion", methods=['GET', 'POST'])
@login_required
def guardar_recomendacion():
    if request.method=='POST':
        descrip = request.form.get("descrip")
        de_acuerdo = request.form.get("de_acuerdo")
        otra_sugerencia = request.form.get("otra_sugerencia")
        recomendacion = Recomendacion(descrip=descrip, de_acuerdo=de_acuerdo, otra_sugerencia=otra_sugerencia,
                                      medicion_id=session.get('id_med'))
        db.session.add(recomendacion)
        db.session.commit()
        print('ID-------->', session.get('id_med'))
        return redirect(url_for('medicionform1'))
    return render_template('recomendacion.html')

@app.route('/reportemedicion', methods=['GET', 'POST'])
@login_required
def reporte_medicion():
    variedades = db.session.query(Variedad).all()
    return render_template('reporte_mediciones.html',variedades=variedades)

@app.route('/imprimirmed', methods=['GET','POST'])
@login_required
def print_reporte_medicion():
    if request.method == 'POST':
        busqueda = []
        results = []
        print(request.form.get('buscarpor'))
        if request.form.get('buscarpor') == '0' or request.form.get('buscarpor') == '1' or request.form.get('buscarpor') == '2':
            desde = request.form.get('desde')
            hasta = request.form.get('hasta')
            if desde > hasta:
                flash('El numero Desde no puede ser mayor al numero Hasta','warning')
            else:
                if request.form.get('buscarpor') == '0':
                    busqueda = db.session.query(Medicion).join(Cama).join(Bloque).filter(Bloque.num_bloque>= int(desde),Bloque.num_bloque<= int(hasta))
                elif request.form.get('buscarpor') == '1':
                    busqueda = db.session.query(Medicion).join(Cama).filter(Cama.num_cama >= int(desde),
                                                                                         Cama.num_cama <= int(hasta))
                elif request.form.get('buscarpor') == '2':
                    busqueda = db.session.query(Medicion).filter(Medicion.muestreo >= int(desde),
                                                                            Medicion.muestreo <= int(hasta))
        elif request.form.get('buscarpor') == '3':
                variedades = request.form.getlist('variedad')
                busqueda = db.session.query(Medicion).join(Cama).join(Variedad).filter(Variedad.nombre_var.in_(variedades))
                print('VARIEDADES', variedades)
        else:
            fecha_desde = request.form.get('fechadesde')
            fecha_hasta = request.form.get('fechahasta')
            if fecha_desde > fecha_hasta:
                flash('La fecha Desde no puede ser mayor a la fecha Hasta','warning')
            else:
                busqueda = db.session.query(Medicion).filter(Medicion.fecha <= fecha_hasta,
                                                                         Medicion.fecha >= fecha_desde).all()
        if busqueda:
            for item in busqueda:
                r = []
                r.append(item.fecha.strftime("%d/%m/%Y"))
                r.append(item.medcama.cama.num_bloque)
                r.append(item.muestreo)
                r.append(item.medcama.camav.nombre_var)
                r.append(item.medcama.num_cama)
                r.append(item.ph)
                r.append(item.densidad)
                r.append(item.cond_elec)
                r.append(item.ph_compost)
                r.append(item.de_compost)
                r.append(item.ce_compost)
                r.append(item.ph_tanque)
                r.append(item.ce_tanque)
                r.append(item.ph_goteo)
                r.append(item.ce_goteo)
                r.append(item.ph_programac)
                r.append(item.ce_programac)
                r.append(item.cant_arr)
                r.append(item.pro_arr)
                r.append(item.cant_arv)
                r.append(item.pro_arv)
                r.append(item.cant_gar)
                r.append(item.pro_gar)
                r.append(item.cant_len)
                r.append(item.prolent)
                r.append(item.cant_pintcolor)
                r.append(item.pro_pintcolor)
                r.append(item.cant_raycolor)
                r.append(item.pro_raycolor)
                r.append(item.cant_colordef)
                r.append(item.pro_colordef)
                results.append(r)
            print('Results', results)
            m2e = MedicionesToExcel(results)
            file_stream = BytesIO()
            m2e.save(file_stream)
            file_stream.seek(0)
        else:
            flash('No existen resultados','warning')
            return redirect(url_for('reporte_medicion'))
        return send_file(file_stream, attachment_filename="Mediciones.xls", as_attachment=True)

@app.route('/historial', methods=['GET', 'POST'])
@login_required
def buscar_recomendaciones():
    if session.get('busqueda_recomendaciones'):
        session.pop('busqueda_recomendaciones',None)
    recs = []
    results = []
    fecha_inicio = request.args.get('desde')
    fecha_fin = request.args.get('hasta')
    if fecha_inicio and fecha_fin:
        if fecha_inicio > fecha_fin:
            flash('La fecha de inicio no puede ser mayor a la fecha fin', 'warning')
        else:
            recs = db.session.query(Recomendacion).join(Medicion).filter(Medicion.fecha <= fecha_fin,
                                                                         Medicion.fecha >= fecha_inicio).all()
        if recs:
            for row in recs:
                r = {}
                r['n'] = row.id
                r['recomendacion'] = row.descrip
                r['de_acuerdo'] = row.de_acuerdo
                r['otra_sugerencia'] = row.otra_sugerencia
                r['fecha'] = row.medicion.fecha
                results.append(r)
            print('RECos',results)
            session['busqueda_recomendaciones'] = results
            session['fecha_inicio'] = fecha_inicio
            session['fecha_fin'] = fecha_fin
        else:
            flash('No existen resultados', 'warning')
    return render_template('historial_recomendaciones.html', recs=recs)

@app.route('/imprimir')
@login_required
def imprimir_reporte():
    if session.get('busqueda_recomendaciones'):
        document = PDF(format='A4',orientation='portrait')
        document.alias_nb_pages()
        document.add_page()
        th = document.font_size
        col_width_cab = document.page_width / 4
        document.ln(6 * th)
        document.set_font('helvetica', 'B', 12)
        document.cell(col_width_cab / 2, th, 'Desde:', border=0)
        document.set_font('helvetica', '', 12)
        document.cell(col_width_cab / 2, th, "{}".format(session.get('fecha_inicio')), border=0)
        document.set_font('helvetica', 'B', 12)
        document.cell(col_width_cab / 2, th, 'Hasta:', border=0)
        document.set_font('helvetica', '', 12)
        document.cell(col_width_cab / 2, th, "{}".format(session.get('fecha_fin')), border=0)
        document.ln(2 * th)
        col_width_tab = document.page_width
        document.cell((col_width_tab*7)/100, th, 'N°', border=1)
        document.cell((col_width_tab*33)/100, th, 'Descripción', border=1)
        document.cell((col_width_tab*14)/100, th, 'De Acuerdo', border=1)
        document.cell((col_width_tab*33)/100, th, 'Sugerencia', border=1)
        document.cell((col_width_tab*13)/100, th, 'Fecha', border=1)
        document.ln(th)
        document.set_font('helvetica', '', 12)
        recos = session.get('busqueda_recomendaciones')
        #recos = ast.literal_eval(session.get('busqueda_recomendaciones'))
        for i in recos:
            top = document.y
            offset = document.x + ((col_width_tab * 33) / 100)
            document.multi_cell((col_width_tab*7)/100, 2*th, str(i['n']),1,0)
            document.y = top
            document.x = offset
            document.multi_cell((col_width_tab*33)/100, 2*th, i['recomendacion'],1,0)
            # top2 = document.y
            offset2 = document.x + ((col_width_tab * 14) / 100)
            document.multi_cell((col_width_tab*14)/100, 2*th, i['de_acuerdo'],1,0)
            # document.y = top2
            document.x = offset2
            document.multi_cell((col_width_tab*33)/100, 2*th, i['otra_sugerencia'],1,0)
            # top3= document.y
            offset3 = document.x + ((col_width_tab * 13) / 100)
            document.multi_cell((col_width_tab*13)/100, 2*th,i['fecha'],1,0)
            # document.y = top3
            document.x = offset3
            document.ln(2*th)

        return Response(document.output(dest='S'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=mediciones.pdf'})
    else:
        flash('Realice primero una búsqueda', 'danger')
        return redirect(url_for('buscar_recomendaciones'))
