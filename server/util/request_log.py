# 23-12-11 用来记录请求的日志装饰器
import datetime
from functools import wraps
from starlette.requests import Request

from loguru import logger


def request_timer_consuming_decorator(func):
    """
        记录请求提的日志
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        url: str = ''
        # TODO:[-] 23-12-11 注意 old 不要放在 wrapper 方法外侧，装饰器方法在首次加载时会执行request_log_decorator ，但不会执行 wrapper 方法
        old: float = datetime.datetime.now().timestamp()
        # 获取 request
        request: Request = kwargs.get('request')
        url = str(request.url)
        # logger.debug(f'接收到请求体为:{url}')
        res = await func(*args, **kwargs)
        now: float = datetime.datetime.now().timestamp()
        timer_consuming: float = now - old
        timer_consuming_str: str = '%.2f' % timer_consuming
        logger.debug(f'当前任务:{url},耗时:{timer_consuming_str}')
        return res

    return wrapper


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
