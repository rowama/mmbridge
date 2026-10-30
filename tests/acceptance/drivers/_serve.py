"""uvicorn on 127.0.0.1 inside the driver's event loop (start on a free or a fixed port, stop, restart)."""
import asyncio

import uvicorn


async def start(app, port: int = 0, lifespan: str = "off"):
    """Serve `app`; returns (server, task, port). A fixed `port` re-binds after stop (relay/tap down -> up)."""
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning",
                                           lifespan=lifespan))
    task = asyncio.create_task(server.serve())
    while not server.started:
        if task.done():
            task.result()
            raise RuntimeError("server exited before start")
        await asyncio.sleep(0.01)
    return server, task, server.servers[0].sockets[0].getsockname()[1]


async def stop(server, task) -> None:
    server.should_exit = True
    await task
