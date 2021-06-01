from datetime import datetime
from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(20), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipous.id'), nullable=False)

    def __repr__(self):
        return f"Usuario('{self.usuario}', '{self.email}', '{self.image_file}')"

class Tipous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_us = db.Column(db.String(20), nullable=False)
    usuarios = db.relationship('Usuario', backref='usuario', lazy=True)
