# link https://atcoder.jp/contests/abc032/tasks/abc032_d

# 入力読み込み
# N, W = map(int, input().split())
# w, v = [0] * N, [0] * N
# for i in range(N):
#     v[i], w[i] = map(int, input().split())

import copy

# 例題(outputが16なら正解)
N = 3  # 荷物の数
W = 10  # ナップサックの許容量
w = [None] + [9, 6, 4]  # 荷物それぞれの重さの配列
v = [None] + [15, 10, 6]  # 荷物それぞれの価値の配列

# DPテーブル
dp = [{} for _ in range(N + 1)]  # dp[1], dp[2], ... には、それぞれに空のディクショナリーが入っている
# 「残り容量」をキーとするディクショナリー

# まずdp[1]を考える。
dp[1][W] = 0  # 1個目を入れない場合
if w[1] <= W:
    dp[1][W - w[1]] = v[1]  # 1個目を入れる場合

for n in range(2, N + 1):
    dp[n] = copy.copy(dp[n - 1])  # n個目を入れない場合
    for w0 in dp[n - 1].keys():  # 「1個目を処理した結果の残容量」を取り出す
        if w[n] <= w0:  # w[n] <= w0(残容量) であれば"n個目を入れる場合"を検討できる。
            if w0 - w[n] in dp[n].keys():  # もしkey=残容量が同じケースが既に記録されていれば...
                # ナップサック内の価値がより大きくなる方を残す。
                dp[n][w0 - w[n]] = max(dp[n][w0 - w[n]], dp[n - 1][w0] + v[n])
            else:
                # key=新たな残容量=w0-w[2], value=新たな合計価値=dp[1][w0] + v[2]
                dp[n][w0 - w[n]] = dp[n - 1][w0] + v[n]

print(max(dp[N].values()))
