from typing import List, Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    """Itemの作成用(request body parameter用?)"""

    pass


class Item(ItemBase):
    """テーブルからデータを取得する時用"""

    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    """Userの作成用(request body parameter用?)"""

    password: str


class User(UserBase):
    """テーブルからデータを取得する時用"""

    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
