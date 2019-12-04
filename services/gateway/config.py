import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig(object):
    DEBUG = True
    PORT = 5000
    HOST = "http://127.0.0.1"
    GATE_SERVER_NAME = HOST + ":" + str(PORT)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jfhky56456456jutyghgfhjgdjhfu78'



class TestConfig(object):
    DEBUG = True
    PORT = os.environ.get('GATEWAY_PORT')
    HOST = os.environ.get('GATEWAY_HOST')
    GATE_SERVER_NAME = str(HOST) + ":" + str(PORT)
    SECRET_KEY = os.environ.get('GATEWAY_SECRET_KEY')
