# nums = list(map(int, list(input())))
nums = input()  # eval使う用に、strのまま読み込む

# +-を差し込む隙間の数
op_cnt = len(nums) - 1
for i in range(2**op_cnt):  # 2^n通り
    # i番目のoptionの初期値を設定
    op_i = ["-"] * op_cnt

    # option iに対して、+-を取得(0->-, 1->+)
    for j in range(op_cnt):
        if (i >> j) & 1:  # iを2進数とみなしたbit演算子
            op_i[op_cnt - 1 - j] = "+"

    # 実際に計算
    formula = ""
    for p_num, p_op in zip(nums, op_i + [""]):
        formula += p_num + p_op

    # formulaが7と一致するかチェック
    if eval(formula) == 7:  # 文字列のプログラムをevalで実行
        print(formula + "=7")
        break
