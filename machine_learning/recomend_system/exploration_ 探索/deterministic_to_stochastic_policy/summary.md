## はじめに

### なんでこのトピックを??

- 先日のRecommendation Industry Talksというイベントで「推薦システムを本番導入する上で一番優先すべきだったこと」というタイトルで発表してきましたー!
  - 結論: **推薦システムのオフライン評価が難しいから一旦諦めて、まずはいかにA/Bテスト(オンライン評価)しやすい基盤を設計することが大事だった**...!

<https://speakerdeck.com/morinota/tui-jian-sisutemuwoben-fan-dao-ru-surushang-de-fan-you-xian-subekidatutakoto-newspicksji-shi-tui-jian-ji-neng-nogai-shan-shi-li-woyuan-ni>

- 一方で、やっぱりオフライン評価できた方が嬉しい...!
  - A/Bテストなどのオンライン評価と比べて、高速にフィードバックを得られる。ユーザ体験を毀損するリスクがない、という利点。
  - というか、オフライン評価が難しいってことは、ハイパーパラメータチューニングやオフライン学習も難しいのでは...!:scared:
- オフライン評価のアプローチを調べていると...
  - 決定的な推薦方策によって収集した観測データだと、かなり打ち手がなさそうな印象。
  - **確率的な推薦方策によってある程度探索的に収集したデータを使えば、だいぶ打ち手が増えそう**...!:thinking:
- というわけで、確率的な推薦方策を本番導入することを色々考えてみた!

## ざっくりこういう話をした

ということで、決定的な推薦方策と確率的な推薦方策

- 決定的(deterministic)な方策
  - 常に同じ行動を選択する方策。
  - ex.) ユーザ1に対して、アイテムAを100%の確率で推薦する。
- 確率的(stochastic)な方策
  - ある確率でランダムに行動を選択する方策。
  - ex.) ユーザ1に対して、アイテムAを50%、アイテムBを30%、アイテムCを20%の確率で推薦する。

今回は、推薦モデルの評価・学習に使用しやすいログデータを収集したいというモチベーションで、前者から後者への移行について考えてみます!

## 推薦システムのオフライン評価の話を少し

### 意思決定の最適化問題とオフライン評価

- 推薦システムは意思決定の最適化問題!
  - 例えば、ニュース推薦の場合
    - 何らかのモデルによって、(ユーザ, 記事)のペアの相性やクリック確率などのスコアを予測
    - スコアの予測値に基づいて、ユーザにどんな記事を推薦するかの意思決定を行う

> 予測というよりもむしろデータに基づいた意思決定の最適化問題
> (*書籍「反実仮想機械学習」より引用*)

データに基づいて導かれる意思決定の規則 = 意思決定方策(decision-making policy)。
オフライン評価のモチベーションは、この意思決定方策の性能をログデータに基づいて正確に評価できるようになること。でも**意思決定方策のオフライン評価がなかなか難しい**...:thinking:
(今回は特に推薦タスクの話がしたいので、以降では意思決定方策ではなく「推薦方策」という用語を使います)

以下の図は、Booking.comさんのMLアプリケーション開発運用の教訓に関する論文で、以下の「相関がなかった」という有名な相関図。

