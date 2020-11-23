#import the socket module
import socket
import random

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
waitingForServerToComeback = True
unsentBuffer = []
secondSocket = socket.socket()

# Receive the data
while(True):
    if len(unsentBuffer) > 0: 
        print("Re-sending lost messages to server")
        for i in range(len(unsentBuffer)):
            messageBytes = str.encode(unsentBuffer[i])
            secondSocket.sendall(messageBytes)
            res = secondSocket.recv(1024)
            print("Re-sending lost messages to server")
            print(res)
        unsentBuffer = []

    message = input("Input message to send to server: ")

    if message.tolower() == "exit":
        break
    
    else:
        try:
            if waitingForServerToComeback == True:
                messageBytes = str.encode(message)
                socketObject.sendall(messageBytes)
            else:
                messageBytes = str.encode(message)
                secondSocket.sendall(messageBytes)


        except ConnectionResetError as e: #server connection shut down
            unsentBuffer.append(message) #place the unsent message in the buffer
            
            while(waitingForServerToComeback):
                
                try:
                    #newPort = random.randint(port+1,8000)
                    #port_number = newPort
                    #newPort = socket.socket() #new socket used to try and reconnect
                    secondSocket.connect((host,port))
                    print("Server is back")
                    waitingForServerToComeback = False
                    

                except ConnectionRefusedError:
                    print(str(e))

        
    if waitingForServerToComeback == True:
        data = socketObject.recv(1024)
        print(data)
    else:
        data = secondSocket.recv(1024)
        print(data)


socketObject.close()
secondSocket.close()