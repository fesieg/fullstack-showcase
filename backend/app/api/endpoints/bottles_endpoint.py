from sqlite3 import Connection
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies.validate_token import validate_token
from app.db.db_setup import get_db_conn
from app.models.bottle import Bottle, BottleCreateData
from app.services.bottle_service import (
    add,
    barcode_is_unique,
    get_all,
    get_balance,
    get_unredeemed,
    redeem_all_for_user,
)

bottle_router = APIRouter(
    prefix="/bottles",
    dependencies=[Depends(validate_token)],
    tags=["bottles"],
)


@bottle_router.post("/")
def create_bottle(
    bottle: BottleCreateData,
    conn: Annotated[Connection, Depends(get_db_conn)],
) -> Bottle:
    return add(conn, bottle)


@bottle_router.get("/{user_id}")
def get_all_bottles_for_user(
    user_id: int,
    conn: Annotated[Connection, Depends(get_db_conn)],
) -> list[Bottle]:
    return get_all(conn, user_id)


@bottle_router.get("/unredeemed/{user_id}")
def get_unredeemed_bottles_for_user(
    user_id: int,
    conn: Annotated[Connection, Depends(get_db_conn)],
) -> list[Bottle]:
    return get_unredeemed(conn, user_id)


@bottle_router.get("/balance/{user_id}")
def get_balance_for_user(
    user_id: int,
    conn: Annotated[Connection, Depends(get_db_conn)],
) -> float:
    return get_balance(conn, user_id)


@bottle_router.post("/redeem/{user_id}")
def redeem_all_bottles_for_user(
    user_id: int,
    conn: Annotated[Connection, Depends(get_db_conn)],
) -> float:
    return redeem_all_for_user(conn, user_id)


@bottle_router.post("/validate_barcode/{barcode}")
def validate_barcode(
    barcode: str,
    conn: Annotated[Connection, Depends(get_db_conn)],
) -> bool:
    return barcode_is_unique(conn, barcode)
