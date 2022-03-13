from datetime import datetime

import ormar

from movements.database import BaseMeta, ModelBase


class Poop(ModelBase):
    taken_at: datetime = ormar.DateTime(timezone=True)

    class Meta(BaseMeta):
        tablename = 'poops'


__all__ = ['Poop']
