# import the socket module
import socket

import counter
import time
import matplotlib.pyplot as plt
import csv

time_list = []
idx_list = []



for i in range(30):
    start = time.time()
    time.sleep(0.2)
    
    for j in range(i+1):

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

        message = counter.gen_operation()
        messageBytes = str.encode(message)
        socketObject.sendall(messageBytes)
        data = socketObject.recv(1024)
        print(data)

    end = time.time() - start
    time_list.append(end)
    idx_list.append(i+1)

print(time_list)


# Plot graph
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(idx_list, time_list, 'go-', alpha=0.5)
ax.set_title(
    "Time Taken to Reach Eventual Consistency (ms) against Number of Clients"
)
ax.set_xlabel("Number of clients")
ax.set_ylabel("Time Taken to reach eventual consistency (ms)")
plt.savefig('client_server.png', format='png')


# Save values as csv file
with open('client_server.csv', 'w', encoding='utf-8', newline='') as fh:
    writer = csv.writer(fh)
    writer.writerow([
        "Number of Clients", "Time Taken to Reach Eventual Consistency (ms)"
    ])
    for _each in list(zip(idx_list, time_list)):
        writer.writerow(list(_each))



socketObject.close()
