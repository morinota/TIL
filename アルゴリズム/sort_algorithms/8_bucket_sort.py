"""Bucketソート
- Insertionソートを応用したもの
- 並び変える対象をバケットに分割してから、insertion sortする
- ex)
    - 0~9までバケットをつくった（バケットサイズ10　<=最大値/数?）
    - 対象の数字を、一つずつ、各バケットに振り分けていく
    - 10で割ったときの商(quodient)によって、振り分ける
"""

import random
from typing import List

from numpy import size
from sort_7_insertion import insertion_sort
from sympy import re
from utils import is_in_order


def bucket_sort(numbers: List[int]) -> List[int]:
    """bucketソートを実行する"""
    max_num = max(numbers)
    len_numbers = len(numbers)
    bucket_size = max_num // len_numbers  # 商をバケットサイズに. (バケットサイズを固定するケースもある)

    buckets = [[] for _ in range(bucket_size)]
    # bucket_sizeで割った時の商(quotient)によって、数字を各バケットに振り分けて行く
    for num in numbers:
        quotient = num // bucket_size
        if quotient != bucket_size:
            buckets[quotient].append(num)
        else:
            buckets[bucket_size - 1].append(num)
    print(buckets)

    # 各バケット毎にinsertionソート
    for bucket_idx in range(bucket_size):
        insertion_sort(buckets[bucket_idx])
    # 後は各バケットを足し合わせるだけ
    # connected_numbers = []
    # for bucket_idx in range(bucket_size):
    #     connected_numbers += buckets[bucket_idx]
    # リスト内包表記ver.
    connected_numbers = [num for bucket in buckets for num in bucket]

    return connected_numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    sorted_numbers = bucket_sort(numbers)
    print(sorted_numbers)
    print(is_in_order(sorted_numbers))
