# コンテストに3N人が参加する。
# i番目の参加者の強さは整数a_iで表される。
# 3人一組となるようにチームをN組作る。
# チームの強さは、チームメンバーの強さのうち2番目に大きい値で表される.
# N組のチームの強さの和としてあり得る値の内、最大値を求めよ。

# 標準入力
N = int(input())
a = list(map(int, input().split()))

a.sort(reverse=False)  # 各iの強さの昇順でソート
# この時、最初のN人は、N個のチームの最弱メンバー。
# この時、N+1番目の参加者はどのチームに入っても2番目に強いメンバー。
# すると、N+2番目の人はN+1番目の参加者と同じチームにすると良い。
# よって答えを最大化する2番手は、[N+1, N+3, N+5, ...]
best_second_players = []
flag = True
for i in range(3 * N):
    if i < N:
        continue
    elif flag == True:
        best_second_players.append(a[i])
        flag = False
    else:
        flag = True
print(sum(best_second_players))
