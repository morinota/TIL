refs: https://arxiv.org/abs/2507.13608

# Off-Policy Evaluation and Learning for Matching Markets
# オフポリシー評価とマッチング市場のための学習

Matching users based on mutual preferences is a fundamental aspect of services driven by reciprocal recommendations, such as job search and dating applications. 
相互の好みに基づいてユーザーをマッチングすることは、求人検索やデーティングアプリケーションなどの相互推薦に基づくサービスの基本的な側面です。
Although A/B tests remain the gold standard for evaluating new policies in recommender systems for matching markets, it is costly and impractical for frequent policy updates. 
**A/Bテストはマッチング市場のレコメンダーシステムにおける新しいポリシーを評価するための金標準であり続けていますが、頻繁なポリシー更新にはコストがかかり、実用的ではありません**。
Off-Policy Evaluation (OPE) thus plays a crucial role by enabling the evaluation of recommendation policies using only offline logged data naturally collected on the platform. 
したがって、オフポリシー評価（OPE）は、プラットフォーム上で自然に収集されたオフラインのログデータのみを使用して推薦ポリシーを評価できるため、重要な役割を果たします。
However, unlike conventional recommendation settings, the large scale and bidirectional nature of user interactions in matching platforms introduce variance issues and exacerbate reward sparsity, making standard OPE methods unreliable. 
しかし、従来の推薦設定とは異なり、マッチングプラットフォームにおけるユーザーインタラクションの大規模かつ双方向の性質は、分散の問題を引き起こし、報酬の希薄化を悪化させるため、標準的なOPE手法は信頼性がありません。
To address these challenges and facilitate effective offline evaluation, we propose novel OPE estimators, DiPS and DPR, specifically designed for matching markets. 
これらの課題に対処し、効果的なオフライン評価を促進するために、マッチング市場向けに特別に設計された新しいOPE推定量、DiPSおよびDPRを提案します。
Our methods combine elements of the Direct Method (DM), Inverse Propensity Score (IPS), and Doubly Robust (DR) estimators while incorporating intermediate labels, such as initial engagement signals, to achieve better bias-variance control in matching markets. 
私たちの手法は、Direct Method（DM）、Inverse Propensity Score（IPS）、およびDoubly Robust（DR）推定量の要素を組み合わせ、**初期のエンゲージメント信号などの中間ラベルを取り入れることで、マッチング市場におけるバイアス-分散制御を改善**します。
Theoretically, we derive the bias and variance of the proposed estimators and demonstrate their advantages over conventional methods. 
理論的には、提案した推定量のバイアスと分散を導出し、従来の手法に対する利点を示します。
Furthermore, we show that these estimators can be seamlessly extended to offline policy learning methods for improving recommendation policies for making more matches. 
さらに、これらの推定量は、より多くのマッチを作成するための推薦ポリシーを改善するための**オフラインポリシー学習手法にシームレスに拡張できる**ことを示します。
We empirically evaluate our methods through experiments on both synthetic data and A/B testing logs from a real job-matching platform. 
私たちは、合成データと実際の求人マッチングプラットフォームからのA/Bテストログの両方に対する実験を通じて、手法を実証的に評価します。
The empirical results highlight the superiority of our approach over existing methods in off-policy evaluation and learning tasks for a variety of configurations. 
実証結果は、さまざまな構成におけるオフポリシー評価と学習タスクにおいて、既存の手法に対する私たちのアプローチの優位性を強調しています。

<!-- ここまで読んだ! -->

## 1.Introduction 1. はじめに

Online platforms for job search and dating increasingly influence how people find employment and establish personal connections(Su etal.,2022). 
求人検索やデートのためのオンラインプラットフォームは、人々が雇用を見つけ、個人的なつながりを築く方法にますます影響を与えています(Su etal.,2022)。 
These services rely heavily on the effectiveness of recommendation policies, as user satisfaction and engagement directly depend on accurate matching(Tomita etal.,2023,2022). 
これらのサービスは、ユーザーの満足度とエンゲージメントが正確なマッチングに直接依存するため、推薦ポリシーの効果に大きく依存しています(Tomita etal.,2023,2022)。 
To help users efficiently find suitable matches, these platforms should recommend user pairs with mutual preferences. 
ユーザーが効率的に適切なマッチを見つけるために、これらのプラットフォームは相互の好みを持つユーザーペアを推薦する必要があります。
However, achieving accurate and efficient matching presents unique challenges due to the large-scale and bidirectional nature of interactions. 
しかし、**正確かつ効率的なマッチングを実現することは、相互作用の大規模かつ双方向の性質により独自の課題を呈します**。 
To address these challenges, researchers have developed recommendation methods specifically designed for matchmaking(Tomita etal.,2023; Kleinerman etal.,2018; Palomares etal.,2021). 
これらの課題に対処するために、研究者たちはマッチメイキングのために特別に設計された推薦手法を開発しました(Tomita etal.,2023; Kleinerman etal.,2018; Palomares etal.,2021)。 
To identify the most effective method for maximizing the number of matches, practitioners often rely on A/B tests. 
マッチの数を最大化するための最も効果的な方法を特定するために、**実務者はしばしばA/Bテストに依存**します。 
However, A/B tests impose substantial costs in time, resources, and risk of exposing users to suboptimal policies. 
しかし、**A/Bテストは、時間、リソース、そしてユーザーを最適でないポリシーにさらすリスクにおいて substantial costs を課します**。(substantial...!:thinking:)
Therefore, in practice, off-policy evaluation (OPE) plays a crucial role in evaluating recommender systems(Saito and Joachims,2021). 
**したがって、実際にはオフポリシー評価（OPE）が推薦システムの評価において重要な役割を果たします(Saito and Joachims,2021)**。 
OPE enables us to estimate the performance of a new policy using only interaction data naturally collected under an existing policy (e.g., the recommender system currently deployed in production)(Saito and Joachims,2021; Uehara etal.,2022). 
OPEは、既存のポリシーの下で自然に収集されたインタラクションデータのみを使用して新しいポリシーのパフォーマンスを推定することを可能にします（例：現在本番環境で展開されている推薦システム）(Saito and Joachims,2021; Uehara etal.,2022)。 
An accurate OPE pipeline allows us to identify better recommendation policies before conducting A/B tests, thereby improving efficiency of the tests by focusing only on policies already validated as promising(Dudík etal.,2014; Su etal.,2020a; Saito etal.,2024). 
正確なOPEパイプラインは、A/Bテストを実施する前により良い推薦ポリシーを特定することを可能にし、すでに有望であると検証されたポリシーにのみ焦点を当てることでテストの効率を向上させます(Dudík etal.,2014; Su etal.,2020a; Saito etal.,2024)。 

<!-- ここまで読んだ! -->

Recent advances in OPE research have led to the development of numerous estimators and policy gradient methods(Saito and Joachims,2021; Uehara etal.,2022), most of which are based on inverse propensity scoring (IPS), the direct method (DM) using reward regression, or their hybrid approach, Doubly Robust (DR)(Dudík etal.,2014; Su etal.,2020a,2019a). 
最近のOPE研究の進展により、多くの推定器やポリシー勾配法が開発されました(Saito and Joachims,2021; Uehara etal.,2022)。これらのほとんどは、逆傾向スコアリング（IPS）、報酬回帰を使用した直接法（DM）、またはそれらのハイブリッドアプローチであるDoubly Robust（DR）に基づいています(Dudík etal.,2014; Su etal.,2020a,2019a)。 
More specifically, IPS applies importance weighting to account for the distributional shift between the new and old (logging) policies, enabling an unbiased estimation of policy performance (such as the expected number of matches). 
より具体的には、IPSは重要度加重を適用して新しいポリシーと古い（ログ）ポリシーの間の分布のシフトを考慮し、ポリシーのパフォーマンス（例えば、期待されるマッチの数）のバイアスのない推定を可能にします。 
However, IPS suffers from extremely high variance, particularly when the number of actions is large or when reward feedback is sparse, both of which are common in matching platforms. 
**しかし、IPSは非常に高い分散に悩まされ、特にアクションの数が多い場合や報酬フィードバックが希薄な場合に問題となります。**これらはマッチングプラットフォームでは一般的です。 
DM, on the other hand, does not rely on importance weights but instead uses a reward regression model to estimate the policy performance. 
一方、DMは重要度加重に依存せず、報酬回帰モデルを使用してポリシーのパフォーマンスを推定します。 
As a result, DM avoids the variance issues but often introduces bias depending on the accuracy of the regression model(Jeunen and Goethals,2021). 
その結果、DMは分散の問題を回避しますが、回帰モデルの精度に応じてバイアスを導入することがよくあります(Jeunen and Goethals,2021)。 
DR combines IPS and DM, leveraging the unbiasedness of IPS and the lower variance of DM. 
DRはIPSとDMを組み合わせ、IPSのバイアスのなさとDMの低い分散を活用します。 
However, since DR still depends on importance weighting, it remains vulnerable to variance issues in cases of large action spaces, policy divergence, and noisy rewards(Saito and Joachims,2022a). 
しかし、DRは依然として重要度加重に依存しているため、**大きなアクション空間、ポリシーの乖離、ノイズの多い報酬の場合に分散の問題に脆弱**です(Saito and Joachims,2022a)。 

<!-- ここまで読んだ! -->

Although these conventional estimation strategies perform well when large amounts of logged data and dense reward observations are available, OPE in matching recommendation settings significantly deviates from these ideal conditions. 
これらの従来の推定戦略は、大量のログデータと密な報酬観測が利用可能な場合には良好に機能しますが、マッチング推薦設定におけるOPEはこれらの理想的な条件から大きく逸脱します。 
The most fundamental challenge is that a successful match (i.e., a positive reward) occurs only when both users mutually express interest. 
**最も基本的な課題は、成功したマッチ（すなわち、正の報酬）が両方のユーザーが相互に興味を示したときにのみ発生すること**です。(i.e. 報酬が希薄...!:thinking:)
Figure1illustrates an example of the reciprocal recommendation problem. 
図1は、相互推薦問題の例を示しています。 
The platform recommends a job seeker for companies, which then decide whether to send scouting messages (first-stage reward). 
プラットフォームは企業に対して求職者を推薦し、企業はスカウトメッセージを送信するかどうかを決定します（第一段階の報酬）。 
Each job seeker who receives a scout then chooses whether to respond (second-stage reward). 
スカウトを受け取った各求職者は、その後、応答するかどうかを選択します（第二段階の報酬）。 
A successful match occurs only when a job seeker responds to a scouting message. 
成功したマッチは、求職者がスカウトメッセージに応答したときにのみ発生します。 
This leads to an environment with significantly sparse reward signals, making standard OPE methods (such as IPS, DM, and DR) unreliable. 
これにより、**報酬信号が非常に希薄な環境**が生まれ、標準的なOPE手法（IPS、DM、DRなど）が信頼できなくなります。 

A particular room for improvement in existing estimators in the matching domain is their inability to leverage the first-stage rewards, such as the sending of scouting messages in the example from Figure1. 
マッチング領域における既存の推定器の改善の余地は、図1の例におけるスカウトメッセージの送信など、**第一段階の報酬を活用できないこと**です。 
These methods rely solely on sparse match labels as reward signals, leading to increased variance relative to the expected policy performance and reduced accuracy in policy evaluation and selection. 
これらの手法は、報酬信号として希薄なマッチラベルのみに依存しており、期待されるポリシーのパフォーマンスに対する分散が増加し、ポリシーの評価と選択の精度が低下します。 
To overcome, we propose two novel OPE estimators, DiPS (Direct and Propensity Score) and DPR (Direct, Propensity, and doubly Robust), specifically designed for evaluating recommendation policies in matching platforms. 
これを克服するために、私たちはマッチングプラットフォームにおける推薦ポリシーを評価するために特別に設計された**2つの新しいOPE推定器、DiPS（Direct and Propensity Score）とDPR（Direct, Propensity, and doubly Robust）を提案**します。 
They are the brand new hybrids of the existing estimators where the key idea is the explicit use of the first-stage rewards. 
これらは、既存の推定器の新しいハイブリッドであり、**重要なアイデアは第一段階の報酬を明示的に使用すること**です。 
Specifically, DiPS applies importance weighting to estimate the first-stage reward under the new policy while imputing the second-stage reward using a regression model, jointly estimating the expected number of matches. 
具体的には、DiPSは重要度加重を適用して新しいポリシーの下で第一段階の報酬を推定し、回帰モデルを使用して第二段階の報酬を補完し、期待されるマッチの数を共同で推定します。 
DPR builds on and enhances DiPS by further reducing variance, depending on the accuracy of the direct match prediction model. 
DPRはDiPSを基に構築され、直接マッチ予測モデルの精度に応じて分散をさらに減少させることで強化します。 

<!-- ここまで読んだ! -->

We conduct a theoretical analysis of our proposed estimators, demonstrating their advantages in terms of bias-variance control under the matching market formulation. 
私たちは提案した推定器の理論的分析を行い、マッチング市場の定式化におけるバイアス-分散制御の観点からの利点を示します。 
Additionally, we show how DiPS and DPR can be extended as policy gradient estimators to implement efficient off-policy learning for matchmaking systems. 
さらに、DiPSとDPRがポリシー勾配推定器として拡張され、マッチメイキングシステムのための効率的なオフポリシー学習を実装できる方法を示します。 
We finally conduct extensive empirical evaluations using both synthetic data and real-world datasets from the job-matching platform Wantedly Visit111https://www.wantedly.com. 
最後に、**合成データと求人マッチングプラットフォームWantedly Visitからの実世界のデータセットの両方を使用して広範な実証評価**を行います111https://www.wantedly.com。 
The results demonstrate that our proposed methods enable more accurate policy evaluation, selection, and learning compared to existing approaches by leveraging both the first- and second-stage rewards explicitly. 
結果は、私たちの提案した手法が第一段階と第二段階の報酬の両方を明示的に活用することにより、既存のアプローチと比較してより正確なポリシー評価、選択、学習を可能にすることを示しています。 
Our real-world experiments using production A/B testing datasets further validate that our methods improve the ability to predict real A/B testing results using only offline logged data, demonstrating their practical significance. 
本番のA/Bテストデータセットを使用した実世界の実験は、私たちの手法がオフラインのログデータのみを使用して実際の**A/Bテスト結果を予測する能力を向上**させることをさらに検証し、その実用的な重要性を示しています。 

