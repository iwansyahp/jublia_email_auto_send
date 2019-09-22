from flask import request
from flask_restful import Resource

from jublia_email_autosend.models import Email, Recipient
from jublia_email_autosend.extensions import ma, db
from jublia_email_autosend.commons.pagination import paginate
from marshmallow import fields
from datetime import datetime
from pytz import timezone

from jublia_email_autosend.tasks.send_email import send_email_task

class EmailSchema(ma.ModelSchema):

    id = ma.Int(dump_only=True)
    timestamp = fields.DateTime(format='%d %b %Y %H:%M') # example: 15 Dec 2015 23:12
    
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

    def put(self, event_id):
        schema = EmailSchema(partial=True)
        email = Email.query.filter_by(event_id=event_id).first_or_404()
        email, errors = schema.load(request.json, instance=email)
        if errors:
            return errors, 422

        db.session.commit()

        return {"msg": "email updated", "email": schema.dump(email).data}

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
                          $ref: '#/components/schemas/EmailSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              EmailSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: email created
                  email: EmailSchema
        400:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: event_id has been registered
    """
  
    def get(self):
        schema = EmailSchema(many=True)
        query = Email.query
        return paginate(query, schema)

    def post(self):
        # make sure that recipients found
        recipient_number = Recipient.query.count()
        if recipient_number == 0:
          return {"msg": "No recipients found in DB"}, 400

        schema = EmailSchema()
        email, errors = schema.load(request.json)
        if errors:
            return errors, 422

        event_id_registered = Email.query.filter_by(event_id=request.json['event_id']).first()
        if event_id_registered:
          return {"msg": "event_id has been registered"}, 400
        else:
          # make sure that timestamp is after now with defined timezone
          singapore_now = datetime.now(timezone("Asia/Singapore"))
          # assume that timestamp that given by user is timezone-d to 'Asia/Singapore (UTC+8) time.
          given_timestamp = datetime.strptime(request.json['timestamp']+"+08:00", '%d %b %Y %H:%M%z')
          if singapore_now > given_timestamp:
            return {"msg": "timestamp must be after email creation time"}, 400
          
          db.session.add(email)
          db.session.commit()
          # get total seconds through given timestamp
          total_seconds  = (given_timestamp - singapore_now).seconds
          print("total_seconds: ", total_seconds)
          print("given timestamp: ", request.json['timestamp'])
          print("timestamp: ", given_timestamp)
          print("singapore-now: ", singapore_now)
          
          # send message asynchronously
          send_email_task.apply_async(countdown=total_seconds, args=[email.event_id])

          return {"msg": "email created", "email": schema.dump(email).data}, 201