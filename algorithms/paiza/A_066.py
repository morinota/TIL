import itertools
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Carender:
    is_horiday_list: List[bool]
    carender_length: int

    @classmethod
    def initialize(cls, start_dates: List[int], end_dates: List[int]) -> "Carender":
        carender_length = max(end_dates)
        return Carender(
            is_horiday_list=[True] * carender_length,
            carender_length=carender_length,
        )

    def update_carender(self, start_date: int, end_date: int) -> None:
        job_date_length = end_date - start_date + 1  # ex) 4日 - 1日 + 1 = 4日間
        start_idx = start_date - 1
        end_idx = end_date - 1

        self.is_horiday_list[start_idx : end_idx + 1] = [False] * job_date_length

    def calc_longest_continuous_work(self) -> int:
        """is_horiday_listを確認し、最も長い、連勤日数を返す"""
        continuous_Falses_list = [
            list(continuous_bools)
            for is_holiday, continuous_bools in itertools.groupby(self.is_horiday_list)
            if not is_holiday
        ]  # is_horiday=Falseの連続した塊を作る.

        continuous_Falses_lengthes = [
            len(continuous_working_days) for continuous_working_days in continuous_Falses_list
        ]  # 各Falseの塊の長さ
        return max(continuous_Falses_lengthes)


class Solver:
    """
    - N 個の仕事を引き受けている.
    - i行目の仕事がi番目に与えられる
    - 最大で連続何日連続出勤しなければならないか
    - 1 ≦ A_i ≦ B_i ≦ 100,000
    - B_i >= A_{i+1}になるケース(i.e. Job同士がoverlapするケース)がある.
    """

    def __init__(self) -> None:
        pass

    def solve(
        self,
        start_dates: List[int],
        end_dates: List[int],
    ) -> int:
        carender_obj = Carender.initialize(start_dates, end_dates)

        # 仕事一件ずつ、カレンダーに書き込む
        for start_date, end_date in zip(start_dates, end_dates):
            carender_obj.update_carender(start_date, end_date)

        # カレンダーを確認し、最も長い連続勤務日数を探す
        return carender_obj.calc_longest_continuous_work()


def main():
    n = int(input())  # 引き受けた仕事の数n
    A_B_list = [tuple(map(int, input().split())) for _ in range(n)]  # 仕事iが始まる日, 仕事iが終わる日
    a_list, b_list = [list(a_or_b) for a_or_b in zip(*A_B_list)]
    print(Solver().solve(start_dates=a_list, end_dates=b_list))


if __name__ == "__main__":
    main()
