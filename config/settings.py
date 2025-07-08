# 游戏Agent配置文件

# 游戏相关配置
GAME_SETTINGS = {
    'game_path': '',  # 游戏安装路径
    'screenshot_dir': 'screenshots',  # 截图保存目录
    'log_dir': 'logs',  # 日志保存目录
}

# Agent配置
AGENT_SETTINGS = {
    'debug_mode': False,  # 调试模式
    'auto_retry': True,  # 失败自动重试
    'max_retries': 3,  # 最大重试次数
}