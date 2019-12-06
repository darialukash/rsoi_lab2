from flask import request, abort, g, jsonify
from flask_restful import Resource, reqparse
import requests

from services.users.models import User, UserSchema, set_password
from services.users import db, app
from services.users.auth import basic_auth, requires_auth

from services.gateway.config import DevConfig as gate_config


class FirstResourse(Resource):

    def get(self):
        msg = """It is the Index page. To continue, please,  use post request with 'email' and 'password' \
        fields to register."""
        return jsonify({"message": msg})

    def post(self):
        data = request.get_json() or {}
        if 'email' not in data or 'password' not in data:
            return 'must include email and password fields!'
        if User.query.filter_by(email=data['email']).first():
            return 'use different email!'
        data.update({"password_hash": set_password(data['password'])})
        user = UserSchema().make_instance(data, partial=False)
        app.logger.info(f'Получен запрос на регистрацию нового пациента с id = {user.id}')
        db.session.add(user)
        db.session.commit()
        return UserSchema().dump(user)


class UserResourse(Resource):

    @basic_auth.login_required
    @requires_auth
    def get(self, id):
        app.logger.info(f'Получен запрос на информацию о регистрационных данных пациента с id = {id}')
        if g.current_user.id != id:
            abort(403)
        return UserSchema().dump(User.query.get_or_404(id))

    @basic_auth.login_required
    @requires_auth
    def put(self, id):
        app.logger.info(f'Получен запрос на редактирование регистрационных данных пациента с id = {id}')
        if g.current_user.id != id:
            abort(403)
        data = request.get_json() or {}
        user = UserSchema().load(data, instance=User.query.get_or_404(id), partial=True)
        db.session.commit()
        return UserSchema().dump(user)


class GateCardResourse(Resource):

    @basic_auth.login_required
    @requires_auth
    def get(self, id):
        app.logger.info(f'Получен запрос на информацию о карте  пациента с id = {id}')
        card = requests.get(gate_config.GATE_SERVER_NAME + '/cards/' + str(id))
        return card

    @basic_auth.login_required
    @requires_auth
    def post(self):
        app.logger.info(f'Получен запрос на создание карты пациента с id = {id}')
        data = request.get_json() or {}
        response = requests.post(gate_config.GATE_SERVER_NAME + '/cards', data=data)
        return response  # data, response.status_code

    @basic_auth.login_required
    @requires_auth
    def put(self, id):
        app.logger.info(f'Получен запрос на редактирование карты пациента с id = {id}')
        data = request.get_json() or {}
        updated = requests.put(gate_config.GATE_SERVER_NAME + '/cards/' + str(id), data=data)
        return data, updated.status_code


class GateDocsResourse(Resource):

    def get(self):
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 1, type=int)
        app.logger.info(f'Получен запрос на информацию о специалистах')
        docs = requests.get(gate_config.GATE_SERVER_NAME + '/doctors')
        return docs.json().paginate(page=page, size=size)


class GateAddtoDocResourse(Resource):

    @basic_auth.login_required
    @requires_auth
    def get(self, id, id_card):
        app.logger.info(f'Получен запрос на информацию записи пациента с id = {id} к специалисту с {id_card}')
        data = {"user_id": id, "id_card": id_card}
        docs = requests.get(gate_config.GATE_SERVER_NAME + '/schedule', data=data)
        if docs.status_code < 500:
            return docs.json()
        return docs.status_code

    @basic_auth.login_required
    @requires_auth
    def post(self, id, id_card):
        app.logger.info(f'Получен запрос на запись пациента с id = {id} к специалисту {id_card}')
        data = {"user_id": id, "id_card": id_card}
        update = requests.post(gate_config.GATE_SERVER_NAME + '/schedule', data=data)
        return update.json(), update.status_code

    @basic_auth.login_required
    @requires_auth
    def delete(self, id, id_card):
        app.logger.info(f'Получен запрос на отмену записи пациента с id = {id} к специалисту {id_card}')
        data = {"user_id": id, "id_card": id_card}
        update = requests.delete(gate_config.GATE_SERVER_NAME + '/schedule', data=data)
        return update.json()


class GateUserScheduleResourse(Resource):

    @basic_auth.login_required
    @requires_auth
    def get(self, id):
        app.logger.info(f'Получен запрос на информацию о всех записях пациента с id = {id}')
        data = {"user_id": id}
        docs = requests.get(gate_config.GATE_SERVER_NAME + '/schedule', data=data)
        if docs.status_code < 500:
            return docs.json()
        return {"message": "Can't get to service"}
