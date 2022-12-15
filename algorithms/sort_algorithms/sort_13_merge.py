import random
from typing import List

from utils import is_in_order

"""Mergeソート
- どんどんnumbersを半分に分割していく。
- すべて分割した後に、今度はマージしていく。マージするときに並び替える
    - マージ手順: 先頭ののnum同士を比べる
        - ex) [4,5]と[1,8]をマージする場合
        - 4と１を比べる→1が入る
        - 4と８を比べる→４が入る
        - ５と８を比べる→5が入る
        - 余った8が最後尾に入り、マージ後は[1,4,5,8].
- デバッガー,step intoで適宜動作をチェックするといい...!
"""


class MergeSort:
    def __init__(self) -> None:
        pass

    def sort(self, numbers: List[int]) -> List[int]:
        len_numbers = len(numbers)
        if len_numbers <= 1:  # 最後まで分割できていたら再起を終了してreturn
            return numbers

        # ex)len=9の場合,9//2 = 4, len=8の場合,8//2 = 4
        center_idx = len_numbers // 2
        # 半分に分割していく
        left_nums = numbers[:center_idx]
        right_nums = numbers[center_idx:]

        self.sort(left_nums)
        self.sort(right_nums)

        # 最後まで分割し終えたら、やっとマージ(しながらソート)へ
        left_idx = right_idx = merged_idx = 0  # left,rightのindex番号を管理するのがi,j(先頭から比較するので0)
        while left_idx < len(left_nums) and right_idx < len(right_nums):
            if left_nums[left_idx] < right_nums[right_idx]:
                # merge後のListへ、より小さい方から入れていく
                numbers[merged_idx] = left_nums[left_idx]
                left_idx += 1
            else:
                numbers[merged_idx] = right_nums[right_idx]
                right_idx += 1
            merged_idx += 1
        # 上の例において、ここまでで[1,4,5]の状態。余った8が入ってない状態.
        while left_idx < len(left_nums):
            numbers[merged_idx] = left_nums[left_idx]
            left_idx += 1
            merged_idx += 1  # TODO:この行はwhileの外になぜ出せないんだろう...?
        while right_idx < len(right_nums):
            numbers[merged_idx] = right_nums[right_idx]
            right_idx += 1
            merged_idx += 1  # TODO:この行はwhileの外になぜ出せないんだろう...?

        return numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    sorted_numbers = MergeSort().sort(numbers)
    print(sorted_numbers)
    print(is_in_order(sorted_numbers))
