import abc
from email.mime import base
from typing import List, Tuple

import numpy as np
import pandas as pd


class xQuADReranker(abc.ABC):
    def __init__(
        self,
        base_user_item_scores: np.ndarray,
        reaction_logs: pd.DataFrame,
        lambda_param: float,
        xquad_type: str = "binary",
    ) -> None:
        """コンストラクタ
        Parameters
        ----------
        base_user_item_scores : np.ndarray
            元の推薦アルゴリズムから得られた、user*item対のスコア.
            行indexがuser_id, 列indexがitem_idと対応している想定.
            (実際には、{id:idx}のmappingが必要かも.)
        reaction_logs : pd.DataFrame
            過去のreaction log. user_id, item_id, createdの3つのカラムを持つ想定.
            (pd.DataFrameが適切かは相談. 実行環境によってはList[dataclass]の方が良いかも.)
        lambda: float
            再ランキングのスコアリングに設定するパラメータ.
        xquad_type: str
            xQuADにおいてP(i|c, S)の計算方法の指定."binary" or "smooth"
        """
        self.user_item_base_scores = base_user_item_scores
        self.reaction_logs = reaction_logs
        self.lambda_param = lambda_param
        self.xquad_type = xquad_type
        self.short_head_items, self.long_tail_items = self._devide_short_head_and_long_tail()

    def _devide_short_head_and_long_tail(self) -> Tuple[List[int], List[int]]:
        """過去のreaction logを用いて、アイテム達をshort-headとlong-tailに分ける
        返り値は、Tuple[List[short-head item ids], List[long-tail item ids]]
        """
        pass

    def rerank(
        self,
        user_id: int,
        R: List[int],
        S_size: int,
    ) -> List[int]:
        """あるユーザ(user_id)の推薦アイテムリスト(R)に対して、
        long-tail多様性を考慮して、推薦アイテムがS_size個になるようにrerankingする.
        """
        S = []
        for _ in range(S_size):
            candidates = [
                (self.calc_score(user_id, item_id, S), idx) for idx, item_id in enumerate(R) if item_id not in S
            ]
            _, idx = max(candidates, key=lambda t: (t[0], -t[1]))  # スコアが同じならオリジナルのランキングに従う
            S.append(R[idx])
        return S

    def calc_score(self, user_id: int, item_id: int, S: List[int]) -> float:
        """あるユーザのあるアイテムに対する、relank後のスコアを算出して返す."""
        base_score = self.user_item_base_scores[user_id, item_id]  # 論文におけるP(v|u)

        divergence_bonus_score = 0.0
        for c_group_items in [self.short_head_items, self.long_tail_items]:
            c_group_reaction_ratio = self._calc_c_group_reaction_ratio(
                user_id,
                c_group_items,
            )  # 論文中のP(c|u)
            is_item_in_c = 1.0 if item_id in c_group_items else 0  # 論文中のP(C|u)
            c_shortage_in_s = self.calc_c_shortage_in_s(c_group_items, S)
            divergence_bonus_score += c_group_reaction_ratio * is_item_in_c * c_shortage_in_s
        return (1 - self.lambda_param) * base_score + self.lambda_param * divergence_bonus_score

    def _calc_c_group_reaction_ratio(self, user_id: int, c_group_items: List[int]) -> float:
        """ユーザの過去のreactionのうち、
        c_group_items(論文の場合はLong-tail/Short-headなアイテム)の占める割合
        を計算して返す. ユーザの行動がアイテムの人気に素直に従っているか、それとも幅広くイロイロ触れるタイプか、
        を表す. (long-tail promotionのパーソナライズの為.)
        """
        pass

    def calc_c_shortage_in_s(self, c_group_items: List[int], S: List[int]) -> float:
        """「現時点で S にはどの程度 c_group のitem達が不足しているか」を表すスコアを計算する.
        論文中のP(S'|c) = \Pi_{i \in S} (1 - P(i|c, S)).
        - binary xQuADの場合:
            - P(i|c, S) = 1 if i in c else 0
        - smooth xQuADの場合:
            - P(i|c, S) = "リストSの中でCに属するアイテムの割合. (iは関係ない...?)"
        """
        c_shortage_in_s = 1.0  # 論文中のP(S'|c)の初期値
        for item_in_s in S:
            c_shortage_in_s *= 1 - self._calc_p_i_c_S(item_in_s, c_group_items, S)
        return c_shortage_in_s

    def _calc_p_i_c_S(
        self,
        item_id: int,
        c_group_items: List[int],
        S_items: List[int],
    ) -> float:
        if self.xquad_type == "binary":
            return 1.0 if item_id in c_group_items else 0.0

        return (1.0 / len(S_items)) if item_id in c_group_items else 0.0
