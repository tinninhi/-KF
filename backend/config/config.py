import os
import sys
import logging
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

REQUIRED_KEYS = [
    'OPENAI_API_KEY',
    'GENIE_API_KEY',
    'TOUTIAO_USER_1',
    'TOUTIAO_PWD_1'
]

def check_required_env_vars():
    missing_keys = [k for k in REQUIRED_KEYS if not os.getenv(k)]
    if missing_keys:
        logging.error(f" 缺失关键环境变量: {', '.join(missing_keys)}")
        sys.exit(1)

# 程序初始化时检查
check_required_env_vars()