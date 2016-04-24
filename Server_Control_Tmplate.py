#SYNAPSEBREAK 2016

#Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
#[GCC 4.9.1] on linux
#Type "copyright", "credits" or "license()" for more information.
#!usr/bin/python

import socket
import sys
import os
import RPi.GPIO as GPIO
import time
import subprocess
import threading

#---------------------------------------------------------------------
                    #GPIO input/output setup:

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
GPIO.setup("""NUMBER""", GPIO.OUT)  #EXAMPLE: GPIO.setup(4, GPIO.OUT) #PalmTree Light
GPIO.output("""NUMBER""", True)   #EXAMPLE: GPIO.output(4, True)

#---------------------------------------------------------------------
                             #Guard Bools.

applianceGuard = None    #Example: palmGuard = None  #Palm Bool.


#---------------------------------------------------------------------
                 #Functions and their associated Threads:

def applianceOn():
    def countThread1(i):
        while True: 
            global data, applianceGuard
            if data == ('applianceOff'):
                GPIO.output("""NUMBER""", True)
                applianceGuard = False
                print(c + ' |applianceGuard set to False| ')
                break
            print(c + ' appliance is on ')           
            GPIO.output("""NUMBER""", False)
            time.sleep(2)
            
    for i in range(1):
            t = threading.Thread(target=countThread1, args=(i,))
            t.start()

"""EXAMPLE:          
def palmOn():
    def countThread1(i):
        while True: # THIS ENTIRE WHILE LOOP IS FUCKED UP WITH INVERSES!
            global data, palmGuard
            if data == ('palmOff'):
                GPIO.output(4, True)
                palmGuard = False
                print(c + ' |palmGuard set to False| ')
                break
            print(c + 'Palmtree is lit ')           
            GPIO.output(4, False)
            time.sleep(2)
            
    for i in range(1):
            t = threading.Thread(target=countThread1, args=(i,))
            t.start()   
"""
#-----------------------------------------------------------------------
                                #Time Variables

c = time.strftime('|%I:%M:%S| ', time.localtime())

#-----------------------------------------------------------------------
                #Socket Connection & listening socket loop:
        
HOST = ''
PORT = 12344 and 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(c + 'TCP Local Socket Created')

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('ERROR: Socket bind has failed.')
    sys.exit()
print(c + 'Socket Bind Complete, Port: ' + str(PORT))


while True:
        s.listen(1000)
        print(c + 'Socket(pi) now listening for connections')
        conn, addr = s.accept()
        if addr[0] == ("""IP ADDRESS OF WINDOWS PC"""):    #EXAMPLE: if addr[0] == (192.168.1.___):
            print(c + 'Connected with ' + addr[0] + ':' + str(addr[1]) + (' ("""NAME OF WINDOWS PC""")'))
        elif addr[0] == (''):
            print(c + 'UNIDENTIFIED CONNECTION')
            break
        data = conn.recv(1024).decode('ascii')
        print(c + 'Client says: ' + data)

        reply = ('Reply from Server(pi) received.'.encode('ascii'))
        conn.sendall(reply)
        
#-----------------------------------------------------------------------
        #"Data" disection section ;D


        #TRANSFORM IT ! 
        if data == ('applianceOn'): 
            if applianceGuard is not True:
                applianceOn()
                
            applianceGuard = True
            print(c + ' |applianceGuard set to True| ')
            continue
        
 """ EXAMPLE:
     if data == ('palmOn'): 
            if palmGuard is not True:
                palmOn()
                
            palmGuard = True
            print(c + ' |palmGuard set to True| ')
            continue
"""
 
    

