import socket
import os
from _thread import *

import sys
sys.path.append('../')
from delta import Delta

import utils

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
clients= set()

delta_object = Delta().insert('ABCD')

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
    global delta_object
    connection.send(str.encode('Server is working:'))
    while True:

        print("[Current State]:", delta_object)
        
        data = connection.recv(2048)
        if not data:
            break

        client_message = data.decode('utf-8')
        print(client_message)

        client_delta = utils.string_to_delta(client_message)

        print("[Client Operation]:", client_delta)


        delta_object = delta_object.compose(client_delta)
        print("[Eventual State in Server]:", delta_object)
        response = str(delta_object)

        connection.sendall(str.encode(response))
        print('\n')
    connection.close()

while True:
    Client, address = ServerSideSocket.accept()
    clients.add(Client)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()