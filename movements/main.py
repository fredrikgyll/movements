from __future__ import annotations

import asyncio
from typing import Any

from fastapi import FastAPI
from ormar.exceptions import ModelError

from movements.database import model_error_handler
from movements.endpoints import api_router
from movements.settings import settings


async def startup(*args: Any, **kwargs: Any) -> None:
    """
    Start-up calls shared by worker and FastAPI app.
    """
    from movements.database import connect_database

    await asyncio.gather(
        asyncio.create_task(connect_database()),
    )


async def shutdown(*args: Any, **kwargs: Any) -> None:
    """
    Shutdown calls shared by worker and FastAPI app.
    """
    from movements.database import disconnect_database

    await asyncio.gather(
        asyncio.create_task(disconnect_database()),
    )


app = FastAPI(
    title=settings.PROJECT_NAME.title(),
    debug=settings.DEBUG,
    exception_handlers={ModelError: model_error_handler},
    on_startup=[startup],
    on_shutdown=[shutdown],
)

app.include_router(api_router)
