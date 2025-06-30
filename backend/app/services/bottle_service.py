from datetime import datetime
from sqlite3 import Connection, Row

from app.models.bottle import Bottle, BottleCreateData


def add(conn: Connection, bottle: BottleCreateData) -> Bottle:
    """Add a new bottle to the database."""
    DEPOSIT_VALUES = {  # noqa: N806
        "plastic": 0.25,
        "glass": 0.50,
        "metal": 0.75,
    }

    deposit_value = DEPOSIT_VALUES.get(bottle.type.value, 0.0)
    current_timestamp = datetime.now()

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO bottles (user_id, barcode, deposit_value, type, brand, added_timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            bottle.user_id,
            bottle.barcode,
            deposit_value,
            bottle.type.value,
            bottle.brand,
            current_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    conn.commit()

    return Bottle(
        id=cursor.lastrowid,
        user_id=bottle.user_id,
        type=bottle.type,
        brand=bottle.brand,
        deposit_value=deposit_value,
        barcode=bottle.barcode,
        redeemed=False,
        added_timestamp=current_timestamp,
    )


def get_all(conn: Connection, user_id: int) -> list[Bottle]:
    """Retrieve all bottles for a user."""
    conn.row_factory = Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM bottles WHERE user_id = ?",
        (user_id,),
    )
    rows = cursor.fetchall()
    return [Bottle(**row) for row in rows]


def get_unredeemed(conn: Connection, user_id: int) -> list[Bottle]:
    """Retrieve all unredeemed bottles for a user."""
    conn.row_factory = Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM bottles WHERE user_id = ? AND redeemed = 0",
        (user_id,),
    )
    rows = cursor.fetchall()
    return [Bottle(**row) for row in rows]


def get_balance(conn: Connection, user_id: int) -> float:
    """Calculate the total value of unredeemed bottles for a user."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(deposit_value) FROM bottles WHERE user_id = ? AND redeemed = 0",
        (user_id,),
    )
    result = cursor.fetchone()[0]
    return result or 0.0


def redeem_all_for_user(conn: Connection, user_id: int) -> float:
    """
    Mark all of a user's bottles as redeemed.

    Returns:
      Total reedemed value, if successful, otherwise 0.0

    """
    cursor = conn.cursor()
    total_redeemable_value = get_balance(conn, user_id)
    cursor.execute("UPDATE bottles SET redeemed = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    return total_redeemable_value


def barcode_is_unique(conn: Connection, barcode: str) -> bool:
    """Check if a barcode already exists in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM bottles WHERE barcode = ?", (barcode,))
    return cursor.fetchone() is None
