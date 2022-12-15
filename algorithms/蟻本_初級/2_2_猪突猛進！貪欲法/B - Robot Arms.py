# https://atcoder.jp/contests/keyence2020/tasks/keyence2020_b

N = int(input())
X, L = [0] * N, [0] * N
for i in range(N):
    X[i], L[i] = map(int, input().split())

# 区間スケジューリング問題
# Greedy Algorithm?
# 選べるものの中で終点が最小のものを選択する。

# 終点と始点を先に入れておく
p = [0] * N
for i in range(N):
    p[i] = {}
    p[i]["start_p"] = X[i] - L[i]
    p[i]["end_p"] = X[i] + L[i]

# 終点の座標の昇順でソート
p = sorted(p, key=lambda x: x["end_p"], reverse=False)
# 区間の終端 (または始端) でソートするのは極めてよくみるテクニック
# 今後難しい問題に挑むときにも常に念頭に置いておきたい

answer = 1  # p[0]の分
t = p[0]["end_p"]  # 現在までに選択した区間の中で一番後ろの点
for i in range(1, N):
    if t <= p[i]["start_p"]:
        answer += 1
        t = p[i]["end_p"]

print(answer)
