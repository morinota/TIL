# 長さNの整数列a_1, ..., a_Nが与えられる。
# 各iに対し、a_iに1足すか、1引くか、何もしないかの3つの操作からどれか一つを選んで行う。
# この操作の後、ある整数Xを選んで、a_i=Xとなるiの個数を数える。
# 上手く操作を行い、Xを選ぶ事で、この個数を最大化せよ。

# 制約
# 1<= N<= 10**5
# 0 <= a_i <= 10^5

N = int(input())
a = list(map(int, input().split()))

# 制約より1≤N≤10^5
# =>よって線形探索(1重)しても2秒以内には間に合いそう。

# Xを決めると、Greedyに(芋づる式)に全て決まるみたい...!
# X
answer = 0
for X in range(0, max(a) + 1):
    count = 0
    for i in range(N):
        dif = a[i] - X
        if dif == -1 or dif == 0 or dif == 1:
            count += 1

    answer = max(count, answer)

print(answer)