# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# directx scan codes http://www.flint.jp/misc/?q=dik&lang=en

import ctypes
import time
import scipy.interpolate
import numpy as np
import win32api

SendInput = ctypes.windll.user32.SendInput


W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
U = 0x16
P = 0x19
K = 0x25

UP = 0xC8
DOWN = 0xD0
RIGHT = 0xCD
LEFT = 0xCB
CTRL = 0x9D

ENTER = 0x9C

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))



# mouse functions
def move(x=None, y=None, duration=0.25, absolute=True, interpolate=False, **kwargs):

    if (interpolate):
        print("mouse move {}".format(interpolate))
        current_pixel_coordinates = win32api.GetCursorPos()
        if interpolate:
            current_pixel_coordinates = win32api.GetCursorPos()
            start_coordinates = _to_windows_coordinates(*current_pixel_coordinates)

            end_coordinates = _to_windows_coordinates(x, y)
            print("In interpolate")
            coordinates = _interpolate_mouse_movement(
                start_windows_coordinates=start_coordinates,
                end_windows_coordinates=end_coordinates
            )
            print(coordinates)
        else:
            coordinates = [end_coordinates]

        for x, y in coordinates:
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.mi = MouseInput(x, y, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

            time.sleep(duration / len(coordinates))
    else:
        x = int(x)
        y = int(y)

        coordinates = _interpolate_mouse_movement(
            start_windows_coordinates=(0, 0),
            end_windows_coordinates=(x, y)
        )

        for x, y in coordinates:
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(0), ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

            time.sleep(duration / len(coordinates))


def _to_windows_coordinates(x=0, y=0):
    display_width = win32api.GetSystemMetrics(0)
    display_height = win32api.GetSystemMetrics(1)

    windows_x = (x * 65535) // display_width
    windows_y = (y * 65535) // display_height

    return windows_x, windows_y

def _interpolate_mouse_movement(start_windows_coordinates, end_windows_coordinates, steps=20):
    x_coordinates = [start_windows_coordinates[0], end_windows_coordinates[0]]
    y_coordinates = [start_windows_coordinates[1], end_windows_coordinates[1]]

    if x_coordinates[0] == x_coordinates[1]:
        x_coordinates[1] += 1

    if y_coordinates[0] == y_coordinates[1]:
        y_coordinates[1] += 1

    interpolation_func = scipy.interpolate.interp1d(x_coordinates, y_coordinates)

    intermediate_x_coordinates = np.linspace(start_windows_coordinates[0], end_windows_coordinates[0], steps + 1)[1:]
    coordinates = list(map(lambda x: (int(round(x)), int(interpolation_func(x))), intermediate_x_coordinates))
    return coordinates


def MoveCursor(x, y, x_offset=0, y_offset=0):
    # current_pixel_coordinates = win32api.GetCursorPos()
    # start_coordinates = _to_windows_coordinates(*current_pixel_coordinates)
    x, y  = _to_windows_coordinates(x + x_offset, y+y_offset)
    
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
    
def LeftClick():
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0004, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))





if __name__ == '__main__':
    while (True):
        # PressKey(0x11)
        # time.sleep(1)
        # ReleaseKey(0x11)
        # time.sleep(1)

        # def move(x=None, y=None, duration=0.25, absolute=True, interpolate=False, **kwargs):
        # move(80, 0, iterpolate = False)
        set_pos(10, 0)
        print("MOVE!")
        time.sleep(2)