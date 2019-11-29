from flask import request
from flask_restful import Resource
from services.cards.models import Cards, CardSchema
from services.cards import db, app


class CardResourse(Resource):

    def get(self, id):
        app.logger.info(f'Получен запрос на информацию о карте пациента с id = {id}')
        return CardSchema().dump(Cards.query.get_or_404(id))

    def post(self):
        data = request.form or request.get_json() or {}
        if "user_id" not in data:
            return 'must include user_id field!'
        app.logger.info(f'Получен запрос на создание карты пациента с id = {data["user_id"]}')
        card = CardSchema().make_instance(data, partial=True)
        db.session.add(card)
        db.session.commit()
        return CardSchema().dump(Cards.query.get_or_404(card.id))

    def put(self, id):
        app.logger.info(f'Получен запрос на редактирование карты пациента с id = {id}')

        data = request.form or request.get_json() or {}

        CardSchema().load(data, instance=Cards.query.get_or_404(id), partial=True)
        db.session.commit()
        return CardSchema().dump(Cards.query.get_or_404(id))
