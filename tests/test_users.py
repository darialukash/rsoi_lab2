import unittest

from services.users import app, db, resourses
from services.users.models import User, UserSchema, set_password
from services.users.resourses import FirstResourse, UserResourse
from services.users.config import TestConfig
from base64 import b64encode
import json

app.config.from_object(TestConfig)

patient1 = {"id": 1, "email": "one@dot.com", "password": "qwerty12"}
patient2 = {"id": 2, "email": "two@dot.com", "password": "qwerty34"}


class TestUserService(unittest.TestCase):

    def test_get(self):
        with app.app_context() as context:
            context.push()
            db.drop_all()
            db.create_all()
            self.assertIsNone(User.query.get(1))

    def test_exist(self):
        with app.app_context() as context:
            context.push()
            db.drop_all()
            db.create_all()
            patient1.update({"password_hash": set_password(patient1['password'])})
            user = UserSchema().make_instance(patient1, partial=False)
            db.session.add(user)
            db.session.commit()
            exist = User.query.get(patient1["id"])
            self.assertEqual(user.id, exist.id)

    def test_get_api(self):
        client = app.test_client()
        response = client.get('/api')
        self.assertEqual(response.status_code, 200)

    def test_post_user(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.drop_all()
                db.create_all()
                patient1.update({"password_hash": set_password(patient1['password'])})
                user = UserSchema().make_instance(patient1, partial=False)
                db.session.add(user)
                db.session.commit()
                authent = 'Basic %s' % b64encode(bytes(patient1["email"] + ':' + patient1["password"],
                                                       "utf-8")).decode("ascii")
                response = client.get('/api/users/1', headers=dict(Authorization=f"{authent}"))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["email"], patient1["email"])


if __name__ == '__main__':
    unittest.main()
