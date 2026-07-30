#屏幕截取功能
from mss import MSS
import numpy as np
from config import monitor

#捕获画面返回numpy图像数组
def get_screen_frame():
    img = MSS().grab(monitor)
    return np.array(img)