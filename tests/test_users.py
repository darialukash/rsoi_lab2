import unittest

from services.users import app, db, resourses
from services.users.models import User, UserSchema
from services.users.config import TestConfig

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
        from services.users.models import set_password
        with app.app_context() as context:
            context.push()
            db.drop_all()
            db.create_all()
            user = UserSchema().make_instance(patient1, partial=False)
            client = app.test_client()
            response = client.post('/api', user)
            getting = client.get('/api/users/1')
            self.assertEqual(response.status_code, 200).json()
            self.assertEqual(getting["email"], patient1["email"])

if __name__ == '__main__':
    unittest.main()
