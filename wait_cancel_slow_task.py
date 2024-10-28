# -*- utf-8 -*-
# @Time:  2024/10/25 22:16
# @Autor: Andy Ye
# @File:  wait_cancel_slow_task.py
# @IDE: PyCharm

import asyncio
import aiohttp
from util import fetch_status

async def main():
    async with aiohttp.ClientSession() as session:
        api_a = fetch_status(session, 'https://www.example.com')
        api_b = fetch_status(session, 'https://www.example.com', delay=2)
        done, pending = await asyncio.wait([asyncio.create_task(api_a), asyncio.create_task(api_b)], timeout=1)
        for task in pending:
            if task is api_b:
                print('API B too slow, cancelling')
                task.cancel()

asyncio.run(main())