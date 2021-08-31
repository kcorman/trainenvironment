# This was a test file used on a different raspberry pi
# I'm saving it here just as a reference

import RPi.GPIO as GPIO
import time
import sys

CLOCK = 0.000
pwmPin = 18
SER = 4
RCLK = 17
SRCLK = 27
NUM_BITS =40


GPIO.setmode(GPIO.BCM)
GPIO.setup(SER, GPIO.OUT)
GPIO.setup(RCLK, GPIO.OUT)
GPIO.setup(SRCLK, GPIO.OUT)
print("starting timer")


def writeByte(val):
    GPIO.output(RCLK, GPIO.LOW)
    for i in range(0, NUM_BITS):
        bit = (val >> (NUM_BITS - 1 - i)) & 1
        print("Write bit: " + str(bin(bit)))
        writeSerBit(int(bit))
    time.sleep(CLOCK)
    GPIO.output(RCLK, GPIO.HIGH)


def writeSerBit(bit):
    GPIO.output(SRCLK, GPIO.LOW)
    time.sleep(CLOCK)
    GPIO.output(SER, bit)
    time.sleep(CLOCK)
    GPIO.output(SRCLK, GPIO.HIGH)
    time.sleep(CLOCK)


writeByte(long(sys.argv[1]))

time.sleep(5)