import numpy as np

R, C = map(int, input().split())
A = np.zeros(shape=(2, 2))


A[0, 0], A[0, 1] = map(int, input().split())
A[1, 0], A[1, 1] = map(int, input().split())
print(int(A[R - 1, C - 1]))
