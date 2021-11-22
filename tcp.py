#Bank Side

import socket
import time

#Use this to choose a new secret port

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 4005   # Port to listen on (non-privileged ports are > 1023)
secretPORT = None
def decrypt(x):
    return x

#blocks a recieve call waiting for data from socket
def receive(socket,n):
    data = ""
    while len(data) == 0:
        data = socket.recv(n)

    return data.decode()

def verify_password(user, pswrd):
    return True

#Login
print(f"Opening Bank on {HOST} at port {PORT}.")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    #wait for client to connect
    s.listen()
    conn, addr = s.accept()
    print('Connected by', addr)
    time.sleep(2)

    conn.sendall("Welcome To HHS Bank.\n Please enter your username >>> ".encode())

    username = receive(conn, 1024)
    print(username)
    conn.sendall("Please enter password >>>".encode())
    password = receive(conn, 1024)

    print(username, password)

    if verify_login(username, password):
        pass
    with conn:
        
        conn.sendall("request new port.".encode())
        while True:
            data = conn.recv(1024)
            if not data:
                break
            secretPORT = int(decrypt(data.decode()))
            print(f"migrating to port: {secretPORT}")
            break
        conn.sendall("migrating to new port ".encode()+ data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, secretPORT))
    print(f"Binding to {HOST} on port {secretPORT}.")
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        conn.sendall("welcome to the secret port.".encode())
        conn.sendall("Enter Username".encode())
        username = ""
        while len(username) == 0:
            username = conn.recv(1024).decode()
        print(username)
        password = ""
        conn.sendall("Enter Password".encode())
        while len(password) == 0:
            password = conn.recv(1024).decode()
        print(password)
        print(".")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall("recieved: ".encode()+ data)
            print(f"recieved: {data.decode()} from {addr}")


#Use this to choose a new secret port

