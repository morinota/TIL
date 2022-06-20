import numpy as np

inputs = list(map(int, input().split()))
h, w = inputs[0:3], inputs[3:]
del inputs

# 工夫したら全探索で行ける??


def judge_(h, w, array: np.ndarray) -> int:
    if sum(array[0, :]) != h[0]:
        return 0
    if sum(array[1, :]) != h[1]:
        return 0
    if sum(array[2, :]) != h[2]:
        return 0
    if sum(array[:, 0]) != w[0]:
        return 0
    if sum(array[:, 1]) != w[1]:
        return 0
    if sum(array[:, 2]) != w[2]:
        return 0
    return 1


count = 0
for a in range(1, min(h[0], w[0]) - 2 + 1, 1):
    for b in range(1, min(h[1], w[1]) - 2 + 1, 1):
        for c in range(1, min(h[2], w[2]) - 2 + 1, 1):
            x_20 = (h[0] - w[2] + h[1] + h[2] - w[1]) / 2
            x_01 = (h[0] - w[2] + 2 * c + h[1] - 2 * b - w[0] - h[2] + w[1]) / (-2)
            x_02 = h[0] - a - x_01
            x_10 = w[0] - a - x_20
            x_12 = h[1] - b - x_10
            x_21 = w[1] - b - x_01
            if x_01 < 1 or x_10 < 1 or x_12 < 1 or x_02 < 1 or x_21 < 1 or x_20:
                continue
            check_list = [x_01, x_02, x_10, x_12, x_21, x_20]
            # 各要素が全て整数だったら条件クリア
            for x in check_list:
                if x % 1 != 0:
                    break
            else:
                count += 1


# 多分一つひとつ足し合わせるようじゃダメ。
print(count)
