from flask import abort
from flask.views import MethodView

from beaver_app.blueprints.product.schemas import ProductSchema, ProductsGetListFilterSchema, ProductsListResponseSchema
from beaver_app.blueprints.product.models.product import Product
from beaver_app.db.db_utils import save, update, get_by_id, safe_delete, get_list
from beaver_app.enums import Entities

from flask_smorest import Blueprint

product_blueprint = Blueprint('products', 'products', url_prefix='/products')


@product_blueprint.route('/', methods=['GET', 'POST'])
class ProductsView(MethodView):
    @product_blueprint.response(200, ProductsListResponseSchema)
    @product_blueprint.arguments(ProductsGetListFilterSchema, location='query')
    def get(self, args):
        return get_list(Entities.PRODUCT, args)

    @product_blueprint.arguments(ProductSchema, location='json')
    @product_blueprint.response(201, ProductSchema)
    def post(self, product_data):
        product = save(
            Product(
                title=product_data.title,
                price=product_data.price,
                description=product_data.description,
                category_id=product_data.category_id,
            ),
        )
        return product


@product_blueprint.route('/<product_id>', methods=['GET', 'PUT', 'DELETE'])
class ProductView(MethodView):
    @product_blueprint.response(200, ProductSchema)
    def get(self, product_id):
        product = get_by_id(Entities.PRODUCT, product_id)
        if product is None:
            abort(404)
        return product

    @product_blueprint.arguments(ProductSchema, location='json')
    @product_blueprint.response(201, ProductSchema)
    def put(self, product_data, product_id):
        product = get_by_id(Entities.PRODUCT, product_id)
        if product is None:
            abort(404)
        product.title = product_data.title
        product.price = product_data.price
        product.description = product_data.description
        product.category_id = product_data.category_id
        update(product)
        return product

    def delete(self, product_id):
        product = get_by_id(Entities.PRODUCT, product_id)
        if product is None:
            abort(404)
        safe_delete(Entities.PRODUCT, product_id)
        return {}
