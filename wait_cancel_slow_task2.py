# -*- utf-8 -*-
# @Time:  2024/10/26 12:42
# @Autor: Andy Ye
# @File:  wait_cancel_slow_task2.py
# @IDE: PyCharm


import asyncio
import aiohttp
from util import fetch_status


async def main():
    async with aiohttp.ClientSession() as session:
        try:
            # 将协程包装为任务
            api_a = asyncio.create_task(fetch_status(session, 'https://www.example.com'))
            api_b = asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=2))

            # 使用 asyncio.wait 等待任务完成
            done, pending = await asyncio.wait([api_a, api_b], timeout=1)

            # 处理未完成的任务
            for task in pending:
                if task is api_b:
                    print('API B too slow, cancelling')
                    task.cancel()
                    try:
                        await task  # Awaiting ensures that cancellation is processed properly
                    except asyncio.CancelledError:
                        print('API B cancelled successfully')

        except aiohttp.ClientError as e:
            print(f'Request failed: {e}')


asyncio.run(main())

