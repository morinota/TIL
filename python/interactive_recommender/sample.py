import pandas as pd


def filter_df_by_text_query(query_text: str, df: pd.DataFrame) -> pd.DataFrame:
    query_expression = eval(query_text)  # parse & evaluate str as a python expression
    filtered_df: pd.DataFrame = df.loc[query_expression].copy(deep=True)
    return filtered_df
