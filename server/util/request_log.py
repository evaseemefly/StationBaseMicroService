# 23-12-11 用来记录请求的日志装饰器
from functools import wraps
from starlette.requests import Request

from loguru import logger


def request_log_decorator(func):
    """
        记录请求提的日志
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        log_msg: str = args
        # 获取 request
        request: Request = kwargs.get('request')
        url: str = str(request.url)
        logger.debug(f'接收到请求体为:{url}')
        return await func(*args, **kwargs)

    return wrapper
