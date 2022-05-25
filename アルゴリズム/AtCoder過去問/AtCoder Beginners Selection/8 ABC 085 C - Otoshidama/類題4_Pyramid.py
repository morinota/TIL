# ピラミッドには中心座標(C_x, C_y)と高さHが定まっており、
# 座標(X,Y)の高度はmax(H-|X-C_x|-|Y-C_y|, 0)であった。
# このピラミッドの中心座標と高さを求める為に調査を行い、以下の情報が得られた
# - C_x, C_yは0以上100以下の整数。Hは1以上の整数。
# 上記と別にN個の情報が得られた。そのうちi個目の情報は
# 「座標(x_i, y_i)の高度はh_iである。」
# 情報を元に、C_x, C_y, Hを求めよ。
N = int(input())  # 標準入力
P = []
for i in range(N):
    x, y, h = map(int, input().split())
    P.append([h, x, y])
P.sort(reverse=True)  # hの降順で観測値をソート


def calc_H(c_x, c_y, x, y, h) -> int:
    return h + abs(c_x - x) + abs(c_y - y)


# Hは上限がない=>C_xとC_yで全探索していけばいい！
for C_x in range(0, 101):
    for C_y in range(0, 101):
        for i in range(N):
            X, Y, h_actual = P[i][1], P[i][2], P[i][0]
            if i == 0:
                H_ori = calc_H(C_x, C_y, X, Y, h_actual)

            # 最終的なチェックは、h_iとして比較！(Hで比較だとダメだった...)
            elif max(H_ori - abs(C_x - X) - abs(C_y - Y), 0) != h_actual:
                break
        else:  # breakされずに最後までいけば...
            print(f"{C_x} {C_y} {H_ori}")