<!-- ここまで読んだ! -->

## 2.OPE for Matching Markets

This section formally formulates the problem of OPE for matching markets. 
このセクションでは、マッチング市場におけるOPEの問題を正式に定式化します。
In particular, we consider a job-matching platform as an example, 
特に、私たちはジョブマッチングプラットフォームを例として考えます。
Note that this does not mean that our formulation is limited to this motivating example regarding the job matching problem. 
これは、私たちの定式化がジョブマッチング問題に関するこの動機付けの例に限定されるわけではないことに注意してください。
Our formulation can be applied to other matching problems such as real estate and dating platforms. 
私たちの定式化は、不動産やデーティングプラットフォームなどの他のマッチング問題にも適用できます。
where companies view job seekers recommended by a policy and send scouting requests when a job seeker aligns with their preferences. 
企業は、ポリシーによって推奨された求職者を見て、求職者が自社の好みに合致したときにスカウトリクエストを送信します。
On the job seeker’s side, they respond to these requests only if they also find the company appealing. 
求職者側では、企業が魅力的だと感じた場合にのみ、これらのリクエストに応じます。
A successful interaction, or "match", occurs when the job seeker responds positively to a scouting request, thus tending to be sparse. 
**成功したインタラクション、または「マッチ」は、求職者がスカウトリクエストに対して肯定的に応答したときに発生し、したがって希少性があります**。

Let $j \in \mathcal{J}$ be a job seeker and $c \in \mathcal{C}$ be a company index. 
$j \in \mathcal{J}$を求職者、$c \in \mathcal{C}$を企業インデックスとします。
A potentially stochastic recommendation policy $\pi(j|c)$ represents the probability of recommending job seeker $j$ to company $c$. 
潜在的に確率的な推薦ポリシー$\pi(j|c)$は、求職者$j$を企業$c$に推薦する確率を表します。
We then introduce three types of binary rewards: $s$, $r$, and $m$. 
次に、**3種類のバイナリ報酬$s$, $r$, $m$を導入**します。
The variable $s$ represents the first-stage reward, where $s=1$ if the company sends a scouting request to a job seeker and $s=0$ otherwise. 
**変数$s$は第一段階の報酬**を表し、企業が求職者にスカウトリクエストを送信した場合は$s=1$、そうでない場合は$s=0$です。
The variable $r$ represents the second-stage reward, where $r=1$ if the job seeker responds to the scouting request. 
**変数$r$は第二段階の報酬**を表し、求職者がスカウトリクエストに応答した場合は$r=1$です。
Finally, $m$ represents the ultimate reward, which takes a value of 1 only when a successful match between a company and a job seeker is observed, meaning $m=s \cdot r$. 
最後に、$m$は最終的な報酬を表し、企業と求職者の間に成功したマッチが観察されたときにのみ1の値を取ります。これは、$m=s \cdot r$を意味します。
Given a context vector $x$, we assume that these rewards are drawn from some unknown conditional distributions: $p(s|c,j)$ and $p(m|c,j,s)$. 
コンテキストベクトル $x$ が与えられたとき、これらの報酬は未知の条件付き分布 $p(s|c,j)$ および $p(m|c,j,s)$ から引き出されると仮定します。
For these reward variables, we define two types of q-functions: 
これらの報酬変数に対して、**2種類のq関数**(=期待報酬関数!)を定義します：

$$
q_s(c,j) := \mathbb{E}[s|c,j]
$$

$$
q_r(c,j) := \mathbb{E}[r|c,j,s=1]
$$

For ease of exposition, we consider only company and job seeker indices, but our formulations can be extended to incorporate their respective features, $x_c$ and $x_j$. 
説明を簡単にするために、企業と求職者のインデックスのみを考慮しますが、私たちの定式化はそれぞれの特徴 $x_c$ と $x_j$ を組み込むように拡張できます。
The function $q_s(c,j)$ represents the probability that company $c$ sends a scouting request to job seeker $j$. 
関数 $q_s(c,j)$ は、企業 $c$ が求職者 $j$ にスカウトリクエストを送信する確率(=binary報酬の期待値!)を表します。
The function $q_r(c,j)$ represents the conditional probability that job seeker $j$ responds to company $c$’s scouting request, given that $c$ has sent a scouting request to $j$. 
関数 $q_r(c,j)$ は、求職者 $j$ が企業 $c$ のスカウトリクエストに応答する条件付き確率を表し、$c$が$j$にスカウトリクエストを送信したことを前提(=条件付き!)とします。
By multiplying these two q-functions, we can ultimately define the probability of observing a successful match between $j$ and $c$ as $q_m(c,j) := q_s(c,j) \cdot q_r(c,j)$. 
これらの2つのq関数を掛け合わせることにより、$j$と$c$の間に成功したマッチを観察する確率を$q_m(c,j) := q_s(c,j) \cdot q_r(c,j)$として定義できます。

<!-- ここまで読んだ! -->

In OPE, our goal is to accurately estimate the policy value, which is defined in our work as follows: 
OPEにおいて、私たちの目標は、ポリシー値を正確に推定することであり、これは私たちの研究で次のように定義されます：

$$
V(\pi) := \frac{1}{|C|} \sum_{c \in C} \sum_{j \in J} \pi(j|c) \cdot q_m(c,j)
\tag{1}
$$

The policy value represents the expected number of matches between job seekers and companies that we obtain under the deployment of a recommendation policy $\pi$. 
ポリシー性能は、**推薦ポリシー$\pi$の展開の下で得られる求職者と企業の間のマッチの期待数**を表します。

<!-- ここまで読んだ! -->

To implement OPE, we rely on logged bandit data naturally collected under the old or logging policy $\pi_0$ (where $\pi_0 \neq \pi$), denoted as $\mathcal{D} := \{(j_c, s_c, r_c)\}_{c \in \mathcal{C}}$. 
OPEを実装するために、私たちは古いまたはロギングポリシー$\pi_0$（ここで$\pi_0 \neq \pi$）の下で自然に収集されたログバンディットデータに依存します。これは$\mathcal{D} := \{(j_c, s_c, r_c)\}_{c \in \mathcal{C}}$と表されます。
The dataset consists of $n$ independent observations drawn from the data distribution induced by the logging policy $\pi_0$. 
データセットは、ロギングポリシー$\pi_0$によって誘導されたデータ分布から引き出された $n$ 個の独立した観察から構成されます。
The data generating process is formally given by 
データ生成プロセスは正式に次のように与えられます：
(うんうん、わかる!)

$$
p(D) = \prod_{c \in  C} p(j_c, s_c, r_c | c) = \prod_{c \in C} \pi_0(j_c|c) \cdot p(s_c|c,j_c) \cdot p(r_c|c,j_c,s_c)
\tag{2}
$$

Multiple metrics exist for evaluating the accuracy of OPE estimators. 
OPE推定器の精度を評価するための複数の指標が存在します。
In this work, we mainly quantify the accuracy of an estimator $\hat{V}$ using the mean squared error (MSE): 
この研究では、**主に平均二乗誤差（MSE）を使用して推定器$\hat{V}$の精度を定量化**します：

$$
\text{MSE} = \mathbb{E}[(\hat{V}(\pi;\mathcal{D}) - V(\pi))^2]
$$

which measures the expected squared difference between the estimated value $\hat{V}(\pi;\mathcal{D})$ and the true policy value $V(\pi)$. 
これは、推定値$\hat{V}(\pi;\mathcal{D})$と真のポリシー値$V(\pi)$との間の期待される二乗差を測定します。
The MSE can be decomposed into the squared bias and variance as below. 
MSEは、以下のように二乗バイアスと分散に分解できます。

$$
\text{MSE} = \text{Bias}^2 + \text{Variance}
$$

where the bias term is defined as $\mathbb{E}[\hat{V}(\pi;\mathcal{D})] - V(\pi)$, and the variance term is given by $\mathbb{E}[(\mathbb{E}[\hat{V}(\pi;\mathcal{D})] - \hat{V}(\pi;\mathcal{D}))^2]$. 
バイアス項は$\mathbb{E}[\hat{V}(\pi;\mathcal{D})] - V(\pi)$として定義され、分散項は$\mathbb{E}[(\mathbb{E}[\hat{V}(\pi;\mathcal{D})] - \hat{V}(\pi;\mathcal{D}))^2]$として与えられます。

While MSE serves as a fundamental measure of estimator accuracy, it does not capture the practical reliability of the estimator in ranking and selecting superior policies. 
**MSEは推定器の精度の基本的な指標として機能しますが、優れたポリシーをランク付けし選択する際の推定器の実際の信頼性を捉えることはできません**。(順位づけ、っていう点ではMSEでは不十分なのか...! これはまえにusaitoさんが言ってた話か!:thinking:)
Thus, we additionally consider the Error Rate as a crucial metric, which quantifies how often an estimator misidentifies the relative value of two policies: 
したがって、私たちは**エラーレート**を重要な指標として追加で考慮します。これは、**推定器が2つのポリシーの相対的な価値を誤って識別する頻度**を定量化します：

$$
\text{Error Rate} = \text{Type I Error Rate} + \text{Type II Error Rate}
$$

The Error Rate is defined as the sum of the type-I and type-II error rates, and represents the probability of making a mistake in policy selection. 
エラーレートは、タイプIエラー率とタイプIIエラー率の合計として定義され、ポリシー選択における誤りを犯す確率を表します。
An estimator with a low MSE but a high Error Rate may still result in suboptimal policy selection. 
低いMSEを持ちながら高いエラーレートを持つ推定器は、依然として最適でないポリシー選択をもたらす可能性があります。
Therefore, it is crucial to design OPE estimators that achieve both low MSE and low Error Rate to ensure reliable policy evaluation in practice. 
したがって、**実際に信頼できるポリシー評価を確保するために、低いMSEと低いエラーレートの両方を達成するOPE推定器を設計することが重要**です。

<!-- ここまで読んだ! -->

### 2.1.典型的推定量

In the OPE literature, DM, IPS, and DR are widely used as baseline methods. 
OPE文献では、DM、IPS、およびDRがベースライン手法として広く使用されています。 
In this section, we analyze the bias and variance of these estimators under the matching market formulation. 
このセクションでは、マッチング市場の定式化におけるこれらの推定量のバイアスと分散を分析します。

#### 2.1.1.直接法 (DM)

DM estimates the policy value based on the estimation of the match probabilities $q_{m}(c,j)$ as 
DMは、マッチ確率 $q_{m}(c,j)$ の推定に基づいてポリシーの価値を推定します。

$$
\hat_{V}_{DM}(\pi;\mathcal{D}) := \frac{1}{|\mathcal{C}|} \sum_{c \in C} E_{\pi(j|c)}[\hat{q}_{m}(c,j)]
\tag{6}
$$

where $\hat{q}_{m}(c,j)$ is a prediction model for matching probabilities between $c$ and $j$ trained on $\mathcal{D}$. 
ここで、$\hat{q}_{m}(c,j)$は、$\mathcal{D}$で訓練された$c$と$j$の間のマッチ確率の**予測モデル**です。 
A key characteristic of DM is its low variance. 
DMの重要な特徴は、その低い分散です。 
However, it is highly susceptible to bias, which occurs depending on the accuracy of $\hat{q}_{m}(c,j)$. 
しかし、$\hat{q}_{m}(c,j)$の精度に依存して発生するバイアスに非常に敏感です。 
Particularly in environments with large action spaces and sparse rewards, DM produces high bias due to the difficulty of achieving accurate regression (Saito and Joachims, 2022b). 
特に、大きなアクション空間とスパースな報酬を持つ環境では、正確な回帰を達成するのが難しいため、DMは高いバイアスを生じます（Saito and Joachims, 2022b）。

<!-- ここまで読んだ! -->

#### 2.1.2.逆傾向スコアリング (IPS)

The IPS estimator, unlike DM, does not rely on prediction models. 
IPS推定量は、DMとは異なり、予測モデルに依存しません。 
Instead of modeling match probabilities directly, it applies importance weighting to correct for bias. 
マッチ確率を直接モデル化するのではなく、バイアスを修正するために重要度重み付けを適用します。 
Given logged data collected under $\pi_{0}$, IPS is defined as: 
$\pi_{0}$の下で収集されたログデータに基づいて、IPSは次のように定義されます：

$$
w(c,j) := \frac{\pi(j|c)}{\pi_{0}(j|c)}
$$
where $w(c,j)$ is called the importance weight, which plays a crucial role in correcting for the distributional shift and ensuring unbiasedness. 
ここで、$w(c,j)$は重要度重みと呼ばれ、分布のシフトを修正し、バイアスのないことを保証する上で重要な役割を果たします。 
There exist situations where the logging policy $\pi_{0}$ is unknown, and in such a circumstance, we need to estimate it by learning a supervised classifier to estimate the probabilities of observing $j$ given $c$ using the logged data $\mathcal{D}$. 
ログポリシー$\pi_{0}$が不明な状況が存在し、そのような場合には、ログデータ$\mathcal{D}$を使用して$c$が与えられたときに$j$を観測する確率を推定するために、教師あり分類器を学習して推定する必要があります。 

