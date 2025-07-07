refs: https://arxiv.org/html/2506.13163v1

# Efficient Algorithms for Logistic Contextual Slate Bandits with Bandit Feedback
# 効率的なアルゴリズムによるロジスティックコンテキストスレートバンディットとバンディットフィードバック

We study the Logistic Contextual Slate Bandit problem, where, at each round, an agent selects a slate of $N$ items from an exponentially large set (of size $2^{\Omega(N)}$) of candidate slates provided by the environment. 
私たちは、ロジスティックコンテキストスレートバンディット問題を研究します。ここで、各ラウンドでエージェントは、環境から提供される候補スレートの指数的に大きなセット（サイズは $2^{\Omega(N)}$）から $N$ 個のアイテムのスレートを選択します。
A single binary reward, determined by a logistic model, is observed for the chosen slate. 
選択されたスレートに対して、ロジスティックモデルによって決定される単一のバイナリ報酬が観測されます。
Our objective is to develop algorithms that maximize cumulative reward over $T$ rounds while maintaining low per-round computational costs. 
私たちの目的は、$T$ ラウンドにわたって累積報酬を最大化し、各ラウンドの計算コストを低く抑えるアルゴリズムを開発することです。
We propose two algorithms, Slate-GLM-OFU and Slate-GLM-TS, that accomplish this goal. 
私たちは、この目標を達成するために、Slate-GLM-OFU と Slate-GLM-TS の2つのアルゴリズムを提案します。
These algorithms achieve $N^{O(1)}$ per-round time complexity via “local planning” (independent slot selections), and low regret through “global learning” (joint parameter estimation). 
**これらのアルゴリズムは、「ローカルプランニング」（独立したスロット選択）を通じて $N^{O(1)}$ の各ラウンドの時間計算量を達成し、「グローバル学習」（共同パラメータ推定）を通じて低い後悔を実現**します。(学習はスレート単位でやって、推論はスロット単位でやるってこと??:thinking:)
We provide theoretical and empirical evidence supporting these claims. 
私たちは、これらの主張を支持する理論的および実証的な証拠を提供します。
Under a well-studied diversity assumption, we prove that Slate-GLM-OFU incurs only $\tilde{O}(\sqrt{T})$ regret.
よく研究された多様性の仮定の下で、Slate-GLM-OFU が $\tilde{O}(\sqrt{T})$ の後悔しか生じないことを証明します。
Extensive experiments across a wide range of synthetic settings demonstrate that our algorithms consistently outperform state-of-the-art baselines, achieving both the lowest regret and the fastest runtime. 
広範な合成設定における広範な実験は、私たちのアルゴリズムが最先端のベースラインを一貫して上回り、最低の後悔と最速の実行時間を達成することを示しています。
Furthermore, we apply our algorithm to select in-context examples in prompts of Language Models for solving binary classification tasks such as sentiment analysis. 
さらに、私たちは、感情分析などのバイナリ分類タスクを解決するために、言語モデルのプロンプト内の文脈に沿った例を選択するためにアルゴリズムを適用します。
Our approach achieves competitive test accuracy, making it a viable alternative in practical scenarios. 
私たちのアプローチは競争力のあるテスト精度を達成し、実際のシナリオにおいて実行可能な代替手段となります。

## 1 Introduction 1 はじめに

Online slate bandit problems provide a popular framework for modeling decision-making scenarios where multiple items must be selected in each round. 
**オンラインスレートバンディット問題は、各ラウンドで複数のアイテムを選択する必要がある意思決定シナリオをモデル化するための一般的なフレームワークを提供**します。
A slate consists of multiple slots, each with its own pool of candidate items, which may change over time. 
スレートは複数のスロットで構成されており、それぞれのスロットには独自の候補アイテムのプールがあり、時間とともに変化する可能性があります。
In each round, the learner selects one item per slot, thereby forming a slate. 
各ラウンドで、学習者は各スロットから1つのアイテムを選択し、スレートを形成します。

A single reward drawn from a logistic model with unknown parameters is then received for the entire slate. 
その後、未知のパラメータを持つロジスティックモデルから引き出された単一の報酬が全体のスレートに対して受け取られます。

The learner’s objective is to adaptively optimize their slate selection policy to maximize the cumulative reward (or equivalently, minimize the cumulative regret) over time. 
学習者の目的は、時間の経過とともに累積報酬を最大化（または同等に、累積後悔を最小化）するために、スレート選択ポリシーを適応的に最適化することです。

Online slate bandits naturally model various real-world applications. 
オンラインスレートバンディットは、さまざまな実世界のアプリケーションを自然にモデル化します。

A prominent example is landing page optimization[Hill etal.,2017], where the goal is to optimize the selection of components for each part of a landing page to maximize conversions. 
顕著な例はランディングページの最適化[Hill etal.,2017]であり、目標はコンバージョンを最大化するためにランディングページの各部分のコンポーネントの選択を最適化することです。

Another important application is the automatic optimization of advertising creatives[Chen etal.,2021], which requires advertisers to automatically compose ads from multiple elements, such as product images, text descriptions, and titles. 
もう一つの重要なアプリケーションは、広告クリエイティブの自動最適化[Chen etal.,2021]であり、これは広告主が製品画像、テキスト説明、タイトルなどの複数の要素から広告を自動的に構成することを要求します。

Beyond these practical applications, slate bandits have been extensively studied in the academic literature, leading to the development of many interesting algorithms in diverse settings[Kale etal.,2010, Dimakopoulou etal.,2019, Rhuggenaath etal.,2020]. 
これらの実用的なアプリケーションを超えて、スレートバンディットは学術文献で広く研究されており、多様な設定で多くの興味深いアルゴリズムの開発につながっています[Kale etal.,2010, Dimakopoulou etal.,2019, Rhuggenaath etal.,2020]。

Although good progress has been made on a variety of online slate bandit settings, some significant challenges still remain that limit the applicability of these algorithms. 
さまざまなオンラインスレートバンディット設定において良好な進展が見られましたが、これらのアルゴリズムの適用性を制限するいくつかの重要な課題が依然として残っています。

In applications such as those mentioned above, at each round, the learner has access to some contextual information (such as user query, user history, or demographics) which influences the set of available items per slot. 
上記のようなアプリケーションでは、各ラウンドで学習者は、スロットごとの利用可能なアイテムのセットに影響を与えるいくつかの文脈情報（ユーザークエリ、ユーザー履歴、または人口統計など）にアクセスできます。

To the best of our knowledge, the current literature focuses heavily on the non-contextual (fixed arms111We use the terms arms and actions interchangeably.) setting, i.e., they do not assume access to such contexts and therefore keep the set of items unchanged over time. 
私たちの知る限り、現在の文献は非文脈的（固定アーム111アームとアクションという用語は互換的に使用します。）設定に重きを置いており、つまり、そうした文脈へのアクセスを仮定せず、したがってアイテムのセットを時間とともに変更しないということです。

Another limitation is that most of the prior work assumes that the reward of a slate is a function (known or unknown) of rewards of the items in the slate which are themselves either adversarially chosen or are stochastic but disjoint from each other (i.e., each item’s reward comes from a different distribution). 
もう一つの制限は、ほとんどの先行研究がスレートの報酬は、スレート内のアイテムの報酬の関数（既知または未知）であると仮定していることであり、これらのアイテムは敵対的に選ばれるか、確率的であるが互いに分離されている（つまり、各アイテムの報酬は異なる分布から来る）ということです。

This assumption neglects the inherent similarities between items. 
この仮定は、アイテム間の固有の類似性を無視しています。

A more realistic approach is to assume a unified parametric reward model shared across all slates. 
より現実的なアプローチは、すべてのスレートで共有される統一されたパラメトリック報酬モデルを仮定することです。

This model allows the learner to leverage shared information, significantly simplifying the learning process. 
このモデルは、学習者が共有情報を活用できるようにし、学習プロセスを大幅に簡素化します。

Specifically, for binary rewards, models based on the logistic or probit function can effectively capture the reward structure. 
具体的には、バイナリ報酬の場合、ロジスティックまたはプロビット関数に基づくモデルが報酬構造を効果的に捉えることができます。

A third, and equally important, limitation is the prevalent focus on the semi-bandit feedback setting. 
第三の、同様に重要な制限は、セミバンディットフィードバック設定に対する一般的な焦点です。

This setting provides separate reward feedback for each item within a selected slate. 
この設定は、選択されたスレート内の各アイテムに対して別々の報酬フィードバックを提供します。

However, many practical applications (e.g., the ad creatives problem[Chen etal.,2021]) offer only a single, slate-level reward (i.e., bandit feedback). 
しかし、多くの実用的なアプリケーション（例：広告クリエイティブの問題[Chen etal.,2021]）は、単一のスレートレベルの報酬（すなわち、バンディットフィードバック）しか提供しません。

Although there are some methods for converting bandit feedback to semi-bandit feedback[Dimakopoulou etal.,2019], these are often heuristic and lack theoretical guarantees. 
バンディットフィードバックをセミバンディットフィードバックに変換するためのいくつかの方法[Dimakopoulou etal.,2019]はありますが、これらはしばしばヒューリスティックであり、理論的保証が欠けています。

The item-level feedback in the semi-bandit setting facilitates per-slot exploration and exploitation, enabling the development of algorithms with $N^{O(1)}$ per-round complexity (e.g.,[Kale etal.,2010, Rhuggenaath etal.,2020]) by avoiding explicit iteration over the entire slate space. 
セミバンディット設定におけるアイテムレベルのフィードバックは、スロットごとの探索と活用を促進し、全体のスレート空間を明示的に反復することを避けることによって、$N^{O(1)}$のラウンドごとの複雑さを持つアルゴリズムの開発を可能にします（例：[Kale etal.,2010, Rhuggenaath etal.,2020]）。

It remains unclear how to achieve similar efficiency in the more challenging bandit feedback setting. 
より困難なバンディットフィードバック設定で同様の効率を達成する方法は不明のままです。

For example, directly applying state-of-the-art bandit algorithms[Lattimore and Szepesvári,2020] to the slate bandit problem (treating slates as arms) and selecting a slate by iterating through the $2^{\Omega(N)}$ sized set of all possible slates, results in exponential per-round time complexity. 
例えば、最先端のバンディットアルゴリズム[Lattimore and Szepesvári,2020]をスレートバンディット問題に直接適用し（スレートをアームとして扱う）、$2^{\Omega(N)}$サイズのすべての可能なスレートのセットを反復してスレートを選択すると、指数的なラウンドごとの時間複雑性が生じます。

Motivated by these challenges, our work introduces efficient and optimal algorithms for the logistic contextual slate bandit problem under bandit feedback, assuming time-varying item features and rewards generated from a global logistic model. 
これらの課題に動機づけられ、私たちの研究は、バンディットフィードバックの下でのロジスティック文脈スレートバンディット問題に対する効率的かつ最適なアルゴリズムを導入し、時間変化するアイテムの特徴とグローバルロジスティックモデルから生成される報酬を仮定します。

We make the following contributions. 
私たちは以下の貢献を行います。



### 1.1 Our Contributions 私たちの貢献

1. We propose two new algorithms Slate-GLM-OFU and Slate-GLM-TS that solve the logistic contextual slate bandit problem under bandit feedback. 
1. 私たちは、バンディットフィードバックの下でロジスティックコンテキストスレートバンディット問題を解決するために、Slate-GLM-OFUとSlate-GLM-TSという2つの新しいアルゴリズムを提案します。
While Slate-GLM-OFU is based on the OFU (Optimization in the Face of Uncertainty) paradigm, Slate-GLM-TS follows the Thompson Sampling (TS) paradigm. 
Slate-GLM-OFUはOFU（不確実性に直面した最適化）パラダイムに基づいているのに対し、Slate-GLM-TSはトンプソンサンプリング（TS）パラダイムに従います。
Under a diversity assumption (Assumption 2.1), we prove that Slate-GLM-OFU incurs a regret of $\tilde{O}(dN\sqrt{T})$ with high probability. 
多様性の仮定（仮定2.1）の下で、Slate-GLM-OFUが高い確率で$\tilde{O}(dN\sqrt{T})$の後悔を被ることを証明します。
Here, $d$ is the dimensionality of the items in the slate, $N$ is the number of slots and $T$ is the total number of rounds the algorithm is run for. 
ここで、$d$はスレート内のアイテムの次元数、$N$はスロットの数、$T$はアルゴリズムが実行される総ラウンド数です。
Both algorithms explore and exploit at the slot level and thus have a per round time complexity that grows polynomially in $N$ and $\log T$, making them feasible in practice. 
両方のアルゴリズムはスロットレベルで探索と活用を行い、そのため、1ラウンドあたりの時間計算量は$N$と$\log T$に対して多項式的に成長し、実際に実行可能です。

2. We also propose a fixed arm version Slate-GLM-TS-Fixed of the Slate-GLM-TS algorithm for the non-contextual (fixed arm) setting. 
私たちは、非コンテキスト（固定アーム）設定のためにSlate-GLM-TSアルゴリズムの固定アームバージョンSlate-GLM-TS-Fixedも提案します。
Using an assumption similar to Assumption 2.1, we prove an $O(d^{3/2}N^{3/2}\sqrt{T})$ regret guarantee for Slate-GLM-TS-Fixed. 
仮定2.1に類似した仮定を使用して、Slate-GLM-TS-Fixedに対する$O(d^{3/2}N^{3/2}\sqrt{T})$の後悔保証を証明します。
Similar to Slate-GLM-TS, Slate-GLM-TS-Fixed also explores and exploits at the slot level and has per round complexity polynomial in $N$ and $\log T$. 
Slate-GLM-TSと同様に、Slate-GLM-TS-Fixedもスロットレベルで探索と活用を行い、$N$と$\log T$に対して多項式的な1ラウンドあたりの計算量を持ちます。

3. We perform extensive experiments to validate the performance of our algorithms for both the contextual and the non-contextual settings. 
私たちは、コンテキスト設定と非コンテキスト設定の両方に対するアルゴリズムの性能を検証するために広範な実験を行います。
Under a wide range of randomly selected instances, we see that Slate-GLM-OFU incurs the least regret compared to all baselines and Slate-GLM-TS, Slate-GLM-TS-Fixed are competitive with other state-of-the-art algorithms. 
広範囲にわたるランダムに選択されたインスタンスの下で、Slate-GLM-OFUがすべてのベースラインと比較して最も少ない後悔を被り、Slate-GLM-TS、Slate-GLM-TS-Fixedは他の最先端アルゴリズムと競争力があることがわかります。
We also evaluate the maximum and average per round time complexity of our algorithms and compare it to the time complexities of the baselines. 
私たちはまた、アルゴリズムの最大および平均の1ラウンドあたりの時間計算量を評価し、それをベースラインの時間計算量と比較します。
Our algorithms are exponentially (most of the time) faster than all baselines. 
私たちのアルゴリズムは、すべてのベースラインよりも指数関数的に（ほとんどの時間）速いです。

4. Finally, we use our algorithm Slate-GLM-OFU to select in-context examples for tuning prompts of language models, applied to binary classification tasks. 
最後に、私たちはアルゴリズムSlate-GLM-OFUを使用して、バイナリ分類タスクに適用される言語モデルのプロンプトを調整するためのインコンテキスト例を選択します。
We perform experiments on two datasets SST2 and Yelp Review and achieve a competitive test accuracy of ∼80%. 
私たちは2つのデータセットSST2とYelp Reviewで実験を行い、約80%の競争力のあるテスト精度を達成します。
making it a possible alternative in practical prompt tuning scenarios. 
これにより、実際のプロンプト調整シナリオにおける可能な代替手段となります。



### 1.2 Related Work 関連研究

Online slate bandits have received significant attention due to their wide applicability in applications such as recommendations and advertising[Hill etal.,2017, Chen etal.,2021, Dimakopoulou etal.,2019], however, there are only a few theoretical studies that provide regret guarantees[Kale etal.,2010, Rhuggenaath etal.,2020]. 
オンラインスレートバンディットは、推薦や広告などのアプリケーションにおける広範な適用性のために大きな注目を集めていますが、後悔保証を提供する理論的研究はほとんどありません。

While these papers make progress on the slate bandit problem, neither do they address the contextual setting, nor do they accommodate bandit feedback which are the main motivations of our work. 
これらの論文はスレートバンディット問題に関して進展をもたらしていますが、文脈設定に対処しておらず、また、私たちの研究の主な動機であるバンディットフィードバックにも対応していません。

Theoretical analysis might be feasible for the Thompson Sampling approach in Dimakopoulou etal. [2019], but proving optimal guarantees might still be hard since their algorithm assigns equal rewards to all slots in order to maintain slot level policies for efficiency purposes. 
Dimakopoulou etal. [2019]のThompson Samplingアプローチに対する理論的分析は可能かもしれませんが、彼らのアルゴリズムは効率のためにスロットレベルのポリシーを維持するためにすべてのスロットに等しい報酬を割り当てるため、最適な保証を証明することは依然として難しいかもしれません。

However, we would like to acknowledge that in our experiments (Section 5), for the fixed arms setting, we found their algorithm to be quite competitive to ours on the instances we considered. 
しかし、私たちは実験（セクション5）において、固定アーム設定の場合、彼らのアルゴリズムが私たちのアルゴリズムと比較してかなり競争力があることを認めたいと思います。

One way of achieving optimal regret guarantees for the slate bandit problem is to reduce it to the canonical logistic bandit problem by considering each candidate slate as a separate arm and then using state of the art algorithms such as those in [Faury etal.,2020, Abeille etal.,2021, Faury etal.,2022]. 
スレートバンディット問題に対する最適な後悔保証を達成する一つの方法は、各候補スレートを別々のアームとして考慮し、[Faury etal.,2020, Abeille etal.,2021, Faury etal.,2022]のような最先端のアルゴリズムを使用することによって、それを標準的なロジスティックバンディット問題に還元することです。

While these algorithms do achieve optimal ($\kappa$) regret, they are infeasible in practice. 
これらのアルゴリズムは最適な ($\kappa$) 後悔を達成しますが、実際には実行不可能です。

During the arm selection step they require an iteration through all the arms which is a $2^{\Omega(N)}$ sized set, thereby incurring exponential time per round. 
アーム選択ステップでは、すべてのアームを通じて反復する必要があり、これはサイズが $2^{\Omega(N)}$ のセットであるため、各ラウンドで指数時間がかかります。

Even though these algorithms are inefficient for the slate bandit problem, we combine some of their key ideas with an efficient planning approach to design our algorithms. 
これらのアルゴリズムはスレートバンディット問題に対して非効率的であるにもかかわらず、私たちは彼らのいくつかの重要なアイデアを効率的な計画アプローチと組み合わせてアルゴリズムを設計します。

In Section 5, we demonstrate that our algorithms perform better than these state of the art logistic bandit algorithms both in regret and time complexity, when applied to a wide variety of slate bandit instances. 
セクション5では、私たちのアルゴリズムがさまざまなスレートバンディットインスタンスに適用された際に、これらの最先端のロジスティックバンディットアルゴリズムよりも後悔と時間計算量の両方で優れていることを示します。

Recently a large number of works [Swaminathan etal.,2017, Kiyohara etal.,2024, Vlassis etal.,2024] have studied the slate bandit problem in the off-policy setting, wherein they utilize a dataset collected using some base policy to find optimal slate bandit policies. 
最近、多くの研究[Swaminathan etal.,2017, Kiyohara etal.,2024, Vlassis etal.,2024]がオフポリシー設定におけるスレートバンディット問題を研究しており、そこで彼らはある基本ポリシーを使用して収集したデータセットを利用して最適なスレートバンディットポリシーを見つけています。

While these works have made significant progress both from the theoretical and practical sides, they are not relevant to our work since we focus on the online setting only. 
これらの研究は理論的および実践的な側面の両方で重要な進展を遂げていますが、私たちはオンライン設定のみに焦点を当てているため、私たちの研究には関連性がありません。



## 2 Preliminaries 前提条件

In this section, we define the notations used in the paper. 
このセクションでは、論文で使用される表記法を定義します。

Following this, we formulate the Slate Bandits problem and present the assumptions that enable us to prove the regret guarantee provided in Theorem 3.1 and Theorem C.1. 
次に、Slate Bandits問題を定式化し、定理3.1および定理C.1で提供される後悔保証を証明するための仮定を示します。

#### Notations 表記法

The set $\{1,2,\ldots,N\}$ is denoted as $[N]$. 
集合 $\{1,2,\ldots,N\}$ は $[N]$ と表記されます。

Unless otherwise specified, we use bold upper case letters for matrices, bold lower case letters for vectors, and upper case calligraphic symbols or greek letters for sets. 
特に指定がない限り、行列には太字の大文字、ベクトルには太字の小文字、集合には大文字のカリグラフィック記号またはギリシャ文字を使用します。

For any matrix $\mathbf{A}$, we denote its minimum and maximum eigenvalues as $\lambda_{min}(\mathbf{A})$ and $\lambda_{max}(\mathbf{A})$ respectively. 
任意の行列 $\mathbf{A}$ に対して、その最小固有値を $\lambda_{min}(\mathbf{A})$、最大固有値を $\lambda_{max}(\mathbf{A})$ と表記します。

We write $\mathbf{A} \succcurlyeq 0$, if matrix $\mathbf{A}$ is positive semi-definite and $\mathbf{A} \succcurlyeq \mathbf{B}$, if $\mathbf{A} - \mathbf{B} \succcurlyeq 0$. 
行列 $\mathbf{A}$ が正半定値である場合、$\mathbf{A} \succcurlyeq 0$ と書き、$\mathbf{A} - \mathbf{B} \succcurlyeq 0$ の場合は $\mathbf{A} \succcurlyeq \mathbf{B}$ と書きます。

For a positive semi-definite matrix $\mathbf{A}$, we define the norm of a vector $\mathbf{x}$ with respect to $\mathbf{A}$ as $\|\mathbf{x}\|_{\mathbf{A}} = \sqrt{\mathbf{x}^{\top} \mathbf{A} \mathbf{x}}$. 
正半定値行列 $\mathbf{A}$ に対して、ベクトル $\mathbf{x}$ の $\mathbf{A}$ に関するノルムを $\|\mathbf{x}\|_{\mathbf{A}} = \sqrt{\mathbf{x}^{\top} \mathbf{A} \mathbf{x}}$ と定義します。

and the spectral norm of $\mathbf{A}$ as $\|\mathbf{A}\|_{2} = \sqrt{\lambda_{max}(\mathbf{A}^{\top} \mathbf{A})}$. 
また、$\mathbf{A}$ のスペクトルノルムを $\|\mathbf{A}\|_{2} = \sqrt{\lambda_{max}(\mathbf{A}^{\top} \mathbf{A})}$ とします。

We use $\mathbf{I}_{m}$ and $\mathbf{0}_{m}$ to denote the $m \times m$ identity and zero matrices respectively. 
$m \times m$ の単位行列とゼロ行列をそれぞれ $\mathbf{I}_{m}$ と $\mathbf{0}_{m}$ で表します。

When the dimension $m$ is clear from the context, we use $\mathbf{I}$ and $\mathbf{0}$ instead. 
次元 $m$ が文脈から明らかな場合、$\mathbf{I}$ と $\mathbf{0}$ を代わりに使用します。

The symbols $\mathbb{P}$ and $\mathbb{E}$ denote probability and expectation respectively. 
記号 $\mathbb{P}$ と $\mathbb{E}$ はそれぞれ確率と期待値を表します。

For sets $\mathcal{A}, \mathcal{X}$ that are subsets of some ambient space $\mathbb{R}^{m}$, we define the diameter of $\mathcal{X}$ as $\text{diam}(\mathcal{X}) = \max_{\bm{x}_{1}, \bm{x}_{2} \in \mathcal{X}} \|\bm{x}_{1} - \bm{x}_{2}\|_{2}$. 
ある環境空間 $\mathbb{R}^{m}$ の部分集合である集合 $\mathcal{A}, \mathcal{X}$ に対して、$\mathcal{X}$ の直径を $\text{diam}(\mathcal{X}) = \max_{\bm{x}_{1}, \bm{x}_{2} \in \mathcal{X}} \|\bm{x}_{1} - \bm{x}_{2}\|_{2}$ と定義します。

and the diameter with respect to $\mathcal{A}$ as $\text{diam}_{\mathcal{A}}(\mathcal{X}) = \max_{\bm{a} \in \mathcal{A}} \max_{\bm{x}_{1}, \bm{x}_{2} \in \mathcal{X}} |\bm{a}^{\top}(\bm{x}_{1} - \bm{x}_{2})|$. 
また、$\mathcal{A}$ に関する直径を $\text{diam}_{\mathcal{A}}(\mathcal{X}) = \max_{\bm{a} \in \mathcal{A}} \max_{\bm{x}_{1}, \bm{x}_{2} \in \mathcal{X}} |\bm{a}^{\top}(\bm{x}_{1} - \bm{x}_{2})|$ とします。



### 2.1 Slate Bandits

In the Slate Bandits problem, a learner interacts with the environment over $T$ rounds. 
Slate Bandits問題では、学習者が$T$ラウンドにわたって環境と相互作用します。

At each round $t \in [T]$, the learner is presented with $N$ finite sets $\mathcal{X}^{i}_{t} \subset \mathbb{R}^{d}$, $i \in [N]$, of items and is expected to select one item (say $\mathbf{x}^{i}_{t}$) from each $\mathcal{X}^{i}_{t}$. 
各ラウンド$t \in [T]$で、学習者はアイテムの有限集合$ \mathcal{X}^{i}_{t} \subset \mathbb{R}^{d}$（$i \in [N]$）を提示され、各$\mathcal{X}^{i}_{t}$から1つのアイテム（例えば$\mathbf{x}^{i}_{t}$）を選択することが期待されます。

Based on the selected $N$-tuple $\mathbf{x}_{t} = (\mathbf{x}^{1}_{t}, \ldots, \mathbf{x}^{N}_{t})$ (called a “slate”), the learner receives a stochastic binary reward $y_{t}(\mathbf{x}_{t})$. 
選択された$N$-タプル$\mathbf{x}_{t} = (\mathbf{x}^{1}_{t}, \ldots, \mathbf{x}^{N}_{t})$（「スレート」と呼ばれる）に基づいて、学習者は確率的な二項報酬$y_{t}(\mathbf{x}_{t})$を受け取ります。

The learner’s goal is to select slates $\mathbf{x}_{t}, t \in [T]$ such that her expected regret, $R(T)$, is minimized. 
学習者の目標は、期待される後悔$R(T)$を最小化するようにスレート$\mathbf{x}_{t}, t \in [T]$を選択することです。

Here, $\mathcal{X}_{t}$ denotes the set $\mathcal{X}^{1}_{t} \times \ldots \times \mathcal{X}^{N}_{t}$ of all possible slates at round $t$. 
ここで、$\mathcal{X}_{t}$はラウンド$t$におけるすべての可能なスレートの集合$\mathcal{X}^{1}_{t} \times \ldots \times \mathcal{X}^{N}_{t}$を示します。

When the chosen slate $\mathbf{x}_{t}$ is clear from the context, for simplicity, we will denote $y_{t}(\mathbf{x}_{t})$ as $y_{t}$. 
選択されたスレート$\mathbf{x}_{t}$が文脈から明らかな場合、簡単のために$y_{t}(\mathbf{x}_{t})$を$y_{t}$と表記します。

For convenience, we say that the slate $\mathbf{x}_{t}$ comprises of $N$ “slots”, and the item $\mathbf{x}^{i}_{t}$ is placed in slot $i$ in the slate. 
便宜上、スレート$\mathbf{x}_{t}$は$N$の「スロット」で構成され、アイテム$\mathbf{x}^{i}_{t}$はスレートのスロット$i$に配置されるといいます。

In this work, we consider two well known settings; (a) Stochastic Contextual and (b) Non-Contextual (also known as Fixed-Arm setting). 
本研究では、2つのよく知られた設定を考慮します。(a) 確率的文脈設定と(b) 非文脈設定（固定アーム設定とも呼ばれる）です。

