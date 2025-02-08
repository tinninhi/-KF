import os
import shutil
import logging

USER_DATA_DIR = "user_data"

class UserStorage:
    """管理用户数字人存储，保存头像和语音数据"""

    def __init__(self, user_id):
        self.user_dir = os.path.join(USER_DATA_DIR, str(user_id))
        os.makedirs(self.user_dir, exist_ok=True)
        logging.info(f"创建/检查用户目录: {self.user_dir}")

    def save_avatar(self, image_path):
        target_path = os.path.join(self.user_dir, "avatar.png")
        try:
            shutil.move(image_path, target_path)
            logging.info(f"头像已保存到 {target_path}")
        except Exception as e:
            logging.error(f"保存头像失败: {e}")
            raise
        return target_path

    def save_voice(self, audio_path):
        target_path = os.path.join(self.user_dir, "voice.wav")
        try:
            shutil.move(audio_path, target_path)
            logging.info(f"语音文件已保存到 {target_path}")
        except Exception as e:
            logging.error(f"保存语音文件失败: {e}")
            raise
        return target_path

    def get_user_data(self):
        return {
            "avatar": os.path.join(self.user_dir, "avatar.png"),
            "voice": os.path.join(self.user_dir, "voice.wav")
        }