N, K = map(int, input().split())
a = list(map(int, input().split()))

# 正解となるソートされたaを用意しておく
a_sorted = sorted(a, reverse=False)

gap = K
answer = "Yes"


# timeoutになる＝＞swappableは続くけど、クリアできない状態??
# 後半部分が問題??
swappable = True
while swappable == True:
    if gap == 1:
        break
    swappted_count = 0
    for i in range(0, N - gap):  # とりあえずaを一周
        if a[i] > a[i + gap]:
            a[i], a[i + gap] = a[i + gap], a[i]  # 入れ替える
            swappted_count += 1
    else:  # 一周終わった時点で.
        if a == a_sorted:  # 一致したらクリア
            answer = "Yes"
            swappable = False
            break
        if swappted_count == 0:  # もし一回も交換できてなかったら諦める。
            swappable = False
            answer = "No"
            break


print(answer)
