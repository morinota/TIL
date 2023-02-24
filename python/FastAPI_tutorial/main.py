from enum import Enum
from turtle import st
from typing import Dict, List, Set, Union

from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl  # strよりも更に特殊な型ヒント(url用)
    name: str


class Item(BaseModel):
    """リクエストボディを受け取る為のクラス?"""

    name: str = Field(example="Foo")
    # description変数は、str or None
    description: Union[str, None] = Field(
        default=None,
        example="A very nice Item",
        title="The description of the item",
        max_length=300,
    )
    price: float = Field(gt=0, description="The price must be greater than zero", example=35.4)
    tax: Union[float, None] = Field(default=None, example=3.2)
    tags: Set[str] = set()  # タグはユニークな文字列であるべきなのでset
    # use the submodel as a type
    images: Union[List[Image], None] = None

    # アプリがreceiveできるデータのexampleを宣言できる！APIドキュメントで参照される.
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "Foo",
    #             "description": "A very nice Item",
    #             "price": 35.4,
    #             "tax": 3.2,
    #         }
    #     }


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[Item]


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


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    for image in images:
        image.url
    return images


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer
