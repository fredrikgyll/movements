from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from movements.database import database
from movements.models import Poop

api_router = APIRouter(prefix='/api')
poop_router = APIRouter(prefix='/poop')
api_router.include_router(poop_router)


@api_router.get('/healthcheck')
async def health_check() -> JSONResponse:
    try:
        time: str = await database.fetch_val("""SELECT datetime('now')""")
        return JSONResponse({'message': f'Database connection working, current time is {time}'})
    except Exception:
        return JSONResponse(status_code=500, content={'message': 'An error occured, database unreachable'})


@poop_router.get('/', response_model=list[Poop])
async def get_poops() -> list[Poop]:
    return await Poop.objects.all()


@poop_router.get('/{id}', response_model=Poop)
async def get_poop(id: int) -> Poop:
    return await Poop.get_or_404(id=id)


class PoopRequest(BaseModel):
    class Config:
        orm_mode = True

    taken_at: datetime


@poop_router.post('/', response_model=Poop)
async def create_poop(poop: PoopRequest) -> Poop:
    return await Poop(**poop.dict()).save()


__all__ = ['api_router']
