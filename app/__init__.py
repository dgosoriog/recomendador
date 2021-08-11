from flask import Flask, redirect, url_for, session
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin import Admin, AdminIndexView, expose
from flask_babelex import Babel
from flask_security import current_user, Security
from flask_mail import Mail
from flask_login import LoginManager

from flask_principal import Principal, Identity, AnonymousIdentity, \
    identity_changed, identity_loaded, UserNeed, RoleNeed, Permission
import os
#from app.config import Config
#mail = Mail()
#db = SQLAlchemy()
#def create_app(config_class=Config):

app = Flask(__name__)
#app.config.from_object(Config)
app.config['SECRET_KEY'] = b'3\x0f\x85\xb6\xf8M4P\x8e\xedA\xb8\xf0\xd5#\t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baseaf.db'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
#app.config['SECURITY_PASSWORD_SALT'] = 'MDfy8APT'
#app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'login.html'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']='floricolaasistente5@gmail.com'
app.config['MAIL_PASSWORD']='MO2021818'
app.config['AF_ADMIN'] ='oso95d@gmail.com'
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
# class AdminView(ModelView):
#     #@expose('/')
#     def is_accessible(self):
#         return current_user.has_role('admin')
#
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('login'))
#
# class MyAdminIndexView(AdminIndexView):
#     @expose('/')
#     def home_admin(self):
#          return self.render('admin/index.html')
#
#     def is_accessible(self):
#         return current_user.has_role('admin')
#
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('login'))
#
# admin = Admin(app,'Admin', url='/home',index_view=MyAdminIndexView())
# admin.name = "Recomendador"
# admin.template_mode = "bootstrap4"
# admin.add_link(MenuLink(name='Salir', url='/logout'))
# babel = Babel(app)
# @babel.localeselector
# def get_locale():
#      override = 'es'
#      if override:
#          session['lang'] = override
#      return session.get('lang', 'en')
from app.errors.handlers import errors
app.register_blueprint(errors)

from app import routes
#mail.init_app(app)
#db.init_app(app)

 # attach routes and custom error pages here
 # from app.main.routes import main
 # app.register_blueprint(main)
 # return app