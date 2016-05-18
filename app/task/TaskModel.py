import datetime
from app import db_client
__author__ = 'jacobgilsaa'


class Task(db_client.Document):
    userid = db_client.StringField(required=True)
    taskid = db_client.StringField(required=True)
    date = db_client.StringField(default=str(datetime.datetime.now()))
    createdby = db_client.StringField(required=True)
    title = db_client.StringField(required=True)
    description = db_client.StringField()
