#Client Side
import socket
import time
import logging
import threading
import pickle
import RSA
import DES

BANK = 'localhost'  # Standard loopback interface address (localhost)
PORT = 4005        # Port to listen on (non-privileged ports are > 1023)

kill = False

def encrypt(P):
    return P

def receive_thread(socket,n):
    data = ""
    while not kill:
        data = socket.recv(n)
        if len(data) > 0:
            print(data.decode())
def receive(socket, n):
    data = socket.recv(n)
    print(data)
    if len(data) == 0:
        print("nothing to receive")
        return
    return pickle.loads(data)
    

def send(socket):
    while not kill:
        msg = input()
        socket.sendall(msg.encode())

def send_thread(socket):
    while not kill:
        msg = input()
        socket.sendall(msg.encode())
        print(f"sending {msg}")
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secret_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#generate RSA keys
p,q,e,d = RSA.RSA_params(512)
N = p*q

#Connect To Bank Server
s.connect( (BANK, PORT) )

print( receive(s,1024) ) #welcome Message

#send RSA Keys
print("Sending RSA Public Keys [e,N].")
msg = pickle.dumps((e, N))
s.sendall(msg)
print("here1234")
#Receive DES Key from Bank
DES_key_encrypted = receive(s, 1024)
DES_key = RSA.decrypt(DES_key_encrypted, d, N)
print(f"DES key is \n{DES_key}")

username = 'alpha'
password = 'GTvQq4nRTHzPGz'


"""

receive_thread = threading.Thread(  target=receive, args=(s,1024) )
send_thread = threading.Thread(  target=send, args=(s,) )

receive_thread.start()
send_thread.start()
"""


"""

    data = ""
    while len(data) == 0:
        data = s.recv(1024)
        print(data.decode())
        #s.sendall(msg.encode())

    msg = input()
    secret_PORT = int(msg)
    s.sendall( encrypt(msg).encode() )
    time.sleep(2)
    secret_sock.connect( (BANK, secret_PORT) )

    data = ""
    data1 = ""
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            print(data.decode())
            data = ""

        data1 = secret_sock.recv(1024)
        if len(data1) > 0:
            print(data1.decode())
            break
    #print("here")
    while True:
        data = secret_sock.recv(1024).decode()
        if (len(data) > 0):
            print(data)
            msg = input()
            msg = msg.encode()
            
            secret_sock.sendall(msg)
            data = ""

    print("done")
    def netcat(hostname, port, content):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        s.sendall(content)
        s.shutdown(socket.SHUT_WR)
        while 1:
            data = s.recv(1024)
            if data == "":
                break
            print ("Received:", repr(data))
        print ("Connection closed.")
        s.close()

"""
