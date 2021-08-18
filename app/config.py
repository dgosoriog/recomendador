import os
#basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = b'3\x0f\x85\xb6\xf8M4P\x8e\xedA\xb8\xf0\xd5#\t'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///baseaf.db'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root',
                                                                                        password='',
                                                                                        server='localhost',
                                                                                        database='baseaf')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'floricolaasistente5@gmail.com'
    MAIL_PASSWORD = 'MO2021818'
    #AF_ADMIN = 'oso95d@gmail.com'
#     @staticmethod
#     def init_app(app):
#         pass
#
# class DevelopmentConfig(Config):
#     DEBUG = True
#
# class TestingConfig(Config):
#     TESTING = True
#
# class ProductionConfig(Config):
#     TESTING = True
#
# config = {
#  'development': DevelopmentConfig,
#  'testing': TestingConfig,
#  'production': ProductionConfig,
#  'default': DevelopmentConfig
# }