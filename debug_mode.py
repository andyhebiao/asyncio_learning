# -*- utf-8 -*-
# @Time:  2024/10/5 17:40
# @Autor: Andy Ye
# @File:  debug_mode.py
# @IDE: PyCharm


import asyncio
from util import async_timed
@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter


async def main() -> None:
    task_one = asyncio.create_task(cpu_bound_work())
    await task_one

asyncio.run(main(), debug=True)