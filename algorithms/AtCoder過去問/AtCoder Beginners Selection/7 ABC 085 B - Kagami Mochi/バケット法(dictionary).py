# N個の整数d[0],d[1],…,d[N−1] が与えられます。
# この中に何種類の異なる値があるでしょうか？

# 標準入力
N = int(input())
d = []
for i in range(N):
    d.append(int(input()))

# バケット
num = {}
for i in range(N):
    if d[i] not in num.keys():
        num[d[i]] = 1
    else:
        num[d[i]] = num[d[i]] + 1 # d[i] が 1 個増える

# 答えを格納
res = 0
for i in range(len(num.keys())):
    if num[d[i]] > 0:
        res+=1

print(res)


