from playsound import playsound

PIN_ON = 1
PIN_OFF = 0
SOUND_CLICKING="/home/pi/trainenvironment/sounds/click.m4a"
SOUND_SSSH="/home/pi/trainenvironment/sounds/sss.m4a"

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
