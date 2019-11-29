from flask import request, jsonify
from flask_restful import Resource
import requests

from services.gateway import app
from services.cards.config import DevConfig as cards_config
from services.doctors.config import DevConfig as doc_config
from services.schedule.config import DevConfig as appoint_config


class GateCardResourse(Resource):

    def get(self, user_id):
        app.logger.info(f'Получен запрос на информацию о карте пользователя id = {user_id}')
        card = requests.get(cards_config.CARDS_SERVER_NAME + '/cards/' + str(user_id)).json()
        return card

    def post(self):
        app.logger.info(f'Получен запрос на создание новой карты пользователя')
        data = request.get_json() or {}
        response = requests.post(cards_config.CARDS_SERVER_NAME + '/cards', data=data)
        return response.json(), response.status_code

    def put(self, user_id):
        app.logger.info(f'Получен запрос на редактирование карты пользователя id = {user_id}')
        data = request.form or request.get_json() or {}

        app.logger.info(f'Отправлен запрос на редактирование карты пользователя id = {user_id}')
        updated = requests.put(cards_config.CARDS_SERVER_NAME + '/cards/' + str(user_id), data=data)

        app.logger.info(f'Получен запрос на информацию о карте пользователя id = {user_id}')
        user_data = requests.get(cards_config.CARDS_SERVER_NAME + '/cards/' + str(user_id))

        if user_data.status_code < 500:
            user_data = user_data.json()

            a = '-'.join(list(map(str, [user_data["dd"], user_data["mm"], user_data["yy"]])))
            b = ' '.join(list(map(str, [user_data["name"], user_data["surname"], user_data["sex"]])))

            us_data = ' '.join([b, a])
            app.logger.info(f'Отправлен запрос на информацию о записях пользователя id = {user_id}')
            sched = requests.get(appoint_config.APPOINT_SERVER_NAME + '/schedule', data={"user_id": user_id})
            if sched.status_code < 500:
                if sched.json():
                    for sch in sched.json():
                        app.logger.info(
                            f'Отправлен редактирование информации о записи {sch["id"]} пользователя id = {user_id}')
                        update = requests.put(appoint_config.APPOINT_SERVER_NAME + '/schedule/' + str(sch["id"]),
                                              data={"user_data": us_data})
            return user_data, updated.status_code
        return user_data.json(), updated.status_code


class GateDocsResourse(Resource):

    def get(self):
        app.logger.info(f'Отправлен запрос на информацию о доступных специалистах')
        doctors = requests.get(doc_config.DOC_SERVER_NAME + '/doctors').json()
        return doctors


