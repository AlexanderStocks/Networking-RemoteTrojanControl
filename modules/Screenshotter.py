# use the PyWin32 to make calls to native windows api to grab screenshots

import win32gui
import win32ui
import win32con
import win32api

# get handle to entire desktop window
hdesktop = win32gui.GetDesktopWindow()

width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# create a memory based device context to store image capture
mem_dc = img_dc.CreateCompatibleDC()

# bitmap object
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# copy the screen into the memory device context
mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

screenshot.SaveBitmapFile(mem_dc, "c:\\Users\\Alex\\Desktop\\screenshot.bmp")

mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
