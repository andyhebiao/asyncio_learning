# -*- utf-8 -*-
# @Time:  2024/10/20 11:28
# @Autor: Andy Ye
# @File:  gather_exception_pparameter.py
# @IDE: PyCharm

from aiohttp import ClientSession
from util import async_timed, delay,fetch_status
import asyncio
import aiohttp


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https:/ / example .com', 'python:/ / example .com']
        tasks = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*tasks)
        print(status_codes)