# N個の整数d[0],d[1],…,d[N−1] が与えられます。
# この中に何種類の異なる値があるでしょうか？

# 標準入力
N = int(input())
d = []
for i in range(N):
    d.append(int(input()))

# Nの制約
d_i_max = 100

# 空のバケットを用意
num = [0] * (d_i_max+10)


for i in range(N):
    num[d[i]] += 1 # d[i] が 1 個増える

# 答えを格納
res = 0
for i in range(d_i_max+10):
    if num[i] > 0:
        res+=1

print(res)


