# DRN: A Deep Reinforcement Learning Framework for News Recommendation

published date: April 2018,
authors: Guanjie Zheng, Fuzheng Zhang, Zihan Zheng, Yang Xiang, Nicholas Jing Yuan, Xing Xie, Zhenhui Li
url(paper): https://dl.acm.org/doi/fullHtml/10.1145/3178876.3185994
(勉強会発表者: morinota)

---

## どんなもの?

## 先行研究と比べて何がすごい？

オンラインパーソナライズドニュースの推薦問題を解決するために、コンテンツベースの方法[19, 22, 33]、協調フィルタリングベースの方法[11, 28, 34]、ハイブリッド方法[12, 24, 25]など、いくつかのグループの方法が提案されている.
近年、これまでの手法の拡張・統合として、ディープラーニングモデル[8, 45, 52]が、複雑な ユーザアイテム (ニュースなど)のやり取りをモデル化できることから、新たな最先端手法となっている.

しかし、これらの手法は、**ニュース推薦における以下の3つの課題**を効果的に解決することはできない.

### 課題1 ニュース推薦がダイナミックに変化することが扱いにくい.

- ニュース推薦のダイナミックな変化は、以下の2つの側面から示すことができる.
- 第一に、**ニュースはすぐに古くなる**.
  - 我々のデータセットでは、**1つのニュースが公開されてから最後にクリックされるまでの平均時間は4.1時間である**.
- 第二に、**ユーザの様々なニュースに対する興味は、時間の経過とともに変化する**可能性がある.
  - ex. 図1は、あるユーザが10週間に読んだニュースのカテゴリを表示したもの.
  - このユーザは、最初の数週間は"政治"（図1の緑のバー）を好んで読むが、時間の経過とともに"娯楽"（図1の紫のバー）や"技術"（図1の灰色のバー）に徐々に関心が移っていく.
  - そのため、定期的にモデルを更新する必要がある.
  - **オンラインモデル更新により、ニュースの特徴やユーザの嗜好の動的変化を捉えることができるオンライン推薦手法** [11, 24] もあるが、それらは現在の報酬（例えば、クリック率）を最適化しようとするだけであり、**現在の推薦が将来にもたらすであろう影響を無視している**.

