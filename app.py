from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from utils.detection import detect_diseases

app = Flask(__name__)
CORS(app)  # 支持跨域请求

# 配置
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大16MB

# 创建上传和结果目录
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/flutter_detect', methods=['POST'])
def flutter_detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400

    filename = f"flutter_{secure_filename(file.filename)}"
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    result_path = os.path.join(app.config['RESULT_FOLDER'], filename)
    file.save(upload_path)

    # 执行检测（你的detect_diseases中需要保存结果图像）
    result = detect_diseases(upload_path, result_path)

    return jsonify({
        'success': True,
        'diseases': result['detections'],  # 返回检测框/标签/置信度信息
        'result_image': f'/static/results/{filename}'  # 返回图片相对路径，Flutter用它显示图像
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
