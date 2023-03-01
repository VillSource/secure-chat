import rsa, os, base64
from rsa import PrivateKey, PublicKey

from ._const import KEY_SIZE, PUBLIC_KEY, PRIVATE_KEY, FORMAT, CLIENT_DATA

def mkdir():
    if not os.path.exists(CLIENT_DATA):
        os.makedirs(CLIENT_DATA)

def generateKeys():
    mkdir()
    (publicKey, privateKey) = rsa.newkeys(KEY_SIZE)
    with open(PUBLIC_KEY, 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open(PRIVATE_KEY, 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))

def loadKeys()->tuple[PrivateKey, PublicKey]:
    assert os.path.exists(PUBLIC_KEY) == True
    assert os.path.exists(PUBLIC_KEY) == True

    with open(PUBLIC_KEY, 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open(PRIVATE_KEY, 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey

def encrypt(message:str, key:PublicKey)->bytes:
    return base64.b64encode(rsa.encrypt(message.encode(FORMAT), key))

def decrypt(ciphertext:bytes, key:PrivateKey):
    try:
        return rsa.decrypt(ciphertext, key).decode(FORMAT)
    except:
        return False
    
def sign(message:str, key:PrivateKey)->bytes:
    return rsa.sign(message.encode(FORMAT), key, 'SHA-1')

def verify(message:str, signature:bytes, key:PublicKey):
    try:
        return rsa.verify(message.encode(FORMAT), signature, key,) == 'SHA-1'
    except:
        return False
    

