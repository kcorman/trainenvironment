import subprocess
import time

# This is a very thin wrapper around sox's play process and is only designed specifically for this raspbian system
# you must have sox installed for this to work

def play_sound(filename):
    return subprocess.Popen(["play","-q", filename])

def stop_sound(proc_handle):
    if(proc_handle.poll() == 0):
        print("sound already finished, doing nothing")
        return None
    else:
        print("sound is in progress; killing its process")
        return subprocess.Popen(["kill", str(proc_handle.pid)])

def is_finished(proc_handle):
    return proc_handle.poll() == 0