In the first setting, we assume that at every round $t \in [T]$, the set $\mathcal{X}^{i}_{t}$ is constructed by sampling from a distribution (unknown to the learner) $\mathbb{D}_{i}$, in an i.i.d fashion. 
最初の設定では、各ラウンド$t \in [T]$で、集合$\mathcal{X}^{i}_{t}$は（学習者には未知の）分布$\mathbb{D}_{i}$からサンプリングすることによって構成されると仮定します。

Moreover, $\mathcal{X}^{i}_{t}$ and $\mathcal{X}^{j}_{s}$ are sampled independently of one another, for all $s, t \in [T]$ and $i, j \in [N]$. 
さらに、すべての$s, t \in [T]$および$i, j \in [N]$に対して、$\mathcal{X}^{i}_{t}$と$\mathcal{X}^{j}_{s}$は互いに独立にサンプリングされます。

In the second setting, we assume $\mathcal{X}^{i}_{t}$ remains fixed over time. 
2番目の設定では、$\mathcal{X}^{i}_{t}$が時間とともに固定されると仮定します。

Thus, in this setting, for simplicity, we denote $\mathcal{X}^{i}_{t}$ by $\mathcal{X}^{i}$. 
したがって、この設定では、簡単のために$\mathcal{X}^{i}_{t}$を$\mathcal{X}^{i}$と表記します。

#### Logistic rewards

In this paper, we assume that the binary reward variable $y_{t}$ comes from a Logistic Model. 
本論文では、二項報酬変数$y_{t}$がロジスティックモデルから来ると仮定します。

Therefore, $\mathbb{P}[y_{t}=1 \mid \mathbf{x}_{t}] = \mu(\mathbf{x}_{t}^{\top} \bm{\theta}^{\star})$, where $\mu: \mathbb{R} \rightarrow \mathbb{R}$ is the logistic function, i.e., $\mu(a) = 1/(1+\exp(-a))$, and $\mathbf{\theta}^{\star} \in \mathbb{R}^{dN}$ is an unknown $d \times N$ dimensional parameter vector. 
したがって、$\mathbb{P}[y_{t}=1 \mid \mathbf{x}_{t}] = \mu(\mathbf{x}_{t}^{\top} \bm{\theta}^{\star})$、ここで$\mu: \mathbb{R} \rightarrow \mathbb{R}$はロジスティック関数であり、すなわち$\mu(a) = 1/(1+\exp(-a))$、そして$\mathbf{\theta}^{\star} \in \mathbb{R}^{dN}$は未知の$d \times N$次元のパラメータベクトルです。

Similar to prior works on Logistic bandits, we assume that $\|\theta^{\star}\|_{2} \leq S$, where $S$ is known to the learner, and $\|\mathbf{x}^{i}\|_{2} \leq 1/\sqrt{N}$, for all $\mathbf{x}^{i} \in \mathcal{X}^{i}_{t}, i \in [N], t \in [T]$. 
ロジスティックバンディットに関する先行研究と同様に、$\|\theta^{\star}\|_{2} \leq S$と仮定します。ここで$S$は学習者に知られており、すべての$\mathbf{x}^{i} \in \mathcal{X}^{i}_{t}, i \in [N], t \in [T]$に対して$\|\mathbf{x}^{i}\|_{2} \leq 1/\sqrt{N}$です。

Recent logistic bandit literature also identifies a critical parameter $\kappa$, that captures the non-linearity of the reward for the given problem instance, defined as follows. 
最近のロジスティックバンディット文献では、与えられた問題インスタンスの報酬の非線形性を捉える重要なパラメータ$\kappa$も特定されています。

$$
\Theta = \{\|\theta\|_{2} \leq S\} \subset \mathbb{R}^{dN}.
$$
$$
\Theta = \{\|\theta\|_{2} \leq S\} \subset \mathbb{R}^{dN}.
$$

The parameter $\kappa$ can be intuitively seen as the mismatch between the true reward function and a linear approximation of the same. 
パラメータ$\kappa$は、真の報酬関数とその線形近似との不一致として直感的に理解できます。

Developing algorithms with regret independent of $\kappa$ has gained significant attention recently and is an active area of research. 
$\kappa$に依存しない後悔を持つアルゴリズムの開発は最近注目を集めており、活発な研究分野です。

We refer the reader to Section 2 of Faury et al. [2020] for a thorough discussion on $\kappa$ and its implications on regret analysis. 
$\kappa$とその後悔分析への影響についての詳細な議論は、Faury et al. [2020]のセクション2を参照してください。

#### Assumption 2.1

(Diversity Assumption) We describe a key assumption that enables us to design algorithms with low per-round computational complexity and strong regret guarantees (Theorem 3.1 in Section 3 and Theorem C.1 in Appendix C). 
（多様性の仮定）我々は、各ラウンドの計算複雑性が低く、強力な後悔保証を持つアルゴリズムを設計することを可能にする重要な仮定を説明します（セクション3の定理3.1および付録Cの定理C.1）。

Let $\mathcal{F}_{t}$ be the sigma algebra generated by $\{\mathbf{x}_{1}, y_{1}, \ldots, \mathbf{x}_{t-1}, y_{t-1}\}$ and $\phi = \mathcal{F}_{0} \subset \mathcal{F}_{1} \subset \ldots \mathcal{F}_{T}$ be the associated filtration. 
$\mathcal{F}_{t}$を$\{\mathbf{x}_{1}, y_{1}, \ldots, \mathbf{x}_{t-1}, y_{t-1}\}$によって生成されるシグマ代数とし、$\phi = \mathcal{F}_{0} \subset \mathcal{F}_{1} \subset \ldots \mathcal{F}_{T}$を関連するフィルトレーションとします。

For each $i \in [N], t \in [T]$, we assume that, 
各$i \in [N], t \in [T]$に対して、次のように仮定します。

where $\rho > 0$ is a fixed constant and $\kappa$ is the non-linearity parameter defined earlier in Section 2. 
ここで、$\rho > 0$は固定定数であり、$\kappa$はセクション2で定義された非線形性パラメータです。

#### Remarks on Assumption 2.1:

The assumption intuitively means that for each slot $i \in [N]$ and round $t \in [T]$, the item features $\mathbf{x}^{i}_{t}$ that can be selected by the algorithm are sufficiently “diverse”, i.e., the expected matrix $\mathbb{E}[\mathbf{x}^{i}_{t}{\mathbf{x}^{i}_{t}}^{\top} \mid \mathcal{F}_{t}]$ is full rank and has sufficiently large eigenvalues. 
この仮定は直感的には、各スロット$i \in [N]$およびラウンド$t \in [T]$に対して、アルゴリズムによって選択可能なアイテムの特徴$\mathbf{x}^{i}_{t}$が十分に「多様」であることを意味します。すなわち、期待行列$\mathbb{E}[\mathbf{x}^{i}_{t}{\mathbf{x}^{i}_{t}}^{\top} \mid \mathcal{F}_{t}]$がフルランクであり、十分に大きな固有値を持つことを示します。

In our proofs, this assumption is used to first prove that with high probability the minimum eigenvalue of certain design matrices $\mathbf{W}^{i}_{t}$ grows (sufficiently) linearly with $t$. 
私たちの証明では、この仮定は、まず特定の設計行列$\mathbf{W}^{i}_{t}$の最小固有値が高い確率で$t$に対して（十分に）線形に成長することを証明するために使用されます。

In particular, we show that 
特に、次のことを示します。

$$
\lambda_{min}(\mathbf{W}^{i}_{t}) \geq \gamma + c \rho \kappa t,
$$
$$
\lambda_{min}(\mathbf{W}^{i}_{t}) \geq \gamma + c \rho \kappa t,
$$

for a fixed constant $c > 0$. 
ここで、$c > 0$は固定定数です。

We critically utilize this linear growth of the minimum eigenvalue to prove multiplicative equivalence between the block diagonal matrix $\mathbf{U}_{t} = \text{diag}(\mathbf{W}^{1}_{t}, \ldots, \mathbf{W}^{N}_{t})$ and a similarly defined slate-level design matrix $\mathbf{W}_{t}$. 
私たちはこの最小固有値の線形成長を重要に利用して、ブロック対角行列$\mathbf{U}_{t} = \text{diag}(\mathbf{W}^{1}_{t}, \ldots, \mathbf{W}^{N}_{t})$と同様に定義されたスレートレベルの設計行列$\mathbf{W}_{t}$との間の乗法的同等性を証明します。

As a result of this multiplicative equivalence, we are able to use slot level exploration bonuses (leading to low per round time complexity in Algorithms 1, 3 and 4), and still continue to have optimal regret. 
この乗法的同等性の結果として、スロットレベルの探索ボーナスを使用することができ（アルゴリズム1、3、4における各ラウンドの時間計算量が低くなります）、それでも最適な後悔を維持し続けることができます。

Details of the algorithm and the regret proof can be found in Sections 3, 4 and Appendix C. 
アルゴリズムの詳細と後悔の証明は、セクション3、4および付録Cに記載されています。

We would like to highlight that many similar diversity assumptions have been used in the literature and connections between them have also been studied. 
多くの類似の多様性の仮定が文献で使用されており、それらの間の関連性も研究されていることを強調したいと思います。

Depending on the strength of the assumption, novel and stronger regret guarantees for well-known algorithms have been established. 
仮定の強さに応じて、よく知られたアルゴリズムに対する新しいより強力な後悔保証が確立されています。

Interestingly, their regret proofs also proceed by first showing a linear lower bound on the minimum eigenvalue of the design matrix. 
興味深いことに、彼らの後悔の証明も、まず設計行列の最小固有値に対する線形下限を示すことから進みます。

Since the assumption is instance/algorithm dependent, there could be instances where the linear lower bound might not hold. 
この仮定はインスタンス/アルゴリズムに依存するため、線形下限が成り立たないインスタンスも存在する可能性があります。

To study this, we empirically examine the growth of the minimum eigenvalues for a large number of randomly chosen instances and see a clear linear trend validating the assumption, at least for these randomly picked instances. 
これを研究するために、ランダムに選ばれた多数のインスタンスに対して最小固有値の成長を経験的に調査し、少なくともこれらのランダムに選ばれたインスタンスに対して仮定を検証する明確な線形傾向を確認します。

More details can be found in Appendix G. 
詳細は付録Gに記載されています。



## 3Slate-GLM-OFU

3
Slate-GLM-OFU
アルゴリズム 1
Algorithm 1
Slate-GLM-OFU
1:
入力:
Inputs:
2:
3:
for
do
4:
5:
6:
2
7:
end
for
アルゴリズム 2
Algorithm 2
ada-OFU-ECOLog-Updates
1:
入力:
Inputs:
2:
3:
3
4
4:
if
then
5:
5
6:
7:
8:
9:
else
10:
11:
6
12:
13:
14:
15:
end
if
16:
return
このセクションでは、バンディットアルゴリズムで使用されるOFU（不確実性に直面した最適化）パラダイムに基づく最初のアルゴリズムSlate-GLM-OFU（アルゴリズム1）を提示します。
In this section, we present our first algorithm Slate-GLM-OFU (Algorithm 1) based on the OFU (Optimization in the Face of Uncertainty) paradigm used in bandit algorithms.
高レベルでは、Slate-GLM-OFU（サブルーチンアルゴリズム2とともに）は、最適な（κフリー）$O(\sqrt{T})$の後悔保証を達成し、$O(K\log T)$のラウンドごとの計算コストを発生させるada-OFU-ECOLogアルゴリズム（Faury et al. [2022]のアルゴリズム2）に基づいています。
At a high level, Slate-GLM-OFU (along with sub-routine Algorithm 2) builds upon the ada-OFU-ECOLog algorithm (Algorithm 2 in Faury et al. [2022]) which achieves an optimal ($\kappa$-free) $O(\sqrt{T})$ regret guarantee and incurs $O(K\log T)$ per round computational cost, where $K$ is the total number of actions to choose from.
スレートバンディット設定では、$K$はスレート内のスロットの数$N$に対して指数的であり、$N$が大きい場合にada-OFU-ECOLogの直接適用は実行不可能です。
In the slate bandit setting, $K$ is exponential in $N$, the number of slots in the slate, making a direct application of ada-OFU-ECOLog infeasible when $N$ is large.
これに対処するために、Slate-GLM-OFUは各スロットのアイテムを独立して選択し、ラウンドごとの計算コストを$N^{O(1)}$に削減します。
To address this, Slate-GLM-OFU selects an item for each slot independently, reducing the per round computational cost to $N^{O(1)}$.
興味深いことに、スレートを構築するためにアイテムを独立して選択するにもかかわらず、Slate-GLM-OFU（サブルーチンアルゴリズム2を介して）は、スレートレベルの報酬フィードバックを使用して単一の報酬モデルのみを推定します。
Interestingly, despite the independent selection of items to build the slate, Slate-GLM-OFU (via sub-routine Algorithm 2) estimates only a single reward model using the slate level reward feedback.
これは、スレート内の個々のアイテムに単一のスレートレベルの報酬フィードバックを帰属させ、$N$個の別々の報酬モデルを推定するスレートバンディットに関する以前の研究との重要な違いです。
This is a critical difference with respect to prior works on slate bandits with bandit feedback which attribute the single slate level reward feedback to individual items in the slate and estimates $N$ separate reward models.
Slate-GLM-OFU
1
Slate-GLM-OFU
2
ada-OFU-ECOLog
ada-OFU-ECOLog
Slate-GLM-OFU
Slate-GLM-OFU
2
Slate-GLM-OFUへの入力は、$T, \delta$および$S$であり、ここで$T$は時間のホライズン、すなわちラウンドの総数、$\delta$は誤差確率、$S$は$\|\bm{\theta}^{\star}\|_{2}$の既知の上限です。
Input to Slate-GLM-OFU are $T, \delta$ and $S$, where $T$ is the time horizon i.e., the total number of rounds, $\delta$ is the error probability and $S$ is a known upper bound for $\|\bm{\theta}^{\star}\|_{2}$.
ada-OFU-ECOLog [Faury et al., 2022]と同様に、Slate-GLM-OFUはベクトル$\bm{\theta}_{t}$を維持し、$\Theta_{t}$および$\mathcal{H}_{t}$を設定します。
Similar to ada-OFU-ECOLog [Faury et al., 2022], Slate-GLM-OFU maintains vectors $\bm{\theta}_{t}$, and sets $\Theta_{t}$ and $\mathcal{H}_{t}$.
ベクトル$\bm{\theta}_{t}$は、$t$回目のラウンド中の$\bm{\theta}^{\star}$の推定値を提供します。
The vector $\bm{\theta}_{t}$ provides an estimate of $\bm{\theta}^{\star}$ during the $t^{th}$ round.
$\Theta_{t} \subseteq \Theta_{1} = \{\|\bm{\theta}\|_{2} \leq S\}$は、$\bm{\theta}_{t+1}$の値の許容集合であり、高い確率で真の報酬パラメータ$\bm{\theta}^{\star}$を含みます（詳細はFaury et al. [2022]の命題7を参照）。
Set $\Theta_{t} \subseteq \Theta_{1} = \{\|\bm{\theta}\|_{2} \leq S\}$ is an admissible set for the values of $\bm{\theta}_{t+1}$ and contains the true reward parameter $\bm{\theta}^{\star}$ with high probability (See Proposition 7 in Faury et al. [2022] for more details).
適応性を促進するために、ada-OFU-ECOLogは、ステップ3（アルゴリズム2）で説明される不等式基準が失敗するペア$(\mathbf{x}_{s}, y_{s}(\mathbf{x}_{s}))$からなる集合$\mathcal{H}_{t}$を導入しました。
In order to facilitate adaptivity, ada-OFU-ECOLog introduced the set $\mathcal{H}_{t}$ comprising pairs $(\mathbf{x}_{s}, y_{s}(\mathbf{x}_{s}))$ at which an inequality criterion (described in Step 3 of Algorithm 2) fails.
これに加えて、ada-OFU-ECOLogは、行列$\mathbf{W}_{t} = \lambda \mathbf{I} + \sum_{s=1}^{t-1} \dot{\mu}(\mathbf{x}_{s}^{\top} \bm{\theta}_{s+1}) \mathbf{x}_{s} \mathbf{x}_{s}^{\top}$を導入しました。
In addition to these, ada-OFU-ECOLog also introduces a matrix $\mathbf{W}_{t} = \lambda \mathbf{I} + \sum_{s=1}^{t-1} \dot{\mu}(\mathbf{x}_{s}^{\top} \bm{\theta}_{s+1}) \mathbf{x}_{s} \mathbf{x}_{s}^{\top}$.
これは、パラメータ推定の効率的なラウンドごとの計算を可能にするための集中行列のオンポリシー代理です。
This is an on-policy proxy for the concentration matrix to enable efficient per round computation of parameter estimates.
Slate-GLM-OFUでは、$\mathbf{W}_{t}$に加えて、$N$個の他のそのような行列（各スロット$i \in [N]$に1つ）を維持します。
In Slate-GLM-OFU, along with $\mathbf{W}_{t}$, we also maintain $N$ other such matrices (one for each slot $i \in [N]$).
これらの行列は、$i^{th}$スロットのアイテムを選択する際の探索と活用のトレードオフに役立ちます。
These matrices help us in the explore-exploit trade-off while selecting the item for the $i^{th}$ slot.
Slate-GLM-OFU
ada-OFU-ECOLog
Slate-GLM-OFU
ada-OFU-ECOLog
2
ada-OFU-ECOLog
Slate-GLM-OFU
次に、Slate-GLM-OFU（アルゴリズム1）とそのサブルーチン（アルゴリズム2）のステップを通じて、より詳細な説明を提供します。
Next we go through the steps of Slate-GLM-OFU (Algorithm 1) and its sub-routine (Algorithm 2) to provide a more detailed explanation.
ステップ3-7（アルゴリズム1）は、Slate-GLM-OFUがada-OFU-ECOLogと大きく異なる部分です。
Steps 3-7 (Algorithm 1) is where Slate-GLM-OFU differs significantly from ada-OFU-ECOLog.
スロット$i$の特徴セット$\mathcal{X}_{t}$（私たちの場合はスレート）を環境から直接取得する代わりに（ada-OFU-ECOLogのように）、Slate-GLM-OFUは各スロット$i \in [N]$に対して$N$個の異なるアイテムセット$\mathcal{X}_{t}^{i}$を受け取ります。
Instead of getting the set of arm features $\mathcal{X}_{t}$ (slates in our case) directly from the environment (as in ada-OFU-ECOLog), Slate-GLM-OFU receives $N$ different sets of items $\mathcal{X}_{t}^{i}$ for each slot $i \in [N]$.
次に、ステップ4（アルゴリズム1）で言及された楽観的ルールを使用して、1つのアイテム$\mathbf{x}_{t}^{i} \in \mathcal{X}_{t}^{i}$を選択します。
Then, it picks one item $\mathbf{x}_{t}^{i} \in \mathcal{X}_{t}^{i}$ using the optimistic rule mentioned in Step 4 (Algorithm 1).
スロット$i$の基礎となる最適化問題は、$\mathcal{X}_{t}^{i}$の候補アイテムと、$i^{th}$スロットに対応する$\bm{\theta}_{t}^{i}$の成分のみを必要とし、したがって、すべてのスロットに対して独立して並行して解決できます。
Note that, the underlying optimization problem for slot $i$, only requires the candidate items in $\mathcal{X}_{t}^{i}$ and the components $\bm{\theta}_{t}^{i}$ of $\bm{\theta}_{t}$ that correspond to the $i^{th}$ slot, and thus, can be solved independently and in parallel for all slots.
スロットレベルでアイテムを独立して選択することがスレートレベルでの最適な選択につながる理由は非常に興味深く、私たちの後悔保証の核心的な技術的部分を構成します（定理3.1）。
Why the selection of items independently at the slot level leads to optimal selection at the slate level is quite interesting and constitutes the core technical part of our regret guarantee (Theorem 3.1).
本質的に、私たちは、私たちの多様性の仮定（仮定2.1）の下で、正定値行列$\mathbf{W}_{t}$と$\text{diag}(\mathbf{W}_{t}^{1}, \ldots, \mathbf{W}_{t}^{N})$が乗法的に同等であることを示すことができます。
Essentially, we can show that, under our diversity assumption (Assumption 2.1), the positive definite matrices $\mathbf{W}_{t}$ and $\text{diag}(\mathbf{W}_{t}^{1}, \ldots, \mathbf{W}_{t}^{N})$ are multiplicatively equivalent.
さらに、すべてのスレート$\mathbf{x}_{t} = (\mathbf{x}_{t}^{1}, \ldots, \mathbf{x}_{t}^{N})$に対して、量$\|\mathbf{x}_{t}\|_{\mathbf{W}_{t}}$と$\sum_{i \in [N]} \|\mathbf{x}_{t}^{i}\|_{\mathbf{W}_{t}^{i}}$は乗法的に同等であることを示唆しています。
This further implies that, for all slates $\mathbf{x}_{t} = (\mathbf{x}_{t}^{1}, \ldots, \mathbf{x}_{t}^{N})$, the quantities $\|\mathbf{x}_{t}\|_{\mathbf{W}_{t}}$ and $\sum_{i \in [N]} \|\mathbf{x}_{t}^{i}\|_{\mathbf{W}_{t}^{i}}$ are multiplicatively equivalent.
この観察は、スレートレベルでの楽観的選択ルールを各スロットの同等の楽観的選択ルールに変換するために、私たちのアルゴリズムで利用されます。
This observation is exploited in our algorithm to convert an optimistic selection rule at the slate level into an equivalent optimistic selection rule for each slot.
ステップ5（アルゴリズム1）では、スレート$\mathbf{x}_{t} = (\mathbf{x}_{t}^{1}, \ldots, \mathbf{x}_{t}^{N})$を選択し、報酬$y_{t}$を得ます。
In Step 5 (Algorithm 1), we select the slate $\mathbf{x}_{t} = (\mathbf{x}_{t}^{1}, \ldots, \mathbf{x}_{t}^{N})$, yielding a reward $y_{t}$.
この時点で、Slate-GLM-OFUはアルゴリズム2で説明されるサブルーチンを呼び出し、パラメータ$\bm{\theta}_{t}$、$\mathbf{W}_{t}$、$(\mathbf{W}_{t}^{1}, \ldots, \mathbf{W}_{t}^{N})$、$\Theta_{t}$、および$\mathcal{H}_{t}$を更新します。
At this point, Slate-GLM-OFU calls a sub-routine described in Algorithm 2 which updates the parameters $\bm{\theta}_{t}$, $\mathbf{W}_{t}$, $(\mathbf{W}_{t}^{1}, \ldots, \mathbf{W}_{t}^{N})$, $\Theta_{t}$, and $\mathcal{H}_{t}$.
アルゴリズム2の更新ルールは、ada-OFU-ECOLogのものに大きく従い、次の不等式基準に基づいています。
The update rules in Algorithm 2 largely follow the one in ada-OFU-ECOLog, which is based on the following inequality criterion.
Slate-GLM-OFU
1
2
1
Slate-GLM-OFU
ada-OFU-ECOLog
ada-OFU-ECOLog
Slate-GLM-OFU
1
3.1
2.1
1
Slate-GLM-OFU
2
2
ada-OFU-ECOLog
(2)
ここで、$\bar{\bm{\theta}}_{t}, \bm{\theta}_{t}^{0}, \bm{\theta}_{t}^{1} \in \mathbb{R}^{dN}$は、適応性を可能にするための$\mathcal{F}_{t}$-適応パラメータです。
Here $\bar{\bm{\theta}}_{t}, \bm{\theta}_{t}^{0}, \bm{\theta}_{t}^{1} \in \mathbb{R}^{dN}$ are $\mathcal{F}_{t}$-adapted parameters that enable adaptivity.
これらは次のように得られます。
They are obtained as follows.
(3)
(4)
ここで、$\ell(\mathbf{x}, y) = -y \log \mu(\mathbf{x}) - (1-y) \log(1-\mu(\mathbf{x}))$はクロスエントロピー損失であり、$\eta = (2 + \text{diam}(\Theta_{t}))^{-1}$です。
where $\ell(\mathbf{x}, y) = -y \log \mu(\mathbf{x}) - (1-y) \log(1-\mu(\mathbf{x}))$ is the cross entropy loss and $\eta = (2 + \text{diam}(\Theta_{t}))^{-1}$.
不等式(2)が成り立つとき、$\bm{\theta}_{t}, \mathbf{W}_{t}$および$\mathbf{W}_{t}^{i}$は、アルゴリズム2のステップ4-6で説明されるように更新されます。
When the inequality in (2) holds, $\bm{\theta}_{t}, \mathbf{W}_{t}$ and $\mathbf{W}_{t}^{i}$ are updated as described in Steps 4-6 (Algorithm 2).
まず、ステップ4では、$\bm{\theta}_{t+1}$が次の最適化問題を解くことによって計算されます。
First, in Step 4, $\bm{\theta}_{t+1}$ is computed by solving the following optimization problem up to a precision of $1/t$.
2
2
(5)
その後、$\mathbf{W}_{t}^{i}$および$\mathbf{W}_{t}$は、ステップ5およびステップ6でそれぞれの定義に従って更新されます。
Following this, $\mathbf{W}_{t}^{i}$ and $\mathbf{W}_{t}$ are updated in Step 5 and Step 6 as per their definitions provided earlier.
不等式(2)が成り立たない場合、$\mathcal{H}_{t}$および$\Theta_{t}$は、アルゴリズム2のステップ9-12で説明されるように更新されます。
When the inequality in (2) does not hold, $\mathcal{H}_{t}$ and $\Theta_{t}$ are updated as described in Steps 9-12 (Algorithm 2).
ステップ9では、不等式基準が失敗したため、$\mathcal{H}_{t}$はペア$(\mathbf{x}_{t}, y_{t})$を追加することによって$\mathcal{H}_{t+1}$に更新されます。
In Step 9, since the inequality criterion failed, $\mathcal{H}_{t}$ is updated to $\mathcal{H}_{t+1}$ by appending the pair $(\mathbf{x}_{t}, y_{t})$ to it.
この新しい推定値を使用して、ステップ10では、別の推定値$\bm{\theta}_{t+1}^{\mathcal{H}}$が、正則化されたクロスエントロピー損失を最小化することによって計算されます（精度は$1/t$まで）。
Using this estimate, and a design matrix $\mathbf{V}_{t}^{\mathcal{H}}$ computed in Step 11, in Step 12 the set $\Theta_{t}$ is updated to $\Theta_{t+1}$ by taking an intersection between a confidence set of radius $\beta_{t}(\delta) = O(dN\log(t/\delta))$ around the new estimate $\bm{\theta}_{t+1}^{\mathcal{H}}$ (that contains $\bm{\theta}^{\star}$ with probability $1 - \delta$) and the initial set $\Theta_{1} = \{\|\bm{\theta}\|_{2} \leq S\}$.
2
2.1
Slate-GLM-OFU
Remark: 定理3.1で定義されたように、$\mathcal{T}$を、$2$の不等式条件が失敗するまでのラウンドの集合とします。
Remark: Let $\mathcal{T}$ denote the set of rounds until the inequality condition in (2) fails, as defined in Theorem 3.1.
Slate-GLM-OFUのラウンドごとの時間計算量は、$O((dN\log t)^{2})$であり、ラウンド$t \in [T] \setminus \mathcal{T}$に対して、$O(Ndt)$です。
The per-round time complexity of Slate-GLM-OFU is $O((dN\log t)^{2})$ for rounds $t \in [T] \setminus \mathcal{T}$ and it is $O(Ndt)$ for rounds $t \in \mathcal{T}$.
Faury et al. [2022]の命題8は、$|\mathcal{T}| = O(\kappa dNS^{6})$を示唆しています。
Lemma 8 in Faury et al. [2022] implies that $|\mathcal{T}| = O(\kappa dNS^{6})$.
したがって、$O(Ndt)$のラウンドごとの計算量は、これらのラウンドに対してのみ発生します。
Thus, the $O(Ndt)$ per-round complexity is incurred for only these many rounds.
Remark:
3.1
Slate-GLM-OFU



