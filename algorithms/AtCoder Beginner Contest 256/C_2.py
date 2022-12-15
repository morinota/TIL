import numpy as np

inputs = list(map(int, input().split()))
H, W = inputs[0:3], inputs[3:]
del inputs

# 工夫したら全探索で行ける??

count = 0
for a in range(1, min(H[0], W[0]) - 2 + 1, 1):
    for b in range(1, min(H[0], W[0]) - 2 + 1, 1):
        for d in range(1, min(H[1], W[0]) - 2 + 1, 1):
            for e in range(1, min(H[1], W[1]) - 2 + 1, 1):
                c = H[0] - a - b
                f = H[1] - d - e
                g = W[0] - a - d
                h = W[1] - b - e

                # 条件として使っていないのはh[2]とw[2]
                # h[2]を使ってiを算出＝＞w[2]を満たしていればOK
                i = H[2] - g - h
                for x in [a, b, c, d, e, f, g, h, i]:
                    if x < 1 or x > 28:
                        break
                else:
                    if c + f + i == W[2]:
                        count += 1

print(count)
