import unittest

from services.doctors import app, db, resourses
from services.doctors.models import Doctors, DoctorSchema
from services.doctors.resourses import DoctorsResourse, DoctorResourse
from services.doctors.config import TestConfig
from base64 import b64encode
import json

app.config.from_object(TestConfig)

doctor1 = {"id": 1, "id_card": 1000, "name": "Maria", "surname": "Kot", "specialization": "family medicine"}
doctor1_update = {"specialization": "cardiology"}
doctor2 = {"id": 2, "id_card": 2000, "name": "Pavel", "surname": "Un", "specialization": "allergology"}


class TestDoctorsService(unittest.TestCase):

    def test_get(self):
        with app.app_context() as context:
            context.push()
            db.session.remove()
            db.drop_all()
            db.create_all()
            self.assertIsNone(Doctors.query.get(1))

    def test_exist(self):
        with app.app_context() as context:
            context.push()
            db.session.remove()
            db.drop_all()
            db.create_all()
            doc = DoctorSchema().make_instance(doctor1, partial=False)
            db.session.add(doc)
            db.session.commit()
            exist = Doctors.query.get(doctor1["id"])
            self.assertEqual(doc.id, exist.id)

    def test_get_api(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.session.remove()
                db.drop_all()
                db.create_all()
                doc = DoctorSchema().make_instance(doctor1, partial=False)
                db.session.add(doc)
                doc = DoctorSchema().make_instance(doctor2, partial=False)
                db.session.add(doc)
                db.session.commit()
                response = client.get('/doctors')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.json), 2)

    def test_post_doc(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.session.remove()
                db.drop_all()
                db.create_all()
                response = client.post('/doctors', data=doctor1)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["id_card"], doctor1["id_card"])

    def test_put_doc(self):
        with app.app_context() as context:
            with app.test_client() as client:
                context.push()
                db.session.remove()
                db.drop_all()
                db.create_all()
                doc = DoctorSchema().make_instance(doctor1, partial=False)
                db.session.add(doc)
                db.session.commit()
                response = client.put('/doctors/1000', data=doctor1_update)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["specialization"], doctor1_update["specialization"])


if __name__ == '__main__':
    unittest.main()