Unlike DM, IPS has zero bias (i.e., $\mathbb{E}_{p(\mathcal{D})}[\hat{V}_{\mathrm{IPS}}(\pi;\mathcal{D})]=V(\pi)$) under the common support condition and known logging policy: 
DMとは異なり、IPSは共通サポート条件および既知のログポリシーの下でゼロバイアスを持ちます（すなわち、$\mathbb{E}_{p(\mathcal{D})}[\hat{V}_{\mathrm{IPS}}(\pi;\mathcal{D})]=V(\pi)$）。 
which ensures the sufficient exploration by the logging policy $\pi_{0}$. 
これは、ログポリシー$\pi_{0}$による十分な探索を保証します。 
However, when the logging policy is estimated, IPS produces bias depending on the accuracy of the estimation. 
しかし、ログポリシーが推定されると、IPSは推定の精度に依存してバイアスを生じます。 
The bias of IPS under an estimated logging policy $\hat{\pi}_{0}(j|c)$ is given as 
推定されたログポリシー$\hat{\pi}_{0}(j|c)$の下でのIPSのバイアスは次のように与えられます：

$$
\mathrm{Bias}(\hat{V}_{\mathrm{IPS}}(\pi;\mathcal{D})) = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} \mathbb{E}_{\pi(j|c)}\left[\left(\frac{\pi_{0}(j|c)}{\hat{\pi}_{0}(j|c)}-1\right)q_{m}(c,j)\right]
$$
which becomes zero when $\pi_{0}(j|c)=\hat{\pi}_{0}(j|c)$. 
これは、$\pi_{0}(j|c)=\hat{\pi}_{0}(j|c)$のときにゼロになります。 
Moreover, a major limitation of IPS is its high variance, particularly when the target policy differs significantly from the logging policy or when the action space is large (Saito and Joachims, 2022a; Saito et al., 2023a; Kiyohara et al., 2024b). 
さらに、IPSの主要な制限はその高い分散であり、特にターゲットポリシーがログポリシーと大きく異なる場合やアクション空間が大きい場合に顕著です（Saito and Joachims, 2022a; Saito et al., 2023a; Kiyohara et al., 2024b）。 
More specifically, we can represent the variance of IPS under our formulation as follows. 
より具体的には、私たちの定式化の下でのIPSの分散を次のように表現できます。

The variance of the IPS estimator under the matching market formulation is represented as follows. 
マッチング市場の定式化の下でのIPS推定量の分散は次のように表現されます。

$$
\sigma_{m}^{2}(c,j) := \operatorname{Var}[m|c,j]
$$
is the conditional variance, or noise, of the match label. 
これは、マッチラベルの条件付き分散、またはノイズです。 
From the variance expression, we can see that it depends on the square and variance of the importance weight $w(c,j)$, which causes the typical variance issue of IPS. 
分散の表現から、これは重要度重み$w(c,j)$の二乗と分散に依存しており、IPSの典型的な分散の問題を引き起こします。 
This problem is further amplified under sparse reward conditions. 
この問題は、スパースな報酬条件下でさらに増幅されます。 
In such settings, reward signals become increasingly noisy relative to their expected values. 
そのような設定では、報酬信号は期待値に対してますますノイズが多くなります。 
The variance of a Bernoulli random variable $m \in \{0,1\}$ with expectation parameter $q$ is $q(1-q)$. 
期待パラメータ$q$を持つベルヌーイ確率変数$m \in \{0,1\}$の分散は$q(1-q)$です。 
The variance relative to the expectation, i.e., $\frac{q(1-q)}{q}=1-q$, increases as $q$ becomes small, which is characteristic of sparse environments. 
期待値に対する分散、すなわち、$\frac{q(1-q)}{q}=1-q$は、$q$が小さくなるにつれて増加し、これはスパースな環境の特徴です。 
Consequently, the first term in the variance, which depends on $\sigma_{m}^{2}(c,j)$, becomes particularly problematic, resulting in highly unstable estimations in OPE for matching markets. 
その結果、分散の最初の項は$\sigma_{m}^{2}(c,j)$に依存し、特に問題となり、マッチング市場におけるOPEの非常に不安定な推定を引き起こします。

#### 2.1.3.二重ロバスト (DR)

The DR estimator combines DM and IPS to leverage their respective strengths. 
DR推定量は、DMとIPSを組み合わせてそれぞれの強みを活用します。 
This approach helps remain unbiased as IPS under common support and known logging policy while controlling variance more effectively than either estimator alone. 
このアプローチは、共通サポートおよび既知のログポリシーの下でIPSのようにバイアスを持たず、かつ、いずれかの推定量単独よりも効果的に分散を制御します。 
The form of the estimator is specifically given by: 
推定量の形式は次のように具体的に与えられます：

$$
\Delta_{q_{m},\hat{q}_{m}}(c,j) := q_{m}(c,j) - \hat{q}_{m}(c,j)
$$
is an estimation error of the match probability estimator $\hat{q}_{m}(c,j)$. 
これは、マッチ確率推定量$\hat{q}_{m}(c,j)$の推定誤差です。 
We can see from the variance expression of DR that the second term is dependent on the accuracy of the q-function estimator, i.e., $\Delta_{q_{m},\hat{q}_{m}}(c,j)$, which is expected to be small compared to the original q-function $q_{m}(c,j)$ unless the match probability estimation $\hat{q}_{m}(c,j)$ is highly inaccurate. 
DRの分散表現から、第二項はq関数推定量の精度に依存していることがわかります。すなわち、$\Delta_{q_{m},\hat{q}_{m}}(c,j)$は、マッチ確率推定$\hat{q}_{m}(c,j)$が非常に不正確でない限り、元のq関数$q_{m}(c,j)$に比べて小さいことが期待されます。 
However, as previously discussed, sparse rewards negatively affect the first term in the variance expression, which remains unchanged for DR as well. 
しかし、前述のように、スパースな報酬は分散表現の最初の項に悪影響を及ぼし、DRでも変わりません。 
Sparse rewards also make it difficult to learn an accurate $\hat{q}_{m}(c,j)$, limiting the variance reduction advantage. 
スパースな報酬は、正確な$\hat{q}_{m}(c,j)$を学習することを困難にし、分散削減の利点を制限します。 
Consequently, despite its theoretical benefits against IPS, DR can suffer from high MSE when applied to the evaluation of recommender systems in matching markets. 
その結果、IPSに対する理論的な利点にもかかわらず、DRはマッチング市場におけるレコメンダーシステムの評価に適用されると高いMSEに苦しむ可能性があります。



## 3.RELATED WORK 関連研究

This section summarizes key related studies.  
このセクションでは、主要な関連研究を要約します。

##### Reciprocal Recommender System 相互推薦システム

A reciprocal recommender system is highly effective in domains where bidirectional preferences play a crucial role, such as matching platforms(Yang etal.,2024).  
相互推薦システムは、マッチングプラットフォームのように双方向の嗜好が重要な役割を果たす領域で非常に効果的です（Yang etal.,2024）。  
In particular, reciprocal recommendation approaches are widely used in dating services(Li and Li,2012; Tu etal.,2014; Pizzato etal.,2010; Neve and Palomares,2019; Luo etal.,2020; Xia etal.,2015)and job-matching platforms(Chen etal.,2023; Hu etal.,2023; Yıldırım etal.,2021; Goda etal.,2024; Mine etal.,2013; Su etal.,2022).  
特に、相互推薦アプローチは、デーティングサービス（Li and Li,2012; Tu etal.,2014; Pizzato etal.,2010; Neve and Palomares,2019; Luo etal.,2020; Xia etal.,2015）や求人マッチングプラットフォーム（Chen etal.,2023; Hu etal.,2023; Yıldırım etal.,2021; Goda etal.,2024; Mine etal.,2013; Su etal.,2022）で広く使用されています。

Various architectures for reciprocal recommender systems have been proposed.  
相互推薦システムのためのさまざまなアーキテクチャが提案されています。  
A well-known approach is training two separate models to predict preferences in each direction and then aggregating their predictions using functions such as the harmonic mean.  
よく知られたアプローチは、各方向の嗜好を予測するために2つの別々のモデルを訓練し、その後、調和平均のような関数を使用して予測を集約することです。  
More recently, deep learning techniques have been employed to capture the complex preferences of both parties more accurately(Yıldırım etal.,2021).  
最近では、深層学習技術が両者の複雑な嗜好をより正確に捉えるために使用されています（Yıldırım etal.,2021）。  
Additionally, methods based on Graph Neural Networks(Lai etal.,2024; Liu etal.,2024; Luo etal.,2020)have been explored to enhance recommendation performance.  
さらに、Graph Neural Networksに基づく手法（Lai etal.,2024; Liu etal.,2024; Luo etal.,2020）が推薦性能を向上させるために探求されています。  
Some studies have also formulated reciprocal recommendation within the framework of sequential recommendation to better model dynamic user preferences(Zheng etal.,2023).  
いくつかの研究では、動的なユーザの嗜好をより良くモデル化するために、逐次推薦の枠組みの中で相互推薦を定式化しています（Zheng etal.,2023）。

Our primary focus is not on developing algorithms for reciprocal recommender systems but on formulating and designing accurate methods for off-policy evaluation in matching markets for the first time.  
私たちの主な焦点は、相互推薦システムのためのアルゴリズムを開発することではなく、マッチング市場におけるオフポリシー評価のための正確な手法を初めて定式化し設計することです。  
By leveraging our methods, practitioners working on reciprocal recommender systems will be able to reliably identify the most suitable algorithms among the many proposed in academia, using only their offline logged interactions.  
私たちの手法を活用することで、相互推薦システムに取り組む実務者は、学術界で提案された多くのアルゴリズムの中から、オフラインで記録されたインタラクションのみを使用して、最も適切なアルゴリズムを信頼性を持って特定できるようになります。

##### Off-Policy Evaluation and Learning オフポリシー評価と学習

Off-policy evaluation (OPE) and learning (OPL) have gained particular attention in contextual bandit and reinforcement learning settings as they offer a safe and cost-efficient alternative to online A/B tests(Mehrotra etal.,2018; Gilotte etal.,2018; Saito etal.,2021; Kiyohara etal.,2024a).  
オフポリシー評価（OPE）と学習（OPL）は、文脈バンディットや強化学習の設定で特に注目を集めており、オンラインA/Bテストに対する安全でコスト効率の良い代替手段を提供します（Mehrotra etal.,2018; Gilotte etal.,2018; Saito etal.,2021; Kiyohara etal.,2024a）。

Numerous OPE methods have been extensively studied(Su etal.,2020b,2019b; Lichtenberg etal.,2023)to enable accurate evaluation of decision-making policies.  
多くのOPE手法が広範に研究されており（Su etal.,2020b,2019b; Lichtenberg etal.,2023）、意思決定ポリシーの正確な評価を可能にしています。  
However, the reward prediction model in DM and the importance weights in IPS can become unstable under certain conditions such as less data, noisy rewards, and large action spaces, preventing them from being effective in the matching market setup.  
しかし、DMにおける報酬予測モデルやIPSにおける重要度重みは、データが少ない、報酬がノイズを含む、大きなアクション空間などの特定の条件下で不安定になる可能性があり、マッチング市場の設定で効果的であることを妨げます。  
Recent efforts have reduced MSE by decreasing bias in the DM term(Farajtabar etal.,2018; Kang and Schafer,2007; Thomas and Brunskill,2016), reducing variance in importance weighting(Bembom and vander Laan,2008; Wang etal.,2017; Lichtenberg etal.,2023; Saito and Joachims,2022a; Shimizu etal.,2024; Metelli etal.,2021; Saito etal.,2023b), or combining multiple estimators(Wang etal.,2017; Farajtabar etal.,2018).  
最近の取り組みでは、DM項のバイアスを減少させることによってMSEを削減したり（Farajtabar etal.,2018; Kang and Schafer,2007; Thomas and Brunskill,2016）、重要度重み付けの分散を減少させたり（Bembom and vander Laan,2008; Wang etal.,2017; Lichtenberg etal.,2023; Saito and Joachims,2022a; Shimizu etal.,2024; Metelli etal.,2021; Saito etal.,2023b）、または複数の推定量を組み合わせたりしています（Wang etal.,2017; Farajtabar etal.,2018）。

A straightforward approach to mitigating the issue of exploding importance weights is called clipping, which restricts the maximum value of the weights to a predefined threshold(Bembom and vander Laan,2008; Su etal.,2019b).  
重要度重みの爆発問題を緩和するための簡単なアプローチはクリッピングと呼ばれ、重みの最大値を事前に定義された閾値に制限します（Bembom and vander Laan,2008; Su etal.,2019b）。  
While this method effectively reduces variance coming from the variation of the importance weights, it introduces bias and does not directly deal with the sparsity of the reward.  
この方法は、重要度重みの変動から生じる分散を効果的に減少させますが、バイアスを導入し、報酬のスパース性に直接対処するものではありません。  
Saito and Joachims (2022a)introduced the marginalized importance weight as a technique to substantially reduce variance compared to conventional IPS leveraging embeddings in the action space.  
SaitoとJoachims（2022a）は、アクション空間における埋め込みを活用して、従来のIPSと比較して分散を大幅に減少させる技術として、周辺重要度重みを導入しました。  
The Switch-DR estimator(Wang etal.,2017)smoothly interpolates between DM and DR via a hyperparameter $\lambda$, allowing for the mitigation of excessive MSE growth by appropriately tuning the parameter.  
Switch-DR推定量（Wang etal.,2017）は、ハイパーパラメータ $\lambda$ を介してDMとDRの間を滑らかに補間し、パラメータを適切に調整することで過剰なMSEの成長を緩和します。  
Even though we focus on DM, IPS, and DR as the baseline estimators, Appendix A demonstrates that we can readily extend our methods to improve more sophisticated estimators such as Switch-DR(Wang etal.,2017)and MIPS(Saito and Joachims,2022a)as well.  
私たちはDM、IPS、DRを基準推定量として焦点を当てていますが、付録Aでは、Switch-DR（Wang etal.,2017）やMIPS（Saito and Joachims,2022a）などのより洗練された推定量を改善するために、私たちの手法を容易に拡張できることを示しています。

