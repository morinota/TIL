# 二分探索法とは

- 狭義の定義では「ソート済み配列の中から目的のものを高速に探索する」方法。
  - =>解釈を拡張して「**探索範囲を半減させていく事によって解を求める手法**」と捉える事で、より多くの問題に適用できる。
- まず二分探索を行う為には、配列がソート済みである事が必要。そうでない場合には、まず配列にソート処理を適用する必要がある。
  - (「配列の各要素を小さい順に並べる」処理は $O(N \log N)$ でできる事を覚えておくと良い。)

## 狭義の二分探索法から、少し拡張する

- 例: algorithms\algorithms_and_data_structures\binary_search_method\配列から目的の値を探索する二分探索法.py
- 少し拡張する:
  - 「ソート済み配列において、目的の値が配列にあるかどうか。どこにあるか。」 -> 「ソート済み配列において、key >= a[i]という条件を満たす最小のindex $i$ を探す。」
  - aの中にkeyがなくても、key以上の値の範囲での最小値がわかる。
  - aの中にkeyが複数あった時、そのうちの最小のindexがわかる。

## 広義の二分探索法へ(単調性の仮定ありver.)

- 更に拡張する。以下は一般化した二分探索法:
  - 各整数 x についてtrue/falseの2値で判定できる条件 Pが与えられた状態で、ある整数 l, r ($l < r$, leftとright) が存在し、以下が成立しているとする。
    - $P(l) = false$, $P(r) = true$
  - ある整数 $M$ ( $l < M <= r$, middle) が存在し、以下が成立している。
    - $P(x) = false, \forall x < M$
    - $P(x) = true, \forall x >= M$
  - **$M$ を計算量 $O \log(D), D = r-1$ で求める事ができるアルゴリズムを 二分探索法と呼ぶ**。
- 重要な性質:
  - アルゴリズムの初期状態から終了状態まで、変数left は常にfalse側、変数right は常にtrue側にいる。
  - アルゴリズムが終了した時、変数rightは $P(right) = true$ を満たす最小の整数値、変数leftは $P(left) = alse$ を満たす最大の整数値、になる。
  - (この定義では、**false領域とtrue領域がソート済み配列内で二分されている仮定**に基づく。以下、この仮定を**単調性**と呼ぶことにする。)

## 更に広義の二分探索法へ(単調性の仮定外したver.)

- 単調性の仮定を外すと...
  - 領域全体(=配列)がfalse領域とtrue領域の２種類あり、$x = l, r$については異なる領域に属するものとする。
  - この時、二分探索法は、**false領域からtrue領域へと変化する境目のうちのいずれか1つを求めるアルゴリズム**とみなせる。

### この一般化が有効な場面の例: 「実数上の二分探索法」

- ある実数区間において連続な(=入出力が連続値の)関数 $f(x)$ が与えられ、区間内の2点 $l, r$ に対して $f(l), f(r)$ のうち一方が正でもう一方が筆あるとする。
- この時、二分探索法は、$f(x) = 0$ を満たす実数 $x (l <x <r)$ のうちの1つを求める事ができる。