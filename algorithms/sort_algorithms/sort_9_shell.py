"""Shellソート
- Comb(櫛)ソートなどに近い
- Insertion sortの改良
- gap = n // 2からスタート
- gap = gap // 2で繰り返し...
"""

import random
from typing import List

from numpy import size
from sort_7_insertion import insertion_sort
from sympy import re
from utils import is_in_order


def shell_sort(numbers: List[int]) -> List[int]:
    """shellソートを実行する"""
    len_numbers = len(numbers)
    gap = len_numbers // 2

    while gap > 0:
        for i in range(gap, len_numbers):
            temp = numbers[i]  # 見ていく数字をtempとして保存する
            j = i  # 見ていく数字に対して、他のint達と比べて正しい位置へ.
            while j >= gap and numbers[j - gap] > temp:
                numbers[j] = numbers[j - gap]
                j -= gap  # どんどん左にずらしていく
            numbers[j] = temp  # 見ていく数字を正しい位置へ入れる

        gap = gap // 2

    return numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    sorted_numbers = shell_sort(numbers)
    print(sorted_numbers)
    print(is_in_order(sorted_numbers))