When learning new policies offline, these OPE estimators serve as estimators for the policy gradient(Saito and Joachims,2021).  
新しいポリシーをオフラインで学習する際、これらのOPE推定量はポリシー勾配の推定量として機能します（Saito and Joachims,2021）。  
By performing iterative gradient ascents based on an estimated policy gradient, we can learn effective policies in ideal scenarios, such as when logged data is abundant, rewards are densely observed, and the action space is relatively small(Jeunen and Goethals,2021; Liang and Vlassis,2022).  
推定されたポリシー勾配に基づいて反復的な勾配上昇を行うことで、記録されたデータが豊富で、報酬が密に観察され、アクション空間が比較的小さい理想的なシナリオで効果的なポリシーを学習できます（Jeunen and Goethals,2021; Liang and Vlassis,2022）。  
However, under those challenging scenarios, estimation of the policy gradient becomes unstable, causing performance lag in OPL as well as OPE.  
しかし、これらの困難なシナリオでは、ポリシー勾配の推定が不安定になり、OPLおよびOPEのパフォーマンスに遅延を引き起こします。  
To the best of our knowledge, no prior research has explicitly addressed the challenges of OPE and OPL in matching markets.  
私たちの知る限り、これまでの研究でマッチング市場におけるOPEおよびOPLの課題に明示的に対処したものはありません。  
This work takes the first step by formulating the problems of OPE and OPL for matching markets and discussing the limitations of directly applying existing methods.  
この研究は、マッチング市場におけるOPEおよびOPLの問題を定式化し、既存の手法を直接適用することの限界について議論することで、第一歩を踏み出します。  
We also develop highly effective methods for OPE and OPL that explicitly leverage first-stage rewards that we can observe in matching markets and provide both theoretical and empirical analyses of their effectiveness.  
また、マッチング市場で観察できる第一段階の報酬を明示的に活用するOPEおよびOPLの非常に効果的な手法を開発し、その有効性について理論的および実証的な分析を提供します。



## 4. 提案手法

In the previous sections, we observed that typical estimators in OPE do not account for the bidirectional nature and reward sparsity of matching platforms. 
前のセクションでは、OPEにおける典型的な推定器がマッチングプラットフォームの双方向性と報酬の希薄性を考慮していないことを観察しました。 
To address these limitations, we explicitly leverage the useful structure of matching platforms, specifically the existence of first-stage rewards $s_s$, not just the ultimate rewards $m_m$.
これらの制限に対処するために、私たちはマッチングプラットフォームの有用な構造、特に最初の段階の報酬$s_s$の存在を明示的に活用し、最終的な報酬$m_m$だけではなくします。



### 4.1. DiPS推定量

We first propose the DiPS estimator, a novel hybrid of the DM and IPS estimators, specifically designed for the matching problem.  
まず、マッチング問題に特化して設計されたDMとIPS推定量の新しいハイブリッドであるDiPS推定量を提案します。

More specifically, DiPS estimates the expected first-stage reward $q_s(c,j)$ (e.g., the probability of company $c$ sending a scouting request to job seeker $j$) by applying IPS to the first-stage reward observations $s$, achieving its unbiased estimate.  
より具体的には、DiPSは、第一段階の報酬観測値$s$にIPSを適用することによって、期待される第一段階の報酬$q_s(c,j)$（例えば、企業$c$が求職者$j$にスカウトリクエストを送信する確率）を推定し、その無偏推定を達成します。

For the second-stage reward, DiPS relies on a reward regression model $\hat{q}_r(c,j)$ trained on offline logged data $\mathcal{D}$, similarly to DM.  
第二段階の報酬については、DiPSは、DMと同様に、オフラインのログデータ$\mathcal{D}$で訓練された報酬回帰モデル$\hat{q}_r(c,j)$に依存します。

By employing this novel hybrid approach, DiPS avoids fully applying IPS to the sparse match label $m$, thereby mitigating the variance problem.  
この新しいハイブリッドアプローチを採用することで、DiPSはスパースマッチラベル$m$にIPSを完全に適用することを避け、分散の問題を軽減します。

At the same time, it does not rely entirely on DM, preventing potential bias issues.  
同時に、DMに完全に依存することもなく、潜在的なバイアスの問題を防ぎます。

The DiPS estimator is rigorously defined as follows:  
DiPS推定量は次のように厳密に定義されます：

$$
w(c,j) := \frac{\pi(j|c)}{\pi_0(j|c)}
$$  
$$
w(c,j) := \frac{\pi(j|c)}{\pi_0(j|c)} 
$$

is the same importance weight used in IPS and DR.  
これは、IPSおよびDRで使用されるのと同じ重要度重みです。

As in Eq.(12), the DiPS estimator estimates the expected first-stage reward function by applying IPS to the first-stage labels $s$.  
式(12)のように、DiPS推定量は第一段階のラベル$s$にIPSを適用することによって期待される第一段階の報酬関数を推定します。

It then estimates the expected second-stage reward using the reward model $\hat{q}_r(c,j_c)$.  
次に、報酬モデル$\hat{q}_r(c,j_c)$を使用して期待される第二段階の報酬を推定します。

By leveraging IPS and DM to estimate different stages of the rewards, DiPS achieves desirable bias-variance control in matching markets compared to typical estimators.  
IPSとDMを活用して報酬の異なる段階を推定することにより、DiPSは典型的な推定量と比較してマッチング市場における望ましいバイアス-分散制御を達成します。

We first analyze the bias of the DiPS estimator as follows.  
まず、DiPS推定量のバイアスを次のように分析します。

The bias of the DiPS estimator under the matching market formulation is represented by the following equation:  
マッチング市場の定式化におけるDiPS推定量のバイアスは、次の式で表されます：

$$
\Delta_{q_r,\hat{q}_r}(c,j) := \hat{q}_r(c,j) - q_r(c,j)
$$  
$$
\Delta_{q_r,\hat{q}_r}(c,j) := \hat{q}_r(c,j) - q_r(c,j)
$$

is an estimation error of the expected second-stage reward estimator $\hat{q}_r(c,j)$.  
これは、期待される第二段階の報酬推定量$\hat{q}_r(c,j)$の推定誤差です。

The bias analysis suggests that the bias of DiPS is characterized by the estimation error of the prediction model for the second-stage reward, $\hat{q}_r(c,j)$.  
バイアス分析は、DiPSのバイアスが第二段階の報酬の予測モデル$\hat{q}_r(c,j)$の推定誤差によって特徴付けられることを示唆しています。

This is reasonable because DiPS provides an unbiased estimate of the first-stage reward by applying importance weighting, leaving bias only in the second-stage reward estimation.  
これは、DiPSが重要度重み付けを適用することによって第一段階の報酬の無偏推定を提供し、第二段階の報酬推定にのみバイアスを残すため、合理的です。

This bias is expected to be smaller than that of DM since it directly estimates the match probability $q_m(c,j)$, which is highly sparse and difficult to estimate accurately.  
このバイアスは、非常にスパースで正確に推定するのが難しいマッチ確率$q_m(c,j)$を直接推定するため、DMのそれよりも小さいと予想されます。

Next, the following analyzes the bias of DiPS under an estimated logging policy $\hat{\pi}_0(j|c)$.  
次に、推定されたログポリシー$\hat{\pi}_0(j|c)$の下でのDiPSのバイアスを分析します。

The bias of the DiPS estimator with an estimated logging policy $\hat{\pi}_0(j|c)$ is represented by the following equation:  
推定されたログポリシー$\hat{\pi}_0(j|c)$を持つDiPS推定量のバイアスは、次の式で表されます：

$$
\text{(14)}
$$

Comparing Eq.(14) to the bias of IPS in Eq.(8), it is interesting that the bias of DiPS can be smaller than that of IPS when the estimation errors against $\pi_0(j|c)$ and $q_r(c,j)$ are positively correlated.  
式(14)を式(8)のIPSのバイアスと比較すると、DiPSのバイアスがIPSのそれよりも小さくなることが興味深いのは、$\pi_0(j|c)$および$q_r(c,j)$に対する推定誤差が正の相関を持つ場合です。

We then derive the variance of the DiPS estimator.  
次に、DiPS推定量の分散を導出します。

The variance of the DiPS estimator under the matching market formulation is given as follows:  
マッチング市場の定式化におけるDiPS推定量の分散は次のように与えられます：

$$
\sigma_s^2(c,j) := \operatorname{Var}[s|c,j]
$$  
$$
\sigma_s^2(c,j) := \operatorname{Var}[s|c,j]
$$

is the conditional variance of the first-stage reward.  
これは第一段階の報酬の条件付き分散です。

Analogous to the variance expression of IPS, the first term in the DiPS variance captures the contribution from the importance weights.  
IPSの分散表現と類似して、DiPSの分散の最初の項は重要度重みからの寄与を捉えます。

A key distinction, however, lies in the fact that the variance in DiPS depends on the noise in the first-stage reward, denoted by $\sigma_s^2(c,j)$, scaled by the square of the second-stage reward model, $\hat{q}_r^2(c,j)$.  
しかし、重要な違いは、DiPSの分散が第一段階の報酬のノイズ$\sigma_s^2(c,j)$に依存し、第二段階の報酬モデル$\hat{q}_r^2(c,j)$の二乗でスケーリングされるという点です。

This quantity is generally smaller than the noise in the sparse match label, $\sigma_m^2(c,j)$, which appears in the IPS variance.  
この量は、IPSの分散に現れるスパースマッチラベルのノイズ$\sigma_m^2(c,j)$よりも一般的に小さいです。

The DiPS estimator reduces the variance by at least the following amount compared to IPS, if the second-stage reward estimator is not overestimating, i.e., $\hat{q}_r(c,j) \leq q_r(c,j), \forall (c,j)$.  
DiPS推定量は、第二段階の報酬推定量が過大評価されていない場合、すなわち、$\hat{q}_r(c,j) \leq q_r(c,j), \forall (c,j)$に対して、IPSと比較して少なくとも次の量だけ分散を減少させます。

$$
\text{(16)}
$$

The theorem indicates that DiPS generally achieves lower variance than IPS.  
この定理は、DiPSが一般的にIPSよりも低い分散を達成することを示しています。

It is intriguing that the variance reduction achieved by DiPS becomes particularly large when the square of the importance weight $w^2(c,j)$, the expected first-stage reward $q_s(c,j)$, and the noise in the second-stage reward $\sigma_r^2(c,j)$ are large.  
DiPSによって達成される分散の減少が、重要度重みの二乗$w^2(c,j)$、期待される第一段階の報酬$q_s(c,j)$、および第二段階の報酬のノイズ$\sigma_r^2(c,j)$が大きいときに特に大きくなることは興味深いです。

This highlights a particularly advantageous property of DiPS in challenging scenarios of large action spaces or significant policy divergence.  
これは、大きなアクション空間や重要なポリシーの乖離のある困難なシナリオにおけるDiPSの特に有利な特性を強調しています。



### 4.2. The DPR Estimator

The previous section introduced DiPS as a new hybrid approach that explicitly leverages the first-stage reward in the matching market setup. 
前のセクションでは、マッチング市場の設定において第一段階の報酬を明示的に活用する新しいハイブリッドアプローチとしてDiPSを紹介しました。

This section further extends DiPS by incorporating a model for the expected match probability, $\hat{q}_{m}(c,j)$, originally used in DM and DR, to achieve even better bias-variance control. 
このセクションでは、DMおよびDRで元々使用されていた期待マッチ確率のモデル$\hat{q}_{m}(c,j)$を組み込むことにより、DiPSをさらに拡張し、バイアス-バリアンス制御をより良く達成します。

The following formulation realizes this idea, defining the new DPR estimator: 
以下の定式化はこのアイデアを実現し、新しいDPR推定量を定義します：

$$
\text{DPR Estimator}
$$

which explicitly incorporates the first-stage reward and leverages both the prediction models for the expected second-stage reward and ultimate reward, $\hat{q}_{r}(c,j)$ and $\hat{q}_{m}(c,j)$. 
これは第一段階の報酬を明示的に組み込み、期待される第二段階の報酬と最終的な報酬の予測モデル$\hat{q}_{r}(c,j)$および$\hat{q}_{m}(c,j)$の両方を活用します。

An interesting interpretation of DPR is that it extends DiPS by the same fundamental idea as DR yet additionally leveraging the first-stage rewards $s$. 
DPRの興味深い解釈は、DRと同じ基本的なアイデアでDiPSを拡張し、さらに第一段階の報酬$s$を活用することです。

The following analyzes the key statistical properties of DPR. 
以下では、DPRの主要な統計的特性を分析します。

The bias of the DPR estimator under the matching market formulation is derived as follows. 
マッチング市場の定式化におけるDPR推定量のバイアスは以下のように導出されます。

