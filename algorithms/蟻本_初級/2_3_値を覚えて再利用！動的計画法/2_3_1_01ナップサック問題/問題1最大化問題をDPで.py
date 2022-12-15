# https://algo-method.com/tasks/307

n = int(input())
A_list = input().split(" ")
a = [0] * 10010  # 最大10000個ですが、少しだけ多めにとります

dp = [0] * 10010  # DP テーブル

dp[0] = 0
for i in range(0, n, 1):
    dp[i + 1] = max(dp[i], dp[i] + a[i])

print(dp[n])
