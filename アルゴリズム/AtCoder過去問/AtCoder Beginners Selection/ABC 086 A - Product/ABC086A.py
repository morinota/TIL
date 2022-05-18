# シカのAtCoDeerくんは二つの正整数 a,b を見つけました。
#  a と b の積が偶数か奇数か判定してください。
# 積が奇数なら Odd と、 偶数なら Even と出力せよ。

# スペース区切りの整数の入力
a, b = map(int, input().split())
if (a*b)%2 == 0:
    print('Even')
elif (a*b)%2 != 0:
    print('Odd')

