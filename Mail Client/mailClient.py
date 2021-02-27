from socket import *
import base64
import ssl
import sys

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
senderMail = "nevragurses16@gmail.com"
receiverMail = "nevra.gurses2016@gtu.edu.tr"
password= "*** ENTER PASSWORD OF SENDER MAIL ***" #I delete my password for this area.

# Choose a mail server (I choose Google mail server) and call mailserver
mailserver = ("smtp.gmail.com", 587) 

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024)
print recv 
if recv[:3] != '220':
    print '220 reply not received from server.'

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '250':
    print '250 reply not received from server.' 


#Open TLS for Google mail server
clientSocket.send(('starttls\r\n').encode())
recv2=clientSocket.recv(1024)
print 'After start TLS: ', recv2
if recv2[:3] != '220':
    print '220 reply not received from server.'


# Secure Sockets Layer (SSL) for authentication and security reasons
wrap_socket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
wrap_socket.send('auth login\r\n')
recv3 =wrap_socket.recv(1024)
print 'Server response after Auth Login:', recv3
wrap_socket.send(base64.b64encode(senderMail)+'\r\n')
recv4 =wrap_socket.recv(1024)
print 'Server response after Mail auth:', recv4
wrap_socket.send(base64.b64encode(password)+'\r\n')
recv5 =wrap_socket.recv(1024)
print 'Server response after Password auth:', recv5


# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM: <"+senderMail+"> \r\n"
wrap_socket.send(mailFrom.encode())
recv6 =wrap_socket.recv(1024)
print 'Server response after MAIL FROM command:' , recv6 
if recv6[:3] != '250':
    print '250 reply not received from server.'

# Send RCPT TO command and print server response.
rcptTo = "RCPT TO: <"+receiverMail+"> \r\n"
wrap_socket.send(rcptTo.encode())
recv7 = wrap_socket.recv(1024)
print 'Server response after RCPT TO command', recv7
if recv7[:3] != '250':
    print '250 reply not received from server.'

# Send DATA command and print server response.
data = "DATA\r\n"
wrap_socket.send(data.encode())
recv8 = wrap_socket.recv(1024).decode()
print 'Server response after DATA command: ',recv8
if recv8[:3] != '354':
    print '354 reply not received from server.' 


# Send message data.
subject = 'Subject: Mail Client Testing with using SMTP protocol \r\n'
wrap_socket.send(subject.encode())
wrap_socket.send(msg.encode())

#message ends with single period.
wrap_socket.send(endmsg.encode())
recv9 = wrap_socket.recv(1024)
print 'After send message data: ',recv9.decode()
if recv9[:3] != '250':
    print '250 reply not received from server.'

# Send QUIT command and get server response.
wrap_socket.send("QUIT\r\n".encode())
recv10=wrap_socket.recv(1024)
print 'Server response after QUIT command: ', recv10
if recv10[:3] != '221':
    print '221 reply not received from server.'
wrap_socket.close() #close socket.