from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    user_name: str
