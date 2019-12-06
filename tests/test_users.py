import unittest
from unittest.mock import patch
from flask import jsonify, make_response, request

from services.users import app, db
from services.users.models import User, UserSchema, set_password
from services.users.resourses import FirstResourse, UserResourse, GateDocsResourse, GateCardResourse
from services.users.config import TestConfig
from base64 import b64encode

app.config.from_object(TestConfig)

card1 = {"id": 1, "email": "one@dot.com", "password": "qwerty12"}
card2 = {"id": 2, "email": "two@dot.com", "password": "qwerty34"}

patient1 = {"id": 1, "name": "Alica", "surname": "Ivanova", "dd": 13, "mm": 10, "yy": 1995, "sex": "f", "user_id": 1}
patient1_update = {"user_id": 1, "dd": 18}
patient2 = {"id": 2, "name": "Alex", "surname": "Sidorov", "dd": 23, "mm": 6, "yy": 1993, "sex": "m", "user_id": 2}
patient3 = {"id": 3, "name": "Sonya", "surname": "Frolova", "dd": 28, "mm": 1, "yy": 1992, "sex": "f", "user_id": 3}

doctor1 = {"id": 1, "id_card": 1000, "name": "Maria", "surname": "Kot", "specialization": "family medicine"}
doctor2 = {"id": 2, "id_card": 2000, "name": "Pavel", "surname": "Un", "specialization": "allergology"}
doctor3 = {"id": 3, "id_card": 2010, "name": "Alica", "surname": "Volkova", "specialization": "cardeology"}
doctor4 = {"id": 4, "id_card": 4000, "name": "Sergei", "surname": "Somov", "specialization": "family medicine"}

appoint1 = {"id": 1, "id_card": 1000, "user_id": 1, "user_data": "Alica Ivannova f 13-10-1995"}
appoint2 = {"id": 2, "id_card": 2000, "user_id": 1, "user_data": "Alica Ivannova f 13-10-1995"}
appoint3 = {"id": 3, "id_card": 2010, "user_id": 1, "user_data": "Alica Ivannova f 13-10-1995"}
appoint4 = {"id": 4, "id_card": 4000, "user_id": 1, "user_data": "Alica Ivannova f 13-10-1995"}
appoint6 = {"id": 2, "id_card": 4000, "user_id": 2, "user_data": "Pavel Sidorov m 23-6-1993"}

body_sched = {
    'appointment': {'id_card': '4000', 'user_data': 'Alex Sidorov m 23-6-1993', 'user_id': '2'},
    'doctor': {'id': 4, 'id_card': 4000, 'name': 'Sergei', 'specialization': 'family medicine', 'surname': 'Somov'},
    'messagge': 'An appointment created'
}

authent = 'Basic %s' % b64encode(bytes(card1["email"] + ':' + card1["password"], "utf-8")).decode("ascii")


class TestUserService(unittest.TestCase):

    def test_get(self):
        with app.app_context() as context:
            context.push()
            db.session.remove()
            db.drop_all()
            db.create_all()
            self.assertIsNone(User.query.get(1))
            db.session.remove()

    def test_exist(self):
        with app.app_context() as context:
            context.push()
            db.session.remove()
            db.drop_all()
            db.create_all()
            patient1.update({"password_hash": set_password(card1['password'])})
            user = UserSchema().make_instance(card1, partial=False)
            db.session.add(user)
            db.session.commit()
            exist = User.query.get(card1["id"])
            self.assertEqual(user.id, exist.id)
            db.session.remove()

    def test_get_api(self):
        with app.app_context() as context:
            context.push()
            db.session.remove()
            db.drop_all()
            db.create_all()
            client = app.test_client()
            response = client.get('/api')
            self.assertEqual(response.status_code, 200)

    def test_post_user(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.session.remove()
                db.drop_all()
                db.create_all()
                card1.update({"password_hash": set_password(card1['password'])})
                user = UserSchema().make_instance(card1, partial=False)
                db.session.add(user)
                db.session.commit()
                response = client.get('/api/users/1', headers=dict(Authorization=f"{authent}"))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["email"], card1["email"])
                db.session.remove()


class TestGateCardResourse(unittest.TestCase):

    @patch('requests.get')
    def test_forbidden_user_get(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context():
                context.push()
                mock_get.return_value = ''
                resp = GateCardResourse().get(1)
                self.assertEqual(resp.status_code, 401)

    @patch('requests.get')
    def test_user_get_card(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context('/api/users/1/card', headers=dict(Authorization=f"{authent}")):
                context.push()
                db.session.remove()
                db.drop_all()
                db.create_all()
                patient1.update({"password_hash": set_password(card1['password'])})
                user = UserSchema().make_instance(card1, partial=False)
                db.session.add(user)
                db.session.commit()
                mock_get.return_value = make_response(jsonify([patient1]), 200)
                resp = GateCardResourse().get(id=1)
                self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
