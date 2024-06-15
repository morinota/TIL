import numpy as np
from pydantic import BaseModel, PlainSerializer, PlainValidator, validator
from typing import Annotated, Any
from patito import Model
import polars as pl
import pandera.polars as pa


def validate_ndarray(x: np.ndarray) -> np.ndarray:
    """np.ndarray型かを検証する関数"""
    if not isinstance(x, np.ndarray):
        raise ValueError("numpy.ndarray型である必要があります")
    return x


def serialize_ndarray(x: np.ndarray) -> list:
    """ndarrayをリストに変換する関数"""
    return x.tolist()


# validationとserializationの方法を定義した、カスタム型を定義
NdArray = Annotated[
    np.ndarray,
    PlainValidator(validate_ndarray),  # 無名関数lambdaでもOK
    PlainSerializer(serialize_ndarray),
]


# # patitoのモデルクラスは、これだけだと`PydanticInvalidForJsonSchema`になっちゃう。
class ImageRecord(Model):
    id: int
    vector: list[float]


class MySchema(pa.DataFrameModel):
    id: int = pa.Field(unique=True)
    vector: list[float]


#     x: np.ndarray

#     @validator("x", pre=True, always=True)
#     def validate_ndarray(cls, v: np.ndarray) -> np.ndarray:
#         if not isinstance(v, np.ndarray):
#             raise ValueError("numpy.ndarray型である必要があります")
#         return v

#     def json(self, **kwargs) -> str:
#         obj_dict = self.model_dump(**kwargs)
#         obj_dict["x"] = obj_dict["x"].tolist()  # Convert numpy array to list
#         return super().model_dump_json(**obj_dict)

#     class Config:
#         arbitrary_types_allowed = True


if __name__ == "__main__":
    # df = pl.DataFrame(
    #     [
    #         {"id": 1, "vector": np.array([1.0, 2.0, 3.0])},
    #         {"id": 2, "vector": np.array([4.0, 5.0, 6.0])},
    #     ]
    # )
    df = pl.DataFrame(
        {
            "id": [1, 2],
            "vector": [np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0])],
        }
    )
    for row in df.iter_rows(named=True):
        vec = row["vector"]
        print(vec)
        print(type(vec))
    # ImageRecord.validate(df)

    # Schema.validate(df)
    print(ImageRecord(id=1, vector=[1.0, 2.0, 3.0]))
    # MySchema(id=1, vector=[1.0, 2.0, 3.0])

    print(df)
