"""Combソート
- 櫛を溶かしていくイメージ
- 櫛の幅をどんどん小さくして、ソートする
- bubbleソートの改良版.
- ex) 
    - Gap = 7 % 1.3(決まっている数値)  = 5(櫛の幅）
    - 5コ離れた要素を比較していく
    - Gap = 5 % 1.3 = 3
    - クシの幅を3にして、同様の事を行う
    - どんどんクシの幅を小さくしていく
    - 幅が一になったら、swapを用いて、Falseになるまで繰り返す
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


def comb_sort(numbers: List[int]) -> List[int]:
    """combソートを実行する"""
    gap_coefficient = 1.3
    len_numbers = len(numbers)
    gap = len_numbers  # ギャップの初期値
    is_swapped = True

    while gap != 1 or is_swapped:
        # gapを狭くする
        gap = int(gap / gap_coefficient)
        if gap < 1:
            gap = 1

        is_swapped = False

        for i in range(0, len_numbers - gap):
            if numbers[i] > numbers[i + gap]:
                numbers[i], numbers[i + gap] = numbers[i + gap], numbers[i]
                is_swapped = True
    return numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    print(comb_sort(numbers))
