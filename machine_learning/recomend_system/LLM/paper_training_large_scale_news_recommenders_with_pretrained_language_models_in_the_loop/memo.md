```python
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt


class TSNEVisualizer:
    def __init__(
        self,
        mapped_dim: int = 2,
        perplexity: int = 20,
    ) -> None:
        self.mapped_dim = mapped_dim
        self.perplexity = perplexity

    def run(self, vectors_by_name: dict[str, list[np.ndarray]]) -> None:
        """t-sneで高次元ベクトルを低次元にmappingする"""
        # 各vectorsを一つにまとめてmappingする

        whole_vectors = [
            vector for vectors in vectors_by_name.values() for vector in vectors
        ]
        whole_vectors_mapped = self._mapping(whole_vectors)

        # mapping結果をnameごとに再分割する
        mapped_vectors_by_name = {}
        start_idx = 0
        for name, vectors in vectors_by_name.items():
            mapped_vectors_by_name[name] = whole_vectors_mapped[
                start_idx : start_idx + len(vectors)
            ]
            start_idx += len(vectors)

        # mapping結果を描画する
        self._visualize(mapped_vectors_by_name)

    def _mapping(self, vectors: list[np.ndarray]) -> list[np.ndarray]:
        """t-sneで高次元ベクトルを低次元にmappingする"""
        tsne = TSNE(
            n_components=self.mapped_dim, random_state=0, perplexity=self.perplexity
        )
        vectors_array = np.array(vectors)  # shape=(sample_num, vector_dimention)
        vectors_array_mapped = tsne.fit_transform(vectors_array)

        # vectors_mapped:npdarray をlist[np.ndarray]に戻す
        vectors_mapped = [np.array(vector) for vector in vectors_array_mapped.tolist()]
        return vectors_mapped

    def _visualize(self, mapped_vectors_by_name: dict[str, list[np.ndarray]]) -> None:
        # 可視化する
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        for name, mapped_vectors in mapped_vectors_by_name.items():
            # mapped_vectorsからx座標とy座標を取り出す
            x = [mapped_vector[0] for mapped_vector in mapped_vectors]
            print(len(mapped_vectors))
            y = [mapped_vector[1] for mapped_vector in mapped_vectors]
            ax.scatter(x, y, label=name)
            # show
            ax.legend()
            fig.savefig(f"{name}.png")
        fig.savefig(f"both.png")


def test_TSNE_vectorizer():
    # Arrange
    # ノルムが等しいが、向きが異なる6個の3次元ベクトル
    vectors = [
        np.array([1, 2, 3]),
        np.array([2, 3, 1]),
        np.array([3, 1, 2]),
        np.array([-1, -2, -3]),
        np.array([-2, -3, -1]),
        np.array([-3, -1, -2]),
    ]
    vectors_B = [
        np.array([4, 5, 6]),
        np.array([5, 6, 4]),
        np.array([6, 4, 5]),
        np.array([-4, -5, -6]),
        np.array([-5, -6, -4]),
        np.array([-6, -4, -5]),
    ]

    sut = TSNEVisualizer(mapped_dim=2, perplexity=3)

    # Act
    sut.run({"vectors": vectors, "vectors_B": vectors_B})


if __name__ == "__main__":
    test_TSNE_vectorizer()

```
