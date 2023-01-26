import * as math from "mathjs";

class MatrixFactorization {
  // アクセス修飾子 private: 自身のクラスのみアクセス可能
  private normLambda: number; // Regularization parameter
  private factorNum: number; // Embedding dimension
  private iterNum: number; // Number of training iterations
  private initSigma: number; // Standard deviation for initialization of embeddings
  private unobservedWeight: number; // Unobserved weight for calculate confidence
  private nu: number; // frequency scaled regularization

  constructor(
    normLambda: number = 1.0,
    factorNum: number = 10,
    iterNum: number = 10,
    initSigma: number = 0.1,
    unobservedWeight: number = 40,
    nu: number = 0.1
  ) {
    this.normLambda = normLambda;
    this.factorNum = factorNum;
    this.iterNum = iterNum;
    this.initSigma = initSigma;
    this.unobservedWeight = unobservedWeight;
    this.nu = nu;
  }
  als(ratingMatrix: math.Matrix): [math.Matrix, math.Matrix] {
    // ユニークなユーザ数とアイテム数を取得.
    const user_num: number = ratingMatrix.size()[0];
    const item_num: number = ratingMatrix.size()[1];

    let userMatrix: math.Matrix = makeRandomMatrixByNormalDist(
      user_num,
      this.factorNum,
      0,
      this.initSigma
    );
    let itemMatrix: math.Matrix = makeRandomMatrixByNormalDist(
      item_num,
      this.factorNum,
      0,
      this.initSigma
    );

    let prefMatrix = this._getPreferenceMatrix(ratingMatrix);
    let confMatrix = this._getConfidenceMatrix(ratingMatrix);

    let Y_T_Y: math.Matrix; // (k×k行列)
    let X_T_X: math.Matrix; // (k×k行列)

    let error: number = 100;
    for (let step_idx = 0; step_idx < this.iterNum; step_idx++) {
      // 更新式において、事前に計算できる値を計算
      Y_T_Y = math.multiply(math.transpose(itemMatrix), itemMatrix);
      X_T_X = math.multiply(math.transpose(userMatrix), userMatrix);

      // userMatrixを更新
      for (let u = 0; u < user_num; u++) {
        console.log("optimize user vector");
        this._updateUserVector(
          u,
          userMatrix,
          itemMatrix,
          confMatrix,
          prefMatrix,
          Y_T_Y
        );
      }

      // itemMatrixを更新
      for (let i = 0; i < user_num; i++) {
        console.log("optimize item vector");
      }
      // 更新後の誤差関数の値を確認
      error = this._getError(prefMatrix, confMatrix, userMatrix, itemMatrix);
      // 十分に評価行列Rを近似できていればパラメータ更新完了
      if (error < this.nu) {
        break;
      }
    }

    return [userMatrix, itemMatrix];
  }
  _getPreferenceMatrix(ratingMatrix: math.Matrix): math.Matrix {
    // 行列の各要素に対して条件分岐処理
    return ratingMatrix.map(function (value: number): number {
      return value > 0 ? 1 : 0;
    });
  }
  _getConfidenceMatrix(ratingMatrix: math.Matrix): math.Matrix {
    return ratingMatrix.map((value: number): number => {
      return value * this.unobservedWeight + 1;
    });
  } // NOTE: mapメソッド内で"this"は実行されたスコープで参照される為, functionではなくアロー関数で定義している.
  _getError(
    prefMatrix: math.Matrix,
    confMatrix: math.Matrix,
    userMatrix: math.Matrix,
    itemMatrix: math.Matrix
  ): number {
    // implicit ALSにおける目的関数の値を計算する.
    // 2重(各アイテム、各ユーザ)のforループでXの各要素に対して処理を実行する.
    const user_num: number = userMatrix.size()[0];
    const item_num: number = itemMatrix.size()[0];
    let error: number = 0.0;

    for (let u = 0; u < user_num; u++) {
      for (let i = 0; i < item_num; i++) {
        let c_ui: number = confMatrix.get([0, 0]);
        let p_ui: number = prefMatrix.get([0, 0]);
        console.log(userMatrix.size());
        let x_u = userMatrix.subset(
          math.index(u, math.range(0, this.factorNum))
        );
        let y_i = itemMatrix.subset(
          math.index(i, math.range(0, this.factorNum))
        );
        error += c_ui * this._getErrorEachElement(p_ui, x_u, y_i) ** 2;
      }
    }
    return error;
  }
  _getErrorEachElement(
    pref_ui: number,
    x_u: math.Matrix,
    y_i: math.Matrix
  ): number {
    x_u = math.flatten(x_u); // (1, factorNum) -> (factorNum)
    y_i = math.flatten(y_i);
    return pref_ui - math.dot(x_u, y_i);
  }