## 4Slate-GLM-TS

4
Slate-GLM-TS
このセクションでは、バンディットアルゴリズムで使用されるトンプソンサンプリングパラダイムに基づく2番目のアルゴリズム、Slate-GLM-TS（アルゴリズム3）を紹介します。
In this section, we present our second algorithm, Slate-GLM-TS (Algorithm 3) based on the Thompson Sampling paradigm used in bandit algorithms.

Slate-GLM-TSは、TS-ECOLogアルゴリズム（付録D.2のアルゴリズム3333、Faury et al. [2022]）に基づいており、アルゴリズム2の更新戦略を使用して変化するアクションセットに適応します。
Slate-GLM-TS builds upon the TS-ECOLog algorithm (Algorithm 3333 in Appendix D.2, Faury et al. [2022]) while adapting to the changing action sets using the update strategy in Algorithm 2.

TS-ECOLogは、AbeilleとLazaric [2017]からの線形トンプソンサンプリングアルゴリズムを適応させ、適切に変換されたノイズベクトルを適切な多変量分布からサンプリングして推定されたパラメータベクトルに加えます。
TS-ECOLog adapts the Linear Thompson Sampling algorithm from Abeille and Lazaric [2017] that perturbs the estimated parameter vector by adding an appropriately transformed noise vector sampled from a suitable multivariate distribution.

このノイズベクトルは、いくつかの良い性質を満たす（AbeilleとLazaric [2017]の定義11を参照）多変量分布$\mathcal{D}^{TS}$からサンプリングされます。
This noise vector is sampled from a suitable multivariate distribution $\mathcal{D}^{TS}$ satisfying some nice properties (See Definition 11 of Abeille and Lazaric [2017]).

これに続いて、新しい摂動されたパラメータベクトルに関して最適なアクション（私たちの場合はスレート）が選択されます。
Following this, the optimal action (slate in our case) with respect to the new perturbed parameter vector is chosen.

TS-ECOLogは、固定アクションセットに対してロジスティック報酬モデルの最適な$O(T)$のレグレット保証を達成しますが、ada-OFU-ECOLogと同様に、スレートレベルでの選択のために、ラウンドごとの計算コストはアクションの数$K$に比例します。
While TS-ECOLog also achieves an optimal $O(T)$ regret guarantee for logistic reward models (for fixed action sets), similar to ada-OFU-ECOLog, it also incurs per round computational cost proportional to the number of actions $K$.

このため、Slate-GLM-TSはスロットレベルで動作し、各スロット$i \in [N]$に対して、他のすべてのスロットから独立にサンプリングされたノイズベクトルを使用して、推定されたパラメータベクトルの成分を摂動します。
To circumvent this, Slate-GLM-TS operates at the slot level and for each slot $i \in [N]$, it perturbs the components of the estimated parameter vector (corresponding to the $i^{th}$ slot) using a noise vector sampled independently of all other slots.

その後、各スロットの最適なアイテムを独立して選択し、スレートを選択する際のラウンドごとの時間計算量は$N^{O(1)}$となります。
This is followed by selecting the optimal items for each slot independently, thereby incurring an $N^{O(1)}$ per round time complexity in choosing the slate.

各スロットのアイテムは独立して決定されますが、Slate-GLM-OFUと同様に、Slate-GLM-TSも単一の報酬モデルを推定し、このモデルのパラメータベクトルをスレートレベルの報酬$y_t$を使用して共同で更新します。
While the items for each slot are independently determined, similar to Slate-GLM-OFU, Slate-GLM-TS also estimates a single reward model and updates the parameter vector for this model jointly using the slate level reward $y_t$, by employing the update strategy in Algorithm 2.

Slate-GLM-TS
3
Slate-GLM-TS
Slate-GLM-TSへの入力は、$T, \delta, S$と$\mathcal{D}^{TS}$であり、ここで$T$は時間のホライズン、すなわちラウンドの総数、$\delta$は誤差確率、$S$は$\|\bm{\theta}^{\star}\|_2$の既知の上限であり、$\mathcal{D}^{TS}$はAbeilleとLazaric [2017]の定義11の性質を満たす多変量分布です。
Input to Slate-GLM-TS are $T, \delta, S$ and $\mathcal{D}^{TS}$, where $T$ is the time horizon i.e., the total number of rounds, $\delta$ is the error probability, $S$ is a known upper bound for $\|\bm{\theta}^{\star}\|_2$ and $\mathcal{D}^{TS}$ is a multivariate distribution satisfying properties in Definition 11 in Abeille and Lazaric [2017].

アルゴリズムの過程で、Slate-GLM-TSはベクトル$\bm{\theta}_t$、行列$\mathbf{W}_t$、$\mathbf{W}_t^i$（$i \in [N]$）および集合$\Theta_t, \mathcal{H}_t$をSlate-GLM-OFUと同じ定義で維持します。
During the course of the algorithm, Slate-GLM-TS maintains vectors $\bm{\theta}_t$, matrices $\mathbf{W}_t$, $\mathbf{W}_t^i$ ($i \in [N]$) and sets $\Theta_t, \mathcal{H}_t$ with exactly the same definition as in Slate-GLM-OFU.

Slate-GLM-TS
Slate-GLM-TS
Slate-GLM-OFU
次に、Slate-GLM-TS（アルゴリズム3）のステップを説明します。ステップ3-10は、Slate-GLM-TSがTS-ECOLogと大きく異なる部分です。
Next, we go through the steps of Slate-GLM-TS (Algorithm 3). Steps 3-10 is where Slate-GLM-TS differs significantly from TS-ECOLog.

TS-ECOLogのように環境からアームの特徴セット$\mathcal{X}_t$（私たちの場合はスレート）を直接取得するのではなく、Slate-GLM-TSはステップ4で$N$個の異なるアイテムセット$\mathcal{X}_t^i, i \in [N]$を受け取ります。
Instead of getting the set of arm features $\mathcal{X}_t$ (slates in our case) directly from the environment (as in TS-ECOLog), Slate-GLM-TS receives $N$ different sets of items $\mathcal{X}_t^i, i \in [N]$ in Step 4.

TS-ECOLogは1つのノイズベクトル$\eta \in \mathbb{R}^{dN}$を$\mathcal{D}^{TS}$からサンプリングし、推定されたパラメータベクトル$\bm{\theta}_t$に$(\mathbf{W}_t)^{-1/2}\bm{\eta}$を加えることで摂動しますが、Slate-GLM-TSは$N$個のベクトル$\bm{\eta}_1, \ldots, \bm{\eta}_N$を独立にサンプリングし、$\bm{\theta}_t^i$の成分を摂動します。
While TS-ECOLog samples one noise vector $\eta \in \mathbb{R}^{dN}$ from $\mathcal{D}^{TS}$ and perturbs the estimated parameter vector $\bm{\theta}_t$ by adding $(\mathbf{W}_t)^{-1/2}\bm{\eta}$, Slate-GLM-TS independently samples $N$ such vectors $\bm{\eta}_1, \ldots, \bm{\eta}_N$ and perturbs the components $\bm{\theta}_t^i$ of $\bm{\theta}_t = (\bm{\theta}_t^1, \ldots, \bm{\theta}_t^N)$.

アルゴリズムは、摂動されたベクトル$\tilde{\bm{\theta}}_t = (\tilde{\bm{\theta}}_t^1, \ldots, \tilde{\bm{\theta}}_t^N)$が許容可能な集合$\Theta_t$に属するまで、これらのノイズベクトルをサンプリングし続けます。
The algorithm continues to sample these noise vectors until the perturbed vector $\tilde{\bm{\theta}}_t = (\tilde{\bm{\theta}}_t^1, \ldots, \tilde{\bm{\theta}}_t^N)$ belongs to the admissible set $\Theta_t$.

これが発生すると、ステップ11で、摂動されたパラメータベクトル$\tilde{\bm{\theta}}_t^i$に関して最適なアイテム$\mathbf{x}_t^i \in \mathcal{X}_t^i$を選択します。
Once this happens, in Step 11, it picks the item $\mathbf{x}_t^i \in \mathcal{X}_t^i$, which is optimal with respect to the perturbed parameter vector $\tilde{\bm{\theta}}_t^i$.

スロット$i$の基礎となる最適化問題は、候補アイテム$\mathcal{X}_t^i$と摂動されたベクトル$\tilde{\bm{\theta}}_t^i$のみを必要とし、したがって、すべてのスロットに対して独立して並行して解決できます。
Note that, the underlying optimization problem for slot $i$, only requires the candidate items in $\mathcal{X}_t^i$ and the perturbed vectors $\tilde{\bm{\theta}}_t^i$, and thus, can be solved independently and in parallel for all slots.

Slate-GLM-TS
3
Slate-GLM-TS
TS-ECOLog
TS-ECOLog
Slate-GLM-TS
TS-ECOLog
Slate-GLM-TS
ステップ12では、スレート$\mathbf{x}_t = (\mathbf{x}_t^1, \ldots, \mathbf{x}_t^N)$を選択し、報酬$y_t$を得ます。
In Step 12, we select the slate $\mathbf{x}_t = (\mathbf{x}_t^1, \ldots, \mathbf{x}_t^N)$, yielding a reward $y_t$.

この時点で、Slate-GLM-OFUはアルゴリズム2で説明されているサブルーチンを呼び出し、$\bm{\theta}_t, \mathbf{W}_t, (\mathbf{W}_t^1, \ldots, \mathbf{W}_t^N), \Theta_t, \mathcal{H}_t$を更新します。
At this point, Slate-GLM-OFU calls a sub-routine described in Algorithm 2 which performs updates to $\bm{\theta}_t, \mathbf{W}_t, (\mathbf{W}_t^1, \ldots, \mathbf{W}_t^N), \Theta_t, \mathcal{H}_t$.

Slate-GLM-TSについていくつかの追加のコメントをします。
We make a few additional remarks about Slate-GLM-TS below.

Slate-GLM-OFU
2
Slate-GLM-TS
アルゴリズム3
Algorithm 3
Slate-GLM-TS
1:
入力:
2:
3:
for
do
4:
5:
6:
while
do
7:
8:
9:
10:
end
while
11:
12:
13:
2
14:
end
for
備考: Slate-GLM-TSのラウンドごとの時間計算量は$N(d \log T)^{O(1)}$であることが簡単にわかります。
Remark: It’s easy to see that the per round time complexity of Slate-GLM-TS is $N(d \log T)^{O(1)}$.

これは、$N$に対して指数的に実行されるTS-ECOLogのそれよりも大幅に低いです。
This is significantly lower than that of TS-ECOLog which runs in time exponential in $N$.

この改善は、Slate-GLM-TSにおけるスロットレベルの選択の結果です。
The improvement comes as a result of the slot-level selection in Slate-GLM-TS.

これにより、アルゴリズムはラウンドごとの時間計算量が低く、実際のシナリオでの利用が可能になります。
This along with the efficient estimation of $\bm{\theta}_t$ in Algorithm 2, ensures that the algorithm has low per-round time complexity making it useful in practical scenarios.

これは、セクション5の合成および実世界の実験によって検証されます。
This is validated by our Synthetic and Real-World experiments in Section 5.

私たちが行ったほぼすべての実験において、Slate-GLM-TSのレグレットは非常に競争力があり、ほとんどのベースラインよりも優れていることも観察しました。
We also observe that in almost all experiments we performed, the regret of Slate-GLM-TS was quite competitive and better than most baselines.

Slate-GLM-TSのレグレットに対する理論的保証は提供していませんが、付録C.1では、Slate-GLM-TSの固定アームバージョンであるSlate-GLM-TS-Fixedを提供します。
Even though we do not provide a theoretical guarantee for the regret of Slate-GLM-TS, in Appendix C.1, we provide a fixed-arms version of Slate-GLM-TS called Slate-GLM-TS-Fixed which operates in the non-contextual setting, like TS-ECOLog i.e., the action (slate) features do not change over time.

これは、TS-ECOLogからの短いウォームアップ手順とSlate-GLM-TSからのスロットレベルの選択技術を使用し、ラウンドごとの時間計算量は$N$に対して線形になります。
It uses the short warm-up procedure from TS-ECOLog and the slot-level selection technique from Slate-GLM-TS resulting in a per round time complexity linear in $N$.

私たちが定理3.1の証明で示した$\bm{W}_t$と$\text{diag}(\mathbf{W}_t^1, \ldots, \mathbf{W}_t^N)$の乗法的同等性を利用し、TS-ECOLogの証明を適応させることで、ラウンド数$T$に対して最適な$O(T)$の依存性を証明します。
By utilizing the multiplicative equivalence of $\bm{W}_t$ and $\text{diag}(\mathbf{W}_t^1, \ldots, \mathbf{W}_t^N)$ that we showed in the proof of Theorem 3.1, and adapting the proof of TS-ECOLog, we prove an optimal $O(T)$ dependence on the number of rounds $T$.

簡潔にするために、Slate-GLM-TS-Fixed（アルゴリズム4）とそのレグレット保証（定理C.1）の詳細については付録C.1で説明します。
For brevity, we discuss details of Slate-GLM-TS-Fixed (Algorithm 4) and its regret guarantee (Theorem C.1) in Appendix C.1.



## 5Experiments 実験

In this section, we perform a wide range of synthetic (Experiments 1,2,3) and real-world experiments (Experiment 4) to demonstrate the empirical performance of our algorithms Slate-GLM-OFU, Slate-GLM-TS and Slate-GLM-TS-Fixed. 
このセクションでは、合成実験（実験1、2、3）と実世界の実験（実験4）を広範囲にわたって実施し、私たちのアルゴリズムSlate-GLM-OFU、Slate-GLM-TS、Slate-GLM-TS-Fixedの実証的な性能を示します。

Details of each experiment are in the respective paragraphs. 
各実験の詳細は、それぞれの段落に記載されています。

The codes for Experiments 1-3 and Experiment 4 can be found here and here respectively. 
実験1-3および実験4のコードは、ここおよびここにそれぞれあります。

### Experiments 1,2,3 実験1,2,3

Experiment 4 実験4

Slate-GLM-OFU

Slate-GLM-TS

Slate-GLM-TS-Fixed

The codes for Experiments 1-3 and Experiment 4 can be found here and here respectively. 
実験1-3および実験4のコードは、ここおよびここにそれぞれあります。

The codes for Experiments 1-3 and Experiment 4 can be found here and here respectively. 
実験1-3および実験4のコードは、ここおよびここにそれぞれあります。

The codes for Experiments 1-3 and Experiment 4 can be found here and here respectively. 
実験1-3および実験4のコードは、ここおよびここにそれぞれあります。

### Figure 1: 図1:

Experiment 1 (R(T) vs. T, Contextual Setting): 
実験1 (R(T) vs. T, 文脈設定):

In this experiment, we compare our algorithms Slate-GLM-OFU and Slate-GLM-TS to their counterparts ada-OFU-ECOLog (Algorithm 2, Faury et al. [2022]) and TS-ECOLog (Section D.2, Faury et al. [2022]). 
この実験では、私たちのアルゴリズムSlate-GLM-OFUとSlate-GLM-TSを、対応するada-OFU-ECOLog（アルゴリズム2、Faury et al. [2022]）およびTS-ECOLog（セクションD.2、Faury et al. [2022]）と比較します。

These are the only logistic bandit algorithms that achieve optimal ($\kappa$-limit-free) regret and are also computationally efficient ($O((\log T)^{2})$ per round time complexity). 
これらは、最適な（$\kappa$-制限なし）後悔を達成し、計算効率も高い唯一のロジスティックバンディットアルゴリズムです（1ラウンドあたりの時間計算量は$O((\log T)^{2})$）。

We perform experiments for the following two settings. 
次の2つの設定で実験を行います。

#### Finite Contexts 有限文脈:

We assume the contexts come from the set $\mathcal{C}=\{1,\ldots,C\}$. 
文脈は集合$\mathcal{C}=\{1,\ldots,C\}$から来ると仮定します。

For each $c \in \mathcal{C}$ and $i \in [N]$, a set of items $\mathcal{X}^{i,c}$ is constructed beforehand by randomly sampling $K$ vectors from the $d$-dimensional ball with radius $1/\sqrt{N}$. 
各$c \in \mathcal{C}$および$i \in [N]$について、アイテムのセット$\mathcal{X}^{i,c}$は、半径$1/\sqrt{N}$の$d$次元ボールから$K$ベクトルをランダムにサンプリングすることによって事前に構築されます。

At each round $t$, a context $c$ is sampled uniformly at random from $\mathcal{C}$ and the sets $\mathcal{X}^{1,c},\ldots,\mathcal{X}^{N,c}$ are presented to the learner. 
各ラウンド$t$で、文脈$c$は$\mathcal{C}$から一様にランダムにサンプリングされ、セット$\mathcal{X}^{1,c},\ldots,\mathcal{X}^{N,c}$が学習者に提示されます。

#### Infinite Contexts 無限文脈:

At each round $t \in [T]$, and for each slot $i \in [N]$, set $\mathcal{X}_{t}^{i}$ is constructed by sampling $K$ vectors randomly from the $d$-dimensional ball with radius $1/\sqrt{N}$. 
各ラウンド$t \in [T]$で、各スロット$i \in [N]$について、セット$\mathcal{X}_{t}^{i}$は、半径$1/\sqrt{N}$の$d$次元ボールから$K$ベクトルをランダムにサンプリングすることによって構築されます。

The learner is then presented with $\mathcal{X}_{t}^{i}$. 
その後、学習者は$\mathcal{X}_{t}^{i}$を提示されます。

For the finite context setting, we fix $C=5$. 
有限文脈設定では、$C=5$に固定します。

For both settings, we fix the number of slots $N=3$, the number of items per slot $K=5$, and the dimension of item features to $d=5$. 
両方の設定で、スロットの数$N=3$、スロットごとのアイテム数$K=5$、アイテム特徴の次元を$d=5$に固定します。

To simulate the reward, we select $\bm{\theta}^{\star}$ by randomly sampling from $[-1,1]^{15}$. 
報酬をシミュレートするために、$[-1,1]^{15}$からランダムにサンプリングして$\bm{\theta}^{\star}$を選択します。

We run our algorithms by varying the time horizon $T$ in $\{1000,5000,10000,15000,20000\}$. 
私たちのアルゴリズムは、時間のホライズン$T$を$\{1000,5000,10000,15000,20000\}$で変化させて実行します。

For each $T$, we average the regret obtained at the end of $T$ rounds over 20 different seeds used to sample the rewards. 
各$T$について、報酬をサンプリングするために使用した20の異なるシードの間で、$T$ラウンドの終了時に得られた後悔を平均します。

The results for the Finite and Infinite context settings are shown in Figures 1(a) and 1(b) respectively. 
有限文脈設定と無限文脈設定の結果は、それぞれ図1(a)と1(b)に示されています。

We can see that in both instances, Slate-GLM-OFU performs the best, while Slate-GLM-TS performs on par with TS-ECOLog. 
両方のケースで、Slate-GLM-OFUが最も優れた性能を発揮し、Slate-GLM-TSはTS-ECOLogと同等の性能を示しています。

Further, in Section F of the appendix, we report the average results along with two standard deviations. 
さらに、付録のセクションFでは、平均結果と2つの標準偏差を報告します。

### Experiment 2 (Per-Round Time vs. N) 実験2（ラウンドごとの時間 vs. N）:

In this experiment, we compare the average and maximum time taken (per round) by our algorithms Slate-GLM-OFU and Slate-GLM-TS, with respect to their counterparts ada-OFU-ECOLog and TS-ECOLog. 
この実験では、私たちのアルゴリズムSlate-GLM-OFUとSlate-GLM-TSが、対応するada-OFU-ECOLogおよびTS-ECOLogに対して、（ラウンドごとの）平均時間と最大時間を比較します。

The per-round time is calculated as the sum of the per-round pull and per-round update times. 
ラウンドごとの時間は、ラウンドごとのプル時間とラウンドごとの更新時間の合計として計算されます。

While doing this comparison, we vary the number of slots $N$ in the set $\{3,\ldots,6\}$. 
この比較を行う際、スロットの数$N$を集合$\{3,\ldots,6\}$で変化させます。

The number of items ($K=|\mathcal{X}^{i}_{t}|$) per slot is fixed to 7 and the dimension $d$ of each item is fixed to 5. 
スロットごとのアイテム数（$K=|\mathcal{X}^{i}_{t}|$）は7に固定され、各アイテムの次元$d$は5に固定されます。

The item features are selected by randomly sampling from $[-1,1]^{5}$ and normalized to have norm $1/\sqrt{N}$. 
アイテムの特徴は、$[-1,1]^{5}$からランダムにサンプリングされ、ノルム$1/\sqrt{N}$に正規化されます。

For each $N \in \{3,4,5,6\}$, we select a different reward parameter vector $\bm{\theta}^{\star}$ by randomly sampling from $[-1,1]^{5N}$. 
各$N \in \{3,4,5,6\}$について、報酬パラメータベクトル$\bm{\theta}^{\star}$を$[-1,1]^{5N}$からランダムにサンプリングして選択します。

Note that the number of possible slates is $K^{N}$ and thus, varying $N$ in $\{3,4,5,6\}$ results in 343,240,16807, and 117649 slates respectively. 
可能なスレートの数は$K^{N}$であり、したがって、$\{3,4,5,6\}$で$N$を変化させると、それぞれ343、240、16807、および117649のスレートが得られます。

We perform this experiment in the infinite context setting (See Experiment 1 for details). 
この実験は無限文脈設定で実施します（詳細は実験1を参照）。

We run all the algorithms for $T=1000$ rounds and average the results over 10 different seeds for sampling rewards. 
すべてのアルゴリズムを$T=1000$ラウンドで実行し、報酬をサンプリングするために使用した10の異なるシードの間で結果を平均します。

We the average per round running time in Figure 1(d) and maximum per round running time in Figure 1(e). 
平均ラウンドごとの実行時間は図1(d)に、最大ラウンドごとの実行時間は図1(e)に示します。

As expected, we observe much lower running times for Slate-GLM-OFU and Slate-GLM-TS compared to their counterparts. 
予想通り、Slate-GLM-OFUおよびSlate-GLM-TSの実行時間は、対応するアルゴリズムと比較してはるかに低いことがわかります。

Moreover, the plots also indicate exponential growth in the per-round running time for both ada-OFU-ECOLog and TS-ECOLog. 
さらに、プロットはada-OFU-ECOLogおよびTS-ECOLogのラウンドごとの実行時間が指数関数的に増加していることを示しています。

Further, there is a significant gap between the maximum and average per-round time of Slate-GLM-OFU and Slate-GLM-TS, implying that the actual per-round time for these algorithms is generally much lower than their maximum values. 
さらに、Slate-GLM-OFUおよびSlate-GLM-TSの最大ラウンドごとの時間と平均ラウンドごとの時間の間には大きなギャップがあり、これらのアルゴリズムの実際のラウンドごとの時間は一般的に最大値よりもはるかに低いことを示唆しています。

In Section F of the appendix, we report the results with two standard deviations, along with each algorithm’s average time for choosing an arm to pull and updating its parameters separately. 
付録のセクションFでは、各アルゴリズムのアームを選択するための平均時間とパラメータを更新するための平均時間とともに、2つの標準偏差を持つ結果を報告します。

### Experiment 3 (R(T) vs. T, Non-Contextual Setting) 実験3（R(T) vs. T, 非文脈設定）:

In this experiment, we compare our algorithms Slate-GLM-OFU, Slate-GLM-TS, and Slate-GLM-TS-Fixed (Algorithm 4, Appendix C) to a number of state-of-the-art baseline algorithms, in the non-contextual setting, i.e., the set of candidate slates remains fixed throughout the course of the algorithm. 
この実験では、私たちのアルゴリズムSlate-GLM-OFU、Slate-GLM-TS、Slate-GLM-TS-Fixed（アルゴリズム4、付録C）を、非文脈設定における最先端のベースラインアルゴリズムと比較します。すなわち、候補スレートのセットはアルゴリズムの進行中に固定されます。

Like previous experiments, our baselines include ada-OFU-ECOLog and TS-ECOLog from Faury et al. [2022]. 
前の実験と同様に、私たちのベースラインにはFaury et al. [2022]のada-OFU-ECOLogおよびTS-ECOLogが含まれます。

However, for the non-contextual setting, we also include other state-of-the-art baselines such as the MPS algorithm (Algorithm 3, Dimakopoulou et al. [2019]) and the Ordered Slate Bandit algorithm (Figure 3, Kale et al. [2010]). 
しかし、非文脈設定では、MPSアルゴリズム（アルゴリズム3、Dimakopoulou et al. [2019]）やOrdered Slate Banditアルゴリズム（図3、Kale et al. [2010]）など、他の最先端のベースラインも含めます。

The latter is designed for semi-bandit feedback, and hence, we adapt it to the bandit feedback setting as explained in Appendix F. 
後者はセミバンディットフィードバック用に設計されているため、付録Fで説明されているように、バンディットフィードバック設定に適応させます。

We fix the number of slots $N$ to 3 and the number of items in each slot $K=|\mathcal{X}^{i}_{t}|$ to 5. 
スロットの数$N$を3に、各スロットのアイテム数$K=|\mathcal{X}^{i}_{t}|$を5に固定します。

The dimension $d$ of items for each slot is fixed to 5. 
各スロットのアイテムの次元$d$は5に固定されます。

The items for each slot are randomly sampled from $[-1,1]^{5}$ and normalized to have norm $1/\sqrt{3}$, while $\bm{\theta}_{\star}$ is randomly sampled from $[-1,1]^{15}$ and normalized. 
各スロットのアイテムは$[-1,1]^{5}$からランダムにサンプリングされ、ノルム$1/\sqrt{3}$に正規化され、$\bm{\theta}_{\star}$は$[-1,1]^{15}$からランダムにサンプリングされて正規化されます。

We run all the algorithms for $T \in \{1000,5000,10000,20000,30000,40000,50000\}$ rounds and average the results over 50 different seeds for sampling rewards. 
すべてのアルゴリズムを$T \in \{1000,5000,10000,20000,30000,40000,50000\}$ラウンドで実行し、報酬をサンプリングするために使用した50の異なるシードの間で結果を平均します。

The rewards are shown in Figure 1(c). 
報酬は図1(c)に示されています。

We see that Slate-GLM-OFU has the best performance, with the only algorithm having comparable performance being MPS. 
Slate-GLM-OFUが最も優れた性能を発揮し、比較可能な性能を持つ唯一のアルゴリズムはMPSであることがわかります。

Also, Slate-GLM-TS performs worse than ada-OFU-ECOLog and MPS while being on par with TS-ECOLog. 
また、Slate-GLM-TSはada-OFU-ECOLogおよびMPSよりも劣っており、TS-ECOLogと同等の性能を示しています。

In Section F, we showcase the average results with two standard deviations, which also demonstrates that MPS showcases a high variance in results, hence, being less reliable in practice. 
セクションFでは、2つの標準偏差を持つ平均結果を示し、MPSが結果に高い分散を示すことも示しています。したがって、実際には信頼性が低くなります。

### Experiment 4 (Prompt Tuning) 実験4（プロンプトチューニング）:

In this experiment, we apply our contextual slate bandit algorithm Slate-GLM-OFU to select in-context examples for tuning prompts of Language Models, applied to binary classification tasks. 
この実験では、文脈スレートバンディットアルゴリズムSlate-GLM-OFUを適用して、バイナリ分類タスクに適用される言語モデルのプロンプトを調整するための文脈内の例を選択します。

Typically, for such applications, a labeled training set of (input query, output label) pairs is used to learn policies of editing different parts of the prompt (instruction, in-context examples, verbalizers) depending on a provided test input query. 
通常、このようなアプリケーションでは、提供されたテスト入力クエリに応じてプロンプトの異なる部分（指示、文脈内の例、言語化者）を編集するポリシーを学習するために、（入力クエリ、出力ラベル）のペアのラベル付きトレーニングセットが使用されます。

