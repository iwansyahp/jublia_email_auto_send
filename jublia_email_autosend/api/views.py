from flask import Blueprint, current_app
from flask_restful import Api

from jublia_email_autosend.extensions import apispec
from jublia_email_autosend.api.resources import EmailResource, EmailList, RecipientResource, RecipientList
from jublia_email_autosend.api.resources.email import EmailSchema
from jublia_email_autosend.api.resources.recipient import RecipientSchema


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(EmailResource, '/emails/<int:event_id>')
api.add_resource(EmailList, '/emails')
api.add_resource(RecipientResource, '/recipients/<string:email>')
api.add_resource(RecipientList, '/recipients')

@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("EmailSchema", schema=EmailSchema)
    apispec.spec.path(view=EmailResource, app=current_app)
    apispec.spec.path(view=EmailList, app=current_app)

    apispec.spec.components.schema("RecipientSchema", schema=RecipientSchema)
    apispec.spec.path(view=RecipientResource, app=current_app)
    apispec.spec.path(view=RecipientList, app=current_app)
