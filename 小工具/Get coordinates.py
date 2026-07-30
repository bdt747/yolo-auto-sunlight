import pyautogui as pa
from pynput import mouse

x, y = pa.size()
count = 0
x1 = y1 = x2 = y2 = 0
print(f"你的屏幕分辨率为{x},{y}")

def on_click(px, py, button, pressed):
    global count, x1, y1, x2, y2
    # 判断右键按下
    if button == mouse.Button.right and pressed:
        count += 1
        if count == 1:
            x1, y1 = px, py
            print(f"起点记录成功：({x1},{y1})")
        elif count == 2:
            x2, y2 = px, py
            print(f"起始坐标:({x1},{y1}),结束坐标:({x2},{y2}),宽度为{x2-x1},高度为{y2-y1}")
            # 重置计数器，持续多次选取；如果只想运行一次加上下面这行
            # return False
            count = 0

# 启动鼠标监听
listener = mouse.Listener(on_click=on_click)
listener.start()

# 保持程序常驻
try:
    while True:
        pass
except KeyboardInterrupt:
    listener.stop()