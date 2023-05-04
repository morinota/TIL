import math
from collections import defaultdict
from typing import Any, Dict, List


def calc_KL_divergence(P: Dict[Any, float], Q: Dict[Any, float]) -> float:
    """ともに確率質量分布を想定.
    P: dictionary of probability distribution 1
    Q: dictionary of probability distribution 2
    """
    kl_div_P_Q = 0
    for x in P.keys():
        if P[x] > 0 and Q.get(x, 0) > 0:
            print(P[x], Q[x])
            kl_div_P_Q += -P[x] * math.log2(Q[x]) + P[x] * math.log2(P[x])
    return kl_div_P_Q


def calc_JS_divergence(P: Dict[Any, float], Q: Dict[Any, float]) -> float:
    js_first_term = 0
    js_second_term = 0
    js_third_term = 0
    for x in P.keys():
        P_x = P.get(x, 0)
        Q_x = Q.get(x, 0)
        if P_x <= 0 or Q_x <= 0:
            continue
        js_first_term += -(P_x + Q_x) / 2 * math.log2((P_x + Q_x) / 2)
        js_second_term += 1 / 2 * P_x * math.log2(P_x)
        js_third_term += 1 / 2 * Q_x * math.log2(Q_x)
    return js_first_term + js_second_term + js_third_term


def calc_rank_weight_nDCG(rank: int) -> float:
    return 1 / (math.log2(rank + 1))


def calc_rank_weight_MMR(rank: int) -> float:
    return 1 / (rank + 1)


def calc_rank_aware_pmf(R: List[Any]) -> Dict[Any, float]:
    rank_aware_pmf = defaultdict(float)
    rank_weights_sum = sum([calc_rank_weight_MMR(rank) for rank in range(1, len(R) + 1)])
    for rank_idx in range(len(R)):
        rank = rank_idx + 1
        rank_aware_pmf[R[rank_idx]] = calc_rank_weight_MMR(rank) / rank_weights_sum
    return rank_aware_pmf


def calc_f_JS_t(t: float) -> float:
    return 1 / 2 * ((t + 1) * math.log2(2 / (t + 1)) + t * math.log2(t))


def calc_rank_aware_JS_divergence(
    P_asterisk: Dict[Any, float],
    Q_asterisk: Dict[Any, float],
) -> float:
    x_candidates = set(P_asterisk.keys()).union(set(Q_asterisk.keys()))
    rank_aware_JS_div = 0
    for x in x_candidates:
        P_x = P_asterisk.get(x, 0)
        Q_x = Q_asterisk.get(x, 0)
        if P_x <= 0 or Q_x <= 0:
            continue
        rank_aware_JS_div += Q_x * calc_f_JS_t(P_x / Q_x)

    return rank_aware_JS_div
