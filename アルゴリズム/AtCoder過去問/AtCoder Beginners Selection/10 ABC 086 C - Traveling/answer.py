# 標準入力
N = int(input())
t, x, y = [0] * (N + 10), [0] * (N + 10), [0] * (N + 10)

for i in range(1, N + 1):
    # i = 1 から格納していく.t[0]=x[0]=y[0]=0は固定
    t[i], x[i], y[i] = map(int, input().split())

flag: bool = True
for i in range(0, N):
    dt = t[i + 1] - t[i]  # 何秒間で?? = 速度が1m/sなので、即ち「移動できる距離」
    dist = abs(x[i + 1] - x[i]) + abs(y[i + 1] - y[i])  # 「移動したい距離」は??

    # 「移動できる距離」と「移動したい距離」の比較
    if dt < dist:
        flag = False
    # 「移動できる距離」と「移動したい距離」の偶奇の比較.
    elif dist % 2 != dt % 2:
        flag = False

if flag:
    print("Yes")
else:
    print("No")
