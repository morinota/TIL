refs: https://arxiv.org/pdf/1902.04056


# Policy Learning for Fairness in Ranking ランキングにおける公平性のためのポリシー学習
**Ashudeep Singh** ashudeep@cs.cornell.edu  
**Thorsten Joachims** tj@cs.cornell.edu _Department of Computer Science, Cornell University, Ithaca, NY_ コーネル大学コンピュータサイエンス学科、ニューヨーク州イサカ

## Abstract 要約

Conventional Learning-to-Rank (LTR) methods optimize the utility of the rankings to the users, but they are oblivious to their impact on the ranked items. 
従来の学習ランキング（LTR）手法は、ユーザに対するランキングの有用性を最適化しますが、**ランキングされたアイテムへの影響には無関心**です。
However, there has been a growing understanding that the latter is important to consider for a wide range of ranking applications (e.g. online marketplaces, job placement, admissions). 
しかし、後者がオンラインマーケットプレイス、職業紹介、入学などの幅広いランキングアプリケーションにおいて考慮すべき重要な要素であるという理解が高まっています。
To address this need, we propose a general LTR framework that can optimize a wide range of utility metrics (e.g. NDCG) while satisfying fairness of exposure constraints with respect to the items. 
このニーズに応えるために、アイテムに関する露出の公平性制約を満たしながら、幅広い有用性指標（例：NDCG）を最適化できる一般的なLTRフレームワークを提案します。
This framework expands the class of learnable ranking functions to stochastic ranking policies, which provides a language for rigorously expressing fairness specifications. 
このフレームワークは、**学習可能なランキング関数のクラスを確率的ランキングポリシーに拡張**し、公平性仕様を厳密に表現するための言語を提供します。
Furthermore, we provide a new LTR algorithm called Fair-PG-Rank for directly searching the space of fair ranking policies via a policy-gradient approach. 
さらに、**ポリシー勾配アプローチを介して公平なランキングポリシーの空間を直接探索するための新しいLTRアルゴリズム**であるFair-PG-Rankを提供します。
Beyond the theoretical evidence in deriving the framework and the algorithm, we provide empirical results on simulated and real-world datasets verifying the effectiveness of the approach in individual and group-fairness settings. 
フレームワークとアルゴリズムの導出における理論的証拠を超えて、個人およびグループの公平性設定におけるアプローチの有効性を検証するシミュレーションデータセットと実世界データセットに関する実証結果を提供します。

<!-- ここまで読んだ! -->

## 1. Introduction はじめに

Interfaces based on rankings are ubiquitous in today’s multi-sided online economies (e.g., online marketplaces, job search, property renting, media streaming).  
ランキングに基づくインターフェースは、今日の多面的なオンライン経済（例：オンラインマーケットプレイス、求人検索、不動産賃貸、メディアストリーミング）において普遍的です。  
In these systems, the items to be ranked are products, job candidates, or other entities that transfer economic benefit, and it is widely recognized that the position of an item in the ranking has a crucial influence on its exposure and economic success.  
これらのシステムでは、ランキングされるアイテムは製品、求職者、または経済的利益を移転する他のエンティティであり、アイテムのランキングにおける位置がその露出と経済的成功に重要な影響を与えることが広く認識されています。 
Surprisingly, though, the algorithms used to learn these rankings are typically oblivious to the effect they have on the items.  
**驚くべきことに、これらのランキングを学習するために使用されるアルゴリズムは、通常、アイテムに与える影響に無頓着**です。  
Instead, the learning algorithms blindly maximize the utility of the rankings to the users issuing queries to the systems (Robertson, 1977), and there is evidence (e.g. Kay et al. (2015); Singh and Joachims (2018)) that this does not necessarily lead to rankings that would be considered fair or desirable.  
代わりに、学習アルゴリズムはシステムにクエリを発行するユーザに対してランキングの効用を盲目的に最大化し（Robertson, 1977）、このことが必ずしも公正または望ましいと見なされるランキングにつながるわけではないという証拠があります（例：Kay et al. (2015); Singh and Joachims (2018)）。

In contrast to fairness in supervised learning for classification (e.g., Barocas and Selbst (2016); Dwork et al. (2012); Hardt et al. (2016); Zemel et al. (2013); Zafar et al. (2017); Kilbertus et al. (2017); Kusner et al. (2017)), fairness for rankings has been a relatively under-explored domain despite the growing influence of online information systems on our society and economy.  
分類のための教師あり学習における公正性（例：Barocas and Selbst (2016); Dwork et al. (2012); Hardt et al. (2016); Zemel et al. (2013); Zafar et al. (2017); Kilbertus et al. (2017); Kusner et al. (2017)）とは対照的に、**ランキングの公正性は、オンライン情報システムが私たちの社会と経済に与える影響が増大しているにもかかわらず、比較的未開拓の領域**です。  
In the work that does exist, some consider group fairness in rankings along the lines of demographic parity (Zliobaite, 2015; Calders et al., 2009), proposing definitions and methods that minimize the difference in the representation between groups in a prefix of the ranking (Yang and Stoyanovich, 2017; Celis et al., 2017; Asudehy et al., 2017; Zehlike et al., 2017).  
既存の研究の中には、ランキングにおけるグループの公正性を人口統計的平等の観点から考慮し（Zliobaite, 2015; Calders et al., 2009）、ランキングの接頭辞におけるグループ間の表現の違いを最小化する定義と方法を提案するものがあります（Yang and Stoyanovich, 2017; Celis et al., 2017; Asudehy et al., 2017; Zehlike et al., 2017）。  
Other recent works have argued that fairness of ranking systems corresponds to how they allocate exposure to individual items or group of items based on their merit (Singh and Joachims, 2018; Biega et al., 2018).  
他の最近の研究では、ランキングシステムの公正性は、アイテムのメリットに基づいて個々のアイテムまたはアイテムのグループに露出をどのように配分するかに対応すると主張しています（Singh and Joachims, 2018; Biega et al., 2018）。  
These works specify and enforce fairness constraints that explicitly link relevance to exposure in expectation or amortized over a set of queries.  
これらの研究は、関連性を期待値で露出に明示的に結びつける公正性制約を特定し、強制します。  
However, these works assume that the relevances of all items are known and they do not address the learning problem.  
しかし、これらの研究はすべてのアイテムの関連性が知られていると仮定しており、**学習問題には対処していません**。  

In this paper, we develop the first Learning-to-Rank (LTR) algorithm – named Fair-PG-Rank – that not only maximizes utility to the users, but that also rigorously enforces merit-based exposure constraints towards the items.  
本論文では、**ユーザに対する効用を最大化するだけでなく、アイテムに対するメリットに基づく露出制約を厳密に強制する最初のLearning-to-Rank（LTR）アルゴリズム**であるFair-PG-Rankを開発します。  
Focusing on notions of fairness around the key scarce resource that search engines arbitrate, namely the relative allocation of exposure based on the items’ merit, such fairness constraints may be required to conform with anti-trust legislation (Scott, 2017), to alleviate winner-takes-all dynamics in a music streaming service (Mehrotra et al., 2018), to implement antidiscrimination measures (Edelman et al., 2017), or to implement some variant of search neutrality (Introna and Nissenbaum, 2000; Grimmelmann, 2011).  
検索エンジンが仲裁する重要な希少資源、すなわちアイテムのメリットに基づく露出の相対的配分に関する公正性の概念に焦点を当てることで、そのような公正性制約は反トラスト法（Scott, 2017）に準拠するため、音楽ストリーミングサービスにおけるウィナー・テイク・オールのダイナミクスを緩和するため（Mehrotra et al., 2018）、差別禁止措置を実施するため（Edelman et al., 2017）、または検索の中立性のいくつかの変種を実施するため（Introna and Nissenbaum, 2000; Grimmelmann, 2011）に必要とされるかもしれません。  
By considering fairness already during learning, we find that Fair-PG-Rank can identify biases in the representation that post-processing methods (Singh and Joachims, 2018; Biega et al., 2018) are, by design, unable to detect.  
学習中にすでに公正性を考慮することで、Fair-PG-Rankは、ポストプロセッシング手法（Singh and Joachims, 2018; Biega et al., 2018）が設計上検出できない表現のバイアスを特定できることがわかりました。  
Furthermore, we find that Fair-PG-Rank performs better than heuristic approaches (Zehlike and Castillo, 2018).  
さらに、Fair-PG-Rankはヒューリスティックアプローチ（Zehlike and Castillo, 2018）よりも優れた性能を発揮することがわかりました。 

From a technical perspective, the main contributions of the paper are three-fold.  
技術的な観点から、本論文の主な貢献は三つあります。  
First, we develop a conceptual framework in which it is possible to formulate fair LTR as a policy-learning problem subject to fairness constraints.  
第一に、公正なLTRを公正性制約に従ったポリシー学習問題として定式化することが可能な概念的枠組みを開発します。  
We show that viewing fair LTR as learning a stochastic ranking policy leads to a rigorous formulation that can be addressed via Empirical Risk Minimization (ERM) on both the utility and the fairness constraint.  
公正なLTRを確率的ランキングポリシーの学習として見ることで、効用と公正性制約の両方に対して経験的リスク最小化（ERM）を通じて対処できる厳密な定式化につながることを示します。  
Second, we propose a class of fairness constraints for ranking that incorporates notions of both individual and group fairness.  
第二に、個人の公正性とグループの公正性の両方の概念を取り入れたランキングのための公正性制約のクラスを提案します。  
And, third, we propose a policy-gradient method for implementing the ERM procedure that can directly optimize any information retrieval utility metric and a wide range of fairness criteria.  
第三に、**任意の情報検索効用メトリックと幅広い公正性基準を直接最適化できるERM手続き**を実装するためのポリシー勾配法を提案します。  
Across a number of empirical evaluations, we find that the policy-gradient approach is a competitive LTR method in its own right, that Fair-PG-Rank can identify and avoid biased features when trading-off utility for fairness, and that it can effectively optimize notions of individual and group fairness on real-world datasets.  
いくつかの実証評価を通じて、**ポリシー勾配アプローチが独自に競争力のあるLTR手法であり**、Fair-PG-Rankが効用と公正性のトレードオフを行う際にバイアスのある特徴を特定し回避できること、そして実世界のデータセットにおいて個人の公正性とグループの公正性の概念を効果的に最適化できることがわかりました。

<!-- ここまで読んだ! -->

## 2. Learning Fair Ranking Policies

The key goal of our work is to learn ranking policies where the allocation of exposure to items is not an accidental by-product of maximizing utility to the users, but where one can specify a merit-based exposure-allocation constraint that is enforced by the learning algorithm. 
私たちの研究の主な目標は、アイテムへの露出の割り当てがユーザーの効用を最大化する偶発的な副産物ではなく、**学習アルゴリズムによって強制されるメリットに基づく露出割り当て制約を指定できるランキングポリシーを学習すること**です。

