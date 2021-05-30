from flask import Flask
#from flask_mail import Mail
from app.config import Config
#mail = Mail()
#db = SQLAlchemy()
def create_app(config_class=Config):
 app = Flask(__name__)
 app.config.from_object(Config)

 #mail.init_app(app)
 #db.init_app(app)

 # attach routes and custom error pages here
 from app.main.routes import main
 app.register_blueprint(main)
 return app