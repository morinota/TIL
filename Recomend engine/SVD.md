# Singular Value Decomposition(特異値分解、SVD)とは？？

- 特異値分解とは、行列に対する行列分解の一手法であり、Autonneによって導入された。
- 特異値分解は、行列に対するスペクトル定理の一般化とも考えられ、正方行列に限らず任意の形の行列を分解できる。
- 次元削減(Dimensionality Reduction)分野でよく用いられる。
- **任意の行列を、3つの行列の積に分解する**手法？(MFは2つ。)

# SVDの理論

SVDでは、任意i×ji×jの実数行列AAを幾何的に解釈可能な3つの行列の積へと分解する。

$$
A_{m\times n} = U_{m\times r} \Sigma_{r\times r} V_{n \times r}^T
$$

ここで、

- $\Sigma$:正数$\sigma$からなる$r \times r$の対角行列。
  - 特異値であり寄与度が高い順にソートされている。
  - 固有値からルートを録るだけ?
- $U$:$m\times r$の直交行列。
  - また、$A$の左特異ベクトルといい、m次元空間におけるAの列の正規直交基底となっている。
- $V$:$n \times r$の直交行列。
  - また、AAの右特異ベクトルといい、nn次元空間におけるAAの行の正規直交基底となっている。
  - 求めた固有値から固有ベクトルを計算して単位ベクトル化するだけである。

更に上式を展開すると、次式のように表現できる。

$$
A =  U_{m\times r} \Sigma_{r\times r} V_{n \times r}^T \\
= \sum_{i}^{r}{\sigma_i u_i \circ v_i^T} \\
= \left\{u_1, u_2, \cdots, u_i \right\}
\begin{bmatrix}
\sigma_1 && \\
& \sigma_2 & \\
&& \ddots \\
&&& \sigma_i
\end{bmatrix}
\begin{bmatrix}
v_1^T \\
v_2^T \\
\vdots \\
v_i^T
\end{bmatrix}
$$

なおこの時、$\Sigma$は降順にソートされているので、$\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_n$となっている。

各行列のイメージとしては、
- Uは列の類似度。
- $V^T$は行の類似度。
- $\Sigma$は各類似度の強調度合い。

# SVD vs MF in Recommender Systems
