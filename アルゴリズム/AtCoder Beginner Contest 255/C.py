import numpy as np

X, A, D, N = map(int, input().split())

S = []
if D == 0:
    S = [A] * N
else:
    last = A + D * (N - 1)
    S = np.arange(A, last + D, D)
    S = list(S)


print(S)

operate_count = 0

# 戦略
# XをSに含まれる整数に一致させるには...
# XをSに追加して、ソートして、Xの前後のS_iとの差を見る。
# より差が小さい方が答え！

if X in S:
    print(0)

S_add_X = S + [X]
S_add_X.sort(reverse=False)

# Xのindexを検索
X_idx = S_add_X.index(X)

# 前との距離
distances = []
if X_idx != 0:
    distance_mae = X - S_add_X[X_idx - 1]
    distances.append(distance_mae)

if X_idx != N:
    distance_ushiro = S_add_X[X_idx + 1] - X
    distances.append(distance_ushiro)


print(min(distances))
