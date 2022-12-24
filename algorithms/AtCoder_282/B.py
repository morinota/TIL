from collections import deque
from typing import List

import numpy as np

"""
- 1 以上 N 以下の整数 i 
- 1 以上 M 以下の整数 j 

"""


class Hogehoge:
    def __init__(self) -> None:
        pass

    def hogehoge(self, person_num: int, question_num: int, str_list: List[str]) -> int:

        good_pair_num = 0
        for i in range(person_num):
            results_i = str_list[i]  # ex) xxooo
            results_i_int = self._convert_results_str_to_list(str_list[i])

            for j in range(person_num):
                if i == j:
                    continue
                results_j_int = self._convert_results_str_to_list(str_list[j])

                if self._judge_all_clear(
                    results_i=results_i_int,
                    results_j=results_j_int,
                    question_num=question_num,
                ):
                    good_pair_num += 1

        return good_pair_num

    def _convert_results_str_to_list(self, results_i_str: str) -> List[int]:
        lookup = {"x": 0, "o": 1}  # ex) xxooo
        return [lookup[res] for res in results_i_str]

    def _judge_all_clear(
        self,
        results_i: List[int],
        results_j: List[int],
        question_num: int,
    ) -> bool:
        for q_idx in range(question_num):
            res_i = results_i[q_idx]
            res_j = results_j[q_idx]
            if res_i + res_j < 1:
                return False

        return True


if __name__ == "__main__":
    n, m = map(int, input().split())
    str_list = [input() for _ in range(n)]
    hogehoge_obj = Hogehoge()
    print(int(hogehoge_obj.hogehoge(person_num=n, question_num=m, str_list=str_list) / 2))
