from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# np.random.seed(123) 乱数生成の結果を固定したい場合は、コメントアウトを外します。
from matplotlib import style

style.use("classic")
import os

import pandas as pd
import statsmodels.api as sm


@dataclass
class SampleDataForIntermediateVariableMask:
    CAUSAL_EFFECT_SALT_TO_BLOOD = 5
    CAUSAL_EFFECT_BLOOD_TO_RISK = 0.5
    CAUSAL_EFFECT_SALT_TO_RISK = CAUSAL_EFFECT_SALT_TO_BLOOD * CAUSAL_EFFECT_BLOOD_TO_RISK

    SALT_INTAKE_MEAN = 10
    SALT_INTAKE_SIGMA = 5
    SALT_INTAKE_MEAN_STANDARDIZED = 0.0
    SALT_INTAKE_SIGMA_STANDARDIZED = 1.0

    BLOOD_PRESSURE_MEAN = 110

    salt_intake_array: np.ndarray
    blood_pressure_array: np.ndarray
    mortarity_risk_array: np.ndarray
    dataframe: pd.DataFrame

    @classmethod
    def generate(cls, sample_num: int = 5000) -> "SampleDataForIntermediateVariableMask":
        """generate sample dataset for experiment"""
        salt_intake_array = cls._generate_salt_intake_array(sample_num)
        blood_pressure_array = cls._generate_blood_pressure_array(sample_num, salt_intake_array)
        mortarity_risk_array = cls._generate_mortarity_risk_array(sample_num, blood_pressure_array)

        df = cls._summarize_to_dataframe(salt_intake_array, blood_pressure_array, mortarity_risk_array)

        return SampleDataForIntermediateVariableMask(
            salt_intake_array,
            blood_pressure_array,
            mortarity_risk_array,
            df,
        )

    @classmethod
    def _generate_salt_intake_array(cls, sample_num: int) -> np.ndarray:
        """正規分布を使って塩分摂取量の仮想データを生成する。
        単位は[g/day]だが、今回は平均0、分散1となるように標準化されているとする。
        """
        return np.random.normal(
            loc=cls.SALT_INTAKE_MEAN_STANDARDIZED,
            scale=cls.SALT_INTAKE_SIGMA_STANDARDIZED,
            size=sample_num,
        )

    @classmethod
    def _generate_blood_pressure_array(cls, sample_num: int, salt_intake_array: np.ndarray) -> np.ndarray:
        """「血圧＝5×塩分 ＋誤差＋平均値」の関係式により血圧データを作成"""
        error_blood_pressure = np.random.normal(loc=0, scale=1.0, size=sample_num)
        return cls.CAUSAL_EFFECT_SALT_TO_BLOOD * salt_intake_array + error_blood_pressure + cls.BLOOD_PRESSURE_MEAN

    @classmethod
    def _generate_mortarity_risk_array(cls, sample_num: int, blood_pressure_array: np.ndarray) -> np.ndarray:
        error_mortarity_risk = np.random.normal(loc=0, scale=1.0, size=sample_num)
        return cls.CAUSAL_EFFECT_BLOOD_TO_RISK * blood_pressure_array + error_mortarity_risk

    @classmethod
    def _summarize_to_dataframe(
        cls, salt_intake_array: np.ndarray, blood_pressure_array: np.ndarray, mortarity_risk_array: np.ndarray
    ) -> pd.DataFrame:
        return pd.DataFrame(
            data={
                "salt_intake": salt_intake_array,
                "blood_pressure": blood_pressure_array,
                "mortarity_risk": mortarity_risk_array,
            }
        )

    def draw_pair_plot(self, filepath: Path) -> None:
        pair_plot = sns.pairplot(self.dataframe)
        plt.savefig(filepath)


