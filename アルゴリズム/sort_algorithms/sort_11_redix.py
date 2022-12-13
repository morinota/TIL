"""Radixソート
- Counting sortを活用したソートアルゴリズム
- まずは一の位だけをみて並びかえる→counting sortを行う
- Counting sortは安定ソート => 順番は変わらない
- 一、十、百の位...と分けて、繰り返しcounting sortしていく
"""

import random
from typing import List

from utils import is_in_order


def counting_sort_for_radix(numbers: List[int], place: int) -> List[int]:
    counts = [0] * 10  # カウント用のリスト(idx = 0 ~ 9)
    result = [0] * len(numbers)  # 結果用のリスト

    # frequencyを計算
    for num in numbers:
        place_value_in_num = int(num / place) % 10  # 余りを計算=>place桁を取得
        counts[place_value_in_num] += 1

    # 上からの累積値を計算
    accululated_counts = [0] * len(counts)
    for place_value in range(10):  # 0 ~ 9
        print(place_value)
        accululated_counts[place_value] = accululated_counts[place_value - 1] + counts[place_value]

    # 累積値を使ってソート
    num_idx = len(numbers) - 1  # 最後尾から見ていく
    while num_idx >= 0:
        place_value_in_num = int(numbers[num_idx] / place) % 10
        result[accululated_counts[place_value_in_num] - 1] = numbers[num_idx]
        accululated_counts[place_value_in_num] -= 1
        num_idx -= 1
    return result


def radix_sort(numbers: List[int]) -> List[int]:
    """radixソートを実行する"""
    len_numbers = len(numbers)
    max_num = max(numbers)
    place = 1  # 1の位からスタート
    while max_num > place:
        numbers = counting_sort_for_radix(numbers, place)
        place = place * 10  # 一つ上の位へ
        print(place)
    return numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    sorted_numbers = radix_sort(numbers)
    print(sorted_numbers)
    print(is_in_order(sorted_numbers))
