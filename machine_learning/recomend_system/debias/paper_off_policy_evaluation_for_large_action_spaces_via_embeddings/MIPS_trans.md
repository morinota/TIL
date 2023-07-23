## link リンク

- https://arxiv.org/pdf/2202.06317.pdf https://arxiv.org/pdf/2202.06317.pdf

## title タイトル

Off-Policy Evaluation for Large Action Spaces via Embeddings
埋め込みによる大規模行動空間のオフポリシー評価

## Abstruct アブストラクト

Off-policy evaluation (OPE) in contextual bandits has seen rapid adoption in real-world systems, since it enables offline evaluation of new policies using only historic log data.
コンテクスチュアル・バンディット(i.e. 決定論的ではなく確率的な推薦アルゴリズム)におけるオフポリシー評価（OPE）は、過去のログデータのみを使用して新しいポリシーをオフラインで評価できるため、実世界のシステムで急速に採用が進んでいる。
Unfortunately, when the number of actions is large, existing OPE estimators – most of which are based on inverse propensity score weighting – degrade severely and can suffer from extreme bias and variance.
**残念なことに、行動数が多い場合、既存のOPE推定量-そのほとんどは逆傾向スコア重み付けに基づく-は著しく劣化**し、極端なバイアスと分散に悩まされることがある。
This foils the use of OPE in many applications from recommender systems to language models.
このため、推薦システムから言語モデルまで、**多くのアプリケーションでOPEを使用することができない**.
To overcome this issue, we propose a new OPE estimator that leverages marginalized importance weights when action embeddings provide structure in the action space.
この問題を克服するために、我々は、**action embeddings**がアクション空間の構造を提供する場合に、**周辺化された重要度重み**を活用する新しいOPE推定器を提案する。
We characterize the bias, variance, and mean squared error of the proposed estimator and analyze the conditions under which the action embedding provides statistical benefits over conventional estimators.
提案する推定量のバイアス、分散、平均二乗誤差を特徴付け、アクション埋め込みが従来の推定量に対して統計的な利点をもたらす条件を分析する。
In addition to the theoretical analysis, we find that the empirical performance improvement can be substantial, enabling reliable OPE even when existing estimators collapse due to a large number of actions.
理論的な分析に加え、経験的な性能の向上はかなりのものであり、多数のアクションによって既存の推定器が崩壊した場合でも、信頼性の高いOPEを可能にすることがわかった。

# Introduction はじめに

Many intelligent systems (e.g., recommender systems, voice assistants, search engines) interact with the environment through a contextual bandit process where a policy observes a context, takes an action, and obtains a reward.
**多くの知的システム（推薦システム、音声アシスタント、検索エンジンなど）は、ポリシーがコンテキストを観察し、行動を起こし、報酬を得るというコンテキスト・バンディット過程を通じて環境と相互作用する。**
Logs of these interactions provide valuable data for off-policy evaluation (OPE), which aims to accurately evaluate the performance of new policies without ever deploying them in the field.
このようなやりとりのログは、オフ・ポリシー評価（OPE）のための貴重なデータとなる。OPEは、新しいポリシーを現場に導入することなく、そのパフォーマンスを正確に評価することを目的としている。
OPE is of great practical relevance, as it helps avoid costly online A/B tests and can also act as subroutines for batch policy learning (Dud´ık et al., 2014; Su et al., 2020a).
OPEは、コストのかかるオンラインA/Bテストを回避するのに役立ち、バッチポリシー学習のサブルーチンとしても機能するため、実用的な意義が大きい（Dud´ık et al, 2014; Su et al, 2020a）。
However, OPE is challenging, since the logs contain only partial-information feedback – specifically the reward of the chosen action, but not the counterfactual rewards of all the other actions a different policy might choose.
しかし、OPEは困難である。なぜなら、ログには部分的な情報のフィードバックしか含まれていないからである。具体的には、選択された行動の報酬であるが、別の政策が選択するかもしれない他のすべての行動の反事実的報酬ではない。

When the action space is small, recent advances in the design of OPE estimators have led to a number of reliable methods with good theoretical guarantees (Dud´ık et al., 2014; Swaminathan & Joachims, 2015a; Wang et al., 2017; Farajtabar et al., 2018; Su et al., 2019; 2020a; Metelli et al., 2021).
行動空間が小さい場合、OPE推定量の設計における最近の進歩により、理論的に保証された信頼性の高い手法が数多く登場している（Dud´ık et al., 2014; Swaminathan & Joachims, 2015a; Wang et al., 2017; Farajtabar et al., 2018; Su et al., 2019; 2020a; Metelli et al., 2021）。
Unfortunately, these estimators can degrade severely when the number of available actions is large.
残念ながら、**利用可能なアクションの数が多い場合、これらの推定量は著しく低下する可能性がある**。
Large action spaces are prevalent in many potential applications of OPE, such as recommender systems where policies have to handle thousands or millions of items (e.g., movies, songs, products).
大きな行動空間は、何千、何百万ものアイテム（映画、曲、商品など）をポリシーとして扱わなければならないレコメンダーシステムなど、OPEの多くの潜在的な応用例で広まっている。
In such a situation, the existing estimators based on inverse propensity score (IPS) weighting (Horvitz & Thompson, 1952) can incur high bias and variance, and as a result, be impractical for OPE.
このような状況では、逆傾向スコア(IPS)重み付け(Horvitz & Thompson, 1952)に基づく既存の推定量では、バイアスと分散が大きくなり、結果としてOPEには実用的ではない。
First, a large action space makes it challenging for the logging policy to have common support with the target policies, and IPS is biased under support deficiency (Sachdeva et al., 2020).
第一に、**行動空間が大きいと、ロギング・ポリシーがターゲット・ポリシーと共通の支持を持つことが難しくなり**、IPSは支持不足の下でバイアスがかかる（Sachdeva et al, 2020）。
Second, a large number of actions typically leads to high variance of IPS due to large importance weights.
第二に、アクションの数が多いと、一般的に重要度の重みが大きくなるため、IPSの分散が大きくなる。
To illustrate, we find in our experiments that the variance and mean squared error of IPS inflate by a factor of over 300 when the number of actions increases from 10 to 5000 given a fixed sample size.
例を挙げると、サンプルサイズが固定されている場合、アクション数が10から5000に増加すると、IPSの分散と平均二乗誤差が300倍以上に膨れ上がることが実験でわかった。
While doubly robust (DR) estimators can somewhat reduce the variance by introducing a reward estimator as a control variate (Dud´ık et al., 2014), they do not address the fundamental issues that come with large action spaces.
二重ロバスト（DR）推定量は、報酬推定量を制御変量として導入することで、分散をいくらか減らすことができるが（Dud´ık et al.

