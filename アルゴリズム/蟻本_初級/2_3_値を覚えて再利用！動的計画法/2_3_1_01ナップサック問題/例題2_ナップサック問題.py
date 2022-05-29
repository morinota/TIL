# 入力
n, W = map(int, input().split())
weight, value = [0] * 110, [0] * 110

# DPテーブル
dp = [[0] * 10010] * 110

# DP初期条件: dp[0][w] = 0
for w in range(0,W+1, 1):
    dp[0][w] = 0

# DPループ
for i in range(0,n,1):
    for w in range(0,W+1, 1):
        if w >= weight[i]:
            dp[i+1][w] = max(
                dp[i][w-weight[i]] + value[i], dp[i][w]
                )
        else:
            dp[i+1][w] = dp[i][w]

print(dp[n][W])