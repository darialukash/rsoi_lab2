import unittest
from unittest.mock import patch, Mock
from flask import make_response, jsonify

from services.gateway import app
from services.gateway.resourses import GateCardResourse, GateDocsResourse, GateScheduleResourse
from services.gateway.config import TestConfig

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


class TestGateCardResourse(unittest.TestCase):

    @patch('requests.get')
    def test_get_card(self, mock_get):
        with app.app_context() as context:
            with app.test_client():
                context.push()
                mock_get.return_value = make_response(jsonify(patient1), 200)
                resp = GateCardResourse().get(user_id=1)
                self.assertEqual(resp.json["user_id"], 1)
                self.assertEqual(resp.status_code, 200)

    @patch('requests.post')
    def test_post_card(self, mock_post):
        with app.app_context() as context:
            with app.test_request_context(data=patient1):
                context.push()
                mock_post.return_value = make_response(jsonify(patient1), 200)
                resp = GateCardResourse().post()
                self.assertEqual(resp.json["user_id"], 1)
                self.assertEqual(resp.status_code, 200)

    @patch('requests.put')
    @patch('requests.get')
    def test_put_card(self, mock_get, mock_put):
        with app.app_context() as context:
            with app.test_request_context(data=patient1):
                context.push()
                mock_put.return_value = make_response(jsonify(patient1), 200)
                mock_get.return_value = make_response(jsonify([]), 200)
                resp = GateCardResourse().put(1)
                self.assertEqual(resp.json["user_id"], 1)
                self.assertEqual(resp.status_code, 200)

    @patch('requests.put')
    @patch('requests.get')
    def test_put_card_schedule_update(self, mock_get, mock_put_card):
        with app.app_context() as context:
            with app.test_request_context(data=patient1):
                context.push()
                mock_put_card.return_value = make_response(jsonify(patient1), 200)
                mock_get.return_value = make_response(jsonify(appoint1), 200)
                resp = GateCardResourse().put(1)
                self.assertEqual(resp.json["user_id"], 1)
                self.assertEqual(resp.status_code, 200)


class TestGateDocsResourse(unittest.TestCase):

    @patch('requests.get')
    def test_get_doc(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context():
                context.push()
                mock_get.return_value = make_response(jsonify([doctor1, doctor2]), 200)
                resp = GateDocsResourse().get()
                self.assertEqual(len(resp.json), 2)
                self.assertEqual(resp.status_code, 200)


class TestGateScheduleResourse(unittest.TestCase):

    @patch('requests.get')
    def test_get_schedule(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context(data={"user_id": 1}):
                context.push()
                fake_responses = [make_response(jsonify([appoint1, appoint2, appoint3, appoint4, appoint6]), 200),
                                  make_response(jsonify([doctor1, doctor1, doctor3, doctor4]), 200)]
                mock_get.side_effect = fake_responses
                resp = GateScheduleResourse().get()
                self.assertEqual(len(resp), 4)

    @patch('requests.get')
    def test_get_no_schedule(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context(data={"user_id": 2}):
                context.push()
                fake_responses = [make_response(jsonify([]), 200)]
                mock_get.side_effect = fake_responses
                resp = GateScheduleResourse().get()
                self.assertEqual(resp.json, {"message": "You have not any appointments."})

    @patch('requests.get')
    def test_get_schedule_doc(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context(data={"user_id": 1, "id_card": 1000}):
                context.push()
                fake_responses = [make_response(jsonify([appoint1, appoint2, appoint3, appoint4, appoint6]), 200),
                                  make_response(jsonify([doctor1]), 200)]
                mock_get.side_effect = fake_responses
                resp = GateScheduleResourse().get()
                self.assertEqual(len(resp), 1)

    @patch('requests.get')
    def test_get_no_schedule_doc(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context(data={"user_id": 1, "id_card": 1000}):
                context.push()
                fake_responses = [make_response(jsonify([]), 200)]
                mock_get.side_effect = fake_responses
                resp = GateScheduleResourse().get()
                self.assertEqual(resp.json, {"message": "No such appointment"})

    @patch('requests.post')
    @patch('requests.get')
    def test_post_schedule(self, mock_get, mock_post):
        with app.app_context() as context:
            with app.test_request_context(data={"user_id": 2, "id_card": 4000}):
                context.push()
                fake_responses = [make_response(jsonify(patient2), 200),
                                  make_response(jsonify(doctor4), 200),
                                  make_response(jsonify([]), 200)]
                mock_get.side_effect = fake_responses
                mock_post.return_value = make_response(jsonify([appoint6]), 200)
                resp = GateScheduleResourse().post()
                self.assertEqual(resp.get_json()["appointment"], body_sched["appointment"])
                self.assertEqual(resp.status_code, 200)

    @patch('requests.get')
    def test_post_no_schedule(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context(data={"user_id": 3, "id_card": 4000}):
                context.push()
                fake_responses = [make_response(jsonify(patient3), 200),
                                  make_response(jsonify(doctor4), 200),
                                  make_response(jsonify([appoint6, appoint4]), 200)]
                mock_get.side_effect = fake_responses
                resp = GateScheduleResourse().post()
                self.assertEqual(resp.get_json(), {"message": "Please make an appoitnment with another doctor"})
                self.assertEqual(resp.status_code, 200)

    @patch('requests.get')
    def test_post_made_schedule(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context(data={"user_id": 2, "id_card": 4000}):
                context.push()
                fake_responses = [make_response(jsonify(patient2), 200),
                                  make_response(jsonify(doctor4), 200),
                                  make_response(jsonify([appoint6]), 200)]
                mock_get.side_effect = fake_responses
                resp = GateScheduleResourse().post()
                self.assertEqual(resp.get_json()["message"], "You already made an appointment")
                self.assertEqual(resp.status_code, 200)

    @patch('requests.get')
    def test_post_no_usercard(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context(data={"user_id": 3, "id_card": 4000}):
                context.push()
                fake_responses = [make_response(jsonify([]), 200),
                                  make_response(jsonify(doctor4), 200),
                                  make_response(jsonify([appoint6, appoint4]), 200)]
                mock_get.side_effect = fake_responses
                resp = GateScheduleResourse().post()
                self.assertEqual(resp.get_json(), {"message": "Please, create a user card before"})
                self.assertEqual(resp.status_code, 200)

    @patch('requests.delete')
    @patch('requests.get')
    def test_del_schedule(self, mock_get, mock_del):
        with app.app_context() as context:
            with app.test_request_context(data={"user_id": 2, "id_card": 4000}):
                context.push()
                fake_responses = [make_response(jsonify([appoint6]), 200)]
                mock_get.side_effect = fake_responses
                mock_del.return_value = make_response(jsonify([]), 200)
                resp = GateScheduleResourse().delete()
                self.assertEqual(resp, 200)

    @patch('requests.get')
    def test_del_no_schedule(self, mock_get):
        with app.app_context() as context:
            with app.test_request_context(data={"user_id": 2, "id_card": 4000}):
                context.push()
                fake_responses = [make_response(jsonify([]), 200)]
                mock_get.side_effect = fake_responses
                resp = GateScheduleResourse().delete()
                self.assertEqual(resp.get_json()["message"], "No such appointment")


if __name__ == '__main__':
    unittest.main()
