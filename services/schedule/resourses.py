from flask import request, abort, g
from flask_restful import Resource, reqparse
from services.schedule.models import Schedules, SchedulesSchema
from services.schedule import db, app


class ScheduleResourse(Resource):

    def get(self, id):
        app.logger.info(f'Получен запрос на информацию о записи с id = {id}')
        return SchedulesSchema().dump(Schedules.query.get_or_404(id))

    def post(self):
        data = request.form or request.get_json() or {}
        if "id_card" not in data:
            return 'must include id_card field!'
        app.logger.info(f'Получен запрос на создание записи к специалисту id = {data["id_card"]}')
        sched = SchedulesResourse().get()
        count = 0
        app.logger.info(f'Подсчет записей к специалисту id = {data["id_card"]}')
        for sh in sched:
            if sh["id_card"] == int(data["id_card"]):
                count += 1
            if sh["id_card"] == int(data["id_card"]) & sh["user_id"] == int(data["user_id"]):
                return {"message": "you already scheduled!"}, sh

        if count > 5:
            return {"message": "There is no free time. Please, make an appointment with another doctor"}
        appoint = SchedulesSchema().make_instance(data, partial=True)
        db.session.add(appoint)
        db.session.commit()
        return SchedulesSchema().dump(Schedules.query.get_or_404(appoint.id))

    def delete(self, id):
        app.logger.info(f'Получен запрос на отмену записи к специалисту id = {id}')
        appoint = Schedules.query.get(id)
        db.session.delete(appoint)
        db.session.commit()
        return {"message": f"Appointment with {id} was delete"}


class SchedulesResourse(Resource):

    def get(self):
        app.logger.info(f'Получен запрос на информацию о всех записях')
        return SchedulesSchema(many=True).dump(Schedules.query.all())
