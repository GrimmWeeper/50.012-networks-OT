#import the socket module
import socket

#Create a socket instance
socketObject = socket.socket()
host = '127.0.0.1'
port = 2004

clientNumber = int(input("Input the number of clients to spawn: "))

for i in range(clientNumber):

    socketObject = socket.socket()
    host = '127.0.0.1'
    port = 2004
    print("Waiting for connection response")

    try:
        socketObject.connect((host, port))
        print("Client {} connected to server.".format(i+1))

    except socket.error as e:
        print(str(e))

    res = socketObject.recv(1024)

    message = "Test message"
    messageBytes = str.encode(message)
    socketObject.sendall(messageBytes)
    data = socketObject.recv(1024)
    print(data)

socketObject.close()
