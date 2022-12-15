# 問題文
# N本の棒を持っている。i番目の棒の長さはl_i
# K本の棒を選んで繋げて、蛇のおもちゃを作りたい。
# 蛇のおもちゃの長さは選んだ棒達の長さの総和で表される。
# 蛇のおもちゃの長さとしてありえる長さのうち、最大値を求めなさい.

# 標準入力を受け取る
N, K = map(int, input().split())
l = list(map(int, input().split()))

l.sort(reverse=True)  # 長い順にソート

max = sum(l[0:K])
print(max)
