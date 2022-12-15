# 2×N のマス目があり、上から i 行目、左から j 列目 (1≤i≤2, 1≤j≤N) のマスをマス (i,j) と表す。
# はじめ、左上のマス (1,1) にいる。
# 右方向または下方向への移動を繰り返し、右下のマス (2,N)に移動したい。
# マス (i,j) には A_ij個のアメが置かれている。
# あなたは移動中に通ったマスに置いてあるアメをすべて回収する。
# 左上および右下のマスにもアメが置かれており、あなたはこれらのマスに置かれているアメも回収する。
# 移動方法をうまく選んだとき、最大で何個のアメを回収できるか?

# 制約:1<=N<=100

N = int(input())
A = [[0]] * 2
A[0] = list(map(int, input().split()))
A[1] = list(map(int, input().split()))

# 作戦
# ギザギザ進んで全マスを通れば最大？？=>右と下しか進めない。
# 2段なので「どのタイミングで下に進むか」に回答が依存する。
# (下に進むタイミングでは)A_1jとA_2j両方のアメを取得できる。
# 1<=N<=100でjを線形探索：余裕で1秒以内！

candies_count = 0
for j_drop in range(N):
    candies_count_each = 0
    i, j = 0, 0
    while j <= j_drop:
        candies_count_each += A[0][j]
        j += 1  # 右へ
    # 下に移動した瞬間
    candies_count_each += A[1][j - 1]
    while j >= j_drop and j < N:
        candies_count_each += A[1][j]
        j += 1  # 右へ
    if candies_count_each > candies_count:
        candies_count = candies_count_each

print(candies_count)
