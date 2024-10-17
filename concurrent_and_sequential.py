# -*- utf-8 -*-
# @Time:  2024/10/5 17:22
# @Autor: Andy Ye
# @File:  concurrent_and_sequential.py
# @IDE: PyCharm


from util import delay
import asyncio


async def main():
	sleep_for_three = asyncio.create_task(delay(3))
	sleep_again = asyncio.create_task(delay(4))
	sleep_once_more = asyncio.create_task(delay(5))
	# await sleep_for_three
	# await sleep_again
	# await sleep_once_more


asyncio.run(main())


# async def main():
# 	await delay(3)
# 	await delay(4)
# 	await delay(5)
#
#
# asyncio.run(main())