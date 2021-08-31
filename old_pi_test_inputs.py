# This was a test file used on a different raspberry pi
# I'm saving it here just as a reference

import RPi.GPIO as GPIO
import time
import sys

SEL_0 = 13
SEL_1 = 25
SEL_2 = 24
SEL_3 = 23
INPUT = 26


GPIO.setmode(GPIO.BCM)
GPIO.setup(SEL_0, GPIO.OUT)
GPIO.setup(SEL_1, GPIO.OUT)
GPIO.setup(SEL_2, GPIO.OUT)
GPIO.setup(SEL_3, GPIO.OUT)
GPIO.setup(INPUT, GPIO.IN)

def writeBit(pin, val, pos):
    bit = (val >> pos) & 1
    GPIO.output(pin, bit)

def writeByte(val):
    #print("Write binary select " + str(bin(val & 0b1111)))
    writeBit(SEL_0, val, 0)
    writeBit(SEL_1, val, 1)
    writeBit(SEL_2, val, 2)
    writeBit(SEL_3, val, 3)

def readPos(pos):
    writeByte(pos)
    time.sleep(0.001)
    val = GPIO.input(INPUT)
    return val


while(True):
    for i in range(3):
        val = readPos(i)
        print("Read at position " + str(i) + ", val="+str(val))
        time.sleep(0.001)
    time.sleep(1)