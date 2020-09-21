# use the PyWin32 to make calls to native windows api to grab screenshots

import win32gui
import win32ui
import win32con
import win32api

# get handle to entire desktop window
desktopHandle = win32gui.GetDesktopWindow()

width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

desktopDC = win32gui.GetWindowDC(desktopHandle)
imageDC = win32ui.CreateDCFromHandle(desktopDC)

# create a memory based device context to store image capture
memoryDC = imageDC.CreateCompatibleDC()

# bitmap object
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(imageDC, width, height)
memoryDC.SelectObject(screenshot)

# copy the screen into the memory device context
memoryDC.BitBlt((0, 0), (width, height), imageDC, (left, top), win32con.SRCCOPY)

screenshot.SaveBitmapFile(memoryDC, "c:\\Users\\Alex\\Desktop\\screenshot.bmp")

memoryDC.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
