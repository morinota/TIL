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
    return all([numbers[i] <= numbers[i + 1] for i in range(len(numbers) - 1)])
    # for i in range(len(numbers)-1):
    #     if numbers[i] > numbers[i+1]:
    #         return False
    # return True


def run_bogo_sort(numbers: List[int]) -> List[int]:
    """List[int]を受け取りBogoソートを実行し、昇順ソートが完了された状態のListを返す.
    - 配列内の数字をランダムに(適当に)を並び替えて、ソートされているか確認する
    - 上の処理ををソートが完了するまで繰り返す.
    """

    while not is_in_order(numbers):
        random.shuffle(numbers)

    return numbers  # Trueになったら処理から抜ける


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(f"[LOG]init numbers: {numbers}")
    print(f"[LOG]sorted numbers: {run_bogo_sort(numbers)}")
