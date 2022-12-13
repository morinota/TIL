"""Gnome(ノーム)ソート
- bubbleソートに類似したもの
- 入れ替えたら左に戻る(bubble sortでは、そのまま右にずれる)
"""

import random
from typing import List

from psutil import swap_memory


def is_in_order(numbers: List[int]) -> bool:
    """numbersが昇順ならTrueを返す関数を定義"""
    # list内包表記ver.
    return all(numbers[i] <= numbers[i + 1] for i in range(len(numbers) - 1))
    # for i in range(len(numbers)-1):
    #     if numbers[i] > numbers[i+1]:
    #         return False
    # return True


def gnome_sort(numbers: List[int]) -> List[int]:
    """selectionソートを実行する"""
    len_numbers = len(numbers)
    right_idx = 0
    while right_idx < len_numbers:
        if right_idx == 0:
            right_idx += 1
        # 左側と比較(Bubbleソートは右側idx+1と比較)
        if numbers[right_idx] < numbers[right_idx - 1]:
            numbers[right_idx], numbers[right_idx - 1] = numbers[right_idx - 1], numbers[right_idx]
            # 入れ替えたら左に戻る(bubble sortでは、そのまま右にずれる)
            right_idx -= 1
        else:
            # 入れ替えない場合はそのまま右へずれる
            right_idx += 1

    return numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    print(gnome_sort(numbers))
