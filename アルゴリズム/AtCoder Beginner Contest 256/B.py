N = int(input())
A = list(map(int, input().split()))

# 整数P
P = 0
koma_list = []  # 座標を格納する


def operate_2(A_i: int):
    return


for i in range(N):
    # 操作1
    koma_list.append(0)
    # 操作2
    koma_list = list(map(lambda x: x + A[i], koma_list))

    # Pに加算
    koma_list_new = []
    for j in range(len(koma_list)):
        if koma_list[j] >= 4:
            P += 1
        else:
            koma_list_new.append(koma_list[j])

    koma_list = koma_list_new.copy()

print(P)
