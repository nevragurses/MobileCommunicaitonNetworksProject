#import socket module
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket
port = 8080
serverSocket.bind(('', port)) 
serverSocket.listen(1)    #for listening socket.

while True:
    #Establish the connection
    print 'Ready to serve...'
    connectionSocket, addr = serverSocket.accept() 

    try:
        message =connectionSocket.recv(1024) #receives message from client.
        filename = message.split()[1] #split message for getting file name.
        f = open(filename[1:]) #opens file and reads the contents
        outputdata =f.read()
        print outputdata
        #send one HTTP header line into socket.
        connectionSocket.send('HTTP/1.0 200 OK\r\n\n\n')

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i]) 

        f.close()  #close the file.     
        connectionSocket.close() #closes the socket for client.

    except IOError:
        #Send response message for file not found
        print '404 Not Found'
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\n') 
        #Close client socket
        connectionSocket.close()
serverSocket.close()