The bias of the DPR estimator under the matching market formulation is derived as follows. 
マッチング市場の定式化におけるDPR推定量のバイアスは以下のように導出されます。

$$
\text{Bias of DPR Estimator}
$$

The above theorem suggests that, theoretically, DPR produces exactly the same bias as DiPS. 
上記の定理は、理論的にはDPRがDiPSと全く同じバイアスを生成することを示唆しています。

This result is reasonable because DPR incorporates the additional reward model $\hat{q}_{m}(c,j)$, similar to DR, in a way that does not introduce additional bias. 
この結果は妥当であり、DPRがDRと同様に追加の報酬モデル$\hat{q}_{m}(c,j)$を組み込んでいるため、追加のバイアスを導入しない方法であるからです。

Next, we analyze the variance of DPR. 
次に、DPRの分散を分析します。

The variance of the DPR estimator under the matching market formulation is derived as follows. 
マッチング市場の定式化におけるDPR推定量の分散は以下のように導出されます。

The variance of the DPR estimator under the matching market formulation is derived as follows. 
マッチング市場の定式化におけるDPR推定量の分散は以下のように導出されます。

$$
\text{Variance of DPR Estimator}
$$

It is interesting that the second term in the variance expression of DPR is characterized by the estimation error of the model $\hat{q}_{r}(c,j)$, i.e., $\Delta_{q_{r},\hat{q}_{r}}(c,j)$, as opposed to $q_{r}(c,j)$ in DiPS. 
DPRの分散表現における第二項は、モデル$\hat{q}_{r}(c,j)$の推定誤差、すなわち$\Delta_{q_{r},\hat{q}_{r}}(c,j)$によって特徴付けられることが興味深いです。これはDiPSの$q_{r}(c,j)$とは対照的です。

Therefore, as long as the prediction model for the second-stage reward is reasonably accurate, DPR produces lower variance than DiPS. 
したがって、第二段階の報酬の予測モデルが合理的に正確である限り、DPRはDiPSよりも低い分散を生成します。



### 4.3. マッチング市場のためのOPLへの拡張

In addition to the OPE counterpart, we can formulate the problem of learning a new policy for matchmaking to optimize the expected reward as $\max_{\theta}V(\pi_{\theta})$ where $\theta \in \mathbb{R}^{d}$ is the policy parameter. 
OPEの対応物に加えて、期待報酬を最適化するためのマッチメイキングの新しいポリシーを学習する問題を、$\max_{\theta}V(\pi_{\theta})$として定式化できます。ここで、$\theta \in \mathbb{R}^{d}$はポリシーのパラメータです。

A common approach to solving this policy learning problem is the policy-based method, which updates the policy parameter iteratively using gradient ascent: $\theta_{t+1} \leftarrow \theta_{t} + \eta \cdot \nabla_{\theta}V(\pi_{\theta})$ where $\eta > 0$ is the learning rate. 
このポリシー学習問題を解決する一般的なアプローチは、ポリシーベースの手法であり、勾配上昇を使用してポリシーパラメータを反復的に更新します：$\theta_{t+1} \leftarrow \theta_{t} + \eta \cdot \nabla_{\theta}V(\pi_{\theta})$、ここで$\eta > 0$は学習率です。

Since the true gradient is unknown, it must be estimated from logged data. 
真の勾配は未知であるため、ログデータから推定する必要があります。

This estimation has been addressed in the existing literature by applying DM, IPS, or DR estimators (Su et al., 2019a; Metelli et al., 2021). 
この推定は、既存の文献でDM、IPS、またはDR推定量を適用することによって対処されています（Su et al., 2019a; Metelli et al., 2021）。

However, similar to OPE for matching markets, policy gradient estimators based on these conventional methods suffer from either bias or high variance in our problem. 
しかし、マッチング市場のOPEと同様に、これらの従来の手法に基づくポリシー勾配推定量は、私たちの問題においてバイアスまたは高い分散のいずれかに悩まされます。

To address these challenges in OPL for matching markets, the following extends DiPS to serve as a policy gradient estimator to optimize the policy value using logged data. 
マッチング市場のOPLにおけるこれらの課題に対処するために、以下はDiPSを拡張して、ログデータを使用してポリシー値を最適化するポリシー勾配推定量として機能します。

$$
s_{\theta}(c,j) := \nabla_{\theta}\log\pi_{\theta}(j|c)
$$
where $s_{\theta}(c,j)$ is the policy score function. 
ここで、$s_{\theta}(c,j)$はポリシースコア関数です。

Note that the policy gradient estimator based on DPR can similarly be defined, and is described in the appendix. 
DPRに基づくポリシー勾配推定量も同様に定義でき、付録に記載されています。

As discussed earlier, the policy gradient estimator in Eq. (20) explicitly incorporates first-stage rewards. 
前述のように、式(20)のポリシー勾配推定量は、第一段階の報酬を明示的に組み込んでいます。

By following the same theoretical reasoning as in the OPE setting, our proposed gradient estimators achieve more efficient OPL for matching markets enjoying better bias-variance control in the gradient estimation. 
OPEの設定と同じ理論的理由に従うことで、私たちの提案した勾配推定量は、勾配推定においてより良いバイアス-分散制御を享受し、マッチング市場のためのより効率的なOPLを実現します。



## 5. 合成データ実験

This section empirically evaluates the proposed methods using synthetic datasets for a variety of situations.
このセクションでは、さまざまな状況に対して合成データセットを使用して提案された方法を実証的に評価します。

##### セットアップ
To generate synthetic data, we begin with characterizing companies ($c \in \mathcal{C}$) and job seekers ($j \in \mathcal{J}$), each by 10-dimensional context vectors ($x_c$ and $x_j$), sampled from the standard normal distribution.
合成データを生成するために、まず企業（$c \in \mathcal{C}$）と求職者（$j \in \mathcal{J}$）をそれぞれ10次元のコンテキストベクトル（$x_c$ と $x_j$）で特徴付け、標準正規分布からサンプリングします。

We then synthesize the first- and second-stage expected reward functions using non-linear transformations as follows:
次に、非線形変換を使用して第一段階および第二段階の期待報酬関数を合成します。

where $\mathrm{sigmoid}(x)$ denotes the sigmoid function, defined as $\frac{1}{1+\exp(-x)}$.
ここで、$\mathrm{sigmoid}(x)$ はシグモイド関数を示し、$\frac{1}{1+\exp(-x)}$ と定義されます。

These reward functions are parameterized by matrices and vectors $M_s$, $M_r$, $\theta_s$, and $\theta_r$, all of which are sampled from the standard normal distribution.
これらの報酬関数は、行列 $M_s$, $M_r$ とベクトル $\theta_s$, $\theta_r$ によってパラメータ化され、すべて標準正規分布からサンプリングされます。

The experimental parameter $\theta_{sp}$ controls the sparsity of rewards, and $b_s$ and $b_r$ are sampled from a uniform distribution over the range $[0,2]$.
実験パラメータ $\theta_{sp}$ は報酬のスパース性を制御し、$b_s$ と $b_r$ は範囲 $[0,2]$ の一様分布からサンプリングされます。

Note that the expected match probability between $c$ and $j$ is defined as $q_m(c,j) = q_s(c,j) \cdot q_r(c,j)$.
$c$ と $j$ の間の期待マッチ確率は $q_m(c,j) = q_s(c,j) \cdot q_r(c,j)$ と定義されることに注意してください。

We construct the logging policy $\pi_0$ by applying the softmax function to $q_m(c,j)$ as
ログポリシー $\pi_0$ は、$q_m(c,j)$ にソフトマックス関数を適用することによって構築されます。

$$
\pi_0(j|c) = \frac{\exp(q_m(c,j)/\beta)}{\sum_{j' \in \mathcal{J}} \exp(q_m(c,j')/\beta)}
$$

where $\beta$ is an experimental parameter that controls the optimality and entropy of the logging policy.
ここで、$\beta$ はログポリシーの最適性とエントロピーを制御する実験パラメータです。

We set $\beta = -0.5$ by default.
デフォルトでは $\beta = -0.5$ に設定します。

In contrast, we define the target policy $\pi(j|c)$ using an epsilon-greedy strategy:
対照的に、ターゲットポリシー $\pi(j|c)$ はエプシロン-グリーディ戦略を使用して定義します。

where $\epsilon \in [0,1]$ controls the level of randomness in $\pi(j|c)$.
ここで、$\epsilon \in [0,1]$ は $\pi(j|c)$ のランダム性のレベルを制御します。

We set $\epsilon = 0.2$ by default.
デフォルトでは $\epsilon = 0.2$ に設定します。

##### 結果
In our experiments on the evaluation task, we compared the MSE and ErrorRate of DiPS and DPR against DM, IPS, and DR, which serve as baseline estimators.
評価タスクに関する実験では、DiPS と DPR の MSE と ErrorRate を、基準推定器として機能する DM、IPS、および DR と比較しました。

We also conducted experiments on the learning task, where we compared the policy value of policies learned using DiPS-PG and DPR-PG against DM-PG, IPS-PG, and DR-PG as baselines (PG stands for Policy Gradient).
また、学習タスクに関する実験も行い、DiPS-PG と DPR-PG を使用して学習したポリシーのポリシー値を、基準として DM-PG、IPS-PG、および DR-PG と比較しました（PG はポリシー勾配を意味します）。

We performed both OPE and OPL experiments by varying the number of companies, the number of job seekers, and reward sparsity parameters.
企業の数、求職者の数、および報酬のスパース性パラメータを変化させることによって、OPE と OPL の両方の実験を実施しました。

The results are presented in Figures 2 to 4.
結果は図 2 から 4 に示されています。

First, we vary the number of companies (i.e., size of the logged data $|\mathcal{D}|$) in Figure 2.
まず、図 2 で企業の数（すなわち、ログデータのサイズ $|\mathcal{D}|$）を変化させます。

The figure shows that every estimator except DM shows a decrease in MSE and variance as the number of companies increases, which is expected.
この図は、DM を除くすべての推定器が企業の数が増えるにつれて MSE と分散が減少することを示しており、これは予想される結果です。

In particular, both DiPS and DPR achieve significantly lower MSE than the baseline methods across most experimental configurations.
特に、DiPS と DPR はほとんどの実験設定において基準方法よりも著しく低い MSE を達成します。

More specifically, they achieve much lower variance than IPS and DR while introducing slightly higher bias due to their reliance on the estimated second-stage reward function, which aligns with our theoretical analysis.
より具体的には、彼らは推定された第二段階の報酬関数に依存するため、IPS および DR よりもはるかに低い分散を達成しますが、わずかに高いバイアスを導入します。これは私たちの理論的分析と一致します。

This improvement in MSE for OPE translates to better performance in policy selection tasks (ErrorRate) for DiPS and DPR as well.
OPE における MSE の改善は、DiPS と DPR にとってポリシー選択タスク（ErrorRate）でのパフォーマンス向上につながります。

Next, we vary the number of job seekers (i.e., size of the action space) in Figure 3.
次に、図 3 で求職者の数（すなわち、アクション空間のサイズ）を変化させます。

The results demonstrate the greater robustness of DiPS and DPR in larger action spaces, primarily due to substantial variance reduction compared to IPS and DR.
結果は、主に IPS および DR に比べて大幅な分散削減により、より大きなアクション空間における DiPS と DPR のより大きなロバスト性を示しています。

In particular, for larger action spaces, IPS and DR, which heavily depend on importance weighting, produce substantial variance, whereas DiPS and DPR mitigate this issue at the cost of introducing a small amount of bias by estimating the second-stage q-function by a regression model.
特に、より大きなアクション空間では、重要度重み付けに大きく依存する IPS および DR が大幅な分散を生じるのに対し、DiPS および DPR は回帰モデルによって第二段階の q 関数を推定することでわずかなバイアスを導入する代償でこの問題を軽減します。

Moreover, the bias introduced by DiPS and DPR remains significantly smaller than that of DM, consistently leading to lower MSE against it.
さらに、DiPS および DPR によって導入されるバイアスは DM のそれよりも著しく小さく、常にそれに対して低い MSE につながります。

Similar to the previous experiment, improved estimation accuracy, particularly for larger numbers of job seekers, results in better policy selection performance (lower ErrorRate) for DiPS and DPR compared to the baseline methods.
前の実験と同様に、特により多くの求職者に対する推定精度の向上は、基準方法に対して DiPS と DPR のポリシー選択パフォーマンス（低い ErrorRate）を向上させます。

We also evaluated the performance of the estimators while varying the sparsity of match labels in Figure 4.
図 4 では、マッチラベルのスパース性を変化させながら推定器の性能を評価しました。

As sparsity increases, estimating the match probability function $q_m(c,j)$ becomes more challenging, leading to higher MSE for DM.
スパース性が増すにつれて、マッチ確率関数 $q_m(c,j)$ の推定がより困難になり、DM の MSE が高くなります。

Since DiPS and DPR do not rely solely on the match prediction model as DM does, they perform significantly better across a range of sparsity configurations.
DiPS と DPR は DM のようにマッチ予測モデルにのみ依存しないため、さまざまなスパース性設定において著しく良い性能を発揮します。

Additionally, DiPS and DPR consistently outperform IPS and DR due to the substantial variance reduction achieved by explicitly leveraging the two-stage reward structure.
さらに、DiPS と DPR は、二段階の報酬構造を明示的に活用することによって達成される大幅な分散削減により、IPS および DR を常に上回ります。

This also results in a lower ErrorRate in the selection task across various sparsity levels.
これにより、さまざまなスパース性レベルにおける選択タスクでの ErrorRate が低下します。

