from flask import Flask, request
from flask_restful import Api
from services.users.config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
# login = LoginManager(app)
api = Api(app)

from services.users.resourses import UserResourse, FirstResourse, GateDocsResourse,  \
    GateAddtoDocResourse, GateUserScheduleResourse, GateCardResourse

api.add_resource(FirstResourse, '/api')
api.add_resource(UserResourse, '/api/users', '/api/users/<id>')  # User
api.add_resource(GateCardResourse, '/api/users/<id>/card')  # User card
api.add_resource(GateDocsResourse, '/api/doctors')  # Return all doctors
api.add_resource(GateUserScheduleResourse, '/api/users/<id>/schedule')  # Return current user schedule
api.add_resource(GateAddtoDocResourse,
                 '/api/users/<id>/schedule/<id_card>')  # Return doctor schedule schedule of current user
