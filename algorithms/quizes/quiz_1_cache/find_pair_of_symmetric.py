"""
Symmetric
Input  [(1, 2), (3, 5), (4, 7), (5, 3), (7, 4)]
Output [(5, 3), (7, 4)]
左右対称のものが出現したらそれをOpututする

回答例:
- tupleの一つ目の値をkey、２つ目の値をvalueとして入れていく.
- 以降に来る2つ目の値がkeyにあり、そのvalueが１つ目の値と一致していればSymmetric
- この手の問題は基本的にcacheかハッシュテーブルを使えばすんなりと解ける.

"""

from typing import Iterator, List, Tuple


def find_symmetric_pair(pairs: List[Tuple[int, int]]) -> Iterator[Tuple[int, int]]:
    """シンメトリックなペアを見つけて、Iteratorで返す"""
    cache = {}
    for pair in pairs:
        first_val, second_val = pair[0], pair[1]
        value = cache.get(second_val)  # ペアになった残りはcacheから削除する必要はない?(問題設定によるが...)
        if not value:
            cache[first_val] = second_val

        elif value == first_val:
            yield pair


if __name__ == "__main__":
    l = [(1, 2), (3, 5), (4, 7), (5, 3), (7, 4)]
    for r in find_symmetric_pair(l):
        print(r)
