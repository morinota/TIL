# 問題文
# 与えられる文字列を好きな順番で全て結合してできる文字列のうち
# もっとも辞書順で小さいものを出力せよ。

# 標準入力を受け取る
N, L = map(int, input().split())
S = []
for i in range(N):
    S.append(input())

S.sort(reverse=False)  # 昇順でソート

answer = ""
for i in range(N):
    answer += S[i]

print(answer)
