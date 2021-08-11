from datetime import date

from flask import current_app

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

class Rol(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permisos = db.Column(db.Integer)
    usuarios = db.relationship('Usuario', backref='role', lazy='dynamic')

    def __repr__(self):
        return f"{self.name}"

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
        default_role = 'Tecnico'
        for r in roles:
            role = Rol.query.filter_by(name=r).first()
            if role is None:
                role = Rol(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class Usuario(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    # roles = db.relationship('Rol', secondary=roles_usuarios,
    #                         backref=db.backref('usuarios', lazy='dynamic'))
    role_id = db.Column(db.Integer, db.ForeignKey('rol.id'))

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

    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['AF_ADMIN']:
                self.role = Rol.query.filter_by(name='Administrador').first()
        if self.role is None:
            self.role = Rol.query.filter_by(default=True).first()

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
    id = db.Column(db.Integer, primary_key=True)
    ph = db.Column(db.Float, nullable=False)
    densidad = db.Column(db.Float, nullable=False)
    cond_elec = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today())
    cant_arr = db.Column(db.Integer, nullable=False)
    pro_arr = db.Column(db.Float, nullable=True)
    cant_arv = db.Column(db.Integer, nullable=False)
    pro_arv = db.Column(db.Float, nullable=True)
    cant_gar = db.Column(db.Integer, nullable=False)
    pro_gar = db.Column(db.Float, nullable=True)
    cant_len = db.Column(db.Integer, nullable=False)
    prolent = db.Column(db.Float, nullable=True)
    cant_pintcolor = db.Column(db.Integer, nullable=False)
    pro_pintcolor = db.Column(db.Float, nullable=True)
    cant_raycolor = db.Column(db.Integer, nullable=False)
    pro_raycolor = db.Column(db.Float, nullable=True)
    cant_colordef = db.Column(db.Integer, nullable=False)
    pro_colordef = db.Column(db.Float, nullable=True)
    muestreo = db.Column(db.Integer, nullable=False)
    ce_compost = db.Column(db.Float, nullable=True)
    ph_compost = db.Column(db.Float, nullable=True)
    de_compost = db.Column(db.Float, nullable=True)
    ce_tanque = db.Column(db.Float, nullable=True)
    ph_tanque = db.Column(db.Float, nullable=True)
    ce_goteo = db.Column(db.Float, nullable=True)
    ph_goteo = db.Column(db.Float, nullable=True)
    ce_programac = db.Column(db.Float, nullable=True)
    ph_programac = db.Column(db.Float, nullable=True)
    cama_id = db.Column(db.Integer, db.ForeignKey('cama.id'))
    recomendacion = db.relationship("Recomendacion", uselist=False, backref="medicion")

class Recomendacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descrip = db.Column(db.String(30), nullable=False)
    de_acuerdo = db.Column(db.Integer, unique=False)
    otra_sugerencia = db.Column(db.String(100),nullable=True, default='')
    medicion_id = db.Column(db.Integer, db.ForeignKey('medicion.id'), unique=True)

    def __repr__(self):
        return f"Recomendacion('{self.descrip}', '{self.de_acuerdo}', '{self.otra_sugerencia}', '{self.medicion.fecha}')"

class Bloque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_bloque = db.Column(db.Integer, nullable=False)
    camas = db.relationship('Cama',backref='cama')

class Variedad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_var = db.Column(db.String(20), nullable=False)
    ciclo = db.Column(db.Integer, nullable=False)
    camav = db.relationship('Cama', backref='camav')

class Cama(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_cama = db.Column(db.Integer, nullable=False)
    bloque_id = db.Column(db.Integer, db.ForeignKey('bloque.id'))
    variedad_id = db.Column(db.Integer, db.ForeignKey('variedad.id'))
    mediciones = db.relationship('Medicion', backref='medcama')