To overcome the limitations of the existing estimators when the action space is large, we leverage additional information about the actions in the form of action embeddings.
**アクション空間が大きい場合の既存の推定器の限界を克服するために、アクション埋め込みという形でアクションに関する追加情報を活用する。**
There are many cases where we have access to such prior information.
そうした事前情報にアクセスできるケースは多い。
For example, movies are characterized by auxiliary information such as genres (e.g., adventure, science fiction, documentary), director, or actors.
例えば、映画はジャンル（例：アドベンチャー、SF、ドキュメンタリー）、監督、俳優などの補助情報によって特徴づけられる。
We should then be able to utilize these supplemental data to infer the value of actions under-explored by the logging policy, potentially achieving much more accurate policy evaluation than the existing estimators.
そして、これらの補足データを利用して、伐採政策によって十分に調査されていない行動の価値を推測することができるはずであり、既存の推定値よりもはるかに正確な政策評価を達成できる可能性がある。
We first provide the conditions under which action embeddings provide another path for unbiased OPE, even with support deficient actions.
我々はまず、**サポート不足のアクションであっても、アクション埋め込みが不偏OPEのための別の道を提供する条件**を提供する。
We then propose the Marginalized IPS (MIPS) estimator, which uses the marginal distribution of action embeddings, rather than actual actions, to define a new type of importance weights.
これは、実際の行動ではなく、行動の埋め込みのマージナル分布を利用して、新しいタイプの重要度重みを定義する。
We show that MIPS is unbiased under an alternative condition, which states that the action embeddings should mediate every causal effect of the action on the reward.
MIPSは、アクションの埋め込みが報酬に対するアクションの因果効果をすべて媒介する、という別の条件下では不偏であることを示す。
Moreover, we show that MIPS has a lower variance than IPS, especially when there is a large number of actions, and thus the vanilla importance weights have a high variance.
さらに、MIPSはIPSよりも分散が小さく、特にアクション数が多い場合、バニラ重要度重みが高い分散を持つことを示す。
We also characterize the gain in MSE provided by MIPS, which implies an interesting bias-variance trade-off with respect to the quality of the action embeddings.
また、MIPSによって得られるMSEの利得の特徴も明らかにする。これは、アクションの埋め込みの質に関して、興味深いバイアスと分散のトレードオフを意味する。
Including many embedding dimensions captures the causal effect better, leading to a smaller bias of MIPS.
多くの埋め込み次元を含めることで、因果効果をよりよく捉え、MIPSのバイアスをより小さくすることができる。
In contrast, using only a subset of the embedding dimensions reduces the variance more.
対照的に、埋め込み次元のサブセットのみを使用することで、分散はより小さくなる。
We thus propose a strategy to intentionally violate the assumption about the action embeddings by discarding less relevant embedding dimensions for achieving a better MSE at the cost of introducing some bias.
そこで我々は、多少のバイアスを導入する代償として、より良いMSEを達成するために、関連性の低い埋め込み次元を破棄することによって、アクション埋め込みに関する仮定を意図的に破る戦略を提案する。
Comprehensive experiments on synthetic and real-world bandit data verify the theoretical findings, indicating that MIPS can provide an effective bias-variance trade-off in the presence of many actions.
合成データおよび実世界のバンディットデータを用いた包括的な実験により、理論的な知見が検証され、MIPSが多くのアクションが存在する場合に効果的なバイアスと分散のトレードオフを提供できることが示された。

# Off-Policy Evaluation

We follow the general contextual bandit setup, and an extensive discussion of related work is given in Appendix A.
我々は一般的なコンテクスト・バンディットの設定に従う。関連する研究の広範な議論は付録Aに示す。
Let x ∈ X ⊆ R dx be a dx-dimensional context vector drawn i.i.d.
x∈X⊆Rのdxをi.i.d.描画されたdx次元の文脈ベクトルとする。
from an unknown distribution p(x).
未知の分布p(x)から
Given context x, a possibly stochastic policy π(a|x) chooses action a from a finite action space denoted as A.
コンテキストxが与えられたとき、確率的な政策π(a|x)は、Aとして示される有限の行動空間から行動aを選択する。
The reward r ∈ [0, rmax] is then sampled from an unknown conditional distribution p(r|x, a).
報酬r∈[0, rmax]は、未知の条件付き分布p(r|x, a)からサンプリングされる。
We measure the effectiveness of a policy π through its value
我々は、政策πの有効性をその値によって測定する。

$$
\tag{1}
$$

where q(x, a) := E[r|x, a] denotes the expected reward given context x and action a.
x, a] denotes the expected reward given context x and action a.

In OPE, we are given logged bandit data collected by a logging policy π0.
OPEでは、ロギングポリシーπ0によって収集されたロギングされたバンディットデータが与えられる。
Specifically, let D := {(xi , ai , ri)} n i=1 be a sample of logged bandit data containing n independent observations drawn from the logging policy as (x, a, r) ∼ p(x)π0(a|x)p(r|x, a).
x)p(r|x, a).
We aim to develop an estimator Vˆ for the value of a target policy π (which is different from π0) using only the logged data in D.
Dに記録されたデータのみを用いて、（π0とは異なる）目標ポリシーの値πの推定量Vˆを開発することを目指す。
The accuracy of Vˆ is quantified by its mean squared error (MSE)
Vˆの精度は、平均二乗誤差（MSE）によって定量化される。

$$
\tag{}
$$

where ED[·] takes the expectation over the logged data and
ここで、ED[-]は記録されたデータに対する期待値をとり

$$
\tag{}
$$

In the following theoretical analysis, we focus on the IPS estimator, since most advanced OPE estimators are based on IPS weighting (Dud´ık et al., 2014; Wang et al., 2017; Su et al., 2019; 2020a; Metelli et al., 2021).
以下の理論的分析では、先進的なOPE推定器のほとんどがIPS重み付けに基づいているため、IPS推定器に焦点を当てる（Dud´ık et al., 2014; Wang et al., 2017; Su et al., 2019; 2020a; Metelli et al., 2021）。
IPS estimates the value of π by re-weighting the observed rewards as follow
IPSは、観測された報酬を以下のように再重み付けすることでπの値を推定する。

$$
\tag{}
$$

where w(x, a) := π(a|x)/π0(a|x) is called the (vanilla) importance weight.
x)/π0(a|x) is called the (vanilla) importance weight.
This estimator is unbiased (i.e., ED[Vˆ IPS(π; D)] = V (π)) under the following common support assumption.
この推定量は、以下の共通支持の仮定の下では不偏である（すなわち、ED[Vˆ IPS(π; D)] = V (π)）。

Assumption 2.1.(Common Support) The logging policy π0 is said to have common support for policy π if π(a|x) > 0 → π0(a|x) > 0 for all a ∈ A and x ∈ X .
x) > 0 → π0(a|x) > 0 for all a ∈ A and x ∈ X .

The unbiasedness of IPS is desirable, making this simple re-weighting technique so popular.
IPSの不偏性は望ましいものであり、この単純な再重み付け技術を非常に人気のあるものにしている。
However, IPS can still be highly biased, particularly when the action space is large.
しかし、IPSは、特にアクション空間が大きい場合、非常に偏ったものになる可能性がある。
Sachdeva et al.(2020) indicate that IPS has the following bias when Assumption 2.1 is not true.
Sachdevaら(2020)は、仮定2.1が真でない場合、IPSは以下のようなバイアスを持つことを示している。

$$
\tag{}
$$

where U0(x, π0) := {a ∈ A | π0(a|x) = 0} is the set of unsupported or deficient actions for context x under π0.
π0(a|x) = 0} is the set of unsupported or deficient actions for context x under π0.
Note that U0(x, π0) can be large especially when A is large.
U0(x,π0)は、特にAが大きいときに大きくなる可能性があることに注意。
This bias is due to the fact that the logged dataset D does not contain any information about the unsupported actions.
このバイアスは、ログに記録されたデータセットDに、サポートされていないアクションに関する情報が含まれていないことに起因する。
Another critical issue of IPS is that its variance can be large, which is given as follows (Dud´ık et al., 2014)
IPSのもう一つの重大な問題は、その分散が大きくなりうることで、それは以下のように与えられる（Dud´ık et al, 2014）。

$$
\tag{2}
$$

where σ 2 (x, a) := V[r|x, a].
x, a].
The variance consists of three terms.
分散は3つの項から成り立っている。
The first term reflects the randomness in the rewards.
第1項は報酬のランダム性を反映している。
The second term represents the variance due to the randomness over the contexts.
第2項はコンテクストのランダム性に起因する分散を表す。
The final term is the penalty arising from the use of IPS weighting, and it is proportional to the weights and the true expected reward.
最後の項は、IPS重み付けの使用から生じるペナルティであり、重みと真の期待報酬に比例する。
The variance contributed by the first and third terms can be extremely large when the weights w(x, a) have a wide range, which occurs when π assigns large probabilities to actions that have low probability under π0.
第1項と第3項が寄与する分散は、重みw(x, a)の範囲が広い場合に非常に大きくなる。
The latter can be expected when the action space A is large and the logging policy π0 aims to have universal support (i.e., π0(a|x) > 0 for all a and x).
後者は、行動空間Aが大きく、ロギング方針π0が普遍的な支持（すなわち、すべてのaとxに対してπ0(a|x)>0）を持つことを目指している場合に予想される。
Swaminathan et al.(2017) also point out that the variance of IPS grows linearly with w(x, a), which can be Ω(|A|).
A|).

