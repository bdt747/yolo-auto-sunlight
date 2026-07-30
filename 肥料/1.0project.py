import cv2
import numpy as np
import win32gui
import win32con
from ultralytics import YOLO
from mss import MSS
import pyautogui as pa
from pynput import keyboard

# 默认关闭自瞄
#auto_aim = False
#stop_program = False
# 键盘监听回调
def on_key_press(key):
    #global auto_aim, stop_program
    try:
        if key.char == 'z':
            auto_aim = True
            print("✅ 已开启自动瞄准")
        elif key.char == 'x':
            auto_aim = False
            print("❌ 已关闭自动瞄准")
        elif key.char == 'q':
            stop_program = True
            print("🛑 准备退出程序")
    except:
        pass

# 启动全局键盘监听
key_listener = keyboard.Listener(on_press=on_key_press)
key_listener.start()

#初始模型
a1 =YOLO('yolov8n.pt')
#创建窗口和调整大小
cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.resizeWindow("img", 560, 560)
#屏幕捕获
monitor ={"top": 438, "left": 456, "width": 844, "height": 431}
while not stop_program:
    img = MSS().grab(monitor)
    img =np.array(img)
    results = a1(img)
    img_result = results[0].plot()

    if auto_aim and len(results[0].boxes) > 0:
        box = results[0].boxes[0]
        x1, y1, x2, y2 = box.xyxy[0]
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        screen_x = monitor["left"] + center_x
        screen_y = monitor["top"] + center_y
        pa.moveTo(screen_x, screen_y, duration=0.01)
        pa.mouseDown(screen_x, screen_y, duration=0.1)
    #窗口句柄置顶
    hwnd = win32gui.FindWindow(None, "img")
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    cv2.imshow('img',img_result)
    cv2.waitKey(1)

# 收尾释放资源
cv2.destroyAllWindows()
key_listener.stop()
print("程序正常退出")