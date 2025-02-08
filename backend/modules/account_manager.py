import json
import os
import time
from datetime import datetime
import logging

ACCOUNT_STATUS_FILE = "data/account_status.json"

class AccountManager:
    """管理账号状态，包括使用频率和健康状况"""

    def __init__(self, accounts):
        """
        :param accounts: dict 格式的账号数据，如：
            {
                "toutiao": [{"username": "user1", ...}, {"username": "user2", ...}],
                "baijia":  [...],
            }
        """
        self.accounts = accounts
        self.account_status = self._load_status()
        self.cooldown_time = 7200  # 2小时冷却
        self.max_daily_uses = 10   # 每日最大使用次数

    def _load_status(self):
        try:
            if os.path.exists(ACCOUNT_STATUS_FILE):
                with open(ACCOUNT_STATUS_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"加载账号状态失败: {e}")
        return {}

    def _save_status(self):
        try:
            with open(ACCOUNT_STATUS_FILE, 'w') as f:
                json.dump(self.account_status, f, indent=2)
        except Exception as e:
            logging.error(f"保存账号状态失败: {e}")

    def get_available_account(self, platform):
        candidates = self.accounts.get(platform, [])
        available = []
        for acc in candidates:
            username = acc['username']
            status = self.account_status.get(username, {})
            today = datetime.now().strftime("%Y-%m-%d")
            daily_uses = status.get(today, 0)
            if daily_uses < self.max_daily_uses and self._check_cooldown(username):
                available.append(acc)

        if not available:
            logging.warning("所有账号达到使用上限或处于冷却中，重置状态")
            self._reset_all_status()
            available = candidates

        selected = min(
            available, 
            key=lambda x: self.account_status.get(x['username'], {}).get(datetime.now().strftime("%Y-%m-%d"), 0)
        )
        self._update_usage(selected['username'])
        logging.info(f"选择账号: {selected['username']}")
        return selected

    def _check_cooldown(self, username):
        status = self.account_status.get(username, {})
        last_used = status.get('last_used', 0)
        return time.time() - last_used > self.cooldown_time

    def _update_usage(self, username):
        today = datetime.now().strftime("%Y-%m-%d")
        status = self.account_status.setdefault(username, {})
status['last_used'] = time.time()
        status[today] = status.get(today, 0) + 1
        self._save_status()

    def _reset_all_status(self):
        self.account_status.clear()
        self._save_status()
        logging.info("已重置所有账号状态")