To simplify our task, we fix the instruction and the verbalizer and only select $N$ in-context examples from an available pool of $K$ examples. 
タスクを簡素化するために、指示と言語化者を固定し、利用可能な$K$の例のプールからのみ$N$の文脈内の例を選択します。

There are $N$ available positions (slots) in the prompt. 
プロンプトには$N$の利用可能な位置（スロット）があります。

Given a test input query (context), we create context-dependent features for the $K$ pool examples and independently select one (with repetition) per slot. 
テスト入力クエリ（文脈）が与えられると、$K$のプール例に対して文脈依存の特徴を作成し、各スロットごとに1つ（繰り返しあり）を独立して選択します。

This matches the contextual slate bandit problem setting (See Section 2) and therefore Slate-GLM-OFU can be applied. 
これは文脈スレートバンディット問題の設定に一致し（セクション2を参照）、したがってSlate-GLM-OFUを適用できます。

We experiment on a sampled subset of size 5000 from two popular sentiment analysis datasets, SST2 and Yelp Review. 
私たちは、2つの人気のある感情分析データセットSST2とYelp Reviewからサイズ5000のサンプルサブセットで実験を行います。

We randomly order the set and use about 80% of them for “warm-up” training and the remaining 20% for testing. 
セットをランダムに並べ替え、約80%を「ウォームアップ」トレーニングに使用し、残りの20%をテストに使用します。

Like most prompt tuning experiments, we report our results only on the test set, however, our algorithm continues to learn throughout the 5000 rounds. 
ほとんどのプロンプトチューニング実験と同様に、私たちは結果をテストセットのみに報告しますが、私たちのアルゴリズムは5000ラウンドを通じて学習を続けます。

The warm-up rounds help us to start with a good estimate of the hidden reward parameter vector. 
ウォームアップラウンドは、隠れた報酬パラメータベクトルの良い推定値で開始するのに役立ちます。

We fix $N=4$ and vary $K$ in the set $\{8,16,32\}$. 
$N=4$に固定し、$K$を集合$\{8,16,32\}$で変化させます。

All the slots choose an example from the same $K$-sized example pool. 
すべてのスロットは、同じ$K$サイズの例プールから例を選択します。

At each round, given an input query $\bm{q}$ that needs to be solved for, item features for each in-context example $\bm{e}=(\bm{x},y)$ is constructed by embedding each of $\bm{q}$, $\bm{x}$, and $y$ into 64 dimensions and concatenating them, thereby resulting in a 192-dimensional item feature vector. 
各ラウンドで、解決する必要がある入力クエリ$\bm{q}$が与えられると、各文脈内の例$\bm{e}=(\bm{x},y)$のアイテム特徴は、$\bm{q}$、$\bm{x}$、および$y$のそれぞれを64次元に埋め込み、それらを連結することによって構築され、192次元のアイテム特徴ベクトルが得られます。

After selecting the 4 items (slate), the resulting prompt (also containing the input query $\bm{q}$) is passed through the RoBERTa model and a possible answer for $\bm{q}$ is generated. 
4つのアイテム（スレート）を選択した後、得られたプロンプト（入力クエリ$\bm{q}$も含む）はRoBERTaモデルを通過し、$\bm{q}$に対する可能な回答が生成されます。

Hence, we are learning to choose best the in-context examples for RoBERTa. 
したがって、私たちはRoBERTaのために文脈内の例を最適に選択することを学んでいます。

At each round, we use GPT-3.5-Turbo to provide feedback (binary, 0 or 1) for the generated answer. 
各ラウンドで、生成された回答に対してフィードバック（バイナリ、0または1）を提供するためにGPT-3.5-Turboを使用します。

This is treated as the reward for the chosen slate and utilized by the rest of the Slate-GLM-OFU algorithm. 
これは選択されたスレートの報酬として扱われ、Slate-GLM-OFUアルゴリズムの残りの部分で利用されます。

Figure 1(f) shows the increase in cumulative accuracy as we sequentially proceed through the 5000 data points in the Yelp Review dataset. 
図1(f)は、Yelp Reviewデータセットの5000データポイントを順次進むにつれて累積精度が増加する様子を示しています。

The data points to the left of the dotted blue line are the warm-up points and those to the right are the test points. 
点線の青い線の左側のデータポイントはウォームアップポイントであり、右側のデータポイントはテストポイントです。

We can see that the cumulative accuracy increases consistently as we sequentially proceed through the points. 
ポイントを順次進むにつれて、累積精度が一貫して増加することがわかります。

Also, on the test set, the accuracy stays well above 80%. 
また、テストセットでは、精度は80%を大きく上回っています。

We vary $K$ in the set $\{8,16,32\}$ and report test accuracy for both datasets in Table 1. 
$K$を集合$\{8,16,32\}$で変化させ、両方のデータセットのテスト精度を表1に報告します。

It can be seen that the cumulative test accuracies for Slate-GLM-OFU are much higher compared to the Random Allocation baseline where each in-context example is chosen randomly and no learning is performed. 
Slate-GLM-OFUの累積テスト精度は、各文脈内の例がランダムに選択され、学習が行われないランダム割り当てベースラインと比較してはるかに高いことがわかります。

Also, we see that the accuracy generally increases when the pool size increases since better examples can be available. 
また、プールサイズが増加すると、より良い例が利用可能になるため、精度が一般的に向上することがわかります。

We do see a small dip for the Yelp Review dataset when $K$ increases from 16 to 32 and hypothesize that this may be happening due to more exploration. 
$K$が16から32に増加すると、Yelp Reviewデータセットで小さな低下が見られ、この現象はより多くの探索によるものかもしれないと仮定します。

### Table 1: 表1:



## 6Conclusions 結論

We proposed three algorithms Slate-GLM-OFU, Slate-GLM-TS, Slate-GLM-TS-Fixed for the slate bandit problem with logistic rewards. 
私たちは、ロジスティック報酬を持つスレートバンディット問題のために、3つのアルゴリズムSlate-GLM-OFU、Slate-GLM-TS、Slate-GLM-TS-Fixedを提案しました。 
While the first two work in both the contextual and non-contextual settings, the third is designed for the non-contextual setting. 
最初の2つは文脈ありおよび文脈なしの設定の両方で機能しますが、3つ目は文脈なしの設定のために設計されています。 
All our algorithms perform explore-exploit at the slot level, making their average per round time complexity logarithmic in the number of candidate slates. 
私たちのすべてのアルゴリズムはスロットレベルで探索と活用を行い、候補スレートの数に対して平均的なラウンドごとの時間計算量が対数的になります。 
By building on algorithms from Faury et al. [2022], the average time per round is also logarithmic in the number of rounds $T$. 
Faury et al. [2022]のアルゴリズムを基にすることで、ラウンドごとの平均時間もラウンド数$T$に対して対数的になります。 
As a result, our algorithms run much faster than state of the art logistic bandit algorithms (having $2^{\Omega(N)}$ per round time complexity). 
その結果、私たちのアルゴリズムは、最先端のロジスティックバンディットアルゴリズム（ラウンドごとの時間計算量が$2^{\Omega(N)}$であるもの）よりもはるかに速く動作します。 
We also show that under a popular diversity assumption (Assumption 2.1), which we also empirically validate, Slate-GLM-OFU and Slate-GLM-TS-Fixed achieve $\kappa$ independent $\tilde{O}(\sqrt{T})$ regret, making them both optimal and computationally efficient. 
また、私たちは、人気のある多様性の仮定（仮定2.1）の下で、Slate-GLM-OFUとSlate-GLM-TS-Fixedが$\kappa$独立の$\tilde{O}(\sqrt{T})$の後悔を達成し、両者が最適かつ計算効率が高いことを示します。



## References 参考文献

- Abbasi-yadkori etal. [2011]↑Yasin Abbasi-yadkori, Dávid Pál, and Csaba Szepesvári. Improved algorithms for linear stochastic bandits. 
- Abbasi-yadkori etal. [2011]↑Yasin Abbasi-yadkori、Dávid Pál、Csaba Szepesváriによる「線形確率バンディットのための改善されたアルゴリズム」。 
In J.Shawe-Taylor, R.Zemel, P.Bartlett, F.Pereira, and K.Q. Weinberger, editors, Advances in Neural Information Processing Systems, volume 24. Curran Associates, Inc., 2011. 
J.Shawe-Taylor、R.Zemel、P.Bartlett、F.Pereira、K.Q. Weinberger編『神経情報処理システムの進展』第24巻。Curran Associates, Inc.、2011年。 
URL https://proceedings.neurips.cc/paper_files/paper/2011/file/e1d5be1c7f2f456670de3d53c7b54f4a-Paper.pdf. 
URL https://proceedings.neurips.cc/paper_files/paper/2011/file/e1d5be1c7f2f456670de3d53c7b54f4a-Paper.pdf.

- Abeille and Lazaric [2017]↑Marc Abeille and Alessandro Lazaric. Linear Thompson Sampling Revisited. 
- Abeille and Lazaric [2017]↑Marc Abeille、Alessandro Lazaricによる「線形トンプソンサンプリングの再考」。 
In Aarti Singh and Jerry Zhu, editors, Proceedings of the 20th International Conference on Artificial Intelligence and Statistics, volume 54 of Proceedings of Machine Learning Research, pages 176–184. PMLR, 20–22 Apr 2017. 
Aarti Singh、Jerry Zhu編『第20回国際人工知能と統計学会議の議事録』、機械学習研究の議事録第54巻、176–184ページ。PMLR、2017年4月20–22日。 
URL https://proceedings.mlr.press/v54/abeille17a.html. 
URL https://proceedings.mlr.press/v54/abeille17a.html.

- Abeille etal. [2021]↑Marc Abeille, Louis Faury, and Clément Calauzènes. Instance-wise minimax-optimal algorithms for logistic bandits, 2021. 
- Abeille etal. [2021]↑Marc Abeille、Louis Faury、Clément Calauzènesによる「ロジスティックバンディットのためのインスタンスごとのミニマックス最適アルゴリズム」、2021年。 
URL https://arxiv.org/abs/2010.12642. 
URL https://arxiv.org/abs/2010.12642.

- Chatterji etal. [2020]↑Niladri S. Chatterji, Vidya Muthukumar, and Peter L. Bartlett. Osom: A simultaneously optimal algorithm for multi-armed and linear contextual bandits, 2020. 
- Chatterji etal. [2020]↑Niladri S. Chatterji、Vidya Muthukumar、Peter L. Bartlettによる「Osom: マルチアームおよび線形コンテキストバンディットのための同時最適アルゴリズム」、2020年。 
URL https://arxiv.org/abs/1905.10040. 
URL https://arxiv.org/abs/1905.10040.

- Chen etal. [2021]↑Jin Chen, Ju Xu, Gangwei Jiang, Tiezheng Ge, Zhiqiang Zhang, Defu Lian, and Kai Zheng. Automated creative optimization for e-commerce advertising. 
- Chen etal. [2021]↑Jin Chen、Ju Xu、Gangwei Jiang、Tiezheng Ge、Zhiqiang Zhang、Defu Lian、Kai Zhengによる「eコマース広告のための自動クリエイティブ最適化」。 
Proceedings of the Web Conference 2021, 2021. 
2021年ウェブ会議の議事録、2021年。 
URL https://api.semanticscholar.org/CorpusID:232076065. 
URL https://api.semanticscholar.org/CorpusID:232076065.

- Das and Sinha [2024]↑Nirjhar Das and Gaurav Sinha. Linear Contextual Bandits with Hybrid Payoff: Revisited, page 441–455. 
- Das and Sinha [2024]↑Nirjhar Das、Gaurav Sinhaによる「ハイブリッドペイオフを持つ線形コンテキストバンディット：再考」、441–455ページ。 
Springer Nature Switzerland, 2024. 
スプリンガー・ネイチャー・スイス、2024年。 
ISBN 9783031703652. 
ISBN 9783031703652. 
doi:10.1007/978-3-031-70365-2˙26. 
doi:10.1007/978-3-031-70365-2˙26. 
URL http://dx.doi.org/10.1007/978-3-031-70365-2_26. 
URL http://dx.doi.org/10.1007/978-3-031-70365-2_26.

- Dimakopoulou etal. [2019]↑Maria Dimakopoulou, Nikos Vlassis, and Tony Jebara. Marginal posterior sampling for slate bandits. 
- Dimakopoulou etal. [2019]↑Maria Dimakopoulou、Nikos Vlassis、Tony Jebaraによる「スレートバンディットのための周辺事後サンプリング」。 
In Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, IJCAI-19, pages 2223–2229. 
第28回国際共同人工知能会議の議事録、IJCAI-19、2223–2229ページ。 
International Joint Conferences on Artificial Intelligence Organization, 7 2019. 
国際共同人工知能会議機構、2019年7月。 
doi:10.24963/ijcai.2019/308. 
doi:10.24963/ijcai.2019/308. 
URL https://doi.org/10.24963/ijcai.2019/308. 
URL https://doi.org/10.24963/ijcai.2019/308.

- Faury etal. [2020]↑Louis Faury, Marc Abeille, Clément Calauzènes, and Olivier Fercoq. Improved optimistic algorithms for logistic bandits, 2020. 
- Faury etal. [2020]↑Louis Faury、Marc Abeille、Clément Calauzènes、Olivier Fercoqによる「ロジスティックバンディットのための改善された楽観的アルゴリズム」、2020年。 
URL https://arxiv.org/abs/2002.07530. 
URL https://arxiv.org/abs/2002.07530.

- Faury etal. [2022]↑Louis Faury, Marc Abeille, Kwang-Sung Jun, and Clément Calauzènes. Jointly efficient and optimal algorithms for logistic bandits, 2022. 
- Faury etal. [2022]↑Louis Faury、Marc Abeille、Kwang-Sung Jun、Clément Calauzènesによる「ロジスティックバンディットのための共同効率的かつ最適なアルゴリズム」、2022年。 
URL https://arxiv.org/abs/2201.01985. 
URL https://arxiv.org/abs/2201.01985.

- Filippi etal. [2010]↑Sarah Filippi, Olivier Cappe, Aurélien Garivier, and Csaba Szepesvári. Parametric bandits: The generalized linear case. 
- Filippi etal. [2010]↑Sarah Filippi、Olivier Cappe、Aurélien Garivier、Csaba Szepesváriによる「パラメトリックバンディット：一般化線形ケース」。 
In J.Lafferty, C.Williams, J.Shawe-Taylor, R.Zemel, and A.Culotta, editors, Advances in Neural Information Processing Systems, volume 23. Curran Associates, Inc., 2010. 
J.Lafferty、C.Williams、J.Shawe-Taylor、R.Zemel、A.Culotta編『神経情報処理システムの進展』第23巻。Curran Associates, Inc.、2010年。 
URL https://proceedings.neurips.cc/paper_files/paper/2010/file/c2626d850c80ea07e7511bbae4c76f4b-Paper.pdf. 
URL https://proceedings.neurips.cc/paper_files/paper/2010/file/c2626d850c80ea07e7511bbae4c76f4b-Paper.pdf.

- Hill etal. [2017]↑Daniel N. Hill, Houssam Nassif, Yi Liu, Anand Iyer, and S.V.N. Vishwanathan. An efficient bandit algorithm for realtime multivariate optimization. 
- Hill etal. [2017]↑Daniel N. Hill、Houssam Nassif、Yi Liu、Anand Iyer、S.V.N. Vishwanathanによる「リアルタイム多変量最適化のための効率的なバンディットアルゴリズム」。 
In Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD ’17. 
第23回ACM SIGKDD国際会議の議事録、KDD ’17。 
ACM, August 2017. 
ACM、2017年8月。 
doi:10.1145/3097983.3098184. 
doi:10.1145/3097983.3098184. 
URL http://dx.doi.org/10.1145/3097983.3098184. 
URL http://dx.doi.org/10.1145/3097983.3098184.

- Kale etal. [2010]↑Satyen Kale, Lev Reyzin, and Robert E Schapire. Non-stochastic bandit slate problems. 
- Kale etal. [2010]↑Satyen Kale、Lev Reyzin、Robert E Schapireによる「非確率的バンディットスレート問題」。 
In J.Lafferty, C.Williams, J.Shawe-Taylor, R.Zemel, and A.Culotta, editors, Advances in Neural Information Processing Systems, volume 23. Curran Associates, Inc., 2010. 
J.Lafferty、C.Williams、J.Shawe-Taylor、R.Zemel、A.Culotta編『神経情報処理システムの進展』第23巻。Curran Associates, Inc.、2010年。 
URL https://proceedings.neurips.cc/paper_files/paper/2010/file/390e982518a50e280d8e2b535462ec1f-Paper.pdf. 
URL https://proceedings.neurips.cc/paper_files/paper/2010/file/390e982518a50e280d8e2b535462ec1f-Paper.pdf.

- Kiyohara etal. [2024]↑Haruka Kiyohara, Masahiro Nomura, and Yuta Saito. Off-policy evaluation of slate bandit policies via optimizing abstraction. 
- Kiyohara etal. [2024]↑Haruka Kiyohara、Masahiro Nomura、Yuta Saitoによる「抽象化の最適化によるスレートバンディットポリシーのオフポリシー評価」。 
In Proceedings of the ACM Web Conference 2024, WWW ’24, page 3150–3161, New York, NY, USA, 2024. 
2024年ACMウェブ会議の議事録、WWW ’24、3150–3161ページ、アメリカ・ニューヨーク、2024年。 
Association for Computing Machinery. 
計算機科学協会。 
ISBN 9798400701719. 
ISBN 9798400701719. 
doi:10.1145/3589334.3645343. 
doi:10.1145/3589334.3645343. 
URL https://doi.org/10.1145/3589334.3645343. 
URL https://doi.org/10.1145/3589334.3645343.

- Lattimore and Szepesvári [2020]↑Tor Lattimore and Csaba Szepesvári. Bandit Algorithms. 
- Lattimore and Szepesvári [2020]↑Tor Lattimore、Csaba Szepesváriによる「バンディットアルゴリズム」。 
Cambridge University Press, 2020. 
ケンブリッジ大学出版局、2020年。

- Nussbaum etal. [2024]↑Zach Nussbaum, John X. Morris, Brandon Duderstadt, and Andriy Mulyar. Nomic embed: Training a reproducible long context text embedder, 2024. 
- Nussbaum etal. [2024]↑Zach Nussbaum、John X. Morris、Brandon Duderstadt、Andriy Mulyarによる「Nomic embed: 再現可能な長文コンテキストテキストエンベッダーのトレーニング」、2024年。

- Papini etal. [2021]↑Matteo Papini, Andrea Tirinzoni, Marcello Restelli, Alessandro Lazaric, and Matteo Pirotta. Leveraging good representations in linear contextual bandits, 2021. 
- Papini etal. [2021]↑Matteo Papini、Andrea Tirinzoni、Marcello Restelli、Alessandro Lazaric、Matteo Pirottaによる「線形コンテキストバンディットにおける良好な表現の活用」、2021年。 
URL https://arxiv.org/abs/2104.03781. 
URL https://arxiv.org/abs/2104.03781.

- Rhuggenaath etal. [2020]↑Jason Rhuggenaath, Alp Akcay, Yingqian Zhang, and Uzay Kaymak. Algorithms for slate bandits with non-separable reward functions, 04 2020. 
- Rhuggenaath etal. [2020]↑Jason Rhuggenaath、Alp Akcay、Yingqian Zhang、Uzay Kaymakによる「非分離報酬関数を持つスレートバンディットのためのアルゴリズム」、2020年4月。

- Russo etal. [2018]↑Daniel J. Russo, Benjamin VanRoy, Abbas Kazerouni, Ian Osband, and Zheng Wen. A tutorial on thompson sampling. 
- Russo etal. [2018]↑Daniel J. Russo、Benjamin VanRoy、Abbas Kazerouni、Ian Osband、Zheng Wenによる「トンプソンサンプリングのチュートリアル」。 
Found. Trends Mach. Learn., 11(1):1–96, July 2018. 
Found. Trends Mach. Learn.、11(1):1–96、2018年7月。 
ISSN 1935-8237. 
ISSN 1935-8237. 
doi:10.1561/2200000070. 
doi:10.1561/2200000070. 
URL https://doi.org/10.1561/2200000070. 
URL https://doi.org/10.1561/2200000070.

- Sawarni etal. [2024]↑Ayush Sawarni, Nirjhar Das, Siddharth Barman, and Gaurav Sinha. Generalized linear bandits with limited adaptivity, 2024. 
- Sawarni etal. [2024]↑Ayush Sawarni、Nirjhar Das、Siddharth Barman、Gaurav Sinhaによる「限られた適応性を持つ一般化線形バンディット」、2024年。 
URL https://arxiv.org/abs/2404.06831. 
URL https://arxiv.org/abs/2404.06831.

- Swaminathan etal. [2017]↑Adith Swaminathan, Akshay Krishnamurthy, Alekh Agarwal, Miro Dudik, John Langford, Damien Jose, and Imed Zitouni. Off-policy evaluation for slate recommendation. 
- Swaminathan etal. [2017]↑Adith Swaminathan、Akshay Krishnamurthy、Alekh Agarwal、Miro Dudik、John Langford、Damien Jose、Imed Zitouniによる「スレート推薦のためのオフポリシー評価」。 
In I.Guyon, U.Von Luxburg, S.Bengio, H.Wallach, R.Fergus, S.Vishwanathan, and R.Garnett, editors, Advances in Neural Information Processing Systems, volume 30. Curran Associates, Inc., 2017. 
I.Guyon、U.Von Luxburg、S.Bengio、H.Wallach、R.Fergus、S.Vishwanathan、R.Garnett編『神経情報処理システムの進展』第30巻。Curran Associates, Inc.、2017年。 
URL https://proceedings.neurips.cc/paper_files/paper/2017/file/5352696a9ca3397beb79f116f3a33991-Paper.pdf. 
URL https://proceedings.neurips.cc/paper_files/paper/2017/file/5352696a9ca3397beb79f116f3a33991-Paper.pdf.

- Thompson [1933]↑William R. Thompson. On the likelihood that one unknown probability exceeds another in view of the evidence of two samples. 
- Thompson [1933]↑William R. Thompsonによる「二つのサンプルの証拠に基づいて、一つの未知の確率が他を超える可能性について」。 
Biometrika, 25(3/4):285–294, 1933. 
Biometrika、25(3/4):285–294、1933年。 
ISSN 00063444. 
ISSN 00063444. 
URL http://www.jstor.org/stable/2332286. 
URL http://www.jstor.org/stable/2332286.

- Tropp [2011a]↑Joel Tropp. Freedman’s inequality for matrix martingales. 
- Tropp [2011a]↑Joel Troppによる「行列マーチンゲールのためのフリードマンの不等式」。 
Electronic Communications in Probability, 16, 01 2011a. 
確率に関する電子通信、16、2011年1月。 
doi:10.1214/ECP.v16-1624. 
doi:10.1214/ECP.v16-1624.

- Tropp [2011b]↑Joel A. Tropp. User-friendly tail bounds for sums of random matrices. 
- Tropp [2011b]↑Joel A. Troppによる「ランダム行列の和のためのユーザーフレンドリーな尾の境界」。 
Foundations of Computational Mathematics, 12(4):389–434, August 2011b. 
計算数学の基礎、12(4):389–434、2011年8月。 
ISSN 1615-3383. 
ISSN 1615-3383. 
doi:10.1007/s10208-011-9099-z. 
doi:10.1007/s10208-011-9099-z. 
URL http://dx.doi.org/10.1007/s10208-011-9099-z. 
URL http://dx.doi.org/10.1007/s10208-011-9099-z.

- Vlassis etal. [2024]↑Nikos Vlassis, Ashok Chandrashekar, Fernando Amat Gil, and Nathan Kallus. Control variates for slate off-policy evaluation. 
- Vlassis etal. [2024]↑Nikos Vlassis、Ashok Chandrashekar、Fernando Amat Gil、Nathan Kallusによる「スレートオフポリシー評価のための制御変数」。 
In Proceedings of the 35th International Conference on Neural Information Processing Systems, NIPS ’21, Red Hook, NY, USA, 2024. 
第35回神経情報処理システム国際会議の議事録、NIPS ’21、アメリカ・ニューヨーク、2024年。 
Curran Associates Inc. 
Curran Associates Inc. 
ISBN 9781713845393. 
ISBN 9781713845393.

- Zhang etal. [2022]↑Tianjun Zhang, Xuezhi Wang, Denny Zhou, Dale Schuurmans, and Joseph E. Gonzalez. Tempera: Test-time prompting via reinforcement learning, 2022. 
- Zhang etal. [2022]↑Tianjun Zhang、Xuezhi Wang、Denny Zhou、Dale Schuurmans、Joseph E. Gonzalezによる「Tempera: 強化学習によるテスト時プロンプティング」、2022年。 
URL https://arxiv.org/abs/2211.11890. 
URL https://arxiv.org/abs/2211.11890.

- Zhuang etal. [2021]↑Liu Zhuang, Lin Wayne, Shi Ya, and Zhao Jun. A robustly optimized BERT pre-training approach with post-training. 
- Zhuang etal. [2021]↑Liu Zhuang、Lin Wayne、Shi Ya、Zhao Junによる「ポストトレーニングを伴う堅牢に最適化されたBERT事前トレーニングアプローチ」。 
In Sheng Li, Maosong Sun, Yang Liu, Hua Wu, Kang Liu, Wanxiang Che, Shizhu He, and Gaoqi Rao, editors, Proceedings of the 20th Chinese National Conference on Computational Linguistics, pages 1218–1227, Huhhot, China, August 2021. 
Sheng Li、Maosong Sun、Yang Liu、Hua Wu、Kang Liu、Wanxiang Che、Shizhu He、Gaoqi Rao編『第20回中国全国計算言語学会議の議事録』、1218–1227ページ、中国・フフホト、2021年8月。 
Chinese Information Processing Society of China. 
中国情報処理学会。 
URL https://aclanthology.org/2021.ccl-1.108/. 
URL https://aclanthology.org/2021.ccl-1.108/.



## Appendix A General Notations and Results
## 付録 A 一般的な表記法と結果

This section presents some general notations and results for the logistic function that would be used throughout the Appendix. 
このセクションでは、付録全体で使用されるロジスティック関数に関する一般的な表記法と結果を示します。

For a matrix $\bm{A}$, let $\lambda_{max}(\bm{A})$ and $\lambda_{min}(\bm{A})$ denote the maximum and minimum eigenvalue of $\bm{A}$ respectively. 
行列 $\bm{A}$ に対して、$\lambda_{max}(\bm{A})$ と $\lambda_{min}(\bm{A})$ はそれぞれ $\bm{A}$ の最大固有値と最小固有値を示します。

Similarly, we define $\sigma_{max}(\bm{A})$ and $\sigma_{min}(\bm{A})$ to be the maximum and minimum singular values respectively. 
同様に、$\sigma_{max}(\bm{A})$ と $\sigma_{min}(\bm{A})$ をそれぞれ最大特異値と最小特異値と定義します。

We also define the following functions, borrowed from Faury et al. [2022]: 
また、Faury et al. [2022] から借用した以下の関数も定義します：

1. $\gamma_{t}(\delta) = O(S^{2}Nd\log(t/\delta))$ 
1. $\gamma_{t}(\delta) = O(S^{2}Nd\log(t/\delta))$ 

2. $\beta_{t}(\delta) = O(S^{6}Nd\log(t/\delta))$ 
2. $\beta_{t}(\delta) = O(S^{6}Nd\log(t/\delta))$ 

3. $\eta_{t}(\delta) = O(S^{2}Nd\log(t/\delta))$ 
3. $\eta_{t}(\delta) = O(S^{2}Nd\log(t/\delta))$ 

Claim A.1 
主張 A.1

