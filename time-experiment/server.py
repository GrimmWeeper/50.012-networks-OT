import socket
import os
from _thread import *

import counter

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
clients= set()

value = 1

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
    global value
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        client_message = data.decode('utf-8')
        print(client_message)
        value = counter.compute(value, client_message)
        print(value)
        response = 'Server message: ' + str(value)
        if not data:
            break
        print(response)
        connection.sendall(str.encode(response))
    # connection.close()

while True:
    Client, address = ServerSideSocket.accept()
    clients.add(Client)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()