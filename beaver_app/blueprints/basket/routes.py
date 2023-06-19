from flask import abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from beaver_app.blueprints.basket.classes import BasketUpdate
from beaver_app.blueprints.basket.schemas import BasketSchema, BasketsListResponseSchema, BasketUpdateSchema
from beaver_app.blueprints.schemas import BaseGetListFilterSchema
from beaver_app.blueprints.basket.utils import update_products_in_basket
from beaver_app.blueprints.user.models import User
from beaver_app.db.db_utils import get_list, get_by_id

from flask_smorest import Blueprint

from beaver_app.enums import Entities

basket_blueprint = Blueprint('baskets', 'baskets', url_prefix='/baskets')


@basket_blueprint.route('/list', methods=['GET'])
class BasketsView(MethodView):
    @basket_blueprint.response(200, BasketsListResponseSchema)
    @basket_blueprint.arguments(BaseGetListFilterSchema, location='query')
    @jwt_required()
    def get(self, args):
        if User.is_admin_by_id(get_jwt_identity()):
            return get_list(
                Entities.BASKET,
                q_filter=args,
            )
        return abort(403)


@basket_blueprint.route('/', methods=['GET', 'PUT'])
class BasketView(MethodView):
    @basket_blueprint.response(200, BasketSchema)
    @jwt_required()
    def get(self):
        user = get_by_id(Entities.USER, get_jwt_identity())
        if user.basket is None:
            abort(404)
        return user.basket

    @basket_blueprint.arguments(BasketUpdateSchema, location='json')
    @basket_blueprint.response(201, BasketSchema)
    @jwt_required()
    def put(self, products_data: BasketUpdate):
        user = get_by_id(Entities.USER, get_jwt_identity())
        if user is None or user.basket is None:
            abort(404)
            return
        update_products_in_basket(user.basket, products_data)
        return user.basket
