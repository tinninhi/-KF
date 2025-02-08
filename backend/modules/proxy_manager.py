import requests
import json
import random
import logging

PROXY_FILE = "data/proxies.json"

class ProxyManager:
    """自动化代理管理"""
    
    def __init__(self):
        self.proxies = self._load_proxies()

    def _load_proxies(self):
        try:
            with open(PROXY_FILE, 'r') as f:
                proxies = json.load(f)
                logging.info(f"加载 {len(proxies)} 个代理")
                return proxies
        except Exception as e:
            logging.error(f"加载代理失败: {e}")
            return []

    def refresh_proxies(self):
        sources = [
            "https://proxy-provider.com/api/get?type=http",
            "https://backup-proxy.com/list"
        ]
        new_proxies = []
        for url in sources:
            try:
                resp = requests.get(url, timeout=10)
                data = resp.json()
                if 'proxies' in data:
                    new_proxies.extend(data['proxies'])
                    logging.info(f"从 {url} 获取 {len(data['proxies'])} 个代理")
                else:
                    logging.warning(f"代理源 {url} 返回数据格式不正确")
            except Exception as e:
                logging.error(f"代理源 {url} 获取失败: {e}")

        self.proxies = new_proxies
        self._save_to_file()

    def _save_to_file(self):
        try:
            with open(PROXY_FILE, 'w') as f:
                json.dump(self.proxies, f)
            logging.info("代理数据已保存")
        except Exception as e:
            logging.error(f"保存代理数据失败: {e}")

    def get_proxy(self):
        if self.proxies:
            proxy = random.choice(self.proxies)
            logging.info(f"选取代理: {proxy}")
            return proxy
        else:
            logging.warning("当前没有可用代理")
            return None