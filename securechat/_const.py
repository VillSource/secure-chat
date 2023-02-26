import os

MODULE_NAME = "securechat"

SERVER_DATA = f"{os.path.expanduser('~')}/.securechat/server"
CLIENT_DATA = f"{os.path.expanduser('~')}/.securechat/client"
DB_SERVER = f"{SERVER_DATA}/sql.db"
DB_CLIENT = f"{CLIENT_DATA}/sql.db"
