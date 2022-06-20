# https://atcoder.jp/contests/joi2008yo/tasks/joi2008yo_a


payment = int(input())

coins = [500, 100, 50, 10, 5, 1]
# 降順にソート
coins = sorted(coins, reverse=True)

# まずお釣りを計算
pay_back = 1000 - payment
answer = 0
for coin in coins:
    use_num = pay_back // coin  # 商を取得=>coin円を使用する枚数
    pay_back -= coin * use_num
    answer += use_num

print(answer)
