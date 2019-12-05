from flask import request, abort, g
from flask_restful import Resource, reqparse
from services.doctors.models import Doctors, DoctorSchema
from services.doctors import db, app


class DoctorResourse(Resource):

    def get(self, id_card):
        app.logger.info(f'Получен запрос на информацию о специалисте с id = {id_card}')
        return DoctorSchema().dump(Doctors.query.filter_by(id_card=id_card).first())

    def post(self):
        data = request.form or request.get_json() or {}
        if "id_card" not in data:
            return 'must include id_card field!'
        app.logger.info(f'Получен запрос на добавление специалиста с id = {data["id_card"]}')
        doc = DoctorSchema().make_instance(data, partial=True)
        db.session.add(doc)
        db.session.commit()
        return DoctorSchema().dump(Doctors.query.get_or_404(doc.id))

    def put(self, id_card):
        app.logger.info(f'Получен запрос на редактирование информации о специалисте с id = {id_card}')
        data = request.form or request.get_json() or {}
        DoctorSchema().load(data, instance=Doctors.query.filter_by(id_card=id_card).first(), partial=True)
        db.session.commit()
        return DoctorSchema().dump(Doctors.query.filter_by(id_card=id_card).first())



class DoctorsResourse(Resource):

    def get(self):
        app.logger.info(f'Получен запрос на информацию о всех доступных специалистах')
        return DoctorSchema(many=True).dump(Doctors.query.all())
