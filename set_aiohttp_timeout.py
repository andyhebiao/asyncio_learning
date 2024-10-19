# -*- utf-8 -*-
# @Time:  2024/10/19 16:03
# @Autor: Andy Ye
# @File:  set_aiohttp_timeout.py


import asyncio  # 导入 asyncio 库以支持异步编程
import aiohttp  # 导入 aiohttp 库以便进行异步 HTTP 请求
from aiohttp import ClientSession  # 从 aiohttp 中导入 ClientSession 类以创建会话对象

# 定义异步函数 fetch_status，接受 aiohttp 的 ClientSession 对象和 URL 字符串作为参数
async def fetch_status(session: ClientSession, url: str) -> int:
    """
    异步获取给定 URL 的 HTTP 状态码。

    参数:
    - session: ClientSession 对象，用于发起 HTTP 请求。
    - url: 需要请求的 URL 地址。

    返回:
    - int: HTTP 响应的状态码。
    """
    # 设置一个超时为 10 毫秒的 ClientTimeout 对象
    ten_millis = aiohttp.ClientTimeout(total=0.01)
    # 使用指定的会话和超时发送 GET 请求，并在响应中获取状态码
    async with session.get(url, timeout=ten_millis) as response:
        return response.status  # 返回响应的状态码

# 定义主异步函数 main
async def main():
    """
    主函数，用于演示如何使用 aiohttp 和 asyncio 进行异步 HTTP 请求。
    """
    # 设置一个总超时为 1 秒，连接超时为 0.1 秒的 ClientTimeout 对象
    session_timeout = aiohttp.ClientTimeout(total=1, connect=0.1)
    # 使用指定的超时创建一个新的 ClientSession 对象
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        # 调用 fetch_status 函数获取指定 URL 的状态码
        status_code = await fetch_status(session, 'https://example.com')
        # 打印状态码
        print(f"The status code for 'https://example.com' is: {status_code}")

# 当脚本被直接运行时
if __name__ == "__main__":
    # 运行主异步函数 main
    asyncio.run(main())



import asyncio
from util import async_timed, delay

@async_timed()
async def main() -> None:
    delay_times = [3, 3, 3]
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks]


asyncio.run(main())