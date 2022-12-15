# 1以上N以下の整数のうち、
# 10進法で各桁の和がA以上B以下であるものについて、総和を求めてください。

def find_sum_of_digits(n:int):
    """各桁の和を計算する関数

    Parameters
    ----------
    num : int
        _description_
    """
    # 各桁の和
    sum_digits = 0
    while (n > 0) :
        # num(10進数)のiの位を取得して足す
        sum_digits += n % 10
        # num(10進数)からiの位を取り除く
        n = n // 10

    return sum_digits

N, A, B= map(int, input().split())

total = 0
# 整数を1つずつ
for n in range(1, N+1):
     
    if (find_sum_of_digits(n) >= A) and (find_sum_of_digits(n) <= B):
        total += n

print(total)