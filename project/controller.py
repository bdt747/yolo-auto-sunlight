#鼠标控制
import pyautogui as pa
import random
from config import monitor

def move_mouse_to_target(box):

    x1, y1, x2, y2 = box.xyxy[0]
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    screen_x = monitor["left"] + center_x
    screen_y = monitor["top"] + center_y
    pa.moveTo(screen_x, screen_y, duration=0.05)
    #pa.mouseDown (duration=0.5)