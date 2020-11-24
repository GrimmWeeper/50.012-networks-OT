import socket
import os
from _thread import *

import sys
sys.path.append('../')
from delta import Delta

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
clients= set()

delta_object = Delta().insert('ABCDE')

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

def string_to_delta(text):
    temp_text = text[7:]
    delta_text = temp_text[:-2]
    delta_list = delta_text.split(',')

    if len(delta_list) == 1:
        ops = delta_list[0][2:8]
        
        if ops == 'insert':
            value = delta_list[0][12:-2]
            print(value)
            return Delta().insert(value)
        
        elif ops == 'delete':
            value = int(delta_list[0][11:-1])
            return Delta().delete(value)

    elif len(delta_list) == 2:
        for i in range(2):
            if i == 0:
                ops_1 = delta_list[0][2:8]
                value_1 = int(delta_list[0][11:12])

            elif i == 1:
                ops_2 = delta_list[1][3:9]

                if ops_2 == 'insert':
                    value_2 = delta_list[1][13:-2]
                    return Delta().retain(value_1).insert(value_2)
                
                elif ops_2 == 'delete':
                    value_2 = int(delta_list[1][12:-1])
                    return Delta().retain(value_1).delete(value_2)

    return Delta()


def multi_threaded_client(connection):
    global delta_object
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        client_message = data.decode('utf-8')
        print(client_message)

        client_delta = string_to_delta(client_message)
        delta_object = delta_object.compose(client_delta)

        print(client_delta)
        print(delta_object)

        response = 'Server message: ' + str(delta_object)
        if not data:
            break
        print(response)
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