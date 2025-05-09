# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid

from yolov11_model.detector import RiceDiseaseDetector

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 初始化模型
detector = RiceDiseaseDetector()

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image_file = request.files['image']
    filename = str(uuid.uuid4()) + '.jpg'
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(image_path)

    # 模型推理
    results = detector.predict(image_path)

    return jsonify({
        'detections': results,
        'image_path': f'{request.host_url}{image_path}'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