  _updateUserVector(
    u: number,
    userMatrix: math.Matrix,
    itemMatrix: math.Matrix,
    confMatrix: math.Matrix,
    prefMatrix: math.Matrix,
    Y_T_Y: math.Matrix
  ): void {
    let n = itemMatrix.size()[0];
    // C_uを作成(n×nの対角行列)
    let C_u = math.diag(confMatrix.subset(math.index(u, math.range(0, n))));
    console.log(C_u.size())
    // p_uを作成(一次元配列=>列ベクトル)
    let p_u = prefMatrix.subset(
      math.index(u, math.range(0, prefMatrix.size()[1]))
    );

    // 更新式(計算量節約ver.)
    // first term
    let Y_T = math.transpose(itemMatrix);
    let C_u_minus_I_Y = math.multiply(
      math.subtract(C_u, math.diag(math.ones(n))),
      itemMatrix
    ); //(n×nの対角行列)
    let lambda_I = math.multiply(
      this.normLambda,
      math.diag(math.ones(this.factorNum))
    ); //(f×fの対角行列)
    let firstTerm = math.add(
      math.add(Y_T_Y, math.multiply(Y_T, C_u_minus_I_Y)),
      lambda_I
    );
    // second term
    let secondTerm = math.multiply(Y_T, math.multiply(C_u, p_u));

    let x_u = math.multiply(math.inv(firstTerm), secondTerm);
    console.log(x_u);

    // 更新したベクトルをuserMatrixにinsertする.
    math.subset(userMatrix, math.index(u, math.range(0, this.factorNum)), x_u)
  }

  _updateItemVector(
    i: number,
    itemMatrix: math.Matrix,
    userMatrix: math.Matrix,
    confMatrix: math.Matrix,
    prefMatrix: math.Matrix,
    X_T_X: math.Matrix
  ): void {
    // C_iを作成(n×nの対角行列)
    // p_iを作成(一次元配列=>列ベクトル)
    // 更新式(計算量節約ver.)
    // 更新したベクトルをuserMatrixにinsertする.
  }
}

function makeRandomMatrixByNormalDist(
  row_num: number,
  col_num: number,
  mean: number = 0,
  std: number = 1.0
): math.Matrix {
  const rnorm = function (): number {
    return (
      Math.sqrt(-2 * Math.log(1 - Math.random())) *
      Math.cos(2 * Math.PI * Math.random())
    );
  }; // mu=0, std=1の正規分布に従う乱数を生成
  console.log(rnorm());
  let data: number[][] = Array.from({ length: row_num }, () =>
    Array.from({ length: col_num }, () => rnorm())
  );
  let randomMatrix: math.Matrix = math
    .matrix(data)
    .map((value: number): number => {
      return value * std;
    });

  return randomMatrix;
}

function main() {
  console.log("hello, world!");
  let ratingMatrix: math.Matrix;
  let inversedRatingMatrix: math.Matrix;

  makeRandomMatrixByNormalDist(3, 4);

  ratingMatrix = math.matrix([
    [5, 3, 0, 1],
    [4, 0, 3, 1],
    [1, 1, 0, 5],
    [1, 0, 3, 4],
  ]);

  const matrixFactorizationObj = new MatrixFactorization();
  matrixFactorizationObj.als(ratingMatrix);

  //   逆行列を計算
  // inversedRatingMatrix = math.inv(ratingMatrix);
  // console.log(inversedRatingMatrix);
}

main();
