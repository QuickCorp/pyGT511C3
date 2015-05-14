pyGT511C3
=========

Python driver for Fingerprint Scanner - TTL (GT-511C3)

https://www.sparkfun.com/products/11792

This is the Python Non Official Version for Sparkfun GT511C3 Fingerprint Scanner

I was made a payment application that uses this fingerprint scanner in a computer version for Windows and Mac and I encountered that Sparkfun don't have a python driver demo or example for this device

I have studied the datasheet 
http://dlnmh9ip6v2uc.cloudfront.net/datasheets/Sensors/Biometric/GT-511C3_datasheet_V1%201_20130411[4].pdf and I have programmed this driver based in standard TTL behavior 


I have been tested with Windows COM3 and /dev/cu.usbserial-A601EQ14 

For /dev/cu.usbserial-A601EQ14 and COM3  you need  an FTDI device that converts the USB protocol to serial commands
More info in:
https://www.sparkfun.com/products/9873

Now supports Raspberry PI GPIO port '/dev/ttyAMA0' too!

If you have any comments or contribution code for this project you are welcome!

NOTE: Please read the LICENSE.txt before to use the code
