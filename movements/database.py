from datetime import datetime
from typing import TYPE_CHECKING, Any, TypeVar

import ormar
import sqlalchemy
from databases import Database
from fastapi import HTTPException
from ormar.exceptions import NoMatch
from pydantic import BaseModel, NoneStr
from starlette.responses import JSONResponse

from movements.settings import settings

if TYPE_CHECKING:
    from fastapi import Request
    from ormar.exceptions import ModelError


url = settings.DATABASE_URL
database = Database(url=url)

metadata = sqlalchemy.MetaData()


class BaseMeta:
    metadata = metadata
    database = database


T = TypeVar('T', bound=BaseModel)


class ModelBase(ormar.Model):
    id: int = ormar.Integer(autoincrement=True, primary_key=True)
    created_at: datetime = ormar.DateTime(timezone=True, server_default=sqlalchemy.func.now())
    updated_at: datetime = ormar.DateTime(
        timezone=True, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()
    )

    class Meta:
        abstract = True

    @classmethod
    async def get_or_404(cls: type[T], prefetch_related: list[str] | NoneStr = None, **kwargs: Any) -> T:
        qs = cls.objects  # type: ignore[attr-defined]

        if prefetch_related:
            qs = qs.prefetch_related(prefetch_related)

        try:
            return await qs.get(**kwargs)
        except NoMatch:
            raise HTTPException(status_code=404, detail=f'{cls.__name__} not found')

    def __hash__(self) -> int:
        return self.id


async def connect_database() -> None:
    if not database.is_connected:
        await database.connect()


async def disconnect_database() -> None:
    if database.is_connected:
        await database.disconnect()


async def model_error_handler(_: 'Request', exc: 'ModelError') -> JSONResponse:
    """
    Ormar raises ModelErrors in some edge cases on model initialization.
    This handler makes sure we return 422s in those cases, rather than having
    FastAPI return a 500 from an unhandled error.
    Re: https://github.com/collerek/ormar/discussions/353
    """
    return JSONResponse(
        status_code=422, content={'message': f'{exc.__class__.__name__}: {exc}', 'description': 'Model error'}
    )