Let $\mu: \mathbb{R} \rightarrow \mathbb{R}$ be the logistic function, i.e., $\mu(x) = \frac{1}{1+\exp(-x)}$ and $\dot{\mu}, \ddot{\mu}$ be the first and second derivative of $\mu$. 
$\mu: \mathbb{R} \rightarrow \mathbb{R}$ をロジスティック関数とし、すなわち $\mu(x) = \frac{1}{1+\exp(-x)}$ とし、$\dot{\mu}, \ddot{\mu}$ を $\mu$ の1階および2階導関数とします。

The following are true. 
以下のことが成り立ちます。

1. $|\ddot{\mu}(x)| \leq \dot{\mu}(x), \forall x \in \mathbb{R}$ 
1. $|\ddot{\mu}(x)| \leq \dot{\mu}(x), \forall x \in \mathbb{R}$ 

2. $\dot{\mu}(x) \leq \dot{\mu}(y)\exp(|x-y|), \forall x,y \in \mathbb{R}$ 
2. $\dot{\mu}(x) \leq \dot{\mu}(y)\exp(|x-y|), \forall x,y \in \mathbb{R}$ 

Definition A.1 
定義 A.1

Let $\dot{\mu}$ be the derivative of the logistic function. 
$\dot{\mu}$ をロジスティック関数の導関数とします。

Define functions $\alpha: \mathbb{R} \times \mathbb{R} \rightarrow \mathbb{R}$ and $\tilde{\alpha}: \mathbb{R} \times \mathbb{R} \rightarrow \mathbb{R}$ as follows. 
関数 $\alpha: \mathbb{R} \times \mathbb{R} \rightarrow \mathbb{R}$ と $\tilde{\alpha}: \mathbb{R} \times \mathbb{R} \rightarrow \mathbb{R}$ を以下のように定義します。

1. $\alpha(x,y) = \int_{0}^{1} \dot{\mu}(x + v(y-x)) \mathop{}\!\mathrm{d}v$ 
1. $\alpha(x,y) = \int_{0}^{1} \dot{\mu}(x + v(y-x)) \mathop{}\!\mathrm{d}v$ 

2. $\tilde{\alpha}(x,y) = \int_{0}^{1} (1-v) \dot{\mu}(x + v(y-x)) \mathop{}\!\mathrm{d}v$ 
2. $\tilde{\alpha}(x,y) = \int_{0}^{1} (1-v) \dot{\mu}(x + v(y-x)) \mathop{}\!\mathrm{d}v$ 

Definition A.2 
定義 A.2

(Exact Taylor Expansion for the Logistic Function) The logistic function $\mu(x)$ can be expanded using an Exact Taylor Expansion as follows: 
（ロジスティック関数の正確なテイラー展開）ロジスティック関数 $\mu(x)$ は以下のように正確なテイラー展開を用いて展開できます：

Definition A.3 
定義 A.3

(Mean Value Theorem for the Logistic Function) The logistic function $\mu$ can be expanded using the Mean Value theorem as follows: 
（ロジスティック関数の平均値定理）ロジスティック関数 $\mu$ は以下のように平均値定理を用いて展開できます：

Recall the following notations from Section 3: 
セクション3から以下の表記を思い出してください：

1. $\bm{W}_{t} = \bm{I} + \sum_{s=1}^{t-1} \dot{\mu}(\bm{x}_{s}^{\top} \bm{\theta}_{s+1}) \bm{x}_{s} \bm{x}_{s}^{\top}$ 
1. $\bm{W}_{t} = \bm{I} + \sum_{s=1}^{t-1} \dot{\mu}(\bm{x}_{s}^{\top} \bm{\theta}_{s+1}) \bm{x}_{s} \bm{x}_{s}^{\top}$ 

2. $\bm{W}_{t}^{i} = \bm{I} + \sum_{s=1}^{t-1} \dot{\mu}(\bm{x}_{s}^{\top} \bm{\theta}_{s+1}) \bm{x}_{s}^{i} \bm{x}_{s}^{i^{\top}}$ 
2. $\bm{W}_{t}^{i} = \bm{I} + \sum_{s=1}^{t-1} \dot{\mu}(\bm{x}_{s}^{\top} \bm{\theta}_{s+1}) \bm{x}_{s}^{i} \bm{x}_{s}^{i^{\top}}$ 

3. $\bm{V}_{t}^{\mathcal{H}} = \gamma_{t}(\delta) \bm{I} + \sum_{\bm{x} \in \mathcal{H}_{t}} \bm{x} \bm{x}^{\top}/\kappa$ 
3. $\bm{V}_{t}^{\mathcal{H}} = \gamma_{t}(\delta) \bm{I} + \sum_{\bm{x} \in \mathcal{H}_{t}} \bm{x} \bm{x}^{\top}/\kappa$ 

We define the following additional matrices. 
以下の追加行列を定義します。

1. $\bm{U}_{t} = \textrm{diag}(\bm{W}_{t}^{1}, \ldots, \bm{W}_{t}^{N})$ 
1. $\bm{U}_{t} = \textrm{diag}(\bm{W}_{t}^{1}, \ldots, \bm{W}_{t}^{N})$ 

2. $\bm{W}_{t}^{i,j} = \sum_{s=1}^{t-1} \dot{\mu}(\bm{x}_{s}^{\top} \bm{\theta}_{s+1}) \bm{x}_{s}^{i} \bm{x}_{s}^{j^{\top}}$ 
2. $\bm{W}_{t}^{i,j} = \sum_{s=1}^{t-1} \dot{\mu}(\bm{x}_{s}^{\top} \bm{\theta}_{s+1}) \bm{x}_{s}^{i} \bm{x}_{s}^{j^{\top}}$ 

3. $\bm{V}_{t}^{\mathcal{H},i} = \gamma_{t}(\delta) \bm{I} + \sum_{\bm{x} \in \mathcal{H}_{t}} \bm{x}^{i} \bm{x}^{i^{\top}}/\kappa$ 
3. $\bm{V}_{t}^{\mathcal{H},i} = \gamma_{t}(\delta) \bm{I} + \sum_{\bm{x} \in \mathcal{H}_{t}} \bm{x}^{i} \bm{x}^{i^{\top}}/\kappa$ 

4. $\bm{V}_{t}^{\mathcal{H},i,j} = \gamma_{t}(\delta) \bm{I} + \sum_{\bm{x} \in \mathcal{H}_{t}} \bm{x}^{i} \bm{x}^{j^{\top}}/\kappa$ 
4. $\bm{V}_{t}^{\mathcal{H},i,j} = \gamma_{t}(\delta) \bm{I} + \sum_{\bm{x} \in \mathcal{H}_{t}} \bm{x}^{i} \bm{x}^{j^{\top}}/\kappa$ 

5. $\bm{U}^{\mathcal{H}}_{t} = \textrm{diag}(\bm{V}_{t}^{\mathcal{H},1}, \ldots, \bm{V}_{t}^{\mathcal{H},N})$ 
5. $\bm{U}^{\mathcal{H}}_{t} = \textrm{diag}(\bm{V}_{t}^{\mathcal{H},1}, \ldots, \bm{V}_{t}^{\mathcal{H},N})$ 



## Appendix BSLATE-GLM-OFU

Appendix B
SLATE-GLM-OFU
Let $\bm{x}^{i} \in \mathbb{R}^{d}$, we define the “lift“ $\tilde{\bm{x}}^{i} \in \mathbb{R}^{dN}$ of $\bm{x}^{i}$ as follows,
$\bm{x}^{i} \in \mathbb{R}^{d}$とすると、$\bm{x}^{i}$の「リフト」を$\tilde{\bm{x}}^{i} \in \mathbb{R}^{dN}$として以下のように定義します。

In other words, consider $\tilde{\bm{x}}^{i}$ to be a vector with $N$ slots of dimension $d$, such that the $i^{th}$ slot is $\bm{x}^{i}$ while the rest of the slots are assigned the zero vector. 
言い換えれば、$\tilde{\bm{x}}^{i}$は次元$d$の$N$スロットを持つベクトルであり、$i^{th}$スロットが$\bm{x}^{i}$で、残りのスロットはゼロベクトルに割り当てられます。

Then, for any vector $\bm{z}=(\bm{z}^{1},\ldots,\bm{z}^{N}) \in \mathbb{R}^{dN}$, with $\bm{z}^{i} \in \mathbb{R}^{d}, \forall i \in [N]$, we get that $\bm{z}=\tilde{\bm{z}}^{1}+\ldots+\tilde{\bm{z}}^{N}$.
次に、任意のベクトル$\bm{z}=(\bm{z}^{1},\ldots,\bm{z}^{N}) \in \mathbb{R}^{dN}$について、$\bm{z}^{i} \in \mathbb{R}^{d}, \forall i \in [N]$とすると、$\bm{z}=\tilde{\bm{z}}^{1}+\ldots+\tilde{\bm{z}}^{N}$が成り立ちます。

Let $T_{0} \in \mathbb{N}$ be a constant (depending on $N$ and $\rho$) such that $\forall t \geq T_{0}, t \geq \frac{3+2\rho N}{3\rho^{2}}(N-1)^{2}\log\left(\frac{2dNT}{\delta}\right)$.
$T_{0} \in \mathbb{N}$を定数とし（$N$と$\rho$に依存）、$\forall t \geq T_{0}, t \geq \frac{3+2\rho N}{3\rho^{2}}(N-1)^{2}\log\left(\frac{2dNT}{\delta}\right)$が成り立つとします。

We assume that the total rounds $T$ satisfies $T \geq T_{0}$.
全体のラウンド数$T$が$T \geq T_{0}$を満たすと仮定します。

We now prove that the regret for Slate-GLM-OFU can be bounded above by the quantity mentioned in Theorem 3.1 (restated and expanded below).
ここで、Slate-GLM-OFUの後悔が定理3.1（以下に再掲し拡張）で述べられた量によって上に制約できることを証明します。

Define the following events:
次のイベントを定義します：

Slate-GLM-OFU
3.1
Theorem B.1
Theorem B.1
Slate-GLM-OFU
.
At the end of $T (\geq T_{0})$ rounds and assuming event $\mathcal{E}$ holds, the regret of Slate-GLM-OFU is bounded by
$T (\geq T_{0})$ラウンドの終了時に、イベント$\mathcal{E}$が成立していると仮定すると、Slate-GLM-OFUの後悔は次のように制約されます。

Recall from Section 3 that $\mathcal{T}$ is the set of all rounds in $[T]$, where the inequality condition in Step 2 of Algorithm 2 does not hold. 
セクション3から思い出してください。$\mathcal{T}$は$[T]$内のすべてのラウンドの集合であり、アルゴリズム2のステップ2での不等式条件が成立しないラウンドです。

Using the bound on $|\mathcal{T}|$ provided in Lemma B.15, we get that,
レマB.15で提供された$|\mathcal{T}|$の制約を使用すると、次のようになります。

$$
\bm{x}_{t}^{\star}=\operatorname*{arg\,max}_{\bm{x}\in\mathcal{X}_{t}}\mu(\bm{x}^{\top}\bm{\theta}^{\star})
$$
$$
R(T)=\sum_{t\notin\mathcal{T}}\mu({\bm{x}_{t}^{\star}}^{\top}\bm{\theta}^{\star})-\mu(\bm{x}_{t}^{\top}\bm{\theta}^{\star})
$$
Now, recall from event $\mathcal{E}$ that all our good events are defined for $t \in [T_{0},T]$.
今、イベント$\mathcal{E}$から思い出してください。すべての良いイベントは$t \in [T_{0},T]$のために定義されています。

Hence, for rounds $t \leq T_{0}$, we can trivially bound the regret as $T_{0}$.
したがって、ラウンド$t \leq T_{0}$の場合、後悔は自明に$T_{0}$として制約できます。

Now, we shift our attention to $t \in [T_{0},T]$.
ここから、$t \in [T_{0},T]$に注意を移します。

From here on, we assume that $t \in [T_{0},T]$.
ここから、$t \in [T_{0},T]$であると仮定します。

From here on, we assume that
ここから、次のように仮定します。

Now, expanding $R(T)$ using an exact Taylor expansion (Definition A.2) along with the fact that $|\ddot{\mu}(.)| \leq \dot{\mu}(.)$ gives us,
今、正確なテイラー展開（定義A.2）を使用して$R(T)$を展開し、$|\ddot{\mu}(.)| \leq \dot{\mu}(.)$という事実を考慮すると、次のようになります。

$$
R(T) \leq R_{1}(T) + R_{2}(T)
$$
Bounding $R_{1}(T)$: To bound $R_{1}(T)$, we define $\mathcal{T}_{1}=\{t\in[T_{0},T]:t\notin\mathcal{T} \text{ and } \dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}) \geq \dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})\}$.
$R_{1}(T)$を制約するために、$\mathcal{T}_{1}=\{t\in[T_{0},T]:t\notin\mathcal{T} \text{ and } \dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}) \geq \dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})\}$を定義します。

And $\mathcal{T}_{2}=\{t\in[T_{0},T]:t\notin\mathcal{T} \text{ and } \dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}) \leq \dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})\}$.
また、$\mathcal{T}_{2}=\{t\in[T_{0},T]:t\notin\mathcal{T} \text{ and } \dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}) \leq \dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})\}$を定義します。

Note that, $\mathcal{T}_{1} \cap \mathcal{T}_{2} = \emptyset$, and $[T_{0},T] \setminus \mathcal{T} = \mathcal{T}_{1} \cup \mathcal{T}_{2}$.
注意してください。$\mathcal{T}_{1} \cap \mathcal{T}_{2} = \emptyset$であり、$[T_{0},T] \setminus \mathcal{T} = \mathcal{T}_{1} \cup \mathcal{T}_{2}$です。

By summing over rounds in $\mathcal{T}_{1}$ we obtain,
$\mathcal{T}_{1}$のラウンドを合計することによって、次のようになります。

Bounding $R_{1}(T)$:
$R_{1}(T)$を制約します：

For some $z_{t}$ between $\bm{x}_{t}^{\top}\bm{\theta}^{\star}$ and $\bm{x}_{t}^{\top}\bm{\theta}_{t+1}$.
$\bm{x}_{t}^{\top}\bm{\theta}^{\star}$と$\bm{x}_{t}^{\top}\bm{\theta}_{t+1}$の間の$z_{t}$について。

Here, (i) follows from the mean value theorem.
ここで、(i)は平均値定理に従います。

Let $R_{1}(T)_{1}=\sum_{t\in\mathcal{T}_{1}}\dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})[(\bm{x}_{t}^{\star}-\bm{x}_{t})^{\intercal}\bm{\theta}^{\star}]$.
$R_{1}(T)_{1}=\sum_{t\in\mathcal{T}_{1}}\dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})[(\bm{x}_{t}^{\star}-\bm{x}_{t})^{\intercal}\bm{\theta}^{\star}]$とします。

And $R_{1}(T)_{2}=\sum_{t\in\mathcal{T}_{1}}\ddot{\mu}(z)(\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}-\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})(\bm{x}_{t}^{\star}-\bm{x}_{t})^{\intercal}\bm{\theta}^{\star}$.
また、$R_{1}(T)_{2}=\sum_{t\in\mathcal{T}_{1}}\ddot{\mu}(z)(\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}-\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})(\bm{x}_{t}^{\star}-\bm{x}_{t})^{\intercal}\bm{\theta}^{\star}$とします。

We bound these separately.
これらを別々に制約します。

where $M(T)=\sum_{t\in\mathcal{T}_{1}}\sum_{i=1}^{N}\sum_{j=1;j\neq i}^{N}\dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})\|\bm{x}^{i}_{t}\|_{(\bm{W}^{i}_{t})^{-1}}\|\bm{x}^{j}_{t}\|_{(\bm{W}^{j}_{t})^{-1}}$.
ここで、$M(T)=\sum_{t\in\mathcal{T}_{1}}\sum_{i=1}^{N}\sum_{j=1;j\neq i}^{N}\dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})\|\bm{x}^{i}_{t}\|_{(\bm{W}^{i}_{t})^{-1}}\|\bm{x}^{j}_{t}\|_{(\bm{W}^{j}_{t})^{-1}}$とします。

Here, (i) follows from the fact that $\dot{\mu}(.) \leq 1$.
ここで、(i)は$\dot{\mu}(.) \leq 1$という事実に従います。

(ii) follows from an application of the Cauchy-Schwarz inequality and the fact that $\bm{\theta}_{t}$ and $\bm{\theta}^{\star} \in \mathcal{C}_{t}(\delta)$.
(ii)はコーシー・シュワルツの不等式の適用と、$\bm{\theta}_{t}$と$\bm{\theta}^{\star} \in \mathcal{C}_{t}(\delta)$という事実に従います。

(iii) follows from a direct application of Lemma B.10 and the definition of $\tilde{\bm{x}}^{i}$.
(iii)はレマB.10の直接的な適用と$\tilde{\bm{x}}^{i}$の定義に従います。

(iv) follows from the UCB rule, i.e. since in slot $i$, $\bm{x}^{i}_{t}$ was chosen, we have $\bm{x}^{i}_{t}^{\top}\bm{\theta}_{t}^{i}+\sqrt{\eta_{t}(\delta)}\|\bm{x}^{i}_{t}\|_{(\bm{W}^{i}_{t})^{-1}} \geq \bm{x}^{\star,i}_{t}^{\top}\bm{\theta}_{t}^{i}+\sqrt{\eta_{t}(\delta)}\|\bm{x}^{\star,i}_{t}\|_{(\bm{W}^{i}_{t})^{-1}}$.
(iv)はUCBルールに従います。すなわち、スロット$i$で$\bm{x}^{i}_{t}$が選ばれたため、$\bm{x}^{i}_{t}^{\top}\bm{\theta}_{t}^{i}+\sqrt{\eta_{t}(\delta)}\|\bm{x}^{i}_{t}\|_{(\bm{W}^{i}_{t})^{-1}} \geq \bm{x}^{\star,i}_{t}^{\top}\bm{\theta}_{t}^{i}+\sqrt{\eta_{t}(\delta)}\|\bm{x}^{\star,i}_{t}\|_{(\bm{W}^{i}_{t})^{-1}}$が成り立ちます。

(v) is a direct application of Lemma E.4 on $\dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})\bm{x}^{i}_{t}$.
(v)は$\dot{\mu}(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1})\bm{x}^{i}_{t}$に関するレマE.4の直接的な適用です。

(vi) holds due to the definition of $\mathcal{T}_{1}$.
(vi)は$\mathcal{T}_{1}$の定義に従います。

(vii) follows from Lemma B.14, and (viii) follows from $\eta_{t}(\delta) \leq CS^{2}Nd\log(T/\delta)$.
(vii)はレマB.14に従い、(viii)は$\eta_{t}(\delta) \leq CS^{2}Nd\log(T/\delta)$に従います。

Turning to $M(T)$, we can bound the term using Rayleigh's quotient and Lemma B.6 (since event $\mathcal{E}_{0}$ holds) as follows:
$M(T)$に移り、レイリーの商とレマB.6を使用して項を制約できます（イベント$\mathcal{E}_{0}$が成立しているため）。

Thus, we get
したがって、次のようになります。

The bound on $R_{1}(T)_{2}$ is as follows:
$R_{1}(T)_{2}$の制約は次のようになります。

Combining all the bounds, we get
すべての制約を組み合わせると、次のようになります。

Applying Lemma E.5 for $R(T)$, we get that
$R(T)$に対してレマE.5を適用すると、次のようになります。

Thus, our overall Regret is
したがって、私たちの全体の後悔は次のようになります。
∎



### B.1 Theorem B.1のための補助補題

B.1  
B.1  

Lemma B.1  
補題 B.1  

$$
\bm{U}_{t}^{-\frac{1}{2}}\bm{W}_{t}\bm{U}_{t}^{-\frac{1}{2}}=\bm{I}_{d}+\bm{A}_{t}
$$  
$$
\bm{U}_{t}^{-\frac{1}{2}}\bm{W}_{t}\bm{U}_{t}^{-\frac{1}{2}}=\bm{I}_{d}+\bm{A}_{t}
$$  

where $\bm{A}_{t}=\begin{bmatrix}\bm{0}_{d}&({\bm{W}^{1}_{t}})^{-\frac{1}{2}}\bm{W}^{1,2}_{t}({\bm{W}^{2}_{t}})^{-\frac{1}{2}}&\ldots&({\bm{W}^{1}_{t}})^{-\frac{1}{2}}\bm{W}^{1,N}_{t}({\bm{W}^{N}_{t}})^{-\frac{1}{2}}\\
\\
({\bm{W}^{2}_{t}})^{-\frac{1}{2}}\bm{W}^{2,1}_{t}({\bm{W}^{1}_{t}})^{-\frac{1}{2}}&\bm{0}_{d}&\ldots&{(\bm{W}^{2}_{t}})^{-\frac{1}{2}}\bm{W}^{2,N}_{t}({\bm{W}^{N}_{t}})^{-\frac{1}{2}}\\
\\
\vdots&\vdots&\ldots&\vdots\\
\\
({\bm{W}^{N}_{t}})^{-\frac{1}{2}}\bm{W}^{N,1}_{t}({\bm{W}^{1}_{t}})^{-\frac{1}{2}}&({\bm{W}^{N}_{t}})^{-\frac{1}{2}}\bm{W}^{N,2}_{t}({\bm{W}^{2}_{t}})^{-\frac{1}{2}}&\ldots&\bm{0}_{d}\end{bmatrix}$  
ここで、$\bm{A}_{t}=\begin{bmatrix}\bm{0}_{d}&({\bm{W}^{1}_{t}})^{-\frac{1}{2}}\bm{W}^{1,2}_{t}({\bm{W}^{2}_{t}})^{-\frac{1}{2}}&\ldots&({\bm{W}^{1}_{t}})^{-\frac{1}{2}}\bm{W}^{1,N}_{t}({\bm{W}^{N}_{t}})^{-\frac{1}{2}}\\
\\
({\bm{W}^{2}_{t}})^{-\frac{1}{2}}\bm{W}^{2,1}_{t}({\bm{W}^{1}_{t}})^{-\frac{1}{2}}&\bm{0}_{d}&\ldots&{(\bm{W}^{2}_{t}})^{-\frac{1}{2}}\bm{W}^{2,N}_{t}({\bm{W}^{N}_{t}})^{-\frac{1}{2}}\\
\\
\vdots&\vdots&\ldots&\vdots\\
\\
({\bm{W}^{N}_{t}})^{-\frac{1}{2}}\bm{W}^{N,1}_{t}({\bm{W}^{1}_{t}})^{-\frac{1}{2}}&({\bm{W}^{N}_{t}})^{-\frac{1}{2}}\bm{W}^{N,2}_{t}({\bm{W}^{2}_{t}})^{-\frac{1}{2}}&\ldots&\bm{0}_{d}\end{bmatrix}$  

It is enough to show  
それを示すのに十分です。  

$$
\bm{W}_{t}=\bm{U}_{t}+\bm{U}_{t}^{\frac{1}{2}}\bm{A}_{t}\bm{U}_{t}^{\frac{1}{2}}
$$  
$$
\bm{W}_{t}=\bm{U}_{t}+\bm{U}_{t}^{\frac{1}{2}}\bm{A}_{t}\bm{U}_{t}^{\frac{1}{2}}
$$  

to prove the claim.  
この主張を証明するために。  

We can decompose  
私たちは分解できます。  

$$
\bm{W}_{t}=\sum_{i=1}^{N}\tilde{\bm{x}}^{i}_{s}
$$  
$$
\bm{W}_{t}=\sum_{i=1}^{N}\tilde{\bm{x}}^{i}_{s}
$$  

Here, (i) follows using the fact  
ここで、(i)は次の事実を使用して従います。  

$$
\bm{x}_{s}=\sum\limits_{i=1}^{N}\tilde{\bm{x}}^{i}_{s}
$$  
$$
\bm{x}_{s}=\sum\limits_{i=1}^{N}\tilde{\bm{x}}^{i}_{s}
$$  

(ii) follows from the definition of  
(ii)は次の定義から従います。  

$$
\tilde{\bm{x}}^{i}_{s}
$$  
$$
\tilde{\bm{x}}^{i}_{s}
$$  

(iii) follows from the definitions of  
(iii)は次の定義から従います。  

$$
\bm{W}^{i}_{t} \text{ and } \bm{W}^{i,j}_{t}
$$  
$$
\bm{W}^{i}_{t} \text{ と } \bm{W}^{i,j}_{t}
$$  

and the fact that  
そして次の事実から。  

$$
\bm{I}_{Nd}=\textrm{diag}(\bm{I}_{d},\ldots\bm{I}_{d})
$$  
$$
\bm{I}_{Nd}=\textrm{diag}(\bm{I}_{d},\ldots\bm{I}_{d})
$$  

and (iv) follows from the definition of  
そして(iv)は次の定義から従います。  

$$
\bm{U}_{t}
$$  
$$
\bm{U}_{t}
$$  

We finish the claim by showing  
私たちは次のことを示すことで主張を終えます。  

$$
\bm{B}_{t}=\begin{bmatrix}\bm{0}_{d}&\bm{W}^{1,2}_{t}&\ldots&\bm{W}^{1,N}_{t}\\
\\
\bm{W}^{2,1}_{t}&\bm{0}_{d}&\ldots&\bm{W}^{2,N}_{t}\\
\\
\vdots&\vdots&\ldots&\vdots\\
\\
\bm{W}^{N,1}_{t}&\bm{W}^{N,2}_{t}&\ldots&\bm{0}_{d}\\
\end{bmatrix}=\bm{U}_{t}^{\frac{1}{2}}\bm{A}_{t}\bm{U}_{t}^{\frac{1}{2}}
$$  
$$
\bm{B}_{t}=\begin{bmatrix}\bm{0}_{d}&\bm{W}^{1,2}_{t}&\ldots&\bm{W}^{1,N}_{t}\\
\\
\bm{W}^{2,1}_{t}&\bm{0}_{d}&\ldots&\bm{W}^{2,N}_{t}\\
\\
\vdots&\vdots&\ldots&\vdots\\
\\
\bm{W}^{N,1}_{t}&\bm{W}^{N,2}_{t}&\ldots&\bm{0}_{d}\\
\end{bmatrix}=\bm{U}_{t}^{\frac{1}{2}}\bm{A}_{t}\bm{U}_{t}^{\frac{1}{2}}
$$  

where  
ここで  

$$
\bm{A}_{t}=\bm{U}_{t}^{-\frac{1}{2}}\bm{B}_{t}\bm{U}_{t}^{-\frac{1}{2}}
$$  
$$
\bm{A}_{t}=\bm{U}_{t}^{-\frac{1}{2}}\bm{B}_{t}\bm{U}_{t}^{-\frac{1}{2}}
$$  

Note that since  
注意してください、次のように。  

$$
\bm{U}_{t}^{-\frac{1}{2}}=\textrm{diag}\left((\bm{W}^{1}_{t})^{-\frac{1}{2}},\ldots,(\bm{W}^{N}_{t})^{-\frac{1}{2}}\right)
$$  
$$
\bm{U}_{t}^{-\frac{1}{2}}=\textrm{diag}\left((\bm{W}^{1}_{t})^{-\frac{1}{2}},\ldots,(\bm{W}^{N}_{t})^{-\frac{1}{2}}\right)
$$  

We can write the  
私たちは次のように書くことができます。  

$$
(i,j)^{\text{th}} \text{ element of } \bm{U}_{t}^{-\frac{1}{2}}\bm{B}_{t}\bm{U}_{t}^{-\frac{1}{2}}
$$  
$$
(i,j)^{\text{th}} \text{ 要素 } \bm{U}_{t}^{-\frac{1}{2}}\bm{B}_{t}\bm{U}_{t}^{-\frac{1}{2}}
$$  

where  
ここで  

$$
\delta_{i,j}
$$  
$$
\delta_{i,j}
$$  

denotes the Kronecker Delta, which takes a value of 1 if $i=j$ and 0 otherwise.  
クロンカーのデルタを示し、$i=j$ の場合は 1 の値を取り、それ以外の場合は 0 の値を取ります。  

Likewise,  
同様に、  

