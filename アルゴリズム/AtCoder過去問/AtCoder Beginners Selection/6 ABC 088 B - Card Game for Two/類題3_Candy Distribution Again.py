# N人の子供がいる。x個のお菓子を子供達に配る。
# x個のお菓子を全て配りきらなければならない。
# お菓子を貰わない子供がいてもOK。
# 子供iはちょうどa_i個のお菓子を貰うと喜ぶ。
# 喜ぶ子供の人数の最大値を出力せよ。

# 標準入力を受け取る

N, x = map(int, input().split())
a = list(map(int, input().split()))

a.sort(reverse=False)  # 喜ぶハードルが小さい順にソート

max_k = 0
if x == sum(a):  # 答えがNになるのはこの条件だけ
    max_k = N
elif x > sum(a):  # この条件の場合は一人に残りのお菓子を押しつける.
    max_k = N - 1
else:
    for i in range(N):  # 喜ぶハードルが大きい何人を除外していくか
        if x >= sum(a[0 : N - i]):
            max_k = N - i
            break

print(max_k)
