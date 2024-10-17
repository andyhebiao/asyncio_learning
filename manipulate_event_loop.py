# -*- utf-8 -*-
# @Time:  2024/10/5 16:52
# @Autor: Andy Ye
# @File:  manipulate_event_loop.py
# @IDE: PyCharm


import asyncio
from util import delay



def call_later():
    print("I'm being called in the future!")


async def main():
    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(5)


asyncio.run(main())