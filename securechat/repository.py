from peewee import *
from enum import Enum

import datetime
import os

from ._const import SERVER_DATA, DB_SERVER, DB_CLIENT, CLIENT_DATA

class DatabaseSourceType(Enum):
    server = "Server"
    client = "Client"

def create_database(source:DatabaseSourceType)->SqliteDatabase:
    assert source is not None
    match source :
        case DatabaseSourceType.server:
            dir = SERVER_DATA
            db_file = DB_SERVER
        case DatabaseSourceType.client:
            dir = CLIENT_DATA
            db_file = DB_CLIENT
    if not os.path.exists(dir):
        os.makedirs(dir)
    try:
        db = SqliteDatabase(db_file)
        return db
    except Exception as e : raise e

DB_SERVER_CONNECTION:SqliteDatabase = create_database(DatabaseSourceType.server)
DB_CLIENT_CONNECTION:SqliteDatabase = create_database(DatabaseSourceType.client)


class ServerBaseModel(Model):
    class Meta:
        database = DB_SERVER_CONNECTION

class User(ServerBaseModel):
    username = CharField(unique=True)

class Tweet(ServerBaseModel):
    user = ForeignKeyField(User, backref='tweets')
    message = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    
def create_server_table():
    DB_SERVER_CONNECTION.connect()
    DB_SERVER_CONNECTION.create_tables([
        User
    ])
    DB_SERVER_CONNECTION.close()

def init_db()->SqliteDatabase:
    create_server_table()
    return DB_SERVER_CONNECTION