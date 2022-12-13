"""Bubble ソート
- 先頭から、隣り合う数字を比較して昇順に入れ替える
- 一周したら、limitのラインを、最後尾から1つ手前にずらす
- 繰り返し
- Bogoソートより遙かにはやい
- for文の中にfor文→big O記法で言う、O(n**2)の処理スピード
"""

import random
from typing import List


def is_in_order(numbers: List[int]) -> bool:
    """numbersが昇順ならTrueを返す関数を定義"""
    # list内包表記ver.
    return all(numbers[i] <= numbers[i + 1] for i in range(len(numbers) - 1))
    # for i in range(len(numbers)-1):
    #     if numbers[i] > numbers[i+1]:
    #         return False
    # return True


def bubble_sort(numbers: List[int]) -> List[int]:
    """Bubbleソートを実行する"""
    len_numbers = len(numbers)
    # limit_lineを最後尾から1つずつ手前にづらしていく
    for i in range(len_numbers):
        len_numbers_in_limit = len_numbers - i
        # limit line内の最後尾の一つ手前まで繰り返し
        for j in range(len_numbers_in_limit - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    print(bubble_sort(numbers))
