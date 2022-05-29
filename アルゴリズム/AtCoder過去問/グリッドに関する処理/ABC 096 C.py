# H * Wのマス目が与えらえる。
# 上から i 番目, 左から j 番目のマスを (i,j) と表します.
# 最初, すべてのマス目は白色.黒い絵の具を使って絵を描きたい.
# 具体的には、s_ij=#の時は黒色。s_ij = .の時は白色にしたい。
# しかし, 彼は絵を描くことが得意ではないので, 何回か (0 回でもよい)「上下左右に隣接する 2 つのマスを選び, 両方黒く塗る」ことしかできません.
# ただし, すでに黒く塗られているマスを選ぶこともでき, この場合マスの色は黒のまま変わりません.
# 目標を達成することができるか判定せよ。


H, W = map(int, input().split())
S = [""] * H
for i in range(H):
    S[i] = list(input())  # str=>list

# 制約:1<=H, W<=50
# 50*50くらいなら線形探索できそう?

# 作戦：
# まずは「達成できない場合を考える」=>上下左右に隣り合うマスに黒いマスがない、黒いマス」があるかないか！＝＞あれば失敗。なければ成功！
def check_masu(i, j) -> bool:
    black_count_neighbor = 0
    # 4方向を一つずつチェック
    # 上
    if i != 0 and S[i - 1][j] == "#":
        black_count_neighbor += 1
    # 右
    if j != W - 1 and S[i][j + 1] == "#":
        black_count_neighbor += 1
    # 下
    if i != H - 1 and S[i + 1][j] == "#":
        black_count_neighbor += 1
    # 左
    if j != 0 and S[i][j - 1] == "#":
        black_count_neighbor += 1
    if black_count_neighbor >= 1:
        return True
    else:
        return False


answer = "Yes"
for i in range(H):
    for j in range(W):
        if S[i][j] == ".":
            pass
        else:
            if check_masu(i, j) is False:
                answer = "No"
                break
    else:
        continue
    break


print(answer)
