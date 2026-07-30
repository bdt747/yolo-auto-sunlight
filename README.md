# 基于YOLO模型的自动收集阳光 ☀️

使用 YOLOv8 目标检测模型实现的自动收集阳光工具（植物大战僵尸）。

素材用的这个：https://gamefunbar.com/zh-cn/game/plants-vs-zombies/
（侵删）

## 项目结构

```
project/
├── main.py          # 主程序入口
├── capture.py       # 屏幕截图/画面捕获
├── detector.py      # YOLO 模型检测
├── controller.py    # 鼠标/键盘控制
├── config.py        # 配置文件
├── data.yaml        # 数据集配置
├── yolov8n.pt       # YOLOv8 轻量模型
├── yolov8s.pt       # YOLOv8 小模型
└── runs/detect/
    └── best.pt      # 训练好的最佳模型

小工具/
├── Get color.py         # 取色工具
├── Get coordinates.py   # 获取坐标工具
└── yolov8官方类别id对照表

肥料/
├── 1.0project.py        # 早期版本
└── 绘制检测框.py        # 绘制检测框工具

训练材料/
└── classes.txt          # 类别标签
```

## 使用说明

1. 安装依赖：`pip install ultralytics opencv-python pyautogui`
2. 运行主程序：`python project/main.py`

## 模型说明

- `yolov8n.pt` - YOLOv8 nano 模型（6.3MB），速度快
- `yolov8s.pt` - YOLOv8 small 模型（21.5MB），精度更高
- `best.pt` - 自定义训练的最佳模型（6.0MB）
