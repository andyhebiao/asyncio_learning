# -*- utf-8 -*-
# @Time:  2024/10/19 22:53
# @Autor: Andy Ye
# @File:  asyncio_concurrent_task.py
# @IDE: PyCharm



import asyncio
from util import async_timed, delay

@async_timed()
async def main() -> None:
    delay_times = [3, 3, 3]
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    await asyncio.gather(*tasks)

asyncio.run(main())
