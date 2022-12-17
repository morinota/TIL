"""Queueとは

"""
from collections import deque
from typing import Any


class Queue(object):
    """単にListを使って、Queueの概念を表現してみた"""

    def __init__(self) -> None:
        self.queue = []

    def enqueue(self, data: Any) -> None:
        self.queue.append(data)

    def dequeue(self) -> Any:
        if self.queue:
            return self.queue.pop(0)  # popの際にindex番号を指定できる


if __name__ == "__main__":
    queue_obj = deque()
    queue_obj.append(1)
    queue_obj.append(2)
    queue_obj.append(3)
    queue_obj.append(4)
    print(queue_obj)
    print(queue_obj.popleft())
    print(queue_obj.popleft())
    print(queue_obj.popleft())
    print(queue_obj.popleft())

    # queue_obj = Queue()
    # queue_obj.enqueue(1)
    # queue_obj.enqueue(2)
    # queue_obj.enqueue(3)
    # queue_obj.enqueue(4)
    # print(queue_obj.queue)
    # print(queue_obj.dequeue())
    # print(queue_obj.dequeue())
    # print(queue_obj.dequeue())
    # print(queue_obj.dequeue())
    # print(queue_obj.queue)
