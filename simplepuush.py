from pygame import mixer
from Xlib import display
from pyxhook import HookManager
from subprocess import Popen, PIPE
from imgurpython import ImgurClient
from secrets import client_id, client_secret
import pyscreenshot as ImageGrab
import time
import datetime
import uuid

mixer.init()
client = ImgurClient(client_id, client_secret)
x, y, x1, y1 = 0,0,0,0
# Can add multiple keys to this dict to do key combinations (e.g ctrl/shift/4)
keydict = {
    "[0]":False
}


def sound():
    mixer.music.load('sound.mp3')
    mixer.music.play()

def paste(str, p=True, c=True):
    if p:
        p = Popen(['xsel', '-pi'], stdin=PIPE)
        p.communicate(input=str)
    if c:
        p = Popen(['xsel', '-bi'], stdin=PIPE)
        p.communicate(input=str)

def keyboard_event(event):
    global x
    global y
    global x1
    global y1
    global keydict
    for key, value in keydict.iteritems():
        if event.Key == key and event.MessageName == "key down" and not value:
            keydict[key] = True
            data = display.Display().screen().root.query_pointer()._data
            x, y = data["root_x"], data["root_y"]
        elif event.Key == key and event.MessageName == "key up":
            keydict[key] = False
            data = display.Display().screen().root.query_pointer()._data
            x1, y1 = data["root_x"], data["root_y"]
            if x1 < x:
                x1, x = x, x1
                y1, y = y, y1
            img = ImageGrab.grab(bbox=(x, y, x1, y1)) # X1,Y1,X2,Y2
            ss_path = "screenshots/" + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + " " + str(uuid.uuid4())
            img.save(ss_path, "png")
            time.sleep(0.5)
            response = client.upload_from_path(ss_path)
            if response:
                paste(response["link"], False)
                sound()

hook = HookManager()
hook.KeyDown = keyboard_event
hook.KeyUp = keyboard_event
hook.HookKeyboard()
hook.start()
while True:
    time.sleep(0.1)
hook.cancel()