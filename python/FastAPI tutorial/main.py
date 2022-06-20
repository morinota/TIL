from turtle import st

from hypothesis import example
from fastapi import FastAPI, Query, Path, Body
from enum import Enum
from typing import List, Union, Set, Dict
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl  # strよりも更に特殊な型ヒント(url用)
    name: str


class Item(BaseModel):
    """リクエストボディを受け取る為のクラス?

    Parameters
    ----------
    BaseModel : _type_
        _description_
    """

    name: str
    # description変数は、str or None
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0, description="The price must be greater than zero", example=3.2
    )
    tax: Union[float, None] = None
    tags: Set[str] = set()  # strの集合
    # use the submodel as a type
    images: Union[List[Image], None] = None

    # アプリが受け取る事ができるデータの例を宣言できる！
    # APIドキュメントで使用される。
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    for image in images:
        image.url
    return images


@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),  # パスパラメータ
    q: Union[str, None] = None,  # クエリパラメータ
    item: Union[Item, None] = Body(
        embed=True,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),  # ボディ(オプション)
):
    results = {"item_id": item_id, "item": item}
    return results
