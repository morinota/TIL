"""Insertion(挿入)ソート
- 簡単かつ有名なソート
- 見る値を適切な位置まで持ってくる
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


def insertion_sort(numbers: List[int]) -> List[int]:
    """insertionソートを実行する"""
    len_numbers = len(numbers)
    for i in range(1, len_numbers):  # index=1から見ていく(idx=0は左側に比べる数字がない)
        temp = numbers[i]  # 見ていく数字をtempとして保存する
        j = i - 1  # 見ていく数字に対して、左側のint達と比べて正しい位置へ.
        while j >= 0 and numbers[j] > temp:
            numbers[j + 1] = numbers[j]
            j -= 1

        numbers[j + 1] = temp  # 左側のint達と比べて正しい位置へ入れる

    return numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    print(insertion_sort(numbers))
