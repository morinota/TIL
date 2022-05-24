# 英小文字からなる文字列Sが与えられる。
# Sに現われない英子文字であって、最も辞書順で小さいものを求めよ。
# ただし、Sに全ての英子文字が現われる場合は、代わりにNoneを出力してください。

import string

# 標準入力
S = input()

# 英子文字26種類のそれぞれについて、Sの中に現れるかを記録する配列=バケットを用意.
alphabet_list = list(string.ascii_lowercase)
backet_dict = {key: False for key in alphabet_list}

for s in S:
    backet_dict[s] = True

answer = "None"
for k, v in backet_dict.items():
    if v == False:
        answer = k
        break
print(answer)
