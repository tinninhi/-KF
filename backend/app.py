from flask import Flask, request, jsonify
from celery import Celery
import logging
import os

# 初始化日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Celery 配置（可通过环境变量调整）
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL', 'redis://localhost:6379/0')

celery = Celery(app.import_name, broker=CELERY_BROKER_URL, backend=CELERY_BACKEND_URL)

@app.route('/publish', methods=['POST'])
def publish():
    """
    接受 JSON 格式请求，包含 user_id 和 text，
    提交发布任务，返回任务 ID。
    """
    data = request.json
    if not data or 'user_id' not in data or 'text' not in data:
        return jsonify({'error': '缺少必填字段: user_id 和 text'}), 400
    user_id = data['user_id']
    text = data['text']
    try:
        # 从 tasks.py 导入发布任务
        from tasks import publish_task
        result = publish_task.delay(user_id, text)
        return jsonify({'message': '任务已提交', 'task_id': result.id}), 200
    except Exception as e:
        logging.error(f"提交任务失败: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    """
    根据任务 ID 返回任务状态和结果
    """
    result = celery.AsyncResult(task_id)
    return jsonify({
        'task_id': task_id,
        'status': result.status,
        'result': result.result
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """
    健康检查接口，返回系统状态
    """
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
