from flask_smorest import Blueprint

from flask import abort
from flask.views import MethodView

from beaver_app.blueprints.category.schemas import CategorySchema, CategoryListResponseSchema, \
    CategoryGetListFilterSchema
from beaver_app.blueprints.category.models.category import Category
from beaver_app.db.db_utils import save, update, get_by_id, safe_delete, get_list
from beaver_app.enums import Entities

category_blueprint = Blueprint('categories', 'categories', url_prefix='/categories')


@category_blueprint.route('/', methods=['GET', 'POST'])
class CategoriesView(MethodView):
    @category_blueprint.response(200, CategoryListResponseSchema)
    @category_blueprint.arguments(CategoryGetListFilterSchema, location='query')
    def get(self, args):
        return get_list(Entities.CATEGORY, args)

    @category_blueprint.arguments(CategorySchema, location='json')
    @category_blueprint.response(201, CategorySchema)
    def post(self, category_data):
        category = save(Category(title=category_data.title))
        return category


@category_blueprint.route('/<category_id>', methods=['GET', 'PUT', 'DELETE'])
class CategoryView(MethodView):
    @category_blueprint.response(200, CategorySchema)
    def get(self, category_id):
        category = get_by_id(Entities.CATEGORY, category_id)
        if category is None:
            abort(404)
        return category

    @category_blueprint.arguments(CategorySchema, location='json')
    @category_blueprint.response(201, CategorySchema)
    def put(self, category_data, category_id):
        category = get_by_id(Entities.CATEGORY, category_id)
        if category is None:
            abort(404)
        category.title = category_data.title
        update(category)
        return category

    def delete(self, category_id):
        category = get_by_id(Entities.CATEGORY, category_id)
        if category is None:
            abort(404)
        safe_delete(Entities.CATEGORY, category_id)
        return {}
