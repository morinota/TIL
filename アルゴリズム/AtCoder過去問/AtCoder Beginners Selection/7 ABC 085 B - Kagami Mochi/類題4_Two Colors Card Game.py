# 青いカードN枚と赤いカードM枚を持っている。
# i枚目の青いカードには文字列s_i
# i枚目の赤いカードには文字列t_i
# 文字列を1つ言う。そして全てのカードを確認し、その文字列が書かれた青いカードを1枚見つける毎に1円貰える。
# 一方で、その文字列が書かれた赤いカードを見つける毎に1円失う。
# なお、文字列は完全一致。
# 最大で差し引き何円貰う事ができるか？ただし、違うカードに同じ文字列が書かれている事がある。
# また1つも存在しない文字列を言う事も出来る＝0円！


N = int(input())  # 標準入力
s = [""] * N
for i in range(N):
    s[i] = input()
M = int(input())
t = [""] * M
for i in range(M):
    t[i] = input()

# Xが最大になるのは、「青カードの文字列sの数」-「赤カードの文字列sの数」が最大になる時。
# ユニークな文字列を取得する
unique_strings = set()
for string in s + t:
    unique_strings.add(string)

backet_dict = {key: 0 for key in unique_strings}  # バケットを作る
for string in s:
    backet_dict[string] += 1
for string in t:
    backet_dict[string] -= 1

if max(backet_dict.values()) <= 0:
    print(0)
else:
    print(max(backet_dict.values()))