This variance issue can be lessened by incorporating a reward estimator qˆ(x, a) ≈ q(x, a) as a control variate, resulting in the DR estimator (Dud´ık et al., 2014).
この分散の問題は，報酬推定量qˆ(x, a) ≈ q(x, a)を制御変量として組み込むことで軽減でき，DR推定量となる(Dud´ık et al., 2014)。
DR often improves the MSE of IPS due to its variance reduction property.
DRは、その分散削減特性により、IPSのMSEを改善することが多い。
However, DR still suffers when the number of actions is large, and it can experience substantial performance deterioration as we demonstrate in our experiments.
しかし、DRはアクションの数が多い場合、依然として問題を抱えており、我々の実験で実証したように、パフォーマンスが大幅に低下する可能性がある。

# The Marginalized IPS Estimator 限界化IPS推定量

The following proposes a new estimator that circumvents the challenges of IPS for large action spaces.
以下では、大きな行動空間に対するIPSの課題を回避する新しい推定器を提案する。
Our approach is to bring additional structure into the estimation problem, providing a path forward despite the minimax optimality of IPS and DR.
我々のアプローチは、IPSとDRのミニマックス最適性にもかかわらず、推定問題にさらなる構造を持ち込み、前進する道を提供することである。
In particular, IPS and DR achieve the minimax optimal MSE of at most O(n −1 (Eπ0 [w(x, a) 2σ 2 (x, a) + w(x, a) 2 r 2 max])), which means that they are impossible to improve upon in the worst case beyond constant factors (Wang et al., 2017; Swaminathan et al., 2017), unless we bring in additional structure.
特に、IPSとDRは、最大でもO(n -1 (Eπ0 [w(x, a) 2σ 2 (x, a) + w(x, a) 2 r 2 max])の最小最適MSEを達成し、これは、追加の構造を持ち込まない限り、最悪の場合、定数因子を超えて改善することが不可能であることを意味する(Wang et al., 2017; Swaminathan et al., 2017)。
Our key idea for overcoming the limits of IPS and DR is to assume the existence of action embeddings as prior information.
IPSとDRの限界を克服するための我々の重要なアイデアは、事前情報としてアクションの埋め込みの存在を仮定することである。
The intuition is that this can help the estimator transfer information between similar actions.
直感的には、これは推定者が類似のアクション間で情報を伝達するのに役立つ。
More formally, suppose we are given a de-dimensional action embedding e ∈ E ⊆ R de for each action a, where we merely assume that the embedding is drawn i.i.d.
より正式には、各アクションaについて、単に埋め込みがi.i.d.描画されると仮定する、非次元のアクション埋め込みe（E⊆Rデ）が与えられたとする。
from some unknown distribution p(e|x, a).
ある未知の分布p(e|x, a)から。
The simplest example is to construct action embeddings using predefined category information (e.g., product category).
最も単純な例は、あらかじめ定義されたカテゴリ情報（例えば、商品カテゴリ）を使ってアクション埋め込みを構築することである。
Then, the embedding distribution is independent of the context and it is deterministic given the action.
その場合、埋め込み分布は文脈に依存せず、アクションが与えられれば決定論的である。
Our framework is also applicable to the most general case of continuous, stochastic, and context-dependent action embeddings.
我々のフレームワークは、連続的、確率的、文脈依存的なアクションの埋め込みという最も一般的な場合にも適用可能である。
For example, product prices may be generated by a personalized pricing algorithm running behind the system.
例えば、商品価格は、システムの背後で実行されるパーソナライズされた価格設定アルゴリズムによって生成される。
In this case, the embedding is continuous, depends on the user context, and can be stochastic if there is some randomness in the pricing algorithm.
この場合、エンベッディングは連続的で、ユーザーのコンテキストに依存し、プライシングアルゴリズムにランダム性があれば確率的である。
Using the action embeddings, we now refine the definition of the policy value as:
アクションの埋め込みを用いて、政策値の定義を次のように洗練する：

$$


$$

Note here that q(x, a) = Ep(e|x,a) [q(x, a, e)] where q(x, a, e) := E[r|x, a, e], so the above refinement does not contradict the original definition given in Eq.(1).
x,a) [q(x, a, e)] where q(x, a, e) := E[r|x, a, e], so the above refinement does not contradict the original definition given in Eq.(1).
A logged bandit dataset now contains action embeddings for each observation in D = {(xi , ai , ei , ri)} n i=1, where each tuple is generated by the logging policy as (x, a, e, r) ∼ p(x)π0(a|x)p(e|x, a)p(r|x, a, e).
x)p(e
Our strategy is to leverage this additional information for achieving a more accurate OPE for large action spaces.
私たちの戦略は、この追加情報を活用して、大きな作用空間に対してより正確なOPEを達成することです。
To motivate our approach, we introduce two properties characterizing an action embedding.
我々のアプローチを動機づけるために、アクションの埋め込みを特徴づける2つの性質を紹介する。

Assumption 3.1.(Common Embedding Support) The logging policy π0 is said to have common embedding support for policy π if p(e|x, π) > 0 → p(e|x, π0) > 0 for all e ∈ E and x ∈ X , where p(e|x, π) := P a∈A p(e|x, a)π(a|x) is the marginal distribution over the action embedding space given context x and policy π.
x, π) > 0 → p(e

Assumption 3.1 is analogous to Assumption 2.1, but requires only the common support with respect to the action embedding space, which can be substantially more compact than the action space itself.
仮定3.1は仮定2.1に類似しているが、作用埋め込み空間に関する共通サポートのみを必要とし、作用空間そのものよりも実質的にコンパクトになりうる。
Indeed, Assumption 3.1 is weaker than common support of IPS (Assumption 2.1).1 Next, we characterize the expressiveness of the embedding in the ideal case, but we will relax this assumption later.
実際、仮定3.1はIPSの共通サポート（仮定2.1）よりも弱い1。次に、理想的な場合の埋め込みの表現力を特徴付けるが、この仮定は後で緩和する。

Assumption 3.2.(No Direct Effect) Action a has no direct effect on the reward r, i.e., a ⊥ r | x, e.
x, e.
As illustrated in Figure 1, Assumption 3.2 requires that every possible effect of a on r be fully mediated by the observed embedding e.
図1に示されているように、仮定3.2は、rに対するaのすべての可能な効果が、観測された埋め込みeによって完全に媒介されることを要求している。
For now, we rely on the validity of Assumption 3.2, as it is convenient for introducing the proposed estimator.
今のところ，仮定3.2は提案する推定量を導入するのに便利なので，この仮定3.2の妥当性に依拠する。
However, we later show that it is often beneficial to strategically discard some embedding dimensions and violate the assumption to achieve a better MSE.
しかし、より良いMSEを達成するためには、戦略的にいくつかの埋め込み次元を捨て、仮定に違反することが有益である場合が多いことを後で示す。
We start the derivation of our new estimator with the observation that Assumption 3.2 gives us another path to unbiased estimation of the policy value without Assumption 2.1.
仮定3.2が、仮定2.1によらない政策価値の不偏推定への別の道を与えてくれるという観察から、新しい推定量の導出を始める。

Proposition 3.3.Under Assumption 3.2, we have
命題3.3.前提3.2の下では、次のようになる。

$$
\tag{}
$$

See Appendix B.1 for the proof.
証明は付録B.1を参照。
Proposition 3.3 provides another expression of the policy value without explicitly relying on the action variable a.
命題3.3は、行動変数aに明示的に依存することなく、政策値を表す別の表現を提供する。
This new expression naturally leads to the following marginalized inverse propensity score (MIPS) estimator, which is our main proposal.
この新しい式は、自然に次のようなMIPS（marginalized inverse propensity score）推定量につながります。

$$
\tag{}
$$

where w(x, e) := p(e|x, π)/p(e|x, π0) is the marginal importance weight defined with respect to the marginal distribution over the action embedding space.
x, π)/p(e|x, π0) is the marginal importance weight defined with respect to the marginal distribution over the action embedding space.
To obtain an intuition for the benefits of MIPS, we provide a toy example in Table 1 with X = {x1}, A = {a1, a2, a3}, and E = {e1, e2, e3} (a special case of our formulation with a discrete embedding space).
MIPSの利点を直感的に理解するために、X＝｛x1｝、A＝｛a1、a2、a3｝、E＝｛e1、e2、e3｝（離散埋め込み空間を持つ我々の定式化の特別な場合）のおもちゃの例を表1に示す。
The left table describes the logging and target policies with respect to A and implies that Assumption 2.1 is violated (π0(a1|x1) = 0.0).
左の表は、Aに関するロギングとターゲット・ポリシーを記述し、仮定2.1が破られることを意味する（π0(a1|x1) = 0.0）。
The middle table describes the conditional distribution of the action embedding e given action a (e.g., probability of a movie a belonging to a genre e).
真ん中の表は、アクションaが与えられたときのアクション埋め込みeの条件付き分布（例えば、映画aがジャンルeに属する確率）を記述している。
The right table describes the marginal distributions over E, which are calculable from the other two tables.
右の表は、E上の周辺分布を記述したもので、他の2つの表から計算できる。
By considering the marginal distribution, Assumption 3.1 is ensured in the right table, even if Assumption 2.1 is not true in the left table.
限界分布を考慮すれば、左の表で仮定2.1が真でなくても、右の表で仮定3.1が保証される。
Moreover, the maximum importance weight is smaller for the right table (maxe∈E w(x1, e) < maxa∈A w(x1, a)), which may contribute to a variance reduction of the resulting estimator.
さらに、最大重要度ウェイトは右のテーブルの方が小さく（maxe∈E w(x1, e) < maxa∈A w(x1, a)）、これは結果として得られる推定量の分散低減に寄与する可能性がある。
Below, we formally analyze the key statistical properties of MIPS and compare them with those of IPS, including the realistic case where Assumption 3.2 is violated.
以下では、MIPSの主要な統計的性質を正式に分析し、仮定3.2に違反する現実的な場合を含め、IPSのそれと比較する。