![](https://i.imgur.com/TZEaYJu.png)

*引用元: 150 Successful Machine Learning Models: 6 Lessons Learned at Booking com, Bernardi et al., 2019*

オフライン評価は難しいが、やっぱりできたら嬉しい。

- オフライン評価が正確にできる場合
  - A/Bテストなどのオンライン評価の前に有効そうな方策を絞り込む事ができ、仮説検証をより高速に回す事ができる。
  - ハイパーパラメータチューニングやオフライン学習もしやすくなる。
  - ユーザ体験を悪化させ得る施策を、オンライン環境に出す前に検知する事ができる。
- 逆に、オフライン評価の確度が低い場合
  - 全ての仮説に対してA/Bテストする必要があり、仮説検証の速度が下がる。(A/Bテストの運用コストを下げても、どうしてもオフライン実験するよりは時間がかかる。10倍くらい?)
  - 誤った基準でハイパーパラメータチューニングしてしまう可能性。
  - ユーザ体験を悪化させ得る施策を、オンライン環境に出す可能性。

### オフライン評価がなかなか難しい問題

基本的な記号を定義

- 特徴量(feature, context)のベクトル: $x$ (ex. ユーザ特徴量など)
- 離散的な行動(action): $a \in A$ (ex. 推薦アイテムなど)
- 行動の結果として観測される報酬: $r$

また、推薦方策 $\pi$ を行動空間 $A$ 上の条件付き確率分布とする。
(i.e. ある特徴量 $x$ の場合に、行動 $a$ を推薦する確率)

$$
\pi(a|x) := p_{\pi}(a|x)
$$

また、推薦方策 $\pi$ の性能(policy value)を、(x,a,r)の同時分布に対する報酬 $r$ の期待値で定義する:

```math
V(\pi) := \mathbb{E}_{p(x, a, r)}[r] =\mathbb{E}_{p(x)\pi(a|x)p(r|a,x)}[r]
```

（例えば、推薦方策の性能をCTRとしたい場合は、報酬 $r$ をクリックした(1)か否(0)かのbinary変数として定義し、その期待値 $V(\pi)$ がCTRになる）

もしA/Bテストなどのオンライン評価で推薦方策 $\pi$ を本番稼働させ収集したログデータ $D_{\pi}:=\{(x_i, a_i, r_i)\}_{i=1}^{n}$ で推薦方策の性能 $V(\pi)$ を推定する場合、以下のような**AVG推定量**が使われる:

```math
\hat{V}_{AVG}(\pi;D_{\pi}) = \frac{1}{n} \sum_{i=1}^{n} r_i
```

（A/Bテストの事後分析で算出してるCTRなどは、 $V(\pi)$ そのものではなく、実際にこの方法で推定した値のはず...!:thinking:）

オンライン評価（データ収集方策 $\pi_0$ と評価方策 $\pi_1$ が同じ）の場合は、AVG推定量（シンプルにログデータの報酬を平均するだけ）で推薦方策の性能 $V(\pi)$ をバイアスなく推定できる。
（具体的には、ログデータ $D$ に対するAVG推定量 $\hat{V}_{AVG}(\pi;D_{\pi})$ の期待値が、$V(\pi)$ に一致する）

```math
\mathbf{E}_{D_{\pi}}[\hat{V}_{AVG}(\pi;D_{\pi})] = \mathbb{E}_{D}[\frac{1}{n} \sum_{i=1}^{n} r_i]
\\
= \frac{1}{n} \sum_{i=1}^{n} \mathbb{E}_{p(x)\pi(a|x)p(r|a,x)}[r] = V(\pi)
\\
\because (x,a,r) \sim^{i.i.d.} p(x)\pi(a|x)p(r|a,x), \text{期待値の線形性より}
\\
= \mathbb{E}_{p(x)\pi(a|x)p(r|a,x)}[r] 
\\
= V(\pi)
```

しかし一方で、オフライン評価（データ収集方策 $\pi_0$ と評価方策 $\pi_1$ が異なる）の場合は、このAVG推定量は推薦方策の性能 $V(\pi)$ に対してバイアスを持ってしまう。

```math
\mathbb{E}_{D_{\pi_0}}[\hat{V}_{AVG}(\pi_1;D_{\pi_0})] = \mathbb{E}_{D_{\pi_0}}[\frac{1}{n} \sum_{i=1}^{n} r_i]
\\
= \frac{1}{n} \sum_{i=1}^{n} \mathbb{E}_{p(x)\pi_0(a|x)p(r|a,x)}[r]
\\
\because (x,a,r) \sim^{i.i.d.} p(x)\pi(a|x)p(r|a,x), \text{期待値の線形性より}
\\
= \mathbb{E}_{p(x)}[\sum_{a \in A} \pi_0(a|x) \mathbb{E}_{p(r|a,x)}[r]]
\neq V(\pi_1)
```

### 　最も基本的な戦略　IPS推定量

AVG推定量では、データ収集方策と評価方策が異なるほど大きなバイアスを持つ。
AVG推定量のバイアスを打ち消す最も基本的な戦略が、以下のIPS(Inverse Propensity Score)推定量。

```math
\hat{V}_{IPS}(\pi_1;D_{\pi_0}) := \frac{1}{n} \sum_{i=1}^{n} \frac{\pi_1(a_i|x_i)}{\pi_0(a_i|x_i)} r_i = \frac{1}{n} \sum_{i=1}^{n} w(x_i, a_i) r_i
```

なお、$w(x_i, a_i) := \frac{\pi_1(a_i|x_i)}{\pi_0(a_i|x_i)}$ を重要度重み(importance weight)と呼び、評価方策 $\pi_1$ とデータ収集方策 $\pi_0$ による行動選択確率の比を表す。

**「反実仮想機械学習」を読んでいてもOPE推定量の多くがIPS推定量の拡張ver.っぽく、最も基本的なオフライン評価の戦略の1つと言ってもよさそう**です...!:thinking:

### IPS推定量を使う上で満たすべき仮定: 共通サポート仮定

そしてIPS推定量は、以下の**共通サポート仮定**を満たす場合に真の性能に対して不偏になります:

$$
\pi_1(a|x) > 0 -> \pi_0(a|x) > 0, \forall a \in A, \forall x \in X
$$

つまり、「**評価方策 $\pi_1$ が特徴 $x$ に対してサポートする(=選択する可能性がある)全ての行動 $a$ を、データ収集方策 $\pi_0$ もサポートしていてくれ!**」という仮定です。

### データ収集方策が決定的方策だと、オフライン評価難しそう

$$
\pi_1(a|x) > 0 \rightarrow \pi_0(a|x) > 0, \forall a \in A, \forall x \in X
$$

IPS推定量（あるいはその拡張ver.たち）を活用するためには、上記の共通サポート仮定をなるべく満たしたい訳です。

ここで、決定的方策と確率的方策の話が出てきます!
データ収集方策 $\pi_0$ と評価方策 $\pi_1$ がそれぞれ、決定的方策/確率的方策であるケース（2^2 = 4通り）を考えてみましょう。

![](https://pbs.twimg.com/media/GVufdqfXkAEkE6W?format=png&name=4096x4096)

- 1. pi_0 = 決定的方策、pi_1 = 決定的方策のケース
  - -> 共通サポート過程を満たせなさそう。唯一満たせるのは、$\pi_0 = \pi_1$ の場合のみなので。
- 2. pi_0 = 決定的方策、pi_1 = 確率的方策のケース
  - -> 共通サポート過程を満たせなさそう。
- 3. pi_0 = 確率的方策、pi_1 = 決定的方策のケース
  - -> 共通サポート過程を満たせそう!
- 4. pi_0 = 確率的方策、pi_1 = 確率的方策のケース
  - -> 共通サポート過程を満たせそう!

これを踏まえると、データ収集方策 $\pi_0$ が決定的方策だと、共通サポート仮定を全然満たせなさそう...!:scream:
一方で、**データ収集方策 $\pi_0$ が確率的方策でさえあれば**、評価方策 $\pi_1$ が決定的方策でも共通サポート仮定を結構満たせそう...!:thinking:

抽象的な表現ですが**方策の探索の度合いが「データ収集方策 ≧ 評価方策」であれば**、共通サポート仮定を満たしやすく、IPS推定量（あるいはその拡張ver.たち）を使ってオフライン評価に打つ手が出てくるのでは...!:thinking:

（ちなみに補足すると、共通サポート仮定を満たしてIPS推定量が真の性能に対して不偏になっただけで、オフライン評価難しい問題が全て解決するとは限りません! **バイアスを除去できたとしてもバリアンスの懸念があるから**です。特に推薦タスクにおいて推薦アイテム候補の数が多かったり、推薦アイテムリストの長さが長かったりすると、方策が取りうる行動の選択肢が爆発的に増え、IPS推定量のバリアンスが大きくなる問題があります。）

## 決定的な推薦方策から確率的な推薦方策への移行アイデア達

決定的な推薦方策から確率的な推薦方策への移行アイデアをいくつか検討してみます。

推薦タスクの問題設定としては、推薦候補のアイテム集合 $A$ から、ユーザ特徴量 $x$ に基づいて、長さ $k$ の推薦アイテムリスト $\mathbf{a} = [a_1, a_2, \ldots, a_k]$ を生成するというものを考えます。

すでに、任意のユーザ特徴量 $x$ とアイテム $a \in A$ の組み合わせに対してスコアを割り当てる関数 $f_{\theta}(x, a)$ が何らか存在しているとします。（$f_{\theta}$ は例えば線形モデルやNN、あるいはシンプルな内積などで実装されているでしょう）

そして現在、このスコア関数 $f_{\theta}(x,a)$ に基づいてスコアが最も高い(or低い)アイテムk個を選択するような決定的な推薦方策が稼働しているとします。

この**決定的な方策を確率的な方策に移行するアイデア**たちを考えてみます。

- 1. プラケットルースモデルに基づくランキングの確率的サンプリング
- 2. ガンベルソフトマックストリックを使う
- 3. epsilon-greedyを使う

### プラケットルースモデルに基づくランキングの確率的サンプリング

- アイテム集合 $A$ から 長さ $k$ の推薦アイテムリスト　$\mathbf{a} = [a_1, a_2, \ldots, a_k]$ を確率的にサンプリングする際は、リスト内で同一アイテムの重複を生まないような工夫が必要。
- よく用いられる方法として「反実仮想機械学習」で紹介されてたのが、**プラケットルースモデル(Pleckett-Luce model、PLモデル)**という方法。

PLモデルの流れは、以下のお気持ち実装を参照:

```python
def sampling_with_plackett_luce_model(f_theta: ScoreFunction, x: FeatureVector, A: set[Item], k: int)->list[Item]:
    """
    PLモデルに基づく推薦アイテムリストの確率的サンプリング
    """
    ranking = []
    # スコア関数 f_theta(x,a) を使って、個別のアイテムaについてスコアを割り当てる
    score_by_item = {a: f_theta(x, a) for a in A}
    for _ in range(k):
        # スコア f_theta(x,a) をソフトマックス関数に渡して、確率分布 p(a|x) に変換
        pmf = calculate_pmf_by_softmax(score_by_item, temperature_param=1.0)
        
        # 確率分布に基づいてi番目のポジションの推薦アイテムをサンプリング
        a_i = np.random.choice(A, p=pmf)
        ranking.append(a_i)

        # 同一アイテムが重複して選ばれないように、選択されたアイテムを推薦候補から除外して、次のポジションのサンプリングへ
        A.remove(a_i)
    return ranking
```

書籍によると、上記のアルゴリズムは現場の推薦・検索システムに適用するには計算量の問題で難しい(**ソフトマックス関数を何度も計算する必要がある**ため...!:scream:)とのこと。

#### 計算量ってどれくらいなんだろ？

- 変数:
  - $|A| = n$ (アイテム集合のサイズ)
  - $k$ (推薦リストの長さ)
- 各処理の計算量
  - スコアの計算: Aの各アイテムに対してスコアを計算してる。なので計算量はO(n)になる。
  - メインのループ処理: サンプリングする推薦リストの長さ $k$ 回ループする。ループの計算量はO(k)になる。
    - 確率分布の計算: Aの各アイテムに対してソフトマックス関数で確率質量を計算してる。計算量はO(n)になる。
    - サンプリング: `np.random.choice(A, p=pmf)`は `A`の要素数に依らずにかかる時間は一定。計算量はO(1)になる。
    - サンプリングしたアイテムを推薦リストに追加: `ranking`はリスト型。リストの末尾に要素を追加する`append`は既存の要素数に関係なくO(1)でできる。計算量はO(1)になる。
    - サンプリングしたアイテムを推薦候補から除外: `A`はset型。`set`はハッシュテーブルで実装されているので、要素の追加・削除がO(1)でできる。計算量はO(1)になる。

よって、全体の計算量はO(n + k *(n + 1 + 1 + 1)) -> O(n + k* n) -> O(k * n)になる??
(スコア関数による推論がめっちゃ軽い前提??:thinking:)

### ガンベルソフトマックストリックを使う

- 前述のように、originalのPLモデルのアルゴリズムは計算量が大きく、実用的ではないっぽい。
- **ガンベルソフトマックストリック(Gumbel-Softmax trick)**と呼ばれるテクニックを使うことで、PLモデルに基づいた確率的なランキング方策を効率化して高速化できることが知られてるみたい。

ガンベルソフトマックストリックが行うこと:

- 1. 各アイテムのスコア $f_{\theta}(x,a)$ を用意する(ここは同じ)。
- 2. スコアに対して**ガンベル分布に従うノイズ**を加える。
- 3. スコア+ノイズの値が大きい順に、アイテムを並び替えて推薦アイテムリストを生成する。

数式で表すと以下。
($Gumbel(0,1)$ は標準ガンベル分布)

$$
\mathbf{a} = argsort_{a \in A} \{ f_{\theta}(x,a) + \epsilon_{a} \}
\\
\epsilon_{a} \sim Gumbel(0,1)
\tag{2}
$$

- 実は、**ガンベルソフトマックストリックでランキングを生成することは、PLモデルに基づくランキングの確率的サンプリングと同等(?)であることが知られているっぽい**。
- ガンベルソフトマックストリックを使うことで、ソフトマックス関数を適用することなくスコア関数に基づいたランキングを確率的に生成できるため、計算効率の意味で非常に嬉しい。

お気持ち実装だとこんな感じ

```python
def sampling_with_gumbel_softmax_trick(f_theta: ScoreFunction, x: FeatureVector, A: set[Item], k: int)->list[Item]:
    """
    ガンベルソフトマックストリックを使った推薦アイテムリストの確率的サンプリング
    """
    # 各アイテムのスコア $f_{\theta}(x,a)$ を用意する(ここは同じ)。
    score_by_item = {a: f_theta(x, a) for a in A}
    # スコアに対してガンベル分布に従うノイズを加える。
    gumbele_noises = np.random.gumbel(
        size=len(preference_score_by_id), loc=0.0, scale=1.0
    )
    perturbed_score_by_item = {
        a: score + noise for (a, score), noise in zip(score_by_item.items(), gumbele_noises)
    }
    # スコア+ノイズの値が大きい順のアイテムk個を、,推薦アイテムリストとして返す
    return sorted(perturbed_score_by_item.items(), key=lambda item_score: item_score[1], reverse=True)[:k]
```

#### 計算量ってどれくらいなんだろ？

- 変数:
  - $|A| = n$ (アイテム集合のサイズ)
  - $k$ (推薦リストの長さ)
- 各処理の計算量
  - スコアの計算: Aの各アイテムに対してスコアを計算してる。なので計算量はO(n)になる。
  - ガンベルノイズの生成: ガンベルノイズは標準ガンベル分布から生成している。これも計算量はO(n)になる。
  - スコアにノイズを加える: Aの各アイテムに対してスコアにノイズを加えている。計算量はO(n)になる。
  - スコア+ノイズの値が大きい順にソートして、上位k個を取り出す: `sorted`関数は計算量がO(n log n)。計算量はO(n log n)になる。

よって全体としては、計算量はO(n + n + n + n * log n) -> O(n log n)になりそう??:thinking:

### epsilon-greedyを使う

- 最後に、epsilon-greedyを使ったアイデアを考えてみます。
- epsilon-greedyの概要:
  - 強化学習でよく使われる探索戦略の1つ。
  - 行動を選択するたびに、確率 $\epsilon$ でランダムに行動を選択し、確率 $1-\epsilon$ でスコアが最も高い行動を選択する。

お気持ち実装だとこんな感じ

```python
def sampling_with_epsilon_greedy(f_theta: ScoreFunction, x: FeatureVector, A: set[Item], k: int, epsilon: float = 0.1)->list[Item]:
    """
    epsilon-greedyを使った推薦アイテムリストの確率的サンプリング
    """
    ranking = []
    # スコア関数 f_theta(x,a) を使って、個別のアイテムaについてスコアを計算してる
    score_by_item = {a: f_theta(x, a) for a in A}
    for _ in range(k):
        # 確率 epsilon で探索(ランダムに推薦アイテムを選択)
        if np.random.rand() < epsilon:
            a_i = np.random.choice(A)
        # 確率 1-epsilon で活用(最適なアイテムを選択)
        else:
            # スコアが最も高いアイテムを選択
            a_i = max(score_by_item, key=score_by_item.get)
        ranking.append(a_i)

        # 同一アイテムが重複して選ばれないように、選択されたアイテムを推薦候補から除外して、次のポジションのサンプリングへ
        A.remove(a_i)
    return ranking
```

#### 計算量ってどれくらいなんだろ？

- 変数:
  - $|A| = n$ (アイテム集合のサイズ)
  - $k$ (推薦リストの長さ)
- 各処理の計算量
  - スコアの計算: Aの各アイテムに対してスコアを計算してる。なので計算量はO(n)になる。
  - メインのループ処理: サンプリングする推薦リストの長さ $k$ 回ループする。ループの計算量はO(k)になる。
    - 探索か活用かの判定: `np.random.rand()`は定数時間で計算できる。計算量はO(1)になる。
    - 探索(ランダムに推薦アイテムを選択): `np.random.choice(A)`は `A`の要素数に依らずにかかる時間は一定。計算量は定数時間 O(1) になりそう。
    - 活用(最適なアイテムを選択): スコアが最も高いアイテムを選択する処理は、`max`関数を使っている。計算量はO(n)になる。
    - 選択されたアイテムを推薦候補から除外: `A`はset型。計算量はO(1)になる。

全体の計算量はO(n + k *(1 + n + 1)) -> O(n + k*n) -> O(k * n)になりそう??:thinking:
（プラケットルースモデルと同じくらい??:thinking:）

## 懸念: オンライン推論の場合、確率的な方策はレイテンシーとか大丈夫??

### 決定的な推薦方策の場合

お気持ち実装

```python
def sampling_with_deterministic_policy(f_theta: ScoreFunction, x: FeatureVector, A: set[Item], k: int)->list[Item]:
    """
    決定的な推薦アイテムリストの生成
    """
    # スコア関数 f_theta(x,a) を使って、個別のアイテムaについてスコアを計算してる
    score_by_item = {a: f_theta(x, a) for a in A}

    # スコアが最も高いアイテムk個を推薦アイテムリストとして返す
    return sorted(score_by_item.items(), key=lambda item_score: item_score[1], reverse=True)[:k]
```

この計算量は...

- 各処理の計算量
  - スコアの計算: Aの各アイテムに対してスコアを計算してる。なので計算量はO(n)になる。
  - スコアが最も高いアイテムを選択: `sorted`関数は計算量がO(n log n)。計算量はO(n log n)になる。

全体の計算量はO(n + n log n)になりそう??:thinking:
(gumbel softmax trickと同じくらい??:thinking:)

## 実際に実験してみる

### リアルタイム推論を想定した実験設定

- 問題設定
  - あるユーザに対して、n個のアイテム集合からk個のアイテムを推薦するタスクを考える。
  - クライアント側からuser_idを指定したリクエストを受け取り、そのユーザに対してk個のアイテムを推薦する。
  - スコア関数 $f_{theta}(x,a)$ について
    - 今回は、ユーザとアイテムの特徴を埋め込み表現をもとに、内積をスコアとするシンプルなスコア関数を想定する。
  - リアルタイム推論時には事前に作成された特徴量を使うケースを想定する。(特徴量作成はバッチ、推論だけリアルタイムのケース)

### ちなみに、今回の実験のための準備方法

- リアルタイムで推薦結果を作って返す推論サーバの作り方:
  - 今回はなるべく簡単にシンプルに推論サーバを提供するために、Sagemaker EndpointとAWS API Gatewayを紐付ける方法を試してみました!
  - 参考にしたAWS公式のブログ: [Creating a machine learning-powered REST API with Amazon API Gateway mapping templates and Amazon SageMaker](https://aws.amazon.com/jp/blogs/machine-learning/creating-a-machine-learning-powered-rest-api-with-amazon-api-gateway-mapping-templates-and-amazon-sagemaker/)

![アーキテクチャ図を作って追加する](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2020/03/04/api-gateway-sagemaker-1.gif)

- こんな感じのエンドポイントを作ってみました!

```shell
curl -X GET "https://xxxxxxxxx.execute-api.{aws-region}.amazonaws.com/1/recommended-items/{user_id}?k={推薦アイテムリストの長さ}&inference_type={推薦結果の作り方の種類}" 
```

- ちなみにSagemaker推論エンドポイントの設定は以下です:
  - instance_type: `ml.m5.large` (利用料金は 0.149 USD/hour)
    - 今回は $f_{\theta}(x,a)$ の計算がシンプルな内積計算なので、m5.largeで十分です!
    - 参考: <https://aws.amazon.com/jp/sagemaker/pricing/>
  - instance_count: 1

## 実験結果

- パスパラメータ
  - user_id=U:114521
- クエリパラメータ
  - k=10&inference_type=deterministic
  - k=10&inference_type=stochastic_plackett_luce
  - k=10&inference_type=stochastic_plackett_luce_cached
  - k=10&inference_type=stochastic_gumbel_softmax_trick
  - k=10&inference_type=stochastic_epsilon_greedy
- リクエストヘッダ:

```yml
content-type:application/json
accept:application/json
```

パッと数回、リクエストを投げてみた結果...。体感的には、どれが遅いとか早いとかなさそうな感じ...:thinking:

- `inference_type=deterministic`
  - 80msくらい
- `inference_type=stochastic_plackett_luce`
  - 80msくらい
- `inference_type=stochastic_plackett_luce_cached`
  - 80msくらい
- `inference_type=stochastic_gumbel_softmax_trick`
  - 80msくらい
- `inference_type=stochastic_epsilon_greedy`
  - 80msくらい

## ちゃんとレイテンシー計測してみたい

### locust

以下の資料を参考に、**locustという負荷試験ツール**を使って、Sagemaker Endpointのレイテンシーを計測してみます。

- 参考: [SageMaker Endpointのレイテンシーを負荷試験ツールlocustで計測する](https://nsakki55.hatenablog.com/entry/2022/12/14/091430)
- locustとは
  - 参考: [【初心者でも安心】Locustで始める負荷テスト](https://zenn.dev/secondselection/articles/locust_sample)
  - オープンソースのPython製の負荷試験ツールの1つ。
    - Pythonistaに使いやすくシンプルなUIで負荷試験ができる
  - locust=イナゴ、という意味らしい。
    - イナゴのように群れて大量発生したリクエストをサーバ（アプリケーション）がどれだけ対処できるかをテストする感じ...!:thinking:

### locustの使い方

`task`という概念を使って、ユーザが操作する想定のタスク（シナリオ）を定義する。

```python:locust_experiment.py
from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 5) # ユーザのリクエスト間隔を1-5秒の間でランダムに設定

    @task
    def test_httpbin(self):
        self.client.get("/get")
```

その後、以下のコマンドでWeb UIを立ち上げる

```shell
locust -f locust_experiment.py --host https://httpbin.org
```

続いて、UIからパラメータを入力し、テストを開始する（各パラメータは起動時にoptionalな引数としても指定できるはず...?）

- Number of users (peak concurrency): 同時ユーザ数(最大)
- Ramp Up (users started/second): 1秒間でのユーザ増加数
- Host: リクエスト先

### いざ実験

今回はレイテンシーに興味があるため、ユーザー数を1としてSageMaker Endopointの負荷をかけすぎないようにしています。
