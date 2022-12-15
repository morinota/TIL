# Alice は Bob より何点多くの得点を獲得できるか

# 標準入力を受け取る
N = int(input())
a = list(map(int, input().split()))

# 最適戦略＝＞二人とも、残っているカードの中から最も大きい値を取れば良い。
# ＝＞aを降順にソートして、偶数奇数のindexの値の合計値の差をとればよい

a.sort(reverse=True) # ソート

Alice, Bob = 0, 0
for i in range(N):
    if (i % 2) == 0: # Aliceのターン
        Alice += a[i]
    else: # Bobのターン
        Bob += a[i]

print(Alice - Bob)


