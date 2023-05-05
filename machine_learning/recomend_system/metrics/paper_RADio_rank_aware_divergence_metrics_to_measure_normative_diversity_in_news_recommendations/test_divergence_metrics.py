import math

from diversity_metrics import JSDivergenceAbstract, KLDivergenceAbstract
from sample import (
    calc_f_JS_t,
    calc_rank_aware_JS_divergence,
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

    calculator = KLDivergenceAbstract()
    kl_div_PQ_actual = calculator.calc(P, Q)
    assert math.isclose(
        kl_div_PQ_actual,
        kl_div_PQ_expected,
        rel_tol=1e-3,
    )  # validな確率分布にする調整(_convert_to_valid_dist)によりやや値は異なる.


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

    calculator = JSDivergenceAbstract()
    js_div_PQ_actual = calculator.calc(P, Q)
    assert math.isclose(
        js_div_PQ_actual,
        js_div_PQ_expected,
        rel_tol=1e-3,
    )  # validな確率分布にする調整(_convert_to_valid_dist)によりやや値は異なる.


def test_calc_rank_weight_nDCG() -> None:
    rank = 2
    rank_weight_expected = 1 / (math.log2(rank + 1))

    rank_weight_actual = calc_rank_weight_nDCG(rank)
    assert math.isclose(
        rank_weight_actual,
        rank_weight_expected,
        rel_tol=1e-5,
    )


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


def test_calc_f_JS_t() -> None:
    t = 1
    f_JS_t_expected = 1 / 2 * ((t + 1) * math.log2(2 / (t + 1)) + t * math.log2(t))

    f_JS_t_actual = calc_f_JS_t(t)
    assert math.isclose(f_JS_t_actual, f_JS_t_expected)


def test_calc_rank_aware_JS_divergence() -> None:
    P_asterisk = {"a": 0.2, "b": 0.3, "c": 0.5}
    Q_asterisk = {"a": 0.3, "b": 0.3, "c": 0.4}

    rank_aware_JS_div_expected = (
        0.3 * calc_f_JS_t(0.2 / 0.3) + 0.3 * calc_f_JS_t(0.3 / 0.3) + 0.4 * calc_f_JS_t(0.5 / 0.4)
    )
    rank_aware_JS_div_actual = calc_rank_aware_JS_divergence(P_asterisk, Q_asterisk)

    assert math.isclose(rank_aware_JS_div_actual, rank_aware_JS_div_expected)
