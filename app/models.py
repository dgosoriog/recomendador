from datetime import date
from enum import Enum

from flask import current_app
from sqlalchemy.dialects import mysql

from app import db, bcrypt, app, login
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Define models
# roles_usuarios = db.Table('roles_usuarios',
#         db.Column('usuario_id', db.Integer(), db.ForeignKey('usuario.id')),
#         db.Column('rol_id', db.Integer(), db.ForeignKey('rol.id')))

class Permission:
 INGRESAR_MEDICION = 1
 CALIFICAR_REC = 2
 CONSULTAR_REC = 4
 IMPRIMIR_REPORTE = 8
 ADMIN = 16

class Alternativas(Enum):
    A0 = 0
    A1 = 1
    A2 = 2
    A3 = 3
    A4 = 4

class Rol(db.Model):
    id = db.Column(mysql.INTEGER(10), primary_key=True)
    nombre = db.Column(db.String(20), unique=True)
    permisos = db.Column(mysql.INTEGER(2))
    usuarios = db.relationship('Usuario', backref='role', lazy='dynamic')

    def __repr__(self):
        return f"{self.nombre}"

    def __init__(self, **kwargs):
        super(Rol, self).__init__(**kwargs)
        if self.permisos is None:
            self.permisos = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permisos += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permisos -= perm

    def reset_permissions(self):
        self.permisos = 0

    def has_permission(self, perm):
        return self.permisos & perm == perm

    @staticmethod
    def insert_roles():
        '' 'No crea directamente el rol, sino que se basa en el rol existente de la base de datos y luego lo actualiza. Se puede realizar la misma operación después de cambiar el rol. '' '
        roles = {
            'Tecnico': [Permission.INGRESAR_MEDICION | Permission.CALIFICAR_REC | Permission.CONSULTAR_REC | Permission.IMPRIMIR_REPORTE],
            'Administrador': [Permission.INGRESAR_MEDICION | Permission.CALIFICAR_REC | Permission.CONSULTAR_REC | Permission.IMPRIMIR_REPORTE,
            Permission.ADMIN]
        }
        for r in roles:
            role = Rol.query.filter_by(nombre=r).first()
            if role is None:
                role = Rol(nombre=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            db.session.add(role)
        db.session.commit()


class Usuario(UserMixin,db.Model):
    id = db.Column(mysql.INTEGER(10), primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60))
    # roles = db.relationship('Rol', secondary=roles_usuarios,
    #                         backref=db.backref('usuarios', lazy='dynamic'))
    role_id = db.Column(mysql.INTEGER(10), db.ForeignKey('rol.id'))
    mediciones = db.relationship('Medicion', backref='medusuario')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Usuario.query.get(user_id)

    @login.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))

    # def __init__(self, **kwargs):
    #     super(Usuario, self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email == current_app.config['AF_ADMIN']:
    #             self.role = Rol.query.filter_by(nombre='Administrador').first()
        #if self.role is None:
        #    self.role = Rol.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False

login.anonymous_user = AnonymousUser


class Medicion(db.Model):
    id = db.Column(mysql.INTEGER(10), primary_key=True)
    ph = db.Column(db.Float(precision='3,2'), nullable=False)
    densidad = db.Column(db.Float(precision='3,2'), nullable=False)
    cond_elec = db.Column(db.Float(precision='3,2'), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today())
    cant_arr = db.Column(mysql.INTEGER(3), nullable=False)
    pro_arr = db.Column(db.Float(precision='3,2'), nullable=True)
    cant_arv = db.Column(mysql.INTEGER(3), nullable=False)
    pro_arv = db.Column(db.Float(precision='3,2'), nullable=True)
    cant_gar = db.Column(mysql.INTEGER(3), nullable=False)
    pro_gar = db.Column(db.Float(precision='3,2'), nullable=True)
    cant_len = db.Column(mysql.INTEGER(3), nullable=False)
    prolent = db.Column(db.Float(precision='3,2'), nullable=True)
    cant_pintcolor = db.Column(mysql.INTEGER(3), nullable=False)
    pro_pintcolor = db.Column(db.Float(precision='3,2'), nullable=True)
    cant_raycolor = db.Column(mysql.INTEGER(3), nullable=False)
    pro_raycolor = db.Column(db.Float(precision='3,2'), nullable=True)
    cant_colordef = db.Column(mysql.INTEGER(3), nullable=False)
    pro_colordef = db.Column(db.Float(precision='3,2'), nullable=True)
    muestreo = db.Column(mysql.INTEGER(3), nullable=False)
    ce_compost = db.Column(db.Float(precision='3,2'), nullable=True)
    ph_compost = db.Column(db.Float(precision='3,2'), nullable=True)
    de_compost = db.Column(db.Float(precision='3,2'), nullable=True)
    ce_tanque = db.Column(db.Float(precision='3,2'), nullable=True)
    ph_tanque = db.Column(db.Float(precision='3,2'), nullable=True)
    ce_goteo = db.Column(db.Float(precision='3,2'), nullable=True)
    ph_goteo = db.Column(db.Float(precision='3,2'), nullable=True)
    ce_programac = db.Column(db.Float(precision='3,2'), nullable=True)
    ph_programac = db.Column(db.Float(precision='3,2'), nullable=True)
    cama_id = db.Column(mysql.INTEGER(10), db.ForeignKey('cama.id'))
    usuario_id = db.Column(mysql.INTEGER(10), db.ForeignKey('usuario.id'))
    recomendacion = db.relationship("Recomendacion", uselist=False, backref="medicion")

class Recomendacion(db.Model):
    id = db.Column(mysql.INTEGER(10), primary_key=True)
    descrip = db.Column(db.String(40), nullable=False)
    de_acuerdo = db.Column(db.String(2), nullable=False, unique=False)
    otra_sugerencia = db.Column(mysql.INTEGER(1),nullable=True)
    medicion_id = db.Column(mysql.INTEGER(10), db.ForeignKey('medicion.id'), unique=True)

    def __repr__(self):
        return f"Recomendacion('{self.descrip}', '{self.de_acuerdo}', '{self.otra_sugerencia}', '{self.medicion.fecha}')"

class Bloque(db.Model):
    id = db.Column(mysql.INTEGER(10), primary_key=True)
    num_bloque = db.Column(mysql.INTEGER(3), nullable=False)
    camas = db.relationship('Cama',backref='cama')

class Variedad(db.Model):
    id = db.Column(mysql.INTEGER(10), primary_key=True)
    nombre_var = db.Column(db.String(20), nullable=False)
    ciclo = db.Column(mysql.INTEGER(2), nullable=False)
    camav = db.relationship('Cama', backref='camav')

class Cama(db.Model):
    id = db.Column(mysql.INTEGER(10), primary_key=True)
    num_cama = db.Column(mysql.INTEGER(3), nullable=False)
    bloque_id = db.Column(mysql.INTEGER(10), db.ForeignKey('bloque.id'))
    variedad_id = db.Column(mysql.INTEGER(10), db.ForeignKey('variedad.id'))
    mediciones = db.relationship('Medicion', backref='medcama')