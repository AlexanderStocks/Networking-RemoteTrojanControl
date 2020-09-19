import ctypes
import random
import time
import sys

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernerl32

keystrokes = 0
mouse_clicks = 0
double_clicks = 0

class LastInputInfo(ctypes.Structure):
    _fields_ = [("cbsize", ctypes.c_unit),
                ("dwTime", ctypes.c_ulong)
                ]


def get_last_input():
    struct_lastinputinfo = LastInputInfo()
    struct_lastinputinfo.cbsize = ctypes.sizeof(LastInputInfo)

    user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))

    run_time = kernel32.GetTickCount()

    elapsed = run_time - struct_lastinputinfo.dwTime

    print("[*] %d milliseconds since the last input event." % elapsed)

    return elapsed

def get_key_press():

    global mouse_clicks
    global keystrokes

    for i in range(0, 0xff):
        if user32.GetAsyncKeyState(i) == -32767:

            # if mouse click
            if i == 0x1:
                mouse_clicks += 1
                return time.time()
            elif 127 > i > 32:
                keystrokes += 1

    return None

def detect_sandbox():

    global mouse_clicks
    global keystrokes

    max_keystrokes = random.randint(10, 25)
    max_mouse_clicks = random.randint(5, 25)

    double_clicks = 0
    max_double_clicks = 10
    double_click_threshold = 0.250
    first_double_click = None

    average_mousetime = 0
    max_input_threshold = 30000

    previous_timestamp = None
    detection_complete = False

    last_input = get_last_input()

    if last_input >= max_input_threshold:
        sys.exit(0)

    while not detection_complete:

        # check for keypresses or mouse-clicks, if value returned then it is the timestamp of when it ocurred
        keypress_time = get_key_press()

        if keypress_time is not None and previous_timestamp is not None:

            elapsed = keypress_time - previous_timestamp

            if elapsed <= double_click_threshold:
                double_clicks += 1

                if first_double_click is None:
                    first_double_click = time.time()

                else:
                    # seeing if trying to fake out snadbox detction techniques
                    if double_clicks == max_double_clicks:
                        if keypress_time - first_double_click <= (max_double_clicks * double_click_threshold):
                            sys.exit(0)

            if keystrokes >= max_keystrokes and double_clicks >= max_double_clicks and mouse_clicks >= max_mouse_clicks:
                return

            previous_timestamp = keypress_time

        elif keypress_time is not None:
            previous_timestamp = keypress_time

detect_sandbox()
print("[*] No sandbox detected...")