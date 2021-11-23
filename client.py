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

BANK = sys.argv[1]
PORT = int(sys.argv[2])

kill = False

def encrypt(P):
    return P

def receive(socket, n):
    data = socket.recv(n)
    return pickle.loads(data)

def send(socket, data):
    msg = pickle.dumps(data)
    socket.sendall(msg)

def encryptedSend(socket, data, key):
    msg = tripleDES.tripleDESCBCEncryptAny(data, key)

    msg = pickle.dumps(msg)
    socket.sendall(msg)

def encryptedReceive(socket, n, key):
    data = socket.recv(n)
    data = pickle.loads(data) 
    return tripleDES.tripleDESCBCDecryptAny(data, key)

def receiveAsync(socket, n, key):
    while not kill:
        data = encryptedReceive(socket, n, key)
        print(data)

def sendAsync(socket, key):
    while not kill:
        time.sleep(0.1)
        print("Type W for withdraw, D for deposit, C for check balance")
        option = input()
        if option == "W":
            number = input("Enter an amount to withdraw")
            number = float(number)
            msg = ("W", number)
            encryptedSend(socket, msg, key)
        elif option == "D":
            number = input("Enter an amount to deposit")
            number = float(number)
            msg = ("D", number)
            encryptedSend(socket, msg, key)
        elif option == "C":
            msg = ("C", None)
            encryptedSend(socket, msg, key)
        else:
            print("invalid choice!")


def threadingStuff(s, DES_key):
    receive_thread = threading.Thread(target=receiveAsync, args=(s, 1024, DES_key) )
    send_thread = threading.Thread(target=sendAsync, args=(s, DES_key) )
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
    password = 'FalseSharkTreaty'
    # send user/pass to server
    encryptedUser = tripleDES.tripleDESCBCEncrypt(username, DES_key)
    encryptedPass = tripleDES.tripleDESCBCEncrypt(password, DES_key)
    print("Sending username and password")
    send(s, (encryptedUser, encryptedPass))
    threadingStuff(s, DES_key)
