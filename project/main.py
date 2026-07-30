import cv2
import win32gui
import win32con
from config import preview_h,preview_w
from detector import detect_image
from capture import get_screen_frame
from controller import move_mouse_to_target
from pynput import keyboard

#初始化快捷键
auto_aim = False
stop_program = False
def on_key_press(key):
    global auto_aim, stop_program
    try:
        if key.char == 'z':
            auto_aim = True
            print("已开启自动瞄准")
        elif key.char == 'x':
            auto_aim = False
            print("已关闭自动瞄准")
        elif key.char == 'q':
            stop_program = True
            print("准备退出程序")
    except:
        pass
key_listener = keyboard.Listener(on_press=on_key_press)
key_listener.start()


#创建窗口
cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image",preview_w,preview_h)

#窗口置顶
hwnd = win32gui.FindWindow(None, "Image")
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

#主循环
while not stop_program:
    Image = get_screen_frame()
    #Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
    results = detect_image(Image)

    Image_result = results[0].plot()
    if auto_aim and len(results[0].boxes) > 0:
        box = results[0].boxes[0]
        move_mouse_to_target(box)

    cv2.imshow("Image", Image_result)
    cv2.waitKey(1)

# 释放资源
cv2.destroyAllWindows()
key_listener.stop()
print("程序正常退出")