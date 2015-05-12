'''
Created on 08/04/2014

@author: jeanmachuca

SAMPLE CODE:

This is for to change the fingerprint baud rate 9600 to 115200, 
The baudrate 9600 have troubles with response in usb serial devices

Executes this script only once
'''
import FPS, sys

if __name__ == '__main__':
    fps = FPS.FPS_GT511C3()
    fps.UseSerialDebug = True
    fps.ChangeBaudRate(115200)
    fps.Close()
    pass