class ExperimentResults:
    def __init__(self) -> None:
        pass

    def conduct_linear_regression(self, df: pd.DataFrame, x_names: List[str], y_name: str) -> Dict:
        X_array = df[x_names].values
        X_array = sm.add_constant(data=X_array)  # constant termを追加
        y_array = df[y_name].values
        model = sm.OLS(y_array, X_array)
        res = model.fit()
        sigma_square_hat = self._estimate_sigma_square(y_array, X_array, a=res.params)
        a_1_hat, a_2_hat = res.params[1], res.params[2]

        return {
            "explanatory_variables": x_names,
            "a_1_hat": a_1_hat,
            "a_2_hat": a_2_hat,
            "abs(actual - estimated)": abs(2.5 - a_1_hat),
            "AIC": res.aic,
        }

    def _estimate_sigma_square(self, y: np.ndarray, X: np.ndarray, a: List[float]) -> float:
        """線形回帰のOLSにおけるsigma_squareの推定値を算出するメソッド"""
        num_explanatory_var = len(a)
        # calc y_hat
        y_hat = np.zeros(shape=y.shape[0])
        for i in range(num_explanatory_var):
            a_i = a[i]

            X_i = X[:, i]
            a_i_times_X_i = X_i * a_i
            y_hat += a_i_times_X_i

        # calc residue(残差e) = y - y_hat
        # df[y_name].valuesで、y_name:strならyでOK。y_name:List[str]ならy[:,0]じゃないとエラー
        residue_array: np.ndarray = y - y_hat
        # print(f"[LOG]residue_array shape is {residue_array.shape}")

        # innor products(内積) of residue_array(= residue_arrayのノルム(長さ)の2乗)
        square_residue_array = np.dot(residue_array, residue_array)
        # calc \hat{\sigma^2}
        n_samples = y.shape[0]
        sigma_square_hat_OLS = square_residue_array / (n_samples - num_explanatory_var)
        return sigma_square_hat_OLS


def draw_results(results_list: List[List], label_list: List[str]) -> None:
    fig, axis = plt.subplots()

    for result, label in zip(results_list, label_list):
        axis.plot(result, label=label)
    axis.set_xlabel("index of each steps")
    axis.set_ylabel("value of regression coefficient")
    axis.legend(
        loc="lower left",
    )
    fig.suptitle("Experiment about Intermediate Variable and Multicollinearity")
    fig.savefig("experiment_bias_by_mediator.png")


def main() -> None:
    # sample_data = SampleDataForIntermediateVariableMask.generate(sample_num=5000)

    # sample_data.draw_pair_plot(Path("pairplots_experiment_intermediate_variable_mask.png"))

    # experiment_obj = ExperimentResults()
    # results_exp_1 = experiment_obj.conduct_linear_regression(
    #     sample_data.dataframe,
    #     x_names=["salt_intake"],
    #     y_name="mortarity_risk",
    # )
    # results_exp_2 = experiment_obj.conduct_linear_regression(
    #     sample_data.dataframe,
    #     x_names=["salt_intake", "blood_pressure"],
    #     y_name="mortarity_risk",
    # )

    experiment_obj = ExperimentResults()
    experiment_num = 50
    a_1_hat_list, a_2_hat_list = [], []

    for _ in range(experiment_num):
        sample_data = SampleDataForIntermediateVariableMask.generate(sample_num=5000)
        result_exp_i = experiment_obj.conduct_linear_regression(
            df=sample_data.dataframe,
            x_names=["salt_intake", "blood_pressure"],
            y_name="mortarity_risk",
        )
        a_1_hat_list.append(result_exp_i["a_1_hat"])
        a_2_hat_list.append(result_exp_i["a_2_hat"])

    print(f"[LOG]mean(a_1_hat_list):{mean(a_1_hat_list)}")
    print(f"[LOG]mean(a_2_hat_list):{mean(a_2_hat_list)}")
    print(f"[LOG]np.var(a_1_hat_list):{np.var(a_1_hat_list)}")
    print(f"[LOG]np.var(a_2_hat_list):{np.var(a_2_hat_list)}")

    draw_results(results_list=[a_1_hat_list, a_2_hat_list], label_list=["a_1(salt intake)", "a_2'(blood pressure)"])


if __name__ == "__main__":
    main()
