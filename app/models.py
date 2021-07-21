from datetime import date
from app import db, bcrypt, app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Define models
roles_usuarios = db.Table('roles_usuarios',
        db.Column('usuario_id', db.Integer(), db.ForeignKey('usuario.id')),
        db.Column('rol_id', db.Integer(), db.ForeignKey('rol.id')))

class Rol(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    descripcion = db.Column(db.String(255))

    def __repr__(self):
        return f"{self.name}"

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Rol', secondary=roles_usuarios,
                            backref=db.backref('usuarios', lazy='dynamic'))

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

class Medicion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ph = db.Column(db.Float)
    densidad = db.Column(db.Float)
    cond_elec = db.Column(db.Float)
    fecha = db.Column(db.Date, nullable=False, default=date.today())
    Cant_arro = db.Column(db.Integer)
    pro_arr = db.Column(db.Float)
    cant_arv = db.Column(db.Integer)
    pro_arv = db.Column(db.Float)
    cant_gar = db.Column(db.Integer)
    pro_gar = db.Column(db.Float)
    cant_len = db.Column(db.Integer)
    cant_pintcolor = db.Column(db.Integer)
    pro_pintcolor = db.Column(db.Float)
    cant_raycolor = db.Column(db.Integer)
    pro_raycolor = db.Column(db.Float)
    cant_colordef = db.Column(db.Integer)
    pro_colordef = db.Column(db.Float)
    prolent = db.Column(db.Float)
    recomendacion = db.relationship("Recomendacion", uselist=False, backref="medicion")

class Recomendacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descrip = db.Column(db.String(30), nullable=False)
    puntuacion = db.Column(db.Integer)
    opinion = db.Column(db.String(100))
    medicion_id = db.Column(db.Integer, db.ForeignKey('medicion.id'), unique=True)

    def __repr__(self):
        return f"Recomendacion('{self.descrip}', '{self.puntuacion}', '{self.opinion}', '{self.medicion.fecha}')"