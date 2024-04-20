## refs:

- 反実仮想機械学習

# (準備)繰り返し期待値の法則(law of iterated expectation)を導出してみる。

- 繰り返し期待値の法則(law of iterated expectation)は、**同時分布に関する期待値が、条件付き期待値(conditional expectation)の周辺分布に関する期待値と等しい**、という法則。

$$
E_{p(x,y)}[f(x,y)] = E_{p(x)}[E_{p(y|x)}[f(x,y)]]
$$

左辺から右辺を導出してみる。

$$
E_{p(x,y)}[f(x,y)] = \int_{x} \int_{y} f(x,y) p(x,y) dx dy
\\
= \int_{x} (\int_{y} f(x,y) \frac{p(x,y)}{p(x)} dy) p(x) dx
\\
= \int_{x} (\int_{y} f(x,y) p(y|x) dy) p(x) dx
\\
= \int_{x} E_{p(y|x)}[f(x,y)] p(x) dx
\\
= E_{p(x)}[E_{p(y|x)}[f(x,y)]]
\\
導出完了!!
$$

# 全分散の法則(Law of Total Variance)を導出してみる。

- 全分散の法則(Law of Total Variance)は、**同時分布に関する分散 (=全分散?)が、条件付き分散(conditional variance)に関する期待値と、条件付き期待値(conditional expectation)に関する分散の和に等しい**、という法則。

$$
V_{p(x,y)}[f(x,y)] = V_{p(x)}[E_{p(y|x)}[f(x,y)]] + E_{p(x)}[V_{p(y|x)}[f(x,y)]]
$$

左辺から右辺を導出してみる。

$$
V_{p(x,y)}[f(x,y)] = E_{p(x,y)}[(f(x,y) - E_{p(x,y)}[f(x,y)])^2]
\\
\because 2乗の項の中身に、条件付き期待値の+-を追加。
\\
= E_{p(x,y)}[((f(x,y) - E_{p(y|x)}[f(x,y)]) + (E_{p(y|x)}[f(x,y)] - E_{p(x,y)}[f(x,y)]))^2]
\\
\because 2乗の項を展開。
\\
= E_{p(x,y)}[(f(x,y) - E_{p(y|x)}[f(x,y)])^2
\\
+ 2(f(x,y) - E_{p(y|x)}[f(x,y)])(E_{p(y|x)}[f(x,y)] - E_{p(x,y)}[f(x,y)])
\\
+ (E_{p(y|x)}[f(x,y)] - E_{p(x,y)}[f(x,y)])^2]
\\
\because 最も外側の期待値関数に対して、和の期待値を期待値の和に展開する。
\\
= E_{p(x,y)}[(f(x,y) - E_{p(y|x)}[f(x,y)])^2]
\\
+ 2E_{p(x,y)}[(f(x,y) - E_{p(y|x)}[f(x,y)])(E_{p(y|x)}[f(x,y)] - E_{p(x,y)}[f(x,y)])]
\\
+ E_{p(x,y)}[(E_{p(y|x)}[f(x,y)] - E_{p(x,y)}[f(x,y)])^2]
$$

ここで、第二項、つまり交差項(criss term)の部分について考える。(実はこの項が消えてほしい...!)

$$
2 E_{p(x,y)}[(f(x,y) - E_{p(y|x)}[f(x,y)])(E_{p(y|x)}[f(x,y)] - E_{p(x,y)}[f(x,y)])]
\\
\text{ここで、記号AとBで置き換える}
\\
= 2 E_{p(x,y)}[A B]
$$

繰り返し期待値の法則(law of iterated expectation)を使って、条件付き期待値の周辺分布に関する期待値に変換する。

$$
= 2 E_{p(x)}[E_{p(y|x)}[A B]]
$$

Bの項について。
Bはxの値に依存する関数である。xが決まれば一意に定まる定数項と言える。なぜなら、1項目の$E_{p(y|x)}[f(x,y)]$はxに依存する関数であり、2項目の$E_{p(x,y)}[f(x,y)]$はxにもyにも依存しない定数項であるから。

よって...

$$
= 2 E_{p(x)}[B \cdot E_{p(y|x)}[A]]
$$

ここで、Aの項について。$A = f(x,y) - E_{p(y|x)}[f(x,y)]$ である。Xが与えられた時のAの期待値は0になる。
数式で表すと確かに0になるな...!

$$
E_{p(y|x)}[A] = E_{p(y|x)}[f(x,y) - E_{p(y|x)}[f(x,y)]]
\\
= \int_{y} (f(x,y) - E_{p(y|x)}[f(x,y)]) p(y|x) dy
\\
= \int_{y} f(x,y) p(y|x) dy - E_{p(y|x)}[f(x,y)] \int_{y} p(y|x) dy
\\
= E_{p(x,y)}[f(x,y)] - E_{p(y|x)}[f(x,y)] \cdot 1
\\
= 0
$$

従って、cross termは消える!

$$
2 E_{p(x,y)}[A B] = 2 E_{p(x)}[B \cdot E_{p(y|x)}[A]]
\\
= 2 E_{p(x)}[B \cdot 0] = 2 E_{p(x)}[0] = 0
$$

よって、全分散の法則(Law of Total Variance)は以下のように導出される。

$$
V_{p(x,y)}[f(x,y)] = E_{p(x,y)}[(f(x,y) - E_{p(y|x)}[f(x,y)])^2]
\\
+ E_{p(x,y)}[(E_{p(y|x)}[f(x,y)] - E_{p(x,y)}[f(x,y)])^2]
\\
ここまだちゃんとわかってない。
\\
= V_{p(x)}[E_{p(y|x)}[f(x,y)]] + E_{p(x)}[V_{p(y|x)}[f(x,y)]]
$$
