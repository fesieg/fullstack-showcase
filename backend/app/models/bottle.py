from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class BottleType(str, Enum):
    PLASTIC = "plastic"
    GLASS = "glass"
    METAL = "metal"


class Bottle(BaseModel):
    id: int | None = None
    user_id: int
    type: BottleType
    brand: str
    deposit_value: float
    barcode: str  #  unique
    added_timestamp: datetime
    redeemed: bool = False


class BottleCreateData(BaseModel):
    user_id: int
    type: BottleType
    brand: str
    barcode: str
