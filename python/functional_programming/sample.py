# 参考: https://pycon.jp/2020/timetable/?id=203810

import dataclasses
from statistics import mean
from typing import List


class Major:
    MATH = "math"


@dataclasses.dataclass
class Student:
    age: int
    major: str
    height: float


def non_pythonic_examlpe(students: List[Student]) -> None:
    average_heighet = mean(map(lambda x: x.height, students))
