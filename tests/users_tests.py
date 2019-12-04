import unittest

from services.users import app, db, resourses
from services.users.models import User, UserSchema
from services.users.config import TestConfig

app.config.from_object(TestConfig)

patient1 = {"id": 1, "email": "one@dot.com", "password": "qwerty12"}
patient2 = {"id": 2, "email": "two@dot.com", "password": "qwerty34"}

'''
def test_session():
    app.config.from_object(TestConfig)
    db.session.remove()
    db.drop_all()
    db.create_all()


def create_user(new_user):
    db.session.add(UserSchema().load(new_user))
    db.session.commit()


def test_index(app):
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello World!' in response.data
'''


class TestUserService(unittest.TestCase):

    def test_get(self):
        app.config.from_object(TestConfig)
        with app.app_context() as context:
            context.push()
            db.drop_all()
            db.create_all()
            self.assertIsNone(User.query.get(1))

    def test_exist(self):
        app.config.from_object(TestConfig)
        with app.app_context() as context:
            context.push()
            db.drop_all()
            db.create_all()

            user = User(**patient1)
            db.session.add(user)
            db.session.commit()
            exist = User.get(patient1["id"])
            self.assertEqual(user.id, exist.id)

    def test_exeeist(self):
        pass


if __name__ == '__main__':
    unittest.main()
