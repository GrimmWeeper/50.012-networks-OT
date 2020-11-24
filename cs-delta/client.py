#import the socket module
import socket

import sys
sys.path.append('../')
from delta import Delta

#Create a socket instance
socketObject = socket.socket()
host = '127.0.0.1'
port = 2004

print("Waiting for connection response")
#Using the socket connect to a server...in this case localhost

try:
    socketObject.connect((host, port))
    print("Connected to localhost")

except socket.error as e:
    print(str(e))

res = socketObject.recv(1024)

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


    messageBytes = str.encode(str(client_delta))
    socketObject.sendall(messageBytes)

    data = socketObject.recv(1024)
    print(data)


socketObject.close()