## Theoretical Analysis 理論的分析

First, the following proposition shows that MIPS is unbiased under assumptions different from those of IPS.
まず、以下の命題は、MIPSがIPSとは異なる仮定のもとでは不偏であることを示している。

Proposition 3.4.Under Assumptions 3.1 and 3.2, MIPS is unbiased, i.e., ED[VˆMIPS(π; D)] = V (π) for any π.
すなわち、ED[VˆMIPS(π; D)] = V (π)である。
See Appendix B.2 for the proof.
証明は付録B.2を参照。
Proposition 3.4 states that, even when π0 fails to provide common support over A such that IPS is biased, MIPS can still be unbiased if π0 provides common support over E (Assumption 3.1) and e fully captures the causal effect of a on r (Assumption 3.2).
命題3.4は、IPSが偏るようなA上の共通支持をπ0が提供できない場合でも、π0がE上の共通支持を提供し（仮定3.1）、eがr上のaの因果効果を完全に捕らえるならば（仮定3.2）、MIPSは依然として不偏であり得ることを述べている。

Having multiple estimators that enable unbiased OPE under different assumptions is in itself desirable, as we can choose the appropriate estimator depending on the data generating process.
異なる仮定の下で不偏OPEを可能にする複数の推定量を持つことは、それ自体望ましいことであり、データ生成プロセスに応じて適切な推定量を選択できるからである。
However, it is also helpful to understand how violations of the assumptions influence the bias of the resulting estimator.
しかし，仮定の違反が結果の推定量のバイアスにどのように影響するかを理解することも有益である。
In particular, for MIPS, it is difficult to verify whether Assumption 3.2 is true in practice.
特にMIPSの場合、仮定3.2が実際に正しいかどうかを検証するのは難しい。
The following theorem characterizes the bias of MIPS.
次の定理は、MIPSのバイアスを特徴づけるものである。
Theorem 3.5.(Bias of MIPS) If Assumption 3.1 is true, but Assumption 3.2 is violated, MIPS has the following bias.
定理3.5.(MIPSのバイアス) 仮定3.1が真で、仮定3.2が破れている場合、MIPSは次のようなバイアスを持つ。

$$
\tag{}
$$

where a, b ∈ A.
ここでa、bはAである。
See Appendix B.3 for the proof.
証明は付録B.3を参照のこと。
Theorem 3.5 suggests that three factors contribute to the bias of MIPS when Assumption 3.2 is violated.
定理3.5は、仮定3.2に違反した場合、3つの要因がMIPSの偏りに寄与することを示唆している。
The first factor is the predictivity of the action embeddings with respect to the actual actions.
第一の要因は、実際のアクションに対するアクションの埋め込みの予測性である。
When action a is predictable given context x and embedding e, π0(a|x, e) is close to zero or one (deterministic), meaning that π0(a|x, e)π0(b|x, e) is close to zero.
x, e) is close to zero or one (deterministic), meaning that π0(a
This suggests that even if Assumption 3.2 is violated, action embeddings that identify the actions well still enable a nearly unbiased estimation of MIPS.
このことは、仮に仮定3.2に違反したとしても、アクションをうまく識別するアクション埋め込みによって、MIPSをほぼ不偏に推定できることを示唆している。
The second factor is the amount of direct effect of the action on the reward, which is quantified by q(x, a, e) − q(x, b, e).
2つ目の要因は、報酬に対する行動の直接的効果の大きさで、q(x, a, e) - q(x, b, e)で定量化される。
When the direct effect of a on r is small, q(x, a, e) − q(x, b, e) also becomes small and so is the bias of MIPS.
rに対するaの直接効果が小さい場合、q(x, a, e) - q(x, b, e)も小さくなり、MIPSのバイアスも小さくなる。
In an ideal situation where Assumption 3.2 is satisfied, we have q(x, a, e) = q(x, b, e) = q(x, e), thus MIPS is unbiased, which is consistent with Proposition 3.4.Note that the first two factors suggest that, to reduce the bias, the action embeddings should be informative so that they are either predictive of the actions or mediate a large amount of the causal effect.
仮定3.2が満たされる理想的な状況では、q(x, a, e) = q(x, b, e) = q(x, e)となり、MIPSは不偏である。
The final factor is the similarity between logging and target policies quantified by w(x, a) − w(x, b).
最後の要因は、w(x, a) - w(x, b)で定量化されるロギングとターゲットポリシーの類似性である。
When Assumption 3.2 is satisfied, MIPS is unbiased for any target policy, however, Theorem 3.5 suggests that if the assumption is not true, MIPS produces a larger bias for target policies dissimilar from the logging policy.2
仮定3.2が満たされる場合、MIPSはどのようなターゲットポリシーに対しても不偏であるが、定理3.5は仮定が真でない場合、MIPSはロギングポリシーと異なるターゲットポリシーに対してより大きなバイアスを生成することを示唆している2。

Next, we analyze the variance of MIPS, which we show is never worse than that of IPS and can be substantially lower.
次に、MIPSの分散を分析する。MIPSの分散はIPSの分散よりも決して悪くなく、大幅に小さくなる可能性があることを示す。
Theorem 3.6.(Variance Reduction of MIPS) Under Assumptions 2.1, 3.1, and 3.2, we have
定理3.6(MIPSの分散削減) 仮定2.1、3.1、3.2の下で、次が成り立つ。

$$
\tag{}
$$

which is non-negative.
これは非負である。
Note that the variance reduction is also lower bounded by zero even when Assumption 3.2 is not true.
仮定3.2が真でない場合でも、分散の減少はゼロで下界されることに注意。
See Appendix B.4 for the proof.
証明は付録B.4を参照のこと。
There are two factors that affect the amount of variance reduction.
分散の減少量に影響を与える要因は2つある。
The first factor is the second moment of the reward with respect to p(r|x, e).
最初の要因は、p(r|x, e)に対する報酬の二次モーメントである。
This term becomes large when, for example, the reward is noisy even after conditioning on the action embedding e.
この項が大きくなるのは、例えば、行動埋め込みeを条件付けした後でも報酬にノイズがある場合である。
The second factor is the variance of w(x, a) with respect to the conditional distribution π0(a|x, e), which becomes large when (i) w(x, a) has a wide range or (ii) there remain large variations in a even after conditioning on action embedding e so that π0(a|x, e) remains stochastic.
x, e), which becomes large when (i) w(x, a) has a wide range or (ii) there remain large variations in a even after conditioning on action embedding e so that π0(a|x, e) remains stochastic.
Therefore, MIPS becomes increasingly favorable compared to IPS for larger action spaces where the variance of w(x, a) becomes larger.
したがって、w(x, a)の分散が大きくなるような大きな行動空間では、MIPSはIPSに比べてますます有利になる。
Moreover, to obtain a large variance reduction, the action embedding should ideally not be unnecessarily predictive of the actions.
さらに、大きな分散削減を得るためには、アクションの埋め込みは、アクションを不必要に予測しないことが理想的である。
Finally, the next theorem describes the gain in MSE we can obtain from MIPS when Assumption 3.2 is violated.
最後に、次の定理は、仮定3.2に違反した場合にMIPSから得られるMSEの利得を記述している。

