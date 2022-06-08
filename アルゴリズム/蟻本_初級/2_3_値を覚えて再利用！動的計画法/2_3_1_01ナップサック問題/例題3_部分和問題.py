# 問題リンク:https://atcoder.jp/contests/tdpc/tasks/tdpc_contest

n, A = map(int, input().split())
a = [0] * n
a = [int(input()) for _ in range(n)]

# DP Table
dp = [[False] * 10001] * 101  # dp[i][j] , 一旦すべて false に
dp[0][0] = True  # dp[0][0]だけTrueに

for i in range(0, n, 1):
    for j in range(0, A, 1):
        if a[j] > j:
            dp[i + 1][j] = dp[i][j]
        elif a[j] <= j:
            dp[i + 1][j] = dp[i][j - a[i]]

if dp[n][A] == True:
    print("YES")
else:
    print("NO")
