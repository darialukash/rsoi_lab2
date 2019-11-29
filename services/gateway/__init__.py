from flask import Flask
from flask_restful import Api

from services.gateway.config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app)

from services.gateway.resourses import GateCardResourse, GateDocsResourse, GateScheduleResourse

api.add_resource(GateCardResourse, '/cards', '/cards/<user_id>')
api.add_resource(GateDocsResourse, '/doctors')
api.add_resource(GateScheduleResourse, '/schedule')

