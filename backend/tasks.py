import logging
from celery import Celery
import os
from modules.user_storage import UserStorage
from modules.enhanced_publisher import EnhancedPublisher

# 初始化日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL', 'redis://localhost:6379/0')

celery_app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_BACKEND_URL)

@celery_app.task(bind=True, max_retries=3)
def publish_task(self, user_id, text):
    """
    异步发布任务，调用 EnhancedPublisher 执行发布操作
    """
    try:
        storage = UserStorage(user_id)
        user_data = storage.get_user_data()
        avatar = user_data.get("avatar")
        voice = user_data.get("voice")
        
        publisher = EnhancedPublisher("toutiao")
        publisher.login_and_publish(avatar, voice, text)
        logging.info(f"用户 {user_id} 发布成功")
    except Exception as e:
        logging.error(f"任务执行失败: {e}, 重试次数: {self.request.retries}")
        raise self.retry(countdown=2 ** self.request.retries, exc=e)