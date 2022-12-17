"""
queueを使ったクイズ
- reverse()を使わずにqueueの順番を並び替えよ
- 非常に簡単なクイズ
"""
from collections import deque


def reverse(queue: deque) -> deque:
    new_queue = deque()  # もう一つデックを作ってやる
    while queue:  # queueがある間(よくある)
        new_queue.append(queue.pop())  # サッと一行で書く
    # return new_queue

    # 引数のqueueをそのまま書き換えるパターン(これで書き換わるのか...!)
    [queue.append(d) for d in new_queue]  # 空になったqueueに再度dataを入れているだけ


if __name__ == "__main__":
    queue_obj = deque()
    queue_obj.append(1)
    queue_obj.append(2)
    queue_obj.append(3)
    queue_obj.append(4)
    print(queue_obj)
    # queue_obj.reverse()  # queueの順番を並び替える
    # print(queue_obj)
    print(reverse(queue_obj))
