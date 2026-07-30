import cv2
import numpy as np
from ultralytics import YOLO
from mss import MSS
import win32gui
import win32con
import win32api
from PIL import Image, ImageWin

# ========== 配置参数 ==========
MODEL_PATH = r'C:\Users\T14S\Desktop\yolo2\训练后2\sun_detect\weights\best.pt'
CONF_THRESHOLD = 0.03
CAPTURE_REGION = {"top": 0, "left": 0, "width": 1280, "height": 1600}
# =============================

# 颜色表 (BGR)
COLORS = [
    (0, 255, 0),    # 绿
    (0, 0, 255),    # 红
    (255, 0, 0),    # 蓝
    (0, 255, 255),  # 黄
    (255, 0, 255),  # 紫
    (255, 255, 0),  # 青
]
TRANSPARENT_BGR = (255, 0, 255)   # 紫色 —— 此颜色部分将变为透明
TRANSPARENT_RGB = (255, 0, 255)


def create_overlay(region):
    """创建一个透明覆盖窗口（紫色=透明），返回窗口句柄"""
    hinst = win32gui.GetModuleHandle(None)

    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = lambda h, m, w, l: (
        0 if m in (win32con.WM_PAINT, win32con.WM_ERASEBKGND)
        else win32gui.DefWindowProc(h, m, w, l)
    )
    wc.hInstance = hinst
    wc.lpszClassName = 'YOLO_Overlay'
    win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindowEx(
        win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST,
        wc.lpszClassName, None,
        win32con.WS_POPUP,
        region["left"], region["top"],
        region["width"], region["height"],
        0, 0, hinst, None
    )
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*TRANSPARENT_RGB), 0, win32con.LWA_COLORKEY)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.UpdateWindow(hwnd)
    return hwnd


def draw_detections(hwnd, region, results):
    """在透明覆盖层上绘制检测框（紫色背景自动透明）"""
    h, w = region["height"], region["width"]

    # 用紫色填充背景（紫色部分 = 透明）
    canvas = np.full((h, w, 3), TRANSPARENT_BGR, dtype=np.uint8)

    if results[0].boxes is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        confs = results[0].boxes.conf.cpu().numpy()
        cls_ids = results[0].boxes.cls.cpu().numpy()
        names = results[0].names

        for box, conf, cls_id in zip(boxes, confs, cls_ids):
            x1, y1, x2, y2 = map(int, box)
            color = COLORS[int(cls_id) % len(COLORS)]

            # 矩形框
            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, 2)

            # 标签背景 + 文字
            label = f"{names[int(cls_id)]} {conf:.2f}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(canvas, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
            cv2.putText(canvas, label, (x1 + 2, y1 - 3),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 用 PIL ImageWin.Dib 直接绘制到窗口 DC（避免 win32gui 位图 API 限制）
    hdc = win32gui.GetDC(hwnd)
    try:
        canvas_rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(canvas_rgb)
        dib = ImageWin.Dib(pil_img)
        dib.draw(hdc, (0, 0, w, h))
    finally:
        win32gui.ReleaseDC(hwnd, hdc)


def main():
    model = YOLO(MODEL_PATH)
    hwnd = create_overlay(CAPTURE_REGION)

    with MSS() as sct:
        print("🟢 屏幕检测已启动 | 按 Q 键退出")
        while True:
            img = np.array(sct.grab(CAPTURE_REGION))
            results = model(img, conf=CONF_THRESHOLD)
            draw_detections(hwnd, CAPTURE_REGION, results)

            if win32api.GetAsyncKeyState(ord('Q')) & 0x8000:
                break

    win32gui.DestroyWindow(hwnd)
    print("🛑 已退出")


if __name__ == "__main__":
    main()