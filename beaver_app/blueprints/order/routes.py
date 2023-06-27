from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from beaver_app.blueprints.order.schemas import OrdersListResponseSchema, OrdersGetListFilterSchema
from beaver_app.blueprints.user.models import User
from beaver_app.db.db_utils import get_list
from beaver_app.enums import Entities

order_blueprint = Blueprint('orders', 'orders', url_prefix='/orders')


@order_blueprint.route('/', methods=['GET'])
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
