# https://atcoder.jp/contests/arc061/tasks/arc061_a

# 2^n通りの全探索=>bit 全探索
S = input()
option_count = len(S) - 1

answer = 0
for i in range(2**option_count):  # 2^n通りのoptionがある。
    # i番目のoptionの初期値を設定(一つも+を差し込まない=>0000)
    option_i = [""] * option_count
    # i番目のoptionに対して、0 or 1を取得
    for j in range(option_count):
        if (i >> j) & 1:
            option_i[option_count - 1 - j] = "+"

    # option iのformulaを生成
    formula = ""
    for p_num, p_op in zip(S, option_i + [""]):
        formula += p_num + p_op

    # formulaの計算結果を取得, 足し合わせ
    answer += eval(formula)

print(answer)
