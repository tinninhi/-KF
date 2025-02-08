from prometheus_client import start_http_server, Counter

# 定义监控指标
PUBLISH_SUCCESS = Counter('publish_success', '成功发布的数量')
PUBLISH_FAILURE = Counter('publish_failure', '失败发布的数量')

def monitor_start():
    # 启动 HTTP 监控端口（例如 8000）
    start_http_server(8000)