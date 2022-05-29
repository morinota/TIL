# 姉と以下のようなゲームをしている。
# - 1. 最初、何もかいてない紙がある。
# - 2. 姉が一つ数字を言う(順にA_1~A_N)。その数字が紙に書いてあれば紙からその数字を消し、書いてなければその数字を紙に書く。これをＮ回繰り返す。
# -3. その後、紙に書かれている数字がいくつあるかを答える。

from collections import Counter

N = int(input())
A = [0] * N
for i in range(N):
    A[i] = int(input())

# 戦略
# Aのユニークな数字とその出現回数を求める。
# 各出現回数が偶数回であれば、最終的に残らない。奇数回であれば最終的に紙に残る。
# =>出現回数が奇数回をカウントすれば、それが答え。
A_unique = Counter(A)  # ->dictみたいに使える！
count_kisuukai = 0
for i in A_unique.keys():
    if A_unique[i] % 2 != 0:
        count_kisuukai += 1

print(count_kisuukai)
