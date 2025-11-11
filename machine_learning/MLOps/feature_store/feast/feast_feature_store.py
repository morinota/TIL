from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
from feast import FeatureStore

from .feature_store_interface import FeatureStoreInterface


class FeastFeatureStore(FeatureStoreInterface):
    """
    Implementation of FeatureStoreInterface using Feast.
    """

    def __init__(self, repo_path: str):
        self.store = FeatureStore(repo_path=repo_path)

    def apply(self) -> None:
        """
        Apply the feature store configuration.
        """
        self.store.apply()

    def fetch_historical_features(self, entity_df: pd.DataFrame) -> pd.DataFrame:
        """
        Fetch historical features for training or batch scoring.
        """
        return self.store.get_historical_features(entity_df=entity_df).to_df()

    def fetch_online_features(self, entity_rows: List[Dict[str, Any]]) -> Dict[str, List[Any]]:
        """
        Fetch online features for real-time inference.
        """
        return self.store.get_online_features(entity_rows=entity_rows).to_dict()

    def materialize_incremental(self, end_date: datetime) -> None:
        """
        Materialize incremental features into the online store.
        """
        self.store.materialize_incremental(end_date=end_date)

    def push(self, feature_view_name: str, data: pd.DataFrame) -> None:
        """
        Push data to the feature store.
        """
        self.store.push(feature_view_name, data)
