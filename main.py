import time
import heapq
import logging
import trainio

TICK_TIME = 0.1

POSSUM_RELAY_PIN = 0
RABBIT_RELAY_PIN = 1
POSSUM_TRIGGER_PIN = 0
RABBIT_TRIGGER_PIN = 1

logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG)

class Event:
    def __init__(self, next_trigger_time, action):
        self.next_trigger_time = next_trigger_time
        self.action = action

class EventQueue:
    def __init__(self):
        self.heap = []

    def peek(self):
        if(len(self.heap) < 1):
            return None
        return self.heap[0][1]
    
    def pop(self):
        item = heapq.heappop(self.heap)
        return item[1]

    def push(self, event):
        item = (event.next_trigger_time, event)
        heapq.heappush(self.heap, item)

class WorldState:
    def __init__(self, event_queue, io):
        self.input_change_subscribers = {}
        self.event_queue = event_queue
        self.input_pin_states = {}
        self.io = io
        for pin in io.get_all_input_pins():
            self.input_change_subscribers[pin] = []

    def get_current_pin_state(self, pin):
        if pin in self.input_pin_states:
            return self.input_pin_states[pin]
        return 0

    def write_pin_state(self, pin, state):
        self.io.write_output_pin_state(pin, state)

    def scan_inputs(self):
        logging.debug("World state scanning all inputs")
        updated_pins = []
        for pin in self.io.get_all_input_pins():
            new_state = self.io.read_input_pin_state(pin)
            past_state = self.get_current_pin_state(pin)
            if(new_state != past_state):
                print("Found changed state for pin " + str(pin))
                updated_pins.append(pin)
            self.input_pin_states[pin] = new_state

        for pin in updated_pins:
            for subscriber in self.input_change_subscribers[pin]:
                print("calling subscriber")
                subscriber()
    
    def subscribe_to_state_change(self, pin_index, subscriber):
        self.input_change_subscribers[pin_index].append(subscriber)
        
class Trigger:
    def __init__(self, name, worldstate, cooldown_duration, trigger_pin, sound):
        self.worldstate = worldstate
        self.name = name
        self.on = False
        self.cooldown_duration = cooldown_duration
        self.cooloff = time.time()
        self.trigger_pin = trigger_pin
        self.sound = sound
        self.subscribe_to_pin_state(trigger_pin)
    
    def fire_trigger(self):
        if(self.worldstate.get_current_pin_state(self.trigger_pin) == trainio.PIN_ON and not self.on and time.time() >= self.cooloff):
            self.on = True
            self.trigger_impl()
            self.cooloff = time.time() + self.cooldown_duration
            self.worldstate.io.play_sound(self.sound)
    
    def trigger_impl(self):
        pass

    def end_impl(self):
        pass

    def end(self):
        self.on = False
        self.end_impl()

    def subscribe_to_pin_state(self, pin_index):
        self.worldstate.subscribe_to_state_change(pin_index, self.fire_trigger)

class TimedRelayTrigger(Trigger):
    def __init__(self, name, worldstate, duration, trigger_pin, drive_pin, cooldown_duration, sound):
        super(TimedRelayTrigger, self).__init__(name, worldstate, cooldown_duration, trigger_pin, sound)
        self.duration = duration
        self.drive_pin = drive_pin

    def start(self):
        self.worldstate.write_pin_state(self.drive_pin, trainio.PIN_ON)

    def end_impl(self):
        self.worldstate.write_pin_state(self.drive_pin, trainio.PIN_OFF)

    def trigger_impl(self):
        self.worldstate.event_queue.push(Event(time.time(), self.start ) )
        self.worldstate.event_queue.push(Event(time.time() + self.duration, self.end ) )

class WigWagRelayTrigger(Trigger):
    def __init__(self, name, worldstate, duration, trigger_pin, drive_pin, cooldown_duration, pulse_interval, pulse_duration, sound):
        super(WigWagRelayTrigger, self).__init__(name, worldstate, cooldown_duration, trigger_pin, sound)
        self.duration = duration
        self.drive_pin = drive_pin
        self.pulse_duration = pulse_duration
        self.pulse_interval = pulse_interval
    
    def reschedule(self):
        if(time.time() < self.end_at):
            self.worldstate.event_queue.push(Event(time.time(), self.do_on) )
            self.worldstate.event_queue.push(Event(time.time() + self.pulse_duration, self.do_off) )
            self.worldstate.event_queue.push(Event(time.time() + self.pulse_interval, self.reschedule) )
        else:
            self.end()
    
    def do_on(self):
        self.worldstate.write_pin_state(self.drive_pin, trainio.PIN_ON)

    def do_off(self):
        self.worldstate.write_pin_state(self.drive_pin, trainio.PIN_OFF)

    def end_impl(self):
        self.do_off()

    def trigger_impl(self):
        self.end_at = time.time() + self.duration
        self.reschedule()

io = trainio.TrainIo()

def setPinState(state):
    print("Set possum pin state: " + str(state))
    io._debug_write_input_pin_state(POSSUM_TRIGGER_PIN, state)


def setRabbitPin(state):
    print("Set rabbit state: " + str(state))
    io._debug_write_input_pin_state(RABBIT_TRIGGER_PIN, state)

def main():
    logging.debug("Starting main")
    eq = EventQueue()
    ws = WorldState(eq, io)
    #trig = TimedRelayTrigger("possum", ws, 3.5, POSSUM_TRIGGER_PIN, POSSUM_RELAY_PIN, 5)
    trig = WigWagRelayTrigger("possum", ws, 6, POSSUM_TRIGGER_PIN, POSSUM_RELAY_PIN, 10, 1, .3, trainio.SOUND_CLICKING)
    trig = TimedRelayTrigger("rabbit", ws, 3, RABBIT_TRIGGER_PIN, RABBIT_RELAY_PIN, 5, trainio.SOUND_SSSH)

    eq.push(Event(time.time() + 1, lambda : setPinState(trainio.PIN_ON)))
    eq.push(Event(time.time() + 4, lambda : setPinState(trainio.PIN_OFF)))
    eq.push(Event(time.time() + 3, lambda : setRabbitPin(trainio.PIN_ON)))
    eq.push(Event(time.time() + 4, lambda : setRabbitPin(trainio.PIN_OFF)))
    eq.push(Event(time.time() + 5, lambda : setRabbitPin(trainio.PIN_ON)))
    eq.push(Event(time.time() + 6, lambda : setRabbitPin(trainio.PIN_OFF)))
    eq.push(Event(time.time() + 12, lambda : setRabbitPin(trainio.PIN_ON)))
    eq.push(Event(time.time() + 15, lambda : setRabbitPin(trainio.PIN_OFF)))

    eq.push(Event(time.time() + 14, lambda : setPinState(trainio.PIN_ON)))
    total_ticks=0
    while(True):
        logging.debug("Running tick " + str(total_ticks))
        total_ticks+=1
        time.sleep(TICK_TIME)
        ws.scan_inputs()
        next_event = eq.peek()
        while(next_event and next_event.next_trigger_time <= time.time()):
            eq.pop()
            logging.debug("Popped an action")
            next_event.action()
            next_event = eq.peek()



if __name__ == "__main__":
    main()
