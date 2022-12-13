import random
from typing import List

from utils import is_in_order

"""Quickソート
- よく出る
- O(n * log n)
- Partitionという概念
- 最後尾のnumをpivotと設定。pivotを上手く使って並び替えていく.
- variablesの初期値をi=-1(最後尾のnum), j=0(先頭のnum)で設定。これらをうまく使っていく.
    - まずnumbers[j]とpivotを比べる.
    - pivotの方が大きかった場合、i+=1してiとjの場所を入れ替える
    - 次はj+=1して、見ている数字をずらしていく(jは見ている数字のindex)
    - こうするとpivotより小さい数字は前へ、大きい数字は後ろへズレていく.
    - pivotを入れる位置を探す（iの位置に入れる)
    - その後、pivotの左側と右側で分けてソートする
- 再起の練習にもなる
- 重要なソート！
"""


class QuickSort:
    def __init__(self) -> None:
        pass

    def sort(self, numbers: List[int]) -> List[int]:
        def _quick_sort(numbers: List[int], low_idx: int, high_idx: int) -> None:
            if low_idx < high_idx:
                partition_idx = self._find_partition(numbers, low_idx, high_idx)
                # pivot(partation)の左側
                _quick_sort(
                    numbers,
                    low_idx,
                    high_idx=partition_idx - 1,
                )
                # pivot(partation)の右側
                _quick_sort(
                    numbers,
                    low_idx=partition_idx + 1,
                    high_idx=high_idx,
                )

        _quick_sort(numbers, 0, len(numbers) - 1)
        return numbers

    def _find_partition(self, numbers: List[int], low_idx: int, high_idx: int) -> int:
        """pivotの場所を見つける関数;これがpartitionの概念"""
        i = low_idx - 1
        pivot = numbers[high_idx]
        # 見ている数字のidx=jをずらしていく
        for j in range(low_idx, high_idx):
            # pivotの方が大きい場合、i+=1してiとjの場所を入れ替える
            if numbers[j] <= pivot:
                i += 1
                numbers[i], numbers[j] = numbers[j], numbers[i]
        numbers[i + 1], numbers[high_idx] = numbers[high_idx], numbers[i + 1]

        return i + 1


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    sorted_numbers = QuickSort().sort(numbers)
    print(sorted_numbers)
    print(is_in_order(sorted_numbers))
