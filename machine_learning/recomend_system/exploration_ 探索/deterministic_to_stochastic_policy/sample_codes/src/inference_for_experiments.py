# sagemaker推論endpointの推論コード
# 4つの必須関数を実装する必要がある
# 初回実行時に呼ばれる処理: model_fn -> input_fn -> predict_fn -> output_fn
# リクエストを受けて呼ばれる処理: input_fn -> predict_fn -> output_fn
import json
from pathlib import Path
from recommender import Recommender
from loader import load_vectors_parquet
from models import Request, Response
from type_aliases import UserId, ContentId, PreferenceScore
from loguru import logger


def model_fn(model_dir: str) -> Recommender:
    """Sagemaker推論エンドポイントの推論コードの必須関数1
    - 初回実行時に呼ばれる。
    - 学習済みモデルをロードして返す。
    """
    model_dir_path = Path(model_dir)
    return Recommender(
        user_vectors=load_vectors_parquet(model_dir_path / "user_vectors"),
        movie_vectors=load_vectors_parquet(model_dir_path / "movie_vectors"),
    )


def input_fn(request_body: str, request_content_type: str) -> Request:
    if request_content_type != "application/json":
        raise ValueError(
            f"Invalid content-type: {request_content_type} (expected: application/json)"
        )
    return Request.model_validate_json(request_body)


def predict_fn(
    input_data: Request, model: Recommender
) -> tuple[UserId, list[tuple[ContentId, PreferenceScore]]]:
    return input_data.user_id, model.predict(
        input_data.user_id,
        input_data.k,
        input_data.inference_type,
    )


def output_fn(
    prediction: tuple[UserId, list[tuple[ContentId, PreferenceScore]]],
    response_content_type: str,
) -> str:
    if response_content_type != "application/json":
        raise ValueError(
            f"Invalid content-type: {response_content_type} (expected: application/json)"
        )

    user_id, recommendations = prediction
    return Response(user_id=user_id, recommendations=recommendations).model_dump_json()