$$
\bar{\delta}(i,j)
$$  
$$
\bar{\delta}(i,j)
$$  

denotes the complement of the Kronecker Delta.  
クロンカーのデルタの補数を示します。  

The second equality follows from the fact that the off-diag entries in  
第二の等式は、オフダイアグのエントリが次の事実から従います。  

$$
\bm{U}_{t}^{-\frac{1}{2}}
$$  
$$
\bm{U}_{t}^{-\frac{1}{2}}
$$  

are zero matrices and likewise, the diagonal entries in  
ゼロ行列であり、同様に、対角エントリは次のようになります。  

$$
\bm{B}_{t}
$$  
$$
\bm{B}_{t}
$$  

This completes the proof.  
これで証明が完了します。  
∎  

Proposition B.1  
命題 B.1  

Let $\Lambda\left(\bm{A}\right)$ denote the set of eigenvalues of $\bm{A}$. Then,  
$\Lambda\left(\bm{A}\right)$ を $\bm{A}$ の固有値の集合とします。  

Proposition B.2  
命題 B.2  

Let $\bm{A}$ and $\bm{B}$ be two symmetric matrices. Then,  
$\bm{A}$ と $\bm{B}$ を二つの対称行列とします。  

Lemma B.2  
補題 B.2  

Define the matrix recurrence relation as follows:  
行列の再帰関係を次のように定義します。  

Then,  
次に、  

$$
\lambda_{max}\left(\bm{A}^{(k)}\right)\leq\sum\limits_{i=1}^{k}\sigma_{max}\left(\bm{Z}_{i}\right)
$$  
$$
\lambda_{max}\left(\bm{A}^{(k)}\right)\leq\sum\limits_{i=1}^{k}\sigma_{max}\left(\bm{Z}_{i}\right)
$$  

and  
そして、  

$$
\lambda_{min}\left(\bm{A}^{(k)}\right)\geq-\sum\limits_{i=1}^{k}\sigma_{max}\left(\bm{Z}_{i}\right)
$$  
$$
\lambda_{min}\left(\bm{A}^{(k)}\right)\geq-\sum\limits_{i=1}^{k}\sigma_{max}\left(\bm{Z}_{i}\right)
$$  

The proof follows by induction.  
証明は帰納法に従います。  

For $k=1$, we see that the statement indeed holds from Lemma E.1.  
$k=1$ の場合、実際に Lemma E.1 からこの主張が成り立つことがわかります。  

Assume that the statement holds for $k=n$, i.e.  
この主張が $k=n$ の場合に成り立つと仮定します。  

$$
\lambda_{max}\left(A^{(n)}\right)\leq\sum\limits_{i=1}^{n}\sigma_{max}\left(\bm{Z}_{i}\right)
$$  
$$
\lambda_{max}\left(A^{(n)}\right)\leq\sum\limits_{i=1}^{n}\sigma_{max}\left(\bm{Z}_{i}\right)
$$  

and  
そして、  

$$
\lambda_{min}\left(A^{(n)}\right)\geq-\sum\limits_{i=1}^{n}\sigma_{min}\left(\bm{Z}_{i}\right)
$$  
$$
\lambda_{min}\left(A^{(n)}\right)\geq-\sum\limits_{i=1}^{n}\sigma_{min}\left(\bm{Z}_{i}\right)
$$  

Consider  
考慮します。  

$$
A(n+1)=[\bm{0}\bm{Z}_{n+1}\bm{Z}_{n+1}^{\top}\bm{A}^{(n)}]=[\bm{0}\bm{Z}_{n+1}\bm{Z}_{n+1}^{\top}\bm{0}]+\bm{0}
$$  
$$
A(n+1)=[\bm{0}\bm{Z}_{n+1}\bm{Z}_{n+1}^{\top}\bm{A}^{(n)}]=[\bm{0}\bm{Z}_{n+1}\bm{Z}_{n+1}^{\top}\bm{0}]+\bm{0}
$$  

We have that,  
私たちは次のように持っています。  

where (i) follows from Proposition B.2,  
ここで (i) は Proposition B.2 から従います。  

(ii) follows from Lemma E.1 and Proposition B.1,  
(ii) は Lemma E.1 と Proposition B.1 から従います。  

and (iii) follows from the induction hypothesis.  
(iii) は帰納法の仮定から従います。  

Similarly,  
同様に、  

where (i) follows from Proposition B.2,  
ここで (i) は Proposition B.2 から従います。  

(ii) follows from Lemma E.1 and Proposition B.1,  
(ii) は Lemma E.1 と Proposition B.1 から従います。  

and (iii) follows from the induction hypothesis.  
(iii) は帰納法の仮定から従います。  

∎  

Lemma B.3  
補題 B.3  

The items chosen at round $t$ in two different slots, say $i$ and $j$, where $i,j\in[N]$ and $i\neq j$ are independent of one another, conditioned on $\mathcal{F}_{t}$.  
ラウンド $t$ で選ばれたアイテムは、異なる2つのスロット、すなわち $i$ と $j$ であり、$i,j\in[N]$ かつ $i\neq j$ の場合、$\mathcal{F}_{t}$ に条件付けられたときに互いに独立です。  

In other words,  
言い換えれば、  

It is easy to see that the item chosen in slot $i$ during round $t$ only depends on  
ラウンド $t$ のスロット $i$ で選ばれたアイテムは、次のようにのみ依存します。  

$$
\{\bm{x}_{s}\}_{s=1}^{t-1},\{\bm{\theta}_{s+1}\}_{s=1}^{t-1}
$$  
$$
\{\bm{x}_{s}\}_{s=1}^{t-1},\{\bm{\theta}_{s+1}\}_{s=1}^{t-1}
$$  

Since, $\mathcal{F}_{t}$ accounts for all of these terms, conditioned on $\mathcal{F}_{t}$, the items being chosen in two different slots are independent of one another.  
$\mathcal{F}_{t}$ はこれらすべての項を考慮しているため、$\mathcal{F}_{t}$ に条件付けられたとき、異なる2つのスロットで選ばれるアイテムは互いに独立です。  

Because of the independence, we can say that  
独立性のため、私たちは次のように言うことができます。  

where the last equality follows from Assumption 2.1.  
最後の等式は仮定 2.1 から従います。  

Lemma B.4  
補題 B.4  

The diversity assumptions in Assumption 2.1 can be extended to the set of vectors  
仮定 2.1 の多様性の仮定は、ベクトルの集合に拡張できます。  

$$
\left\{\sqrt{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}\bm{x}^{i}_{t}\right\}_{i=1}^{N}
$$  
$$
\left\{\sqrt{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}\bm{x}^{i}_{t}\right\}_{i=1}^{N}
$$  

i.e., we can show the following:  
すなわち、次のことを示すことができます。  

1.  
1.  

$$
\mathbb{E}\left[\sqrt{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}\bm{x}^{i}_{t}|\mathcal{F}_{t}\right]=\bm{0}_{d}
$$  
$$
\mathbb{E}\left[\sqrt{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}\bm{x}^{i}_{t}|\mathcal{F}_{t}\right]=\bm{0}_{d}
$$  

2.  
2.  

$$
\mathbb{E}\left[\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)\bm{x}^{i}_{t}{\bm{x}^{j}_{t}}^{\top}|\mathcal{F}_{t}\right]=\bm{0}_{d}
$$  
$$
\mathbb{E}\left[\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)\bm{x}^{i}_{t}{\bm{x}^{j}_{t}}^{\top}|\mathcal{F}_{t}\right]=\bm{0}_{d}
$$  

where $i\neq j$  
ここで $i\neq j$  

3.  
3.  

$$
\mathbb{E}\left[\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)\bm{x}^{i}_{t}{\bm{x}^{i}_{t}}^{\top}|\mathcal{F}_{t}\right]\succcurlyeq\rho\bm{I}_{d}
$$  
$$
\mathbb{E}\left[\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)\bm{x}^{i}_{t}{\bm{x}^{i}_{t}}^{\top}|\mathcal{F}_{t}\right]\succcurlyeq\rho\bm{I}_{d}
$$  

We attempt to bound  
私たちは次のように制約を試みます。  

$$
\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)
$$  
$$
\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)
$$  

Using the Cauchy-Schwarz inequality, it is easy to see that  
コーシー・シュワルツの不等式を使用すると、次のことが簡単にわかります。  

$$
-S\leq\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\leq S
$$  
$$
-S\leq\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\leq S
$$  

Since $\dot{\mu}(.)$ is an increasing function on $(-\infty,0]$ and a decreasing function on $[0,\infty)$, we have that  
$\dot{\mu}(.)$ は $(-\infty,0]$ で増加関数であり、$[0,\infty)$ で減少関数であるため、次のようになります。  

$$
\dot{\mu}\left(-S\right)=\dot{\mu}\left(S\right)
$$  
$$
\dot{\mu}\left(-S\right)=\dot{\mu}\left(S\right)
$$  

Now, we have that  
今、私たちは次のように持っています。  

$$
\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)\in\left[\dot{\mu}\left(S\right),\frac{1}{4}\right]
$$  
$$
\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)\in\left[\dot{\mu}\left(S\right),\frac{1}{4}\right]
$$  

Thus, we can write  
したがって、私たちは次のように書くことができます。  

Similarly, from Lemma B.3,  
同様に、Lemma B.3 から、  

Finally, since  
最後に、次のように。  

$$
\kappa=\max\limits_{\bm{x}}\max\limits_{\bm{\theta}}\frac{1}{\dot{\mu}\left(\bm{x}^{\intercal}\bm{\theta}\right)}
$$  
$$
\kappa=\max\limits_{\bm{x}}\max\limits_{\bm{\theta}}\frac{1}{\dot{\mu}\left(\bm{x}^{\intercal}\bm{\theta}\right)}
$$  

we have that  
私たちは次のように持っています。  

$$
\kappa\geq\frac{1}{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}
$$  
$$
\kappa\geq\frac{1}{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}
$$  

Hence,  
したがって、  

where the last inequality follows from Assumption 2.1.  
最後の不等式は仮定 2.1 から従います。  

∎  

Lemma B.5  
補題 B.5  

For all $i\in[N]$, $j\in[i+1,N]$, and $t\geq 0$,  
すべての $i\in[N]$, $j\in[i+1,N]$, および $t\geq 0$ に対して、  

$$
\left\|\bm{W}^{i,j}_{t}\right\|\leq\sqrt{\frac{t}{2N^{2}}\log\left(\frac{dN(N-1)}{\delta}\right)}
$$  
$$
\left\|\bm{W}^{i,j}_{t}\right\|\leq\sqrt{\frac{t}{2N^{2}}\log\left(\frac{dN(N-1)}{\delta}\right)}
$$  

with probability at least $1-\delta$.  
確率 $1-\delta$ 以上で。  

To prove this lemma, we would invoke Lemma D.2.  
この補題を証明するために、私たちは Lemma D.2 を呼び出します。  

We have already shown in Lemma B.4 that  
私たちはすでに Lemma B.4 で示しました。  

$$
\mathbb{E}\left[\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)\bm{x}^{i}_{t}{\bm{x}^{i}_{t}}^{\top}|\mathcal{F}_{t}\right]=\bm{0}_{d}
$$  
$$
\mathbb{E}\left[\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)\bm{x}^{i}_{t}{\bm{x}^{i}_{t}}^{\top}|\mathcal{F}_{t}\right]=\bm{0}_{d}
$$  

Thus, invoking Lemma D.2 with  
したがって、次のように Lemma D.2 を呼び出します。  

$$
\bm{x}_{s}=\sqrt{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}\bm{x}^{i}_{t}
$$  
$$
\bm{x}_{s}=\sqrt{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}\bm{x}^{i}_{t}
$$  

we get that  
私たちは次のように得ます。  

$$
\mathbb{E}\left[\bm{x}_{s}\bm{x}_{s}^{\top}|\mathcal{F}_{t}\right]\leq\frac{1}{2\sqrt{N}}
$$  
$$
\mathbb{E}\left[\bm{x}_{s}\bm{x}_{s}^{\top}|\mathcal{F}_{t}\right]\leq\frac{1}{2\sqrt{N}}
$$  

Performing a union bound over all $i\in[N]$ and $j\in[i+1,N]$ results in the following:  
すべての $i\in[N]$ および $j\in[i+1,N]$ に対してユニオンバウンドを実行すると、次のようになります。  

This finishes the proof.  
これで証明が完了します。  
∎  

Lemma B.6  
補題 B.6  

For all $i\in[N]$,  
すべての $i\in[N]$ に対して、  

$$
\mathbb{P}\left\{\forall t\geq T_{0}:\lambda_{min}\left(\bm{W}^{i}_{t}\right)\leq 1+\frac{\rho t}{2}\right\}\leq\delta
$$  
$$
\mathbb{P}\left\{\forall t\geq T_{0}:\lambda_{min}\left(\bm{W}^{i}_{t}\right)\leq 1+\frac{\rho t}{2}\right\}\leq\delta
$$  

To prove this claim, we invoke Lemma D.1.  
この主張を証明するために、私たちは Lemma D.1 を呼び出します。  

We have already shown in Lemma B.4 that  
私たちはすでに Lemma B.4 で示しました。  

$$
\mathbb{E}\left[\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)\bm{x}^{i}_{t}|\mathcal{F}_{t}\right]=\bm{0}_{d}
$$  
$$
\mathbb{E}\left[\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)\bm{x}^{i}_{t}|\mathcal{F}_{t}\right]=\bm{0}_{d}
$$  

Thus, invoking Lemma D.1 with  
したがって、次のように Lemma D.1 を呼び出します。  

$$
\bm{x}_{t}=\sqrt{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}\bm{x}^{i}_{t}
$$  
$$
\bm{x}_{t}=\sqrt{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}\bm{x}^{i}_{t}
$$  

we get that  
私たちは次のように得ます。  

$$
\mathbb{P}\left\{\forall t\geq T_{0}:\lambda_{min}\left(\bm{W}^{i}_{t}\right)\leq 1+\frac{\rho t}{2}\right\}\leq\delta
$$  
$$
\mathbb{P}\left\{\forall t\geq T_{0}:\lambda_{min}\left(\bm{W}^{i}_{t}\right)\leq 1+\frac{\rho t}{2}\right\}\leq\delta
$$  

Performing a union bound over all $i\in[N]$ and using the fact that $(N-1)^{2}\geq 1/N^{2}$ gives us:  
すべての $i\in[N]$ に対してユニオンバウンドを実行し、$(N-1)^{2}\geq 1/N^{2}$ という事実を使用すると、次のようになります。  

This finishes the proof.  
これで証明が完了します。  
∎  

Lemma B.7  
補題 B.7  

$$
\mathbb{P}\left\{\mathcal{E}_{0}\right\}\geq 1-2\delta
$$  
$$
\mathbb{P}\left\{\mathcal{E}_{0}\right\}\geq 1-2\delta
$$  

$$
\mathbb{P}\left\{\overline{\mathcal{E}_{0}}\right\}=\mathbb{P}\left\{\overline{\mathcal{E}}_{1}\cup\overline{\mathcal{E}}_{2}\right\}\leq\mathbb{P}\left\{\overline{\mathcal{E}}_{1}\right\}+\mathbb{P}\left\{\overline{\mathcal{E}}_{2}\right\}\leq 2\delta
$$  
$$
\mathbb{P}\left\{\overline{\mathcal{E}_{0}}\right\}=\mathbb{P}\left\{\overline{\mathcal{E}}_{1}\cup\overline{\mathcal{E}}_{2}\right\}\leq\mathbb{P}\left\{\overline{\mathcal{E}}_{1}\right\}+\mathbb{P}\left\{\overline{\mathcal{E}}_{2}\right\}\leq 2\delta
$$  

using a union bound.  
ユニオンバウンドを使用します。  

∎  

Lemma B.8  
補題 B.8  

Define the matrix  
行列を定義します。  

$$
\bm{Z}^{(i)}_{t}=\begin{bmatrix}(\bm{W}^{i}_{t})^{-\frac{1}{2}}\bm{W}^{i,i+1}_{t}(\bm{W}^{i+1}_{t})^{-\frac{1}{2}},\ldots(\bm{W}^{i}_{t})^{-\frac{1}{2}}\bm{W}^{i,N}_{t}(\bm{W}^{N}_{t})^{-\frac{1}{2}}\end{bmatrix}
$$  
$$
\bm{Z}^{(i)}_{t}=\begin{bmatrix}(\bm{W}^{i}_{t})^{-\frac{1}{2}}\bm{W}^{i,i+1}_{t}(\bm{W}^{i+1}_{t})^{-\frac{1}{2}},\ldots(\bm{W}^{i}_{t})^{-\frac{1}{2}}\bm{W}^{i,N}_{t}(\bm{W}^{N}_{t})^{-\frac{1}{2}}\end{bmatrix}
$$  

Then, under event $\mathcal{E}_{0}$, for $t\geq T_{0}$ and $\rho\geq\frac{12}{N}$, we have that  
次に、事象 $\mathcal{E}_{0}$ の下で、$t\geq T_{0}$ および $\rho\geq\frac{12}{N}$ の場合、次のようになります。  

The idea of the proof is borrowed from Das and Sinha [2024].  
証明のアイデアは、Das と Sinha [2024] から借用されています。  

We know that  
私たちは次のことを知っています。  

$$
\left\|\bm{Z}\right\|=\sup\limits_{\left\|\bm{b}\right\|_{2}\leq 1}\left\|\bm{Z}\bm{b}\right\|_{2}
$$  
$$
\left\|\bm{Z}\right\|=\sup\limits_{\left\|\bm{b}\right\|_{2}\leq 1}\left\|\bm{Z}\bm{b}\right\|_{2}
$$  

Thus,  
したがって、  

where (i) follows from triangle inequality,  
ここで (i) は三角不等式から従います。  

(ii) follows from the sub-multiplicativity of the norm,  
(ii) はノルムの部分乗法性から従います。  

(iii) follows from the fact that  
(iii) は次の事実から従います。  

$$
\left\|\bm{A}\right\|=\lambda_{max}\left(\bm{A}\right) \text{ and } \lambda_{max}\left(\bm{A}^{-1}\right)=\frac{1}{\lambda_{min}\left(\bm{A}\right)}
$$  
$$
\left\|\bm{A}\right\|=\lambda_{max}\left(\bm{A}\right) \text{ と } \lambda_{max}\left(\bm{A}^{-1}\right)=\frac{1}{\lambda_{min}\left(\bm{A}\right)}
$$  

(iv) follows from Lemma D.2,  
(iv) は Lemma D.2 から従います。  

(v) follows from $1+\frac{\rho t}{2}\leq 1$ and $t\geq T_{0}$,  
(v) は $1+\frac{\rho t}{2}\leq 1$ および $t\geq T_{0}$ から従います。  

and (vi) follows from the fact that  
(vi) は次の事実から従います。  

$$
\rho N\geq 12
$$  
$$
\rho N\geq 12
$$  

∎  

Lemma B.9  
補題 B.9  

Under event $\mathcal{E}_{0}$, for all $t\geq T_{0}$, we have  
事象 $\mathcal{E}_{0}$ の下で、すべての $t\geq T_{0}$ に対して、次のようになります。  

Define the matrix recurrence relation:  
行列の再帰関係を定義します。  

where  
ここで  

$$
\bm{Z}^{(i)}_{t}=\begin{bmatrix}(\bm{W}^{i}_{t})^{-\frac{1}{2}}\bm{W}^{i,i+1}_{t}(\bm{W}^{i+1}_{t})^{-\frac{1}{2}},\ldots(\bm{W}^{i}_{t})^{-\frac{1}{2}}\bm{W}^{i,N}_{t}(\bm{W}^{N}_{t})^{-\frac{1}{2}}\end{bmatrix}
$$  
$$
\bm{Z}^{(i)}_{t}=\begin{bmatrix}(\bm{W}^{i}_{t})^{-\frac{1}{2}}\bm{W}^{i,i+1}_{t}(\bm{W}^{i+1}_{t})^{-\frac{1}{2}},\ldots(\bm{W}^{i}_{t})^{-\frac{1}{2}}\bm{W}^{i,N}_{t}(\bm{W}^{N}_{t})^{-\frac{1}{2}}\end{bmatrix}
$$  

Then, it is easy to see that  
次に、次のことが簡単にわかります。  

$$
\bm{A}_{t} \text{ from Lemma B.1 is the same as } \bm{A}^{(1)}_{t}
$$  
$$
\bm{A}_{t} \text{ は Lemma B.1 から } \bm{A}^{(1)}_{t} と同じです
$$  

From Lemma B.2, we have that  
Lemma B.2 から、次のようになります。  

$$
\bm{A}_{t} \text{ is bounded.}
$$  
$$
\bm{A}_{t} \text{ は制約されます。}
$$  

Similarly,  
同様に、  

Thus, we can write  
したがって、私たちは次のように書くことができます。  

∎  

Lemma B.10  
補題 B.10  

Let $\tilde{\bm{x}}^{i}$ be the lift of $\bm{x}^{i}$. Then,  
$\tilde{\bm{x}}^{i}$ を $\bm{x}^{i}$ のリフトとします。  

From Lemma B.9, we have  
Lemma B.9 から、次のようになります。  

where the last inequality follows from the definition of the lift of $\bm{x}$ and the structure of $\bm{U}$.  
最後の不等式は、$\bm{x}$ のリフトの定義と $\bm{U}$ の構造から従います。  

∎  

Lemma B.11  
補題 B.11  

With probability at least $1-2\delta$, for all $t\geq T_{0}$, we have  
確率 $1-2\delta$ 以上で、すべての $t\geq T_{0}$ に対して、次のようになります。  

First, notice the similarity in structures between  
まず、次の間の構造の類似性に注意してください。  

$$
\bm{V}^{\mathcal{H}}_{t} \text{ and } \bm{W}_{t}
$$  
$$
\bm{V}^{\mathcal{H}}_{t} \text{ と } \bm{W}_{t}
$$  

as well as between  
および次の間の。  

$$
\bm{U}^{\mathcal{H}}_{t} \text{ and } \bm{U}_{t}
$$  
$$
\bm{U}^{\mathcal{H}}_{t} \text{ と } \bm{U}_{t}
$$  

Thus, we can perform a decomposition similar to the one in Lemma B.1.  
したがって、私たちは Lemma B.1 のものと同様の分解を行うことができます。  

We first show that the diversity conditions hold.  
まず、多様性の条件が成り立つことを示します。  

It is enough to obtain a bound on the norm of the matrices  
行列のノルムに制約を得るのに十分です。  

$$
\bm{V}^{\mathcal{H},i,j}_{t} \text{ and } \bm{V}^{\mathcal{H},i}_{t}
$$  
$$
\bm{V}^{\mathcal{H},i,j}_{t} \text{ と } \bm{V}^{\mathcal{H},i}_{t}
$$  

to prove the claim.  
この主張を証明するために。  

We first show that the diversity assumptions also hold for the set of vectors  
まず、ベクトルの集合に対しても多様性の仮定が成り立つことを示します。  

$$
\left\{\frac{1}{\sqrt{\kappa}}\bm{x}^{i}_{t}\right\}_{i=1}^{N}
$$  
$$
\left\{\frac{1}{\sqrt{\kappa}}\bm{x}^{i}_{t}\right\}_{i=1}^{N}
$$  

For this, we show that  
これに対して、次のことを示します。  

$$
\frac{1}{\sqrt{\kappa}} \text{ is bounded.}
$$  
$$
\frac{1}{\sqrt{\kappa}} \text{ は制約されます。}
$$  

From the proof of Lemma B.4, we have shown that  
Lemma B.4 の証明から、次のように示しました。  

$$
\dot{\mu}\left(\bm{x}^{\intercal}\bm{\theta}\right)\in\left[\dot{\mu}\left(S\right),\frac{1}{4}\right]
$$  
$$
\dot{\mu}\left(\bm{x}^{\intercal}\bm{\theta}\right)\in\left[\dot{\mu}\left(S\right),\frac{1}{4}\right]
$$  

Thus,  
したがって、  

$$
\kappa=\max\limits_{\bm{x}}\max\limits_{\bm{\theta}}\frac{1}{\dot{\mu}\left(\bm{x}^{\intercal}\bm{\theta}\right)}
$$  
$$
\kappa=\max\limits_{\bm{x}}\max\limits_{\bm{\theta}}\frac{1}{\dot{\mu}\left(\bm{x}^{\intercal}\bm{\theta}\right)}
$$  

we have that  
私たちは次のように持っています。  

$$
\kappa\geq\frac{1}{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}
$$  
$$
\kappa\geq\frac{1}{\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}_{t+1}\right)}
$$  

Hence,  
したがって、  

where the last inequality follows from the definition of the lift of $\bm{x}_{s}$ and the structure of $\bm{U}$.  
最後の不等式は、$\bm{x}_{s}$ のリフトの定義と $\bm{U}$ の構造から従います。  

∎  

Lemma B.12  
補題 B.12  

(Faury et al. [2022], Proposition 7) Let $\delta\in(0,1)$ and  
(Faury et al. [2022], 命題 7) $\delta\in(0,1)$ とします。  

$$
\left\{\left(\bm{\theta}_{t},\bm{W}_{t},\bm{\theta}_{t}\right)\right\}_{r}
$$  
$$
\left\{\left(\bm{\theta}_{t},\bm{W}_{t},\bm{\theta}_{t}\right)\right\}_{r}
$$  

be maintained by the ada-OFU-ECOLog algorithm. Then,  
ada-OFU-ECOLog アルゴリズムによって維持されます。  

Lemma B.13  
補題 B.13  

Define the following events:  
次の事象を定義します。  

Then, we have that  
次に、次のようになります。  

$$
\mathbb{P}\left\{\mathcal{E}\right\}\leq 6\delta
$$  
$$
\mathbb{P}\left\{\mathcal{E}\right\}\leq 6\delta
$$  

where the last inequality follows from Lemma B.7, B.11, and B.12 respectively.  
最後の不等式はそれぞれ Lemma B.7, B.11, B.12 から従います。  

∎  

Lemma B.14  
補題 B.14  

(Abeille et al. [2021], Theorem 1)  
(Abeille et al. [2021], 定理 1)  

$$
\sum\limits_{t=1}^{T}\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}\right)\leq R(T)+\sum\limits_{t=1}^{T}\dot{\mu}\left({\bm{x}_{t}^{\star}}^{\intercal}\bm{\theta}^{\star}\right)
$$  
$$
\sum\limits_{t=1}^{T}\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}\right)\leq R(T)+\sum\limits_{t=1}^{T}\dot{\mu}\left({\bm{x}_{t}^{\star}}^{\intercal}\bm{\theta}^{\star}\right)
$$  

where  
ここで  

$$
R_{T}=\sum\limits_{t=1}^{T}\mu\left({\bm{x}_{t}^{\star}}^{\intercal}\bm{\theta}^{\star}\right)-\mu\left(\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}\right)
$$  
$$
R_{T}=\sum\limits_{t=1}^{T}\mu\left({\bm{x}_{t}^{\star}}^{\intercal}\bm{\theta}^{\star}\right)-\mu\left(\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}\right)
$$  

We provide a brief proof for the sake of completeness.  
完全性のために簡単な証明を提供します。  

Here, (i) follows from  
ここで、(i) は次のことから従います。  

$$
\left|\int f(x)dx\right|\leq\int|f(x)|dx
$$  
$$
\left|\int f(x)dx\right|\leq\int|f(x)|dx
$$  

(ii) follows from  
(ii) は次のことから従います。  

$$
\bm{x}_{t}^{\star}\bm{\theta}^{\star}\geq\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}
$$  
$$
\bm{x}_{t}^{\star}\bm{\theta}^{\star}\geq\bm{x}_{t}^{\intercal}\bm{\theta}^{\star}
$$  

(iii) follows since  
(iii) は次のように従います。  

$$
\left|\dot{\mu}(.)\right|\leq\dot{\mu}(.)
$$  
$$
\left|\dot{\mu}(.)\right|\leq\dot{\mu}(.)
$$  

