from flask import abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from beaver_app.blueprints.order.models import Order
from beaver_app.blueprints.order.schemas import OrdersListResponseSchema, OrdersGetListFilterSchema, OrderSchema
from beaver_app.blueprints.order.utils import handle_basket
from beaver_app.blueprints.user.models import User
from beaver_app.db.db_utils import get_list, save, get_by_id
from beaver_app.enums import Entities

order_blueprint = Blueprint('orders', 'orders', url_prefix='/orders')


@order_blueprint.route('/', methods=['GET', 'POST'])
class OrdersView(MethodView):
    @order_blueprint.response(200, OrdersListResponseSchema)
    @order_blueprint.arguments(OrdersGetListFilterSchema, location='query')
    @jwt_required()
    def get(self, args):
        if not User.is_admin_by_id(get_jwt_identity()):
            args.user_id = get_jwt_identity()
        return get_list(
            Entities.ORDER,
            q_filter=args,
        )

    @order_blueprint.arguments(OrderSchema, location='json')
    @order_blueprint.response(201, OrderSchema)
    @jwt_required()
    def post(self, order_data):
        user = get_by_id(Entities.USER, get_jwt_identity())
        if user is None or user.basket is None:
            abort(404)
            return
        order = save(Order(
            user_id=user.id,
            status='new',
            address=order_data.address,
            comment=order_data.comment,
        ))
        handle_basket(order, user.basket)

        return order
