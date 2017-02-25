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


This script Enrolls your finger in the device internal database
you have 200 ids avalilables for enroll
Each time you executes this enroll script, enrollid is autoincrement for a free number

'''
import FPS, sys
DEVICE_GPIO = '/dev/ttyAMA0'
DEVICE_LINUX = '/dev/cu.usbserial-A601EQ14'
DEVICE_MAC = '/dev/cu.usbserial-A601EQ14'
DEVICE_WINDOWS = 'COM3'
FPS.BAUD = 115200
FPS.DEVICE_NAME = DEVICE_MAC

def LegacyEnroll(fps):
    '''
    Enroll test
    '''

    enrollid=0
    okid=False
    #search for a free enrollid, you have max 200
    while not okid and enrollid < 200:
        okid = fps.CheckEnrolled(enrollid)
        if not okid:
            enrollid+=1
    if enrollid <200:
        #press finger to Enroll enrollid
        print 'Press finger to Enroll %s' % str(enrollid)
        fps.EnrollStart(enrollid)
        while not fps.IsPressFinger():
            FPS.delay(1)
        iret = 0
        if fps.CaptureFinger(True):
            #remove finger
            print 'remove finger'
            fps.Enroll1()
            while not fps.IsPressFinger():
                FPS.delay(1)
            #Press same finger again
            print 'Press same finger again'
            while not fps.IsPressFinger():
                FPS.delay(1)
            if fps.CaptureFinger(True):
                #remove finger
                print 'remove finger'
                fps.Enroll2()
                while not fps.IsPressFinger():
                    FPS.delay(1)
                #Press same finger again
                print 'press same finger yet again'
                while not fps.IsPressFinger():
                    FPS.delay(1)
                if fps.CaptureFinger(True):
                    #remove finger
                    iret = fps.Enroll3()
                    if iret == 0:
                        print 'Enrolling Successfull'
                    else:
                        print 'Enrolling Failed with error code: %s' % str(iret)
                else:
                    print 'Failed to capture third finger'
            else:
                print 'Failed to capture second finger'
        else:
            print 'Failed to capture first finger'
    else:
        print 'Failed: enroll storage is full'

if __name__ == '__main__':
    fps = FPS.FPS_GT511C3(device_name=DEVICE_MAC,baud=115200,timeout=2,is_com=False) #settings for raspberry pi GPIO
    fps.Open()
    if fps.SetLED(True):
        LegacyEnroll(fps)
        fps.SetLED(False)
