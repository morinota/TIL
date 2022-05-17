# あなたは、500 円玉を A 枚、100 円玉を B 枚、50 円玉を C 枚持っています。 
# これらの硬貨の中から何枚かを選び、合計金額をちょうど X 円にする方法は何通りありますか。
# 同じ種類の硬貨どうしは区別できません。
# 2通りの硬貨の選び方は、ある種類の硬貨についてその硬貨を選ぶ枚数が異なるとき区別されます。

A = int(input())
B = int(input())
C = int(input())
X = int(input())

ans = 0
for i in range(A+1):
    for j in range(B+1):
        for k in range(C+1):
            if 500 * i + 100 * j + 50 * k == X:
                ans+=1

print(ans)
