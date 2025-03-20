import polars as pl


class Candidate:
    def __init__(self) -> None:
        self.user_col = "session_id"
        self.item_col = "yad_id"

    def generate(self) -> pl.DataFrame:
        pass
