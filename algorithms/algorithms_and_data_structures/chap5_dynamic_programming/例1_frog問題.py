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


def main(N: int, heights: list[int]) -> None:
    # メモ化用の配列を定義
    dp = defaultdict(lambda: INF_COST)

    # 初期条件
    dp[0] = 0
    dp[1] = abs(heights[1] - heights[0])

    for i in range(2, N):
        dp[i] = min(
            dp[i - 1] + abs(heights[i] - heights[i - 1]),
            dp[i - 2] + abs(heights[i] - heights[i - 2]),
        )

    print(dp[N - 1])


if __name__ == "__main__":
    N = 7
    heights = [random.randint(0, 10) for _ in range(N)]
    main(N, heights)
