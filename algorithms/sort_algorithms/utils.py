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
