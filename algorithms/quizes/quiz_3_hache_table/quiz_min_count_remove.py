"""２つのリストに出現する値のうち、数が少ない値をリストから削除する
Input  X: [1, 2, 3, 4, 4, 5, 5, 8, 10] Y: [4, 5, 5, 5, 6, 7, 8, 8, 10]
  =>   X: [1, 2, 3, 4, 4, 10]          Y: [5, 5, 5, 6, 7, 8, 8, 10]
それぞれ特定の数字が削除されている.
- 両方のリストに含まれている.
- 出現回数が小さい方をリストから全て削除する.

tips
- Counterの使い方.(だめと言われるケースではハッシュテーブルで)
- list.remove(5)では全ての5は削除できない-> List内包表記でやるケース！
"""

from collections import Counter
from typing import List


def less_count_remove(x: List[int], y: List[int]) -> None:
    """引数で渡されたxとyの値をそのまま書き換えるので、返り値はなし
    (自分で実装)
    """
    # counter_x = {}
    # counter_y = {}
    # for i in x:
    #     counter_x[i] = counter_x.get(i, 0) + 1
    # for i in y:
    #     counter_y[i] = counter_y.get(i, 0) + 1
    counter_x = Counter(x)  # 各valueの出現回数をカウント
    counter_y = Counter(y)

    for key_x, value_x in counter_x.items():
        value_y = counter_y.get(key_x)
        if value_y:  # xの値がyにも含まれているか調べたい
            if value_x < value_y:
                x[:] = [i for i in x if i != key_x]  # listの書き換え
            elif value_x > value_y:
                y[:] = [i for i in y if i != key_x]


if __name__ == "__main__":
    x = [1, 2, 3, 4, 4, 5, 5, 8, 10]
    y = [4, 5, 5, 5, 6, 7, 8, 8, 10]
    print("x =", x)
    print("y =", y)
    less_count_remove(x, y)
    print("x =", x)
    print("y =", y)
