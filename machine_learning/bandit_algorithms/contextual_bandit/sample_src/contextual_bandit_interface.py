import abc
from dataclasses import dataclass
from typing import Any


@dataclass
class Arm:
    _reward: int

    def is_new(self) -> bool:
        pass


@dataclass
class Context:
    feature1: Any


class ContextualBanditInterface(abc.ABC):
    @abc.abstractmethod
    def select_arm(self) -> Arm:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, selected_arm: Arm, reward: float) -> None:
        raise NotImplementedError
