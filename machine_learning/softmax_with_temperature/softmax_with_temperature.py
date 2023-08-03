## references


import numpy as np


class SoftmaxFunctionWithTemperature:
    def __init__(
        self,
        temperature: float,
        y_i_by_action: dict[str, float],
    ) -> None:
        """
        - temperatureが1.0より大きい場合-> 低いスコアのactionを強調
        - temperatureが1.0より小さい場合-> 高いスコアのactionを強調(決定論的なaction選択に近づく)
        (解釈: y =e^{x}にて、xが大きくなるとyが指数関数的に大きくなる. Tが小さい->xが大きくなる->高いactionの確率が強調される.)
        """
        self.temperature = temperature
        self.score_by_action = y_i_by_action

    def calc(self, y_i: float):
        return self._calc_softmax(y_i / self.temperature)

    def _calc_softmax(self, x: float) -> float:
        numerator = np.e ** (x)  # (分子)
        denominator = np.sum([np.e ** (score) for score in self.score_by_action.values()])
        return numerator / denominator
