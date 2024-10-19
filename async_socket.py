# -*- utf-8 -*-
# @Time:  2024/10/7 14:00
# @Autor: Andy Ye
# @File:  async_socket.py


import asyncio
import socket
from asyncio import AbstractEventLoop

async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    """
    Handle echo service for a single connection.

    This function continuously receives data from the connection and sends it back until the connection is closed.

    :param connection: Client connection socket
    :param loop: Event loop
    """
    try:
        while data := await loop.sock_recv(connection, 1024):
            await loop.sock_sendall(connection, data)
    finally:
        connection.close()

async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    """
    Listen for new client connections.

    Once a new client connects, a task is created to handle the echo service for that connection.

    :param server_socket: Server listening socket
    :param loop: Event loop
    """
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")
        asyncio.create_task(echo(connection, loop))

async def main():
    """
    Main function to start the server.

    Initializes the server socket, sets it to non-blocking mode, and binds to the specified address.
    Then, it listens for new client connections and handles them with the echo service.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    await listen_for_connection(server_socket, asyncio.get_event_loop())

# Start the asyncio event loop and run the main coroutine
asyncio.run(main())

