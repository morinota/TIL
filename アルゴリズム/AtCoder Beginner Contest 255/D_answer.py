N, Q = map(int, input().split())

A = list(map(int, input().split()))
X = [0] * Q
for i in range(Q):
    X[i] = int(input())

# 戦術
# Aをソートして, A_1<=A_2<=...<=A_Nとする。
# ある質問q=iについての解答は...
# A_1<=...<=A_j<=X<=A_j+1<=...<=A_Nである時、答えは以下の式で表される。
# \sum_{k=1~j}{(X_i - A_k)} + \sum_{k=j+1~N}{(A_k - X_i)}
# ここで第一項\sum_{k=1~j}{(X_i - A_k)} = j*X_i - \sum_{k=1~j}{A_k}
# j*X_iはO(1),
# \sum_{k=1~j}{A_k}は累積和を用いて事前計算O(N), クエリあたりO(1)で求める事ができる。
# また、第二項についても同様。
# \sum_{k=j+1~N}{(X_i - A_k)} = \sum_{k=j+1~N}{A_k} - (N-j+1+1)*X_i

# また、A_j<=X_i<=A_j+1となるようなjは、二分探索によりクエリあたりO(log N)で求める事ができる。

# 以上より、この問題をO((N+Q) * log N)で解くことができる。

# Aをソート
A = sorted(A, reverse=False)
# 0~j, j = 0, 1, 2, ...N, までの累積和を事前に計算しておく
dp = {}
for j in range(0, N + 1):
    dp[j] = sum(A[0:j])

# 各クエリに対して
for i in range(Q):
    # A_j<=X_i<=A_j+1となるようなjを探す
    A_with_X = sorted(A + [X[i]])
    j = A_with_X.index(X[i]) - 1
    # j*X_iを計算
    j_X_i = (j + 1) * X[i]
    # \sum_{k=1~j}{A_k}を取得
    sum_1_toj = dp[j + 1]
    # \sum_{k=j+1~N}{A_k}を取得
    sum_jplus1_toN = dp[N] - sum_1_toj
    # (N-(j+1)+1)*X_iを計算
    N_j_1_1_X_i = (N - (j + 1)) * X[i]

    answer = (j_X_i - sum_1_toj) + (sum_jplus1_toN - N_j_1_1_X_i)
    print(answer)
