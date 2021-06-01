from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_mail import Mail
#from app.config import Config
#mail = Mail()
#db = SQLAlchemy()
#def create_app(config_class=Config):
app = Flask(__name__)
#app.config.from_object(Config)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#db = SQLAlchemy(app)
from app import routes
#mail.init_app(app)
#db.init_app(app)

 # attach routes and custom error pages here
 # from app.main.routes import main
 # app.register_blueprint(main)
 # return app