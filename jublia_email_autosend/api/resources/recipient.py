from flask import request
from flask_restful import Resource

from jublia_email_autosend.models import Recipient
from jublia_email_autosend.extensions import ma, db
from jublia_email_autosend.commons.pagination import paginate
from marshmallow import fields

class RecipientSchema(ma.ModelSchema):

    id = ma.Int(dump_only=True)
    email = fields.Email()
    
    class Meta:
        model = Recipient
        sqla_session = db.session

class RecipientResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: email
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  recipient: RecipientSchema
        404:
          description: recipient does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: email
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              RecipientSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: recipient updated
                  recipient: RecipientSchema
        404:
          description: recipient does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: email
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: recipient deleted
        404:
          description: recipient does not exists
    """

    def get(self, email):
        schema = RecipientSchema()
        recipient = Recipient.query.filter_by(email=email).first_or_404()
        return {"recipient": schema.dump(recipient).data}

    def put(self, email):
        schema = RecipientSchema(partial=True)
        recipient = Recipient.query.filter_by(email=email).first_or_404()
        recipient, errors = schema.load(request.json, instance=recipient)
        if errors:
            return errors, 422

        db.session.commit()

        return {"msg": "recipient updated", "recipient": schema.dump(recipient).data}

    def delete(self, email):
        recipient = Recipient.query.filter_by(email=email).first_or_404()
        db.session.delete(recipient)
        db.session.commit()

        return {"msg": "recipient deleted"}


class RecipientList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/RecipientSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              RecipientSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: recipient added
                  recipient: RecipientSchema
        400:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: email has been registered
    """
  
    def get(self):
        schema = RecipientSchema(many=True)
        query = Recipient.query
        return paginate(query, schema)

    def post(self):
        schema = RecipientSchema()
        recipient, errors = schema.load(request.json)
        if errors:
            return errors, 422
        # make sure that email is not registered yet
        email_registered = Recipient.query.filter_by(email=request.json['email'])
        if email_registered:
          return {"msg": "email has been registered"}, 400
        else:
          db.session.add(recipient)
          db.session.commit()

          return {"msg": "recipient added", "recipient": schema.dump(recipient).data}, 201
