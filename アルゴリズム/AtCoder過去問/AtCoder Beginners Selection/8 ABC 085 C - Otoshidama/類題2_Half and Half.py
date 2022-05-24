# Aピザ、Bピザ、ABピザの三種類のメニュー
# AピザとBピザは全く異なるピザで、
# これらをそれぞれ半分に切って組み合わせたものがABピザ。
# 値段はそれぞれA円、B円、C円

# 中橋君は、今夜のパーティの為にAピザX枚とBピザY枚を用意する必要がある。
# これらのピザを入手する方法は、AピザやBピザを直接買うorABピザ2枚買って組み替える。
# この為に最小で何円が必要になるか？
# なお、ピザの組み替えにより、必要な量を超えたピザが発生してもOK。

# 制約
# A, B, C <= 5000
# X, Y <= 10^5

# 標準入力
from subprocess import TimeoutExpired


A, B, C, X, Y = map(int, input().split())
# 方針
# => AピザBピザ, ABセット(2枚1セット)のどれについても、買う個数は10^5個以下で良い。
# =>従って、この三種類のうちどれか一種類で、買う個数を0~10万まで全て試す方針！
# ではどれについて全探索すべきか?=>ABセット。
# ABセットをi個購入した場合、
# - i>=XであればAピザを買い足す必要なし.
# - i < X であれば、AピザをX-i 個買い足す必要がある。
# - 同様に、i>=Y であればBピザを買い足す必要なし。
# - i< Y であれば、BピザをY - i個買い足す
# - この時の合計金額はi*2C+ max(0, X-i)*A + + max(0, Y-i)*B円

min_total_price: int
# ABセットをiセット買う場合の合計金額を探索する
for i in range(0, 10**5 + 1):
    total_price = i * 2 * C + max(0, X - i) * A + max(0, Y - i) * B
    if i == 0:
        min_total_price = total_price
    if min_total_price > total_price:
        min_total_price = total_price
print(min_total_price)