An illustrative example adapted from Singh and Joachims (2018) is that of ranking 10 job candidates, where the probabilities of relevance (e.g., probability that an employer will invite for an interview) of 5 male job candidates are {0.89, 0.89, 0.89, 0.89, 0.89} and those of 5 female candidates are {0.88, 0.88, 0.88, 0.88, 0.88}. 
SinghとJoachims（2018）から適応した例として、10人の求職者をランキングする場合を考えます。5人の男性求職者の関連性の確率（例：雇用主が面接に招待する確率）は{0.89, 0.89, 0.89, 0.89, 0.89}であり、5人の女性候補者のそれは{0.88, 0.88, 0.88, 0.88, 0.88}です。
If these 10 candidates were ranked by probability of relevance – thus maximizing utility to the users under virtually all information retrieval metrics (Robertson, 1977) – the female candidates would get far less exposure (ranked 6,7,8,9,10) than the male candidates (ranked 1,2,3,4,5) even though they have almost the same relevance. 
もしこれらの10人の候補者が関連性の確率によってランク付けされていた場合（したがって、ほぼすべての情報検索メトリック（Robertson, 1977）の下でユーザーに対する効用を最大化する）、女性候補者は男性候補者よりもはるかに少ない露出（ランク6,7,8,9,10）を得ることになります。
In this way, the ranking function itself is responsible for creating a strong endogenous bias against the female candidates, greatly amplifying any exogenous bias that the employers may have. 
このように、ランキング関数自体が女性候補者に対して強い内生的バイアスを生み出す責任があり、雇用主が持つ可能性のある外生的バイアスを大いに増幅します。
Addressing the endogenous bias created by the system itself, we argue that it should be possible to explicitly specify how exposure is allocated (e.g. make exposure proportional to relevance), that this specified exposure allocation is truthfully learned by the ranking policy (e.g. no systematic bias towards one of the groups), and that the ranking policy maintains a high utility to the users. 
システム自体によって生じる内生的バイアスに対処するために、露出がどのように割り当てられるかを明示的に指定すること（例：露出を関連性に比例させる）が可能であるべきであり、この指定された露出割り当てがランキングポリシーによって真実に学習されるべきである（例：一方のグループに対する体系的なバイアスがない）、そしてランキングポリシーがユーザーに対して高い効用を維持するべきであると主張します。
Generalizing from this illustrative example, we develop our fair LTR framework as guided by the following three goals: 
この例から一般化して、**私たちは次の3つの目標に導かれて公正なLTRフレームワーク**を開発します。

_Goal 1_ : Exposure allocated to an item is based on its merit. More merit means more exposure. 
_目標1_ : アイテムに割り当てられる露出はそのメリットに基づいています。より多くのメリットはより多くの露出を意味します。

_Goal 2_ : Enable the explicit statement of how exposure is allocated relative to the merit of the items. 
_目標2_ : アイテムのメリットに対して露出がどのように割り当てられるかを明示的に述べることを可能にします。

_Goal 3_ : Optimize the utility of the rankings to the users while satisfying Goal 1 and Goal 2. 
_目標3_ : 目標1と目標2を満たしながら、ユーザーに対するランキングの効用を最適化します。

We will illustrate and further refine these goals as we develop our framework in the rest of this section. 
このセクションの残りの部分でフレームワークを開発する際に、これらの目標を示し、さらに洗練させていきます。
In particular, we first formulate the LTR problem in the context of empirical risk minimization (ERM) where exposure-allocation constraints are included in the empirical risk. 
特に、私たちはまず、露出割り当て制約が経験的リスクに含まれる経験的リスク最小化（ERM）の文脈でLTR問題を定式化します。
We then define concrete families of allocation constraints for both individual and group fairness. 
次に、個人およびグループの公正性のための具体的な割り当て制約のファミリーを定義します。


### 2.1 Learning to Rank as Policy Learning via ERM ERM(経験リスク最小化)によるポリシー学習としてのランキング学習

Let Q be the distribution from which queries are drawn. 
Qをクエリが引き出される分布とします。(i.e. ユーザ特徴量xの分布 P(x)...!:thinking:)
Each query q has a candidate set of documents d[q] = {d[q]1[, d][q]2[, . . . d][q]n(q)[}][ that needs to be ranked, and a corresponding set of real-valued] relevance judgments, rel[q] = (rel[q]1[,][ rel]2[q] _[. . .][ rel]n[q]_ (q)[)][. 
各クエリqには、ランク付けが必要なドキュメントの候補セット $d^{q} = \{d^{q}_{1}, d^{q}_{2}, \ldots, d^{q}_{n(q)}\}$ と、それに対応する実数値の関連性判断 $rel^{q} = (rel^{q}_{1}, rel^{q}_{2}, \ldots, rel^{q}_{n(q)})$ が存在します。
Our framework is agnostic to how relevance is] defined, and it could be the probability that a user with query q finds the document relevant, or it could be some subjective judgment of relevance as assigned by a relevance judge. 
私たちのフレームワークは、関連性がどのように定義されるかに依存しません。それは例えば、クエリqを持つユーザーがドキュメントを関連性があると見なす確率であったり、関連性の判断者によって割り当てられた主観的な関連性の判断であったりする可能性があります。
Finally, each document d[q]i [is represented by a feature vector][ x]i[q] [= Ψ(][q, d]i[q][)][ that describes the match between] document d[q]i [and query][ q][.] 
最後に各ドキュメント $d^{q}_{i}$ は、ドキュメント $d^{q}_{i}$ とクエリ $q$ の間のマッチを記述する特徴ベクトル $x^{i}_{q} = \Psi(q, d^{i}_{q})$ で表されます。

We consider stochastic ranking functions π ∈ Π, where π(r|q) is a distribution over the rankings r (i.e. permutations) of the candidate set. 
私たちは、確率的ランキング関数 $\pi \in \Pi$ を考慮します。ここで、$\pi(r|q)$ は候補セットのランキング $r$（すなわち順列）に対する分布です。
We refer to π as a ranking policy and note that deterministic ranking functions are merely a special case. 
私たちは**$\pi$をランキングポリシー**と呼び、決定論的ランキング関数は単なる特別なケースであることに注意します。(うんうん、反実仮想機械学習っぽいnotationだ...!:thinking:)
However, a key advantage of considering the full space of stochastic ranking policies is their ability to distribute expected exposure in a continuous fashion, which provides more fine-grained control and enables gradient-based optimization. 
しかし、**確率的ランキングポリシーの全空間を考慮することの重要な利点は、期待される露出を連続的に分配できること**であり、これによりより細かい制御が可能になり、勾配ベースの最適化が可能になります。

The conventional goal in LTR is to find a ranking policy π[∗] that maximizes the expected utility of π _π[∗]_ = argmaxπ∈Π Eq∼Q�U (π|q)�, 
LTRにおける従来の目標は、期待される効用を最大化するランキングポリシー $\pi^{*}$ を見つけることです。これは、次のように表されます： 

$$
\pi^{*} = \arg\max_{\pi \in \Pi} \mathbb{E}_{q \sim Q} [U(\pi | q)]
$$

where the utility of a stochastic policy π for a query q is defined as the expectation of a ranking metric ∆ over π _U_ (π|q) = Er∼π(r|q) �∆�r, rel[q][��] _._ 
ここで、クエリ $q$ に対する確率的ポリシー $\pi$ の効用は、ランキングメトリック $\Delta$ の期待値として定義されます。これは次のように表されます: 
(Utilityって、クエリ $q$ に対してランキング方策 $\pi$ を適用する場合の報酬期待値みたいな感じ...??:thinking:)

$$
U(\pi | q) = \mathbb{E}_{r \sim \pi(r|q)} [\Delta(r, rel[q])]
$$

Common choices for ∆ are DCG, NDCG, Average Rank, or ERR. 
**∆の一般的な選択肢には、DCG、NDCG、平均ランク、またはERR**があります。
For concreteness, we focus on NDCG as in (Chapelle and Chang, 2011), which is the normalized version of ∆DCG(r, rel[q]) = [�]j[n]=1[q] _ulog(1+(r(j)|jq))_ [,] where u(r(j)|q) is the utility of the document placed by ranking r on position j for q as a function of relevance (e.g., u(i|q) = 2[rel]i[q] − 1). 
具体的には、私たちはNDCGに焦点を当てます（Chapelle and Chang, 2011）。これは、次のように表される $\Delta_{DCG}(r, rel[q]) = \sum_{j=1}^{n[q]} \frac{u(r(j)|q)}{\log(1 + j)}$ の正規化バージョンです。ここで、$u(r(j)|q)$ は、ランキング $r$ によって位置 $j$ に配置されたドキュメントの効用を関連性の関数として表します（例：$u(i|q) = 2^{rel[i][q]} - 1$）。
NDCG normalizes DCG via ∆NDCG(r, rel[q]) = max∆rDCG ∆DCG(r,rel(r,[q]rel) _[q])_ [.]
NDCGは、次のようにDCGを正規化します：$\Delta_{NDCG}(r, rel[q]) = \frac{\Delta_{DCG}(r, rel[q])}{\max_{r'} \Delta_{DCG}(r', rel[q])}$。

<!-- ここまで読んだ! -->

#### Fair Ranking policies. 公正なランキングポリシー

Instead of single-mindedly maximizing this utility measure like in conventional LTR algorithms, we include a constraint into the learning problem that enforces an application-dependent notion of fair allocation of exposure. 
従来のLTRアルゴリズムのようにこの効用指標を単純に最大化するのではなく、私たちは露出の公正な割り当てのアプリケーション依存の概念を強制する制約を学習問題に含めます。
To this effect, let’s denote with D(π|q) ≥ 0 a measure of unfairness or the disparity, which we will define in detail in Section § 2.2. 
この目的のために、$D(\pi|q) >= 0$ を unfairness (不公平さ) または disparity (格差) の尺度とし、§ 2.2 で詳細に定義します。
We can now formulate the objective of fair LTR by constraining the space of admissible ranking policies to those that have expected disparity less than some parameter δ. 
これにより、期待される格差があるパラメータ $\delta$ よりも小さいランキングポリシーの空間を制約することによって、公正なLTRの目的を定式化できます。(方策を探索する際に、閾値を制約にするのか...!:thinking:)

_πδ[∗]_ [= argmax]π [E][q][∼Q] [[][U] [(][π][|][q][)]][ s.t.][ E][q][∼Q] [[][D][(][π][|][q][)]][ ≤] _[δ]_ 
_πδ[∗]_ [= argmax]π [E][q][∼Q] [[][U] [(][π][|][q][)]][ s.t.][ E][q][∼Q] [[][D][(][π][|][q][)]][ ≤] _[δ]_ 

