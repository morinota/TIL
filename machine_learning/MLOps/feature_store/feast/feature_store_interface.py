from abc import ABC, abstractmethod
from typing import Protocol

import polars as pl


# 汎用的な「特徴量定義」型（Feastとは無関係）
class FeatureDefinition(Protocol):
    """特徴量定義オブジェクトのインターフェース"""

    # 必要なら共通メソッドとか（例: nameを持つ）定義できる


class FeatureStoreInterface(ABC):
    """特徴量ストア共通インターフェース"""

    @abstractmethod
    def apply(self, definitions: list[FeatureDefinition]) -> None:
        """特徴量を登録"""
        pass

    @abstractmethod
    def ingest(self, df: pl.DataFrame) -> None:
        """特徴量をオフラインストアに書き込む"""
        pass

    @abstractmethod
    def push(self, feature_view_name: str, df: pl.DataFrame) -> None:
        """特徴量をストアにプッシュ"""
        pass

    @abstractmethod
    def get(self, features: list[str], entity_rows: list[dict[str, object]]) -> pd.DataFrame:
        pass

    @abstractmethod
    def delete(self, project: str) -> None:
        pass
