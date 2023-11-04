"""
- 問題:
    - N個の足場がある。 
    - i(=0, 1, ..., N-1)番目の足場の高さは h_i。
    - 最初0番目の足場にカエルがいて、以下のいづれかの行動を繰り返してi=N-1番目の足場を目指す:
        - 足場 i から足場 i+1へと移動する。(コストは |h_i - h_{i+1}|)
        - 足場 i から足場 i+2へと移動する。(コストは |h_i - h_{i+2}|)
    - カエルが N-1番目の足場にたどり着くまでに要するコストの総和の最小値を求めよ。
- 問題を、グラフの問題として定式化し直す:
    - 足場を頂点、足場間の移動を辺で表す。
    - また辺には、足場間の移動に要するコストを「重み」として表記する。
    - 定式化し直したグラフ問題:
        - 「与えられたグラフにおいて、頂点0から頂点N-1までまで辺を辿っていく方法のうち、辿った各辺の重みの総和の最小値を求めよ」
- グラフ問題を一連の部分問題に上手に分解する:
    - 頂点0, 1, 2,...,への最小コストを順に考えていく。
    - 結果を配列dp にメモ化(i.e. キャッシュ)していく。
"""


from collections import defaultdict
import random

INF_COST = 10**8
# メモ化用の配列を定義
DP_MEMO = defaultdict(lambda: INF_COST)


def calc_smallest_cost(
    destination_idx: int,
    heights: list[int],
) -> int:
    # ベースケース
    if destination_idx == 0:
        DP_MEMO[0] = 0
        return DP_MEMO[0]
    elif destination_idx == 1:
        DP_MEMO[1] = abs(heights[1] - heights[0])
        return DP_MEMO[1]

    # メモをチェック(すでに計算済みなら答えをリターンする)
    if DP_MEMO[destination_idx] != INF_COST:
        return DP_MEMO[destination_idx]

    # 答えをメモ化しながらrecursive call
    DP_MEMO[destination_idx] = min(
        calc_smallest_cost(destination_idx - 1, heights) + abs(heights[destination_idx] - heights[destination_idx - 1]),
        calc_smallest_cost(destination_idx - 2, heights) + abs(heights[destination_idx] - heights[destination_idx - 2]),
    )
    return DP_MEMO[destination_idx]


def main(N: int, heights: list[int]) -> None:
    """再帰で実装ver."""
    print(calc_smallest_cost(N - 1, heights))


if __name__ == "__main__":
    N = 7
    heights = [random.randint(0, 10) for _ in range(N)]
    main(N, heights)