Theorem 3.7.(MSE Gain of MIPS) Under Assumptions 2.1 and 3.1, we have
定理3.7.(MIPSのMSE利得) 仮定2.1と3.1の下で、次が成り立つ。

$$
\tag{}
$$

See Appendix B.5 for the proof.
証明は付録B.5を参照のこと。
Note that IPS can have some bias when Assumption 2.1 is not true, possibly producing a greater MSE gain for MIPS
仮定2.1が真でない場合、IPSに偏りが生じ、MIPSのMSE利得が大きくなる可能性がある。

## Data-Driven Embedding Selection データ駆動型埋め込み選択

The analysis in the previous section implies a clear biasvariance trade-off with respect to the quality of the action embeddings.
前節の分析は、アクションの埋め込みの質に関して、バイアスと分散のトレードオフが明確であることを示唆している。
Specifically, Theorem 3.5 suggests that the action embeddings should be as informative as possible to reduce the bias when Assumption 3.2 is violated.
具体的には、定理3.5は、仮定3.2に違反した場合のバイアスを減らすために、アクションの埋め込みは可能な限り情報的であるべきであることを示唆している。
On the other hand, Theorem 3.6 suggests that the action embeddings should be as coarse as possible to gain a greater variance reduction.
一方、定理3.6は、より大きな分散削減を得るためには、アクションの埋め込みをできるだけ粗くすべきことを示唆している。
Theorem 3.7 summarizes the bias-variance trade-off in terms of MSE.
定理3.7は、バイアスと分散のトレードオフをMSEの観点からまとめたものである。
A possible criticism to MIPS is Assumption 3.2, as it is hard to verify whether this assumption is satisfied using only the observed logged data.
MIPSに対する批判として考えられるのは、仮定3.2である。なぜなら、観測されたログデータだけでは、この仮定が満たされているかどうかを検証するのが難しいからである。
However, the above discussion about the bias-variance trade-off implies that it might be effective to strategically violate Assumption 3.2 by discarding some embedding dimensions.
しかし、バイアスと分散のトレードオフに関する上記の議論は、いくつかの埋め込み次元を捨てることによって、戦略的に仮定3.2に違反することが効果的である可能性があることを示唆している。
This action embedding selection can lead to a large variance reduction at the cost of introducing some bias, possibly improving the MSE of MIPS.
このアクション・エンベッディング・セレクションは、多少のバイアスを導入する代償として、大きな分散削減をもたらし、MIPSのMSEを改善する可能性がある。
To implement the action embedding selection, we can adapt the estimator selection method called SLOPE proposed in Su et al.(2020b) and Tucker & Lee (2021).
アクション埋め込み選択を実装するには、Su et al.(2020b)やTucker & Lee(2021)で提案されているSLOPEと呼ばれる推定量選択法を適応すればよい。
SLOPE is based on Lepski’s principle for bandwidth selection in nonparametric statistics (Lepski & Spokoiny, 1997) and is used to tune the hyperparameters of OPE estimators.
SLOPEは、ノンパラメトリック統計における帯域幅選択のためのLepskiの原理(Lepski & Spokoiny, 1997)に基づいており、OPE推定量のハイパーパラメータを調整するために使用される。
A benefit of SLOPE is that it avoids estimating the bias of the estimator, which is as difficult as OPE.
SLOPEの利点は、OPEと同様に困難な推定値のバイアスの推定を回避できることである。
Appendix C describes how to apply SLOPE to the action embedding selection in our setup, and Section 4 evaluates its benefit empirically.
付録Cでは、我々のセットアップにおけるアクション埋め込み選択にSLOPEを適用する方法を説明し、セクション4ではその利点を実証的に評価する。

## Estimating the Marginal Importance Weights 限界重要度重みの推定

When using MIPS, we might have to estimate w(x, e) depending on how the embeddings are given.
MIPSを使う場合、埋め込みがどのように与えられるかによって、w(x, e)を推定しなければならないかもしれない。
A simple approach to this is to utilize the following transformation
これに対する簡単なアプローチは、以下の変換を利用することである。

$$
\tag{3}
$$

Eq.(3) implies that we need an estimate of π0(a|x, e), which we compute by regressing a on (x, e).
式(3)は、π0(a|x, e)の推定値が必要であることを意味し、これはaを(x, e)に回帰することによって計算される。
We can then estimate w(x, e) as wˆ(x, e) = Eπˆ0(a|x,e) [w(x, a)].3 This procedure is easy to implement and tractable, even when the embedding space is high-dimensional and continuous.
そして、w(x,e)をwˆ(x,e)=Eπˆ0(a|x,e) [w(x, a)]として推定することができる。3 この手続きは、埋め込み空間が高次元で連続的な場合でも、簡単に実行でき、扱いやすい。
Note that, even if there are some deficient actions, we can directly estimate w(x, e) by solving density ratio estimation as binary classification as done in Sondhi et al.(2020).
なお、欠損アクションがあったとしても、Sondhiら(2020)のように密度比推定を二値分類として解くことで、w(x, e)を直接推定することができる。

# Empirical Evaluation 実証的評価

We first evaluate MIPS on synthetic data to identify the situations where it enables a more accurate OPE.
まずMIPSを合成データで評価し、MIPSがより正確なOPEを可能にする状況を特定する。
Second, we validate real-world applicability on data from an online fashion store.
第二に、オンライン・ファッション・ストアのデータを用いて、実世界での適用可能性を検証する。
Our experiments are conducted using the OpenBanditPipeline (OBP)4 , an open-source software for OPE provided by Saito et al.(2020).
我々の実験は、Saitoら(2020)が提供するOPE用のオープンソースソフトウェアであるOpenBanditPipeline(OBP)4を用いて行われた。
Our experiment implementation is available at https://github.com/usaito/icml2022-mips
我々の実験の実装は https://github.com/usaito/icml2022-mips にある。

## Synthetic Data 合成データ

