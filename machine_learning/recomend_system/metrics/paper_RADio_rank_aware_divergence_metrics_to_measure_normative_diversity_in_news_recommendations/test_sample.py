import math

from sample import (
    calc_JS_divergence,
    calc_KL_divergence,
    calc_rank_aware_pmf,
    calc_rank_weight_MMR,
    calc_rank_weight_nDCG,
)


def test_calc_KL_divergence() -> None:
    P = {"a": 0.2, "b": 0.3, "c": 0.5}
    Q = {"a": 0.3, "b": 0.3, "c": 0.4}
    kl_div_PQ_expected = -(0.2 * math.log2(0.3) + 0.3 * math.log2(0.3) + 0.5 * math.log2(0.4)) + (
        0.2 * math.log2(0.2) + 0.3 * math.log2(0.3) + 0.5 * math.log2(0.5)
    )

    kl_div_PQ_actual = calc_KL_divergence(P, Q)
    assert math.isclose(kl_div_PQ_actual, kl_div_PQ_expected)


def test_calc_JS_divergence() -> None:
    P = {"a": 0.2, "b": 0.3, "c": 0.5}
    Q = {"a": 0.3, "b": 0.3, "c": 0.4}

    js_div_first_term = (
        -(0.2 + 0.3) / 2 * math.log2((0.2 + 0.3) / 2)
        - (0.3 + 0.3) / 2 * math.log2((0.3 + 0.3) / 2)
        - (0.5 + 0.4) / 2 * math.log2((0.5 + 0.4) / 2)
    )
    js_div_second_term = 1 / 2 * (0.2 * math.log2(0.2) + 0.3 * math.log2(0.3) + 0.5 * math.log2(0.5))
    js_div_third_term = 1 / 2 * (0.3 * math.log2(0.3) + 0.3 * math.log2(0.3) + 0.4 * math.log2(0.4))
    js_div_PQ_expected = js_div_first_term + js_div_second_term + js_div_third_term

    js_div_PQ_actual = calc_JS_divergence(P, Q)
    print(js_div_PQ_actual)
    assert math.isclose(js_div_PQ_actual, js_div_PQ_expected)


def test_calc_rank_weight_nDCG() -> None:
    rank = 2
    rank_weight_expected = 1 / (math.log2(rank + 1))

    rank_weight_actual = calc_rank_weight_nDCG(rank)
    assert math.isclose(rank_weight_actual, rank_weight_expected)


def test_calc_rank_weight_MMR() -> None:
    rank = 2
    rank_weight_expected = 1 / (rank + 1)

    rank_weight_actual = calc_rank_weight_MMR(rank)
    assert math.isclose(rank_weight_actual, rank_weight_expected)


def test_calc_rank_aware_pmf() -> None:
    R = ["a", "b", "c"]
    Q_asterisk_expected = {
        "a": calc_rank_weight_MMR(1) / (calc_rank_weight_MMR(1) + calc_rank_weight_MMR(2) + calc_rank_weight_MMR(3)),
        "b": calc_rank_weight_MMR(2) / (calc_rank_weight_MMR(1) + calc_rank_weight_MMR(2) + calc_rank_weight_MMR(3)),
        "c": calc_rank_weight_MMR(3) / (calc_rank_weight_MMR(1) + calc_rank_weight_MMR(2) + calc_rank_weight_MMR(3)),
    }
    Q_asterisk_actual = calc_rank_aware_pmf(R)
    assert Q_asterisk_actual == Q_asterisk_expected


def test_calc_rank_aware_JS_divergence() -> None:
    P_asterisk = {"a": 0.2, "b": 0.3, "c": 0.5}
    Q_asterisk = {"a": 0.3, "b": 0.3, "c": 0.4}

    rank_aware_JS_div_expected = 
