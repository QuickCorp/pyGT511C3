'''
Created on 08/04/2014

@author: jeanmachuca

SAMPLE CODE:

This script is a test for device connected to GPIO port in raspberry pi 

For test purpose:

Step 1:
Connect the TX pin of the fingerprint GT511C3 to RX in the GPIO

Step 2:
Connect the RX pin of the fingerprint GT511C3 to TX in the GPIO 

Step 3: 
Connect the VCC pin of the fingerprint GTC511C3 to VCC 3,3 in GPIO

Step 4: 
Connect the Ground pin of fingerprint GT511C3 to ground pin in GPIO


This may be works fine, if don't, try to change the fingerprint baud rate with baud_to_115200.py sample code


'''
import FPS, sys

if __name__ == '__main__':
    fps =  FPS.FPS_GT511C3(device_name='/dev/ttyAMA0',baud=9600,timeout=2)
    fps.UseSerialDebug = True
    fps.SetLED(True) # Turns ON the CMOS LED
    fps.delay(1) # wait 1 second
    print 'Put your finger in the scan'
    counter = 0 # simple counter for wait 10 seconds
    while counter < 10:
        if fps.IsPressFinger():  #verify if the finger is in the scan
            print 'Your finger is in the scan'
            fps.SetLED(False) # Turns OFF the CMOS LED
            break
        else:
            delay(1) #wait 1 second
            counter = counter + 1
    
    fps.Close() # Closes serial connection
    pass

