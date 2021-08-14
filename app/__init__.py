from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager
from app.config import Config
#mail = Mail()
#db = SQLAlchemy()
#def create_app(config_class=Config):

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = 'login'
login.refresh_view = 'relogin'
login.needs_refresh_message = (u"La sesión ha expirado, por favor vuelva a iniciar sesión")
login.needs_refresh_message_category = "info"

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