import socket
import threading

from rsa import PublicKey, PrivateKey

from ._const import FORMAT, BUFFER_SIZE
from .key import loadB64Key, loadKeys, loadKeysBase64, encrypt, decrypt

class ChatServer:
    '''
    class for chat server
    '''
    def __init__(self, host, port, max_clients):
        print("init server...")
        self.all_users = []
        #create socket and listen new connections
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(max_clients)
        self.pirvate_key, _ = loadKeys()
        _, self.public_key64 = loadKeysBase64()
        print("server: OK")
        print("started")
        
        
    def run(self):
        '''
        function for receiving new connection,
        for creating new thread, which handle own clients.
        '''
        while True:
            conn, addr = self.sock.accept()
            tr = threading.Thread( target=self.client_handler, args=(conn,))
            tr.daemon = True
            tr.start()

    def resive_name(self, conn:socket.socket):
        name = conn.recv(BUFFER_SIZE)
        name = decrypt(name,self.pirvate_key)
        return name
    
    def resive_key(self, conn:socket.socket)->PublicKey:
        key = conn.recv(BUFFER_SIZE).decode(FORMAT)
        return loadB64Key(key)
            
    def client_handler(self, conn:socket.socket):
        '''
        function for handling new connection
        '''
        
        # Resive client key then send server key to client
        key = self.exchange_key(conn)
        # Resive name from client as a message on first connection
        name = self.resive_name(conn)
        
        print(name,'joined with key : ', key)
        hello_string = f"Hello, {name}. Users online is {len(self.all_users)}"
        hello_string = encrypt(hello_string, key)
        conn.sendall(hello_string)
        self.all_users.append((conn, name, key))
        msg_to_all = " Entered chat!"
        self.send_message_to_others_with_encryption((conn, name, key), msg_to_all)    
        
        #infinite loop for receiving messages from client
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            print(name + ' ' + data.decode(FORMAT))
            data = decrypt(data, self.pirvate_key)
            self.send_message_to_others_with_encryption((conn, name, key), data)    
        #client left chat
        conn.sendall(b'By')
        self.send_message_to_others_with_encryption( (conn, name, key), " ~ left the chat! ~".format(name))    
        self.delete_user(conn)

    def exchange_key(self,conn):
        '''
        exchange key between client and server
        '''
        key = self.resive_key(conn)
        conn.sendall(self.public_key64.encode(FORMAT))
        
        return key
        
    def delete_user(self, del_user):
        '''
        function for delete client from list all_users
        '''
        for i in range(len(self.all_users)):
            if self.all_users[i][0] == del_user:
                del self.all_users[i]
                break

    def send_message_to_others(self, from_user, message):
        '''
        function for sending message to all client except sender
        '''
        if len(self.all_users) > 1:
            for user in self.all_users:
                if user[0] != from_user[0]:
                    msg = "{}: {}".format(from_user[1], message)
                    user[0].sendall(msg.encode(FORMAT))
                    #print("message send")

    def send_message_to_others_with_encryption(self, from_user, message):
        '''
        function for sending message to all client except sender with encrypt with sender key
        '''
        assert len(from_user) == 3

        if len(self.all_users) > 1:
            for user in self.all_users:
                if user[0] != from_user[0]:
                    msg = "{}: {}".format(from_user[1], message)
                    cipher = encrypt(msg,user[2])
                    user[0].sendall(cipher)
                    #print("message send")
                    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, tb):
        self.sock.close()
        print("server is going down.")

def startServer(host:str, port:int, max_clients:int):
    with ChatServer(host, port, max_clients) as chat:
        chat.run()