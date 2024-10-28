# -*- utf-8 -*-
# @Time:  2024/10/25 0:41
# @Autor: Andy Ye
# @File:  wait_timeout.py
# @IDE: PyCharm

from util import async_timed
import asyncio
from aiohttp import ClientSession
import aiohttp
from util import fetch_status



@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://example.com'
        fetchers = [asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url, delay=3))]
        done, pending = await asyncio.wait(fetchers, timeout=1)
        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)

asyncio.run(main())