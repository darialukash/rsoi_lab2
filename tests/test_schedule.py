import unittest

from services.schedule import app, db, resourses
from services.schedule.models import Schedules, SchedulesSchema
from services.schedule.resourses import ScheduleResourse, SchedulesResourse
from services.schedule.config import TestConfig

app.config.from_object(TestConfig)

patient1 = {"id": 1, "id_card": 1000, "user_id": 1, "user_data": "Alica Ivannova f 13-10-1995"}
patient2 = {"id": 2, "id_card": 1000, "user_id": 2, "user_data": "Pavel Sidorov m 23-6-1993"}


class TestUserService(unittest.TestCase):

    def test_get(self):
        with app.app_context() as context:
            context.push()
            db.drop_all()
            db.create_all()
            self.assertIsNone(Schedules.query.get(1))

    def test_exist(self):
        with app.app_context() as context:
            context.push()
            db.drop_all()
            db.create_all()
            appoint = SchedulesSchema().make_instance(patient1, partial=False)
            db.session.add(appoint)
            db.session.commit()
            exist = Schedules.query.get(patient1["id"])
            self.assertEqual(appoint.id, exist.id)

    def test_get_appoint(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.drop_all()
                db.create_all()
                appoint = SchedulesSchema().make_instance(patient1, partial=False)
                db.session.add(appoint)
                db.session.commit()
                response = client.get('/schedule/1')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["user_data"], patient1["user_data"])

    def test_update_appoint(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.drop_all()
                db.create_all()
                appoint = SchedulesSchema().make_instance(patient1, partial=False)
                db.session.add(appoint)
                db.session.commit()
                response = client.put('/schedule/1', data=dict(id_card=2000))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["id_card"], 2000)

    def test_post_appoint(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.drop_all()
                db.create_all()
                response = client.post('/schedule', data=patient1)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["user_id"], 1)

    def test_delete_appoint(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.drop_all()
                db.create_all()
                appoint = SchedulesSchema().make_instance(patient1, partial=False)
                db.session.add(appoint)
                db.session.commit()
                response = client.delete('/schedule/1')
                self.assertEqual(response.status_code, 200)
                appoints = Schedules.query.get.all()
                self.assertIsNone(appoints)


if __name__ == '__main__':
    unittest.main()
