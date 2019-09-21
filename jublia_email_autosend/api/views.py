from flask import Blueprint, current_app
from flask_restful import Api

from jublia_email_autosend.extensions import apispec
from jublia_email_autosend.api.resources import UserResource, UserList
from jublia_email_autosend.api.resources.user import UserSchema


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserList, '/users')


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
