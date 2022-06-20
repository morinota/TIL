import numpy as np

X, A, D, N = map(int, input().split())

S = []
answer = 0

# そもそも交差が0の場合
if D == 0:
    # 初項とXの差
    print(abs(X - A))

# 交差が非ゼロの場合
else:
    S_last = A + D * (N - 1)
    print(S_last)

    def judge_in_S(num) -> bool:

        if (num - A) % D == 0:
            return True
        else:
            return False

    # 正の等差行列において、行列の外側にXがある場合
    if D > 0 and (X >= S_last or X <= A):
        answer = min(abs(X - S_last), abs(A - X))
    # 負の等差行列において、行列の外側にXがある場合
    elif D < 0 and (X <= S_last or X >= A):
        answer = min(abs(S_last - X), abs(X - A))
    # 行列の内側にXがあり、且つすでにXがSに含まれる場合
    elif judge_in_S(X):
        answer = 0
    # 行列の内側にXがあり、且つXがSに含まれない場合
    else:
        # X の前後でSの要素となりうる整数を全探索していく(D <= 10^6なので 1重ループだったら１秒以内に行ける??)
        # Xの両サイドを近場から遠くへ探索していく。
        for diff in range(1, D + 1):
            if judge_in_S(X + diff):
                answer_1 = diff
                break
        for diff in range(1, D+1):
            if judge_in_S(X - diff):
                answer_2 = diff
                break

    print(answer)
