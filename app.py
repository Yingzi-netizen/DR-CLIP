import argparse
import json
import os
import shutil
import time
from werkzeug.utils import secure_filename
from flask import render_template, jsonify, url_for, request, Flask
from flask_cors import CORS
from gevent import pywsgi
app = Flask(__name__)
CORS(app)  # 使用 Flask-CORS 简化跨域配置
# 配置文件夹路径
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# 确保文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/get_drawedImage', methods=['POST'])
def anyname_you_like():
    start_time = time.time()
    received_file = request.files.get('input_image')
    if not received_file:
        return jsonify(error="No file uploaded"), 400

    # 检查文件类型
    if not allowed_file(received_file.filename):
        return jsonify(error="Invalid file type"), 400

    # 保存文件到 static 文件夹，命名为 1.png
    image_file_path = os.path.join(UPLOAD_FOLDER, "1.png")
    try:
        received_file.save(image_file_path)
    except Exception as e:
        return jsonify(error=f"Failed to save file: {str(e)}"), 500

    print(f"接收图片文件保存到此路径：{image_file_path}")
    used_time = time.time() - start_time
    print(f"接收图片并保存，总共耗时{used_time:.2f}秒")

    # 返回图片路径
    image_source_url = url_for('static', filename="1.png")
    return jsonify(src=image_source_url)

@app.route('/images', methods=['POST'])
def images():
    start_time = time.time()
    received_file = request.files.get('input_image')
    if not received_file:
        return jsonify(error="No file uploaded"), 400

    # 检查文件类型
    if not allowed_file(received_file.filename):
        return jsonify(error="Invalid file type"), 400

    # 保存文件到 static 文件夹，命名为 1.png
    image_file_path = os.path.join(UPLOAD_FOLDER, "1.png")
    try:
        received_file.save(image_file_path)
    except Exception as e:
        return jsonify(error=f"Failed to save file: {str(e)}"), 500
    return jsonify({
        'data': {
            'list': [
                {
                    'img': url_for('static', filename="1.png"),
                    'description': test1234
                },
            ]
        }
    })

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/album')
def album():
    return render_template('album.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/join')
def join():
    return render_template('join.html')

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8888), app)
    print("服务器已启动！")
    server.serve_forever()