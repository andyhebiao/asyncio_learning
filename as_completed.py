# -*- utf-8 -*-
# @Time:  2024/10/21 0:02
# @Autor: Andy Ye
# @File:  as_completed.py
# @IDE: PyCharm

import asyncio
from aiohttp import ClientSession
from util import async_timed

import aiohttp

async def fetch_status(session: ClientSession, url: str, delay: int = 0) -> int:
    """
    异步获取给定URL的状态码。

    :param session: ClientSession实例，用于HTTP请求。
    :param url: 需要获取状态码的URL。
    :param delay: 请求前的延迟时间，默认为0秒。
    :return: HTTP请求的状态码。
    """
    # 增加延迟以模拟请求不是立即发生的
    await asyncio.sleep(delay)
    # 发起GET请求并获取结果的状态码
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    """
    主函数，异步获取多个URL的状态码并打印。
    使用asyncio.as_completed以在任务完成后立即处理结果。
    """
    async with aiohttp.ClientSession() as session:
        # 创建三个fetch_status任务，模拟并发请求
        fetchers = [fetch_status(session, 'https://www.example.com', 1),
                    fetch_status(session, 'https://www.example.com', 1),
                    fetch_status(session, 'https://www.example.com', 5)]
        # 使用asyncio.as_completed处理异步任务，以便在任务完成后立即处理
        for done_task in asyncio.as_completed(fetchers, timeout=2):
            # 尝试执行异步任务并处理可能的超时异常
            try:
                # 等待异步任务完成并获取结果
                result = await done_task
                # 打印任务执行结果
                print(result)
            except asyncio.TimeoutError:
                # 处理超时异常
                print('We got a timeout error!')
                # 遍历所有未完成的任务并打印它们
        for task in asyncio.tasks.all_tasks():
            print("===", task)

# 运行主函数
asyncio.run(main())
