from flask import Blueprint, current_app
from flask_restful import Api

from jublia_email_autosend.extensions import apispec
from jublia_email_autosend.api.resources import EmailResource, EmailList
from jublia_email_autosend.api.resources.email import EmailSchema


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(EmailResource, '/emails/<int:event_id>')
api.add_resource(EmailList, '/emails')


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("EmailSchema", schema=EmailSchema)
    apispec.spec.path(view=EmailResource, app=current_app)
    apispec.spec.path(view=EmailList, app=current_app)
