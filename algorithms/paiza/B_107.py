from collections import deque
from typing import Deque


def answer(card_num: int, set_num: int, shuffle_num: int) -> None:
    """n枚のカードには1~nまでの整数が重複なく並んでいる.
    初期状態ではiは上からi番目にある.
    シャッフル:
    - 重ねられたカードを上からm枚毎のセットに分ける. 一番下のセットがm枚未満の場合はそのまま.
    - 上からj番目のセットが、下からj番目のセットになるように並び替える.
    """
    cards = deque([num for num in range(1, card_num + 1)])  # 1~nのカードを作る.

    for _ in range(shuffle_num):
        cards = shuffle(
            cards,
            set_num,
        )

    # 回答
    for card in cards:
        print(card)


def shuffle(cards: Deque[int], set_num: int) -> Deque[int]:
    cards_shuffled = deque([])

    while cards:
        # i番目のセットの処理
        card_set = []
        for _ in range(set_num):
            card_set.append(cards.popleft())  # i番目のセットを作った.
            if len(cards) == 0:  # 一番下のセットがm枚未満の場合はそのまま.
                break

        for card_in_set in reversed(card_set):  # セットからは逆順に取り出す
            cards_shuffled.appendleft(card_in_set)  # 左側から追加

    return cards_shuffled


if __name__ == "__main__":
    n, m, k = map(int, input().split())  # カード枚数n, 1セットあたりの枚数m, シャッフル回数k

    answer(n, m, k)  # k回シャッフルした後のカードを上から巡に!
