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


def run_bubble_sort(numbers: List[int]) -> List[int]:
    """List[int]を受け取りBubbleソートを実行し、昇順ソートが完了された状態のListを返す
    1. limit_lineの場所をnumbersの`最後尾の要素の右側`で初期化
    2. 「隣り合う数字を比較して昇順に入れ替える」処理を、
    先頭からlimit line内の最後尾の一つ手前まで順番に実行する.
    3. limit_lineの場所を1つずつ手前にずらす
    4. limit lineの左側の要素が先頭の要素のみになった時点でソート完了

    """
    limit_line_idx = len(numbers)

    while limit_line_idx > 1:
        for j in range(limit_line_idx - 1):  # limit line内の最後尾の一つ手前まで繰り返し
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
        limit_line_idx -= 1  # limit_lineを1つずつ手前にずらす

    return numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(f"[LOG]init numbers: {numbers}")
    print(f"[LOG]sorted numbers: {run_bubble_sort(numbers)}")
