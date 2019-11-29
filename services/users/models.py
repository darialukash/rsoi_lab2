from services.users import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for, jsonify
from marshmallow import pre_load, fields
from flask_restful import Resource


class PaginatedAPIMIXIN(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(PaginatedAPIMIXIN, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# @login.user_loader
# def load_user(id):
#    return User.query.get(int(id))


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

        fields = ('id', 'email')


def set_password(password):
    return generate_password_hash(password)
