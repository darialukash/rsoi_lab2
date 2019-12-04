import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig(object):
    DEBUG = True
    PORT = 5003
    HOST = "http://127.0.0.1"
    DOC_SERVER_NAME = HOST + ":" + str(PORT)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jfhkyjutyghj576567657gdjhfu78'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DOC_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'doctors.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    DEBUG = True
    PORT = os.environ.get('DOCTORS_PORT')
    HOST = os.environ.get('DOCTORS_HOST')
    DOCTORS_SERVER_NAME = str(HOST) + ":" + str(PORT)
    SECRET_KEY = os.environ.get('DOCTORS_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DOCTORS_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
