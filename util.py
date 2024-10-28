# -*- utf-8 -*-
# @Time:  2024/10/4 10:05
# @Autor: Andy Ye
# @File:  util.py.py
# @IDE: PyCharm


import functools
import time
from typing import Callable, Any
import asyncio
from aiohttp import ClientSession

def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'starting {func} with args {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'finished {func} in {total:.4f} second(s)')
        return wrapped
    return wrapper


async def delay(delay_seconds: int) -> int:
    """
    异步延迟函数，用于模拟异步等待场景。

    此函数的主要目的是演示如何在异步环境中使用await来实现延迟执行。
    它首先打印一条消息指示即将进入睡眠状态以及睡眠时长，然后使用await来等待指定的秒数，
    最后打印一条消息指示睡眠结束，并返回睡眠时长。

    参数:
    delay_seconds: int - 指定的睡眠秒数。

    返回值:
    int - 返回睡眠的秒数，这是函数执行结束后的一个结果。
    """
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds



async def fetch_status(session: ClientSession, url: str, delay: int = 0) -> int:
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status