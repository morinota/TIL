"""Count ソート
- O(n):非常に計算量が少ないソート
- ただその分デメリットもある
- 対象の中で最大の数字(=max_num)を見つける
- 0~max_numまでのリストを用意
    - (maxが100だったら、100個のList用意しないと→リソース消費、弱点)
- 対象内の各indexの数字をカウント→カウントした値(frequency)をリストに入れる
- 今度は、frequencyのListの先頭からの累積値のListを作る
- ＝自分の前に何個数字があるのか＝先頭から数えていくつか
- リストに入れた後はリストの累積値を一つ減らす
- そんなに重要なアルゴリズムでもない
"""

import random
from typing import List

from sort_7_insertion import insertion_sort
from utils import is_in_order


def radix_sort(numbers: List[int]) -> List[int]:
    """countソートを実行する"""
    len_numbers = len(numbers)
    max_num = max(numbers)
    counts = [0] * (max_num + 1)  # カウント用のリスト(最後尾のidx=max_numとする為に長さ+1)
    result = [0] * len_numbers  # 結果用のリスト

    # 対象内の各indexの数字をカウント→カウントした値(frequency)をリストに入れる
    for num in numbers:
        counts[num] += 1

    # count_listの各要素を累積
    accumlated_counts = [0] * (max_num + 1)  # Frequencyの累積値の格納用
    for num_idx in range(1, len(counts)):
        # np.cumsum()を使ってもいいが...
        accumlated_counts[num_idx] = accumlated_counts[num_idx - 1] + counts[num_idx]

    num_idx = len_numbers - 1  # 最後尾のnumから累積値を使ってresultにnumを入れていく
    while num_idx >= 0:
        num = numbers[num_idx]
        result[accumlated_counts[num] - 1] = numbers[num_idx]
        accumlated_counts[num] -= 1  # 累積のfrequencyを-1する
        num_idx -= 1  # 一つ手前の数字へ
    return result


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    sorted_numbers = radix_sort(numbers)
    print(sorted_numbers)
    print(is_in_order(sorted_numbers))
