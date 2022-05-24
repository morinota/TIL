# N個のボールを持っている。
# 最初、i番目のボールには整数A_iが書かれている。
# いくつかのボールに書かれている整数を書き換える事で、
# N個のボールに書かれている整数がK種類以下になるようにしたい。
# 少なくとも何個のボールの整数を書き換える必要があるか？？

# 標準入力
N, K = map(int, input().split())
A = list(map(int, input().split()))

# ユニーク値をK以下にするには、出現数の少ない整数を
# 出現数の多い整数に書き換えるのが効率的！

unique_int = set(i for i in A)
backet_dict = {key: 0 for key in unique_int}  # 各整数の出現回数を計るバケットを作る。

for integer in A:
    backet_dict[integer] += 1  # バケットにカウントしていく

list_sorted = sorted(backet_dict.values(), reverse=False)  # 昇順でソート
print(sum(list_sorted[0 : (len(unique_int) - K)]))
