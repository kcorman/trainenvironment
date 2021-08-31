from playsound import playsound
import RPi.GPIO as GPIO
import logging
import time
import sys

PIN_ON = 1
PIN_OFF = 0
CLOCK = 0.001

GPIO.setmode(GPIO.BCM)

# GPIO pin mappings
SER = 4
GPIO.setup(SER, GPIO.OUT)
RCLK = 17
GPIO.setup(RCLK, GPIO.OUT)
SRCLK = 27
GPIO.setup(SRCLK, GPIO.OUT)

SEL_0 = 13
GPIO.setup(SEL_0, GPIO.OUT)
SEL_1 = 25
GPIO.setup(SEL_1, GPIO.OUT)
SEL_2 = 24
GPIO.setup(SEL_2, GPIO.OUT)
SEL_3 = 23
GPIO.setup(SEL_3, GPIO.OUT)
MULTI_INPUT = 26
GPIO.setup(MULTI_INPUT, GPIO.IN)

# End GPIO pin mappings

# Number of multi plexed output bits via using multiple serial to parallel chips daisy chained
NUM_BITS =40

# Number of input bits via parallel to parallel 16 bit multiplexer
NUM_MULTI_INPUT_PINS = 16

# Assumes that the SEL0-4 pins are used to control a parallel multiplexer board that selects from 16 different possible inputs
def writeInputSelect(val):
    assert val >= 0 and val < NUM_MULTI_INPUT_PINS
    #print("Write binary select " + str(bin(val & 0b1111)))
    writeInputSelectBit(SEL_0, val, 0)
    writeInputSelectBit(SEL_1, val, 1)
    writeInputSelectBit(SEL_2, val, 2)
    writeInputSelectBit(SEL_3, val, 3)

def writeInputSelectBit(pin, val, pos):
    bit = (val >> pos) & 1
    GPIO.output(pin, bit)

def readInputBit(pin_num):
    writeInputSelect(pin_num)
    time.sleep(CLOCK) # Might not be necessary
    val = GPIO.input(MULTI_INPUT)
    return val

# Writes serial data of length NUM_BITS to the SER pin
def writeSerialData(val):
    GPIO.output(RCLK, GPIO.LOW)
    for i in range(0, NUM_BITS):
        bit = (val >> (NUM_BITS - 1 - i)) & 1
        writeSerBit(int(bit))
    time.sleep(CLOCK)
    GPIO.output(RCLK, GPIO.HIGH)

# Writes a single serial bit to the SER pin
def writeSerBit(bit):
    logging.debug("Writing serial output data: " + str(bin(bit)))
    GPIO.output(SRCLK, GPIO.LOW)
    time.sleep(CLOCK)
    GPIO.output(SER, bit)
    time.sleep(CLOCK)
    GPIO.output(SRCLK, GPIO.HIGH)
    time.sleep(CLOCK)

class TrainIo():
    def __init__(self):
        self.virtual_output_pin_state = 0b00000000
        self.virtual_sound_channel_state = 0b00000000

    def performTest(self):
        for i in range(NUM_BITS):
            self.write_output_pin_state(i, PIN_OFF)
        time.sleep(1)
        # Go through the lower 8 pins and turn them on
        for i in range(8):
            self.write_output_pin_state(i, PIN_ON)
            time.sleep(.5)
            
        # Go through the lower 8 pins and turn them off
        for i in range(8):
            self.write_output_pin_state(i, PIN_OFF)
            time.sleep(.5)
            
        time.sleep(2)
        # Go through the upper 8 pins and turn them on
        for i in range(8):
            self.write_output_pin_state(i + 32, PIN_ON)
            time.sleep(.5)
            
        # Go through the upper 8 pins and turn them off
        for i in range(8):
            self.write_output_pin_state(i + 32, PIN_OFF)
            time.sleep(.5)

        time.sleep(2)
        # Read the first 8 inputs and pipe the result into the output pins
        for i in range(8):
            val = self.read_input_pin_state(i)
            self.write_output_pin_state(i, val)
            time.sleep(1)
            self.write_output_pin_state(i, PIN_OFF)

        # blink twice to signify end of test
        time.sleep(1)
        for i in range(3): 
            self.write_output_pin_state(0, PIN_ON)
            self.write_output_pin_state(7, PIN_ON)
            time.sleep(.25)
            self.write_output_pin_state(0, PIN_OFF)
            self.write_output_pin_state(7, PIN_OFF)
            time.sleep(.25)

    
    def read_input_pin_state(self, pin):
        return readInputBit(pin)
    
    def write_output_pin_state(self, virtual_pin_index, state):
        assert virtual_pin_index >= 0 and virtual_pin_index <= NUM_BITS
        assert state >= PIN_OFF and state <= PIN_ON

        res = self.virtual_output_pin_state
        if(state == 1):
            res = res | (1 << virtual_pin_index)
        else:
            res = res & ~(1 << virtual_pin_index)
        self.virtual_output_pin_state = res
        logging.debug("updated virtual output pins:" + bin(self.virtual_output_pin_state))
        writeSerialData(self.virtual_output_pin_state)
    
    def get_all_input_pins(self):
        return range(0, NUM_MULTI_INPUT_PINS)

    def set_virtual_sound_channel(self, virtual_channel):
        self.virtual_sound_channel = virtual_channel

    def play_sound(self, filename):
        if(filename != None):
            playsound(filename, False)

    def print_state(self):
        print("virtualPins:" + bin(self.virtual_output_pin_state))
        print("virtual_channel:" + self.virtual_sound_channel)

def main():
    func_type = sys.argv[1]
    if(func_type == "main_test"):
        print("Performing main test")
        v = TrainIo()
        v.performTest()
        print("Testing complete)
    elif(func_type == "output_test"):
        output_pin_index = int(sys.argv[1])
        assert output_pin_index >= 0 and output_pin_index <= NUM_BITS
        v = TrainIo()
        v.write_output_pin_state(output_pin_index, PIN_OFF)
        time.sleep(.5)
        v.write_output_pin_state(output_pin_index, PIN_ON)
        time.sleep(2)
        v.write_output_pin_state(output_pin_index, PIN_OFF)
    elif(func_type == "input_test"):
        input_pin_index = int(sys.argv[1])
        assert input_pin_index >= 0 and input_pin_index <= NUM_MULTI_INPUT_PINS
        v = TrainIo()
        val = v.read_input_pin_state(input_pin_index)
        print("read value: " + str(val) + " from input pin " + str(input_pin_index))


if __name__ == "__main__":
    main()