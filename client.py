#Client Side
import socket
import time
import logging
import threading
import bitarray.util
import pickle
import RSA
import tripleDES
import sys

BANK = 'localhost'  # Standard loopback interface address (localhost)
PORT = int(sys.argv[1])

kill = False

def encrypt(P):
    return P

def receive(socket, n):
    data = socket.recv(n)
    return pickle.loads(data)

def send(socket, data):
    msg = pickle.dumps(data)
    socket.sendall(msg)

def receiveAsync(socket, n):
    while not kill:
        data = receive(socket, n)
        print(data)



def sendAsync(socket):
    while not kill:
        print("Type W for withdraw, D for deposit, C for check balance")
        option = input()
        if option == "W":
            number = input("Enter an amount to withdraw")
            number = float(number)
            msg = ("W", number)
            send(socket, msg)
        elif option == "D":
            number = input("Enter an amount to deposit")
            number = float(number)
            msg = ("D", number)
            send(socket, msg)
        elif option == "C":
            msg = ("W", None)
            send(socket, msg)
        else:
            print("invalid choice!")
        time.sleep(0.1)


def threadingStuff(s):
    receive_thread = threading.Thread(target=receiveAsync, args=(s, 1024) )
    send_thread = threading.Thread(target=sendAsync, args=(s,) )
    receive_thread.start()
    send_thread.start()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secret_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #generate RSA keys
    p,q,e,d = RSA.RSA_params(512)
    N = p*q

    #Connect To Bank Server
    s.connect( (BANK, PORT) )
    # client receives welcome message
    welcome = receive(s,1024)
    print(welcome) #welcome Message
    #send RSA Keys
    print("Sending RSA Public Keys [e,N].")
    send(s, (e, N))
    #Receive DES Key from Bank
    DES_key_encrypted = receive(s, 1024)
    # DES 
    DES_key = RSA.decrypt(DES_key_encrypted, d, N)
    DES_key = bitarray.util.int2ba(DES_key, length=192)
    print(len(DES_key))
    assert(len(DES_key) == 192)
    print(f"DES key is \n{DES_key}")
    # at this point the client and server have the DES key
    # get username/password prompt from server
    prompt = receive(s, 1024)
    print(prompt)
    username = 'alpha'
    password = 'GTvQq4nRTHzPGz'
    # send user/pass to server
    encryptedUser = tripleDES.tripleDESCBCEncrypt(username, DES_key)
    encryptedPass = tripleDES.tripleDESCBCEncrypt(password, DES_key)
    send(s, (encryptedUser, encryptedPass))
    threadingStuff(s)

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
