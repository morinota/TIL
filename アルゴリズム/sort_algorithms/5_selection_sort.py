"""Selectionソート
- Bubble sortの改良版
- リストのトップ(start地点)をテンポラリに保持
- その値を各要素と比較していく
- 比較した時、より小さい値を保持して比較していく
- 一周した時、保持している値を先頭の数字と入れ替える(これで確定)
- start地点を一つ後ろにずらして繰り返し
- selectionソートは有名で、コードも難しくない
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


def selection_sort(numbers: List[int]) -> List[int]:
    """selectionソートを実行する"""
    len_numbers = len(numbers)
    for start_idx in range(len_numbers):
        min_idx = start_idx  # 先頭(start_idx)をmin_idxの初期値として保存
        for j in range(start_idx + 1, len_numbers):
            if numbers[min_idx] > numbers[j]:
                min_idx = j  # min_idxとして保持する値を更新

        # 一周したら、min_idxの値をstart_idxの値と入れ替える
        numbers[start_idx], numbers[min_idx] = numbers[min_idx], numbers[start_idx]
        # -> start_idxを後ろに一つずらして次のループへ
    return numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    print(selection_sort(numbers))
