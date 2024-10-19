# -*- utf-8 -*-
# @Time:  2024/10/19 0:05
# @Autor: Andy Ye
# @File:  async_context.py
# @IDE: PyCharm


import asyncio
import socket
from types import TracebackType
from typing import Optional, Type

class ConnectedSocket:
    """
    一个用于异步管理socket连接的上下文管理器类。

    参数:
    - server_socket: 用于接受连接请求的服务器socket对象。
    """
    def __init__(self, server_socket):
        self._connection = None
        self._server_socket = server_socket

    async def __aenter__(self):
        """
        异步上下文管理器的__aenter__方法，用于在进入上下文时自动执行。
        它等待并接受一个连接请求，然后返回这个连接。
        """
        print('Entering context manager, waiting for connection')
        loop = asyncio.get_event_loop()
        connection, address = await loop.sock_accept(self._server_socket)
        self._connection = connection
        print('Accepted a connection')
        return self._connection

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ):
        """
        异步上下文管理器的__aexit__方法，用于在退出上下文时自动执行。
        它关闭当前连接。

        参数:
        - exc_type: 异常类型（如果有异常发生）。
        - exc_val: 异常值（如果有异常发生）。
        - exc_tb: 异常的traceback（如果有异常发生）。
        """
        print('Exiting context manager')
        self._connection.close()
        print('Closed connection')


async def main():
    """
    主函数，用于设置服务器socket，创建ConnectedSocket实例，并接收数据。
    """
    loop = asyncio.get_event_loop()
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    # 使用ConnectedSocket上下文管理器来处理连接
    async with ConnectedSocket(server_socket) as connection:
        data = await loop.sock_recv(connection, 1024)
        print(data)


asyncio.run(main())

