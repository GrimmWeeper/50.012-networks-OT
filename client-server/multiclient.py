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
    if(i == 0): 
        message = "Test message from Client {} \n".format(i+1)
        f = open("sharedfile.txt","w")
        f.write(message)
        f.close()
        messageBytes = str.encode(message)
        socketObject.sendall(messageBytes)
        data = socketObject.recv(1024)
        print(data)
    elif(i==1):
        message = "Test message from other client {} \n".format(i+1)
        f = open("sharedfile.txt","a")
        f.write(message)
        f.close()
        messageBytes = str.encode(message)
        socketObject.sendall(messageBytes)
        data = socketObject.recv(1024)
        print(data)
    elif(i == 2): 
        message = "I've deleted edits made by client 1"
        open_file = open("sharedfile.txt","r")
        lines = open_file.readlines()
        print(lines)
        open_file.close()
        del lines[1]
        f = open("sharedfile.txt","w+")
        for line in lines:
            f.write(line)
        f.write(message)
        f.close()
        messageBytes = str.encode(message)
        socketObject.sendall(messageBytes)
        data = socketObject.recv(1024)
        print(data)
    

socketObject.close()
