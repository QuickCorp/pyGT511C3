'''
Created on 08/04/2014

@author: jeanmachuca

SAMPLE CODE:

This is for to change the fingerprint baud rate to 9600

Executes this script only once
'''
import FPS, sys

DEVICE_GPIO = '/dev/ttyAMA0'
DEVICE_LINUX = '/dev/cu.usbserial-A601EQ14'
DEVICE_MAC = '/dev/cu.usbserial-A601EQ14'
DEVICE_WINDOWS = 'COM3'
FPS.BAUD = 115200 #initial baud rate
FPS.DEVICE_NAME = DEVICE_MAC

if __name__ == '__main__':
    fps = FPS.FPS_GT511C3(device_name=DEVICE_MAC,is_com=True)
    fps.UseSerialDebug = True
    fps.ChangeBaudRate(9600)
    fps.Close()
    pass