![](https://camo.qiitausercontent.com/ab51592008bbdad5e97e078adb976a4031ea0933/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f32313436646138302d313138622d643635332d663839642d6135633431393565366165662e706e67)

将来を考える必要性を示す例として、例1.1.を挙げる.

- 例1.1:
  - ユーザMikeがニュースを要求したとき、推薦エージェントは、雷雨警報に関するニュースと、バスケットボール選手Kobe Bryantに関するニュースの**2つをクリックする確率がほぼ同じであることを予測している**とする.
  - しかし、マイクの読書嗜好、ニュースの特徴、他のユーザーの読書パターンによると、雷雨のニュースを読んだ後、マイクはこの警報に関するニュースを読む必要はなくなったが、**コービーに関するニュースを読んだ後は、バスケットボールに関するニュースをもっと読むだろうと、我々のエージェントは推測する**のである.

この例は、**後者のニュースを推薦することで、より大きな報酬が得られることを示唆している**.
そのため、将来の報酬を考慮することで、長期的にレコメンデーションパフォーマンスを向上させることができる.

### 課題2: 現在の推薦手法[23, 35, 36, 43]は、通常、クリックを考慮するのみ

次に、現在の推薦手法[23, 35, 36, 43]は、通常、クリックを考慮するのみである.
しかし、**あるユーザがどれだけ早くこのサービスに戻ってくるか**[48]は、このユーザが推薦にどれだけ満足しているかを示すことにもなる.
とはいえ、**ユーザの帰省パターン**を取り入れて、レコメンデーションの改善に役立てようという試みは、これまでほとんど行われてこなかった.

### 課題3:

現在の推薦手法の3つ目の大きな問題は、**ユーザに似たようなものを推薦し続ける傾向があり、ユーザの類似した話題への興味を低下させる可能性があること**.
文献では、**すでにいくつかの強化学習法が、新しいアイテムを見つける判断にランダム性（＝ exploration ）を加えることを提案している**.
最新の強化学習法では、通常、単純な?グリーディ戦略 [31] またはUCB (Upper Confidence Bound) [23, 43] (主に多腕バンディット法) を適用する.
しかし、どちらの戦略も、**短期間では、推薦者のパフォーマンスをある程度損なう可能性がある**.
ϵグリーディ戦略では、全く関係のないアイテムを顧客に勧めることがあるが、UCBでは、そのアイテムが何度か試されるまでは、比較的正確な報酬推定を得ることができない.
そのため、**より効果的な探索を行うことが必要**.

### 課題1 ~ 3を踏まえて...

本論文では、オンラインパーソナライズドニュース推薦におけるこれら**3つの課題を解決するのに役立つDeep Reinforcement Learningフレームワーク**を提案する.

まず、ニュースの特性やユーザーの嗜好の動的な性質をよりよくモデル化するために、**Deep Q-Learning (DQN) [31] のフレームワークを使用することを提案**する.
このフレームワークは、**現在の報酬と将来の報酬を同時に考慮することができる**.
強化学習を推薦に用いる最近の試みは、将来の報酬を明示的にモデル化していない（MABベースの作品[23, 43]）、あるいは、状態を表すために離散的なユーザログを用いるため、大規模システムに拡張することができない（MDPベースの作品 [35, 36]）というものである.
これに対し、我々のフレームワークは**DQN構造**(??)を採用しており、容易にスケールアップすることが可能.
**第二に、各ユーザのアクティブネススコアを保持することで、ユーザリターンをユーザフィードバック情報のもう一つの形として考えている.**
第三に、現在のレコメンダーの近傍にあるアイテム候補をランダムに選んで探索する **Dueling Bandit Gradient Descent (DBGD) 法** [16, 17, 49] を適用することを提案する.

## 技術や手法の肝は？

### Deep Q-Learning (DQN)による推薦システムの概要:

私たちの深層強化レコメンダーシステムは、図2のように示すことができる.

![](https://camo.qiitausercontent.com/abb6a468bc200566c692011fa7f0f486c214912b/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f33373434386534362d663862652d333862652d613563622d3163656261306433633130622e706e67)

システムを説明するために、強化学習[37]の一般的な用語に従う.

- environment: ユーザプールとニュースプールが環境を構成.
- agent: 推薦アルゴリズムがエージェントの役割を果たす.
- state: ユーザーの特徴表現.
- action: ニュースの特徴表現.

ユーザがニュースを要求するたびに、state表現(i.e.ユーザの特徴)とaction表現(i.e. すなわちニュース候補の特徴)のセットが、エージェントに渡される.
エージェントは、最適なアクション(i.e. ユーザに推薦するニュースのリスト)を選択し、報酬としてユーザのフィードバックを取得する.
具体的には、クリックラベルとユーザの activeness を推定することで報酬を構成している.
これらのレコメンデーションとフィードバックログは、すべてエージェントのメモリに保存される.
1時間ごとに、エージェントはメモリ内のログを利用して、推薦アルゴリズムを更新する.

#### Model Framework

#### 特徴量:

- news features:
- user features:
- user news features:
- context features:

強化学習推薦フレームワークの分析に集中するため、テキスト特徴[45]など、より多くの特徴量を追加することは試みなかったが、簡単に適用可能.

### 工夫1:Deep Q-Learning (DQN) [31] のフレームワークを使用:

前述したニュース推薦の動的な特徴と将来の報酬を推定する必要性を考慮し、あるユーザがある特定のニュースをクリックする確率をモデル化するために、**Deep Q-Network (DQN)** [31] を適用する.
強化学習の設定では、**ユーザがニュース(および将来の推薦ニュース)をクリックする確率**が、基本的に我々のエージェントが得ることのできる**報酬**となる.
従って、総報酬を式1のようにモデル化できる:

$$
y_{s, a} = Q(s, a) = r_{immediate} + \gamma r_{future}
\tag{1}
$$

ここで,

- $s$:
- $a$:
- $r_{immediate}$:
- $r_{future}$:
- $\gamma$: 割引係数(discount factor).

具体的には、sを現在の状態として、DDQN[41]ターゲットを用いて、式2のようにタイムスタンプtで行動aをとることによる報酬の合計を予測する.

$$
y_{s,a,t} = r_{a, t+1}  + \gamma Q(s_{a, t+1}, \argmax_{a'} Q(s_{a,t+1}, a':W_t);W_t')
\tag{2}
$$

ここで、

- $r_{a, t+1}$: 時刻tにて行動aをとることによる即時報酬.(添字t+1は、報酬が常に行動より1タイムスロット遅れるから!)(状況 sには依存しないの??)
- $W_t$ と $W_t'$: DQNの**2種類**(=切り替えて使うパラメータがある???)のパラメータセット.

この定式化では、エージェントGは、行動aが選択された場合に、次の状態$s_{a,t+1}$を推測することになる.(=つまり状態遷移関数??)
これに基づき、アクションの候補セット ${a'}$ が与えられると、パラメータ $W_t$ に従って、**将来報酬が最大となるアクション$a′$を選択する**.
この後、状態$s_{a,t+1}$が与えられた将来の推定報酬が$W'_t$に基づいて計算される.

数回繰り返すごとに、WtとW′tが入れ替わる.(??)この戦略により、Qの過大な値推定を排除できることが証明されている[41].

![](https://camo.qiitausercontent.com/8d81be7978a10e4553b595c575772da7fe78fd26/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f34323739373361372d363535312d646639642d356139652d6332363231326139313365322e706e67)

図4に示すように、4つのカテゴリーの特徴をネットワークに投入する.
ユーザ特徴量とコンテキスト特徴量を状態特徴量として、ユーザ\*ニュース特徴量とニュース特徴量を行動特徴量として使用する.
ある状態sで行動aをとったときの報酬(=即時報酬??)は、すべての特徴と密接に関係している.
一方、ユーザー自身の特性(例えば、このユーザーはアクティブか、このユーザーは今日十分なニュースを読んだか)によって決まる報酬(=将来報酬??)は、ユーザーのステータスと文脈のみに影響されやすいと言える.
この観察に基づき、[47]と同様に、Q関数を価値関数(value function) $V(s)$ と優位関数(advantage function) $A(s, a)$ に分け、$V(s)$は状態特徴のみ、$A(s, a)$は状態特徴と行動特徴の両方によって決定される.(つまりvalue functionは将来報酬, advantage functionは即時報酬を出力する関数??)

### 工夫2: 各ユーザのuser returnを feedbackの追加要素として考慮:

従来のレコメンダーシステムは、**CTRのような指標の最適化(クリック／クリックなしのラベルの活用のみ)にのみ**注力しており、ユーザーからのフィードバック情報の一部しか描かれていなかった.
レコメンデーションの性能は、**ユーザが再びアプリケーションを使いたいと思うかどうかにも影響を与えるかもしれない**.
したがって、user activenessの変化もきちんと考慮する必要がある.

- -> (具体的には?)ユーザからのニュースに対するリクエストが不規則なパターンである.(??)
  - ユーザは通常、30分程度の短時間でニュースを読み、その間に高い頻度でニュースのリクエストやクリックを行う.
  - そして、一度アプリケーションから離れ、数時間後にもっとニュースを読みたくなったときにアプリケーションに戻るかもしれない.
  - ユーザリターン とは、**ユーザがニュースを要求したときに発生するもの**である(ユーザーはニュースをクリックする前に必ずニュースを要求するため、ユーザクリックも暗黙のうちに考慮される).

**生存モデル[18, 30]を使用**して、ユーザリターン(ユーザの復帰?)とユーザの活性化をモデル化する.

次のイベント（ユーザーリターン）が起こるまでの時間を $T$ とすると、hazard function(イベントが起こりうる 瞬間的な割合=微分っぽい? = **たぶん$T = t$となるような確率密度関数**)は、式3のように定義できる.

$$
\lambda(t) = \lim_{dt -> 0} \frac{Pr(t \leq T < t + dt|T \geq t)}{dt}
\tag{3}
$$

すると、**$t$ 以降にイベントが発生する確率**は式4で定義できる[1, 30].

$$
S(t) = e^{- \int_{0}^{t} \lambda(x)dx}
\tag{4}
$$

そして、expected lifespan $T_0$ は次のように計算できる[1, 30].

$$
T_0 = \int_{0}^{\infty} S(t) dt
\tag{5}
$$

- この問題では、単純に$\lambda(t)=\lambda_0$を仮定する. これは**各ユーザが一定の確率で戻ってくること**を意味する.
- ユーザリターンを検出するたびに、この特定のユーザについて $S(t)=S(t)+S_a$ を設定することになる. (つまり、S(t)(=tにおけるユーザ活性度)を更新する...!)
- ユーザ活性度スコアは1を超えることはない.
- 例えば、図5に示すように、この特定ユーザの**ユーザ活性度は、時刻0の$S_0$から減衰し始める.**
- タイムスタンプt1ではユーザリターンが発生し、その結果、**ユーザのアクティブ度がSa上昇する**.
- そして、t1以降、**再びユーザの活性度は減衰し続ける**.t2、t3、t4、t5でも同様のことが起こる.
- なお、このユーザーはt4～t9の間は比較的リクエスト(=ユーザリターン)頻度が高いが、**ユーザの活性度の最大値は1に切り捨てられている**.

![](https://camo.qiitausercontent.com/0c71918b587e78c40f06786909e4d146673713a1/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f66366537366664632d656139322d363165362d626165372d3839386263656330396565642e706e67)

ここで、パラメータS0, Sa, λ0, T0は、本データセットに含まれる実際のユーザパターンに応じて決定される.("決定される"=ハイパーパラメータって意味??)

- S0は、ユーザのランダムな初期状態(つまり、アクティブにもインアクティブにもなる)を表すために0.5に設定されている.(=じゃあハイパーパラメータなのか...!)
- 図6に示すように、ユーザの連続した2つのリクエストの間の時間間隔のヒストグラムを観察することができる.
- 1日に何度もニュースを読む以外に、**毎日定期的にアプリケーションに戻るのが普通**であることが観察される. -> T0を24時間に設定.
- 減衰パラメータλ0は、式4と式5により、$1.2 \times 10^{-5} \text{ second}^{-1}$ に設定.
- 1回のクリックに対するユーザ活性度 増加量Saは、1日単位の要求でユーザーが初期状態に戻るように、0.32とした.
  - すなわち、$S_0 * $e^{- \lambda_0 T_0}$ + S_a = S_0$.

![](https://camo.qiitausercontent.com/fa73326005bd478a3983bcb3938e3b66875db2f8/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f33353431363763632d383934652d376562632d656539332d3533313262336334353262322e706e67)

そして、クリック/クリックなしラベル $r_{click}$ とユーザー活性度 $r_{active}$ は、式6のように組み合わせている.

$$
r_{total} = r_{click} + \beta r_{active}
\tag{6}
$$

ここでは、生存モデルを用いてユーザ活性度を推定しているが、ポアソン点過程[13]などの**他の選択肢も適用可能**.

### 工夫3: Dueling Bandit Gradient Descent (DBGD) 法による探索戦略

強化学習において探索を行う最も簡単な戦略は、epsilon-greedy [31]とUCB [23]だが、**このような些細な探索手法では、短期間で推薦性能に悪影響が出ることは明らか**.
そこで、ランダムな探索を行うのではなく、**Dueling Bandit Gradient Descentアルゴリズム** [16, 17, 49] を適用して探索を行う.

![](https://camo.qiitausercontent.com/b7a25c517a559b3a2975b733201ea2637eb67980/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f64393163633666312d643166642d336631352d343531322d3763383635626338646537612e706e67)

**直感的には、図7に示すように、エージェントGは、現在のネットワークQを用いて推薦リストLを生成し、探索ネットワーク $Q^~$ を用いて別のリスト$L^~$を生成**しようと考えている.
ネットワーク$Q^~$のパラメータ $W^~$ は、**現在のネットワークのパラメータ $W$ に小さな外乱 $\delta W$ (式7)を加えることで得ることができる**.

$$
\Delta W = \alpha \cdot rand(-1, 1) \cdot W
\tag{7}
$$

ここで、

- αは探索係数
- rand(-1, 1)は-1～1の乱数.

次に、エージェントGは、確率的interleave[16](=複数のランキングを混ぜ合わせる手法!)を行い、 $L$ と $L^~$ を用いてマージされた推薦リスト $\hat{L}$ を生成する.(なるほど、ここでInterleavingの手法が出てくるのか...!)

- 確率的interleaveに関して:
  - 推薦リスト$\hat{L}$の各位置のアイテムを決定するために、確率的インターリーブアプローチは基本的に、まずリストLとL〜をランダムに選択する.
  - Lが選択されたとすると、Lのアイテムiは、Lでの順位で決まる確率でLˆに入れられる(順位が上位のアイテムは高い確率で選択される).
  - そして、リストLˆがユーザuに推薦され、**エージェントGはフィードバックBを得る**ことになる.

**探索ネットワーク $Q^~$ が推薦するアイテムがより良いフィードバックを受けた場合、エージェントGはネットワークQをQ〜に向けて更新**される.
ネットワークQのパラメータは式8のように更新される:

$$
W' = W + \eta \tilde{W}
\tag{8}
$$

そうでない場合は、エージェントGは**ネットワークQを変更せずに維持する**.(=フィードバックを受けて更新しないの? あ、一時間毎に更新するんだっけ)
このような探索を行うことで、**エージェントは推薦精度をあまり落とさずに、より効果的な探索を行うことができる**.

## どうやって有効だと検証した?

本システムは、商用ニュース推薦アプリケーションでオンライン展開された. オフラインとオンラインの広範な実験により、本手法の優れた性能が示された.

### オフライン実験

まず、オフラインデータセットにおいて、我々の手法を他のベースラインと比較する.
オフラインデータセットは静的なものであり、**ユーザニュースのインタラクションの特定のペアのみが記録されている**.

#### Accuracy

精度の結果を表4に示す.

![](https://camo.qiitausercontent.com/e594ccb17585f55586b00b02dceeb517395709df/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f39396164613663632d333130362d663663372d646337372d6532336536376361623636352e706e67)

我々のアルゴリズムは全てのベースラインアルゴリズムを凌駕した.
ベースモデルのDNは、すでにベースラインと比較して非常に良い結果を出している.
これは、**dueling network構造の方が、ユーザーとニュースの相互作用をよりよくモデル化できるため**.
将来の報酬を考慮すること（DDQN）を加えることで、さらに大きな改善を実現している.
そして、ユーザactivenessや探索性を取り込んでも、オフライン環境下では必ずしも性能は向上しない、
これは、オフラインの設定では、候補となるニュースの静的な集合が限られているため、**アルゴリズムがユーザと最適なやりとりをすることができない**ためと思われる.
また、ϵ-greedyのような素朴なランダム探索は、推薦精度を低下させることになる.

#### モデルの収束処理(Model converge process)

図9に異なる手法の累積CTRを示し、収束の過程を説明する.
オフラインデータは時間順に並んでおり、ユーザが時間の経過とともにニュースリクエストを送信する過程をシミュレートしている.
比較されたすべての方法は、100リクエストセッションごとにモデルを更新する.

![](https://camo.qiitausercontent.com/78407c2c4c6e67abb4c2c0b239174ff139746ed6/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f62623137373533622d313061652d373830372d666430312d3937373238363233656534662e706e67)

予想通り、我々のアルゴリズム（DDQN + U + DBGD）は、他の方法よりも早く良いCTRに収束する.

### オンライン実験

オンライン評価段階では、商用ニュース推薦アプリケーションにモデルを導入し、アルゴリズムを比較した.
ユーザはアルゴリズムごとに均等に分かれている.
オンライン設定では、推薦の精度を測定するだけでなく、異なるアルゴリズムによる推薦の多様性を観察する事ができる.
いずれのアルゴリズムも、ニュースリクエストがあったときに、**トップ20**のニュースをユーザに推薦するように設計されている.

#### Accuracy

CTR、Precision@5、nDCGの観点から、異なるアルゴリズムを比較する.

![](https://camo.qiitausercontent.com/868976b26a1c74fbc8e732c57eabf47db42c594b/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f65393037643663392d616663302d303965392d306632612d3262363264316365656330612e706e67)

表5に示すように、我々のフルモデルDDQN + U + DBGDは、CTR、Precision@5、nDCGの点で他のすべてのモデルを大きく上回った.
**将来の報酬を追加する（DDQN）ことで、基本的なDNよりも推薦精度が向上する.**
しかし、さらにユーザの活性度を考慮したUを追加しても、推薦精度の面ではあまり意味がないように思われる. (ただし、このコンポーネントはユーザのactivenessやレコメンデーションの多様性を向上させるのに有用.)
また、DBGDを探索手法として用いることで、古典的なϵグリーディ法で引き起こされる性能低下を回避することができる.

#### Diversity

最後に、探索の効果を評価するために、ILSを用いた各アルゴリズムの推薦多様性を計算する.

$$
ILS(L) = \frac{\sum_{b_i \in L} \sum_{b_j \in L, b_j \neq b_i} S(b_i, b_j)}
{\sum_{b_i \in L} \sum_{b_j \in L, b_j \neq b_i} 1}
\tag{13}
$$

ここで、$S(b_i, b_j)$ は、アイテム bi と bj の間のコサイン類似度を表す.
表6に、ユーザがクリックしたニュースの多様性を示す.

![](https://camo.qiitausercontent.com/0b326a143f9cb2e1a42b7f02ac776091d14a06ec/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f39373836353265362d633135362d323436392d323336352d6265313165613035326133312e706e67)

一般的に、我々のアルゴリズムDDQN + U + DBGDのユーザーは、最高のクリック多様性を達成する.
興味深いことに、EGを追加しても推薦の多様性は改善されないらしい.
これは、ランダム探索（＝EG）を行った場合、レコメンダーが**ユーザに全く関係のないものを推薦してしまう**可能性があるためと考えられる.
これらの項目は多様性が高いが、ユーザーは読むことに興味を持たず、より自分の興味に合った項目の続きを読むために引き返してしまうかもしれない. そうすると、この探索は推薦の多様性を向上させることにはつながらない.

## 議論はある？

- 今後の課題:
  - ヘビーユーザやと一度きりのユーザなど、異なるユーザタイプに対応したモデルを設計することがより有意義なのでは...??
  - 特に user-activeness を測る指標は重要そう?

## 次に読むべき論文は？

- REINFORCEの元論文は読んでおくべきかもしれない. [Simple statistical gradient-following algorithms for connectionist reinforcement learning](https://link.springer.com/article/10.1007/BF00992696)

## お気持ち実装

余力がなく実装できず...! また!
