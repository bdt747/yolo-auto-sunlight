import cv2
import webbrowser
from mss import mss
import numpy as np
import win32gui
import win32con

def empty(a):
    pass
cv2.namedWindow('set color')
cv2.resizeWindow('set color', 640, 240)
cv2.createTrackbar('H_min', 'set color', 0, 179, empty)
cv2.createTrackbar('H_max', 'set color', 179, 179, empty)
cv2.createTrackbar('S_min', 'set color', 0, 255, empty)
cv2.createTrackbar('S_max', 'set color', 255, 255, empty)
cv2.createTrackbar('V_min', 'set color', 0, 255, empty)
cv2.createTrackbar('V_max', 'set color', 255, 255, empty)
while True:
    #获取滑块条
    h_min = cv2.getTrackbarPos('H_min', 'set color')
    h_max = cv2.getTrackbarPos('H_max', 'set color')
    s_min = cv2.getTrackbarPos('S_min', 'set color')
    s_max = cv2.getTrackbarPos('S_max', 'set color')
    v_min = cv2.getTrackbarPos('V_min', 'set color')
    v_max = cv2.getTrackbarPos('V_max', 'set color')

    #读取图片信息 浏览器缩放设置为80%
    img = mss().grab({"top":410,"left":550,"width":950,"height":620})
    img = np.array(img)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)

    #窗口
    cv2.namedWindow('My Window', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('My Window',950, 620)
    cv2.moveWindow('My Window', 1500, 350)
    hwnd = win32gui.FindWindow(None, "My Window")
    # 强制永久置顶
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    cv2.imshow('My Window',mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break