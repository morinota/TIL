# すぬけ君は 1,2,3 の番号がついた 3 つのマスからなるマス目を持っています。 
# 各マスには 0 か 1 が書かれており、マス i には s i ​ が書かれています。 
# すぬけ君は 1 が書かれたマスにビー玉を置きます。
#  ビー玉が置かれるマスがいくつあるか求めてください。

# 整数の入力
from itertools import count

s_1, s_2, s_3 = map(int, list(input()))

print(s_1+s_2+s_3)