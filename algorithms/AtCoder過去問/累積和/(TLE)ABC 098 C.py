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
# N<=3 * 10**5なら線形探索できそう(確か10**8で1秒?)
min_num_change_direction = N - 1

num_change_direction_list = []
for i_l in range(N):
    num_change_direction = 0
    # i<i_lのWの人数をカウント
    count_W_i_less_than_i_l = Counter(S[0:i_l])["W"]

    # i >i_lのEの人数をカウント
    count_E_i_more_than_i_l = Counter(S[i_l + 1 :])["E"]
    num_change_direction_list.append(count_E_i_more_than_i_l + count_W_i_less_than_i_l)


print(min(num_change_direction_list))
