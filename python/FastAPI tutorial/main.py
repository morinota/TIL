from fastapi import FastAPI, Query, Path, Body
from enum import Enum
from typing import Union
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    """リクエストボディを受け取る為のクラス?

    Parameters
    ----------
    BaseModel : _type_
        _description_
    """

    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),  # パスパラメータ
    q: Union[str, None] = None,  # クエリパラメータ
    item: Union[Item, None] = Body(embed=True),  # ボディ(オプション)
    user: Union[User, None] = None,  # ボディ(オプション)
    importance: int = Body(gt=0)
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
