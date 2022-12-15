from typing import List

# 3つの整数A,B,Cが与えられる。
# 以下の2種の操作を好きな順で繰り替えして、
# A,B,Cを全て等しくする為に必要な操作の最小回数を求めよ
# - 操作1: A,B,Cのうち2つを選んで、その両方を1増やす
# - 操作2: A,B,Cのうち1つを選んで、その整数を2増やす

# 制約 0 <= A,B,C <= 50

list_int = list(map(int, input().split()))


def judge_int_list(list_int: List):
    max_int = max(list_int)
    return (
        (list_int[0] == max_int) + (list_int[1] == max_int) + (list_int[2] == max_int)
    )


# 戦略
# 操作は「増やす」系のみ=>3つの整数が等しくなるのは、3つの内、最大の整数(M)以上。
# =>3つの内、Mに合わせて、他の二つを増やしていく？
# もし3つの整数の偶奇が等しければ、操作1=>操作2の順でクリア =>最後はM
# そうでなければ、操作1=>操作2=>操作1(１回) =>最後はM+1

operate_count = 0


while judge_int_list(list_int) < 3:
    max_int = max(list_int)  # A,B,Cのうち最大の整数を取得
    max_int_index = list_int.index(max_int)  # それがA,B,Cのどれか
    while judge_int_list(list_int) < 2:
        # 2つを増やす
        operate_count += 1
        for i in range(0, 3):
            if list_int[i] == max_int:
                continue
            list_int[i] += 1

    if judge_int_list(list_int) == 3:
        break

    # 3つのうち2つが合致したら、残り1つを+2為ていく
    operate_count += 1
    for i in range(0, 3):
        if list_int[i] == max_int:
            continue
        list_int[i] += 2

print(operate_count)