Finally, we compare the effectiveness of each estimator in policy learning when used for policy gradient estimation in Figure 7 in the appendix.
最後に、付録の図 7 でポリシー勾配推定に使用される各推定器のポリシー学習における効果を比較します。

The figures show the resulting policy values relative to that of the logging policy $\pi_0$ (higher values indicate better performance) for policies learned using each method under varying numbers of companies, numbers of job seekers, and reward sparsity levels.
図は、企業の数、求職者の数、および報酬のスパース性レベルが異なる中で各方法を使用して学習されたポリシーに対するログポリシー $\pi_0$ に対する結果のポリシー値（高い値はより良いパフォーマンスを示す）を示しています。

The results suggest that the proposed methods improve upon the logging policy even in challenging scenarios, such as when the number of companies is small, the number of job seekers is large, or reward sparsity is severe.
結果は、提案された方法が企業の数が少ない、求職者の数が多い、または報酬のスパース性が厳しいといった困難なシナリオにおいてもログポリシーを改善することを示唆しています。

Compared to the baseline methods (DM-, IPS-, and DR-PG), DiPS- and DPR-PG achieve the highest policy values in most cases, demonstrating their effectiveness not only in policy evaluation and selection but also in learning.
基準方法（DM-、IPS-、および DR-PG）と比較して、DiPS- および DPR-PG はほとんどのケースで最高のポリシー値を達成し、ポリシー評価と選択だけでなく学習においてもその効果を示しています。



## 6.REAL-WORLD DATA EXPERIMENTS

To evaluate the real-world applicability of DiPS and DPR, we conduct experiments about OPE using real-world A/B testing data collected from Wantedly Visit, an industrial job-matching platform with over 4 million registered users and more than 40,000 companies. 
DiPSとDPRの実世界での適用可能性を評価するために、私たちはWantedly Visitから収集した実世界のA/Bテストデータを使用してOPEに関する実験を行います。このプラットフォームは、400万人以上の登録ユーザーと40,000社以上の企業を持つ産業の求人マッチングプラットフォームです。

On this platform, job seekers can apply for jobs, and conversely, recruiters can send scouting requests to job seekers. 
このプラットフォームでは、求職者が求人に応募でき、逆にリクルーターは求職者にスカウトリクエストを送信できます。

We use A/B testing data from a recommender system in the Wantedly Visit’s scouting service, which recommends job seekers to companies. 
私たちは、Wantedly VisitのスカウトサービスにおけるレコメンダーシステムからのA/Bテストデータを使用します。このシステムは、求職者を企業に推薦します。

This system is designed as a reciprocal recommender system and recalculates rankings once per day. 
このシステムは相互推薦システムとして設計されており、ランキングを1日1回再計算します。

The dataset includes records of recommendations, which companies sent scouts to which job seekers, and whether the job seekers responded. 
データセットには、どの企業がどの求職者にスカウトを送ったか、そして求職者が応答したかどうかの推薦記録が含まれています。

##### Dataset

We processed the online testing data to align the original ranked interaction data with our formulation. 
私たちは、オンラインテストデータを処理して、元のランク付けされたインタラクションデータを私たちの定式化に合わせました。

Specifically, we regard $c$ as a mix of (recommended date, interaction rank, company ID), and $j$ as a mix of (recommended date, job seeker ID). 
具体的には、$c$を（推薦日、インタラクションランク、企業ID）の組み合わせと見なし、$j$を（推薦日、求職者ID）の組み合わせと見なします。

These definitions include the ”recommended date” because the contexts of companies, job seekers, and policies vary from day to day. 
これらの定義には「推薦日」が含まれています。なぜなら、企業、求職者、ポリシーのコンテキストは日々異なるからです。

Additionally, we introduce the notion of ”interaction rank,” which denotes the position in the ranking at which the company interacted with the job seeker. 
さらに、「インタラクションランク」という概念を導入します。これは、企業が求職者とインタラクションを行った際のランキング内の位置を示します。

This framing supports a bandit setting and allows us to distinguish between situations in which a company encounters a job seeker at rank $k$ versus rank $k'$ on the same day (where $k \neq k'$). 
この枠組みはバンディット設定をサポートし、企業が同じ日にランク $k$ とランク $k'$ の求職者に出会う状況を区別できるようにします（ここで $k \neq k'$）。

For this evaluation, we used only data where $k \leq 3$ from the original logged dataset. 
この評価のために、元のログデータセットから $k \leq 3$ のデータのみを使用しました。

Table 1 in the appendix shows the statistics of the preprocessed dataset. 
付録の表1には、前処理されたデータセットの統計が示されています。

In our dataset, the first-stage rewards $s$ corresponds to the scout request, while the ultimate reward $m$ corresponds to a successful match, that is, the company sends a scout to the job seeker, and the job seeker replies positively. 
私たちのデータセットでは、第一段階の報酬 $s$ はスカウトリクエストに対応し、最終的な報酬 $m$ は成功したマッチに対応します。つまり、企業が求職者にスカウトを送り、求職者が肯定的に応答することです。

##### Setup

Since we were not able to replicate the exact action choice probabilities under our recommendation policies, we estimated both the logging $\pi_0(j|c)$ and the new $\pi(j|c)$ policies using Gradient Boosting Decision Tree (GBDT). 
私たちは、推薦ポリシーの下で正確なアクション選択確率を再現できなかったため、ログの $\pi_0(j|c)$ と新しい $\pi(j|c)$ ポリシーの両方をGradient Boosting Decision Tree (GBDT)を使用して推定しました。

During the policy estimation task, we treated instances where a job seeker was recommended as a rank-$k$ candidate for a company whose interaction rank was also $k$ as positive examples, and all other instances as negative examples. 
ポリシー推定タスク中、求職者がランク-$k$ の候補として推薦された場合を、インタラクションランクも $k$ の企業に対する正の例と見なし、他のすべてのインスタンスを負の例と見なしました。

We trained the models using a 5-fold cross-validation procedure, and then applied the softmax function to normalize the model outputs, ensuring that $\sum_{j \in \mathcal{J}} \pi'(j|c) = 1$ for $\pi' \in \{\pi_0, \pi\}$. 
私たちは5分割交差検証手法を使用してモデルを訓練し、その後ソフトマックス関数を適用してモデル出力を正規化しました。これにより、$\pi' \in \{\pi_0, \pi\}$ に対して $\sum_{j \in \mathcal{J}} \pi'(j|c) = 1$ が保証されます。

##### Results

In our experiments, we compared the MSE and ErrorRate of DiPS and DPR against baseline estimators. 
私たちの実験では、DiPSとDPRのMSEとErrorRateをベースライン推定器と比較しました。

During evaluation, we sampled a specific number of companies from the logged data, trained reward estimation models using GBDT within a cross-validation framework, and then estimated the policy value with each method. 
評価中、ログデータから特定の数の企業をサンプリングし、交差検証フレームワーク内でGBDTを使用して報酬推定モデルを訓練し、その後各手法でポリシー値を推定しました。

We repeated this evaluation process 20 times, varying the number of companies in $\mathcal{D}$. 
この評価プロセスを20回繰り返し、$\mathcal{D}$内の企業の数を変えました。

Figure 5 presents the evaluation results under different company sampling sizes, and Figure 6 shows the distributions of policy values estimated by IPS and DiPS over 20 repetitions with 8,000 companies. 
図5は異なる企業サンプリングサイズの下での評価結果を示し、図6は8,000社での20回の繰り返しにわたってIPSとDiPSによって推定されたポリシー値の分布を示しています。

We discuss the results below. 
以下に結果を議論します。

First, Figure 5 shows that DiPS and DPR achieve low MSE, in particular, DPR achieves significantly lower MSE than the baseline methods across most configurations. 
まず、図5はDiPSとDPRが低いMSEを達成していることを示しており、特にDPRはほとんどの構成でベースライン手法よりも有意に低いMSEを達成しています。

This reduction in MSE results from both low bias and low variance. 
このMSEの低下は、低いバイアスと低い分散の両方から生じています。

The low variance aligns with our theoretical analysis and findings from synthetic data experiments. 
低い分散は、私たちの理論的分析と合成データ実験の結果と一致しています。

In contrast, the bias behavior of DiPS and DPR has two noteworthy characteristics. 
対照的に、DiPSとDPRのバイアスの挙動には2つの注目すべき特徴があります。

First, DiPS produces lower bias than IPS, and DPR shows lower bias than DR. 
まず、DiPSはIPSよりも低いバイアスを生成し、DPRはDRよりも低いバイアスを示します。

As shown in Theorem 4.2, the bias of DiPS can be smaller than that of IPS when the estimation errors of $\hat{\pi}_{0}(j|c)$ and $\hat{q}_{r}(c,j)$ are positively correlated. 
定理4.2に示されているように、DiPSのバイアスは、$\hat{\pi}_{0}(j|c)$ と $\hat{q}_{r}(c,j)$ の推定誤差が正の相関を持つ場合、IPSのバイアスよりも小さくなる可能性があります。

The overestimation observed in $\hat{V}_{\mathrm{IPS}}(\pi)$ in Figure 6 suggests an underestimation of the logging policy probability $\hat{\pi}_{0}(j|c)$. 
図6における$\hat{V}_{\mathrm{IPS}}(\pi)$で観察された過大評価は、ログポリシー確率$\hat{\pi}_{0}(j|c)$の過小評価を示唆しています。

Additionally, we observed that the model $\hat{q}_{r}(c,j)$ tends to underestimate $q_{r}(c,j)$ during cross-validation. 
さらに、モデル$\hat{q}_{r}(c,j)$は交差検証中に$q_{r}(c,j)$を過小評価する傾向があることを観察しました。

These factors contribute to bias reduction of DiPS. 
これらの要因は、DiPSのバイアス削減に寄与しています。

A similar reasoning applies to DPR compared to DR. 
同様の理由がDPRにもDRと比較して適用されます。

The second notable observation is that DPR tends to produce smaller bias than DiPS. 
2つ目の注目すべき観察は、DPRがDiPSよりも小さいバイアスを生成する傾向があることです。

Under a known logging policy, both estimators have the same bias, as confirmed by theoretical analysis and synthetic experiments. 
既知のログポリシーの下では、両方の推定器は同じバイアスを持ち、これは理論的分析と合成実験によって確認されています。

However, under an unknown logging policy, Eq.(26) in the appendix shows that the bias of DPR differs from that of DiPS by the term $(1 - \pi_{0}(j|c)/\hat{\pi}_{0}(j|c))\hat{q}_{m}(j|c)$. 
しかし、未知のログポリシーの下では、付録の式(26)はDPRのバイアスがDiPSのバイアスと$(1 - \pi_{0}(j|c)/\hat{\pi}_{0}(j|c))\hat{q}_{m}(j|c)$という項によって異なることを示しています。

In our experiments, the underestimation of the logging policy probability mitigates the bias in DPR. 
私たちの実験では、ログポリシー確率の過小評価がDPRのバイアスを軽減します。

Taken together, these results demonstrate that our proposed methods provide more accurate estimations on real-world data than the baselines by effectively reducing variance and, with unknown logging policies, our methods even reduce bias. 
これらの結果を総合すると、私たちの提案した手法は、分散を効果的に減少させることによって、実世界のデータに対してベースラインよりもより正確な推定を提供し、未知のログポリシーの下でもバイアスを減少させることを示しています。

Next, DiPS and DPR also achieve low ErrorRate. 
次に、DiPSとDPRも低いErrorRateを達成します。

An interesting observation is that DiPS and IPS show lower ErrorRate than DPR and DR, despite DPR and DR achieving smaller MSE. 
興味深い観察は、DPRとDRがより小さいMSEを達成しているにもかかわらず、DiPSとIPSがDPRとDRよりも低いErrorRateを示すことです。

Figure 6 helps explain this phenomenon. 
図6はこの現象を説明するのに役立ちます。

The overestimation of $V(\pi)$ by IPS contributes to its large MSE but leads to a low ErrorRate, as it more often ranks the target policy above the logging policy, which is correct. 
IPSによる$V(\pi)$の過大評価は、その大きなMSEに寄与しますが、ターゲットポリシーをログポリシーの上にランク付けすることが多いため、低いErrorRateにつながります。

DiPS significantly reduces overestimation by lowering both bias and variance, leading to a slight improvement in ErrorRate. 
DiPSはバイアスと分散の両方を低下させることによって過大評価を大幅に減少させ、ErrorRateのわずかな改善につながります。

Overall, these findings demonstrate that our estimators are well-suited for real-world applications, achieving both low MSE and ErrorRate compared to their respective counterparts. 
全体として、これらの発見は、私たちの推定器が実世界のアプリケーションに適しており、それぞれの対照と比較して低いMSEとErrorRateを達成していることを示しています。



## 7. 結論

This paper studies and formulates the problems of off-policy evaluation (OPE) and off-policy learning (OPL) for matching markets for the first time in the relevant literature. 
本論文は、関連文献においてマッチング市場のオフポリシー評価（OPE）およびオフポリシー学習（OPL）の問題を初めて研究し、定式化します。

Existing estimators, such as DM, IPS, and DR, perform poorly in matching markets due to the large-scale environment and sparse reward nature. 
既存の推定量（DM、IPS、DRなど）は、大規模な環境とスパースな報酬の特性により、マッチング市場での性能が低下します。

We introduce two novel estimators, DiPS and DPR, for off-policy evaluation in the matching domain. 
私たちは、マッチング領域におけるオフポリシー評価のための2つの新しい推定量、DiPSとDPRを導入します。

