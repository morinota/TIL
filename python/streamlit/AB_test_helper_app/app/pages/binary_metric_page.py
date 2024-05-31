import streamlit as st

from utils.desirable_sample_size_calculation import (
    DesirableSampleSizeSimulatorWithBinaryMetric,
)


def display():
    st.header("二値メトリクスの場合の理想的なサンプルサイズ計算")
    acceptable_false_positive_rate = st.number_input(
        "許容する誤陽性率(α)", min_value=0.0, max_value=1.0, value=0.05
    )
    acceptable_false_negative_rate = st.number_input(
        "許容する誤陰性率(β)", min_value=0.0, max_value=1.0, value=0.2
    )
    control_metric_mean_percent = st.number_input(
        "コントロールグループのメトリクスの平均値 (%)", min_value=0.0, value=10.0
    )
    treatment_metric_mean_percent = st.number_input(
        "トリートメントグループに期待するメトリクスの平均値 (%)",
        min_value=0.0,
        value=12.0,
    )
    if st.button("計算"):
        simulator = DesirableSampleSizeSimulatorWithBinaryMetric(
            significance_level=acceptable_false_positive_rate,
            desirable_power=1.0 - acceptable_false_negative_rate,
        )
        desirable_sample_size = simulator.calculate(
            control_metric_mean_percent / 100,
            treatment_metric_mean_percent / 100,
        )

        st.success(
            f"理想的なサンプルサイズ: 片側ユーザグループ当たり {desirable_sample_size} 人"
        )