For the first set of experiments, we create synthetic data to be able to compare the estimates to the ground-truth value of the target policies.
最初の実験セットでは、ターゲット・ポリシーのグランド・トゥルース値と推定値を比較できるように、合成データを作成する。
To create the data, we sample 10- dimensional context vectors x from the standard normal distribution.
データを作成するために、標準正規分布から10次元のコンテキスト・ベクトルxをサンプリングする。
We also sample de-dimensional categorical action embedding e ∈ E from the following conditional distribution given action a.
また、アクションaが与えられたときの以下の条件分布から、非次元のカテゴリー的アクション埋め込みe∈Eをサンプリングする。

$$
\tag{4}
$$

which is independent of the context x in the synthetic experiment.
これは、合成実験における文脈xとは無関係である。
{αa,ek } is a set of parameters sampled independently from the standard normal distribution.
{αa,ek}は標準正規分布から独立にサンプリングされたパラメータの集合である。
Each dimension of E has a cardinality of 10, i.e., Ek = {1, 2, .
すなわち、Ek = {1, 2, .
..
..
, 10}.
, 10}.
We then synthesize the expected reward as
そして、期待報酬を次のように合成する。

$$
\tag{5}
$$

where M, θx, and θe are parameter matrices or vectors to define the expected reward.
ここで、M、θx、θeは期待報酬を定義するパラメータ行列またはベクトルである。
These parameters are sampled from a uniform distribution with range [−1, 1].
これらのパラメータは、範囲[-1, 1]の一様分布からサンプリングされる。
xek is a context vector corresponding to the k-th dimension of the action embedding, which is unobserved to the estimators.
xekは、行動埋め込みのk番目の次元に対応する文脈ベクトルであり、推定量にとっては未観測である。
ηk specifies the importance of the k-th dimension of the action embedding, which is sampled from Dirichlet distribution so that Pde k=1 ηk = 1.
ηkは作用埋込みのk番目の次元の重要度を指定し、Pde k=1 ηk = 1となるようにディリクレ分布からサンプリングされる。
Note that if we observe all dimensions of E, then q(x, e) = q(x, a, e).
Eのすべての次元を観測する場合、q(x, e) = q(x, a, e)であることに注意。
On the other hand, q(x, e) 6= q(x, a, e), if there are some missing dimensions, which means that Assumption 3.2 is violated.
一方、q(x, e) 6= q(x,a,e)であるが、これは次元がいくつか欠けている場合であり、仮定3.2に違反することを意味する。
We synthesize the logging policy π0 by applying the softmax function to q(x, a) = Ep(e|a) [q(x, e)] a
我々は、q（x，a）＝Ep（e|a）［q（x，e）］aにソフトマックス関数を適用することによって、ロギングポリシーπ0を合成する。

$$
\tag{6}
$$

where β is a parameter that controls the optimality and entropy of the logging policy.
ここで、βはロギングポリシーの最適性とエントロピーを制御するパラメータである。
A large positive value of β leads to a near-deterministic and well-performing logging policy, while lower values make the logging policy increasingly worse.
βの大きな正の値は、ほぼ決定論的で性能の良いロギング・ポリシーにつながり、低い値はロギング・ポリシーをますます悪くする。
In the main text, we use β = −1, and additional results for other values of β can be found in Appendix D.2.In contrast, the target policy π is defined a
メイン・テキストでは、β = -1を使用し、βの他の値に関する追加結果は付録D.2にある。

$$
\tag{}
$$

where the noise  ∈ [0, 1] controls the quality of π.
ここで、ノイズ∈[0, 1]はπの質を制御する。
In the main text, we set  = 0.05, which produces a near-optimal and near-deterministic target policy.
本文では、=0.05とし、ほぼ最適でほぼ決定論的なターゲット・ポリシーを生成する。
We share additional results for other values of  in Appendix D.2.To summarize, we first sample context x and define the expected reward q(x, e) as in Eq.(5).
要約すると、まずコンテキストxをサンプリングし、期待報酬q(x, e)を式(5)のように定義する。
We then sample discrete action a from π0 based on Eq.(6).
次に、式(6)に基づいてπ0から離散アクションaをサンプリングする。
Given action a, we sample categorical action embedding e based on Eq.(4).
アクションaが与えられたとき、式(4)に基づいてカテゴリカルアクション埋め込みeをサンプリングする。
Finally, we sample the reward from a normal distribution with mean q(x, e) and standard deviation σ = 2.5.Iterating this procedure n times generates logged data D with n independent copies of (x, a, e, r).
最後に、平均q(x, e)、標準偏差σ = 2.5を持つ正規分布から報酬をサンプリングする。この手順をn回繰り返すと、(x, a, e, r)のn個の独立したコピーを持つログデータDが生成される。

### BASELINES ベースライン

We compare our estimator with Direct Method (DM), IPS, and DR.5 We use the Random Forest (Breiman, 2001) implemented in scikit-learn (Pedregosa et al., 2011) along with 2-fold cross-fitting (Newey & Robins, 2018) to obtain qˆ(x, e) for DR and DM.
我々は，DRとDMのqˆ(x, e)を求めるために，scikit-learn (Pedregosa et al, 2011)に実装されたRandom Forest (Breiman, 2001)と2-fold cross-fitting (Newey & Robins, 2018)を使用する。
We use the Logistic Regression of scikit-learn to estimate πˆ0(a|x, e) for MIPS.
scikit-learnのロジスティック回帰を用いて、MIPSのπˆ0(a|x, e)を推定する。
We also report the results of MIPS with the true importance weights as “MIPS (true)”.
また、真の重要度重みを用いたMIPSの結果も「MIPS（真の）」として報告する。
MIPS (true) provides the best performance we could achieve by improving the procedure for estimating the importance weights of MIPS
MIPS（true）は、MIPSの重要度重みを推定する手順を改善することで達成できる最高のパフォーマンスを提供する。

### RESULTS 結果

The following reports and discusses the MSE, squared bias, and variance of the estimators computed over 100 different sets of logged data replicated with different seeds.
以下では、異なるシードで再現された100セットのログデータに対して計算された推定量のMSE、二乗バイアス、分散を報告し、議論する。

#### How does MIPS perform with varying numbers of actions? MIPSは様々なアクション数でどのようなパフォーマンスを発揮するか？

First, we evaluate the estimators’ performance when we vary the number of actions from 10 to 5000.
まず、アクション数を10から5000まで変化させたときの推定値の性能を評価する。
The sample size is fixed at n = 10000.
サンプルサイズはn = 10000に固定されている。
Figure 2 shows how the number of actions affects the estimators’ MSE (both on linear- and log-scale).
図2は、アクション数が推定値のMSE（線形スケールと対数スケールの両方）にどのように影響するかを示している。
We observe that MIPS provides substantial improvements over IPS and DR particularly for larger action sets.
我々は、MIPSがIPSやDRよりも、特に大規模なアクションセットにおいて大幅に改善されることを確認した。
More specifically, when |A| = 10, MSE(VˆIPS) MSE(VˆMIPS) = 1.38, while MSE(VˆIPS) MSE(VˆMIPS) = 12.38 for |A| = 5000, indicating a significant performance improvement of MIPS for larger action spaces as suggested in Theorem 3.6.MIPS is also consistently better than DM, which suffers from high bias.
A
The figure also shows that MIPS (true) is even better than MIPS in large action sets, mostly due to the reduced bias when using the true marginal importance weights.
また、MIPS(true)は、大規模なアクションセットにおいて、MIPSよりも優れている。
This observation implies that there is room for further improvement in how to estimate the marginal importance weights.
この観察結果は、限界重要度ウエイトの推定方法にさらなる改善の余地があることを示唆している。

#### How does MIPS perform with varying sample sizes? サンプルサイズを変化させた場合のMIPSの性能は？