and (iv) follows from applying the Mean-Value Theorem on the expression for $R(T)$.  
(iv) は $R(T)$ の表現に平均値定理を適用することから従います。  

∎  

Lemma B.15  
補題 B.15  

Let $\mathcal{T}$ represent the set of all time instances where the data-dependent condition fails, i.e.  
$\mathcal{T}$ をデータ依存条件が失敗するすべての時間インスタンスの集合とします。すなわち、  

$$
\forall t\in\mathcal{T},\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bar{\bm{\theta}}_{t}\right)\geq 2\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}^{u}_{t}\right)
$$  
$$
\forall t\in\mathcal{T},\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bar{\bm{\theta}}_{t}\right)\geq 2\dot{\mu}\left(\bm{x}_{t}^{\intercal}\bm{\theta}^{u}_{t}\right)
$$  

for all $u\in\{0,1\}$.  
すべての $u\in\{0,1\}$ に対して。  

Then, the proof follows along the lines of Faury et al. [2022].  
この場合、証明は Faury et al. [2022] のラインに沿って進みます。  

By the self-concordance property of the logistic function, we know that  
ロジスティック関数の自己調和性の特性により、私たちは次のことを知っています。  

Thus, if $t\in\mathcal{T}$, we have that  
したがって、$t\in\mathcal{T}$ の場合、次のようになります。  

$$
\left|\bm{x}_{t}^{\intercal}(\bar{\bm{\theta}}_{t}-\bm{\theta}^{u}_{t})\right|\geq\log 2
$$  
$$
\left|\bm{x}_{t}^{\intercal}(\bar{\bm{\theta}}_{t}-\bm{\theta}^{u}_{t})\right|\geq\log 2
$$  

Summing this over all indices in $\mathcal{T}$, we get that  
これを $\mathcal{T}$ のすべてのインデックスにわたって合計すると、次のようになります。  

Here, (i) follows from the Cauchy-Schwarz Inequality,  
ここで、(i) はコーシー・シュワルツの不等式から従います。  

(ii) follows from the fact that  
(ii) は次の事実から従います。  

$$
\bm{\theta}^{u}_{t},\bar{\bm{\theta}}_{t}\in\Theta_{t}
$$  
$$
\bm{\theta}^{u}_{t},\bar{\bm{\theta}}_{t}\in\Theta_{t}
$$  

(iii) follows from  
(iii) は次のように従います。  

$$
(a+b)^{2}\leq 2a^{2}+2b^{2}
$$  
$$
(a+b)^{2}\leq 2a^{2}+2b^{2}
$$  

(iv) follows due to event $\mathcal{E}_{0}^{\prime}$,  
(iv) は事象 $\mathcal{E}_{0}^{\prime}$ によるものです。  

(v) follows from the triangle inequality,  
(v) は三角不等式から従います。  

(vi) follows from a direct application of Lemma E.4 on  
(vi) は次のように Lemma E.4 を直接適用することから従います。  

$$
\frac{1}{\sqrt{\kappa}}\bm{x}^{i}_{t}
$$  
$$
\frac{1}{\sqrt{\kappa}}\bm{x}^{i}_{t}
$$  

and the fact that  
および次の事実から。  

$$
\left\|\frac{1}{\sqrt{\kappa}}\bm{x}^{i}_{t}\right\|_{2}\leq\frac{1}{\sqrt{N\kappa}}
$$  
$$
\left\|\frac{1}{\sqrt{\kappa}}\bm{x}^{i}_{t}\right\|_{2}\leq\frac{1}{\sqrt{N\kappa}}
$$  

and (vii) follows from the definition  
(vii) は定義から従います。  

$$
\beta_{T}(\delta)\leq CS^{6}Nd\log\left(\frac{T}{\delta}\right)
$$  
$$
\beta_{T}(\delta)\leq CS^{6}Nd\log\left(\frac{T}{\delta}\right)
$$  

∎  



## Appendix CSLATE-GLM-TSandSLATE-GLM-TS-FIXED 付録 C

SLATE-GLM-TS
SLATE-GLM-TS-FIXED



### C.1 固定アーム設定におけるアルゴリズム

C.1  
We present a Thompson Sampling based algorithm Slate-GLM-TS-Fixed in the non-contextual (fixed-arm) setting in Algorithm 4.  
Thompson Samplingに基づくアルゴリズムSlate-GLM-TS-Fixedを、非文脈（固定アーム）設定においてAlgorithm 4で示します。  
Following this, we analyze the regret of this algorithm in Theorem C.1.  
次に、このアルゴリズムの後悔を定理C.1で分析します。  
Since we are in the non-contextual setting, we directly use the minimum eigenvalue bound in Assumption C.1.  
非文脈設定にいるため、仮定C.1の最小固有値の境界を直接使用します。  
(See Remarks on Assumption 2.1 in Section 2).  
（セクション2の仮定2.1に関する注釈を参照してください）。  

Algorithm 4  
アルゴリズム4  

Slate-GLM-TS-Fixed  
Slate-GLM-TS-Fixed  

1:  
1:  

Inputs:  
入力：  

2:  
2:  

3:  
3:  

4:  
4:  

for  
for  

do  
行う  

5:  
5:  

6:  
6:  

7:  
7:  

end  
終了  

for  
for  

8:  
8:  

9:  
9:  

10:  
10:  

for  
for  

11:  
11:  

12:  
12:  

while  
while  

do  
行う  

13:  
13:  

14:  
14:  

15:  
15:  

end  
終了  

while  
while  

16:  
16:  

17:  
17:  

5  
5  

18:  
18:  

19:  
19:  

end  
終了  

for  
for  

Assumption C.1  
仮定C.1  

The minimum eigenvalue of the design matrices grows linearly, i.e.  
設計行列の最小固有値は線形に増加します。すなわち、  

Define $T_0 = \max\left\{\frac{(N-1)^{2}}{2\rho^{2}}\log\frac{dN(N-1)}{\delta},\frac{8(N-1)^{2}}{\kappa^{2}\rho^{2}}\log\frac{dN(N-1)}{\delta}\right\} = \frac{(N-1)^{2}}{2\rho^{2}}\log\frac{dN(N-1)}{\delta}$  
$T_0$を次のように定義します：$T_0 = \max\left\{\frac{(N-1)^{2}}{2\rho^{2}}\log\frac{dN(N-1)}{\delta},\frac{8(N-1)^{2}}{\kappa^{2}\rho^{2}}\log\frac{dN(N-1)}{\delta}\right\} = \frac{(N-1)^{2}}{2\rho^{2}}\log\frac{dN(N-1)}{\delta}$  

since $\kappa > 4$.  
ここで、$\kappa > 4$です。  

Theorem C.1  
定理C.1  

(Regret of Slate-GLM-TS-Fixed) At the end of $T \geq T_0$ rounds, the regret of Slate-GLM-TS-Fixed is bounded by  
（Slate-GLM-TS-Fixedの後悔）$T \geq T_0$ラウンドの終わりに、Slate-GLM-TS-Fixedの後悔は次のように制約されます。  

We have that the good events are defined for $t \in [T_0, T]$.  
良い事象は、$t \in [T_0, T]$の範囲で定義されます。  
Since the first $|\mathcal{T}| = \tau$ rounds constitute a warm-up (Steps 4-7 in Algorithm 4), we can trivially bound the regret of these rounds (warm-up as well as first $T_0$) by $1 \cdot \max\{\tau, T_0\}$.  
最初の$|\mathcal{T}| = \tau$ラウンドはウォームアップ（アルゴリズム4のステップ4-7）を構成するため、これらのラウンドの後悔（ウォームアップおよび最初の$T_0$）は$1 \cdot \max\{\tau, T_0\}$で単純に制約できます。  
Going forward, let $\max\{\tau, T_0\} = T'$.  
今後、$\max\{\tau, T_0\} = T'$とします。  

Hence, we have  
したがって、次のようになります。  

$$
R(T) = R^{TS}(T) + R^{PRED}(T)
$$  
$$
R(T) = R^{TS}(T) + R^{PRED}(T)
$$  

where $R^{TS}(T) = \sum_{t=T' + 1}^{T} \mu(\bm{x}_{\star}^{\intercal} \bm{\theta}_{\star}) - \mu(\bm{x}_{t}^{\intercal} \tilde{\bm{\theta}}_{t})$  
ここで、$R^{TS}(T) = \sum_{t=T' + 1}^{T} \mu(\bm{x}_{\star}^{\intercal} \bm{\theta}_{\star}) - \mu(\bm{x}_{t}^{\intercal} \tilde{\bm{\theta}}_{t})$  

and $R^{PRED}(T) = \sum_{t=T' + 1}^{T} \mu(\bm{x}_{t}^{\intercal} \tilde{\bm{\theta}}_{t}) - \mu(\bm{x}_{t}^{\intercal} \bm{\theta}_{\star})$  
および$R^{PRED}(T) = \sum_{t=T' + 1}^{T} \mu(\bm{x}_{t}^{\intercal} \tilde{\bm{\theta}}_{t}) - \mu(\bm{x}_{t}^{\intercal} \bm{\theta}_{\star})$  

The first inequality follows from Lemma C.1.  
最初の不等式は、補題C.1から導かれます。  

We first bound $R^{PRED}(T)$ as follows:  
まず、$R^{PRED}(T)$を次のように制約します：  

where (i) follows from the Self-Concordance result and uses Cauchy-Schwarz,  
ここで、(i)は自己調和性の結果から導かれ、コーシー・シュワルツの不等式を使用します。  

(ii) follows from the fact that $|\bm{x}_{t}^{\top}(\bm{\theta}_{\star} - \bm{\theta}_{t + 1})| \leq \text{diam}_{\mathcal{X}}(\Theta) \leq 1$  
(ii)は、$|\bm{x}_{t}^{\top}(\bm{\theta}_{\star} - \bm{\theta}_{t + 1})| \leq \text{diam}_{\mathcal{X}}(\Theta) \leq 1$という事実から導かれます。  

(Lemma C.1) and Lemma C.5,  
（補題C.1）および補題C.5、  

(iii) follows from Cauchy-Schwarz,  
(iii)はコーシー・シュワルツの不等式から導かれ、  

(iv) follows from Lemma E.4 on $\dot{\mu}(\bm{x}_{t}^{\intercal} \bm{\theta}_{t + 1}) \bm{x}_{t}$  
(iv)は、$\dot{\mu}(\bm{x}_{t}^{\intercal} \bm{\theta}_{t + 1}) \bm{x}_{t}$に関する補題E.4から導かれます。  

and Lemma B.14,  
および補題B.14、  

and (v) follows from the fact that $\sigma_{t}(\delta) \leq CS^{2}Nd\log(T/\delta)$  
(v)は、$\sigma_{t}(\delta) \leq CS^{2}Nd\log(T/\delta)$という事実から導かれます。  

We now turn to bounding $R^{TS}(T)$.  
次に、$R^{TS}(T)$を制約することに移ります。  

Define $J(\bm{\theta}) = \max_{\bm{x} \in \mathcal{X}} \bm{x}^{\intercal} \bm{\theta}$  
$J(\bm{\theta}) = \max_{\bm{x} \in \mathcal{X}} \bm{x}^{\intercal} \bm{\theta}$と定義します。  

Then, it is easy to see that $J(\bm{\theta}_{\star}) = \bm{x}_{\star}^{\top} \bm{\theta}_{\star}$.  
したがって、$J(\bm{\theta}_{\star}) = \bm{x}_{\star}^{\top} \bm{\theta}_{\star}$であることは明らかです。  

Also, note that  
また、次のことに注意してください。  

which uses the fact that the selection of the item in each slot is independent of the rest of the slots.  
これは、各スロットのアイテムの選択が他のスロットとは独立であるという事実を利用しています。  

Hence, we have  
したがって、次のようになります。  

Similar to Section D.2 of the Appendix in Faury et al. [2022] and Section C of Abeille and Lazaric [2017], using the convexity of $J$ gives us:  
Faury et al. [2022]の付録のセクションD.2およびAbeilleとLazaric [2017]のセクションCと同様に、$J$の凸性を使用すると次のようになります。  

where (i) follows from the fact that $\nabla J(\bm{\theta}) = \operatorname*{arg\,max}_{\bm{x} \in \mathcal{X}} \bm{x}^{\top} \bm{\theta}$  
ここで、(i)は、$\nabla J(\bm{\theta}) = \operatorname*{arg\,max}_{\bm{x} \in \mathcal{X}} \bm{x}^{\top} \bm{\theta}$という事実から導かれます。  

and (ii) follows from Lemma C.1.  
(ii)は、補題C.1から導かれます。  

Thus, we have that  
したがって、次のようになります。  

where the first inequality follows from self-concordance.  
最初の不等式は自己調和性から導かれます。  

Substituting this into the original bound, we get  
これを元の境界に代入すると、次のようになります。  

Following the same steps as the proof in Abeille and Lazaric [2017] and referring to Section D.2 in Faury et al. [2022], we get that  
AbeilleとLazaric [2017]の証明と同様の手順を踏み、Faury et al. [2022]のセクションD.2を参照すると、次のようになります。  

Substituting this into the original equation, we get that:  
これを元の方程式に代入すると、次のようになります。  

where (i) follows from self-concordance,  
ここで、(i)は自己調和性から導かれ、  

(ii) follows from the fact that $|\bm{x}_{t}^{\intercal} \bm{\theta}_{t + 1} - \bm{x}_{\star}^{\intercal} \bm{\theta}_{\star}| \leq 2 \text{diam}_{\mathcal{X}}(\Theta)$  
(ii)は、$|\bm{x}_{t}^{\intercal} \bm{\theta}_{t + 1} - \bm{x}_{\star}^{\intercal} \bm{\theta}_{\star}| \leq 2 \text{diam}_{\mathcal{X}}(\Theta)$という事実から導かれます。  

(iii) follows from Cauchy-Schwarz,  
(iii)はコーシー・シュワルツの不等式から導かれ、  

(iv) follows from Lemma E.4 on $\dot{\mu}(\bm{x}_{t}^{\intercal} \bm{\theta}_{t + 1}) \bm{x}_{t}$  
(iv)は、$\dot{\mu}(\bm{x}_{t}^{\intercal} \bm{\theta}_{t + 1}) \bm{x}_{t}$に関する補題E.4から導かれます。  

and (v) follows from the fact that $\sigma_{t}(\delta) \leq CS^{2}Nd\log(T/\delta)$  
(v)は、$\sigma_{t}(\delta) \leq CS^{2}Nd\log(T/\delta)$という事実から導かれます。  

Combining the bounds on $R(T)$, we get  
$R(T)$の境界を組み合わせると、次のようになります。  

Using Lemma E.5, we get  
補題E.5を使用すると、次のようになります。  

Finally, combining the bound for Regret(T) gives us:  
最後に、Regret(T)の境界を組み合わせると、次のようになります。  

∎  
∎  



### C.2 Theorem C.1のための補助補題

### C.2 補助補題 C.1

Let $\delta \in (0,1)$, then, setting $\tau = CS^{6}N^{2}d^{2}\kappa\log(T/\delta)^{2}$ ensures that $\Theta$ returned after the warm-up phase satisfies the following:
$\delta \in (0,1)$ のとき、$\tau = CS^{6}N^{2}d^{2}\kappa\log(T/\delta)^{2}$ と設定すると、ウォームアップフェーズの後に返される $\Theta$ は以下を満たします。

1. $\mathbb{P}\left\{\bm{\theta}_{\star}\in\Theta\right\}\geq 1-\delta$
   1. $\mathbb{P}\left\{\bm{\theta}_{\star}\in\Theta\right\}\geq 1-\delta$

2. $\text{diam}_{\mathcal{X}}\left(\Theta\right)\leq 1$
   2. $\text{diam}_{\mathcal{X}}\left(\Theta\right)\leq 1$

The proof for the first part is the same as the proof for the first part in Proposition 5 in Faury et al. [2022] since the proof does not depend on the manner in which the arm is selected.
最初の部分の証明は、Faury et al. [2022] の命題5の最初の部分の証明と同じであり、証明はアームの選択方法に依存しません。

For the second part notice that:
2番目の部分については、以下に注意してください。

where (i) follows from an application of Cauchy-Schwarz, (ii) follows from the definition of $\Theta$, (iii) follows from Lemma C.3, (iv) follows from how items in each slot are selected, (v) follows from Lemma E.4 on $\frac{1}{\sqrt{\kappa}}\bm{x}^{i}_{t}$.
ここで、(i) はコーシー・シュワルツの適用から、(ii) は $\Theta$ の定義から、(iii) は補題 C.3 から、(iv) は各スロット内のアイテムの選択方法から、(v) は補題 E.4 の $\frac{1}{\sqrt{\kappa}}\bm{x}^{i}_{t}$ から導かれます。

Thus, setting $\tau \leq Nd\beta_{t}(\delta)\kappa\log(T/\kappa N) \leq CS^{6}N^{2}d^{2}\kappa\log(T/\kappa N)\log(T/\delta)$ ensures $\text{diam}_{\mathcal{X}}\left(\Theta\right)\leq 1$.
したがって、$\tau \leq Nd\beta_{t}(\delta)\kappa\log(T/\kappa N) \leq CS^{6}N^{2}d^{2}\kappa\log(T/\kappa N)\log(T/\delta)$ と設定すると、$\text{diam}_{\mathcal{X}}\left(\Theta\right)\leq 1$ が保証されます。

∎

### 補題 C.2

For $t \geq \frac{(N-1)^{2}}{2\rho^{2}}\log\frac{dN(N-1)}{\delta}$, we have
$t \geq \frac{(N-1)^{2}}{2\rho^{2}}\log\frac{dN(N-1)}{\delta}$ のとき、次のようになります。

Following the same line of thought as Lemma B.3, Lemma B.4, and Lemma B.5, we have that
補題 B.3、B.4、および B.5 と同様の考え方に従って、次のようになります。

Following the same line of thought as Lemma B.8 and making use of Assumption C.1, we can derive
補題 B.8 と同様の考え方に従い、仮定 C.1 を利用することで、次のように導出できます。

where the last inequality follows from the fact that $t \geq \frac{(N-1)^{2}}{2\rho^{2}}\log\frac{dN(N-1)}{2\delta}$.
最後の不等式は、$t \geq \frac{(N-1)^{2}}{2\rho^{2}}\log\frac{dN(N-1)}{2\delta}$ であることから導かれます。

Finally, using the same line of thought as Lemma B.9, we get
最後に、補題 B.9 と同様の考え方を用いることで、次のようになります。

∎

### 補題 C.3

For $t \geq \frac{8(N-1)^{2}}{\kappa^{2}\rho^{2}}\log\frac{dN(N-1)}{\delta}$, we have
$t \geq \frac{8(N-1)^{2}}{\kappa^{2}\rho^{2}}\log\frac{dN(N-1)}{\delta}$ のとき、次のようになります。

Following the same line of thought as Lemma B.11 and making use of Assumption C.1, we get
補題 B.11 と同様の考え方に従い、仮定 C.1 を利用することで、次のようになります。

∎

where the last inequality follows from the fact that $t \geq \frac{8(N-1)^{2}}{\kappa^{2}\rho^{2}}\log\frac{dN(N-1)}{\delta}$.
最後の不等式は、$t \geq \frac{8(N-1)^{2}}{\kappa^{2}\rho^{2}}\log\frac{dN(N-1)}{\delta}$ であることから導かれます。

Finally, we can show that
最後に、次のことを示すことができます。

### 補題 C.4

Define the distribution $\mathcal{D}=\bigtimes\limits_{i=1}^{N}\mathcal{D}^{TS}$ where $\mathcal{D}^{TS}$ is a multivariate distribution that satisfies the properties given in Definition E.2. Then, $\mathcal{D}$ also satisfies the properties given in Definition E.2, making it a suitable distribution for Thompson Sampling.
分布 $\mathcal{D}=\bigtimes\limits_{i=1}^{N}\mathcal{D}^{TS}$ を定義します。ここで、$\mathcal{D}^{TS}$ は定義 E.2 に示される特性を満たす多変量分布です。したがって、$\mathcal{D}$ も定義 E.2 に示される特性を満たし、Thompson Sampling に適した分布となります。

Define $\bm{\eta}=\left(\bm{\eta}^{1},\ldots,\bm{\eta}^{N}\right)\in\mathbb{R}^{Nd}$ where $\bm{\eta}^{i}\sim\mathcal{D}^{TS}$. Then, it is easy to see that sampling $\bm{\eta}^{i}, i\in[N]$ in an iid fashion from $\mathcal{D}^{TS}$ is the same as sampling $\bm{\eta}$ from $\mathcal{D}$.
$\bm{\eta}=\left(\bm{\eta}^{1},\ldots,\bm{\eta}^{N}\right)\in\mathbb{R}^{Nd}$ を定義し、ここで $\bm{\eta}^{i}\sim\mathcal{D}^{TS}$ とします。すると、$\mathcal{D}^{TS}$ から独立同分布で $\bm{\eta}^{i}, i\in[N]$ をサンプリングすることは、$\mathcal{D}$ から $\bm{\eta}$ をサンプリングすることと同じであることが簡単にわかります。

We begin by showing the Concentration property, i.e. $\exists C,C^{\prime}$ such that
集中特性を示すことから始めます。すなわち、$\exists C,C^{\prime}$ が存在して次のようになります。

Since $\mathcal{D}^{TS}$ satisfies the concentration property, we know that $\left\|\bm{\eta}^{i}\right\|_{2}\geq\sqrt{cd\log\frac{c^{\prime}d}{\delta}}$ with probability at most $\delta$.
$\mathcal{D}^{TS}$ が集中特性を満たすため、$\left\|\bm{\eta}^{i}\right\|_{2}\geq\sqrt{cd\log\frac{c^{\prime}d}{\delta}}$ が確率 $\delta$ 以下で成り立つことがわかります。

Hence, it is easy to see that
したがって、次のことが簡単にわかります。

with probability at most $\delta^{N}$.
確率 $\delta^{N}$ 以下で。

Setting $C=cN,C^{\prime}=(c^{\prime})^{N}d^{N-1}$, we get that
$C=cN,C^{\prime}=(c^{\prime})^{N}d^{N-1}$ と設定すると、次のようになります。

with probability at least $1-\delta^{\prime}$.
確率 $1-\delta^{\prime}$ 以上で。

This proves that $\mathcal{D}$ satisfies the concentration property.
これにより、$\mathcal{D}$ が集中特性を満たすことが証明されます。

We now show that $\mathcal{D}$ satisfies the Anti-Concentration property, i.e. $\exists P\in(0,1)$ such that
次に、$\mathcal{D}$ が反集中特性を満たすことを示します。すなわち、$\exists P\in(0,1)$ が存在して次のようになります。

Assume $\bm{u}=\left(\bm{u}^{1},\ldots,\bm{u}^{N}\right)$ such that $\left\|\bm{u}\right\|_{2}=1$.
$\bm{u}=\left(\bm{u}^{1},\ldots,\bm{u}^{N}\right)$ とし、$\left\|\bm{u}\right\|_{2}=1$ であると仮定します。

This implies that $\sum\limits_{i=1}^{N}\left\|\bm{u}^{i}\right\|_{2}^{2}=1$ which in turn implies that $\left\|\bm{u}^{i}\right\|_{2}\leq 1$.
これは、$\sum\limits_{i=1}^{N}\left\|\bm{u}^{i}\right\|_{2}^{2}=1$ であることを意味し、さらに $\left\|\bm{u}^{i}\right\|_{2}\leq 1$ であることを示します。

Since, $\left\|\bm{u}^{i}\right\|_{2}\leq 1$, we have that $\left\|\bm{u}^{i}\right\|_{2}^{2}\leq\left\|\bm{u}^{i}\right\|_{2}$, and since $\bm{\eta}^{i}\sim\mathcal{D}^{TS}$, we have that
したがって、$\left\|\bm{u}^{i}\right\|_{2}\leq 1$ であるため、$\left\|\bm{u}^{i}\right\|_{2}^{2}\leq\left\|\bm{u}^{i}\right\|_{2}$ となり、さらに $\bm{\eta}^{i}\sim\mathcal{D}^{TS}$ であるため、次のようになります。

Hence, we have that
したがって、次のようになります。

Thus, we have that $\mathbb{P}\left\{\bm{u}^{\top}\bm{\eta}\geq\left\|\bm{u}\right\|_{2}\right\} \geq 1-(1-p)^{N}$.
したがって、$\mathbb{P}\left\{\bm{u}^{\top}\bm{\eta}\geq\left\|\bm{u}\right\|_{2}\right\} \geq 1-(1-p)^{N}$ となります。

Setting $P=1-(1-p)^{N}$ finishes the claim.
$P=1-(1-p)^{N}$ と設定することで、主張が完了します。

∎

### 補題 C.5

At round $t \geq T_{0}$, let $\tilde{\bm{\theta}}^{i}=\bm{\theta}^{i}_{t}+\sqrt{\sigma_{t}(\delta)}(\bm{W}^{i}_{t})^{-\frac{1}{2}}\bm{\eta}^{i}$ for all $i\in[N]$, where $\bm{\eta}^{i}\sim\mathcal{D}^{TS}$.
ラウンド $t \geq T_{0}$ において、すべての $i\in[N]$ に対して $\tilde{\bm{\theta}}^{i}=\bm{\theta}^{i}_{t}+\sqrt{\sigma_{t}(\delta)}(\bm{W}^{i}_{t})^{-\frac{1}{2}}\bm{\eta}^{i}$ とします。ここで、$\bm{\eta}^{i}\sim\mathcal{D}^{TS}$ です。

Define $\tilde{\bm{\theta}}_{t}=\left(\tilde{\bm{\theta}}^{1}_{t},\ldots,\tilde{\bm{\theta}}^{N}_{t}\right)$.
$\tilde{\bm{\theta}}_{t}=\left(\tilde{\bm{\theta}}^{1}_{t},\ldots,\tilde{\bm{\theta}}^{N}_{t}\right)$ を定義します。

Assuming event $\mathcal{E}$ holds, we have that,
事象 $\mathcal{E}$ が成立すると仮定すると、次のようになります。

We can write $\tilde{\bm{\theta}}_{t}=\left(\tilde{\bm{\theta}}^{1}_{t},\ldots,\tilde{\bm{\theta}}^{N}_{t}\right)$ as the following:
$\tilde{\bm{\theta}}_{t}=\left(\tilde{\bm{\theta}}^{1}_{t},\ldots,\tilde{\bm{\theta}}^{N}_{t}\right)$ を次のように書くことができます。

Thus, we get
したがって、次のようになります。

where (i) follows from Lemma C.2 and (ii) follows from the concentration property shown in Lemma C.4.
ここで、(i) は補題 C.2 から、(ii) は補題 C.4 で示された集中特性から導かれます。



## Appendix D ランダム行列とベクトルの集中結果

Appendix D
レマ D.1
レマ D.1
.
(Chatterji et al. [2020], レマ 7の一般化) $\{ \bm{x}_{s} \}_{s=1}^{\top}$ を $\mathbb{R}^{d}$ の確率過程とし、フィルタ $\mathcal{F}_{t}$ に対して、$\mathbb{E}[\bm{x}_{s} | \mathcal{F}_{s-1}] = \bm{0}_{d}$ かつ $\mathbb{E}[\bm{x}_{s} \bm{x}_{s}^{\top} | \mathcal{F}_{s-1}] \succcurlyeq \rho \bm{I}_{d}$ が成り立つとする。
(Chatterji et al. [2020], レマ 7の一般化) Let $\{ \bm{x}_{s} \}_{s=1}^{\top}$ be a stochastic process in $\mathbb{R}^{d}$ such that for filtration $\mathcal{F}_{t}$, we have that $\mathbb{E}[\bm{x}_{s} | \mathcal{F}_{s-1}] = \bm{0}_{d}$ and $\mathbb{E}[\bm{x}_{s} \bm{x}_{s}^{\top} | \mathcal{F}_{s-1}] \succcurlyeq \rho \bm{I}_{d}$.
さらに、$\|\bm{x}_{s}\|_{2} \leq m$ が $s \geq 1$ のすべてに対して成り立つとする。
Further, let $\|\bm{x}_{s}\|_{2} \leq m$ for all $s \geq 1$.

また、行列を定義する。
Also, define the matrix.

その後、確率 $1 - \delta$ で次が成り立つ。
Then, with probability at least $1 - \delta$, we have that.

$0 \leq c \leq 1$ のとき、すべての $t$ に対して次が成り立つ。
for $0 \leq c \leq 1$ and for all $t$ such that.

証明は Chatterji et al. [2020] のものと同様である。
The proof follows on the same lines as that of Chatterji et al. [2020].

$\mathbb{E}[\bm{x}_{s} \bm{x}_{s}^{\top} | \mathcal{F}_{s-1}] = \bm{\Sigma}_{c} \succcurlyeq \rho \bm{I}_{d}$ と仮定する。
Assume $\mathbb{E}[\bm{x}_{s} \bm{x}_{s}^{\top} | \mathcal{F}_{s-1}] = \bm{\Sigma}_{c} \succcurlyeq \rho \bm{I}_{d}$.

行列マルティンゲールを定義する。
Define the matrix martingale $\bm{Z}_{s} = \sum_{s=1}^{t} [\bm{x}_{s} \bm{x}_{s}^{\top} - \bm{\Sigma}_{c}]$ with $\bm{Z}_{0} = 0$.
また、対応するマルティンゲール差分列を $\bm{X}_{s} = \bm{Z}_{s} - \bm{Z}_{s-1}$ とする。
and the corresponding martingale difference sequence $\bm{X}_{s} = \bm{Z}_{s} - \bm{Z}_{s-1}$ for all $s \geq 1$.

次が成り立つ。
We have that.

$\|\bm{x}_{s}\|_{2} \leq m$ である。
$\|\bm{x}_{s}\|_{2} \leq m$.

また、$\|\bm{\Sigma}_{c}\| = \|\mathbb{E}[\bm{x}_{s} \bm{x}_{s}^{\top} | \mathcal{F}_{t-1}] \| \leq \|\bm{x}_{s}\|_{2}^{2} \leq m^{2}$ である。
Also, $\|\bm{\Sigma}_{c}\| = \|\mathbb{E}[\bm{x}_{s} \bm{x}_{s}^{\top} | \mathcal{F}_{t-1}]\| \leq \|\bm{x}_{s}\|_{2}^{2} \leq m^{2}$.

したがって、三角不等式を用いると次が成り立つ。
Therefore, using triangle inequality, we have that.

最終的に次が成り立つ。
Finally, we have that.

したがって、行列フリードマン不等式（レマ E.2）を適用すると、次が得られる。
Thus, applying the Matrix Freedman Inequality (Lemma E.2) gives us.

$t \geq \frac{12m^{4}+4m^{2}\rho(1-c)}{3(1-c)^{2}\rho^{2}}\log\left(\frac{2dT}{\delta}\right)$ を選ぶ。
Choosing $t \geq \frac{12m^{4}+4m^{2}\rho(1-c)}{3(1-c)^{2}\rho^{2}}\log\left(\frac{2dT}{\delta}\right)$.

今、ノルムの定義を思い出す。
Now, recall the definition of the norm.

これを代入すると次のようになる。
Substituting this definition results in.

Rayleighの商を用いると、次が成り立つ。
Now, using Rayleigh’s quotient, we also know that.

したがって、次が成り立つ。
Thus, we have that.

このことは確率 $1 - \frac{\delta}{T}$ で成り立つ。
This holds with probability $1 - \frac{\delta}{T}$.

すべての時間インデックスに対してユニオンバウンドを行うことで、主張が完了する。
Performing a union bound over all time indices finishes the claim.
∎
レマ D.2
レマ D.2
.
(Das and Sinha [2024], レマ 17) $\delta \in (0,1)$ とし、$\bm{x}_{s} \in \mathbb{R}^{d_{1}}$ および $\bm{z}_{s} \in \mathbb{R}^{d_{2}}$ とする。
(Das and Sinha [2024], Lemma 17) Let $\delta \in (0,1)$ and $\bm{x}_{s} \in \mathbb{R}^{d_{1}}$ and $\bm{z}_{s} \in \mathbb{R}^{d_{2}}$ such that.

$\mathbb{E}[\bm{x}_{s} \bm{z}_{s}^{\top} | \mathcal{F}_{s-1}] = \bm{0}_{d_{1} \times d_{2}}$ である。
$\mathbb{E}[\bm{x}_{s} \bm{z}_{s}^{\top} | \mathcal{F}_{s-1}] = \bm{0}_{d_{1} \times d_{2}}$.

行列 $\bm{M}_{t} = \sum_{s=1}^{t} \bm{x}_{s} \bm{z}_{s}^{\top}$ を定義する。
Define $\bm{M}_{t} = \sum_{s=1}^{t} \bm{x}_{s} \bm{z}_{s}^{\top}$.

さらに、$\|\bm{x}_{s}\|_{2} \leq m_{1}$ および $\|\bm{z}_{s}\|_{2} \leq m_{2}$ と仮定する。
Further, assume that $\|\bm{x}_{s}\|_{2} \leq m_{1}$ and $\|\bm{z}_{s}\|_{2} \leq m_{2}$.

次が成り立つ。
Then, with probability at least $1 - \delta$.

$\bm{X}_{s} = \bm{x}_{s} \bm{z}_{s}^{\top}$ とする。
Denote $\bm{X}_{s} = \bm{x}_{s} \bm{z}_{s}^{\top}$.

$\mathbb{E}[\bm{X}_{s} | \mathcal{F}_{s-1}] = \bm{0}_{d_{1} \times d_{2}}$ である。
Since $\mathbb{E}[\bm{X}_{s} | \mathcal{F}_{s-1}] = \bm{0}_{d_{1} \times d_{2}}$.

$\bm{X}_{s}$ はマルティンゲール差分列である。
$\bm{X}_{s}$ is a Martingale Difference sequence.

さらに、$\bm{M}_{t} = \sum_{s=1}^{t} \bm{X}_{s}$ はマルティンゲール差分列の和である。
Further, $\bm{M}_{t} = \sum_{s=1}^{t} \bm{X}_{s}$ is the sum of Martingale Difference Sequences.

次に、$\bm{X}_{s}$ のエルミート拡張の二乗を考える。
Consider the square of the Hermitian Dilation of $\bm{X}_{s}$.

行列アズマ不等式（レマ E.3）を適用すると、次が得られる。
Applying the Matrix Azuma inequality (Lemma E.3) gives us.

$\sigma_{t}^{2} = (m_{1} \wedge m_{2})^{4} t$ である。
$\sigma_{t}^{2} = (m_{1} \wedge m_{2})^{4} t$.

したがって、次を選ぶ。
Thus, choosing $\epsilon = \sqrt{8(m_{1} \wedge m_{2})^{4} t \log\left(\frac{d_{1}+d_{2}}{\delta}\right)}$ finishes the proof.



## Appendix E その他の有用な結果と定義

Appendix E

Definition E.1
定義 E.1
.
(Hermitian Dilation) The Hermitian matrix for a matrix $\bm{A}$ is defined as
(Hermitian Dilation) 行列 $\bm{A}$ のエルミート行列は次のように定義されます。

Lemma E.1
補題 E.1
.
(Das and Sinha [2024], Lemma 16) Let $\mathcal{H}(\bm{Z})=\begin{bmatrix}\mathbf{0}&\bm{Z}\\ \bm{Z}^{\top}&\mathbf{0}\end{bmatrix}$ where $\bm{Z}$ has positive singular values.
(Das and Sinha [2024], 補題 16) $\mathcal{H}(\bm{Z})=\begin{bmatrix}\mathbf{0}&\bm{Z}\\ \bm{Z}^{\top}&\mathbf{0}\end{bmatrix}$ とし、ここで $\bm{Z}$ は正の特異値を持つとします。
Then, it holds almost surely, $\lambda_{max}\left(\mathcal{H}(\bm{Z})\right)=-\lambda_{min}\left(\mathcal{H}(\bm{Z})\right)=\sigma_{max}\left(\bm{Z}\right)$.
すると、ほぼ確実に、$\lambda_{max}\left(\mathcal{H}(\bm{Z})\right)=-\lambda_{min}\left(\mathcal{H}(\bm{Z})\right)=\sigma_{max}\left(\bm{Z}\right)$ が成り立ちます。

Lemma E.2
補題 E.2
.
(Matrix Freedman Inequality Tropp [2011a] Corollary 1.3) Define a matrix martingale $\bm{Z}_{s}\in\mathbb{R}^{d_{1}\times d_{2}}$ with respect to the filtration $\mathcal{F}_{s}$ and a martingale difference sequence $\bm{X}_{s}=\bm{Z}_{s}-\bm{Z}_{s-1}$.
(行列フリードマン不等式 Tropp [2011a] 補題 1.3) 行列マルティンゲール $\bm{Z}_{s}\in\mathbb{R}^{d_{1}\times d_{2}}$ をフィルトレーション $\mathcal{F}_{s}$ に関して定義し、マルティンゲール差列 $\bm{X}_{s}=\bm{Z}_{s}-\bm{Z}_{s-1}$ とします。
Assume that the difference sequence is almost surely uniformly bounded, i.e. $\|\bm{X}_{s}\| \leq R$.
差列がほぼ確実に一様に有界であると仮定します。すなわち、$\|\bm{X}_{s}\| \leq R$ です。

Then, for all $u \geq 0$ and $\omega^{2} > 0$, we have
すべての $u \geq 0$ および $\omega^{2} > 0$ に対して、次のようになります。

Lemma E.3
補題 E.3
.
(Matrix Azuma Inequality, Tropp [2011b], Theorem 7.1) Let $\{\bm{X}_{s}\}_{s=1}^{\infty}$ be a matrix martingale difference sequence in $\mathbb{R}^{d_{1}\times d_{2}}$ and let $\mathcal{H}(\bm{X}_{s})$ represent the Hermitian Dilation of $\bm{X}_{s}$.
(行列アズマ不等式、Tropp [2011b]、定理 7.1) $\{\bm{X}_{s}\}_{s=1}^{\infty}$ を $\mathbb{R}^{d_{1}\times d_{2}}$ の行列マルティンゲール差列とし、$\mathcal{H}(\bm{X}_{s})$ を $\bm{X}_{s}$ のエルミート拡張とします。
Let $\{\bm{A}_{s}\}_{s=1}^{\infty}$ be a sequence of matrices in $\mathbb{R}^{(d_{1}+d_{2})\times(d_{1}+d_{2})}$ such that $\mathbb{E}[\bm{X}_{s}|\mathcal{F}_{s-1}]=\mathbf{0}$ and $\mathcal{H}(\bm{X}_{s})^{2} \preccurlyeq \bm{A}_{s}^{2}$.
$\{\bm{A}_{s}\}_{s=1}^{\infty}$ を $\mathbb{R}^{(d_{1}+d_{2})\times(d_{1}+d_{2})}$ の行列列とし、$\mathbb{E}[\bm{X}_{s}|\mathcal{F}_{s-1}]=\mathbf{0}$ および $\mathcal{H}(\bm{X}_{s})^{2} \preccurlyeq \bm{A}_{s}^{2}$ が成り立つとします。
Let $\sigma_{t}^{2}=\lambda_{max}\sum_{s=1}^{t}\bm{A}_{k}^{2}$ for $t \geq 1$.
$t \geq 1$ のとき、$\sigma_{t}^{2}=\lambda_{max}\sum_{s=1}^{t}\bm{A}_{k}^{2}$ とします。

Then, for all $\epsilon \geq 0$:
すべての $\epsilon \geq 0$ に対して：

Lemma E.4
補題 E.4
.
(Elliptical Potential Lemma, Abbasi-yadkori et al. [2011], Lemma 11) Let $\{\bm{x}_{s}\}_{s=1}^{\top}$ represent a set of vectors in $\mathbb{R}^{d}$ and let $\|\bm{x}_{s}\|_{2} \leq L$.
(楕円ポテンシャル補題、Abbasi-yadkori et al. [2011]、補題 11) $\{\bm{x}_{s}\}_{s=1}^{\top}$ を $\mathbb{R}^{d}$ のベクトルの集合とし、$\|\bm{x}_{s}\|_{2} \leq L$ とします。
Let $\bm{V}_{s}=\lambda\bm{I}_{d}+\sum_{m=1}^{s-1}\bm{x}_{m}\bm{x}_{m}^{\top}$.
$\bm{V}_{s}=\lambda\bm{I}_{d}+\sum_{m=1}^{s-1}\bm{x}_{m}\bm{x}_{m}^{\top}$ とします。
Then, for $\lambda \geq 1$:
$\lambda \geq 1$ のとき：

Lemma E.5
補題 E.5
.
(Abeille et al. [2021], Proposition 7) Let $b,c \geq 0$ and $x^{2}-bx-c \leq 0$. Then, $x^{2} \leq 2b^{2}+2c$.
(Abeille et al. [2021]、命題 7) $b,c \geq 0$ とし、$x^{2}-bx-c \leq 0$ とします。すると、$x^{2} \leq 2b^{2}+2c$ となります。
Since the coefficient of the quadratic term is 1, the quadratic expression can attain non-positive values only if it has two distinct or equal real roots.
二次項の係数が1であるため、二次式は2つの異なるまたは等しい実数の根を持つ場合にのみ非正の値を取ることができます。
We denote the roots by $\alpha_{1}$ and $\alpha_{2}$.
根を $\alpha_{1}$ と $\alpha_{2}$ とします。
Without loss of generality, assume $\alpha_{1}=\frac{b-\sqrt{b^{2}+4c}}{2}$ and $\alpha_{2}=\frac{b+\sqrt{b^{2}+4c}}{2}$.
一般性を失わずに、$\alpha_{1}=\frac{b-\sqrt{b^{2}+4c}}{2}$ および $\alpha_{2}=\frac{b+\sqrt{b^{2}+4c}}{2}$ とします。
Then, the set of $x$ for which $x^{2}-bx-c \leq 0$ is true is $x \in [\alpha_{1},\alpha_{2}]$.
したがって、$x^{2}-bx-c \leq 0$ が成り立つ $x$ の集合は $x \in [\alpha_{1},\alpha_{2}]$ です。
Thus, we can say
したがって、次のように言えます。

using the fact that $\sqrt{a+b} \leq \sqrt{a}+\sqrt{b}$ for $a,b \geq 0$.
$a,b \geq 0$ のとき、$\sqrt{a+b} \leq \sqrt{a}+\sqrt{b}$ という事実を用います。
Finally,
最後に、

using the fact that $(b-\sqrt{c})^{2} \geq 0 \implies 2b\sqrt{c} \leq b^{2}+c$.
$(b-\sqrt{c})^{2} \geq 0 \implies 2b\sqrt{c} \leq b^{2}+c$ という事実を用います。
∎
証明終了

Definition E.2
定義 E.2
.
(Multivariate distribution for Thompson Sampling, Abeille and Lazaric [2017], Definition 1) $\mathcal{D}^{TS}$ is a suitable multivariate distribution on $\mathbb{R}^{d}$ for Thompson Sampling if it is absolutely continuous with respect to the Lebesgue measure and satisfies the following properties:
(トンプソンサンプリングのための多変量分布、Abeille and Lazaric [2017]、定義 1) $\mathcal{D}^{TS}$ はトンプソンサンプリングのための $\mathbb{R}^{d}$ 上の適切な多変量分布であり、ルベーグ測度に関して絶対連続であり、次の特性を満たす場合です：
1. Concentration: There exist constants $c$ and $c'$ such that $\forall \delta \in (0,1)$, $\mathbb{P}_{\bm{\eta}\sim\mathcal{D}^{TS}}\left\{\left\|\bm{\eta}\right\|_{2} \leq \sqrt{cd\log\frac{c'}{d\delta}}\right\} \geq 1-\delta$.
1. 集中：定数 $c$ と $c'$ が存在して、すべての $\delta \in (0,1)$ に対して、$\mathbb{P}_{\bm{\eta}\sim\mathcal{D}^{TS}}\left\{\left\|\bm{\eta}\right\|_{2} \leq \sqrt{cd\log\frac{c'}{d\delta}}\right\} \geq 1-\delta$ が成り立ちます。
2. Anti-Concentration: There exists a strictly positive probability $p$ such that for any $\bm{u} \in \mathbb{R}^{d}$, $\mathbb{P}_{\bm{\eta}\sim\mathcal{D}^{TS}}\left\{\bm{u}^{\top}\bm{\eta} \geq \left\|\bm{u}\right\|_{2}\right\} \geq p$.
2. 反集中：任意の $\bm{u} \in \mathbb{R}^{d}$ に対して、厳密に正の確率 $p$ が存在して、$\mathbb{P}_{\bm{\eta}\sim\mathcal{D}^{TS}}\left\{\bm{u}^{\top}\bm{\eta} \geq \left\|\bm{u}\right\|_{2}\right\} \geq p$ が成り立ちます。



