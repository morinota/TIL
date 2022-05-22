# 標準入力
S = input()

divide = ["dream", "dreamer", "erase", "eraser"]

# 後ろから解く代わりに、全ての文字列を「左右反転」する
S = S[::-1]
for i in range(4):
    divide[i] = divide[i][::-1]

# 端から切っていく
can: bool = True

i = 0
while i < len(S):
    can2: bool = False  # 4個の文字列達のどれかでdivideできるか
    for j in range(4):
        d: str = divide[j]
        if S[i : i + len(d)] == d:  # dでdivideできるか
            can2 = True
            i += len(d)  # divide できたら i を進める
            break  # 再度4個の文字列を探索へ

    if can2 == False:  # どれでもdivideできなかったら
        can = False
        break  # その時点で終了

if can:
    print("YES")
else:
    print("NO")
