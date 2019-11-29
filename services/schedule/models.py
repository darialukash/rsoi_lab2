from services.schedule import db, ma
from flask_login import UserMixin

from services.users.models import PaginatedAPIMIXIN
from flask import url_for


class Schedules(PaginatedAPIMIXIN, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_card = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_data = db.Column(db.String(280))


class SchedulesSchema(ma.ModelSchema):
    class Meta:
        model = Schedules
