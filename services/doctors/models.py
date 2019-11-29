from services.doctors import db, ma
from flask_login import UserMixin

from services.users.models import PaginatedAPIMIXIN
from flask import url_for


class Doctors(PaginatedAPIMIXIN, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_card = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    specialization = db.Column(db.String(64))


class DoctorSchema(ma.ModelSchema):
    class Meta:
        model = Doctors
