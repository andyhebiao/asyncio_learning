# -*- utf-8 -*-
# @Time:  2024/10/20 1:36
# @Autor: Andy Ye
# @File:  oder.py
# @IDE: PyCharm


import asyncio
# 导入asyncio库，用于处理异步I/O操作

# 假设delay函数是一个已经定义好的异步函数，用于模拟延迟操作
from util import delay

async def main():
    """
    主异步函数，用于并发执行多个delay任务，并在所有任务完成后打印结果。

    该函数演示了如何使用asyncio.gather来并发执行多个异步操作，并收集其结果。
    """
    # 使用asyncio.gather并发执行两个delay任务，参数分别为3秒和1秒的延迟
    # 并发意味着这两个任务将同时执行，而不是按顺序等待
    results = await asyncio.gather(delay(3), delay(1))

    # 打印所有完成的任务返回的结果
    print(results)


# 使用asyncio.run来运行主异步函数main
# asyncio.run是Python 3.7+推荐的运行异步程序的首选方式，它会自动创建一个事件循环并运行直到完成
asyncio.run(main())
