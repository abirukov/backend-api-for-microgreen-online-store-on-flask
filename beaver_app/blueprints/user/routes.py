import sqlalchemy
from flask import jsonify, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from beaver_app.blueprints.user.models.token_blocklist import TokenBlocklist
from beaver_app.blueprints.user.models.user import User
from beaver_app.blueprints.user.schemas import UserSchema
from beaver_app.db.db import db_session
from beaver_app.db.db_utils import save, get_list, get_by_id, update, safe_delete

from flask_smorest import Blueprint

from beaver_app.enums import Entities

user_blueprint = Blueprint('users', 'users', url_prefix='/users')


@user_blueprint.route('/', methods=['GET', 'POST'])
class UsersView(MethodView):
    @user_blueprint.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):

        if User.is_admin_by_id(get_jwt_identity()):
            return get_list(Entities.USER)
        return abort(403)

    @user_blueprint.arguments(UserSchema, location='json')
    @user_blueprint.response(201, UserSchema)
    def post(self, user_data):
        user = save(
            User(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                middle_name=user_data.middle_name,
                phone=user_data.phone,
                email=user_data.email,
                password=user_data.password,
            ),
        )
        return user


@user_blueprint.route('/<user_id>', methods=['GET', 'PUT', 'DELETE'])
class UserView(MethodView):
    @user_blueprint.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        user = get_by_id(Entities.USER, user_id)
        if user is None:
            abort(404)
        if User.is_admin_by_id(get_jwt_identity()) or User.is_current_user(get_jwt_identity(), user.id):
            return user
        return abort(403)

    @user_blueprint.arguments(UserSchema, location='json')
    @user_blueprint.response(201, UserSchema)
    @jwt_required()
    def put(self, user_data, user_id):
        user = get_by_id(Entities.USER, user_id)
        if user is None:
            abort(404)
        if User.is_admin_by_id(get_jwt_identity()) or User.is_current_user(get_jwt_identity(), user.id):
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
    @user_blueprint.response(201, UserSchema)
    def post(self, register_data):
        try:
            user = save(register_data)
        except sqlalchemy.exc.IntegrityError:
            db_session.rollback()
            return abort(400)
        return jsonify(access_token=user.get_token())


@user_blueprint.route('/login', methods=['POST'])
class UserLoginView(MethodView):
    @user_blueprint.arguments(UserSchema, location='json')
    @user_blueprint.response(200, UserSchema)
    def post(self, login_data):
        user = User.authenticate_by_mail(login_data.email, login_data.password)
        if user is not None:
            return jsonify(access_token=user.get_token())
        return abort(400)


@user_blueprint.route('/logout', methods=['DELETE'])
class UserLogoutView(MethodView):
    @user_blueprint.response(200)
    @jwt_required()
    def delete(self):
        token = get_jwt()
        save(TokenBlocklist(jti=token['jti'], type=token['type'], user_id=get_jwt_identity()))
        return jsonify(msg=f'{token["type"].capitalize()} token successfully revoked')