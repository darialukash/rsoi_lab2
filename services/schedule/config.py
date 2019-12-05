import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig(object):
    DEBUG = True
    PORT = 5004
    HOST = "http://127.0.0.1"
    APPOINT_SERVER_NAME = HOST + ":" + str(PORT)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jfhkyj089978090870utyghjgdjhfu78'
    SQLALCHEMY_DATABASE_URI = os.environ.get('APPOINTS_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'appoints.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    DEBUG = True
    PORT = os.environ.get('SCHEDULE_PORT') or 5004
    HOST = os.environ.get('SCHEDULE_HOST') or "http://127.0.0.1"
    DOCTORS_SERVER_NAME = str(HOST) + ":" + str(PORT)
    SECRET_KEY = os.environ.get('SCHEDULE_SECRET_KEY') or 'jfdjhfu78'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SCHEDULE_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'test_appoints.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
