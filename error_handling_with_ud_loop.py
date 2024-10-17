# -*- utf-8 -*-
# @Time:  2024/10/17 23:32
# @Autor: Andy Ye
# @File:  error_handling_with_ud_loop.py
# @IDE: PyCharm

class GracefulExit(SystemExit):
    pass

def shutdown():
    raise GracefulExit()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown)
    try:
        loop.run_until_complete(main())
    except GracefulExit:
        loop.run_until_complete(close_echo_tasks(echo_tasks))
    finally:
        loop.close()


async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            # We expect a timeout error here
            pass