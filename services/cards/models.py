from services.cards import db, ma
from flask_login import UserMixin

from services.users.models import PaginatedAPIMIXIN
from flask import url_for


class Cards(PaginatedAPIMIXIN, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    dd = db.Column(db.Integer)
    mm = db.Column(db.Integer)
    yy = db.Column(db.Integer)
    sex = db.Column(db.String(1))
    user_id = db.Column(db.Integer, unique=True)


class CardSchema(ma.ModelSchema):
    class Meta:
        model = Cards

