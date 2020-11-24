#import the socket module
import socket

import sys
sys.path.append('../')
from delta import Delta

import utils

#Create a socket instance
socketObject = socket.socket()
host = '127.0.0.1'
port = 2005

print("Waiting for connection response")
#Using the socket connect to a server...in this case localhost

try:
    socketObject.connect((host, port))
    print("Connected to localhost")

except socket.error as e:
    print(str(e))

res = socketObject.recv(1024)

delta_object = Delta().insert('ABCD')

# Receive the data
while(True):

    operation = ''
    retain = ''

    retain = input("Input position value to retain: ")
    operation = input("Input Operation (insert/delete): ")
    value = input("Input value for operation (insert: text | delete: position value): ")


    if retain == '':
        if operation == 'insert':
            client_delta = Delta().insert(value)
        
        elif operation == 'delete':
            client_delta = Delta().delete(int(value))
    
    else:
        if operation == 'insert':
            client_delta = Delta().retain(int(retain)).insert(value)
        
        elif operation == 'delete':
            client_delta = Delta().retain(int(retain)).delete(int(value))        

    

    print("[Initial State]:", delta_object)
    print("[Client Operation]:", client_delta)

    client_local = delta_object.compose(client_delta)

    print("[State after Client Operation]:", client_local)
    
    messageBytes = str.encode(str(client_delta))
    socketObject.sendall(messageBytes)

    data = socketObject.recv(1024).decode('utf-8')

    server_delta = utils.string_to_delta(data)

    print("[Server Operation]:", server_delta)

    server_transform = client_delta.transform(server_delta)
    print("[Transformed Server Operation]:", server_transform)

    client_result = client_local.compose(server_transform)
    print("[Eventual State in Client]:", client_result)



socketObject.close()