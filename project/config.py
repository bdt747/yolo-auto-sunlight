#存放所有配置函数
import os
#截图区域
monitor = {"top": 97, "left": 301, "width": 2334, "height": 1141}
#创建窗口大小
preview_w = 560
preview_h = 560
#防止鼠标越界报错边距
padding =30
#yolo模型路径（基于脚本位置）
model_path = os.path.join(os.path.dirname(__file__), "runs", "detect", "best.pt")