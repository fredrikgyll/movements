from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from movements.models import Poop

poop_router = APIRouter(prefix='/poop')


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


api_router = APIRouter(prefix='/api')
api_router.include_router(poop_router)

__all__ = ['api_router']
