"""dictのhashを使ったクイズ
1. Input: [11, 2, 5, 9, 10, 3], 12   => Output: (2, 10) or None
- 12になるようなペアを探して出力せよ. 一番始めに見つけたペアを出力すればOK

2. Input: [11, 2, 5, 9, 10, 3]       => Output: (11, 9) or None  ex) 11 + 9 = 2 + 5 + 10 + 3
- ２つのnumの和 = 残りのnumの和 となるような2つのnumのペアを探せ。なければNone

ペアを探すようなクイズ関係は、集合を上手く使って、
次に入ってくる値を上手く検証してcacheの中にあるかどうかを確認して解く、という傾向が非常に多い。
パターンを覚えておくと良い。
"""

from typing import List, Optional, Tuple


def get_pair(numbers: List[int], target: int) -> Optional[Tuple]:
    """Q 1"""
    cache = set()  # キャッシュに集合(要素の重複を避ける為)を保存できるようにする
    for num in numbers:
        val = target - num
        if val in cache:
            return val, num
        cache.add(num)  # ユニークなものだけ入る


def get_pair_half_sum(numbers: List[int]) -> Optional[Tuple]:
    """Q 2
    ２つのnumの和 = sum_numbers / 2 = 残りのnumの和となるようなペアを探す
    """
    # sum_numbers = sum(numbers)
    # if sum_numbers % 2 != 0:  # 合計が奇数だったら、そもそもペアがない
    #     return None
    # half_sum = int(sum_numbers / 2)

    # ↑よりもbuild-in関数のdivmod()を使った方がスマートかも
    half_sum, remainder = divmod(sum(numbers), 2)  # ->商と余り
    if remainder != 0:
        return None

    # あとはq1と同様の事をやる. target = half_sum
    return get_pair(numbers, target=half_sum)


if __name__ == "__main__":
    numbers = [11, 2, 5, 9, 10, 3]
    target = 12
    print(get_pair(numbers, target))
    print(get_pair_half_sum(numbers))
