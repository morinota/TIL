import math

N, K = map(int, input().split())

A = list(map(int, input().split()))
X, Y = [0] * N, [0] * N
for i in range(N):
    X[i], Y[i] = map(int, input().split())

R = 0  # 初期値

# 方針
# 「明かりを持ってる人」と「持ってない人」の中で、最短の距離を考える。
# 全ての「持ってない人」に対して、「明かりを持っている人」との"最短の距離"を考える。それを記録していく。
# "最短の距離"のうち、最も大きい値がRの最小値.


def calc_distance(x_1, y_1, x_2, y_2):
    return math.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)


min_distance_list = []
for i in range(N):
    # もし明かりを持ってる人だったら...
    if i + 1 in A:
        continue
    else:
        # 「明かりを持っている人」との"最短の距離"を考える。
        min_distance = 100000000
        for j in A:
            distance = calc_distance(X[i], Y[i], X[j - 1], Y[j - 1])
            min_distance = min(min_distance, distance)

        min_distance_list.append(min_distance)

answer = max(min_distance_list)
print(answer)
