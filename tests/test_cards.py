import unittest
from unittest.mock import patch, MagicMock
from flask import jsonify, make_response

from services.cards import app, db, resourses
from services.cards.models import Cards, CardSchema
from services.cards.resourses import CardResourse
from services.cards.config import TestConfig

import json

app.config.from_object(TestConfig)

patient1 = {"id": 1, "name": "Alica", "surname": "Ivanova", "dd": 13, "mm": 10, "yy": 1995, "sex": "f", "user_id": 1}
patient1_update = {"user_id": 1, "dd": 18}
patient2 = {"id": 2, "name": "Alex", "surname": "Sidorov", "dd": 23, "mm": 6, "yy": 1993, "sex": "m", "user_id": 2}


class TestUserService(unittest.TestCase):

    def test_get(self):
        with app.app_context() as context:
            context.push()
            db.session.remove()
            db.drop_all()
            db.create_all()
            self.assertIsNone(Cards.query.get(1))

    def test_exist(self):
        with app.app_context() as context:
            context.push()
            db.session.remove()
            db.drop_all()
            db.create_all()
            card = CardSchema().make_instance(patient1, partial=False)
            db.session.add(card)
            db.session.commit()
            exist = Cards.query.get(patient1["id"])
            self.assertEqual(card.id, exist.id)

    def test_get_user_card(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.session.remove()
                db.drop_all()
                db.create_all()
                card = CardSchema().make_instance(patient1, partial=False)
                db.session.add(card)
                db.session.commit()
                response = client.get('/cards/1')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["surname"], patient1["surname"])

    def test_update_user_card(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.session.remove()
                db.drop_all()
                db.create_all()
                card = CardSchema().make_instance(patient1, partial=False)
                db.session.add(card)
                db.session.commit()
                response = client.put('/cards/1', data=patient1_update)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["dd"], 18)

    def test_post_user_card(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.session.remove()
                db.drop_all()
                db.create_all()
                response = client.post('/cards', data=patient1)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["user_id"], 1)

    @patch.object(CardResourse, 'get')
    def test_get_card(self, mock_get):
        with app.app_context() as context:
            with app.test_client():
                context.push()
                mock_get.return_value = make_response(jsonify(patient1, 200))
                resp = CardResourse.get(1)
                mock_get.assert_called_with(1)
                self.assertEqual(resp.json[0]["user_id"], 1)
                self.assertEqual(resp.status_code, 200)

    @patch.object(CardResourse, 'post')
    def test_post_card(self, mock_post):
        with app.app_context() as context:
            with app.test_client():
                context.push()
                mock_post.return_value = make_response(jsonify(patient1, 200))
                resp = CardResourse.post()
                mock_post.assert_called_with()
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.json[0]["user_id"], 1)

    @patch.object(CardResourse, 'put')
    def test_put_card(self, mock_put):
        with app.app_context() as context:
            with app.test_client():
                context.push()
                mock_put.args = patient1_update
                patient1["dd"] = 18
                mock_put.return_value = make_response(jsonify(patient1), 200)
                resp = CardResourse.put(1)
                mock_put.assert_called_with(1)
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.json["user_id"], 1)


if __name__ == '__main__':
    unittest.main()
