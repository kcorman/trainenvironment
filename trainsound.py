# Defines a Sound that rotates through multiple files
# these files are mutually exclusive. If a sound is in progress and play is called again, nothing will happen
from os import listdir
from os.path import isfile, join
import time
import logging
import random
import simple_sound_lib

class Sound:
    def __init__(self, dirname):
        # name of directory that the sounds reside in
        self.dirname = dirname
        self.update_known_files()
        self.curr_sound_handle = None

    def update_known_files(self):
        self.files = [f for f in listdir(self.dirname) if isfile(join(self.dirname, f))]
        if(len(self.files) < 1):
            print("sound with dir " + self.dirname + " has no files found in the directory")
        else:
            print("sound with dir " + self.dirname + " found files " + str(self.files))
        self.file_index = random.randrange(len(self.files))

    def num_files(self):
        return len(self.files)

    def next_file(self):
        if(self.num_files() < 1):
            return None
        self.file_index = (self.file_index + 1) % self.num_files()
        return self.files[self.file_index] 

    def is_playing(self):
        if(self.curr_sound_handle == None):
            return False
        return not simple_sound_lib.is_finished(self.curr_sound_handle)

    def play_next_sound(self):
        if(self.is_playing()):
            print("play_next_sound invoked for sound " + self.dirname + " but sound is already in progress")
        else:
            print("Going to play next sound since none is in progress for sound " + self.dirname)
            f = self.next_file()
            self.curr_sound_handle = simple_sound_lib.play_sound(join(self.dirname, f))

    def stop_current_sound(self):
        if(self.curr_sound_handle != None):
            simple_sound_lib.stop_sound(self.curr_sound_handle)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # test out sounds in tmp
    snd = Sound("./sounds/tmp/")
    while(True):
        snd.play_next_sound()
        while(snd.is_playing()):
            print("sound still playing, waiting...")
            time.sleep(1)
        print("sound done")
