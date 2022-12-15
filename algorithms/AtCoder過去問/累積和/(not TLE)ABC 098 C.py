# N 人の人が東西方向(西が左と仮定する笑)に一列に並んでいます。それぞれの人は、東または西を向いています。
# 誰がどの方向を向いているかは長さ N の文字列 Sによって与えられます。
# あなたは、N 人のうち誰か 1 人をリーダーとして任命します。 そして、リーダー以外の全員に、リーダーの方向を向くように命令します。 このとき、リーダーはどちらの方向を向いていても構いません。
# 並んでいる人は、向く方向を変えるのを嫌っています。 そのためあなたは、向く方向を変える人数が最小になるようにリーダーを選びたいです。
# 向く方向を変える人数の最小値を求めてください。

from collections import Counter

# 制約 2<=N<=3 * 10**5
N = int(input())
S = list(input())
# 作戦
# リーダーのindexをi_lとすると、i<i_lは全員E(right)を向く。i>i_lは全員Wを向く。
int_s = [0] * N
cum_sum_w = [0] * (N + 1)
cum_sum_e = [0] * (N + 1)
answers = [0] * N

# 「西を向いている人数」と「東を向いている人数」の累積和を予め求めておく。
for i in range(N):  # i = 0~iの範囲で「西を向いている人数」
    if S[i] == "W":
        int_s[i] = 1
    else:
        int_s[i] = 0
    cum_sum_w[i + 1] = cum_sum_w[i] + int_s[i]
    
for i in range(N):  # i = 0~iの範囲で「東を向いている人数」
    if S[i] == "E":
        int_s[i] = 1
    else:
        int_s[i] = 0
    cum_sum_e[i + 1] = cum_sum_e[i] + int_s[i]

for i in range(N):
    # i<i_lのWの人数 + (Eの人数 - i <i_lのEの人数)
    answers[i] = cum_sum_w[i] + (cum_sum_e[N] - cum_sum_e[i + 1])
print(min(answers))
