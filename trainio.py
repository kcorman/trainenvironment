from playsound import playsound

PIN_ON = 1
PIN_OFF = 0
SOUND_CLICKING="click.m4a"
SOUND_SSSH="sss.m4a"


class TrainIo():
    def __init__(self):
        self.virtual_output_pin_state = 0b00000000
        self.virtual_sound_channel = 0
    
    def read_input_pin_state(self, pin):
        return 0
    
    def write_output_pin_state(self, pin, state):
        self.__set_virtual_output_pin_state(pin, state)

    def set_virtual_sound_channel(self, virtual_channel):
        self.virtual_sound_channel = virtual_channel

    def play_sound(self, filename):
        if(filename != None):
            playsound(filename, False)

    def get_all_input_pins(self):
        return range(0, 2)

    def __set_virtual_output_pin_state(self, virtual_pin_index, state):
        res = self.virtual_output_pin_state
        if(state == 1):
            res = res | (1 << virtual_pin_index)
        else:
            res = res & ~(1 << virtual_pin_index)
        self.virtual_output_pin_state = res
        print("updated virtual output pins:" + bin(self.virtual_output_pin_state))

    def print_state(self):
        print("virtualPins:" + bin(self.virtual_output_pin_state))
        print("virtual_channel:" + self.virtual_sound_channel)

class FakeIo():
    def __init__(self):
        self.virtual_sound_channel = 0
        self.input_pins = {}
        self.output_pins = {}
        for i in range(0, 16):
            self.input_pins[i] = PIN_OFF
            self.output_pins[i] = PIN_OFF
    
    def read_input_pin_state(self, pin):
        return self.input_pins[pin]
    
    def write_output_pin_state(self, pin, state):
        print("Write output pin " + str(pin) + " to state " + str(state))
        self.output_pins[pin] = state
    
    def play_sound(self, filename):
        if(filename != None):
            playsound(filename, False)

    def _debug_write_input_pin_state(self, pin, state):
        self.input_pins[pin] = state

    def set_virtual_sound_channel(self, virtual_channel):
        self.virtual_sound_channel = virtual_channel

    def get_all_input_pins(self):
        return self.input_pins.keys()


    def print_state(self):
        print("virtualPins:" + str(self.output_pins))
        print("virtual_channel:" + self.virtual_sound_channel)