## Appendix F 追加実験および実験の詳細

Appendix F  
このセクションでは、セクション5で示した実験を裏付けるための追加のプロットを提供します。また、私たちの実験設定に関する追加の詳細も提供します。

5  
(a)  
(b)  
(c)  
(d)  
(e)  
(f)  
(g)  
(h)  
(i)  
Figure 2:  
すべての図において、陰影のある領域は二つの標準偏差を表しています。図2(a)および2(b)は、実験1（セクション5）からのグラフを示しており、私たちのアルゴリズムSlate-GLM-OFUおよびSlate-GLM-TSを、有限および無限のコンテキスト設定における対応するada-OFU-ECOLogおよびTS-ECOLogと比較しています。

2(a)  
2(b)  
Experiment 1  
5  
Slate-GLM-OFU  
Slate-GLM-TS  
ada-OFU-ECOLog  
TS-ECOLog  
図2(c)および2(d)は、実験3（セクション5）からのグラフを示しており、私たちのアルゴリズムSlate-GLM-OFU、Slate-GLM-TS、およびSlate-GLM-TS-Fixedを、いくつかの最先端の非コンテキストロジスティックバンディットアルゴリズムと比較しています。図2(c)では、Slate-GLM-OFUおよびSlate-GLM-TSに関する不確実性のみを示しています。Slate-GLM-OFUが最良のパフォーマンスを示し、比較可能なパフォーマンスを持つ唯一のアルゴリズムはMPSです。一方、Slate-GLM-TSはada-OFU-ECOLogおよびMPSよりもパフォーマンスが劣り、TS-ECOLogと同等の結果を示しています。しかし、図2(d)では、MPSの分散が非常に高いため、実際にはこのアルゴリズムが信頼性に欠けることを示しています。

2(c)  
2(d)  
Experiment 3  
5  
Slate-GLM-OFU  
Slate-GLM-TS  
Slate-GLM-TS-Fixed  
2(c)  
Slate-GLM-OFU  
Slate-GLM-TS  
Slate-GLM-OFU  
MPS  
Slate-GLM-TS  
ada-OFU-ECOLog  
MPS  
TS-ECOLog  
2(d)  
MPS  
図2(e)および2(f)は、アルゴリズムの平均および最大（ラウンドごとの）実行時間における二つの標準偏差を示しています。ada-OFU-ECOLogおよびTS-ECOLogの実行時間は指数関数的に増加することがわかります。さらに、Slate-GLM-OFUおよびSlate-GLM-TSの平均および最大（ラウンドごとの）実行時間の間の大きなギャップ（下の表で強調されています）は、真のラウンドごとの時間が最大よりもはるかに低いことを示しています。私たちが主論文で述べたように、アルゴリズムのラウンドごとの実行時間は、ラウンドごとのプル時間と更新時間の合計として計算します。図2(g)および2(h)は、平均および最大プル時間（ラウンドごと）を示し、図2(i)は平均ラウンドごとの更新時間を表示します。ada-OFU-ECOLogおよびTS-ECOLogのプル時間はスロット数の増加に伴い指数関数的に増加する一方で、更新時間はすべてのアルゴリズムで類似しています。したがって、ラウンドごとの実行時間の違いは、各アルゴリズムのプル時間に主に起因しており、これは私たちの理論的主張と一致しています。さらに、各アルゴリズムの平均および最大ラウンドごとのプル時間を表2にまとめて、より明確にしています。

2(e)  
2(f)  
ada-OFU-ECOLog  
TS-ECOLog  
2  
Slots  
ada-OFU-ECOLog  
Slate-GLM-OFU  
TS-ECOLog  
Slate-GLM-TS  
Average (ms)  
Maximum (ms)  
Average (ms)  
Maximum (ms)  
Average (ms)  
Maximum (ms)  
Average (ms)  
Maximum (ms)  
Table 2:  
さて、私たちの実験設定に関する追加の詳細を提供します。実験3では、Ordered Slate BanditおよびETC-SlateをKale et al. [2010]およびRhuggenaath et al. [2020]からそれぞれ実装します。これらのアルゴリズムはセミバンディットフィードバック用に設計されているため、私たちの設定でこれらのアルゴリズムを実装するために修正を加えます。これらの修正は以下に詳述します。

Experiment 3  
Ordered Slate Bandit  
ETC-Slate  
Ordered Slate Bandit: Kale et al. [2010]の元のアルゴリズムは、基底集合𝒳が存在し、$|\mathcal{X}|=K$であると仮定し、学習者は𝒳からN個のアイテムを選択します。したがって、彼らのアルゴリズムは、各基底アイテムが任意のスロットに配置される可能性が等しいと仮定しています。したがって、彼らは初期分布$P$を次のように設定します：$P_{i,j}=1$ for all $i \in [N]$ and $j \in [K]$。一方、私たちは異なるアイテムのセット$\mathcal{X}^{i}_{t}$を各スロット$i \in [N]$に対して取得するため、同じ仮定をすることはできません。したがって、初期分布を次のように変更します：$P_{i,j}=1$ if and only if $j \in [K(i-1)+1,K(i)]$。この修正により、特定のスロットに対して選択できるアイテムが制限されます。各ラウンドの探索分布にも同様の修正が加えられます。損失行列の構築方法には大きな違いがあります。このアルゴリズムはセミバンディットフィードバック用に設計されているため、アルゴリズムは各ラウンドで選択された各スロットのアイテムに対する損失を伝播します。私たちは、損失が報酬の加法的逆数であるという事実を利用し、伝播したい損失には二つの選択肢があります。ロジスティック設定で動作するため、明らかな選択肢は非線形損失をアルゴリズムに伝播することです。しかし、スレートの総損失は各スロットで得られた損失の合計であると仮定されているため、線形損失の方が適しているようです。私たちはこれら二つの選択肢を試し、非線形損失を持つアルゴリズムが非常に高い後悔を引き起こすことを発見しました。したがって、私たちはOrdered Slate Banditアルゴリズムを線形損失で比較することにします。

Ordered Slate Bandit  
Ordered Slate Bandit  
ETC-Slate: Rhuggenaath et al. [2020]の元のアルゴリズムもセミバンディットフィードバック用に設計されており、各スロットの報酬が一様分布などの分布からサンプリングされると仮定されています（Rhuggenaath et al. [2020]の例1を参照）。しかし、私たちの場合、スロットレベルでの報酬分布の概念はありません。したがって、スロットレベルでの報酬分布を作成するために、スロット$i$の報酬が$\mathcal{N}({\bm{x}_{s}^{i}}^{\top}\bm{\theta}_{\star}^{i},0.0001)$からサンプリングされると仮定します。これにより、期待値として特定のスロットに帰属する報酬がプレイされたアイテムの線形報酬となることが保証されます。スレートレベルの報酬関数$f$を、スロットレベルで得られた報酬の合計に適用されるシグモイド関数とし、アルゴリズムを進めます。私たちはETC-Slateが非常に高い後悔を引き起こすことを発見し、したがってこのアルゴリズムを比較に含めません。


```md
## Appendix G Empirical Validation of the Diversity Assumption (Assumption 2.1) 付録 G 多様性仮定の実証的検証（仮定 2.1）

In this section, we show that our (instance and algorithm dependent) diversity assumption we make indeed holds for a lot of instances. 
このセクションでは、私たちが行う（インスタンスおよびアルゴリズム依存の）多様性仮定が多くのインスタンスに対して実際に成り立つことを示します。

We choose the number of slots $N$ to be 3 and the number of items in each slot $|\mathcal{X}^{i}_{t}|$ is fixed to 5. 
スロットの数を $N$ = 3 とし、各スロットのアイテム数 $|\mathcal{X}^{i}_{t}|$ を 5 に固定します。

The dimension of items for each slot is fixed to 5, resulting in the slate having a dimension $d=15$. 
各スロットのアイテムの次元は 5 に固定され、スレートの次元は $d=15$ になります。

The items for each slot are randomly sampled from $[-1,1]^{5}$ and normalized to have norm $\frac{1}{\sqrt{3}}$, 
各スロットのアイテムは $[-1,1]^{5}$ からランダムにサンプリングされ、ノルムを $\frac{1}{\sqrt{3}}$ に正規化します。

while $\bm{\theta}_{\star}$ is randomly sampled from $[-1,1]^{15}$. 
また、$\bm{\theta}_{\star}$ は $[-1,1]^{15}$ からランダムにサンプリングされます。

We operate in the Infinite context setting, wherein the items in each slot change every time round (check Experiment 1 in Section 5 for more details). 
私たちは無限コンテキスト設定で操作し、各スロットのアイテムは毎回のラウンドで変化します（詳細についてはセクション 5 の実験 1 を参照してください）。

We run both Slate-GLM-OFU and Slate-GLM-TS 100 times with different seeds for a horizon of $T=10000$ rounds. 
Slate-GLM-OFU と Slate-GLM-TS の両方を、異なるシードで 100 回、$T=10000$ ラウンドのホライズンで実行します。

For each run of the algorithm, we plot the minimum eigenvalue of $\bm{W}^{i}_{t}$ for $i \in [3]$ as a function of the time round $t$ and show our results in Figure 3. 
アルゴリズムの各実行について、時間ラウンド $t$ の関数として $i \in [3]$ の $\bm{W}^{i}_{t}$ の最小固有値をプロットし、結果を図 3 に示します。

The figures clearly depict a (near) linear growth in the eigenvalues of the matrices $\bm{W}^{i}_{t}$ for all the slots $i \in [3]$ and all rounds $t \in [T]$. 
図は、すべてのスロット $i \in [3]$ およびすべてのラウンド $t \in [T]$ に対して、行列 $\bm{W}^{i}_{t}$ の固有値が（ほぼ）線形に成長する様子を明確に示しています。

Experiment 1 実験 1

Slate-GLM-OFU Slate-GLM-TS
```



## Instructions for reporting errors エラー報告の手順

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. 
私たちは論文のHTMLバージョンを改善し続けており、あなたのフィードバックはアクセシビリティとモバイルサポートの向上に役立ちます。 
To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:
HTMLのエラーを報告して、変換とレンダリングの改善に役立てるために、以下のいずれかの方法を選択してください：
- Click the "Report Issue" button.
- "Report Issue"ボタンをクリックしてください。
- Open a report feedback form via keyboard, use "Ctrl + ?".
- キーボードを使って報告フィードバックフォームを開くには、「Ctrl + ?」を使用してください。
- Make a text selection and click the "Report Issue for Selection" button near your cursor.
- テキストを選択し、カーソルの近くにある「選択範囲の問題を報告」ボタンをクリックしてください。
- You can use Alt+Y to toggle on and Alt+Shift+Y to toggle off accessible reporting links at each section.
- 各セクションでアクセシブルな報告リンクをオンにするにはAlt+Yを、オフにするにはAlt+Shift+Yを使用できます。

Our team has already identified the following issues. 
私たちのチームはすでに以下の問題を特定しています。 
We appreciate your time reviewing and reporting rendering errors we may not have found yet. 
私たちは、まだ見つけていない可能性のあるレンダリングエラーをレビューし報告するためにあなたが費やした時間に感謝します。 
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
