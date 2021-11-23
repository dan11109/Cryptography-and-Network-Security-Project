#Bank Side
import pickle
import threading
import socket
import time
import tripleDES
import DES
import sys
import RSA
kill = False
#Use this to choose a new secret port

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = int(sys.argv[1])
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

def verify_password(user, pswrd):
    return True

def receiveAsync(socket, n):
    while not kill:
        option, data = receive(socket, n)
        if option == "W":
            print("received withdraw command from client")
            send(socket, "successful withdrawal\n")
        elif option == "D":
            print("received deposit command from client")
            send(socket, "successful deposit\n")
        elif option == "C":
            print("received check command from client")
            send(socket, "successful check\n")
        else:
            print("invalid choice!\n")


def threadingStuff(s, n):
    receive_thread = threading.Thread(target=receiveAsync, args=(s,n) )
    receive_thread.start()

if __name__ == '__main__':
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
        RSA_keys = receive(conn, 1024)
        e,N = RSA_keys
        print(f"Recieved Public RSA Keys: {e}, {N}")

        #send encrypted DES keys to client
        print("Sending encrypted DES key")
        DES_key_encrypted = RSA.encrypt(DES_key, e, N)
        send(conn, DES_key_encrypted)
        #conn.sendall((DES_key_encrypted) )
        time.sleep(1)
        send(conn, "Please enter username and password >>>")
        encryptedUsername, encryptedPassword = receive(conn, 1024)
        decryptedUsername = tripleDES.tripleDESCBCDecrypt(encryptedUsername, DES_key)
        decryptedPassword = tripleDES.tripleDESCBCDecrypt(encryptedPassword, DES_key)
        print("why doesn't this print")
        print(decryptedUsername, decryptedPassword)
        threadingStuff(conn, 1024)


