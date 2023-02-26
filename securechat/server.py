from .repository import User, Tweet, init_server

def start_server():
    db = init_server()