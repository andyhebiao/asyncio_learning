# -*- utf-8 -*-
# @Time:  2024/10/19 14:54
# @Autor: Andy Ye
# @File:  web_request_with_aiohttp.py


import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed

# 使用装饰器测量异步函数执行时间
@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    """
    异步获取给定URL的HTTP状态码。

    参数:
    - session: aiohttp的ClientSession实例，用于发起HTTP请求。
    - url: 需要请求的URL地址。

    返回:
    - int: HTTP响应状态码。
    """
    async with session.get(url) as response:
        return response.status

# 使用装饰器测量异步函数执行时间
@async_timed()
async def main():
    """
    主函数，用于驱动整个程序的执行。
    - 创建aiohttp的ClientSession实例。
    - 定义目标URL。
    - 调用fetch_status函数获取HTTP状态码。
    - 打印URL及其状态码。
    """
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'
        status = await fetch_status(session, url)
        print(f'Status for {url} was {status}')

# 使用asyncio.run来运行主函数
if __name__ == '__main__':
    asyncio.run(main())
