from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    data: Any
    next: Optional["Node"] = None
    previous: Optional["Node"] = None


class DoublyLinkedList:
    def __init__(self, head_node: Optional[Node] = None) -> None:
        self.head_node = head_node
