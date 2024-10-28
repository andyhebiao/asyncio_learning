# -*- utf-8 -*-
# @Time:  2024/10/23 1:04
# @Autor: Andy Ye
# @File:  wait_all_completed.py
# @IDE: PyCharm


import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed
from util import fetch_status

# 使用async_timed装饰器来测量异步函数的执行时间
@async_timed()
async def main():
    """
    主函数，用于异步获取URL状态的示例。
    """
    # 异步创建一个HTTP客户端会话
    async with aiohttp.ClientSession() as session:
        # 创建两个任务，同时获取同一个URL的状态
        fetchers = \
            [asyncio.create_task(fetch_status(session, 'https://example.com')),
             asyncio.create_task(fetch_status(session, 'https://example.com'))]
        # 使用asyncio.wait等待所有任务完成
        done, pending = await asyncio.wait(fetchers)
        # 输出完成的任务数量
        print(f'Done task count: {len(done)}')
        # 输出挂起的任务数量
        print(f'Pending task count: {len(pending)}')
        # 遍历完成的任务，获取结果
        for done_task in done:
            result = await done_task
            print('result', result)
        # 输出任务结果


# 使用asyncio.run运行主函数
asyncio.run(main())
