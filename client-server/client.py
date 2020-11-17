#import the socket module
import socket

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

    message = input("Input message to send to server: ")

    if message == "exit":
        break
    
    else:
        messageBytes = str.encode(message)
        socketObject.sendall(messageBytes)

    data = socketObject.recv(1024)
    print(data)


socketObject.close()