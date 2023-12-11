COMMON_OPTIONS = {
    'LOGGING': {
        'LOG_DIR': r'/opt/project/logs',
        'LOG_FILE': 'logging_{time}.log'
    }
}

# log 存储目录
LOG_DIR: str = COMMON_OPTIONS.get('LOGGING').get('LOG_DIR')
# log 日志文件命名规范
LOG_FILE: str = COMMON_OPTIONS.get('LOGGING').get('LOG_FILE')
