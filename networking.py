# -*- utf-8 -*-
# @Time:  2024/10/6 21:42
# @Autor: Andy Ye
# @File:  networking.py
# @IDE: PyCharm


import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple
from asyncio import AbstractEventLoop
import asyncio

selector = selectors.DefaultSelector()
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('127.0.0.1', 8000)
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()
selector.register(server_socket, selectors.EVENT_READ)


async def echo(connection: socket.socket, loop: AbstractEventLoop) -> None:
    while data := await loop.sock_recv(connection, 1024):
        if data == b'boom\r\n':
            raise Exception("Unexpected network error")
        await loop.sock_sendall(connection, data)


while True:
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)
    if len(events) == 0:
        print('No events, waiting a bit more!')
    for event, _ in events:
        event_socket = event.fileobj
        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f"I got a connection from {address}")
            selector.register(connection, selectors.EVENT_READ)
        else:
            data = event_socket.recv(1024)
            print(f"I got some data: {data}")
            event_socket.send(data)


tasks = []
async def listen_for_connection(server_socket: socket,loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")
        tasks.append(asyncio.create_task(echo(connection, loop)))


import logging

async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    try:
        # 持续接收数据，直到客户端关闭连接或没有更多数据
        while data := await loop.sock_recv(connection, 1024):
            print('got data!')  # 打印收到的数据通知
            # 检查数据是否为 "boom" 触发异常
            if data == b'boom\r\n':
                raise Exception("Unexpected network error")
            # 将收到的数据回传给客户端
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        # 捕获异常并使用 logging 模块记录异常信息
        logging.exception(ex)
    finally:
        # 无论是否发生异常，最后都关闭连接
        connection.close()
