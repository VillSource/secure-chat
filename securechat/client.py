import socket
import threading
import base64
import sys

from loguru import logger

from ._const import CHAT_SERVER, DISCONNECT_MESSAGE, FORMAT, HEADER

from .key import loadKeys, encrypt, decrypt

_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_erase = '\x1b[1A\x1b[2K'


def send(msg:str):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    _client.send(send_len)
    _client.send(message)

def sendEncrypt(msg:str,key):
    ciper = encrypt(msg,key)
    send(ciper.decode(FORMAT))
    
def closeConnection(exitCode:int=0):
    send(DISCONNECT_MESSAGE)
    _client.close()
    sys.exit(exitCode)

def connectToServer():
    try: _client.connect(CHAT_SERVER)
    except: _client.connect(("localhost",65432))

def sendInputMessages():
    pri, pub = loadKeys()
    while True:
        m = input("> ")
        print(_erase + "[ME] : " + m, end="\n\n")
        sendEncrypt(m,pub)

def printResivedMessages():
    while True:
        msg = _client.recv(1024).decode(FORMAT)
        if msg:
            print(_erase + msg, end="\n\n" )
            if msg == DISCONNECT_MESSAGE:closeConnection()

def gochat():
    connectToServer()

    revm = threading.Thread( target= printResivedMessages )
    sndm = threading.Thread( target= printResivedMessages )

    # printResivedMessages()
    sndm.start()
    revm.start()

    sndm.join()
    closeConnection()

def online(name):
    pass