Next, we compare the estimators under varying numbers of samples (n ∈ {800, 1600, 3200, 6400, 12800, 25600}).
次に、サンプル数（n∈{800, 1600, 3200, 6400, 12800, 25600}）を変化させて推定量を比較する。
The number of actions is fixed at |A| = 1000.
A
Figure 3 reports how the estimators’ MSE changes with the size of logged bandit data.
図3は、ロギングされたバンディットデータのサイズによって推定値のMSEがどのように変化するかを示している。
We can see that MIPS is appealing in particular for small sample sizes where it outperforms IPS and DR by a larger margin than in large sample regimes ( MSE(VˆIPS) MSE(VˆMIPS) = 9.10 when n = 800, while MSE(VˆIPS) MSE(VˆMIPS) = 4.87 when n = 25600).
MIPSは特にサンプルサイズが小さい場合に魅力的であり、サンプルサイズが大きい場合よりも大きなマージンでIPSとDRを上回ることがわかる（n = 800のときのMSE(VˆIPS) MSE(VˆMIPS) = 9.10、n = 25600のときのMSE(VˆIPS) MSE(VˆMIPS) = 4.87）。
With the growing sample size, MIPS, IPS, and DR improve their MSE as their variance decreases.
サンプルサイズが大きくなるにつれて、MIPS、IPS、DRは分散が小さくなるにつれてMSEが向上する。
In contrast, the accuracy of DM does not change across different sample sizes, but it performs better than IPS and DR because they converge very slowly in the presence of many actions.
対照的に、DMの精度はサンプルサイズが異なっても変わらないが、多くのアクションが存在する場合には収束が非常に遅くなるため、IPSやDRよりも優れている。
In contrast, MIPS is better than DM except for n = 800, as the bias of MIPS is much smaller than that of DM.
一方、MIPSのバイアスはDMのバイアスよりもはるかに小さいため、n = 800を除いてMIPSはDMよりも優れている。
Moreover, MIPS becomes increasingly better than DM with the growing sample size, as the variance of MIPS decreases while DM remains highly biased.
さらに、MIPSの分散が減少する一方で、DMは非常に偏ったままであるため、サンプルサイズが大きくなるにつれて、MIPSはDMよりもますます良くなる。

#### How does MIPS perform with varying numbers of deficient actions? MIPSは欠陥アクションの数を変化させた場合、どのようなパフォーマンスを発揮するのだろうか。

We also compare the estimators under varying numbers of deficient actions (|U0| ∈ {0, 100, 300, 500, 700, 900}) with a fixed action set (|A| = 1000).
U0
Figure 4 shows how the number of deficient actions affects the estimators’ MSE, squared bias, and variance.
図4は、欠陥アクションの数が推定値のMSE、二乗バイアス、分散にどのように影響するかを示している。
The results suggest that MIPS (true) is robust and not affected by the existence of deficient actions.
その結果、MIPS（真）はロバストであり、欠陥行動の存在に影響されないことが示唆された。
In addition, MIPS is mostly better than DM, IPS, and DR even when there are many deficient actions.
また、MIPSはDM、IPS、DRに比べ、欠陥のあるアクションが多い場合でも、ほとんど優れている。
However, we also observe that the gap between MIPS and MIPS (true) increases for large numbers of deficient actions due to the bias in estimating the marginal importance weights.
しかし、MIPSとMIPS(true)の間のギャップは、限界重要度重みを推定する際のバイアスにより、欠陥のあるアクションの数が多いほど大きくなることも観察された。
Note that the MSE of IPS and DR decreases with increasing number of deficient actions, because their variance becomes smaller with a smaller number of supported actions, even though their bias increases as suggested by Sachdeva et al.(2020).
Sachdevaら(2020)が示唆するように、IPSとDRのバイアスは増加するが、その分散はサポートされるアクションの数が少ないほど小さくなるため、IPSとDRのMSEは欠陥アクションの数が増えるほど減少することに注意。

#### How does MIPS perform when Assumption 3.2 is violated? 仮定3.2が破られたとき、MIPSはどのような性能を発揮するか？

Here, we evaluate the accuracy of MIPS when Assumption 3.2 is violated.
ここでは、仮定3.2に違反した場合のMIPSの精度を評価する。
To adjust the amount of violation, we modify the action embedding space and reduce the cardinality of each dimension of E to 2 (i.e., Ek = {0, 1}), while we increase the number of dimensions to 20 (de = 20).
違反量を調整するため、アクション埋め込み空間を変更し、Eの各次元のカーディナリティを2（すなわち、Ek＝{0,1}）に減らす一方、次元数を20（de＝20）に増やす。
This leads to |E| = 220 = 1, 048, 576, and we can now drop some dimensions to increase violation.
E
In particular, when we observe all dimensions of E, Assumption 3.2 is perfectly satisfied.
特に、Eのすべての次元を観測する場合、仮定3.2は完全に満たされる。
However, when we withhold {0, 2, 4, .
しかし、{0, 2, 4, .
..
..
, 18} embedding dimensions, the assumption becomes increasingly invalid.
18}の埋め込み次元では、この仮定はますます無効になっていく。
When many dimensions are missing, the bias of MIPS is expected to increase as suggested in Theorem 3.5, potentially leading to a worse MSE.
多くの次元が欠落している場合、定理3.5で示唆されているようにMIPSのバイアスが増加し、MSEが悪化する可能性がある。
Figure 5 shows how the MSE, squared bias, and variance of the estimators change with varying numbers of unobserved embedding dimensions.
図5は、推定量のMSE、二乗バイアス、分散が、未観測の埋め込み次元の数を変えることによってどのように変化するかを示している。
Somewhat surprisingly, we observe that MIPS and MIPS (true) perform better when there are some missing dimensions, even if it leads to the violated assumption.
少し意外なことに、MIPSとMIPS（true）は、たとえそれが仮定に反することになったとしても、いくつかの次元が欠落している場合に、より良い性能を発揮することが観察された。
Specifically, the MSE of MIPS and MIPS (true) is minimized when there are 4 and 8 missing dimensions (out of 20), respectively.
具体的には、MIPSとMIPS(true)のMSEは、それぞれ（20次元中）4次元と8次元の欠落がある場合に最小化される。
This phenomenon is due to the reduced variance.
この現象は分散の減少によるものである。
The third column of Figure 5 implies that the variance of MIPS and MIPS (true) decreases substantially with an increasing number of unobserved dimensions, while the bias increases with the violated assumption as expected.
図5の第3列は、MIPSとMIPS（true）の分散が、観察されない次元の数が増えるにつれて大幅に減少する一方、バイアスは予想通り仮定に違反するにつれて増加することを意味している。
These observations suggest that MIPS can be highly effective despite the violated assumption.
これらの観察結果は、MIPSが前提に違反しているにもかかわらず、高い効果を発揮できることを示唆している。

#### How does data-driven embedding selection perform combined with MIPS? データ駆動型エンベッディング選択はMIPSとどのように組み合わされるのか？

The previous section showed that there is a potential to improve the accuracy of MIPS by selecting a subset of dimensions for estimating the marginal importance weights.
前節では、限界重要度重みを推定するために次元のサブセットを選択することで、MIPSの精度を向上させる可能性があることを示した。
We now evaluate whether we can effectively address this embedding selection problem.
次に、この埋め込み選択問題に効果的に対処できるかどうかを評価する。
Figure 6 compares the MSE, squared bias, and variance of MIPS and MIPS with SLOPE (MIPS w/ SLOPE) using the same embedding space as in the previous section.
図6は、前節と同じ埋め込み空間を用いたMIPSとMIPS with SLOPE（MIPS w/SLOPE）のMSE、二乗バイアス、分散を比較したものである。
Note that we vary the sample size n and fix |A| = 1000.
A
The results suggest that the data-driven embedding selection provides a substantial improvement in MSE for small sample sizes.
その結果、データ駆動型の埋め込み選択は、サンプルサイズが小さい場合にMSEの大幅な改善をもたらすことが示唆された。
As shown in the second and third columns in Figure 6, the embedding selection significantly reduces the variance at the cost of introducing some bias by strategically violating the assumption, which results in a better MSE.
図6の2列目と3列目に示されているように、埋め込み選択は、戦略的に仮定に違反することによって多少のバイアスを導入する代償として、分散を大幅に削減し、その結果、MSEが改善される。

