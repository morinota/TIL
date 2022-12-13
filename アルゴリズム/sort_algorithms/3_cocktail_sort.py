"""Cocktailソート
- カクテルをシェイクする＝＞シェーカーソート
- bubbleソートの改良版(バブルソートを振るver)
- バブルソートと同様の手順,
- 一周の中で一回でも入れ替えたら、swap = Trueに！
- 一周したら初期値swap = Falseに戻し、limitを1つずらし今度は後ろから
- swapがTrueにならなかったら、処理終了.
- bubbleソートのように最後までやらなくてもswap=falseが分かり次第終了できる
    -> より早い
- for文が一乗×2 -> big O記法で言う、O(2n)の処理スピード?
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


def cocktail_sort(numbers: List[int]) -> List[int]:
    """cocktailソートを実行する"""
    len_numbers = len(numbers)
    swapped = True
    start_limit_line = 0
    end_limit_line = len_numbers - 1
    while swapped:
        swapped = False
        for i in range(start_limit_line, end_limit_line):
            if numbers[i] > numbers[i + 1]:
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
                swapped = True

        if not swapped:
            break

        # 逆走
        swapped = False
        end_limit_line = end_limit_line - 1  # 一つ手前にずらしていく

        for i in range(end_limit_line - 1, start_limit_line - 1, -1):  # -1個ずつ進む
            if numbers[i] > numbers[i + 1]:
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
                swapped = True
        start_limit_line = start_limit_line + 1  # 一つ後ろにずらしていく

    return numbers


if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(numbers)
    print(cocktail_sort(numbers))
