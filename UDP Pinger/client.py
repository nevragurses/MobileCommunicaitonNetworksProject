from socket import * 
import datetime
import time

clientSocket = socket(AF_INET,SOCK_DGRAM) #create the socket.
clientSocket.settimeout(1) #set the timeout at 1 second.
sequence_number = 1 #ping counter.

while sequence_number<=10:
    message =  'Ping: '+ str(sequence_number) + ' '  + str(datetime.datetime.now()) #ping message.
    start=time.time() #keep current time.

    clientSocket.sendto(message,('Localhost', 12000))#send ping message via localhost.

    print 'Sending Ping Message:', message
    try:
        message_pong, address = clientSocket.recvfrom(1024) #recieving message from server.
        finish = time.time() #finish time.
        rtt=finish-start #round trip time.

        #print pong message.
        print 'Receiving Pong Message:',message_pong
        print 'Round Trip Time(RTT): ',rtt, 'seconds','\n'
    except timeout: #if the socket takes longer that 1 second print timed out message.
        print 'Request timed out for sequence number:', sequence_number,'\n' 

    sequence_number = sequence_number + 1 #increase ping index number
    if sequence_number > 10: #closes the socket after 10 ping message.
        clientSocket.close()