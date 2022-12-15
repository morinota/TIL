# link https://atcoder.jp/contests/abc032/tasks/abc032_d

# 入力読み込み
# N, W = map(int, input().split())
# weight, value = [0] * N, [0] * N
# for i in range(N):
#     value[i], weight[i] = map(int, input().split())


# 例題(outputが16なら正解)
N = 3  # 荷物の数
W = 10  # ナップサックの許容量
weight = [9, 6, 4]  # 荷物それぞれの重さの配列
value = [15, 10, 6]  # 荷物それぞれの価値の配列

# DPテーブル
dp = [[-1] * (W + 1) for i in range(N + 1)]
# DP初期条件: dp[0][w] = 0
for w in range(0, W + 1, 1):
    dp[0][w] = 0

# DPループ, 漸化式にしたがって DP を実行する
# dp[i+1][w]：i番目までの品物の中から、重さがw(基準)を超えないように選んだ時の、価値の総和の最大値。
# dp[i][w]の値が既に求まっている事を前提に、dp[i+1][w]の値を考える。
# =>すなわち前回までの結果を使いまわして、効率よく計算しようって話！
for i in range(0, N, 1):
    for w in range(0, W + 1, 1):
        if w < weight[i]:  # そもそも品物iの重さが基準wより大きければ、iを選択しようがないので...
            dp[i + 1][w] = dp[i][w]
        else:  # それ以外の場合は、品物iを選ぶor選ばないの場合分け。
            # 選ぶ場合と選ばない場合で、価値が大きくなる方が最適解。
            answer = max(dp[i][w - weight[i]] + value[i], dp[i][w])
            dp[i + 1][w] = answer

# dp 配列の末尾が N 番目までの品物から重さ W 以下で選ぶ場合の品物の価値の最大値となる。
print(dp[N][W])
