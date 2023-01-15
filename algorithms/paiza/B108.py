# coding: utf-8
# 自分の得意な言語で
# Let's チャレンジ！！
from collections import deque
from dataclasses import dataclass
from typing import List


@dataclass
class Gondora:
    capacity: int
    ride_log: List[int]
    idx: int

    def get_total_ride(self) -> int:
        return sum(self.ride_log)


def answer(capa_list: List[int], waiting_customer_nums: List[int]) -> None:
    """返り値は各ゴンドラのトータルの乗車人数"""

    gondra_queue = deque(
        [
            Gondora(
                capacity,
                [],
                idx,
            )
            for idx, capacity in enumerate(capa_list)
        ]
    )  # ゴンドラを初期化

    customers_queue = deque([num for num in waiting_customer_nums])

    while customers_queue:  # 待ってる乗客
        # キューから客を一つ取り出す
        customers_num = customers_queue.popleft()
        while customers_num > 0:
            gondora = gondra_queue.popleft()  # 先頭のゴンドラを一つ取り出す
            if gondora.capacity >= customers_num:  # 全員乗って次の顧客へ
                gondora.ride_log.append(customers_num)  # ログへ登録
                customers_num -= gondora.capacity
            elif gondora.capacity < customers_num:  # 一部が乗って、残りは次へ
                gondora.ride_log.append(gondora.capacity)  # ログへ登録
                customers_num -= gondora.capacity

            gondra_queue.append(gondora)  # 先頭のゴンドラを再度最後尾へ

    # gondra_dequeを並び替える
    while True:
        gondra = gondra_queue.popleft()
        if gondra.idx == 0:
            gondra_queue.appendleft(gondora)
            break
        else:
            gondra_queue.append(gondra)  # 後ろへ回して次へ

    # 回答
    for gondora in gondra_queue:
        print(gondora.get_total_ride())


if __name__ == "__main__":
    n, m = map(int, input().split())  # ゴンドラ数n, 観覧車に乗りたい客m組
    a_list = [int(input()) for _ in range(n)]  # 各ゴンドラの収容人数a
    b_list = [int(input()) for _ in range(m)]  # 各客グループの人数b
    answer(a_list, b_list)
