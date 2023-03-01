import os

MODULE_NAME = "securechat"

SERVER_DATA = f"{os.path.expanduser('~')}/.securechat/server"
CLIENT_DATA = f"{os.path.expanduser('~')}/.securechat/client"
DB_SERVER = f"{SERVER_DATA}/sql.db"
DB_CLIENT = f"{CLIENT_DATA}/sql.db"

HOST = ""
PORT = 65432
HEADER = 64
FORMAT = "utf-8"
ADDR = (HOST,PORT)
CHAT_SERVER = ("server",PORT)
DISCONNECT_MESSAGE = "________!DISSCONNECT!________"

KEY_SIZE = 1024
PUBLIC_KEY = f"{CLIENT_DATA}/publicKey.pem"
PRIVATE_KEY = f"{CLIENT_DATA}/privateKey.pem"