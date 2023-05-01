import abc
from typing import Any, Dict


class DiversityMetricAbstract(abc.ABC):
    def calc(self, P: Dict[Any, float], Q: Dict[Any, float]) -> float:
        pass


class KLDivergenceAbstract(DiversityMetricAbstract):
    pass


class JSDivergenceAbstract(DiversityMetricAbstract):
    pass
