import pandas as pd
from scipy.stats import chi2, chi2_contingency


def conduct_chi_squared_test():
    # ABテストの振り返り
    observed_values = [[14929, 1498], [14911, 1628]]
    observed_values = pd.DataFrame(
        observed_values, columns=["PV", "CV"], index=["old_model", "new_model"]
    )  # PV: Page View, CV: コンバージョン数, CVR = CV/PV

    # 観測されたCV, PV数から、「CVがあったPV」「CVがなかったPV」を二次元表で表す
    data = [
        [
            observed_values.loc["old_model", "CV"],
            observed_values.loc["old_model", "PV"]
            - observed_values.loc["old_model", "CV"],
        ],
        [
            observed_values.loc["new_model", "CV"],
            observed_values.loc["new_model", "PV"]
            - observed_values.loc["new_model", "CV"],
        ],
    ]
    cross_table = pd.DataFrame(
        data, columns=["CV", "not_CV"], index=["old_model", "new_model"]
    )
    print(cross_table)

    g, p, dof, expctd = chi2_contingency(cross_table.values)
    print(f"χ２乗値: {g:.3f}")
    print(f"p値:  {p:.3f}")


if __name__ == "__main__":
    conduct_chi_squared_test()
