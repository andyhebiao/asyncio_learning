# -*- utf-8 -*-
# @Time:  2024/10/17 22:30
# @Autor: Andy Ye
# @File:  await_task_to_shutdown.py
# @IDE: PyCharm

import asyncio
import signal
import time



async def await_all_tasks():
    tasks = asyncio.all_tasks()
    [await task for task in tasks]

async def main():
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT,
    lambda: asyncio.create_task(await_all_tasks()))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
