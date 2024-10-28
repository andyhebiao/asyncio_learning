# -*- utf-8 -*-
# @Time:  2024/10/23 23:49
# @Autor: Andy Ye
# @File:  wait_exception_handling.py
# @IDE: PyCharm



import asyncio
import logging
import aiohttp
from util import async_timed, fetch_status


# 使用 @async_timed 装饰的主函数，用于测量其执行时间
@async_timed()
async def main():
    # 创建一个 aiohttp 会话，用于进行HTTP请求
    async with aiohttp.ClientSession() as session:
        # 准备一个正确的请求和一个错误的请求
        good_request1 = fetch_status(session, 'https://www.example.com')
        bad_request = fetch_status(session, 'python:///bad')  # 无效的URL，用于演示错误处理

        # 为每个请求创建任务
        fetchers = [asyncio.create_task(good_request1),
                    asyncio.create_task(bad_request)]

        # 等待两个任务完成，将它们分别分类为 done 和 pending
        done, pending = await asyncio.wait(fetchers)

        # 打印完成的任务数量和未完成的任务数量
        print(f'已完成任务数量: {len(done)}')
        print(f'未完成任务数量: {len(pending)}')

        for done_task in done:
            # result = await done_task will throw an exception
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("Request got an exception",
                              exc_info=done_task.exception())

asyncio.run(main())

