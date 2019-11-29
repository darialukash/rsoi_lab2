import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig(object):
    DEBUG = True
    PORT = 5001
    HOST = "http://127.0.0.1"
    USER_SERVER_NAME = HOST + ":" + str(PORT)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ghtjh1223kjijl'
    SQLALCHEMY_DATABASE_URI = os.environ.get('USERS_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    DEBUG = True
    PORT = os.environ.get('USERS_PORT')
    HOST = os.environ.get('USERS_HOST')
    USER_SERVER_NAME = str(HOST) + ":" + str(PORT)
    SECRET_KEY = os.environ.get('USERS_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('USERS_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
