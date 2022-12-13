"""Bogo ソート
- 適当に並び替える
- サルでもできる
- アルゴリズムと言えばBogoソート以外を検討する
- 特に重要ではない
- 昇順に並べるまでにめっちゃ時間かかる
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


def bogo_sort(numbers: List[int]) -> List[int]:
    """Bogoソートを実行する"""
    # is_in_order()がTrueにならない限り並び替え続ける
    while not is_in_order(numbers):
        random.shuffle(numbers)

    return numbers  # Trueになったら処理から抜ける


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    print(bogo_sort(numbers))
