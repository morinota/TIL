"""最も多く出現する文字列をカウントする. 大文字と小文字は分けない.
スペースは含めない. カンマやピリオドは含める.
# Input: 'This is a pen. This is an apple. Applepen.'
# Output: ('p', 6)

こういったカウント系は、ハッシュテーブルやディクショナリを使うのが基本。
- version 1では↑を使わずにリストで.
    - lower()
    - isspace()
    - operator.itemgetter(idx): tupleのidx番目の要素を取得する
    - max()のkey引数. key=functionの結果を使って...
"""
import operator
from collections import Counter
from typing import Tuple


def count_chars_v1(strings: str) -> Tuple[str, int]:
    strings = strings.lower()
    # l = []
    # for char in strings:
    #     if not char.isspace():
    #         l.append((char, strings.count(char)))
    l = [(c, strings.count(c)) for c in strings if not c.isspace()]
    return max(l, key=operator.itemgetter(1))  # tupleの２つ目の要素を基準にmaxを取得する.


def count_chars_v2(strings: str) -> Tuple[str, int]:
    """dictを使うケース(listより早い)
    ただd.get(char, 0) + 1があまり綺麗じゃない.
    """
    strings = strings.lower()
    d = {}  # dict(hash, cache)を作る
    for char in strings:
        if not char.isspace():
            d[char] = d.get(char, 0) + 1  # charがdictに入ってるか確認, 入ってなかったら0を取得
    max_key = max(d, key=d.get)  # key=functionの返り値を使って... maxの返り値はdictのkey?
    return max_key, d[max_key]


def count_chars_v3(strings: str) -> Tuple[str, int]:
    """Counterを使う"""
    strings = strings.lower()
    d = Counter()
    for char in strings:
        if not char.isspace():
            d[char] += 1
    max_key = max(d, key=d.get)
    return max_key, d[max_key]


if __name__ == "__main__":
    s = "This is a pen. This is an apple. Applepen."
    print(count_chars_v3(s))
