# import the socket module
import socket

# Create a socket instance
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
    # Writing something
    if(i == 0):
        message = "Test message from Client {} \n".format(i+1)
        f = open("sharedfile.txt", "w")
        f.write(message)
        f.close()
        messageBytes = str.encode(message)
        socketObject.sendall(messageBytes)
        data = socketObject.recv(1024)
        print(data)
    #Adding on to client 1
    elif(i == 1):
        message = "Test message from other client {} \n".format(i+1)
        f = open("sharedfile.txt", "a")
        f.write(message)
        f.close()
        messageBytes = str.encode(message)
        socketObject.sendall(messageBytes)
        data = socketObject.recv(1024)
        print(data)
    #Delete
    elif(i == 2):
        message = "Client 3: I've deleted edits made by client 2 \n"
        open_file = open("sharedfile.txt", "r")
        lines = open_file.readlines()
        open_file.close()
        del lines[1]
        f = open("sharedfile.txt", "w+")
        for line in lines:
            f.write(line)
        f.write(message)
        f.close()
        messageBytes = str.encode(message)
        socketObject.sendall(messageBytes)
        data = socketObject.recv(1024)
        print(data)
    #Insert 
    elif(i == 3):
        open_file = open("sharedfile.txt", "r")
        lines = open_file.readlines()
        open_file.close()
        message = "Client 4 has inserted this message between the first two lines \n"
        lines.insert(1,message)
        f = open("sharedfile.txt","w+")
        for line in lines:
            f.write(line)
        f.close()
        messageBytes = str.encode(message)
        socketObject.sendall(messageBytes)
        data = socketObject.recv(1024)
        print(data)
    #Move
    else: 
        open_file = open("sharedfile.txt","r")
        lines = open_file.readlines()
        open_file.close()
        first_line = lines[0]
        lines.pop(0)
        lines.append(first_line)
        f = open("sharedfile.txt","w+")
        for line in lines:
            f.write(line)
        message = "Client 5 has moved the edit made by client 1 \n"
        f.write(message)
        f.close()
        messageBytes = str.encode(message)
        socketObject.sendall(messageBytes)
        data = socketObject.recv(1024)
        print(data)



socketObject.close()
