# link https://atcoder.jp/contests/abc032/tasks/abc032_d

# 入力読み込み
N, W = map(int, input().split())
w, v = ([None] + [0] * N), ([None] + [0] * N)
for i in range(1, N + 1):
    v[i], w[i] = map(int, input().split())

import copy

# # 例題(outputが16なら正解)
# N = 3  # 荷物の数
# W = 10  # ナップサックの許容量
# w = [None] + [9, 6, 4]  # 荷物それぞれの重さの配列
# v = [None] + [15, 10, 6]  # 荷物それぞれの価値の配列

# DPテーブル
# ここまで、DPの遷移処理について、**「dp[1],...,dp[n-1] と A[n]（今の場合は w[n] と v[n]）だけを使って dp[n] を求める」**と説明してきた。
# しかし今回のケースでは、dp[n] を求める際に必要なのは、dp[n-1] と w[n]、v[n] だけ！
# 従って、dp[n] の計算が終わった段階で、dp[n-1] はメモリー上から破棄してOK！
dp = {}


# まずdp[1]を考える。
dp[W] = 0  # 1個目を入れない場合
if w[1] <= W:
    dp[W - w[1]] = v[1]  # 1個目を入れる場合

for n in range(2, N + 1):
    dp_n = copy.copy(dp)  # n個目を入れない場合
    for w0 in dp.keys():
        if w[n] <= w0:  # n個目を入れる場合
            if w0 - w[n] in dp_n.keys():
                dp_n[w0 - w[n]] = max(dp_n[w0 - w[n]], dp[w0] + v[n])
            else:
                dp_n[w0 - w[n]] = dp[w0] + v[n]
        dp = dp_n  # dp[n] の計算が終わった段階で、dp[n-1] をメモリー上から破棄！(dp[n]で上書き)

print(max(dp.values()))
