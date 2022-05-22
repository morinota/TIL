# 整数 a,b,cと、文字列 s が与えられます。
#  a+b+c の計算結果と、文字列 s を並べて表示しなさい。

# -*- coding: utf-8 -*-
# 整数の入力
a = int(input())
# スペース区切りの整数の入力
b, c = map(int, input().split())
# 文字列の入力
s = input()
# 出力
# print("{} {}".format(a+b+c, s))
print(f"{a+b+c} {s}")
