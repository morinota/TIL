"""
- 問題:
    - N個の品物がある。
    - i(=0 ~ N-1)番目の品物の重さはweight_{i}, 価値はvalue_{i}。
    - N個の品物から、重さの総和がWを超えないようにいくつか選ぶ。
    - 選んだ品物の価値の総和として考えられる最大値を求めよ。
- DPの部分問題の作り方の基本パターン:
  - N個の対象物 {0, 1, ..., N-1}に関する問題に対して、**最初のi個の対象物{0,1,...,i-1}に関する問題**を部分問題として考える。
- 部分問題に分解する:
    - 0,1,...,i-1番目の品物からいくつか選んだ後に、i番目の品物を選ぶor選ばないの2通りの選択肢がある。
        - -> このような「**各段階においていくつかの選択肢が存在する」状況**は、DPを有効に適用できそう...!
    - ->dp[i] <- 最初のi個の品物{0, 1, ..., i-1}までの中から重さがWを超えないように選んだ時の、価値の総和の最大値。
- しかしこのままでは、部分問題 間の遷移を作れずに詰まってしまう...
    - dp[i] ->dp[i+1]への遷移を考える時、品物iを加えるようにした時に、重さの合計がWを超えるかどうかがわからない。
    - この問題を解決する為に、dpテーブル(キャッシュ)の定義を以下のように変更する。
    - ->dp[i][w] <- 最初のi個の品物{0, 1, ..., i-1}までの中から重さがwを超えないように選んだ時の、価値の総和の最大値。
    - このように、考案したdpテーブル設計で上手く遷移が作れなかった場合に、添字を付け加える事で遷移が成立するようにする作業をしばしば行う...!
"""


from collections import defaultdict
import random

MINIMUM_VALUE = -1
# メモ化用の配列を定義
DP_MEMO = defaultdict(lambda: MINIMUM_VALUE)  # key=(item_idx, upper_weight_limit), value=価値の最大値


def calc_heighest_value(
    item_idx: int,
    upper_weight_limit: int,
    values: list[int],
    weights: list[int],
) -> int:
    """ナップサック問題の部分問題の答えを返す関数"""
    # ベースケース
    if item_idx == 0:
        DP_MEMO[(0, upper_weight_limit)] = values[0] if weights[0] <= upper_weight_limit else 0
        return DP_MEMO[(0, upper_weight_limit)]

    # メモをチェック(すでに計算済みなら答えをリターンする)
    if DP_MEMO[(item_idx, upper_weight_limit)] != MINIMUM_VALUE:
        return DP_MEMO[(item_idx, upper_weight_limit)]

    # 答えをメモ化しながらrecursive call
    DP_MEMO[(item_idx, upper_weight_limit)] = max(
        # i番目の品物を選ぶ時
        calc_heighest_value(item_idx - 1, upper_weight_limit - weights[item_idx], values, weights) + values[item_idx],
        # i番目の品物を選ばない時
        calc_heighest_value(item_idx - 1, upper_weight_limit, values, weights),
    )

    return DP_MEMO[(item_idx, upper_weight_limit)]


def main(
    N: int,
    W: int,
    values: list[int],
    weights: list[int],
) -> None:
    """再帰で実装ver."""
    print(calc_heighest_value(N - 1, W, values, weights))


if __name__ == "__main__":
    N = 7
    W = 100
    values = [random.randint(0, 10) for _ in range(N)]
    weights = [random.randint(0, 10) for _ in range(N)]
    main(N, W, values, weights)