These estimators explicitly leverage first-stage reward labels, such as the ”sending scout” label in job-matching recommender systems, to achieve better bias-variance control. 
これらの推定量は、ジョブマッチング推薦システムにおける「送信スカウト」ラベルのような第一段階の報酬ラベルを明示的に活用し、より良いバイアス-バリアンス制御を実現します。

Extensive experiments on synthetic data and the real-world A/B testing dataset demonstrated that our proposed methods outperformed conventional estimators in policy evaluation, selection, and learning tasks, showing practical impact. 
合成データおよび実世界のA/Bテストデータセットにおける広範な実験により、私たちの提案した手法がポリシー評価、選択、学習タスクにおいて従来の推定量を上回り、実際の影響を示しました。



## References 参考文献
- (1)↑
- Bembom and vander Laan (2008)↑
Oliver Bembom and MarkJ vander Laan. 2008.
データ適応型の逆確率治療重み付け推定量の切断レベルの選択。(2008).
- Chen etal.(2023)↑
Jiaxing Chen, Hongzhi Liu, Hongrui Guo, Yingpeng Du, Zekai Wang, Yang Song, and Zhonghai Wu. 2023.
双方向シーケンシャルハイパーグラフ畳み込みネットワークによる相互推薦。2023 IEEE国際データマイニング会議（ICDM）において。IEEE, 974–979.
- Dudík etal.(2014)↑
Miroslav Dudík, Dumitru Erhan, John Langford, and Lihong Li. 2014.
二重ロバストポリシー評価と最適化。
Statist. Sci.29, 4 (2014), 485 – 511. https://doi.org/10.1214/14-STS500
- Farajtabar etal.(2018)↑
Mehrdad Farajtabar, Mohammad Ghavamzadeh, and Yinlam Chow. 2018.
よりロバストな二重ロバストオフポリシー評価。
- Friedman (2001)↑
JeromeH. Friedman. 2001.
貪欲な関数近似：勾配ブースティングマシン。
The Annals of Statistics29, 5 (2001), 1189 – 1232. https://doi.org/10.1214/aos/1013203451
- Gilotte etal.(2018)↑
Alexandre Gilotte, Clément Calauzènes, Thomas Nedelec, Alexandre Abraham, and Simon Dollé. 2018.
レコメンダーシステムのためのオフラインA/Bテスト。第11回ACM国際ウェブ検索およびデータマイニング会議の議事録において。198–206.
- Goda etal.(2024)↑
Shuhei Goda, Yudai Hayashi, and Yuta Saito. 2024.
仕事検索のためのマッチ予測と相互推薦を改善するための両方のアプローチ。
arXiv:2409.10992[cs.IR]
- Hu etal.(2023)↑
Xiao Hu, Yuan Cheng, Zhi Zheng, Yue Wang, Xinxin Chi, and Hengshu Zhu. 2023.
Boss: オンライン採用のための双方向職業適合性を考慮したレコメンダーシステム。第29回ACM SIGKDD知識発見とデータマイニング会議の議事録において。4146–4155.
- Jeunen and Goethals (2021)↑
Olivier Jeunen and Bart Goethals. 2021.
推薦におけるオフポリシー学習のための悲観的報酬モデル。第15回ACMレコメンダーシステム会議の議事録において。63–74.
- Kang and Schafer (2007)↑
JosephDY Kang and JosephL Schafer. 2007.
二重ロバスト性の解明：不完全データからの母集団平均推定のための代替戦略の比較。(2007).
- Kiyohara etal.(2024a)↑
Haruka Kiyohara, Ren Kishimoto, Kosuke Kawakami, Ken Kobayashi, Kazuhide Nakata, and Yuta Saito. 2024a.
オフポリシー評価のリスク・リターンのトレードオフを評価し、ベンチマークすることに向けて。第12回国際表現学習会議において。https://openreview.net/forum?id=ycF7mKfVGO
- Kiyohara etal.(2024b)↑
Haruka Kiyohara, Masahiro Nomura, and Yuta Saito. 2024b.
抽象化の最適化によるスレートバンディットポリシーのオフポリシー評価。2024年ACMウェブ会議の議事録において。3150–3161.
- Kleinerman etal.(2018)↑
Akiva Kleinerman, Ariel Rosenfeld, Francesco Ricci, and Sarit Kraus. 2018.
相互レコメンダーシステムにおける受信者と推薦ユーザーの重要性の最適なバランス。第12回ACMレコメンダーシステム会議の議事録において。131–139.
- Lai etal.(2024)↑
Kai-Huang Lai, Zhe-Rui Yang, Pei-Yuan Lai, Chang-Dong Wang, Mohsen Guizani, and Min Chen. 2024.
知識を考慮した説明可能な相互推薦。
AAAI人工知能会議の議事録38, 8 (2024年3月), 8636–8644. https://doi.org/10.1609/aaai.v38i8.28708
- Li and Li (2012)↑
Lei Li and Tao Li. 2012.
MEET: 相互レコメンダーシステムのための一般化フレームワーク。第21回ACM国際情報および知識管理会議（ハワイ州マウイ、アメリカ合衆国）（CIKM ’12）において。計算機機械協会、ニューヨーク、NY、アメリカ合衆国、35–44. https://doi.org/10.1145/2396761.2396770
- Liang and Vlassis (2022)↑
Dawen Liang and Nikos Vlassis. 2022.
レコメンダーシステムのためのローカルポリシー改善。
arXivプレプリントarXiv:2212.11431(2022).
- Lichtenberg etal.(2023)↑
JanMalte Lichtenberg, Alexander Buchholz, Giuseppe DiBenedetto, Matteo Ruffini, and Ben London. 2023.
ダブルクリッピング：オフポリシー評価におけるバイアスの少ない分散削減。
arXivプレプリントarXiv:2309.01120(2023).
- Liu etal.(2024)↑
Ping Liu, Haichao Wei, Xiaochen Hou, Jianqiang Shen, Shihai He, KayQianqi Shen, Zhujun Chen, Fedor Borisyuk, Daniel Hewlett, Liang Wu, Srikant Veeraraghavan, Alex Tsun, Chengming Jiang, and Wenjing Zhang. 2024.
LinkSAGE: グラフニューラルネットワークを用いた仕事マッチングの最適化。
arXiv:2402.13430[cs.LG]
- Luo etal.(2020)↑
Linhao Luo, Liqi Yang, Ju Xin, Yixiang Fang, Xiaofeng Zhang, Xiaofei Yang, Kai Chen, Zhiyuan Zhang, and Kai Liu. 2020.
RRCN: 双方向フィードバックに基づく強化ランダム畳み込みネットワークによる相互推薦アプローチ。arXiv:2011.12586[cs.IR]
- Mehrotra etal.(2018)↑
Rishabh Mehrotra, James McInerney, Hugues Bouchard, Mounia Lalmas, and Fernando Diaz. 2018.
公正な市場に向けて：推薦システムにおける関連性、公正性、満足度のトレードオフの反事実的評価。第27回ACM国際情報および知識管理会議の議事録において。2243–2251.
- Metelli etal.(2021)↑
AlbertoMaria Metelli, Alessio Russo, and Marcello Restelli. 2021.
オフポリシー評価と学習のためのサブガウスおよび微分可能重要度サンプリング。神経情報処理システムの進歩において、A.Beygelzimer, Y.Dauphin, P.Liang, and J.Wortman Vaughan (Eds.). https://openreview.net/forum?id=_8vCV7AxPZ
- Mine etal.(2013)↑
Tsunenori Mine, Tomoyuki Kakuta, and Akira Ono. 2013.
双方向フィードバックによる仕事マッチングのための相互推薦。2013年第2回IIAI国際会議において。39–44. https://doi.org/10.1109/IIAI-AAI.2013.91
- Neve and Palomares (2019)↑
James Neve and Ivan Palomares. 2019.
相互レコメンダーシステムにおける協調フィルタリングのための潜在因子モデルと集約演算子。第13回ACMレコメンダーシステム会議（デンマーク、コペンハーゲン）（RecSys ’19）において。計算機機械協会、ニューヨーク、NY、アメリカ合衆国、219–227. https://doi.org/10.1145/3298689.3347026
- Palomares etal.(2021)↑
Iván Palomares, Carlos Porcel, Luiz Pizzato, Ido Guy, and Enrique Herrera-Viedma. 2021.
相互レコメンダーシステム：最先端文献の分析、課題、社会的推薦に向けた機会。
Information Fusion69 (2021), 103–127.
- Pizzato etal.(2010)↑
Luiz Pizzato, Tomek Rej, Thomas Chung, Irena Koprinska, and Judy Kay. 2010.
RECON: オンラインデーティングのための相互レコメンダー。第4回ACMレコメンダーシステム会議（スペイン、バルセロナ）（RecSys ’10）において。計算機機械協会、ニューヨーク、NY、アメリカ合衆国、207–214. https://doi.org/10.1145/1864708.1864747
- Saito etal.(2024)↑
Yuta Saito, Himan Abdollahpouri, Jesse Anderton, Ben Carterette, and Mounia Lalmas. 2024.
長期オフポリシー評価と学習。2024年ACMウェブ会議の議事録において（シンガポール、シンガポール）（WWW ’24）。計算機機械協会、ニューヨーク、NY、アメリカ合衆国、3432–3443. https://doi.org/10.1145/3589334.3645446
- Saito and Joachims (2021)↑
Yuta Saito and Thorsten Joachims. 2021.
レコメンダーシステムのための反事実学習と評価：基礎、実装、および最近の進展。第15回ACMレコメンダーシステム会議（オランダ、アムステルダム）（RecSys ’21）において。828–830.
- Saito and Joachims (2022a)↑
Yuta Saito and Thorsten Joachims. 2022a.
埋め込みを介した大規模アクション空間のオフポリシー評価。
arXiv:2202.06317[cs.LG]
- Saito and Joachims (2022b)↑
Yuta Saito and Thorsten Joachims. 2022b.
埋め込みを介した大規模アクション空間のオフポリシー評価。第39回国際機械学習会議の議事録において。PMLR, 19089–19122.
- Saito etal.(2023a)↑
Yuta Saito, Qingyang Ren, and Thorsten Joachims. 2023a.
結合効果モデリングを介した大規模アクション空間のオフポリシー評価。第40回国際機械学習会議の議事録において。PMLR, 29734–29759.
- Saito etal.(2023b)↑
Yuta Saito, Qingyang Ren, and Thorsten Joachims. 2023b.
結合効果モデリングを介した大規模アクション空間のオフポリシー評価。第40回国際機械学習会議の議事録において（アメリカ合衆国ハワイ州ホノルル）（ICML’23）。JMLR.org, Article 1234, 26ページ.
- Saito etal.(2021)↑
Yuta Saito, Takuma Udagawa, Haruka Kiyohara, Kazuki Mogi, Yusuke Narita, and Kei Tateno. 2021.
オフポリシー評価のロバスト性の評価。第15回ACMレコメンダーシステム会議の議事録において。ACM, 114–123.
- Shimizu etal.(2024)↑
Tatsuhiro Shimizu, Koichi Tanaka, Ren Kishimoto, Haruka Kiyohara, Masahiro Nomura, and Yuta Saito. 2024.
文脈的組合バンディットにおける効果的なオフポリシー評価と学習。第18回ACMレコメンダーシステム会議の議事録において（イタリア、バーリ）（RecSys ’24）。計算機機械協会、ニューヨーク、NY、アメリカ合衆国、733–741. https://doi.org/10.1145/3640457.3688099
- Su etal.(2022)↑
Yi Su, Magd Bayoumi, and Thorsten Joachims. 2022.
マッチング市場における推薦のためのランキングの最適化。2022年ACMウェブ会議の議事録において。328–338.
- Su etal.(2020a)↑
Yi Su, Maria Dimakopoulou, Akshay Krishnamurthy, and Miroslav Dudík. 2020a.
シュリンクを用いた二重ロバストオフポリシー評価。第37回国際機械学習会議の議事録において（ICML’20）。JMLR.org, Article 850, 10ページ.
- Su etal.(2020b)↑
Yi Su, Pavithra Srinath, and Akshay Krishnamurthy. 2020b.
オフポリシー評価のための適応推定器選択。第37回国際機械学習会議の議事録において（機械学習研究の議事録、Vol.119）、HalDaumé IIIとAarti Singh (Eds.). PMLR, 9196–9205. https://proceedings.mlr.press/v119/su20d.html
- Su etal.(2019a)↑
Yi Su, Lequn Wang, Michele Santacatterina, and Thorsten Joachims. 2019a.
CAB: ポリシー評価と学習のための連続適応ブレンディング。第36回国際機械学習会議の議事録において、Vol.97。PMLR, 6005–6014.
- Su etal.(2019b)↑
Yi Su, Lequn Wang, Michele Santacatterina, and Thorsten Joachims. 2019b.
CAB: ポリシー評価と学習のための連続適応ブレンディング。第36回国際機械学習会議の議事録において（機械学習研究の議事録、Vol.97）、Kamalika ChaudhuriとRuslan Salakhutdinov (Eds.). PMLR, 6005–6014. https://proceedings.mlr.press/v97/su19a.html
- Thomas and Brunskill (2016)↑
PhilipS. Thomas and Emma Brunskill. 2016.
強化学習のためのデータ効率的なオフポリシーポリシー評価。第33回国際機械学習会議の議事録において - ボリューム48（アメリカ合衆国ニューヨーク）（ICML’16）。JMLR.org, 2139–2148.
- Tomita etal.(2023)↑
Yoji Tomita, Riku Togashi, Yuriko Hashizume, and Naoto Ohsaka. 2023.
マッチング市場における迅速かつ試験に依存しない相互推薦。第17回ACMレコメンダーシステム会議の議事録において。12–23.
- Tomita etal.(2022)↑
Yoji Tomita, Riku Togashi, and Daisuke Moriwaki. 2022.
オンラインデーティングにおけるマッチング理論に基づくレコメンダーシステム。第16回ACMレコメンダーシステム会議の議事録において。538–541.
- Tu etal.(2014)↑
Kun Tu, Bruno Ribeiro, David Jensen, Don Towsley, Benyuan Liu, Hua Jiang, and Xiaodong Wang. 2014.
オンラインデーティングの推薦：マッチング市場と学習の好み。第23回国際WWW会議の議事録において（韓国、ソウル）（WWW ’14 Companion）。計算機機械協会、ニューヨーク、NY、アメリカ合衆国、787–792. https://doi.org/10.1145/2567948.2579240
- Uehara etal.(2022)↑
Masatoshi Uehara, Chengchun Shi, and Nathan Kallus. 2022.
強化学習におけるオフポリシー評価のレビュー。
arXivプレプリントarXiv:2212.06355(2022).
- Wang etal.(2017)↑
Yu-Xiang Wang, Alekh Agarwal, and Miroslav Dudík. 2017.
文脈バンディットにおける最適かつ適応的なオフポリシー評価。第34回国際機械学習会議の議事録において - ボリューム70（オーストラリア、シドニー）（ICML’17）。JMLR.org, 3589–3597.
- Xia etal.(2015)↑
Peng Xia, Benyuan Liu, Yizhou Sun, and Cindy Chen. 2015.
オンラインデーティングのための相互推薦システム。2015 IEEE/ACM国際社会ネットワーク分析およびマイニング会議の議事録において（ASONAM ’15）。ACM. https://doi.org/10.1145/2808797.2809282
- Yang etal.(2024)↑
Chen Yang, Sunhao Dai, Yupeng Hou, WayneXin Zhao, Jun Xu, Yang Song, and Hengshu Zhu. 2024.
相互レコメンダーシステムの再考：メトリクス、定式化、および方法。第30回ACM SIGKDD知識発見とデータマイニング会議の議事録において（スペイン、バルセロナ）（KDD ’24）。計算機機械協会、ニューヨーク、NY、アメリカ合衆国、3714–3723. https://doi.org/10.1145/3637528.3671734
- Yıldırım etal.(2021)↑
Ezgi Yıldırım, Payam Azad, and ŞuleGündüz Öğüdücü. 2021.
biDeepFM: 相互推薦のための多目的深層因子分解機。
Engineering Science and Technology, an International Journal24, 6 (2021), 1467–1477.
- Yıldırım etal.(2021)↑
Ezgi Yıldırım, Payam Azad, and ŞuleGündüz Öğüdücü. 2021.
biDeepFM: 相互推薦のための多目的深層因子分解機。
Engineering Science and Technology, an International Journal24, 6 (2021), 1467–1477. https://doi.org/10.1016/j.jestch.2021.03.010
- Zheng etal.(2023)↑
Bowen Zheng, Yupeng Hou, WayneXin Zhao, Yang Song, and Hengshu Zhu. 2023.
相互シーケンシャル推薦。第17回ACMレコメンダーシステム会議の議事録において（シンガポール、シンガポール）（RecSys ’23）。計算機機械協会、ニューヨーク、NY、アメリカ合衆国、89–100. https://doi.org/10.1145/3604915.3608798



