# yolov11_model/detector.py

from ultralytics import YOLO
import os

class RiceDiseaseDetector:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'best.pt')
        self.model = YOLO(model_path)
        self.labels = self.model.names  # 标签索引：{0: 'Blast', 1: 'Blight', 2: 'Brown_Spot'}

    def predict(self, image_path):
        results = self.model(image_path)
        detections = []

        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.labels[cls_id]
                detections.append({
                    'label': label,
                    'confidence': round(conf, 3)
                })

        return detections
