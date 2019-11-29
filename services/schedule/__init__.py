from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from services.schedule.config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)

from services.schedule.resourses import ScheduleResourse, SchedulesResourse

api.add_resource(SchedulesResourse,  '/schedule')
api.add_resource(ScheduleResourse,  '/schedule', '/schedule/<id>')