#### Other benefits of MIPS. MIPSのその他の利点

MIPS has additional benefits over the conventional estimators.
MIPSには、従来の推定量よりもさらに大きな利点がある。
In fact, in addition to the case with many actions, IPS is also vulnerable when logging and target policies differ substantially and the reward is noisy (see Eq.(2)).
実際、アクションが多い場合だけでなく、ログとターゲットのポリシーが大きく異なり、報酬がノイジーな場合にもIPSは脆弱である（式(2)参照）。
Appendix D.2 empirically investigates the additional benefits of MIPS with varying logging/target policies and varying noise levels with a fixed action set.
付録D.2では、ロギング／ターゲットポリシーを変化させ、アクションセットを固定してノイズレベルを変化させた場合のMIPSの付加的な利点を実証的に調査している。
We observe that MIPS is substantially more robust to the changes in policies and added noise than IPS or DR, which provides further arguments for the applicability of MIPS.
我々は、MIPSがIPSやDRよりも、ポリシーの変更やノイズの付加に対してロバストであることを観察した。

## Real-World Data 実世界のデータ

To assess the real-world applicability of MIPS, we now evaluate MIPS on real-world bandit data.
MIPSの実世界での適用性を評価するため、次にMIPSを実世界のバンディットデータで評価する。
In particular, we use the Open Bandit Dataset (OBD)6 (Saito et al., 2020), a publicly available logged bandit dataset collected on a large-scale fashion e-commerce platform.
特に、大規模なファッションEコマース・プラットフォームで収集された、一般に利用可能なログ・バンディット・データセットであるオープン・バンディット・データセット（OBD）6（Saito et al.
We use 100,000 observations that are randomly sub-sampled from the “ALL” campaign of OBD.
我々は、OBDの "ALL "キャンペーンから無作為にサブサンプリングされた100,000のオブザベーションを使用する。
The dataset contains user contexts x, fashion items to recommend as action a ∈ A where |A| = 240, and resulting clicks as reward r ∈ {0, 1}.
A
OBD also includes 4-dimensional action embedding vectors such as hierarchical category information about the fashion items.
OBDはまた、ファッションアイテムに関する階層的なカテゴリー情報のような4次元のアクション埋め込みベクトルを含む。
The dataset consists of two sets of logged bandit data collected by two different policies (uniform random and Thompson sampling) during an A/B test of these policies.
データセットは、2つの異なるポリシー（一様ランダムサンプリングとトンプソンサンプリング）のA/Bテストで収集された2セットのログバンディットデータから構成される。
We regard uniform random and Thompson sampling as logging and target policies, respectively, to perform an evaluation of OPE estimators.
一様無作為サンプリングとトンプソンサンプリングをそれぞれロギング政策とターゲット政策とみなして、OPE推定量の評価を行う。
Appendix D.3 describes the detailed experimental procedure to evaluate the accuracy of the estimators on real-world bandit data.
付録D.3では、実際のバンディットデータを用いて推定値の精度を評価するための詳細な実験手順を説明する。

#### Results. 結果

We evaluate MIPS (w/o SLOPE) and MIPS (w/ SLOPE) in comparison to DM, IPS, DR, Switch-DR, More Robust DR (Farajtabar et al., 2018), DRos, and DR-λ.
MIPS（SLOPEなし）とMIPS（SLOPEあり）を、DM、IPS、DR、Switch-DR、More Robust DR（Farajtabar et al, 2018）、DRos、DR-λと比較して評価する。
We apply SLOPE to tune the built-in hyperparameters of SwitchDR, DRos, and DR-λ.
SLOPEを適用して、SwitchDR、DRos、DR-λの組み込みハイパーパラメータを調整する。
Figure 7 compares the estimators by drawing the cumulative distribution function (CDF) of their squared errors estimated with 150 different bootstrapped samples of the logged data.
図7は、ログデータの150の異なるブートストラップサンプルで推定された二乗誤差の累積分布関数（CDF）を描画することにより、推定量を比較したものである。
Note that the squared errors are normalized by that of IPS.
なお、二乗誤差はIPSの誤差で正規化されている。
We find that MIPS (w/ SLOPE) outperforms IPS in about 80% of the simulation runs, while other estimators, including MIPS (w/o SLOPE), work similarly to IPS.
MIPS(SLOPE付き)はシミュレーションの約80%でIPSを上回り、MIPS(SLOPEなし)を含む他の推定量はIPSと同様に機能することがわかった。
This result demonstrates the real-world applicability of our estimator as well as the importance of implementing action embedding selection in practice.
この結果は、我々の推定器の実世界での適用可能性を示すとともに、アクション埋め込み選択を実際に実装することの重要性を示している。
We report qualitatively similar results for other sample sizes (from 10,000 to 500,000) in Appendix D.3.
付録D.3では、他のサンプルサイズ（10,000から500,000まで）についても定性的には同様の結果を報告している。

# Conclusion and Future Work 結論と今後の課題

We explored the problem of OPE for large action spaces.
我々は、大規模な行動空間に対するOPEの問題を探求した。
In this setting, existing estimators based on IPS suffer from impractical variance, which limits their applicability.
このような設定において、IPSに基づく既存の推定量は実用的でない分散に悩まされ、適用が制限される。
This problem is highly relevant for practical applications, as many real decision making problems such as recommender systems have to deal with a large number of discrete actions.
推薦システムのような実際の意思決定問題の多くは、多数の離散的な行動を扱わなければならないため、この問題は実用的な応用に非常に適している。
To achieve an accurate OPE for large action spaces, we propose the MIPS estimator, which builds on the marginal importance weights computed with action embeddings.
大規模な行動空間に対して正確なOPEを実現するために、我々は行動埋め込みで計算された限界重要度重みを基にしたMIPS推定器を提案する。
We characterize the important statistical properties of the proposed estimator and discuss when it is superior to the conventional ones.
提案する推定量の重要な統計的性質を明らかにし、どのような場合に従来の推定量より優れているかを議論する。
Extensive experiments demonstrate that MIPS provides a significant gain in MSE when the vanilla importance weights become large due to large action spaces, substantially outperforming IPS and related estimators.
広範な実験により、行動空間が大きいためにバニラ重要度重みが大きくなった場合、MIPSはMSEにおいて有意な利得を提供し、IPSや関連推定量を大幅に上回ることが実証された。

Our work raises several interesting research questions.
私たちの研究は、いくつかの興味深い研究課題を提起している。
For example, this work assumes the existence of some predefined action embeddings and analyzes the resulting statistical properties of MIPS.
例えば、この研究では、事前に定義されたアクションの埋め込みが存在すると仮定し、その結果生じるMIPSの統計的特性を分析している。
Even though we discussed how to choose which embedding dimensions to use for OPE (Section 3.2), it would be intriguing to develop a more principled method to optimize or learn (possibly continuous) action embeddings from the logged data for further improving MIPS.
OPEに使用する埋め込み次元を選択する方法（セクション3.2）について説明したが、MIPSをさらに向上させるために、ログデータから行動埋め込みを最適化または学習する（おそらく連続的な）より原理的な方法を開発することは興味深い。
Developing a method for accurately estimating the marginal importance weight would also be crucial to fill the gap between MIPS and MIPS (true) observed in our experiments.
また、限界重要度ウェイトを正確に推定する方法を開発することは、我々の実験で観察されたMIPSとMIPS（真）の間のギャップを埋めるために極めて重要である。
It would also be interesting to explore off-policy learning using action embeddings and possible applications of marginal importance weighting to other estimators that depend on the vanilla importance weight such as DR.
また、アクションの埋め込みを用いたオフポリシー学習や、DRのようなバニラ重要度ウェイトに依存する他の推定量への限界重要度ウェイトの応用の可能性を探ることも興味深い。
