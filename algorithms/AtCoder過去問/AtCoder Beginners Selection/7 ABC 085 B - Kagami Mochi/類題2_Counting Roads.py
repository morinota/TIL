# N個の都市があり、M本の道路がある。
# i番目の道路は、都市a_iと都市b_iを双方向に結んでいる。
# 同じ2つの都市を結ぶ道路は、一本とは限らない。
# 各都市iから他の都市に向けて、何本の道路が伸びているか求めよ。
# 出力はN行。i行目には、都市iから他の都市に向けて、何本の道路が延びているか。

# 標準入力
N, M = map(int, input().split())
a, b = [0] * M, [0] * M
for j in range(M):
    a[j], b[j] = map(int, input().split())

# 各都市i(1~N)から伸びている道路の本数を記録する配列＝バケットを用意
backet_list = [0] * N

for a_j, b_j in zip(a, b):
    backet_list[a_j - 1] += 1  # indexは0からなので.
    backet_list[b_j - 1] += 1

for answer in backet_list:
    print(answer)
