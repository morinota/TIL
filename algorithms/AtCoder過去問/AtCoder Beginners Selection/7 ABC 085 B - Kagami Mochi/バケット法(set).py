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
num = set()

for i in range(N):
    num.add(d[i]) # d[i]をsetに追加

# 答えを格納
res = len(num)

print(res)
