N, Q = map(int, input().split())

A = list(map(int, input().split()))
X = [0] * Q
for q in range(Q):
    X[q] = int(input())

# 作戦
# 多分、QとNで二重で全探索すると、Time Out
# q=1の記録を使って、q=2の質問に答えられれば...!=>dp!!
dp = {}

# X_qとA_iの差(A_iの方が大きいと負。小さいと正)
A_diff_X_1 = [X[0] - v for v in A]
answer = sum([abs(diff) for diff in A_diff_X_1])
print(answer)

dp[X[0]] = answer


for q in range(1, Q):
    if X[q] in dp.keys():
        print(dp[X[q]])
    else:
        X_diff = X[0] - X[q]
        A_diff_X_q = [a_diff_x_1 - X_diff for a_diff_x_1 in A_diff_X_1]
        answer = sum([abs(diff) for diff in A_diff_X_q])
        dp[X[q]] = answer
        print(dp[X[q]])
