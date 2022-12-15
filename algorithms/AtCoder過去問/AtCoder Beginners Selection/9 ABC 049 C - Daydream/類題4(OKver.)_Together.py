# 長さNの整数列a_1, ..., a_Nが与えられる。
# 各iに対し、a_iに1足すか、1引くか、何もしないかの3つの操作からどれか一つを選んで行う。
# この操作の後、ある整数Xを選んで、a_i=Xとなるiの個数を数える。
# 上手く操作を行い、Xを選ぶ事で、この個数を最大化せよ。

# 制約
# 1<= N<= 10**5
# 0 <= a_i <= 10^5

from collections import Counter

N = int(input())
a = list(map(int, input().split()))

# 制約より1≤N≤10^5
# =>よって線形探索(1重)しても2秒以内には間に合いそう。

# Xを決めると、Greedyに(芋づる式)に全て決まるみたい...!
# Xの値を決めると、求める個数は
# Aの中の (X-1の個数) + (Xの個数) + (X+1の個数)になる。
# 従って先に各数の個数を数えておき、Xを全て試す事で答えが決まる。

unique_counts_a = Counter(a)  # リスト内のすべての一意な値と数のdictを取得

answer = 0
for X in range(0, max(a) + 1):
    count = unique_counts_a[X] + unique_counts_a[X - 1] + unique_counts_a[X + 1]

    answer = max(count, answer)

print(answer)
