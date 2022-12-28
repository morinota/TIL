"""cache functionをデコレーター(functionをデコレートするもの)を使って実装せよ.

# Implements decorator to cache func
# from functools import lru_cache のようなcacheをしてくれるデコレータを作ってください.
- max_sizeとかは気にせず、単純にキャッシュして引き数がヒットしたら
すぐに結果を返すようなキャッシュデコレータでOK ->一回目は遅いが、2回目はスッと実行される.
- まずはデコレータを作る.
- デコレータ知らない人の為に
    - functionが実行される前後に「なにかの処理をさせたい」場合にデコレータを使う
    - デコレータの使い方をよくわかっているか.豆知識的な.
- ハッシュテーブル, dictをcacheとして使うと非常に速くアクセスできる.

"""

import time
from functools import lru_cache
from typing import Dict


def memoize(f):

    cache = {}  # dictでハッシュテーブルを作る. 引数と結果(返り値)のペアをcacheの中に入れておけば良い.

    def _wrapper(n: int) -> Dict:
        print("something before run decoreted function")
        if n not in cache:
            cache[n] = f(n)  # cacheにない結果の場合は、cacheに保存
        print("something after run decoreted function")
        return cache[n]  # cacheに保存された結果を返す.

    return _wrapper


# @lru_cache()  # デコレータとして使ってみると...->一回目は同様に遅いが、2回目はスッと実行される.
@memoize
def long_func(num: int) -> int:
    """例. 非常に時間のかかるfunction"""
    r = 0
    for i in range(10000000):
        r += num * i
    return r


if __name__ == "__main__":
    for i in range(10):  # 各ループが非常にゆっくりと実行される(再度実行しても時間は変わらない.)
        print(long_func(i))

    start = time.time()
    for i in range(10):
        print(long_func(i))
    print(time.time() - start)
