# xy平面上に、左下(0,0), 右上(W, H)で、
# 各辺がx軸かy軸に平行な長方形がある。
# 最初、長方形の内部は白く塗られている。
# すぬけ君はこの長方形の中にN個の点を打った。
# i個目の点の座標は(x_i, y_i)
# また、長さNの数列aを決めて、各iに対して、以下の領域を黒く塗りつぶす。
# - a_i =1 の時は長方形のx<x_iを満たす領域
# - a_i =2 の時は長方形のx>x_iを満たす領域
# - a_i =3 の時は長方形のy<y_iを満たす領域
# - a_i =4 の時は長方形のy>y_iを満たす領域

# 出力：塗りつぶしが終わった後の長方形内での白い部分の面積を出力せよ
import numpy as np

# 標準入力
W, H, N = map(int, input().split())
x, y, a = [0] * N, [0] * N, [0] * N
for i in range(N):
    x[i], y[i], a[i] = map(int, input().split())

# 二次元のバケットを用意する。
backet_array = np.array([[1] * W] * H)  # W=H=2だったら[[1,1],[1,1]]
for i in range(N):
    if a[i] == 1:
        backet_array[:, : x[i]] = 0  # [H, W]
    elif a[i] == 2:
        backet_array[:, x[i] :] = 0  # [H, W]
    elif a[i] == 3:
        backet_array[H - y[i] :, :] = 0  # [H, W]
    elif a[i] == 4:
        backet_array[: H - y[i], :] = 0  # [H, W]
print(backet_array.sum())
