import socket
import os
from _thread import *

import sys
sys.path.append('../')
from delta import Delta

import utils

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2005
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
        operation = ''
        retain = ''

        retain = input("Input position value to retain: ")
        operation = input("Input Operation (insert/delete): ")
        value = input("Input value for operation (insert: text | delete: position value): ")


        if retain == '':
            if operation == 'insert':
                server_delta = Delta().insert(value)
            
            elif operation == 'delete':
                server_delta = Delta().delete(int(value))
        
        else:
            if operation == 'insert':
                server_delta = Delta().retain(int(retain)).insert(value)
            
            elif operation == 'delete':
                server_delta = Delta().retain(int(retain)).delete(int(value))   


        print("\n")
        print("[Initial State]:", delta_object)
        print("[Server Operation]:", server_delta)

        server_local = delta_object.compose(server_delta)

        print("[State after Server Operation]:", server_local)
        print("\n")
        
        data = connection.recv(2048)
        client_message = data.decode('utf-8')
        print(client_message)

        client_delta = utils.string_to_delta(client_message)

        print("[Client Operation]:", client_delta)

        client_transform = server_delta.transform(client_delta)
        print("[Transformed Client Operation]:", client_transform)

        server_result = server_local.compose(client_transform)
        print("\n")
        print("[Eventual State in Server]:", server_result)

        response = str(server_delta)
        if not data:
            break
        connection.sendall(str.encode(response))
    connection.close()

while True:

    Client, address = ServerSideSocket.accept()
    clients.add(Client)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()