$$
\pi^{*}_{\delta} = \argmax_{\pi} \mathbb{E}_{q \sim Q} [U(\pi | q)] \quad \text{s.t.} \quad \mathbb{E}_{q \sim Q} [D(\pi | q)] \leq \delta
% 日本語にすると、$\pi^{*}_{\delta}$ は、クエリ空間における効用の期待値を最大化しつつ、不公平さ期待値が $\delta$ 以下であるようなランキングポリシーを最適化する。
$$

Since we only observe samples from the query distribution Q, we resort to the ERM principle and estimate the expectations with their empirical counterparts. 
クエリ分布 $Q$ からのサンプルのみを観察するため、私たちはERM原則(=経験的リスク最小化原則)に頼り、期待値を経験的な対応物で推定します。
(これはつまり、クエリ分布 $Q$ から観測されたサンプルの経験平均を用いて、クエリ分布に対する各種期待値を推定する、ってこと...!:thinking:)
Denoting the training set as _T = {(x[q], rel[q])}q[N]=1[, the empirical analog of the optimization problem becomes_  
トレーニングセットを_T = {(x[q], rel[q])}q[N]=1_とし、最適化問題の経験的アナログ(=実際に計算する式?)は次のようになります。

$$
\hat{\pi}^{*}_{\delta} = \argmax_{\pi} \frac{1}{N} \sum_{q=1}^{N} U(\pi | q) \quad \text{s.t.} \quad \frac{1}{N} \sum_{q=1}^{N} D(\pi | q) \leq \delta
% 日本語にすると、$\pi^{*}_{\delta}$ は、トレーニングセットの経験平均による期待効用の推定値を最大化しつつ、トレーニングセットの経験平均による期待不公平さの推定値が $\delta$ 以下であるようなランキングポリシーを最適化する。
$$


Using a Lagrange multiplier, this is equivalent to  
ラグランジュ乗数 $\lambda$ を使用すると、これは次のように等価になります。

$$
\hat{\pi}^{*}_{\delta} = \argmax_{\pi} \min_{\lambda \geq 0} \frac{1}{N} \sum_{q=1}^{N} U(\pi | q) - \lambda \left( \frac{1}{N} \sum_{q=1}^{N} D(\pi | q) - \delta \right)
$$

In the following, we avoid minimization w.r.t. λ for a chosen δ. 
以下では、選択した $\delta$ に対して $\lambda$ に関する最小化を避けます。
Instead, we steer the utility/fairness trade-off by chosing a particular $\lambda$ and then computing the corresponding $\delta$ afterwards.
代わりに、特定の $\lambda$ を選択し、その後に対応する $\delta$ を計算することによって、効用と公正性のトレードオフを調整します。
This means we merely have to solve
これは、単に次の問題を解決する必要があることを意味します。

$$
\hat{\pi}^{*}_{\lambda} = \argmax_{\pi} \frac{1}{N} \sum_{q=1}^{N} U(\pi | q) - \lambda \frac{1}{N} \sum_{q=1}^{N} D(\pi | q)
\tag{1}
$$

and then recover δλ = _N[1]_ �Nq=1 _[D][(][π][ˆ]λ[∗][|][q][)][ afterwards. 
その後、$\delta_{\lambda} = \frac{1}{N} \sum_{q=1}^{N} D(\hat{\pi}^{*}_{\lambda} | q)$ を回復します。
Note that this formulation implements our third]_
goal from the opening paragraph, although we still lack a concrete definition of D. 
この定式化は、冒頭の段落からの私たちの3番目の目標を実装していますが、Dの具体的な定義はまだ欠けています。

<!-- ここまで読んだ! -->

### 2.2 Defining a Class of Fairness Measures for Rankings ランキングの公平性を測定するクラスの定義

To make the training objective in Equation (1) fully specified, we still need a concrete definition of the unfairness measure D. 
式(1)のトレーニング目的を完全に特定するためには、不公平さの尺度Dの具体的な定義がまだ必要です。
To this effect, we adapt the “Fairness of Exposure for Rankings” framework from Singh and Joachims (2018), since it allows a wide range of application dependent notions of group-based fairness, including Statistical Parity, Disparate Exposure, and Disparate Impact. 
この目的のために、私たちはSinghとJoachims（2018）からの「ランキングの露出の公正性」フレームワークを適応します。これは、統計的平等、不均等な露出、不均等な影響を含む、グループベースの公正性のアプリケーション依存の概念の広範囲を許可します。
In order to formulate any specific disparity measure D, we first need to define position bias and exposure. 
特定の格差測定Dを定式化するために、まず位置バイアスと露出を定義する必要があります。

#### **Position Bias**. 

The position bias of position j, vj, is defined as the fraction of users accessing a ranking who examine the item at position j. 
**位置バイアス**。位置 $j$ の**位置バイアス $v_j$ は、ランキングにアクセスするユーザのうち、位置 $j$ のアイテムを調べる割合**として定義されます。
This captures how much attention a result will receive, where higher positions are expected to receive more attention than lower positions. 
**これは、結果がどれだけの注意を受けるかを捉え、高い位置は低い位置よりも多くの注意を受けることが期待されます**。
In operational systems, position bias can be directly measured using eye-tracking (Joachims et al., 2007), or indirectly estimated through swap experiments (Joachims et al., 2017) or intervention harvesting (Agarwal et al., 2019; Fang et al., 2019). 
運用システムでは、位置バイアスは、アイ・トラッキング（Joachims et al., 2007）を使用して直接測定することができるか、スワップ実験（Joachims et al., 2017）や介入収穫（Agarwal et al., 2019; Fang et al., 2019）を通じて間接的に推定することができます。

<!-- ここまで読んだ! -->

#### **Exposure**. 

For a given query q and ranking distribution π(r|q), the exposure of a document is defined as the expected attention that a document receives. 
**露出**。特定のクエリ $q$ とランキング分布 $\pi(r|q)$ に対するドキュメントの露出は、**ドキュメントが受ける注意の期待値**として定義されます。
This is equivalent to the expected position bias from all the positions that the document can be placed in. 
これは、ドキュメントが配置される可能性のあるすべての位置からの位置バイアスの期待値に相当します。
Exposure is denoted as $v_{\pi}(d_i)$ and can be expressed as
露出は $v_{\pi}(d_i)$ $と表され、次のように表現できます。

$$
Exposure(d_{i}|\pi) = v_{\pi}(d_i) = \mathbb{E}_{r \sim \pi(r|q)} [v_{r}(d_i)]
$$

where $r(d_i)$ is the position of document $d_i$ under ranking $r$. 
ここで、$r(d_i)$ はランキング $r$ の下でのドキュメント $d_i$ の位置です。

#### **Allocating exposure based on merit.**

Our first two goals from the opening paragraph postulate that exposure should be based on an application dependent notion of merit. 
**メリットに基づく露出の割り当て。** 冒頭の段落からの最初の2つの目標は、**露出はアプリケーション依存のメリットの概念に基づくべき**であると仮定しています。
We define the _merit of a document as a function of its relevance to the query (e.g., $M_i = \text{rel}(d_i)$ for document $d_i$). 
私たちは、**ドキュメントのメリットをそのクエリに対する関連性の関数として定義**します（例：$rel_{i}$, $rel_{i}^2$, or $\sqrt{rel_{i}}$） 
Let’s denote the merit of document $d_i$ as $M_i \geq 0$, or simply $M_i$, and we state that each document in the candidate set should get exposure proportional to its merit $M_i$. 
ドキュメント $d_i$ のメリットを $M(rel_{i}) \geq 0$、または単に $M_i$ とし、**候補セット内の各ドキュメントはそのメリット $M_i$ に比例した露出を得るべき**であると述べます。

$$
% 全てのドキュメントにおいて、露出はメリットに比例すべき。
\forall d_i \in d^{q}, Exposure(d_i|\pi) \propto M(rel_i)
$$


For many queries, however, this set of exposure constraints is infeasible. 
しかし、多くのクエリに対して、この露出制約のセットは実現不可能です。
As an example, consider a query where one document in the candidate set has relevance 1, while all other documents have small relevance ϵ. 
例として、**候補セット内の1つのドキュメントが関連度 1 を持ち、他のすべてのドキュメントが小さな関連度 $\epsilon$ を持つクエリ**を考えます。(なんかepsilon-greedyっぽい設定だ...!!:thinking:)
For sufficiently small ϵ, any ranking will provide too much exposure to the ϵ-relevant documents, since we have to put these documents somewhere in the ranking. 
十分に小さなϵの場合、どのランキングでも関連度 $\epsilon$ のドキュメントに過剰な露出を提供します。なぜなら、これらのドキュメントをランキングのどこかに配置しなければならないからです。(なるほど、これだと、露出とメリットが比例する、という制約を満たせない:thinking:)
This violates the exposure constraint, and this shortcoming is also present in the Disparate Exposure measure of Singh and Joachims (2018) and the Equity of Attention constraint of Biega et al. (2018). 
これは露出制約に違反し、この欠点はSinghとJoachims（2018）の不均等な露出測定やBiegaら（2018）の注意の公平性制約にも存在します。

To overcome this problem of overabundance of exposure, we instead consider the following set of inequality constraints where ∀di, dj ∈ _d[q]_ with M (reli) ≥ _M_ (relj) > 0, 
<!-- 露出の過剰供給の問題を克服するために、私たちは代わりに次の不等式制約のセットを考慮します。ここで、∀di, dj ∈ _d[q]_ でM (reli) ≥ _M_ (relj) > 0です。 -->
露出の過剰供給の問題を克服するために、代わりに次の不等式制約のセットを考慮します。ここで、$\forall d_i, d_j \in d^{q}$ で $M(rel_i) \geq M(rel_j) > 0$ です。

$$
\frac{Exposure(d_i|\pi)}{M(rel_i)} \leq \frac{Exposure(d_j|\pi)}{M(rel_j)}
$$

This set of constraints still enforces proportionality of exposure to merit, but allows the allocation of overabundant exposure. 
この制約のセットは、**依然として露出をメリットに比例させることを強制しますが、過剰な露出の割り当てを許可**します。
This is achieved by only enforcing that higher merit items don’t get exposure beyond their merit, since the opposite direction is already achieved through utility maximization. 
これは、**より高いメリットのアイテムがそのメリットを超える露出を得ないようにすることを強制することによって達成されます**。なぜなら、逆の方向はすでに効用の最大化を通じて達成されているからです。
This counteracts unmerited rich-get-richer dynamics, as present in the motivating example from above. 
これは、上記の動機付けの例に見られるように、不当な富の集中ダイナミクスに対抗します。

<!-- ここまで読んだ! -->

#### Measuring disparate exposure. 不均等な露出の測定

We can now define the following disparity measure D that** captures in how far the fairness-of-exposure constraints are violated  
私たちは今、露出の公正性制約がどの程度違反されているかを捉える次の格差測定 $D$ を定義できます。

$$
D_{ind}(\pi|q) = \frac{1}{|H_q|} \sum_{(i,j) \in H_q} \max(0, \frac{Exposure(d_i|\pi)}{M(rel_i)} - \frac{Exposure(d_j|\pi)}{M(rel_j)})
\tag{3}
$$

where $H_q = \{(i,j) \mid M(rel_i) \geq M(rel_j) > 0\}$. 
ここで、$H_q = \{(i,j) \mid M(rel_i) \geq M(rel_j) > 0\}$ ($H_q$ は、メリットが高いドキュメントと低いドキュメントの全てのペアの集合)です。
The measure Dind(π|q) is always non-negative and it equals zero only when the individual constraints are exactly satisfied. 
格差測定 $D_{ind}(\pi|q)$ は常に非負であり、個々の制約が正確に満たされている場合にのみゼロになります。

<!-- ここまで読んだ! -->

#### Group fairness disparity.  グループの公正性の格差

The disparity measure from above implements an individual notion** of fairness, while other applications ask for a group-based notion. 
上記の格差測定は個々の公正性の概念を実装していますが、**他のアプリケーションではグループベースの概念を求めています**。(まあ確かに。動画ランキングの文脈では、各チャンネル単位の公正性を考えることも多そう...!:thinking:)
Here, fairness is aggregated over the members of each group. 
ここでは、公正性は各グループのメンバーに対して集約されます。
A group of documents can refer to sets of items sold by one seller in an online marketplace, to content published by one publisher, or to job candidates belonging to a protected group. 
ドキュメントのグループは、例えば、オンラインマーケットプレイスで1人の売り手によって販売されるアイテムのセット、1人の出版社によって公開されたコンテンツ、または保護されたグループに属する求職者を指すことができます。(うんうん...!:thinking:)
Similar to the case of individual fairness, we want to allocate exposure to groups proportional to their merit. 
個々の公正性のケースと同様に、私たちはグループに対してそのメリットに比例した露出を割り当てたいと考えています。
Hence, in the case of only two groups G0 and G1, we can define the following group fairness disparity for query q as  
したがって、2つのグループ $G_0$ と $G_1$ のみの場合、クエリ $q$ に対する次のグループ公正性の格差を定義できます:

$$
D_{group}(\pi|q) = \max(0, \frac{Exposure(G_i|\pi)}{M_{G_i}} - \frac{Exposure(G_j|\pi)}{M_{G_j}})
\tag{4}
$$

where Gi and Gj are such that MGi ≥ _MGj and Exposure(G|π) = vπ(G) =_ _|G1_ _|_ �di∈G _[v][π][(][d][i][)] is the average exposure of group G, and the merit of the group G is denoted by MG = _|G1_ _|_ �di∈G _[M][i][.]_
ここで、$G_i$ と $G_j$ は $M_{G_i} \geq M_{G_j}$ (i.e. つまりグループ $G_i$ のメリット 大なり等しい グループ $G_j$ のメリット) である。
$Exposure(G|\pi) = v_{\pi}(G) = \frac{1}{|G|} \sum_{d_i \in G} v_{\pi}(d_i)$ はあるグループ $G$ の平均露出を表し、グループ $G$ のメリットは $M_G = \frac{1}{|G|} \sum_{d_i \in G} M_i$ (i.e. グループ $G$ の全ドキュメントのメリットの平均) で表されます。

<!-- ここまで読んだ! -->

## 3. Fair-PG-Rank: A Policy Learning Algorithm for Fair LTR 公平なLTRのためのポリシー学習アルゴリズム

In the previous section, we defined a general framework for learning ranking policies under fairness-of-exposure constraints. 
前のセクションでは、露出の公平性制約の下でランキングポリシーを学習するための一般的なフレームワークを定義しました。
What remains to be shown is that there exists a stochastic policy class Π and an associated training algorithm that can solve the objective in Equation (1) under the disparities D defined above. 
残る課題は、上記の格差 D の下で式 (1) の目的を解決できる確率的ポリシークラス Π とそれに関連するトレーニングアルゴリズムが存在することを示すことです。 
To this effect, we now present the Fair-PG-Rank algorithm. 
この目的のために、私たちは今、Fair-PG-Rank アルゴリズムを提示します。 
In particular, we first define a class of Plackett-Luce ranking policies that incorporate a machine learning model, and then present a policy-gradient approach to efficiently optimize the training objective. 
特に、**最初に機械学習モデルを組み込んだ Plackett-Luce ランキングポリシー**のクラスを定義し、その後、トレーニング目的を効率的に最適化するためのポリシー勾配アプローチを提示します。 

### **3.1 Plackett-Luce Ranking Policies Plackett-Luce ランキングポリシー**

The ranking policies π we define in the following comprise of two components: a scoring model that defines a distribution over rankings, and its associated sampling method. 
以下で定義する**ランキングポリシー π は、ランキングに対する分布を定義するスコアリングモデルと、それに関連するサンプリング手法の2つのコンポーネントで構成**されています。
(メモ: やっぱりこの2段階にはなるのか。いきなりランキングをサンプリングするような手法はあまり現実的ではないのかも...!:thinking:)
Starting with the scoring model hθ, we allow any differentiable machine learning model with parameters θ, for example a linear model or a neural network.
スコアリングモデル $h_{\theta}$ から始めて、パラメータ $\theta$ を持つ任意の微分可能な機械学習モデル、たとえば線形モデルやニューラルネットワークを許可します。 
Given an input x[q] representing the feature vectors of all query-document pairs of the candidate set, the scoring model outputs a vector of scores _hθ(x[q]) = (hθ(x[q]1[)][, h][θ][(][x][q]2[)][, . . . h][θ][(][x]n[q]_ _q_ [))][. 
候補セットのすべてのクエリ-ドキュメントペアの特徴ベクトルを表す入力 $x^q$ が与えられると、スコアリングモデルはスコアのベクトル $h_{\theta}(x^q) = (h_{\theta}(x^q_1), h_{\theta}(x^q_2), \ldots, h_{\theta}(x^{n[q]}))$ を出力します。
Based on this score vector, the probability][ π][θ][(][r][|][q][)][ of a ranking] _r = ⟨r(1), r(2), . . . r(nq)⟩_ under the Plackett-Luce model (Plackett, 1975; Luce, 1959) is the following product of softmax distributions  
このスコアベクトルに基づいて、Plackett-Luce モデル (Plackett, 1975; Luce, 1959) の下で、ランキング $r = (r(1), r(2), \ldots, r(n_q))$ の確率 $\pi_{\theta}(r|q)$ は 以下のソフトマックス分布になります:

$$
\piθ(r|q) = \frac{exp(hθ(x[q]r(i)[))}{\sum_{i=1}^{nq} exp(hθ(x[q]r(i)[))} 

\pi_{\theta}(r|q) = \prod_{i=1}^{n_q} \frac{\exp(h_{\theta}(x^q_{r(i)}))}{\sum_{j=i}^{n_q} \exp(h_{\theta}(x^q_{r(j)}))}
\tag{5}
$$  

Note that this probability of a ranking can be computed efficiently, and that the derivative of $\pi_{\theta}(r|q)$ and $\log \pi_{\theta}(r|q)$ exists whenever the scoring model $h_{\theta}$ is differentiable. 
このランキングの確率は効率的に計算でき、スコアリングモデル $h_{\theta}$ が微分可能である限り、$\pi_{\theta}(r|q)$ および $\log \pi_{\theta}(r|q)$ の導関数が存在することに注意してください。 
Sampling a ranking under the Plackett-Luce model is efficient as well. 
Plackett-Luce モデルの下でランキングをサンプリングすることも効率的です。 
To sample a ranking, starting from the top, documents are drawn recursively from the probability distribution resulting from Softmax over the scores of the remaining documents in the candidate set, until the set is empty. 
ランキングをサンプリングするには、最初に上から始めて、候補セット内の残りのドキュメントのスコアに対するソフトマックスから得られる確率分布からドキュメントを再帰的に引き出し、セットが空になるまで続けます。(うんうん、これぞプラケットルースモデルだ...!!:thinking:)

<!-- ここまで読んだ! -->

### 3.2 Policy-Gradient Training Algorithm** ポリシー勾配トレーニングアルゴリズム

The next step is to search this policy space Π for a model that maximizes the objective in Equation (1). 
次のステップは、このポリシースペース $\Pi$ を検索して、式 (1) の目的を最大化するモデルを見つけることです。 
This section proposes a policy-gradient approach (Williams, 1992; Sutton, 1998), where we use stochastic gradient descent (SGD) updates to iteratively improve our ranking policy. 
このセクションでは、ポリシー勾配アプローチ (Williams, 1992; Sutton, 1998) を提案し、確率的勾配降下法 (SGD) アップデートを使用してランキングポリシーを反復的に改善します。 
However, since both U and D are expectations over rankings sampled from π, computing the gradient brute-force is intractable. 
ただし、$U$ と $D$ の両方が $\pi$ からサンプリングされたランキングの期待値であるため、勾配を強引に計算することは困難です。 
In this section, we derive the required gradients over expectations as an expectation over gradients. 
このセクションでは、期待値に対する必要な勾配を勾配に対する期待値として導出します(=これって期待値の式変形かな...!!:thinking:).
We then estimate this expectation as an average over a finite sample of rankings from the policy to get an approximate gradient. 
次に、**この期待値をポリシーからの有限サンプルのランキングの平均として推定し、近似勾配**を得ます。(はいはい、方策勾配の推定値を使って学習するんだよね...!!ここだと経験平均に基づくAVG推定量なのかな...??:thinking:)
Conventional LTR methods that maximize user utility are either designed to optimize over a smoothed version of a specific utility metric, such as SVMRank (Joachims et al., 2009), RankNet (Burges et al., 2005) etc., or use heuristics to optimize over probabilistic formulations of rankings (e.g. SoftRank (Taylor et al., 2008)). 
ユーザのユーティリティを最大化する従来の LTR メソッドは、SVMRank (Joachims et al., 2009)、RankNet (Burges et al., 2005) などの特定のユーティリティメトリックの平滑化バージョンを最適化するように設計されているか、ランキングの確率的定式化を最適化するためにヒューリスティックを使用します (例: SoftRank (Taylor et al., 2008))。 
Our LTR setup is similar to ListNet (Cao et al., 2007), however, instead of using a heuristic loss function for utility, we present a policy gradient method to directly optimize over both utility and disparity measures.
私たちの LTR セットアップは ListNet (Cao et al., 2007) に似ていますが、ユーティリティのためのヒューリスティック損失関数を使用する代わりに、**ユーティリティと格差の両方の指標を直接最適化するためのポリシー勾配法**を提示します。
Directly optimizing the ranking policy via policy-gradient learning has two advantages over most conventional LTR algorithms, which optimize upper bounds or heuristic proxy measures. 
**ポリシー勾配学習を介してランキングポリシーを直接最適化すること**には、上限やヒューリスティックプロキシ測定値を最適化するほとんどの従来の LTR アルゴリズムに対して**2つの利点**があります。

- First, our learning algorithm directly optimizes a specified user utility metric and has no restrictions in the choice of the information retrieval (IR) metric. 
    第一に、私たちの学習アルゴリズムは指定されたユーザユーティリティメトリックを直接最適化し、情報検索 (IR) メトリックの選択に制限がありません。

- Second, we can use the same policy-gradient approach on our disparity measure D as well, since it is also an expectation over rankings. 
第二に、格差測定 D に対しても同じポリシー勾配アプローチを使用できます。これは、ランキングに関する期待値でもあるからです。

Overall, the use of policy-gradient optimization in the space of stochastic ranking policies elegantly handles the non-smoothness inherent in rankings.
全体として、確率的ランキングポリシーの空間におけるポリシー勾配最適化の使用は、ランキングに固有の非滑らかさを優雅に処理します。

<!-- ここまで読んだ! -->

#### 3.2.1 PG-Rank: Maximizing User Utility ユーザユーティリティの最大化

The user utility of a policy πθ for a query q is defined as U (π|q) = Er∼πθ(r|q)∆�r, rel[q][�].
クエリ $q$ に対するポリシー $\pi_{\theta}$ のユーザユーティリティは $U(\pi_{\theta}|q) = E_{r \sim \pi_{\theta}(r|q)} [\Delta(r, rel[q])]$ と定義されます。
Note that taking the gradient w.r.t. θ over this expectation is not straightforward, since the space of rankings is exponential in cardinality. 
この期待値に対して $\theta$ に関する勾配を取ることは簡単ではありません。なぜなら、ランキングの空間は基数に対して指数的だからです。 
To overcome this, we use sampling via the log-derivative trick pioneered in the REINFORCE algorithm (Williams, 1992) as follows: 
これを克服するために、REINFORCE アルゴリズム (Williams, 1992) で先駆けられた**ログ導関数トリック**を使用してサンプリングします。次のようになります。
(なんかlogを追加するように式変形するよ、ってやつか...!:thinking:)

$$
\nabla_{\theta} U(\pi_{\theta}|q) = \nabla_{\theta} E_{r \sim \pi_{\theta}(r|q)} [\Delta(r, rel[q])] = E_{r \sim \pi_{\theta}(r|q)} [\nabla_{\theta} \log \pi_{\theta}(r|q) \Delta(r, rel[q])]
$$

This transformation exploits that the gradient of the expected value of the metric ∆ over rankings sampled from π can be expressed as the expectation of the gradient of the log probability of each sampled ranking multiplied by the metric value of that ranking. 
この変換は、$\pi$ からサンプリングされたランキングに対するメトリック $\Delta$ の期待値の勾配が、サンプリングされた各ランキングの対数確率の勾配とそのランキングのメトリック値の積の期待値として表現できることを利用しています。(ここは、特に何かしらの仮定を置いてるとかではなくて、確か普通に式変形してるはず...!:thinking:)
The final expectation is approximated via Monte-Carlo sampling from the Plackett-Luce model in Eq. (5).
**最終的な期待値は、式 (5) の Plackett-Luce モデルからのモンテカルロサンプリングを介して近似**されます。

Note that this policy-gradient approach to LTR, which we call PG-Rank, is novel in itself and beyond fairness. 
このポリシー勾配アプローチは、私たちが PG-Rank と呼ぶ LTR に対して新しいものであり、公平性を超えています。 
It can be used as a standalone LTR algorithm for virtually any choice of utility metric ∆, including NDCG, DCG, ERR, and Average-Rank. 
これは、NDCG、DCG、ERR、Average-Rank を含む、ほぼすべてのユーティリティメトリック $\Delta$ の選択に対してスタンドアロンの LTR アルゴリズムとして使用できます。 
Furthermore, PG-Rank also supports non-linear metrics, IPS-weighted metrics for partial information feedback (Joachims et al., 2017), and listwise metrics that do not decompose as a sum over individual documents (Zhai et al., 2003). 
さらに、PG-Rank は非線形メトリック、部分情報フィードバックのための IPS 加重メトリック (Joachims et al., 2017)、および個々のドキュメントの合計として分解されないリストワイズメトリック (Zhai et al., 2003) もサポートしています。 

<!-- ここまで読んだ! -->

#### Using baseline for variance reduction. **分散削減のためのベースラインの使用。**

(DR推定量的な考え方っぽい...! ベースラインの計算はラフだけど:thinking:)

Since making stochastic gradient descent updates with this gradient estimate is prone to high variance, we subtract a baseline term from the reward (Williams, 1992) to act as a control variate for variance reduction. 
この勾配推定を使用して確率的勾配降下法の更新を行うと、高い分散が生じやすいため、報酬からベースライン項を引き算します (Williams, 1992)。これにより、分散削減のための制御変数として機能します。 
Specifically, in the gradient estimate in Eq. (6), we replace ∆(r, rel[q]) with ∆(r, rel[q]) − _b(q) where b(q) is the average ∆_ for the current query. 
具体的には、式 (6) の勾配推定において、$\Delta(r, rel[q])$ を $\Delta(r, rel[q]) - b(q)$ に置き換えます。ここで、$b(q)$ は現在のクエリの $\Delta$ の平均値です(経験平均??:thinking:)。

<!-- ここまで読んだ! -->

#### Entropy Regularization  エントロピー正則化

While optimizing over stochastic policies, entropy regularization is used as a method for encouraging exploration as to avoid convergence to suboptimal deterministic policies (Mnih et al., 2016; Williams and Peng, 1991). 
エントロピー正則化は、確率的ポリシーを最適化する際に、最適でない決定論的ポリシーへの収束を避けるための探索を促す手法として使用されます (Mnih et al., 2016; Williams and Peng, 1991)。 
For our algorithm, we add the entropy of the probability distribution Softmax(hθ(x[q])) times a regularization coefficient γ to the objective. 
私たちのアルゴリズムでは、$\gamma$ を正則化係数として、目的関数に確率分布 $\text{Softmax}(h_{\theta}(x[q]))$ のエントロピーを追加します。

<!-- ここまで読んだ! -->

#### 3.2.2 Minimizing disparity 格差の最小化

When a fairness-of-exposure term D is included in the training objective, we also need to compute the gradient of this term. 
露出の公平性項 $D$ がトレーニング目的に含まれる場合、この項の勾配も計算する必要があります。
Fortunately, it has a structure similar to the utility term, so that the same Monte-Carlo approach applies. 
幸いなことに、これはユーティリティ項と似た構造を持っているため、同じモンテカルロアプローチが適用されます。 
Specifically, for the individual-fairness disparity measure in Equation (3), the gradient can be computed as:  
具体的には、式 (3) のindividual-fairness disparity measure(個別公平性格差指標??)に対して、勾配は次のように計算できます。  

$$
\nabla_{\theta} D_{ind} = \sum_{(i,j) \in H_1} v_r(d_i) - v_r(d_j) \times E_{r \sim \pi_{\theta}(r|q)} [v_r(d_i) - v_r(d_j) \nabla_{\theta} \log \pi_{\theta}(r|q)]

\\
(H = {(i, j) s.t. Mi ≥ _Mj})
$$
  
For the group-fairness disparity measure defined in Equation (4), the gradient can be derived as follows:
式 (4) で定義されたグループ公平性格差測定に対して、勾配は次のように導出できます。  

$$
\nabla_{\theta} D_{group}(\pi|G_0, G_1, q) = \nabla_{\theta} \max(0, \xi_q \text{diff}(\pi|q)) = 1_{\xi_q \text{diff}(\pi|q) > 0} \xi_q \nabla_{\theta} \text{diff}(\pi|q)
$$  

where diff(π|q) = ∑_{d∈G0} vMπ(G0) - vMπ(G1) , and ξq = sign(MG0 - MG1).  
ここで、$diff(\pi|q) = \sum_{d \in G_0} v_{\pi}(d) - \sum_{d \in G_1} v_{\pi}(d)$ (言い換えると、グループ $G_0$ の平均露出からグループ $G_1$ の平均露出を引いたもの) です。また、$\xi_q = \text{sign}(M_{G_0} - M_{G_1})$ はグループ $G_0$ のメリットがグループ $G_1$ のメリットより大きいかどうかを示す符号関数です。

$$
\nabla_{\theta} \text{diff}(\pi|q) = E_{r \sim \pi_{\theta}} \left[ \sum_{d \in G_0} v_r(d) - \sum_{d \in G_1} v_r(d) \nabla_{\theta} \log \pi_{\theta}(r|q) \right]
$$  

The derivation of the gradients is shown in the supplementary material. 
方策勾配の導出は補足資料に示されています。 
The expectation of the gradient in both the cases can be estimated as an average over a Monte Carlo sample of rankings from the distribution. 
両方のケースにおける勾配の期待値は、**分布からのランキングのモンテカルロサンプルの平均として推定**できます。(そうか、ここは解析的な推定量じゃなくても、モンテカルロサンプリングで近似値を得るのか...!:thinking:)
The size of the sample is denoted by S in the rest of the paper. 
サンプルのサイズは、論文の残りの部分で $S$ と表記されます。 
The completes all necessary ingredients for SGD training of objective (1), and all steps of the Fair-PG-Rank algorithm are summarized in the supplementary material. 
これにより、目的 (1) の SGD トレーニングに必要なすべての要素が揃い、Fair-PG-Rank アルゴリズムのすべてのステップが補足資料に要約されています。 

<!-- ここまで読んだ! よくわからん!-->

## 4. Empirical Evaluation 実証評価

We conduct experiments on simulated and real-world datasets to empirically evaluate our approach.  
私たちは、シミュレーションデータセットと実世界のデータセットで実験を行い、私たちのアプローチを実証的に評価します。
First, we validate that the policy-gradient algorithm is competitive with conventional LTR approaches independent of fairness considerations.  
まず、ポリシー勾配アルゴリズムが公平性の考慮に依存せず、**従来のLTRアプローチと競争力があることを検証**します。
Second, we use simulated data to verify that Fair-PG-Rank can detect and mitigate unfair features.  
次に、シミュレーションデータを使用して、Fair-PG-Rankが不公平な特徴を検出し、軽減できることを確認します。
Third, we evaluate real-world applicability on the Yahoo! Learning to Rank dataset and the German Credit Dataset (Dheeru and Karra Taniskidou, 2017) for individual fairness and group fairness respectively.  
第三に、個別の公平性とグループの公平性について、Yahoo! Learning to RankデータセットとGerman Credit Dataset（DheeruとKarra Taniskidou、2017）で実世界の適用性を評価します。
For all the experiments, we use NDCG as the utility metric, define merit using the identity function M (rel) = rel, and set the position bias v to follow the same distribution as the gain factor in DCG i.e. $v_j \propto \log_2(1+1_j)$ [where $j = 1, 2, 3, \ldots$ is a] position in the ranking.  
すべての実験で、NDCGをユーティリティメトリックとして使用し、$M(rel) = rel$ を使用してメリットを定義し、位置バイアス $v$ をDCGのゲイン係数と同じ分布に従うように設定します。すなわち、$v_j \propto \log_2(1+1_j)$ [ここで $j = 1, 2, 3, \ldots$ はランキングの位置]です。

<!-- ここまで読んだ! -->

### 4.1 Can PG-Rank learn accurate ranking policies?** PG-Rankは正確なランキングポリシーを学習できるか？**

To validate that PG-Rank is indeed a highly effective LTR method, we conduct experiments on the Yahoo dataset (Chapelle and Chang, 2011).  
PG-Rankが実際に非常に効果的なLTR手法であることを検証するために、Yahooデータセット（ChapelleとChang、2011）で実験を行います。

We use the standard experiment setup on the SET 1 dataset and optimize NDCG using PG-Rank, which is equivalent to finding the optimal policy in Eq. (1) with $\lambda = 0$.  
SET 1データセットで標準的な実験設定を使用し、PG-Rankを使用してNDCGを最適化します。これは、$\lambda = 0$のときに式(1)で最適ポリシーを見つけることに相当します。
We train Fair-PG-Rank for two kinds of scoring models: a linear model and a neural network (one hidden layer with 32 hidden units and ReLU activation).  
私たちは、線形モデルとニューラルネットワーク（隠れユニット32の隠れ層1つとReLU活性化）という2種類のスコアリングモデルのためにFair-PG-Rankを訓練します。
Details of the models and training hyperparameters are given in the supplementary material.  
モデルとトレーニングハイパーパラメータの詳細は、補足資料に記載されています。
The policy learned by our method is a stochastic policy, however, for the purpose of evaluation in this task, we use the highest probability ranking of the candidate set for each query to compute the average NDCG@10 and ERR (Expected Reciprocal Rank) over all the test set queries.  
私たちの方法で学習されたポリシーは確率的ポリシーですが、このタスクの評価の目的のために、各クエリの候補セットの最高確率ランキングを使用して、すべてのテストセットクエリに対する平均NDCG@10とERR（期待逆順位）を計算します。
We compare our evaluation scores with two baselines from Chapelle and Chang (2011) – a linear RankSVM (Joachims, 2006) and a non-linear regression-based ranker that uses Gradient-boosted Decision Trees (GBDT) (Ye et al., 2009).  
私たちは、ChapelleとChang（2011）からの2つのベースライン、すなわち線形RankSVM（Joachims、2006）と、勾配ブースト決定木（GBDT）（Ye et al.、2009）を使用する非線形回帰ベースのランカーと評価スコアを比較します。

Table 1 shows that PG-Rank achieves competitive performance compared to the conventional LTR methods.  
表1は、PG-Rankが従来のLTR手法と比較して競争力のあるパフォーマンスを達成していることを示しています。
When comparing PG-Rank to RankSVM for linear models, our method outperforms RankSVM in terms of both NDCG@10 and ERR.  
線形モデルに対してPG-RankとRankSVMを比較すると、私たちの方法はNDCG@10とERRの両方の点でRankSVMを上回ります。
This verifies that the policy-gradient approach is effective at optimizing utility without having to rely on a possibly lose convex upper bound like RankSVM.  
これは、ポリシー勾配アプローチがRankSVMのような緩い凸上限に依存せずにユーティリティを最適化するのに効果的であることを確認します。
PG-Rank with the non-linear neural network model further improves on the linear model.  
非線形ニューラルネットワークモデルを使用したPG-Rankは、線形モデルをさらに改善します。
Furthermore, additional parameter tuning and variance-control techniques from policy optimization are likely to further boost the performance of PG-Rank, but are outside the scope of this paper.  
さらに、ポリシー最適化からの追加のパラメータ調整と分散制御技術は、PG-Rankのパフォーマンスをさらに向上させる可能性がありますが、これは本論文の範囲外です。

<!-- ここまで読んだ! -->

### 4.2 Can Fair-PG-Rank effectively trade-off between utility and fairness?** Fair-PG-Rankはユーティリティと公平性の間で効果的にトレードオフできるか？**

We designed a synthetic dataset to allow inspection into how Fair-PG-Rank trades-off between user utility and fairness of exposure.  
私たちは、Fair-PG-Rankがユーザのユーティリティと露出の公平性の間でどのようにトレードオフするかを検査できるように、合成データセットを設計しました。
The dataset contains 100 queries with 10 candidate documents each.  
データセットには、各10の候補文書を持つ100のクエリが含まれています。
In expectation, 8 of those documents belong to the majority group G0 and 2 belong to the minority group G1.  
期待値として、これらの文書の8つは多数派グループG0に属し、2つは少数派グループG1に属します。
For each document we independently and uniformly draw two values $x_1$ and $x_2$ from the interval (0, 3), and set the relevance of the document to $x_1 + x_2$ clipped between 0 and 5.  
各文書について、独立して均等に区間(0, 3)から2つの値$x_1$と$x_2$を引き出し、文書の関連性を$0$と$5$の間にクリップされた$x_1 + x_2$に設定します。
For the documents from the majority group G0, the features vector $(x_1, x_2)$ representing the documents provides perfect information about relevance.  
多数派グループG0の文書については、文書を表す特徴ベクトル$(x_1, x_2)$が関連性に関する完全な情報を提供します。
For documents in the minority group G1, however, feature $x_2$ is corrupted by replacing it with zero so that the information about relevance for documents in G1 only comes from $x_1$.  
しかし、少数派グループG1の文書については、特徴$x_2$がゼロに置き換えられることによって破損し、G1の文書に関する関連性の情報は$x_1$からのみ得られます。
This leads to a biased representation between groups, and any use of $x_2$ is prone to producing unfair exposure between groups.  
これにより、グループ間での偏った表現が生じ、$x_2$の使用はグループ間で不公平な露出を生じる可能性があります。

In order to validate that Fair-PG-Rank can detect and neutralize this biased feature, we consider a linear scoring model $h_\theta(x) = \theta_1 x_1 + \theta_2 x_2$ with parameters $\theta = (\theta_1, \theta_2)$.  
Fair-PG-Rankがこの偏った特徴を検出し、中和できることを検証するために、パラメータ$\theta = (\theta_1, \theta_2)$を持つ線形スコアリングモデル$h_\theta(x) = \theta_1 x_1 + \theta_2 x_2$を考えます。
Figure 1 shows the contour plots of NDCG and $D_{group}$ evaluated for different values of $\theta$.  
図1は、異なる$\theta$の値に対して評価されたNDCGと$D_{group}$の等高線プロットを示しています。
Note that not only the direction of the $\theta$ vector affects both NDCG and $D_{group}$, but also its length as it determines the amount of stochasticity in $\pi_\theta$.  
$\theta$ベクトルの方向がNDCGと$D_{group}$の両方に影響を与えるだけでなく、その長さも$\pi_\theta$の確率的要素の量を決定することに注意してください。
The true relevance model lies on the $\theta_1 = \theta_2$ line (dotted), however, a fair model is expected to ignore the biased feature $x_2$.  
真の関連性モデルは$\theta_1 = \theta_2$の線（点線）上にありますが、公平なモデルは偏った特徴$x_2$を無視することが期待されます。
We use PG-Rank to train this linear model to maximize NDCG and minimize $D_{group}$.  
私たちは、NDCGを最大化し、$D_{group}$を最小化するためにこの線形モデルを訓練するためにPG-Rankを使用します。
The dots in Figure 1 denote the models learned by Fair-PG-Rank for different values of $\lambda$.  
図1の点は、異なる$\lambda$の値に対してFair-PG-Rankによって学習されたモデルを示しています。
For small values of $\lambda$, Fair-PG-Rank puts more emphasis on NDCG and thus learns parameter vectors along the $\theta_1 = \theta_2$ direction.  
小さな$\lambda$の値では、Fair-PG-RankはNDCGにより重点を置き、そのため$\theta_1 = \theta_2$の方向に沿ったパラメータベクトルを学習します。
As we increase emphasis on group fairness disparity $D_{group}$ by increasing $\lambda$, the policies learned by Fair-PG-Rank become more stochastic and it correctly starts to discount the biased attribute by learning models where increasingly $\theta_1 >> \theta_2$.  
グループの公平性の不均衡$D_{group}$に対する重点を$\lambda$を増加させることで高めると、Fair-PG-Rankによって学習されたポリシーはより確率的になり、$\theta_1 >> \theta_2$のモデルを学習することで偏った属性を正しく割り引き始めます。

In Figure 1(c), we compare Fair-PG-Rank with two baselines.  
図1(c)では、Fair-PG-Rankを2つのベースラインと比較します。
As the first baseline, we estimate relevances with a fairness-oblivious linear regression and then use the post-processing method from (Singh and Joachims, 2018) on the estimates.  
最初のベースラインとして、公平性を無視した線形回帰で関連性を推定し、その後、推定値に(SinghとJoachims、2018)の後処理手法を使用します。
Unlike Fair-PG-Rank, which reduces disparity with increasing $\lambda$, the post-processing method is misled by the estimated relevances that use the biased feature $x_2$, and the ranking policies become even less fair as $\lambda$ is increased.  
$\lambda$を増加させることで不均衡を減少させるFair-PG-Rankとは異なり、後処理手法は偏った特徴$x_2$を使用した推定関連性に誤導され、ランキングポリシーは$\lambda$が増加するにつれてさらに不公平になります。
As the second baseline, we apply the method of Zehlike and Castillo (2018), but the heuristic measure it optimizes shows little effect on disparity.  
第二のベースラインとして、ZehlikeとCastillo（2018）の手法を適用しますが、最適化するヒューリスティックな測定は不均衡に対してほとんど効果を示しません。

**4.3 Can Fair-PG-Rank learn fair ranking policies on real-world data?**  
**4.3 Fair-PG-Rankは実世界のデータで公平なランキングポリシーを学習できるか？**

In order to study Fair-PG-Rank on real-world data, we conducted two sets of experiments.  
実世界のデータにおけるFair-PG-Rankを研究するために、私たちは2つの実験を行いました。

For Individual Fairness, we train Fair-PG-Rank with a linear and a neural network model on the Yahoo! Learning to rank challenge dataset, optimizing Equation 1 with different values of $\lambda$.  
個別の公平性のために、Yahoo! Learning to rankチャレンジデータセットで線形モデルとニューラルネットワークモデルを使用してFair-PG-Rankを訓練し、異なる$\lambda$の値で式1を最適化します。
The details about the model and training hyperparameters are present in the supplementary material.  
モデルとトレーニングハイパーパラメータの詳細は、補足資料に記載されています。
For both the models, Figure 2 shows the average NDCG@10 and $D_{ind}$ (individual disparity) over the test and training (dotted line) datasets for different values of $\lambda$ parameter.  
両方のモデルについて、図2は異なる$\lambda$パラメータの値に対するテストおよびトレーニング（点線）データセット全体の平均NDCG@10と$D_{ind}$（個別の不均衡）を示しています。
As desired, Fair-PG-Rank emphasizes lower disparity over higher NDCG as the value of $\lambda$ increases, with disparity going down to zero eventually.  
期待通り、Fair-PG-Rankは$\lambda$の値が増加するにつれて高いNDCGよりも低い不均衡を強調し、不均衡は最終的にゼロにまで下がります。
Furthermore, the training and test curves for both NDCG and disparity overlap indicating the learning method generalizes to unseen queries.  
さらに、NDCGと不均衡の両方のトレーニングとテストの曲線が重なり、学習方法が未見のクエリに一般化することを示しています。
This is expected since both training quantities concentrate around their expectation as the training set size increases.  
これは、トレーニングセットのサイズが増加するにつれて、両方のトレーニング量がその期待値の周りに集中するため、予想されることです。

For Group fairness, we adapt the German Credit Dataset from the UCI repository (Dheeru and Karra Taniskidou, 2017) to a learning-to-rank task (described in the supplementary), choosing gender as the group attribute.  
グループの公平性のために、UCIリポジトリからGerman Credit Dataset（DheeruとKarra Taniskidou、2017）を学習ランキングタスクに適応させ（補足に記載）、性別をグループ属性として選択します。
We train Fair-PG-Rank using a linear model, for different values of $\lambda$.  
異なる$\lambda$の値に対して線形モデルを使用してFair-PG-Rankを訓練します。
Figure 3 shows that Fair-PG-Rank is again able to effectively trade-off NDCG and fairness.  
図3は、Fair-PG-Rankが再びNDCGと公平性の間で効果的にトレードオフできることを示しています。
Here we also plot the standard deviation to illustrate that the algorithm reliably converges to solutions of similar performance over multiple runs.  
ここでは、標準偏差もプロットして、アルゴリズムが複数回の実行で同様のパフォーマンスの解に確実に収束することを示しています。
Similar to the synthetic example, Figure 3 (right) again shows that Fair-PG-Rank can effectively trade-off NDCG for $D_{group}$, while the baselines fail.  
合成例と同様に、図3（右）は再びFair-PG-Rankが$D_{group}$に対してNDCGを効果的にトレードオフできることを示しており、ベースラインは失敗しています。



### 5. Conclusion 結論

We presented a framework for learning ranking functions that not only maximize utility to their users, but that also obey application specific fairness constraints on how exposure is allocated to the ranked items based on their merit. 
私たちは、ユーザに対する効用を最大化するだけでなく、ランク付けされたアイテムに対する露出の配分がその価値に基づく特定のアプリケーションの公平性制約を遵守するランキング関数を学習するためのフレームワークを提示しました。
Based on this framework, we derived the Fair-PG-Rank policy-gradient algorithm that directly optimizes both utility and fairness without having to resort to upper bounds or heuristic surrogate measures. 
このフレームワークに基づいて、私たちは、上限やヒューリスティックな代理測定に頼ることなく、効用と公平性の両方を直接最適化するFair-PG-Rankポリシー勾配アルゴリズムを導出しました。
We demonstrated that our policy-gradient approach is effective for training high-quality ranking functions, that Fair-PG-Rank can identify and neutralize biased features, and that it can effectively learn ranking functions under both individual fairness and group fairness constraints. 
私たちは、**ポリシー勾配アプローチが高品質なランキング関数のトレーニングに効果的**であり、Fair-PG-Rankがバイアスのある特徴を特定し中和できること、さらに個別の公平性と集団の公平性の制約の下でランキング関数を効果的に学習できることを示しました。

<!-- ここまで読んだ! -->

### Appendix A. Policy Gradient for PL Ranking policy  
### 付録A. PLランキングポリシーのためのポリシー勾配  
In this section, we will show the derivation of gradients for utility U and disparity (Dgroup and _Dind).  
このセクションでは、ユーティリティUと不均等（Dgroupおよび_Dind）の勾配の導出を示します。  
Since both U and D are expectations over rankings sampled from π, computing the gradient_ brute-force is intractable.  
UとDの両方がπからサンプリングされたランキングの期待値であるため、勾配をブートフォースで計算することは困難です。  
We derive the required gradients over expectations as an expectation over gradients.  
必要な勾配を期待値の勾配として導出します。  
We then estimate this expectation as an average over a finite sample of rankings from the policy to get an approximate gradient.  
次に、この期待値をポリシーからの有限サンプルのランキングの平均として推定し、近似勾配を得ます。  
Later, we also present a summary of the Fair-PG-Rank algorithm.  
後で、Fair-PG-Rankアルゴリズムの概要も示します。  

**A.1 Gradient of Utility measures**  
**A.1 ユーティリティ測定の勾配**  
To overcome taking a gradient over expectations, we use the log-derivative trick pioneered in the REINFORCE algorithm (Williams, 1992) as follows  
期待値に対する勾配を取ることを克服するために、REINFORCEアルゴリズム（ウィリアムズ、1992年）で先駆けた対数微分トリックを次のように使用します。  

$$
∇θU(πθ|q) = ∇θEr∼πθ(r|q)∆r, rel[q]
= ∇θ ∑_{r∈σ(nq)} πθ(r|q)∆r, rel[q]
= ∑_{r∈σ(nq)} ∇θ[πθ(r|q)]∆r, rel[q]
$$  

$$
= ∑_{r∈σ(nq)} πθ(r|q)∇θ[log πθ(r|q)]∆r, rel[q] \text{ (Log-derivative trick (Williams, 1992))}
$$  

$$
= Er∼πθ(r|q)[∇θlog πθ(r|q)∆(r, rel[q])]
$$  

The expectation over $r ∼ πθ(r|q)$ can be computed as an average over a finite sample of rankings from the policy.  
$r ∼ πθ(r|q)$の期待値は、ポリシーからの有限サンプルのランキングの平均として計算できます。  

**A.2 Gradient of Disparity functions**  
**A.2 不均等関数の勾配**  
The gradient of the disparity measure for individual fairness can be derived as follows:  
個々の公正性のための不均等測定の勾配は次のように導出できます：  

$$
∇θDind = ∇θ \sum_{H} \frac{1}{|H|} \max(0, [v(π)(d[i]) - v(π)(d[j])])_{(i,j)∈H}
$$  

$$
= \frac{1}{|H|} \sum_{(i,j)∈H} \max(0, pdiffq(π, i, j)) ∇θpdiffq(π, i, j)
$$  

$$
= Er∼πθ(r|q) \left[ ∇θ \left( v_r(d[i]) - v_r(d[j]) \right) \right] \text{ (using the log-derivative trick)}
$$  

The gradient of the disparity measure for group fairness can be derived as follows:  
グループ公正性のための不均等測定の勾配は次のように導出できます：  

$$
∇θDgroup(π|G0, G1, q) = ∇θ \max(0, ξqdiff(π|q))
$$  

where $diff(π|q) = vM(π|G0) - vM(π|G1)$, and $ξq = +1$ if $MG0 ≥ MG1$, $−1$ otherwise.  
ここで、$diff(π|q) = vM(π|G0) - vM(π|G1)$、および$ξq = +1$は$MG0 ≥ MG1$の場合、そうでなければ$−1$です。  
Further,  
さらに、  

$$
∇θDgroup(π|G0, G1, q) = \frac{1}{ξq} \text{ if } diff(π|q) > 0 \Rightarrow ξq∇θdiff(π|q)
$$  

$$
∇θdiff(π|q) = ∇θ \left( -v(π)(G1) \right) \text{ (using the log-derivative trick)}
$$  

Similarly, the expectation over $r ∼ πθ(r|q)$ can be computed as an average over a finite sample of rankings from the policy.  
同様に、$r ∼ πθ(r|q)$の期待値は、ポリシーからの有限サンプルのランキングの平均として計算できます。  

**A.3 Summary of the Fair-PG-Rank algorithm**  
**A.3 Fair-PG-Rankアルゴリズムの概要**  
Algorithm 1 summarizes our method for learning fair ranking policies given a training dataset.  
アルゴリズム1は、トレーニングデータセットを考慮した公正なランキングポリシーを学習するための私たちの方法を要約しています。  

**Algorithm 1 Fair-PG-Rank**  
**アルゴリズム1 Fair-PG-Rank**  

**Input: T = {(x[q], rel[q])}i[N]=1[, disparity measure][ D][, utility/fairness trade-off][ λ]**  
**入力：T = {(x[q], rel[q])}i[N]=1[, 不均等測定][ D][, ユーティリティ/公正性のトレードオフ][ λ]**  
Parameters: model hθ, learning rate η, entropy reg γ  
パラメータ：モデルhθ、学習率η、エントロピー正則化γ  
Initialize hθ with parameters θ0  
パラメータθ0でhθを初期化  

**repeat**  
**繰り返す**  
$q = (x[q], rel[q]) ∼T \{Draw a query from training set\}$  
$q = (x[q], rel[q]) ∼T \{トレーニングセットからクエリを引く\}$  
$hθ(x[q]) = (hθ(x[q][1]), hθ(x[q][2]), \ldots, hθ(x[n][q]))$  
$hθ(x[q]) = (hθ(x[q][1]), hθ(x[q][2]), \ldots, hθ(x[n][q]))$  
{Obtain scores for each document}  
{各ドキュメントのスコアを取得}  

**for i = 1 to S do**  
**i = 1からSまでのループ**  
$ri ∼ πθ(r|q) \{Plackett-Luce sampling\}$  
$ri ∼ πθ(r|q) \{プラケット・ルースサンプリング\}$  
**end for**  
**ループ終了**  
$∇← ∇[ˆ]θU - λ∇[ˆ]θD \{Compute gradient as an average over all ri using § A.1 and § A.2\}$  
$∇← ∇[ˆ]θU - λ∇[ˆ]θD \{§ A.1および§ A.2を使用してすべての$ri$の平均として勾配を計算\}$  
$θ ← θ + η∇ \{Update\}$  
$θ ← θ + η∇ \{更新\}$  

**until convergence on the validation set**  
**検証セットでの収束まで繰り返す**  

### Appendix B. Datasets and Models  
### 付録B. データセットとモデル  
**B.1 Yahoo! Learning to Rank dataset**  
**B.1 Yahoo! ラーニング・トゥ・ランクデータセット**  
We used Set 1 from the Yahoo! Learning to Rank challenge (Chapelle and Chang, 2011), which consists of 19, 944 training queries and 6, 983 queries in the test set.  
私たちは、Yahoo! ラーニング・トゥ・ランクチャレンジ（シャペルとチャン、2011年）のセット1を使用しました。これは、19,944のトレーニングクエリと6,983のテストセットのクエリで構成されています。  
Each query has a variable sized candidate set of documents that needs to be ranked.  
各クエリには、ランキングが必要な可変サイズの候補ドキュメントセットがあります。  
There are a total of 473, 134 and 165, 660 documents in training and test set respectively.  
トレーニングセットには473,134件、テストセットには165,660件のドキュメントがあります。  
The query-document pairs are represented by a 700-dimensional feature vector.  
クエリ-ドキュメントペアは700次元の特徴ベクトルで表されます。  
For supervision, each query-document pair is assigned an integer relevance judgments from 0 (bad) to 4 (perfect).  
監視のために、各クエリ-ドキュメントペアには、0（悪い）から4（完璧）までの整数の関連性判断が割り当てられます。  

**B.2 German Credit Dataset**  
**B.2 ドイツ信用データセット**  
The original German Credit dataset (Dheeru and Karra Taniskidou, 2017) consists of 1000 individuals, each described by a feature vector xi consisting of 20 attributes with both numerical and categorical features, as well as a label reli classifying it as creditworthy (reli = 1) or not (reli = 0).  
元のドイツ信用データセット（ディールとカラ・タニスキドゥ、2017年）は、1000人の個人で構成されており、それぞれは数値的およびカテゴリカルな特徴を持つ20の属性からなる特徴ベクトルxiで説明され、信用に値する（reli = 1）かどうかを分類するラベルreliが付与されています（reli = 0）。  
We adapt this binary classification task to a learning-to-rank task in the following way: for each query q, we sample a candidate set of 10 individuals each, randomly sampling irrelevant documents (non-creditworthy individuals) and relevant documents (creditworthy individuals) in the ratio 4:1.  
この二項分類タスクをランキング学習タスクに適応させる方法は次のとおりです：各クエリqについて、10人の個人の候補セットをサンプリングし、無関係なドキュメント（信用に値しない個人）と関連するドキュメント（信用に値する個人）を4:1の比率でランダムにサンプリングします。  
Each individual is identified as a member of group G0 or G1 based on their gender attribute.  
各個人は、その性別属性に基づいてグループG0またはG1のメンバーとして識別されます。  

**B.3 Baselines**  
**B.3 ベースライン**  
We compare our method to two methods:  
私たちの方法を2つの方法と比較します：  
1. Post-processing method on estimated relevances: First, we train a linear regression model on all the training set query-document pairs that predicts their relevances.  
1. 推定された関連性に対するポストプロセッシング法：まず、すべてのトレーニングセットのクエリ-ドキュメントペアに対して、関連性を予測する線形回帰モデルをトレーニングします。  
For each query in the test set, we use the estimated relevances of the documents as an input to the linear program from Singh and Joachims (2018) with the disparate exposure constraint for group fairness (section § 2.2).  
テストセットの各クエリに対して、ドキュメントの推定された関連性を、グループ公正性のための不均等な露出制約を持つシンとヨアヒムス（2018年）の線形プログラムへの入力として使用します（セクション§ 2.2）。  
We use the following linear program to find the optimal ranking that satisfies fairness constraints on estimated relevances:  
次の線形プログラムを使用して、推定された関連性に対する公正性制約を満たす最適なランキングを見つけます：  

$$
\text{reli} \quad P^* = \arg\max_P \sum_{u[T]} P v - λξ
$$  

$$
\text{s.t.} \quad \forall j \quad \sum_{i} P_{ij} = 1 \quad (\text{sum of probabilities for each document})  
\forall i \quad \sum_{j} P_{ij} = 1 \quad (\text{sum of probabilities at each position})  
\forall i, j \quad 0 ≤ P_{ij} ≤ 1 \quad (\text{valid probabilities})  
\sum_{d_i∈G_k} P_{i[T]} v - \sum_{d_{i}∈G_{k'}} P_{i[T]} v \geq M(G_k) - M(G_{k'}) \Rightarrow -ξ \geq 0
$$  

Note that the relevances used in the linear program (in $u$) are estimated relevances.  
線形プログラムで使用される関連性（$u$内）は推定された関連性であることに注意してください。  
This is one of the reasons that even when using this linear program to minimize disparity, we cannot guarantee that disparity on unseen queries can be reduced to zero.  
これは、この線形プログラムを使用して不均等を最小化しても、見えないクエリに対する不均等をゼロに減少させることが保証できない理由の1つです。  
In contrast to Singh and Joachims (2018), rather than solving the exact constraint, we use a $λ$ hyperparameter to control how much unfairness we can allow.  
シンとヨアヒムス（2018年）とは対照的に、正確な制約を解決するのではなく、どれだけの不公正を許可できるかを制御するために$λ$ハイパーパラメータを使用します。  
For our experiments, we evaluate the performance for values of $λ ∈ [0, 0.2]$ (at $λ = 0.2$, for all queries the disparity measure on estimated relevances was reduced to zero).  
私たちの実験では、$λ ∈ [0, 0.2]$の値に対するパフォーマンスを評価します（$λ = 0.2$の場合、すべてのクエリに対して推定された関連性の不均等測定がゼロに減少しました）。  
The linear program outputs a $nq × nq$-sized probabilistic matrix $P$ representing the probability of each document at each position.  
線形プログラムは、各位置での各ドキュメントの確率を表す$nq × nq$サイズの確率行列$P$を出力します。  
We compare the NDCG and $Dgroup$ for this probabilistic matrix to other methods in sections § 4.2 and § 4.3.  
この確率行列に対するNDCGと$Dgroup$を他の方法と比較します（セクション§ 4.2および§ 4.3）。  

2. Zehlike and Castillo (2018): This method uses a cross-entropy loss on the top-1 probability of each document to maximize utility.  
2. ゼリケとカスティリョ（2018年）：この方法は、各ドキュメントのトップ1確率に対するクロスエントロピー損失を使用してユーティリティを最大化します。  
The top-1 probabilities of each document is obtained through a Softmax over scores output by a linear scoring function.  
各ドキュメントのトップ1確率は、線形スコアリング関数によって出力されたスコアに対するソフトマックスを通じて得られます。  
The disparity measure is implemented as the squared loss of the difference between the top-1 exposure of the groups $G0$ and $G1$.  
不均等測定は、グループ$G0$と$G1$のトップ1露出の差の二乗損失として実装されます。  
Training is done using stochastic gradient descent on the sum of cross entropy and $λ$ times the disparity measure.  
トレーニングは、クロスエントロピーの合計と不均等測定の$λ$倍に対して確率的勾配降下法を使用して行われます。  
For all our experiments with this method, we didn’t use any regularization, searched for the best learning rate in the range $[10^{-3}, 1]$, and evaluated the performance for $λ ∈ \{0, 1, 10, 10^{2}, \ldots, 10^{6}\}$.  
この方法でのすべての実験では、正則化を使用せず、$[10^{-3}, 1]$の範囲で最適な学習率を検索し、$λ ∈ \{0, 1, 10, 10^{2}, \ldots, 10^{6}\}$のパフォーマンスを評価しました。  

**B.4 Model and Training: Yahoo! Learning to Rank challenge dataset**  
**B.4 モデルとトレーニング：Yahoo! ラーニング・トゥ・ランクチャレンジデータセット**  
We train two different models for experiments in Section § 4.1: a linear model, and a neural network.  
セクション§ 4.1の実験のために、2つの異なるモデルをトレーニングします：線形モデルとニューラルネットワーク。  
The neural network has one hidden layer of size 32 and ReLU activation function.  
ニューラルネットワークは、サイズ32の隠れ層とReLU活性化関数を持っています。  
For training, all the weights were randomly initialized between (−0.001, 0.001) for the linear model and (−1/32, 1/32) for the neural network.  
トレーニングのために、線形モデルのすべての重みは（−0.001、0.001）の間でランダムに初期化され、ニューラルネットワークは（−1/32、1/32）の間で初期化されます。  
We use an Adam optimizer with a learning rate of 0.001 for the linear model and $5 × 10^{-5}$ for the neural network.  
線形モデルには学習率0.001のAdamオプティマイザーを使用し、ニューラルネットワークには$5 × 10^{-5}$を使用します。  
For both the cases, we set the entropy regularization constant to $γ = 1.0$, use a baseline, and use a sample size of $S = 10$ to estimate the gradient.  
両方の場合において、エントロピー正則化定数を$γ = 1.0$に設定し、ベースラインを使用し、勾配を推定するためにサンプルサイズ$S = 10$を使用します。  
Both models are trained for 20 epochs over the training dataset, updating the model one query at a time.  
両方のモデルは、トレーニングデータセットに対して20エポックのトレーニングを行い、1回のクエリごとにモデルを更新します。  

**B.5 Model and Training: German Credit Dataset**  
**B.5 モデルとトレーニング：ドイツ信用データセット**  
To validate whether Fair-PG-Rank can also optimize for Group fairness, we used the modified German Credit Dataset from the UCI repository (section § B.2).  
Fair-PG-Rankがグループ公正性を最適化できるかどうかを検証するために、UCIリポジトリから修正されたドイツ信用データセット（セクション§ B.2）を使用しました。  
We train a linear scoring model with Adam, using a fixed learning rate of 0.001 with no regularization, and a sample size $S = 25$, for different values of $λ$ in the range $[0, 25]$.  
正則化なしで固定学習率0.001を使用してAdamで線形スコアリングモデルをトレーニングし、$λ$の異なる値に対してサンプルサイズ$S = 25$を使用します。  
We compare our method to baselines mentioned in § B.3.  
私たちの方法を§ B.3で言及されたベースラインと比較します。  
