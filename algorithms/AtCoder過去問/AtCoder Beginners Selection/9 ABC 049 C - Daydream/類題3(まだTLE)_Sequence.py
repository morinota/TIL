# 長さNの数列があり、i番目の数はa_i
# あなたは一回の操作で、どれか一つの要素の値を+1or-1できる。
# 以下の条件を満たす為に必要な操作回数の最小値を求めよ。
# - 全てのi(1~n)に対し、a_1~a_iまでの和は0でない。
# - 全てのi(1~n-1)に対し、i項までの和と、i+1までの和の符号が異なる。

# 標準入力
n = int(input())
a_original = list(map(int, input().split()))

# 方針
# 端っこから順に考えると芋づる式に全体が決まっていくタイプの問題かも...!=>Greety性ある？
# 偶数番目と奇数番目どちらを正にするかで2通り考え、小さい方を答える事にする。
# sum(a[0:i])が欲しい符号と同じ場合、i番目の数を変更する必要はない。
# sum(a[0:i])が欲しい符号と異なる場合、まず欲しい符号のうち絶対値最小までは変更しないと行けない.
# =>(1か-1)

# 偶数項が+のケース
total_count_operate_patten1 = 0
a_pattern1 = a_original.copy()
next_desiable_sign = True  # True=>+, False =>-と定義
for i in range(n):
    if next_desiable_sign == True:
        while sum(a_pattern1[0 : i + 1]) <= 0:
            # 地道に足す作戦だと、TLEになる！
            # a[i] += 1  # ＋になるまで足す.
            # count_operate += 1  # 回数を記録していく
            # +1になるように、a[i]に数値を足す。
            count_operate = 1 - sum(a_pattern1[0 : i + 1])
            a_pattern1[i] += count_operate
            total_count_operate_patten1 += count_operate
    elif next_desiable_sign == False:
        while sum(a_pattern1[0 : i + 1]) >= 0:
            # 地道に引く作戦だと、TLEになる！
            # a[i] -= 1  # ＋になるまで足す.
            # total_count_operate += 1  # 回数を記録していく
            count_operate = sum(a_pattern1[0 : i + 1]) + 1
            a_pattern1[i] -= count_operate
            total_count_operate_patten1 += count_operate

    next_desiable_sign = not next_desiable_sign  # 「欲しい符号」も反転

# 偶数項が-のケース
a_pattern2 = a_original.copy()
total_count_operate_patten2 = 0
next_desiable_sign = False  # True=>+, False =>-と定義
for i in range(n):
    if next_desiable_sign == True:
        while sum(a_pattern2[0 : i + 1]) <= 0:
            # 地道に足す作戦だと、TLEになる！
            # a[i] += 1  # ＋になるまで足す.
            # count_operate += 1  # 回数を記録していく
            # +1になるように、a[i]に数値を足す。
            count_operate = 1 - sum(a_pattern2[0 : i + 1])
            a_pattern2[i] += count_operate
            total_count_operate_patten2 += count_operate
    elif next_desiable_sign == False:
        while sum(a_pattern2[0 : i + 1]) >= 0:
            # 地道に引く作戦だと、TLEになる！
            # a[i] -= 1  # ＋になるまで足す.
            # total_count_operate += 1  # 回数を記録していく
            count_operate = sum(a_pattern2[0 : i + 1]) + 1
            a_pattern2[i] -= count_operate
            total_count_operate_patten2 += count_operate

    next_desiable_sign = not next_desiable_sign  # 「欲しい符号」も反転

print(min(total_count_operate_patten1, total_count_operate_patten2))
