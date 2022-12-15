# 3*3のグリッドがある。
# 上からi番目で左からj番目のマスを(i,j)で表す時、マス(i,j)には数c_ijが書かれている。
# 高橋君によると、整数a_1, a_2, a_3, b_1, b_2, b_3の値が決まっており、
# マス(i,j)には数「a_i+b_j」が書かれているらしい。
# 高橋君の情報が正しいか判定しなさい。
# 制約c_ij 0以上100以下の整数 => a_iは0~99
import numpy as np

# 標準入力
c = [[0] * 3] * 3
c = np.array(c)
c[0, :] = list(map(int, input().split()))
c[1, :] = list(map(int, input().split()))
c[2, :] = list(map(int, input().split()))

# 方針:
# a_1が決まれば入力c_1jを使ってb_1, b_2, b_3の値が定まる。
# そのb_1, b_2, b_3の値を使ってa_2, a_3の値を3通り求める事ができる。
# a_2, a_3の3通りの値がそれぞれ全て一致したらYes, 一致しなかったらNoを出力する。
answer = "No"
for a_1 in range(0, 101):  # 線形探索
    b_1, b_2, b_3 = c[0, 0] - a_1, c[0, 1] - a_1, c[0, 2] - a_1

    a_2_by_b_1 = c[1, 0] - b_1
    a_2_by_b_2 = c[1, 1] - b_2
    a_2_by_b_3 = c[1, 2] - b_3
    a_3_by_b_1 = c[2, 0] - b_1
    a_3_by_b_2 = c[2, 1] - b_2
    a_3_by_b_3 = c[2, 2] - b_3

    if a_2_by_b_1 == a_2_by_b_2 == a_2_by_b_3:
        if a_3_by_b_1 == a_3_by_b_2 == a_3_by_b_3:
            answer = "Yes"
            break
print(answer)
