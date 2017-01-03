#!/usr/bin/python

import os
import sys
sys.path.append(os.getcwd() + "/MPU6050")
import mpu6050
import time
import math
import csv
import socket
import smbus
from pycomms import PyComms

# Sensor initialization
mpu = mpu6050.MPU6050()
mpusla = mpu6050.MPU6050(0x69)
mpu.dmpInitialize()
mpusla.dmpInitialize()
mpu.setDMPEnabled(True)
mpusla.setDMPEnabled(True)

# Send UDP Data
def send_data(msg):
    try:
        sock.sendto(msg,(REMOTE_IP,DST_PORT))
    except socket.error as err:
        sock.close()
        print "Connection err!"
    
# get expected DMP packet size for later comparison
packetSize = mpu.dmpGetFIFOPacketSize() 

'''

# TCP socket instance
addr=('192.168.0.105',8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(addr)
sock.listen(5)
print("waiting for connect")
conn,addr=sock.accept()
print("server already connect client...->")

'''

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

REMOTE_IP="192.168.0.101"
DST_PORT=8000

print ("IMU Sensor started (CTRL-C to stop)!")
num=0
while True:
    print (num)
    num=num+1
    # Get INT_STATUS byte
    # master part
    mpuIntStatus = mpu.getIntStatus()
    mpuslaIntStatus = mpusla.getIntStatus()
  
    # check for DMP data ready interrupt (this should happen frequently) 
    if mpuIntStatus >= 2:
        # get current FIFO count
        fifoCount = mpu.getFIFOCount()
        
        # check for overflow (this should never happen unless our code is too inefficient)
        if fifoCount == 1024:
            # reset so we can continue cleanly
            mpu.resetFIFO()
            #print('FIFO overflow!')
        # wait for correct available data length, should be a VERY short wait
        fifoCount = mpu.getFIFOCount()
        while fifoCount < packetSize:
            fifoCount = mpu.getFIFOCount()
        
        result = mpu.getFIFOBytes(packetSize)
        # Get quaternio, q return y, x, z, w
        q = mpu.dmpGetQuaternion(result)
        x = "{0:.6f}".format(q['x'])
	y = "{0:.6f}".format(q['y'])
	z = "{0:.6f}".format(q['z'])
	w = "{0:.6f}".format(q['w'])
        send_data(str(x) + "," + str(y) + "," + str(z) + "," + str(w)+",1")
        #print ("mas: %s %s %s" %(x,y,z))
        fifoCount -= packetSize
    ##### slave part ######################################
    #mpuslaIntStatus = mpusla.getIntStatus()
  
    # check for slave DMP data ready interrupt (this should happen frequently) 
    if mpuslaIntStatus >= 2:
        # get current FIFO count
        fifoslaCount = mpusla.getFIFOCount()
        
        # check for overflow (this should never happen unless our code is too inefficient)
        if fifoslaCount == 1024:
            # reset so we can continue cleanly
            mpusla.resetFIFO()
            #print('slave FIFO overflow!')
        # wait for correct available data length, should be a VERY short wait
        fifoslaCount = mpusla.getFIFOCount()
        while fifoslaCount < packetSize:
            fifoslaCount = mpusla.getFIFOCount()
        
        slaresult = mpusla.getFIFOBytes(packetSize)
        # Get quaternion, q return y, x, z, w
        qslave = mpusla.dmpGetQuaternion(slaresult)
    #################################################################
        sla_x = "{0:.6f}".format(qslave['x'])
	sla_y = "{0:.6f}".format(qslave['y'])
	sla_z = "{0:.6f}".format(qslave['z'])
	sla_w = "{0:.6f}".format(qslave['w'])
        #print ("sla: %s" %sla_w)
        #print ("sla: %s %s %s" %(sla_x,sla_y,sla_z))
        send_data(str(sla_x) + "," + str(sla_y) + "," + str(sla_z) + "," + str(sla_w)+",2")
        fifoslaCount -= packetSize  
        '''
        if DEBUG == "1":
           print (x),
	   print (y),
	   print (z),
	   print (w)
        '''
	# Sends quaternion through UDP

