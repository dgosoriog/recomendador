from flask import Flask, redirect, url_for, session
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin import Admin, AdminIndexView, expose
from flask_babelex import Babel
from flask_security import current_user
from flask_mail import Mail
import os
#from app.config import Config
#mail = Mail()
#db = SQLAlchemy()
#def create_app(config_class=Config):

app = Flask(__name__)
#app.config.from_object(Config)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basereco.db'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECURITY_PASSWORD_SALT'] = 'abcdefg'
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'templates/login.html'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']='oso95d@gmail.com'
app.config['MAIL_PASSWORD']='myfirstaccount'
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def home_admin(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app,index_view=MyAdminIndexView())
admin.name = "Recomendador"
admin.template_mode = "bootstrap4"
admin.add_link(MenuLink(name='Salir', url='/logout'))
babel = Babel(app)
@babel.localeselector
def get_locale():
     override = 'es'
     if override:
         session['lang'] = override
     return session.get('lang', 'en')


from app import routes

#mail.init_app(app)
#db.init_app(app)

 # attach routes and custom error pages here
 # from app.main.routes import main
 # app.register_blueprint(main)
 # return app