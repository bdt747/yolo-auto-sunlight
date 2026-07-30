#yolo检测
from ultralytics import YOLO
from config import model_path

#加载模型
model = YOLO(model_path)
def detect_image(img):
    results = model.predict(source=img,classes=[0])#可以修改模型设别的物品
    draw_img = results[0].plot()
    return results
