import ctypes
import random
import time
import sys

windows32User = ctypes.windll.user32
windows32Kernel = ctypes.windll.kernerl32

numberOfKeystrokes = 0
numberOfMouseClicks = 0
numberOfDoubleClicks = 0


class LastInput(ctypes.Structure):
    _fields_ = [("cbsize", ctypes.c_unit), ("dwTime", ctypes.c_ulong)]


def getLastInput():
    LastInputStruct = LastInput()
    LastInputStruct.cbsize = ctypes.sizeof(LastInput)

    windows32User.GetLastInput(ctypes.byref(LastInputStruct))

    runTime = windows32Kernel.GetTickCount()

    timeElapsed = runTime - LastInputStruct.dwTime

    print("[*] %d milliseconds since the last input event." % timeElapsed)

    return timeElapsed


def getKeyPress():
    global numberOfMouseClicks
    global numberOfKeystrokes

    for i in range(0, 0xff):
        if windows32User.GetAsyncKeyState(i) == -32767:

            # if mouse click
            if i == 0x1:
                numberOfMouseClicks += 1
                return time.time()
            elif 127 > i > 32:
                numberOfKeystrokes += 1

    return None


def detectSandbox():
    global numberOfMouseClicks
    global numberOfKeystrokes

    max_numberOfKeystrokes = random.randint(10, 25)
    max_numberOfMouseClicks = random.randint(5, 25)

    numberOfDoubleClicks = 0
    maxNumberOfDoubleClicks = 10
    doubleClickThreshold = 0.250
    firstDoubleClick = None

    maxInputThreshold = 30000

    previousTimestamp = None
    finishedDetection = False

    lastInput = getLastInput()

    if lastInput >= maxInputThreshold:
        sys.exit(0)

    while not finishedDetection:

        # check for key-presses or mouse-clicks, if value returned then it is the timestamp of when it ocurred
        timeKeyHeldFor = getKeyPress()

        if timeKeyHeldFor is not None and previousTimestamp is not None:

            timeElapsed = timeKeyHeldFor - previousTimestamp

            if timeElapsed <= doubleClickThreshold:
                numberOfDoubleClicks += 1

                if firstDoubleClick is None:
                    firstDoubleClick = time.time()

                else:
                    # seeing if trying to fake out snadbox detction techniques
                    if numberOfDoubleClicks == maxNumberOfDoubleClicks:
                        if timeKeyHeldFor - firstDoubleClick <= (maxNumberOfDoubleClicks * doubleClickThreshold):
                            sys.exit(0)

            if numberOfKeystrokes >= max_numberOfKeystrokes and numberOfDoubleClicks >= maxNumberOfDoubleClicks and numberOfMouseClicks >= max_numberOfMouseClicks:
                return

            previousTimestamp = timeKeyHeldFor

        elif timeKeyHeldFor is not None:
            previousTimestamp = timeKeyHeldFor


detectSandbox()
print("[*] No sandbox detected...")
