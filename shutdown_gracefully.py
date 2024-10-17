# -*- utf-8 -*-
# @Time:  2024/10/17 23:38
# @Autor: Andy Ye
# @File:  shutdown_gracefully.py
# @IDE: PyCharm

import asyncio
from asyncio import AbstractEventLoop
import socket
import logging
import signal
from typing import List


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    '''这个 echo 函数用于处理一个客户端连接：
        使用 loop.sock_recv 异步接收数据，直到没有更多数据（接收每次最多 1024 字节的数据）。
        如果接收到的消息是 "boom\r\n"，它会抛出异常，模拟网络错误。
        如果接收到其他数据，则会将数据通过 loop.sock_sendall 发送回客户端。
        异常被捕获并记录日志，最后无论是否有异常都会关闭连接
        '''
    try:
        while data := await loop.sock_recv(connection, 1024):
            print('got data!')
            if data == b'boom\r\n':
                raise Exception("Unexpected network error")
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()


echo_tasks = []

async def connection_listener(server_socket, loop):
    '''这是一个异步函数，用于监听传入的连接：
    loop.sock_accept 异步接受客户端连接，并返回客户端 connection 和其 address。
    将连接设置为非阻塞模式（connection.setblocking(False)）。
    创建并启动一个新的 echo 任务来处理客户端连接，并将任务添加到 echo_tasks 列表中以便后续管理。
    '''
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")
        echo_task = asyncio.create_task(echo(connection, loop))
        echo_tasks.append(echo_task)



class GracefulExit(SystemExit):
    # 自定义异常 GracefulExit 继承自 SystemExit，用于在关闭服务器时控制程序流。
    pass


def shutdown():
    '''
    当接收到终止信号（如 SIGINT 或 SIGTERM）时，调用 shutdown 函数抛出 GracefulExit 异常以停止事件循环并进入清理阶段。
    '''
    raise GracefulExit()

async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    '''
    close_echo_tasks 异步函数用于在服务器关闭时等待所有活动的 echo 任务完成：
    对于每个 echo_task，使用 asyncio.wait_for(task, 2) 设置 2 秒的超时时间等待任务完成。
    捕获超时异常，因为在关闭期间可能会有任务未能及时完成。
    :param echo_tasks:
    :return:
    '''
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            # We expect a timeout error here
            pass

async def main():
    '''
    main 函数负责启动服务器：
    创建 TCP 服务器 socket，绑定到地址 127.0.0.1:8000，并将其设置为非阻塞模式。
    注册信号处理器，捕捉 SIGINT 和 SIGTERM 信号，当这些信号到来时调用 shutdown 函数。
    调用 connection_listener，开始监听并处理客户端连接。
    :return:
    '''
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)

    await connection_listener(server_socket, loop)

if __name__ == '__main__':
    '''
    创建新的事件循环，并运行 main 函数。
    如果接收到 GracefulExit 异常（例如通过 shutdown 触发），调用 close_echo_tasks 关闭所有 echo 任务。
    最后，确保事件循环被关闭。

    '''
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except GracefulExit:
        loop.run_until_complete(close_echo_tasks(echo_tasks))
    finally:
        loop.close()

'''
总结：
这个代码实现了一个异步的 echo 服务器，每当客户端连接时会启动一个新的任务来处理数据传输。
当收到终止信号时，服务器可以优雅地关闭所有未完成的任务，并避免出现孤立任务或未捕获的异常。
'''