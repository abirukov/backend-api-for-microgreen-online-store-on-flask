from flask import jsonify, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from werkzeug.security import generate_password_hash

from beaver_app.blueprints.user.models.token_blocklist import TokenBlocklist
from beaver_app.blueprints.user.models.user import User
from beaver_app.blueprints.user.schemas import UserSchema, UsersGetListFilterSchema,\
    UsersListResponseSchema, UserLoginSchema
from beaver_app.blueprints.user.utils import generate_personal_code, is_current_user
from beaver_app.blueprints.utils import response_unique_fields_error
from beaver_app.db.db_utils import save, get_list, get_by_id, update, safe_delete,\
    check_entity_by_unique_fields

from flask_smorest import Blueprint

from beaver_app.enums import Entities

user_blueprint = Blueprint('users', 'users', url_prefix='/users')


@user_blueprint.route('/', methods=['GET', 'POST'])
class UsersView(MethodView):
    @user_blueprint.response(200, UsersListResponseSchema)
    @user_blueprint.arguments(UsersGetListFilterSchema, location='query')
    @jwt_required()
    def get(self, args):
        if User.is_admin_by_id(get_jwt_identity()):
            return get_list(
                Entities.USER,
                q_filter=args,
            )
        return abort(403)

    @user_blueprint.arguments(UserSchema, location='json')
    @user_blueprint.response(201, UserSchema)
    @jwt_required()
    def post(self, user_data):
        if not User.is_admin_by_id(get_jwt_identity()):
            abort(403)
        unique_attrs = ['phone', 'email', 'tg_id']
        error_attrs = check_entity_by_unique_fields(Entities.USER, unique_attrs, user_data)
        if error_attrs:
            return response_unique_fields_error(error_attrs)
        return save(
            User(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                middle_name=user_data.middle_name,
                phone=user_data.phone,
                email=user_data.email,
                password=generate_password_hash(user_data.password),
                tg_id=user_data.tg_id,
                tg_username=user_data.tg_username,
                personal_code=generate_personal_code(),
                inviter_id=user_data.inviter_id,
            ),
        )


@user_blueprint.route('/<user_id>', methods=['GET', 'PUT', 'DELETE'])
class UserView(MethodView):
    @user_blueprint.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        user = get_by_id(Entities.USER, user_id)
        if user is None:
            abort(404)
        if User.is_admin_by_id(get_jwt_identity()) or is_current_user(get_jwt_identity(), user.id):
            return user
        return abort(403)

    @user_blueprint.arguments(UserSchema, location='json')
    @user_blueprint.response(201, UserSchema)
    @jwt_required()
    def put(self, user_data, user_id):
        user = get_by_id(Entities.USER, user_id)
        if user is None:
            abort(404)
        if User.is_admin_by_id(get_jwt_identity()) or is_current_user(get_jwt_identity(), user.id):
            user.first_name = user_data.first_name
            user.last_name = user_data.last_name
            user.middle_name = user_data.middle_name
            user.phone = user_data.phone
            user.email = user_data.email
            user.password = user_data.password
            update(user)
            return user
        return abort(403)

    @jwt_required()
    def delete(self, user_id):
        user = get_by_id(Entities.USER, user_id)
        if user is None:
            abort(404)
        if User.is_admin_by_id(get_jwt_identity()):
            safe_delete(Entities.USER, user_id)
            return {}
        return abort(403)


@user_blueprint.route('/register', methods=['POST'])
class UserRegisterView(MethodView):
    @user_blueprint.arguments(UserSchema, location='json')
    @user_blueprint.response(201)
    def post(self, register_data):
        error_attrs = check_entity_by_unique_fields(Entities.USER, User.get_uniq_fields(), register_data)
        if error_attrs:
            return response_unique_fields_error(error_attrs)
        user = save(
            User(
                first_name=register_data.first_name,
                last_name=register_data.last_name,
                middle_name=register_data.middle_name,
                phone=register_data.phone,
                email=register_data.email,
                password=generate_password_hash(register_data.password),
                tg_id=register_data.tg_id,
                tg_username=register_data.tg_username,
                personal_code=generate_personal_code(),
                inviter_id=register_data.inviter_id,
            ),
        )
        return jsonify(access_token=user.create_token())


@user_blueprint.route('/login', methods=['POST'])
class UserLoginView(MethodView):
    @user_blueprint.arguments(UserLoginSchema, location='json')
    @user_blueprint.response(200)
    def post(self, login_data):
        user = User.authenticate_by_mail(login_data['email'], login_data['password'])
        if user is not None:
            return jsonify(access_token=user.create_token())
        return abort(400)


@user_blueprint.route('/logout', methods=['DELETE'])
class UserLogoutView(MethodView):
    @user_blueprint.response(200)
    @jwt_required()
    def delete(self):
        token = get_jwt()
        save(TokenBlocklist(jti=token['jti'], type=token['type'], user_id=get_jwt_identity()))
        return jsonify(msg=f'{token["type"].capitalize()} token successfully revoked')
