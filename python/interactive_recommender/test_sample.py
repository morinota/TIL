import numpy as np
import pandas as pd
from sample import filter_df_by_text_query


def test_filter_df_by_text_query() -> None:
    df = pd.DataFrame(
        {
            "column1": [1, 2, 3, 4],
            "column2": ["a", "b", "c", "d"],
        }
    )
    filter_query = "df['column1'] >= 3"

    filtered_df_expected = pd.DataFrame(
        {
            "column1": [3, 4],
            "column2": ["c", "d"],
        }
    )
    filtered_df_actual = filter_df_by_text_query(filter_query, df)

    assert filtered_df_actual.values.tolist() == filtered_df_expected.values.tolist()
