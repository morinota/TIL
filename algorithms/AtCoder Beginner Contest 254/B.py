from copy import copy


N = int(input())

# Aiの長さはi+1
# 各i, j(j<=i)について、Ａ_iのj+1番目の値a_ijは次のように定められる.

for i in range(N):
    A_i = [0] * (i+1)
    for j in range(i+1):
        if j==0 or j==i:
            A_i[j] = 1
        else:
            A_i[j] = A_i_1[j-1] + A_i_1[j]
    print(' '.join([str(v) for v in A_i]))
    A_i_1 = copy(A_i)



