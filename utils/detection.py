import cv2
from ultralytics import YOLO
import os

model = None  # 全局加载模型

def load_model(model_path):
    global model
    if model is None:
        model = YOLO(model_path)
    return model

def detect_diseases(image_path, output_path=None):
    """执行病害检测，保存带框的结果图像"""
    model = load_model("models/best.pt")  # 修改为你的模型路径
    results = model(image_path)

    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                'class_id': int(box.cls[0]),
                'class_name': result.names[int(box.cls[0])],
                'confidence': float(box.conf[0]),
                'bbox': box.xyxy[0].tolist()  # [x1, y1, x2, y2]
            })

    # 如果没有传入保存路径，则默认保存到 static/results/ 目录下同名文件
    if output_path is None:
        output_path = os.path.join('static/results', os.path.basename(image_path))

    # 读取原图，绘制检测框和标签
    img = cv2.imread(image_path)
    for det in detections:
        x1, y1, x2, y2 = map(int, det['bbox'])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{det['class_name']} {det['confidence']:.2f}"
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 保存绘制好检测框的图像
    cv2.imwrite(output_path, img)

    return {
        'detections': detections,
        'count': len(detections),
        'result_image_path': output_path  # 返回保存后的图片路径
    }