class GateScheduleResourse(Resource):

    def get(self):
        app.logger.info(f'Отправлен запрос на информацию о записях')
        data = request.form or request.get_json() or {}
        sched = requests.get(appoint_config.APPOINT_SERVER_NAME + '/schedule').json()
        if "id_card" not in data:
            app.logger.info(f'Отправлен запрос на информацию о всех записях пользователя с id = {data["user_id"]}')
            doctors = requests.get(doc_config.DOC_SERVER_NAME + '/doctors')
            selected = [sch["id_card"] for sch in sched if sch["user_id"] == int(data["user_id"])]
            if selected:
                if doctors.status_code < 500:
                    selected_docs = [doc for doc in doctors.json() if doc["id_card"] in selected]
                    return selected_docs
            return jsonify({"message": "You have not any appointments."})
        else:
            app.logger.info(
                f'Отправлен запрос на информацию о записи пользователя с id = {data["user_id"]} к специалисту с id_card = {data["id_card"]}')
            selected = [sch for sch in sched if
                        (sch["id_card"] == int(data["id_card"]) and (sch["user_id"] == int(data["user_id"])))]
            if selected:
                doctor = requests.get(doc_config.DOC_SERVER_NAME + '/doctors/' + data["id_card"])
                if doctor.status_code < 500:
                    return doctor.json()
            return jsonify({"message": "No such appointment"})

    def post(self):

        data = request.form or request.get_json() or {}
        app.logger.info(
            f'Получен запрос на создание записи пользователя с id = {data["user_id"]} к специалисту с id_card = {data["id_card"]}')

        card = requests.get(cards_config.CARDS_SERVER_NAME + '/cards/' + data["user_id"])
        app.logger.info(
            f'Отправлен запрос на информацию о карте пользователя с id = {data["user_id"]}')
        doctor = requests.get(doc_config.DOC_SERVER_NAME + '/doctors/' + data["id_card"])
        app.logger.info(
            f'Отправлен запрос на информацию о специалисте с id_card = {data["id_card"]}')
        appoints = requests.get(appoint_config.APPOINT_SERVER_NAME + '/schedule', data).json()
        app.logger.info(
            f'Отправлен запрос на информацию записи пользователя с id = {data["user_id"]} к специалисту с id_card = {data["id_card"]}')

        if card.status_code == 500:
            return jsonify({"message": "Please, create a user card before"})

        user_data = card.json()

        a = '-'.join(list(map(str, [user_data["dd"], user_data["mm"], user_data["yy"]])))
        b = ' '.join(list(map(str, [user_data["name"], user_data["surname"], user_data["sex"]])))

        us_data = ' '.join([b, a])

        data_to_post = {
            "user_id": data["user_id"],
            "id_card": data["id_card"],
            "user_data": us_data
        }

        if not appoints:
            app.logger.info(
                f'Отправлен запрос на создание записи пользователя с id = {data["user_id"]} к специалисту с id_card = {data["id_card"]}')
            makeappointment = requests.post(appoint_config.APPOINT_SERVER_NAME + '/schedule', data=data_to_post)

            return jsonify({"message": "An appointment created",
                            "appointment": data_to_post,
                            "doctor": doctor.json()})
        else:
            apps = [1 for appoint in appoints if (appoint["id_card"] == int(data["id_card"]) and
                                                  (appoint["user_id"] == int(data["user_id"])))]
            if sum(apps) > 0:
                return jsonify({"message": "You already made an appointment",
                                "user_card": card.json(),
                                "doctor": doctor.json()})
            apps = [1 for appoint in appoints if (appoint["id_card"] == int(data["id_card"]))]
            if sum(apps) > 5:
                return jsonify({"message": "Please make an appoitnment with another doctor"})
            app.logger.info(
                f'Отправлен запрос на создание записи пользователя с id = {data["user_id"]} к специалисту с id_card = {data["id_card"]}')
            makeappointment = requests.post(appoint_config.APPOINT_SERVER_NAME + '/schedule', data=data_to_post)

            return jsonify({"message": "An appointment created",
                            "appointment": data_to_post,
                            "doctor": doctor.json()})

    def delete(self):
        data = request.form or request.get_json() or {}
        app.logger.info(
            f'Получен запрос на отмену записи пользователя с id = {data["user_id"]} к специалисту с id_card = {data["id_card"]}')
        appoints = requests.get(appoint_config.APPOINT_SERVER_NAME + '/schedule', data)
        app.logger.info(
            f'Отправлен запрос на информацию о записи пользователя с id = {data["user_id"]} к специалисту с id_card = {data["id_card"]}')

        if appoints.status_code < 500:
            sched_id = [appoint["id"] for appoint in appoints.json() if (appoint["id_card"] == int(data["id_card"]) and
                                                                         (appoint["user_id"] == int(data["user_id"])))]
            if not sched_id:
                return jsonify({"message": "No such appointment"})
            app.logger.info(
                f'Отправлен запрос на удаленение записи пользователя с id = {data["user_id"]} к специалисту с id_card = {data["id_card"]}')
            del_sched = requests.delete(appoint_config.APPOINT_SERVER_NAME + '/schedule/' + str(sched_id[0]))
            if del_sched.status_code == 200:
                return del_sched.status_code
        return jsonify({"message": "Server not allowed"})
