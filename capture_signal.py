# -*- utf-8 -*-
# @Time:  2024/10/16 23:55
# @Autor: Andy Ye
# @File:  capture_signal.py
# @IDE: PyCharm


import asyncio, signal
from asyncio import AbstractEventLoop
from typing import Set
from util import delay


def cancel_tasks():
    print('Got a SIGINT!')
    tasks: Set[asyncio.Task] = asyncio.all_tasks()  # 表示这是一个包含 asyncio.Task 对象的集合，所有运行的任务都会被存储在这个集合中。
    print(f'Cancelling {len(tasks)} task(s).')
    [task.cancel() for task in tasks]


async def main():
    loop: AbstractEventLoop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, cancel_tasks)
    await delay(10)


asyncio.run(main())