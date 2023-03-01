from time import sleep
import socket
import threading

from loguru import logger

from .repository import User, Tweet, init_db

from ._const import ADDR,HEADER, DISCONNECT_MESSAGE, FORMAT

__db = init_db()
__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
__server.bind(ADDR)

def handle_client(conn:socket.socket,addr):
    logger.info(f"[NEW CONNECTION] {addr} connected.")
    sleep(1)
    conn.send(b"Welcome1...")
    print(b"Welcome1...")
    sleep(1)
    conn.send(b"Welcome1...")
    print(b"Welcome1...")
    sleep(1)
    conn.send(b"Welcome1...")
    print(b"Welcome1...")
    sleep(1)
    conn.send(b"Welcome1...")
    print(b"Welcome1...")
    sleep(1)
    conn.send(b"Welcome1...")
    print(b"Welcome1...")

    connected = True
    try:
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                conn.send(f"reseved : {str(msg)}".encode(FORMAT))
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                logger.info(f"[{addr}] {msg}")
    except KeyboardInterrupt:pass
    conn.close()

def start_server():
    logger.info("Starting server")
    __server.listen()
    try:
        while True:
            conn, addr = __server.accept()
            thred = threading.Thread(target=handle_client, args=(conn, addr))
            thred.start()
            logger.info(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")
    except KeyboardInterrupt :pass
    __server.close()
    print("[CLOSED]")