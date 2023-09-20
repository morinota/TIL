# 全てを束ねて動かす人
import json
from pathlib import Path
from typing import Any
import streamlit as st
import numpy as np
from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt


def load_embeddings(uploaded_file: Any) -> list[np.ndarray]:
    data = json.load(uploaded_file)
    return [np.array(record["vector"]) for record in data]


def reduce_dimension_by_tSNE(embeddings: list[np.ndarray]) -> np.ndarray:
    embeddings_matrix = np.vstack(embeddings)
    tsne = TSNE(2, random_state=0)
    return tsne.fit_transform(embeddings_matrix)  # 行がレコード数、列が隠れ次元


def main():
    st.write("# 推薦システムの推論 品質モニタリング")
    st.write("推薦システムの推論の品質をモニタリングする為のapplicationです。主に教師ラベルに依存せずに推論直後に計算できる指標のみを採用します。")

    st.write("## 埋め込みベクトルの品質のモニタリング")

    uploaded_file = st.file_uploader("埋め込みベクトルのJSONファイルをuploadしてください")
    if uploaded_file is not None:
        embeddings = load_embeddings(uploaded_file)
        st.write("以下のJSONデータが読み込まれました:")
        st.write(embeddings)

        embeddings_2d = reduce_dimension_by_tSNE(embeddings)

        df = pd.DataFrame(embeddings_2d, columns=["Dimension 1", "Dimension 2"])
        st.write("t-SNE可視化:")
        st.write(df)
        st.write(plt.scatter(df["Dimension 1"], df["Dimension 2"]))
        st.pyplot()


if __name__ == "__main__":
    main()
