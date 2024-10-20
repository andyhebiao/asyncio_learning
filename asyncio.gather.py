# -*- utf-8 -*-
# @Time:  2024/10/20 1:27
# @Autor: Andy Ye
# @File:  asyncio.gather.py
# @IDE: PyCharm


import asyncio
import aiohttp
from util import fetch_status
from util import async_timed

# 定义主异步函数，使用async_timed装饰器测量函数执行时间
@async_timed()
async def main():
    """
    主函数，用于异步获取一组URL的状态码并打印。
    使用aiohttp库创建一个异步客户端会话，批量发送HTTP请求。
    """
    # 创建一个异步客户端会话
    async with aiohttp.ClientSession() as session:
        # 生成1000个相同的URL
        urls = ['https://example.com' for _ in range(1000)]
        # 为每个URL创建一个fetch_status任务
        requests = [fetch_status(session, url) for url in urls]
        # 并发执行所有fetch_status任务，并等待它们全部完成
        status_codes = await asyncio.gather(*requests)
        # 打印所有URL的状态码
        print(status_codes)

# 使用asyncio.run运行主异步函数
asyncio.run(main())
