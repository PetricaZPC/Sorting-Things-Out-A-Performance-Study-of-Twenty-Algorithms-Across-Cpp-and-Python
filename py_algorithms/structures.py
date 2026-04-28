from __future__ import annotations
from typing import Iterable, Optional, Any


class LinkedListNode:
    def __init__(self, value: Any, next_node: Optional["LinkedListNode"] = None) -> None:
        self.value = value
        self.next = next_node


class LinkedList:
    def __init__(self, values: Optional[Iterable[Any]] = None) -> None:
        self.head: Optional[LinkedListNode] = None
        self.length = 0
        if values is not None:
            self.head = None
            for value in reversed(list(values)):
                self.head = LinkedListNode(value, self.head)
                self.length += 1

    @classmethod
    def from_list(cls, values: Iterable[Any]) -> "LinkedList":
        return cls(values)

    def to_list(self) -> list[Any]:
        result: list[Any] = []
        node = self.head
        while node is not None:
            result.append(node.value)
            node = node.next
        return result

    def clone(self) -> "LinkedList":
        return LinkedList(self.to_list())

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Iterable[Any]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next