## Appendix A 他のOPE推定量のマッチング市場への再設計

Appendix A  
本論文では、DM、IPS、DRをベースライン推定量として焦点を当てていますが、以下に示すように、Switch-DR（Wang et al., 2017）やMIPS（Saito and Joachims, 2022a）などのより洗練された推定量を改善するために、私たちの手法を容易に拡張できることを示します。  

First, we rigorously define the Switch-DR(Wang etal.,2017)estimator under our formulation as follows.  
まず、私たちの定式化の下でSwitch-DR（Wang et al., 2017）推定量を厳密に定義します。  

(22)  
(22)  

where $\lambda > 0$ is a hyperparameter.  
ここで、$\lambda > 0$はハイパーパラメータです。  

For samples with $\frac{\pi(j_{c}|c)}{\pi_{0}(j_{c}|c)} \leq \lambda$, Switch-DR is equal to DR, while it applies DM when $\frac{\pi(j_{c}|c)}{\pi_{0}(j_{c}|c)} > \lambda$.  
$\frac{\pi(j_{c}|c)}{\pi_{0}(j_{c}|c)} \leq \lambda$ のサンプルに対して、Switch-DRはDRと等しく、$\frac{\pi(j_{c}|c)}{\pi_{0}(j_{c}|c)} > \lambda$ の場合にはDMを適用します。  

We can readily extend the Switch-DR estimator to explicitly use the first-stage reward observations $s$ as in our proposed methods.  
私たちは、提案した手法と同様に、Switch-DR推定量を第一段階の報酬観測$s$を明示的に使用するように容易に拡張できます。  

(23)  
(23)  

Next, the MIPS estimator(Saito and Joachims,2022b) is known as a method to leverage action embeddings to reduce variance in OPE, particularly for large action spaces.  
次に、MIPS推定量（Saito and Joachims, 2022b）は、特に大規模なアクション空間においてOPEの分散を減少させるためにアクション埋め込みを活用する方法として知られています。  

It is defined in our setting as follows.  
それは私たちの設定で次のように定義されます。  

(24)  
(24)  

where $e_{j}$ is a embedding of job seeker $j$, and $\pi(e_{j}|c)$ is a marginalized distribution of job seeker embeddings conditional on $c$.  
ここで、$e_{j}$は求職者$j$の埋め込みであり、$\pi(e_{j}|c)$は$c$に条件付けられた求職者埋め込みの周辺分布です。  

It is again immediate to extend this MIPS estimator in our matching market formulation to incorporate the two-stage reward structure as follows.  
このMIPS推定量を私たちのマッチング市場の定式化に拡張し、二段階の報酬構造を組み込むことも容易です。  

(25)  
(25)  

By applying the same theoretical analysis presented in the main text, these estimators achieve better bias-variance tradeoff in our problem of matching markets due to the use of the two-stage reward structure.  
本論文で示されたのと同じ理論的分析を適用することにより、これらの推定量は二段階の報酬構造の使用により、マッチング市場の問題においてより良いバイアス-分散トレードオフを達成します。  



## Appendix B The Policy Gradient Estimator based on DPR 付録B DPRに基づくポリシー勾配推定器

Appendix B  
付録B

The following extends the DPR estimator as a policy gradient estimator.  
以下では、DPR推定器をポリシー勾配推定器として拡張します。



## Appendix CProofs 付録 C 証明

Appendix C
付録 C

This section provides derivations of the theorems provided in the main text.
このセクションでは、本文で提供された定理の導出を示します。



### C.1. 命題 2.1 と 2.2

C.1.  
We first derive the variance of DR via applying the law of total variance below.  
まず、以下の全体分散の法則を適用して、DRの分散を導出します。

By setting $q^m(c,j)=0$ in the variance expression of DR, we can derive the variance of IPS in Eq.(9).  
DRの分散表現において $q^m(c,j)=0$ と設定することで、式(9)におけるIPSの分散を導出できます。



### C.2.定理4.1および4.5

C.2.
4.1
4.5
We first derive the expectation of DPR below.
まず、以下にDPRの期待値を導出します。

Therefore, the bias of DPR is
したがって、DPRのバイアスは

By setting $ \hat{q}_{m}(c,j) = 0 $ in the bias expression of DR, we can derive the bias of DiPS in Eq.(18).
DRのバイアス表現において $ \hat{q}_{m}(c,j) = 0 $ と設定することにより、式(18)におけるDiPSのバイアスを導出できます。



### C.3. 定理 4.3 と 4.6

C.3.  
We first derive the variance of DR via applying the law of total variance below.  
まず、以下の全体分散の法則を適用して、DRの分散を導出します。

By setting $q^m(c,j)=0$ in the variance expression of DPR, we can derive the variance of DiPS in Eq.(15).  
DPRの分散表現において$q^m(c,j)=0$と設定することで、式(15)におけるDiPSの分散を導出できます。



### C.4.定理4.2およびC.1

C.4.  
4.2  
C.1  
The bias of the DPR estimator with an estimated logging policy $\hat{\pi}_{0}(j|c)$ is derived as follows.  
推定されたロギングポリシー $\hat{\pi}_{0}(j|c)$ を用いたDPR推定量のバイアスは以下のように導出されます。

The bias of the DPR estimator with an estimated logging policy $\hat{\pi}_{0}(j|c)$ is derived as follows.  
推定されたロギングポリシー $\hat{\pi}_{0}(j|c)$ を用いたDPR推定量のバイアスは以下のように導出されます。

(26)  
(26)

To derive the above theorem, we first derive the expectation of DPR with an estimated logging policy.  
上記の定理を導出するために、まず推定されたロギングポリシーを用いたDPRの期待値を導出します。

Therefore, the bias of DPR with an estimated logging policy is  
したがって、推定されたロギングポリシーを用いたDPRのバイアスは

By setting $\hat{q}_{m}(c,j)=0$ in the bias expression of DPR with an estimated logging policy, we can derive the bias of DiPS with an estimated logging policy in Eq.(14).  
推定されたロギングポリシーを用いたDPRのバイアス表現において $\hat{q}_{m}(c,j)=0$ と設定することにより、式(14)における推定されたロギングポリシーを用いたDiPSのバイアスを導出することができます。



### C.5.Theorem4.4 C.5.定理4.4

The following calculates the difference in the variance of IPS and DiPS using the condition, 
以下では、条件を用いてIPSとDiPSの分散の違いを計算します。

$q^r(c,j) \leq q_r(c,j), \forall (c,j)$ 
$\hat{q}_{r}(c,j) \leq q_{r}(c,j), \forall (c,j)$ 
for-all $c,j$.
すべての$c,j$に対して、$q^r(c,j) \leq q_r(c,j)$、$\hat{q}_{r}(c,j) \leq q_{r}(c,j)$です。

Figure 7. 
図7。

Table 1. 
表1。



## Appendix D 追加実験設定と結果

Appendix D
付録 D



### D.1. 報酬推定モデルの性能

D.1.  
Table3shows the ROC-AUC of our reward prediction models for reply and match.  
表3は、返信とマッチのための私たちの報酬予測モデルのROC-AUCを示しています。

In addition, the following table represents the underestimation in each reward model.  
さらに、以下の表は各報酬モデルにおける過小評価を示しています。

The value is $\mathbb{E}[\hat{q}_{r}(c,j)]/\mathbb{E}[q_{r}(c,j)]-1$ and $\mathbb{E}[\hat{q}_{m}(c,j)]/\mathbb{E}[q_{m}(c,j)]-1$ calculated with the logged data.  
その値は、ログデータを用いて計算された $\mathbb{E}[\hat{q}_{r}(c,j)]/\mathbb{E}[q_{r}(c,j)]-1$ および $\mathbb{E}[\hat{q}_{m}(c,j)]/\mathbb{E}[q_{m}(c,j)]-1$ です。

Table 3.  
表3。



### D.2. すべての推定器の推定ポリシー値分布

D.2.  
Figure 8 shows the estimated policy value distribution for DiPS, DPR and other baseline estimators.  
図8は、DiPS、DPRおよび他のベースライン推定器の推定ポリシー値分布を示しています。  
The red and blue box represent the estimated policy distributions and the dashed lines represent true policy values.  
赤と青のボックスは推定されたポリシー分布を表し、破線は真のポリシー値を表しています。  

Figure 8.  
図8。  

##### Report Github Issue  
##### GitHubの問題を報告  

LATE  
LATE  

A  
A  

E  
E  

xml  
xml  



## Instructions for reporting errors エラー報告の手順

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. 
私たちは論文のHTMLバージョンを改善し続けており、あなたのフィードバックはアクセシビリティとモバイルサポートの向上に役立ちます。 
To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:
HTMLのエラーを報告するには、以下のいずれかの方法を選択してください。

- Click the "Report Issue" button.
- "Report Issue"ボタンをクリックしてください。
- Open a report feedback form via keyboard, use "Ctrl + ?".
- キーボードを使用して報告フィードバックフォームを開くには、「Ctrl + ?」を使用してください。
- Make a text selection and click the "Report Issue for Selection" button near your cursor.
- テキストを選択し、カーソルの近くにある「Report Issue for Selection」ボタンをクリックしてください。
- You can use Alt+Y to toggle on and Alt+Shift+Y to toggle off accessible reporting links at each section.
- 各セクションでアクセシブルな報告リンクをオンにするにはAlt+Yを、オフにするにはAlt+Shift+Yを使用できます。

Our team has already identified the following issues. 
私たちのチームはすでに以下の問題を特定しています。 
We appreciate your time reviewing and reporting rendering errors we may not have found yet. 
私たちは、まだ見つけていない可能性のあるレンダリングエラーをレビューし報告するためにあなたが費やす時間に感謝します。 
Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. 
あなたの努力は、すべての読者のためにHTMLバージョンを改善するのに役立ちます。なぜなら、障害は研究へのアクセスの障壁であってはならないからです。 
Thank you for your continued support in championing open access for all.
すべての人にオープンアクセスを推進するための継続的なサポートに感謝します。

Have a free development cycle? 
開発サイクルに余裕がありますか？ 
Help support accessibility at arXiv! 
arXivでのアクセシビリティをサポートしてください！ 
Our collaborators at LaTeXML maintain a list of packages that need conversion, and welcome developer contributions.
LaTeXMLの協力者は、変換が必要なパッケージのリストを維持しており、開発者の貢献を歓迎しています。
