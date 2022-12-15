# 空港には毎日飛行機でN人の乗客が到着します。
# i番目の乗客は時刻T_iに到着する。
# 乗客は全員バスで市内へ移動する
# どのバスも定員はC人であり、C人以下を乗せる事ができる。
# i番目の乗客は、出発時刻がT_i以上T_i+K以下であるようなバスに乗る必要がある。
# この条件のもとで、上手くバスの出発時間を定める時、
# 必要なバスの数の最小値を求めよ。
# ただしバスの出発時間は必ずしも整数である必要も無い。
# また同じ時刻に出発するバスが複数あってもOK。

# 標準入力
N, C, K = map(int, input().split())
T = []
for i in range(N):
    T.append(int(input()))

# t_iが小さい方からC人ずつ順に切り出していく?=>Greedy性のある問題?
T = sorted(T, reverse=False)  # まずソート
answer = 0
i = 0
customer_count = 0
while i < N:
    customer_count = 0  # 乗客0人の状態
    # 先頭の乗客が乗る。
    time_first_customer = T[i]
    customer_count += 1  # 乗客一人目
    i += 1  # i をインクリメント(=数値に1を加える)して、次の乗客の判定へ

    # バスが切り替わる3つの条件でwhileループ！
    while (i < N) and (T[i] <= time_first_customer + K) and (customer_count < C):
        customer_count += 1
        i += 1  # i をインクリメント(=数値に1を加える)して、次の乗客の判定へ

    # 一番外のwhileループが一回終わる度にバス台数をカウント
    answer += 1
    # # i をインクリメント(=数値に1を加える)して、新しい配列の先頭とする
    # i += 1
print(answer)
