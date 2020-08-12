# Done by Frannecklp
import time
import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api

def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)


    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


# returns target window size
def window_pos(target):
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    window = [(hwnd, title) for hwnd, title in winlist if target in title.lower()]
    
    
    if (target == 'fénixao'):
    #     # in a recent update of ao the display doesn't have a name
    #     # so I patched the function for this specific game
        for elem in window:
            if elem[1] == 'FénixAO': 
              wndsize = list(win32gui.GetWindowRect(elem[0]))
              xsize = wndsize[2] - wndsize[0]
              ysize = wndsize[3] - wndsize[1]

        for elem in winlist:
            hwnd = elem[0]
            bbox = list(win32gui.GetWindowRect(hwnd))
            if (bbox[2] - bbox[0] == xsize) and bbox[1] != 0:
                win32gui.SetForegroundWindow(hwnd)
                # print(elem, bbox)
                return bbox
    
    # just grab the hwnd for first window matching fenixao
    window = window[0]
    hwnd = window[0]
    bbox = list(win32gui.GetWindowRect(hwnd))

    return bbox