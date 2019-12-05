import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig(object):
    DEBUG = True
    PORT = 5002
    HOST = "http://127.0.0.1"
    CARDS_SERVER_NAME = HOST + ":" + str(PORT)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jfhkyjutyghjgdjhfu78'
    SQLALCHEMY_DATABASE_URI = os.environ.get('CARDS_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'cards.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    DEBUG = True
    PORT = os.environ.get('CARDS_PORT') or 5002
    HOST = os.environ.get('CARDS_HOST') or  "http://127.0.0.1"
    CARDS_SERVER_NAME = str(HOST) + ":" + str(PORT)
    SECRET_KEY = os.environ.get('CARDS_SECRET_KEY') or 'jfhkyjutyghjgdjhfu78'
    SQLALCHEMY_DATABASE_URI = os.environ.get('CARDS_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'test_cards.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
