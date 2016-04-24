# SYNAPSEBREAK 2016
import socket
import sys

try:
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print('Failed to create socket. Error code:' + str(msg[0]) + ' Error Message: ' + msg[1])
    sys.exit();
          
print('Socket Created')

host = 'IP OF SERVER'
port = 12344 and 12345
          
try:
    remote_ip =(host)

except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit
print('IP adress of PiServer is ' + remote_ip)

s.connect((remote_ip, port))

print('Socket Connected to ' + host + ' on ip ' + remote_ip)
      
message = ('applianceOn'.encode('ascii'))

try:
    s.sendall (message)
except socket.error:
    print('Send failed')
    sys.exit()

print('Message was sent successfully')

reply = s.recv(4096).decode('ascii')

print(reply)
s.close()
