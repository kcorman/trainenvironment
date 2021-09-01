# Defines the main sound handling logic
# this is loosely coupled to the gpio handling class because it
# also needs to set "virtual sound channels" appropriately
# The core idea is that the caller can play a sound on a virtual channel by name
# the caller can also stop sounds by name
import time
import logging
from trainsound import Sound

# logging.basicConfig(level=logging.DEBUG)
# Globally define the sound names to Sound object mappings
ALL_SOUNDS = {
    "test": Sound("sounds/test"),
    "test_left": Sound("sounds/test_left"),
    "test_right": Sound("sounds/test_right"),
    "tmp1": Sound("sounds/tmp1"),
    "tmp2": Sound("sounds/tmp2"),
    #"cave_bats": Sound("sounds/cave_bats"),
    "saloon": Sound("sounds/saloon")
}

class SoundHandler():
    # virtual_sound_channel_mgr is expected to have 2 methods:
    #   enable_virtual_channel(int)
    #   disable_virtual_channel(int)
    #   num_channels : int
    def __init__(self, virtual_sound_channel_mgr):
        self.virtual_sound_channel_mgr = virtual_sound_channel_mgr
        self.active_channels = []
        for i in range(virtual_sound_channel_mgr.num_channels()):
            self.active_channels.append([]) # list of currently in progress sounds in that channel

    # Plays the given named sound on the specified virtual channel
    # if the given sound is already in progress, this will do nothing
    # if another virtual channel is already being used, the new channel will also be enabled but all active channels
    # will play all sounds
    # if virtual_channel is set to None, this will not open any virtual channels (i.e. used for the other real channel that doesn't go through)
    #   virtual channels

    def cleanup_channels(self):
        res = []
        for i in range(len(self.active_channels)):
            active_channel_list = self.active_channels[i]
            # cut list down 
            has_elements = len(active_channel_list) > 0
            if has_elements:
                active_channel_list[:] = [snd for snd in active_channel_list if snd.is_playing()]
                if(len(active_channel_list) == 0):
                    # means we did have elements but now we don't
                    self.virtual_sound_channel_mgr.disable_virtual_channel(i)
                    logging.debug("Disabling virtual sound channel " + str(i) + " because all sounds completed on it")
                else:
                    res.append(i)
        return res
                

    def play_sound(self, name, virtual_channel):
        active_channels=self.cleanup_channels()
        if(not name in ALL_SOUNDS):
            logging.warning("Asked to play sound that doesn't exist in known sounds: " + name)
            return
        sound = ALL_SOUNDS[name]
        if(virtual_channel == None):
            sound.play_next_sound()
        else:
            if(len(active_channels) > 0):
                logging.warning("Playing sound on channel " + str(virtual_channel) + " but found sounds already in progress on channels " + str(active_channels))
            self.virtual_sound_channel_mgr.enable_virtual_channel(virtual_channel)
            sound.play_next_sound()
            logging.debug("adding sound " + name + " to active virtual channel " + str(virtual_channel))
            self.active_channels[virtual_channel].append(sound)
            

if __name__ == "__main__":
    # fake virtual sound chnl mgr
    class ChannelMgr:
        def enable_virtual_channel(self, val):
            pass
        def disable_virtual_channel(self, val):
            pass
        def num_channels(self):
            return 8

    # test out sounds in tmp
    handler = SoundHandler(ChannelMgr())
    #logging.debug("Play sound tmp1 on channel 3")
    #handler.play_sound("tmp1", 3)
    #time.sleep(13)
    #logging.debug("Play sound tmp1 on channel 3")
    #handler.play_sound("tmp1", 3)
    #time.sleep(2)
    #logging.debug("Play sound tmp2 on channel 5")
    #handler.play_sound("tmp2", 5)
    #time.sleep(20)
    #logging.debug("Play sound tmp2 on channel 5")
    #handler.play_sound("tmp2", 1)
    #time.sleep(10)
    logging.debug("Play sound tmp2 on no channel")
    handler.play_sound("tmp2", None)
    time.sleep(10)
    logging.debug("done")

