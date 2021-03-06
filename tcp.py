#Bank Side
import bitarray
import bitarray.util
import pickle
import threading
import socket
import time
import tripleDES
import DES
import sys
import RSA
import bank
from MAC import *
kill = False
#Use this to choose a new secret port

BUFFSIZE = 2048
HOST = sys.argv[1]  # Standard loopback interface address (localhost)
PORT = int(sys.argv[2])
SECRET_PORT = int(sys.argv[3])
secretPORT = None
def decrypt(x):
    return x

#blocks a recieve call waiting for data from socket
def receive(socket,n):
    data = socket.recv(n)
    return pickle.loads(data)

def send(socket, data):
    msg = pickle.dumps(data)
    socket.sendall(msg)
def encryptedSend(socket, data, key):
    # pass data through hmac
    # send DES[(data, hash)]
    mac = hmac_fn(str(data), int(key, 2))
    payload = (data, mac)
    msg = tripleDES.tripleDESCBCEncryptAny(payload, key)
    msg = pickle.dumps(msg)
    socket.sendall(msg)

def encryptedReceive(socket, n, key):
    data = socket.recv(n)
    data = pickle.loads(data) 
    data, mac = tripleDES.tripleDESCBCDecryptAny(data, key)
    if vrfy(str(data), mac, int(key, 2)):
        return data
    else:
        assert(False)

def receiveAsync(socket, n, username, bankfile, DES_key):
    while not kill:
        option, data = encryptedReceive(socket, BUFFSIZE, DES_key)
        if option == "W":
            print("received withdraw command from client")
            success, balance = bank.withdraw(bankfile, username, data)
            if success:
                encryptedSend(socket, "Successful withdrawal\nCurrent balance: ${:.2f}".format(balance), DES_key)
            else:
                encryptedSend(socket, "Failed withdrawal, insufficient funds!\nCurrent balance: ${:.2f}".format(balance), DES_key)
        elif option == "D":
            print("received deposit command from client")
            success, balance = bank.deposit(bankfile, username, data)
            if success:
                encryptedSend(socket, "Successful deposit\nCurrent balance: ${:.2f}".format(balance), DES_key)
            else:
                encryptedSend(socket, "Failed deposit, this is not possible!\nCurrent balance: ${:.2f}".format(balance), DES_key)
        elif option == "C":
            print("received check command from client")
            success, balance = bank.checkBalance(bankfile, username)
            encryptedSend(socket, "Current balance: ${:.2f}".format(balance), DES_key)
        else:
            print("invalid choice!\n")

def threadingStuff(s, n, username, bankfile, key):
    receive_thread = threading.Thread(target=receiveAsync, args=(s,n, username, bankfile, key) )
    receive_thread.start()

if __name__ == '__main__':
    bankfile = "accounts.json"
    #Generate DES Keys
    DES_key = tripleDES.genRandomKey(192)
    #Login
    print(f"Opening Bank on {HOST} at port {PORT}.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        #wait for client to connect
        s.listen()
        conn, addr = s.accept()
        print('Connected by', addr)
        welcome = "Welcome To HHS Bank.\n Please send Public RSA Keys >>> "
        time.sleep(1)
        send(conn, welcome)

        # RSA Key Exchange
        RSA_keys = receive(conn, BUFFSIZE)
        e,N = RSA_keys
        print(f"Recieved Public RSA Keys: {e}, {N}")

        SECRET_PORT_encrypted = RSA.encrypt(SECRET_PORT, e, N)

        #Send Secret Port to client
        print(f"Sending Secret Port {SECRET_PORT} to client.")
        send(conn, SECRET_PORT_encrypted)

        secret_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secret_socket.bind( (HOST, SECRET_PORT) )
        print(f"Opening Secret Bank on {HOST} at port {SECRET_PORT}.")
        
        #wait for client to connect to secret port
        secret_socket.listen()
        conn, addr = secret_socket.accept()
        print('Connected by', addr)

        send(conn, "Welcome to the secret port.")

        #send encrypted DES keys to client
        print("Sending encrypted DES key")
        DES_key_encrypted = RSA.encrypt(DES_key, e, N)
        send(conn, DES_key_encrypted)
        #conn.sendall((DES_key_encrypted) )
        time.sleep(1)
        send(conn, "Please enter username and password >>>")
        encryptedUsername, encryptedPassword = receive(conn, BUFFSIZE)
        decryptedUsername = tripleDES.tripleDESCBCDecrypt(encryptedUsername, DES_key)
        decryptedPassword = tripleDES.tripleDESCBCDecrypt(encryptedPassword, DES_key)
        if bank.verifyPassword(bankfile, decryptedUsername, decryptedPassword):
            print(f"{decryptedUsername} has logged in.")
            encryptedSend(conn, f"Hello {decryptedUsername}, you are logged in!", DES_key)
        else:
            encryptedSend(conn, "Incorrect password! Terminating connection!", DES_key)
            print(f"Invalid login with username {decryptedUsername}.")
            exit(0)

        threadingStuff(conn, BUFFSIZE, decryptedUsername, bankfile, DES_key)


