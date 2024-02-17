from typing import Literal, Callable


def calcuraate_statistical_power(
    effect_size: float,
    n: int,
    acceptable_false_positive_rate: float = 0.05,
    alternative: Literal["two-sided", "larger", "smaller"] = "larger",
) -> float:
    """
    This function calculates the statistical power of the A/B test
    """
    pass
