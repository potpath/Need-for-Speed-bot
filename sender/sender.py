from nfs.settings import *
import serial

PORT = '/dev/cu.usbmodem14101'
BAUD_RATE = 115200
TIMEOUT = .1


arduino = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)

BL = L.encode('utf8')
BR = R.encode('utf8')


def sendl():
    arduino.write(BL)


def sendr():
    arduino.write(BR)
