# Link - https://stackoverflow.com/questions/12590942/is-there-any-better-way-to-capture-the-screen-than-pil-imagegrab-grab

import cv2
import numpy as np
import win32gui as wgui
import win32ui as wui
import win32con as wcon
import win32api as wapi

def grab_frame(region = None):

    hwin = wgui.GetDesktopWindow()

    # Setting the value and finding the width and height of frame to grab
    if region:
        left, top, right, bottom = region
        width = right - left + 1
        height = bottom - top + 1
    else:
        width = wapi.GetSystemMetrics(wcon.SM_CXVIRTUALSCREEN)
        height = wapi.GetSystemMetrics(wcon.SM_CYVIRTUALSCREEN)
        left = wapi.GetSystemMetrics(wcon.SM_XVIRTUALSCREEN)
        top = wapi.GetSystemMetrics(wcon.SM_YVIRTUALSCREEN)

    hwindc = wgui.GetWindowDC(hwin)
    srcdc = wui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = wui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), wcon.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    wgui.ReleaseDC(hwin, hwindc)
    wgui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

