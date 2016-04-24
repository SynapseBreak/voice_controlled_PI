#Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
#SYNAPSEBREAK 2016
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
GPIO.setup(4, GPIO.OUT) #PalmTree Light
GPIO.setup(17, GPIO.OUT) #Christmas Lights (white)
GPIO.setup(27, GPIO.OUT) #TV
GPIO.output(4, True)
GPIO.output(17, True)
GPIO.output(27, True)

#---------------------------------------------------------------------
                             #Guard Bools.

palmGuard = None  #Palm Bool.
houseGuard = None #Houselight Bool.
tvGuard = None  #TV Bool.

#---------------------------------------------------------------------
                 #Functions and their associated Threads:

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

def houseLightOn():   
    def countThread2(i):        
        while True: # THIS ENTIRE WHILE LOOP IS FUCKED UP WITH INVERSES!
            global data, houseGuard
            if data == ('houseLightOff'):
                GPIO.output(17, True)
                houseGuard = False
                print(c + '|houseGuard set to False| ')
                break
            print(c + 'House Lights On ') 
            GPIO.output(17, False)
            time.sleep(2)
            
    for i in range(1):
        t = threading.Thread(target=countThread2, args=(i,))
        t.start()
        
def tvOn():   
    def countThread3(i):        
        while True: # THIS ENTIRE WHILE LOOP IS FUCKED UP WITH INVERSES!
            global data, tvGuard
            if data == ('tvOff'):
                GPIO.output(27, True)
                tvGuard = False
                print(c + ' |tvGuard set to False| ')
                break
            print(c + 'Television is on ')
            GPIO.output(27, False)
            time.sleep(2)
            
    for i in range(1):
        t = threading.Thread(target=countThread3, args=(i,))
        t.start()

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
        if addr[0] == ('192.168.1.111'):
            print(c + 'Connected with ' + addr[0] + ':' + str(addr[1]) + (' (Lizzie)'))
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
        if data == ('palmOn'): 
            if palmGuard is not True:
                palmOn()
                
            palmGuard = True
            print(c + ' |palmGuard set to True| ')
            continue
            
        if data == ('houseLightOn'):
            if houseGuard is not True:
                houseLightOn()

            houseGuard = True  
            print(c + ' |houseGuard set to True| ')
            continue

        if data == ('tvOn'):
            if tvGuard is not True:
                tvOn()

            tvGuard = True
            print(c + ' |tvGuard set to True| ')
            continue

    

