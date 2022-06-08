import math

import itertools

# N = int(input())
N = 4
# 平方数＝整数の二乗で表される数
# 0 <= i,j<=N

# nまでの素数を表示させるプログラム
import math 

def sieve_of_eratosthenes(n): 
    candidate = [i for i in range(2, n+1)] 
    prime = []
    limit = math.sqrt(n) + 1 

    while True:
        p = min(candidate) 
        if limit <= p:
            prime.extend(candidate) 
            break
        prime.append(p) 

        candidate = [i for i in candidate if i % p != 0]
    
    return prime

primes = sieve_of_eratosthenes(int(math.sqrt(N))+1) # \sqrt(N)+1 以下の素数のリストを取得
print(primes)

count = 1 # 1 * 1を追加
count += len(primes) # (prime * prime)の分を追加
count += len(primes) # 1 * prime^2 を追加できる

# これ以降は、prime_1^2 * prime_2^2の組み合わせとか??
for prime_1 in primes:
    for prime_2 in r
# 後はこのprimeの各要素^2を組み合わせてできる数?
# count = 0
# while True:
# 平方数よりも素数の方が多いらしい...
# count = 0

# 
        