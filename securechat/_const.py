import os

MODULE_NAME = "securechat"
FORMAT = "utf-8"

SERVER_DATA = f"{os.path.expanduser('~')}/.securechat/server"
CLIENT_DATA = f"{os.path.expanduser('~')}/.securechat/client"

HOST = ""
PORT = 65432
BUFFER_SIZE = 1024

KEY_SIZE = 1024
PUBLIC_KEY = f"{CLIENT_DATA}/publicKey.pem"
PRIVATE_KEY = f"{CLIENT_DATA}/privateKey.pem"