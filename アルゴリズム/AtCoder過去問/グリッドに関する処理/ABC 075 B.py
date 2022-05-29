# H * Wのマス目が与えらえる。
# 入力において、全てのマスは文字で表されており、.は空きマス。#は爆弾マスに対応する。
# マス目はH個の文字列S_1~S_Hで表される。
# S_iのj文字目は、マス目の上からi番目、左からj番目のマスに対応する。
# 各空きマスの上下左右及び斜めの8方向で隣接してるマスに爆弾マスが何個あるか気になっている。
# そこで、各空きマスに対応する.を、その空きマスの「周囲8方向に隣接するマスにおける爆弾マスの個数」を表す数字に置き換える事にした。
# 上記の規則で置き換えられた後のマス目を出力せよ

H, W = map(int, input().split())
S = [""] * H
for i in range(H):
    S[i] = list(input())  # str=>list

# S_ijは、S[i][j]で取得できる。

# 制約:1<=H, W<=50
# 作戦：
# 50*50=2500の線形探索(2重)でいけそう??


def count_bomb_num(i, j):
    bomb_count = 0
    # 8方向を一つずつ確認していく
    # 上
    if i != 0 and S[i - 1][j] == "#":
        bomb_count += 1
    # 左上
    if i != 0 and j != 0 and S[i - 1][j - 1] == "#":
        bomb_count += 1
    # 右上
    if i != 0 and j != W - 1 and S[i - 1][j + 1] == "#":
        bomb_count += 1
    # 右
    if j != W - 1 and S[i][j + 1] == "#":
        bomb_count += 1
    # 右下
    if i != H - 1 and j != W - 1 and S[i + 1][j + 1] == "#":
        bomb_count += 1
    # 下
    if i != H - 1 and S[i + 1][j] == "#":
        bomb_count += 1
    # 左下
    if i != H - 1 and j != 0 and S[i + 1][j - 1] == "#":
        bomb_count += 1
    # 左
    if j != 0 and S[i][j - 1] == "#":
        bomb_count += 1

    return str(bomb_count)


for i in range(H):
    for j in range(W):
        if S[i][j] == "#":
            pass  # 次のチェックへ
        else:
            S[i][j] = count_bomb_num(i, j)

for i in range(H):
    print("".join(S[i]))
