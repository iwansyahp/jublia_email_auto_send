from flask import request
from flask_restful import Resource

from jublia_email_autosend.models import Email
from jublia_email_autosend.extensions import ma, db
from jublia_email_autosend.commons.pagination import paginate


class EmailSchema(ma.ModelSchema):

    id = ma.Int(dump_only=True)
    
    class Meta:
        model = Email
        sqla_session = db.session

class EmailResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: event_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  email: EmailSchema
        404:
          description: email does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: event_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              EmailSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: email updated
                  email: EmailSchema
        404:
          description: email does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: event_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: email deleted
        404:
          description: email does not exists
    """

    def get(self, event_id):
        schema = EmailSchema()
        email = Email.query.filter_by(event_id=event_id).first_or_404()
        return {"email": schema.dump(email).data}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user, errors = schema.load(request.json, instance=user)
        if errors:
            return errors, 422

        db.session.commit()

        return {"msg": "email updated", "email": schema.dump(user).data}

    def delete(self, event_id):
        email = Email.query.filter_by(event_id=event_id).first_or_404()
        db.session.delete(email)
        db.session.commit()

        return {"msg": "email deleted"}


class EmailList(Resource):
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
                          $ref: '#/components/schemas/UserSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              UserSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: user created
                  user: UserSchema
    """
    method_decorators = [jwt_required]

    def get(self):
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

    def post(self):
        schema = UserSchema()
        user, errors = schema.load(request.json)
        if errors:
            return errors, 422

        db.session.add(user)
        db.session.commit()

        return {"msg": "user created", "user": schema.dump(user).data}, 201
