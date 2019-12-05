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
    PORT = os.environ.get('USERS_PORT') or 5001
    HOST = os.environ.get('USERS_HOST') or "http://127.0.0.1"
    USER_SERVER_NAME = str(HOST) + ":" + str(PORT)
    SECRET_KEY = os.environ.get('USERS_SECRET_KEY') or "12334"
    SQLALCHEMY_DATABASE_URI = os.environ.get('USERS_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'test_users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
