import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
    RESULT_FOLDER = os.path.join(basedir, 'static/results')
    MODEL_PATH = os.path.join(basedir, 'models/best.pt')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB