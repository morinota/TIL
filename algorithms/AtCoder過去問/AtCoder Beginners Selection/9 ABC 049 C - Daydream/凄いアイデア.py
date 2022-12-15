# 標準入力

S = input()
divide = ["dream", "dreamer", "erase", "eraser"]
S = (
    S.replace(divide[0], "")
    .replace(divide[1], "")
    .replace(divide[2], "")
    .replace(divide[3], "")
)
print("YES" if len(S) == 0 else "NO")
