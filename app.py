from flask import Flask, request, jsonify, render_template
import os
import json
from werkzeug.utils import secure_filename
from flask_cors import CORS
from utils.detection import detect_diseases

app = Flask(__name__)
CORS(app)

# 配置
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# 简单用户数据库（实际请换成数据库）
USER_FILE = 'users.json'
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ---------------- 注册和登录接口 ----------------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    if username in users:
        return jsonify({'status': 'fail', 'message': '用户名已存在'}), 400

    users[username] = password
    save_users(users)
    return jsonify({'status': 'success', 'message': '注册成功'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    if users.get(username) == password:
        return jsonify({'status': 'success', 'message': '登录成功'})
    return jsonify({'status': 'fail', 'message': '用户名或密码错误'}), 401

# ---------------- 检测接口不变 ----------------
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

    result = detect_diseases(upload_path, result_path)

    return jsonify({
        'success': True,
        'diseases': result['detections'],
        'result_image': f'/static/results/{filename}'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)












