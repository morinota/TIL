# 特定の場所に誰かがチェックインした時刻とチェックアウトした時刻がログとして与えられる。
# このログに対するクエリを処理するプログラムを作成せよ。
# 各クエリでは場所と時刻が与えられるので、その時刻にその場所にいた人数をカウントせよ。
# ただし、チェックインした時刻およびチェックアウトした時刻もその場所にいたとしてカウントすること。
# 一つのクエリ内で、同じユーザを重複カウントしてはいけない

# 制約：1<=N<=10^3, 1<=Q<=10^3
# 利用可能メモリ：1GB
# 実行時間：10s (=>なんか線形探索できそう?)

# 出力：Q個のクエリに対する「答え」の最小値、最大値、最頻値、中央値を半角スペース区切りで標準出力。

import numpy as np
from typing import List


def median(l: List):
    half = len(l) // 2
    l.sort(reverse=False)
    if len(l) % 2 == 0:  # リストの長さが偶数の場合
        return (l[half - 1] + l[half]) / 2.0
    else:  # リストの長さが奇数の場合
        return l[half]


def mode(l: List):
    uniques, counts = np.unique(l, return_counts=True)
    mode_list = uniques[counts == np.amax(counts)]
    if len(mode_list) > 1:
        return min(mode_list)
    else:
        return mode_list[0]


def main():
    # ログ件数、クエリ件数
    N, Q = map(int, input().split())
    # N件のログ: ログID, 場所ID, チェックイン時刻(エポック秒), チェックアウト時刻(エポック秒)
    ID, X, S, T = [""] * N, [""] * N, [""] * N, [""] * N
    for i in range(N):
        ID[i], X[i], S[i], T[i] = input().split()
    # Q件のクエリ:場所ID, エポック秒
    A, B = [""] * Q, [""] * Q
    for j in range(Q):
        A[j], B[j] = input().split()

    # 作戦(10^3 * 10^3で線形探索しちゃう？)
    query_result_list = [0] * Q

    for query_idx in range(Q):
        query_count = 0
        query_user_list = []
        place_id = A[query_idx]
        time = B[query_idx]
        for log_idx in range(N):  # 各ログに対して線形探索
            if place_id != X[log_idx]:  # まずログの場所IDが異なっていたらcontinue
                continue
            if ID[log_idx] in query_user_list:
                continue
            if (S[log_idx] <= time) and (time <= T[log_idx]):
                query_count += 1
                query_user_list.append(ID[log_idx])
        else:
            query_result_list[query_idx] = query_count

    min_query_result = min(query_result_list)
    max_query_result = max(query_result_list)
    mode_query_result = mode(query_result_list)
    median_query_result = median(query_result_list)
    print(min_query_result, max_query_result, mode_query_result, median_query_result)


if __name__ == "__main__":
    main()
