import numpy as np
from numpy import c_
from tqdm import tqdm

np.seterr(over='raise')  # =>オーバーフローしたらエラーメッセージ出してくれる。


def _get_preference_all_element(R: np.ndarray) -> np.ndarray:
    '''
    評価行列Rの各要素r_uiを入力とし嗜好度p_uiを計算する関数。
    '''
    # 各要素に対して条件分岐処理
    P = np.where(R > 0, 1, 0)
    return P


def _get_confidence_all_element(R: np.ndarray, alpha) -> np.ndarray:
    '''
    評価行列Rの各要素r_uiと\alphaを入力とし、信頼度を計算する関数
    '''
    # 各要素に対して四則演算
    C = R * alpha + 1
    return C


def _get_error_each_element(p_ui, x_u, y_i: np.ndarray) -> float:
    '''
    嗜好度行列内の各要素の実測値と推定値の差を計算する関数

    parameters
    ------------
    p_ui: 評価行列Rの各要素r_uiから算出された嗜好度p_ui
    x_u:ユーザ行列Xのu列目(列ベクトル)
    y_i:アイテム行列yのi列目(列ベクトル)

    Return
    ---------
    X_uiとX_ui_hat(wとhの内積)の誤差.
    '''
    return (p_ui - np.dot(x_u, y_i))


def _get_error_all_element(P, C, X, Y: np.ndarray, beta) -> float:
    '''
    ALSによる行列分解における誤差関数の値を計算する関数

    parameters
    -----------
    P:評価行列の各要素r_uiから算出された嗜好度p_uiの行列(ユーザ×アイテム).
    C:評価行列の各要素r_uiから算出された信頼度c_uiの行列(ユーザ×アイテム).
    X:ユーザ行列(潜在変数×ユーザ)
    Y:アイテム行列(潜在変数×アイテム)
    alpha:信頼度の計算におけるハイパーパラメータ(元論文では40)
    beta:L2正則化における罰則項のハイパーパラメータlambda

    Return
    -------
    ALSによる行列分解における目的関数(誤差関数)の値.
    '''
    # 誤差関数の初期値
    error = 0.0
    # 2重(各アイテム、各ユーザ)のforループでXの各要素に対して処理を実行する.
    for u in range(len(P)):
        for i in range(len(P[u])):
            # 誤差をpow関数で2乗して、信頼度c_uiで重み付して、足し合わせ
            error += C[u][i] * \
                pow(_get_error_each_element(P[u][i], X[u, :], Y[i, :]), 2)

    # 全ての要素を足し終えたら、L2正則化項を追加
    error += beta/2.0 * (np.linalg.norm(x=X, ord=2) +
                         np.linalg.norm(x=Y, ord=2))

    return error


def matrix_factorization_implicit(R, len_of_latest_variable, steps=5000, lr=0.0002, alpha=40, beta=0.02, threshold=0.001):
    '''
    ALSによる行列分解を実行する関数

    parameters
    -----------
    X:実際に観測された評価行列.
    len_of_latest_variable:潜在変数の数.
    alpha:信頼度の計算におけるハイパーパラメータ(元論文では40)
    beta:L2正則化における罰則項のハイパーパラメータlambda
    lr:勾配降下法の学習率
    threshold:学習を終了するかどうかを判定する、誤差関数の値の閾値.

    Return
    -----------
    分解されたユーザ行列W(潜在変数×ユーザ)とアイテム行列H(潜在変数×アイテム)
    '''
    # ユニークなユーザ数mとアイテム数nを取得
    m = len(R)
    n = len(R[0])

    # WとHの初期値を設定
    X = np.random.rand(m, len_of_latest_variable)  # m * k行列
    Y = np.random.rand(n, len_of_latest_variable)  # n * k行列

    # 嗜好度行列Pを取得
    P = _get_preference_all_element(R=R)
    print(P)
    # 信頼度行列Cを取得
    C = _get_confidence_all_element(R=R, alpha=alpha)
    # 誤差関数の値の初期値
    error_value = 100

    # パラメータ更新
    for step in tqdm(range(steps)):
        # 更新式において、事前に計算できる値を計算
        Y_T_Y = np.dot(Y.T, Y)  # -.(k×k行列)
        X_T_X = np.dot(X.T, X)  # -.(k×k行列)

        # まずはユーザ行列を更新
        for u in range(m):
            # C_uを作成(n×nの対角行列)
            C_u = np.diag(C[u])
            # p_uを作成(一次元配列=>列ベクトル)
            p_u = P[u].reshape(-1, 1)
            # 更新式
            # x_u = np.linalg.inv(Y.T @ C_u @ Y + np.eye(len_of_latest_variable)
            #                     * beta) @ Y.T @ C_u @ p_u
            # 更新式(計算量節約ver.)
            x_u = np.linalg.inv(Y_T_Y + Y.T @ (C_u - np.eye(n)) @ Y +
                                np.eye(len_of_latest_variable) * beta) @ Y.T @ C_u @ p_u
            X[u:u+1, :] = x_u.T

            del C_u, p_u, x_u

        # 続いてアイテム行列を更新
        for i in range(n):
            # C_i を作成
            C_i = np.diag(C[:, i])
            # p_iを作成(一次元配列=>列ベクトル)
            p_i = P[:, i].reshape(-1, 1)

            # 更新式
            # y_i = np.linalg.inv(
            #     X.T @ C_i @ X + np.eye(len_of_latest_variable)*beta) @ X.T @ C_i @ p_i

            # 更新式(計算量節約ver.)
            y_i = np.linalg.inv(X_T_X + X.T @ (C_i - np.eye(m)) @ X +
                                np.eye(len_of_latest_variable) * beta) @ X.T @ C_i @ p_i
            Y[i:i+1, :] = y_i.T

            del C_i, p_i, y_i

        # 更新後の目的関数(誤差関数)の値を確認
        error_value = _get_error_all_element(P, C, X, Y, beta)
        # 十分に評価行列Xを近似できていれば、パラメータ更新終了！
        if error_value < threshold:
            break

    print(error_value)
    return X, Y


def main():
    # サンプルの評価行列を生成(行がユーザ、列がアイテム、各要素は購入回数を意味する)
    R = np.array([
        [5, 3, 0, 1],
        [4, 0, 0, 1],
        [1, 1, 0, 5],
        [1, 0, 0, 4],
        [0, 1, 5, 4],
    ]
    )

    # 行列分解
    X_hat, Y_hat = matrix_factorization_implicit(
        R, len_of_latest_variable=3, steps=10)
    # P\hatを生成.
    P_hat = np.dot(a=X_hat, b=Y_hat.T)
    print(P_hat)


if __name__ == '__main__':
    main()
