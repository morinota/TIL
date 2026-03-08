refs: https://arxiv.org/pdf/2209.07663.pdf


Monolith: Real Time Recommendation System With Collisionless Embedding Table
Monolith: Collisionless Embedding Tableを用いたリアルタイム推薦システム

### 0.0.1. Zhuoran Liu Leqi Zou Xuan Zou ##### Bytedance Inc. Bytedance Inc. Bytedance Inc.  
### 0.0.2. Caihua Wang Biao Zhang Da Tang ##### Bytedance Inc. Bytedance Inc. Bytedance Inc.
### 0.0.3. Bolin Zhu[∗] Yijie Zhu Peng Wu
##### 0.0.3.0.1. Fudan University Bytedance Inc. Bytedance Inc.
### 0.0.4. Ke Wang Youlong Cheng[†] ##### Bytedance Inc. Bytedance Inc.
youlong.cheng@bytedance.com  

## 0.1. ABSTRACT 要約

Building a scalable and real-time recommendation system is vital for many businesses driven by time-sensitive customer feedback, such as short-videos ranking or online ads. 
スケーラブルでリアルタイムな推薦システムを構築することは、短編動画のランキングやオンライン広告など、時間に敏感な顧客フィードバックに駆動される多くのビジネスにとって重要です。
Despite the ubiquitous adoption of production-scale deep learning frameworks like TensorFlow or PyTorch, these general-purpose frameworks fall short of business demands in recommendation scenarios for various reasons: 
TensorFlowやPyTorchのような生産規模の深層学習フレームワークが普及しているにもかかわらず、これらの汎用フレームワークはさまざまな理由で推薦シナリオにおけるビジネスの要求を満たしていません。
on one hand, tweaking systems based on static parameters and dense computations for recommendation with dynamic and sparse features is detrimental to model quality; 
一方で、動的かつスパースな特徴を持つ推薦のために静的パラメータと密な計算に基づいてシステムを調整することは、モデルの品質に悪影響を及ぼします。
on the other hand, such frameworks are designed with batch-training stage and serving stage completely separated, preventing the model from interacting with customer feedback in real-time. 
他方で、そのようなフレームワークはバッチトレーニング段階とサービス段階が完全に分離されるように設計されており、モデルがリアルタイムで顧客フィードバックと相互作用することを妨げています。
These issues led us to reexamine traditional approaches and explore radically different design choices. 
これらの問題は、私たちに従来のアプローチを再検討し、根本的に異なる設計選択肢を探求させました。
In this paper, we present Monolith[1], a system tailored for online training. 
本論文では、**オンライントレーニングに特化したシステムMonolith**[1]を紹介します。
Our design has been driven by observations of our application workloads and production environment that reflects a marked departure from other recommendations systems. 
私たちの設計は、他の推薦システムとは明らかに異なるアプリケーションのワークロードと生産環境の観察に基づいています。
Our contributions are manifold: 
私たちの貢献は多岐にわたります。
first, we crafted a collisionless embedding table with optimizations such as expirable embeddings and frequency filtering to reduce its memory footprint; 
まず、メモリフットプリントを削減するために、期限付き埋め込みや頻度フィルタリングなどの最適化を施した衝突のない埋め込みテーブルを作成しました。
second, we provide an production-ready online training architecture with high fault-tolerance; 
次に、高い耐障害性を持つ生産準備が整ったオンライントレーニングアーキテクチャを提供します。
finally, we proved that system reliability could be traded-off for real-time learning. 
最後に、システムの信頼性はリアルタイム学習とトレードオフできることを証明しました。
Monolith has successfully landed in the BytePlus Recommend[2] product.  
MonolithはBytePlus Recommend[2]製品に成功裏に導入されました。

<!-- ここまで読んだ! -->

**ACM Reference Format:** Zhuoran Liu, Leqi Zou, Xuan Zou, Caihua Wang, Biao Zhang, Da Tang, Bolin Zhu, Yijie Zhu, Peng Wu, Ke Wang, and Youlong Cheng. 2022. Monolith: Real Time Recommendation System With Collisionless Embedding Table.  
**ACMリファレンス形式:** Zhuoran Liu, Leqi Zou, Xuan Zou, Caihua Wang, Biao Zhang, Da Tang, Bolin Zhu, Yijie Zhu, Peng Wu, Ke Wang, and Youlong Cheng. 2022. Monolith: Collisionless Embedding Tableを用いたリアルタイム推薦システム。

In Proceedings of 5th Workshop on Online Recommender Systems and User _Modeling, in conjunction with the 16th ACM Conference on Recommender_ _Systems (ORSUM@ACM RecSys 2022). ACM, New York, NY, USA, 10 pages._  
第5回オンライン推薦システムとユーザーモデリングに関するワークショップの議事録、16回ACM推薦システム会議（ORSUM@ACM RecSys 2022）と併催。ACM, ニューヨーク, NY, USA, 10ページ。

<!-- ここまで読んだ! -->

## 0.2. 1 INTRODUCTION はじめに  

The past decade witnessed a boom of businesses powered by recommendation techniques.  
過去10年間は、推薦技術によって支えられたビジネスのブームを目撃しました。
In pursuit of a better customer experience, delivering personalized content for each individual user as real-time response is a common goal of these business applications.  
より良い顧客体験を追求する中で、各個人のユーザーに対してリアルタイムでパーソナライズされたコンテンツを提供することは、これらのビジネスアプリケーションの共通の目標です。
To this end, information from a user’s latest interaction is often used as the primary input for training a model, as it would best depict a user’s portrait and make predictions of user’s interest and future behaviors.  
この目的のために、ユーザーの最新のインタラクションからの情報がモデルのトレーニングの主要な入力として使用されることが多く、これはユーザーの肖像を最もよく描写し、ユーザーの興味や将来の行動を予測することができます。

<!-- ここまで読んだ! -->

Deep learning have been dominating recommendation models [5, 6, 10, 12, 20, 21] as the gigantic amount of user data is a natural fit for massively data-driven neural models.  
深層学習は、膨大な量のユーザーデータが大規模なデータ駆動型ニューラルモデルに自然に適合するため、推薦モデルを支配しています[5, 6, 10, 12, 20, 21]。
However, efforts to leverage the power of deep learning in industry-level recommendation systems are constantly encountered with problems arising from the unique characteristics of data derived from real-world user behavior.
しかし、業界レベルの推薦システムにおいて深層学習の力を活用しようとする努力は、現実のユーザー行動から派生したデータの独自の特性から生じる問題に常に直面しています。
These data are drastically different from those used in conventional deep learning problems like language modeling or computer vision in two aspects:  
これらのデータは、言語モデリングやコンピュータビジョンのような従来の深層学習問題で使用されるデータとは2つの点で大きく異なります。

(1) The features are mostly sparse, categorical and dynamically changing;  
    (1) **特徴量は主にスパースで、カテゴリカルで、動的に変化します。**

(2) The underlying distribution of training data is non-stationary, a.k.a. Concept Drift [8].  
    (2) **トレーニングデータの基礎となる分布は非定常**であり、いわゆるコンセプトドリフト[8]です。

Such differences have posed unique challenges to researchers and engineers working on recommendation systems.  
このような違いは、推薦システムに取り組む研究者やエンジニアに独自の課題をもたらしています。

### 0.2.1. 1.1 Sparsity and Dynamism スパース性と動的性  

![]()
**Figure 1: Monolith Online Training Architecture.**  
**図1: Monolithオンライントレーニングアーキテクチャ。**

The data for recommendation mostly contain sparse categorical features, some of which appear with low frequency.  
推薦のためのデータは主にスパースなカテゴリカル特徴を含み、その中には低頻度で現れるものもあります。
The common practice of mapping them to a high-dimensional embedding space would give rise to a series of issues:

- Unlike language models where number of word-pieces are limited, the amount of users and ranking items are orders of magnitude larger.  
単語の数が限られている言語モデルとは異なり、ユーザーの数とランキングアイテムの数は桁違いに大きいです。
Such an enormous embedding table would hardly fit into single host memory;  
このような巨大な埋め込みテーブルは、単一のホストメモリに収まることはほとんどありません。

- Worse still, the size of embedding table is expected to grow over time as more users and items are admitted, while frameworks like [1, 17] uses a fixed-size dense variables to represent embedding table.  
さらに悪いことに、埋め込みテーブルのサイズは、より多くのユーザーやアイテムが追加されるにつれて時間とともに増加することが期待されますが、[1, 17]のようなフレームワークは埋め込みテーブルを表すために固定サイズの密な変数を使用します。

In practice, many systems adopt low-collision hashing [3, 6] as a way to reduce memory footprint and to allow growing of IDs.  
**実際には、多くのシステムがメモリフットプリントを削減し、IDの増加を許可する方法として低衝突ハッシング[3, 6]を採用しています。** (hash-trickってやつか...!!:thinking:)
This relies on an over-idealistic assumption that IDs in the embedding table is distributed evenly in frequency, and collisions are harmless to the model quality.  
これは、埋め込みテーブル内のIDが頻度的に均等に分布しており、衝突がモデルの品質に無害であるという過度に理想的な仮定に依存しています。
Unfortunately this is rarely true for a realworld recommendation system, where a small group of users or items have significantly more occurrences.  
**残念ながら、これは現実の推薦システムではほとんど真実ではなく、小さなグループのユーザーやアイテムが著しく多くの出現を持っています。**
With the organic growth of embedding table size, chances of hash key collision increases and lead to deterioration of model quality [3].  
埋め込みテーブルのサイズが有機的に成長するにつれて、ハッシュキーの衝突の可能性が増加し、モデルの品質が悪化します[3]。

<!-- ここまで読んだ! -->

Therefore it is a natural demand for production-scale recommendation systems to have the capacity to capture as many features in its parameters, and also have the capability of elastically adjusting the number of users and items it tries to book-keep.  
したがって、**production規模の推薦システムには、そのパラメータにできるだけ多くの特徴をキャプチャする能力と、管理しようとするユーザーやアイテムの数を弾力的に調整する能力が求められます。**

<!-- ここまで読んだ! -->

### 0.2.2. 1.2 Non-stationary Distribution 非定常分布

Visual and linguistic patterns barely develop in a time scale of centuries, while the same user interested in one topic could shift their zeal every next minute.  
視覚的および言語的パターンは、数世代の時間スケールでほとんど発展しませんが、同じユーザーが1つのトピックに興味を持つと、その熱意は次の瞬間に変わる可能性があります。
As a result, the underlying distribution of user data is non-stationary, a phenomenon commonly referred to as Concept Drift [8].  
その結果、**ユーザーデータの基礎となる分布は非定常であり、一般的にコンセプトドリフト[8]と呼ばれる現象**です。

Intuitively, information from a more recent history can more effectively contribute to predicting the change in a user’s behavior.  
直感的には、より最近の履歴からの情報は、ユーザーの行動の変化を予測するのにより効果的に寄与します。
To mitigate the effect of Concept Drift, serving models need to be updated from new user feedback as close to real-time as possible to reflect the latest interest of a user.  
コンセプトドリフトの影響を軽減するために、サービスモデルはユーザーの最新の興味を反映するために、新しいユーザーフィードバックからできるだけリアルタイムに更新される必要があります。

<!-- ここまで読んだ! -->

In light of these distinction and in observation of issues that arises from our production, we designed Monolith, a large-scale recommendation system to address these pain-points.  
これらの違いを考慮し、私たちの生産から生じる問題を観察した結果、これらの痛点に対処するための大規模な推薦システムMonolithを設計しました。
We did extensive experiments to verify and iterate our design in the production environment.  
私たちは、生産環境での設計を検証し、反復するために広範な実験を行いました。
Monolith is able to  
Monolithは次のことが可能です。

(1) Provide full expressive power for sparse features by designing a collisionless hash table and a dynamic feature eviction mechanism;  
    (1) 衝突のないハッシュテーブルと動的特徴排除メカニズムを設計することにより、スパースな特徴に対して完全な表現力を提供します。

(2) Loop serving feedback back to training in real-time with online training.  
    (2) オンライントレーニングを使用して、サービスフィードバックをリアルタイムでトレーニングに戻すことができます。

Empowered by these architectural capacities, Monolith consistently outperforms systems that adopts hash-tricks with collisions with roughly similar memory usage, and achieves state-of-the-art online serving AUC without overly burdening our servers’ computation power.  
これらのアーキテクチャ能力により、Monolithは、衝突のあるハッシュトリックを採用するシステムを、ほぼ同様のメモリ使用量で一貫して上回り、サーバーの計算能力を過度に負担することなく、最先端のオンラインサービングAUCを達成します。

<!-- ここまで読んだ! -->

---

The rest of the paper is organized as follows.  
残りの論文は次のように構成されています。
We first elaborate design details of how Monolith tackles existing challenge with collisionless hash table and realtime training in Section 2.  
まず、セクション2でMonolithが衝突のないハッシュテーブルとリアルタイムトレーニングの既存の課題にどのように対処するかの設計詳細を詳述します。
Experiments and results will be presented in Section 3, along with production-tested conclusions and some discussion of trade-offs between timesensitivity, reliability and model quality.  
実験と結果はセクション3で提示され、生産でテストされた結論と時間感度、信頼性、モデル品質の間のトレードオフに関するいくつかの議論が行われます。
Section 4 summarizes related work and compares them with Monolith.  
セクション4では関連する作業を要約し、それらをMonolithと比較します。
Section 5 concludes this work.  
セクション5ではこの作業を結論づけます。

![]()
**Figure 2: Worker-PS Architecture.**  
**図2: Worker-PSアーキテクチャ。**

<!-- ここまで読んだ! -->

## 0.3. 2 DESIGN 設計

The overall architecture of Monolith generally follows TensorFlow’s distributed Worker-ParameterServer setting (Figure 2)  
Monolithの全体的なアーキテクチャは、一般的にTensorFlowの分散Worker-ParameterServer設定（図2）に従っています。



. . .
Server Server
**Figure 2: Worker-PS Architecture.**
#### 0.3.0.1. 2 DESIGN 設計
The overall architecture of Monolith generally follows TensorFlow’s distributed Worker-ParameterServer setting (Figure 2). 
Monolithの全体アーキテクチャは、一般的にTensorFlowの分散Worker-ParameterServer設定（図2）に従っています。
In a Worker-PS architecture, machines are assigned different roles; Worker machines are responsible for performing computations as defined by the graph, and PS machines stores parameters and updates them according to gradients computed by Workers.
Worker-PSアーキテクチャでは、マシンに異なる役割が割り当てられます。Workerマシンはグラフで定義された計算を実行する責任があり、PSマシンはパラメータを保存し、Workersによって計算された勾配に従ってそれらを更新します。
In recommendation models, parameters are categorized into two sets: dense and sparse. 
推薦モデルでは、パラメータは2つのセットに分類されます：密なパラメータと疎なパラメータ。
Dense parameters are weights/variables in a deep neural network, and sparse parameters refer to embedding tables that corresponds to sparse features. 
密なパラメータは深層ニューラルネットワークの重み/変数であり、疎なパラメータは疎な特徴に対応する埋め込みテーブルを指します。
In our design, both dense and sparse parameters are part of TensorFlow Graph, and are stored on parameter servers.
私たちの設計では、密なパラメータと疎なパラメータの両方がTensorFlowグラフの一部であり、パラメータサーバーに保存されます。
Similar to TensorFlow’s Variable for dense parameters, we designed a set of highly-efficient, collisionless, and flexible HashTable operations for sparse parameters. 
TensorFlowの密なパラメータ用のVariableに似て、私たちは疎なパラメータ用に非常に効率的で衝突のない柔軟なHashTable操作のセットを設計しました。
As an complement to TensorFlow’s limitation that arises from separation of training and inference, Monolith’s elastically scalable online training is designed to efficiently synchronize parameters from training-PS to online serving-PS within short intervals, with model robustness guarantee provided by fault tolerance mechanism.
トレーニングと推論の分離から生じるTensorFlowの制限を補完するために、Monolithの弾力的にスケーラブルなオンライントレーニングは、トレーニングPSからオンラインサービングPSへのパラメータを短い間隔で効率的に同期するように設計されており、モデルの堅牢性はフォールトトレランスメカニズムによって保証されています。
#### 0.3.0.2. 2.1 Hash Table ハッシュテーブル
A first principle in our design of sparse parameter representation is to avoid cramping information from different IDs into the same fixed-size embedding. 
疎なパラメータ表現の設計における第一原則は、異なるIDからの情報を同じ固定サイズの埋め込みに詰め込むことを避けることです。
Simulating a dynamic size embedding table with an out-of-the-box TensorFlow Variable inevitably leads to ID collision, which exacerbates as new IDs arrive and table grows.
既製のTensorFlow Variableを使用して動的サイズの埋め込みテーブルをシミュレートすると、必然的にIDの衝突が発生し、新しいIDが到着しテーブルが成長するにつれて悪化します。
Therefore instead of building upon Variable, we developed a new key-value HashTable for our sparse parameters.
したがって、Variableに基づくのではなく、私たちは疎なパラメータ用の新しいキー-バリューHashTableを開発しました。
Our HashTable utilizes Cuckoo Hashmap [16] under the hood, which supports inserting new keys without colliding with existing ones. 
私たちのHashTableは、Cuckoo Hashmap [16]を内部で利用しており、既存のキーと衝突することなく新しいキーを挿入することをサポートします。
Cuckoo Hashing achieves worst-case $O(1)$ time complexity for lookups and deletions, and an expected amortized $O(1)$ time for insertions. 
Cuckoo Hashingは、検索と削除に対して最悪の場合の$O(1)$の時間計算量を達成し、挿入に対して期待される平均$O(1)$の時間を実現します。
As illustrated in Figure 3 it maintains two tables $T_0$, $T_1$ with different hash functions $h_0(x)$, $h_1(x)$, and an element would be stored in either one of them. 
図3に示すように、異なるハッシュ関数$h_0(x)$、$h_1(x)$を持つ2つのテーブル$T_0$、$T_1$を維持し、要素はそのいずれかに格納されます。
When trying to insert an element $A$ into $T_0$, it first attempts to place $A$ at $h_0(A)$; 
要素$A$を$T_0$に挿入しようとすると、最初に$h_0(A)$に$A$を配置しようとします。
If $h_0(A)$ is occupied by another element $B$, it would evict $B$ from $T_0$ and try inserting $B$ into $T_1$ with the same logic. 
もし$h_0(A)$が別の要素$B$によって占有されている場合、$B$を$T_0$から追い出し、同じ論理で$B$を$T_1$に挿入しようとします。
This process will be repeated until all elements stabilize, or rehash happens when insertion runs into a cycle.
このプロセスは、すべての要素が安定するまで繰り返されるか、挿入がサイクルに入ったときに再ハッシュが発生します。
Memory footprint reduction is also an important consideration in our design. 
メモリフットプリントの削減も私たちの設計において重要な考慮事項です。
A naive approach of inserting every new ID into the HashTable will deplete memory quickly. 
新しいIDをすべてHashTableに挿入するという単純なアプローチは、メモリをすぐに消耗させます。
Observation of real production models lead to two conclusions:
実際のプロダクションモデルの観察から2つの結論が得られました：
(1) IDs that appears only a handful of times have limited contribution to improving model quality. 
(1) わずか数回しか現れないIDは、モデルの品質向上に対する貢献が限られています。
An important observation is that IDs are long-tail distributed, where popular IDs may occur millions of times while the unpopular ones appear no more than ten times. 
重要な観察は、IDがロングテール分布していることであり、人気のあるIDは何百万回も現れる一方で、人気のないIDは10回も現れないことです。
Embeddings corresponding to these infrequent IDs are underfit due to lack of training data and the model will not be able to make a good estimation based on them. 
これらの頻度の低いIDに対応する埋め込みは、トレーニングデータが不足しているためにアンダーフィットしており、モデルはそれに基づいて良い推定を行うことができません。
At the end of the day these IDs are not likely to affect the result, so model quality will not suffer from removal of these IDs with low occurrences;
結局、これらのIDは結果に影響を与える可能性が低いため、モデルの品質はこれらの出現頻度の低いIDを削除しても損なわれません。
(2) Stale IDs from a distant history seldom contribute to the current model as many of them are never visited. 
(2) 遠い過去の古いIDは、訪問されることがほとんどないため、現在のモデルに貢献することはほとんどありません。
This could possibly due to a user that is no longer active, or a short video that is out-of-date. 
これは、もはやアクティブでないユーザーや、古くなったショートビデオが原因である可能性があります。
Storing embeddings for these IDs could not help model in any way but to drain our PS memory in vain.
これらのIDの埋め込みを保存することは、モデルに何の助けにもならず、無駄にPSメモリを消耗させるだけです。
Based on these observation, we designed several feature ID filtering heuristics for a more memory-efficient implementation of HashTable:
これらの観察に基づいて、私たちはHashTableのよりメモリ効率の良い実装のためにいくつかの特徴IDフィルタリングヒューリスティックを設計しました：
(1) IDs are filtered before they are admitted into embedding tables. 
(1) IDは埋め込みテーブルに受け入れられる前にフィルタリングされます。
We have two filtering methods: First we filter by their occurrences before they are inserted as keys, where the threshold of occurrences is a tunable hyperparameter that varies for each model; 
私たちは2つのフィルタリング方法を持っています：最初に、キーとして挿入される前に出現回数でフィルタリングし、出現回数のしきい値は各モデルに応じて調整可能なハイパーパラメータです；
In addition we utilize a probabilistic filter which helps further reduce memory usage;  
さらに、メモリ使用量をさらに削減するのに役立つ確率的フィルターを利用します；  
Parameter Parameter
Server Server  
. . .  
Parameter
Server  
Client  
_A_
_h0(A)_
_B A_ _D C_
_h1(D)_ _h1(B)_ _h0(C)_
_E_ _F_ _C B_
**Figure 3: Cuckoo HashMap.**  
Worker Worker  
. . .  
Master  
_T0_
_T1_
0.4. |Col1|Col2|Col3|h0(A)|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12| |---|---|---|---|---|---|---|---|---|---|---|---| |||B A||||||D C|||G| |h1(D) h1(B) h0(C)|||||||||||| |D|||||E||F|||C B||  
-----
ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA Zhuoran, Leqi, Xuan, Caihua, Biao, Da, Bolin, Yijie, Peng, Ke, and Youlong  
Batch Training Data
HDFS  
Training Worker  
Feature Kafka  
Model Server  
Dump Batch Data  
Training PS  
Serving PS  
In Monolith, training is divided into two stages (Figure 1):
Monolithでは、トレーニングは2つのステージに分かれています（図1）：
(1) Batch training stage. 
(1) バッチトレーニングステージ。
This stage works as an ordinary TensorFlow training loop: In each training step, a training worker reads one mini-batch of training examples from the storage, requests parameters from PS, computes a forward and a backward pass, and finally push updated parameters to the training PS. 
このステージは通常のTensorFlowトレーニングループとして機能します：各トレーニングステップで、トレーニングワーカーはストレージから1つのミニバッチのトレーニング例を読み取り、PSからパラメータを要求し、フォワードパスとバックワードパスを計算し、最後に更新されたパラメータをトレーニングPSにプッシュします。
Slightly different from other common deep learning tasks, we only train our dataset for one pass. 
他の一般的な深層学習タスクとは少し異なり、私たちはデータセットを1回のパスでのみトレーニングします。
Batch training is useful for training historical data when we modify our model architecture and retrain the model;
バッチトレーニングは、モデルアーキテクチャを変更し、モデルを再トレーニングする際に、履歴データをトレーニングするのに役立ちます；
(2) Online training stage. 
(2) オンライントレーニングステージ。
After a model is deployed to online serving, the training does not stop but enters the online training stage. 
モデルがオンラインサービングにデプロイされた後、トレーニングは停止せず、オンライントレーニングステージに入ります。
Instead of reading mini-batch examples from the storage, a training worker consumes realtime data on-the-fly and updates the training PS. 
ストレージからミニバッチの例を読み取るのではなく、トレーニングワーカーはリアルタイムデータを即座に消費し、トレーニングPSを更新します。
The training PS periodically synchronizes its parameters to the serving PS, which will take effect on the user side immediately. 
トレーニングPSは定期的にそのパラメータをサービングPSに同期し、これがユーザー側に即座に反映されます。
This enables our model to interactively adapt itself according to a user’s feedback in realtime. 
これにより、私たちのモデルはユーザーのフィードバックに応じてリアルタイムでインタラクティブに適応することができます。  
Batch Training  
_2.2.1_ _Streaming Engine. Monolith is built with the capability of_ seamlessly switching between batch training and online training.
バッチトレーニング  
_2.2.1_ _ストリーミングエンジン。Monolithは、バッチトレーニングとオンライントレーニングの間をシームレスに切り替える能力を備えています。_
This is enabled by our design of streaming engine as illustrated by Figure 4.
これは、図4に示すように、ストリーミングエンジンの設計によって実現されています。
In our design, we use one Kafka [13] queue to log actions of users (E.g. Click on an item or like an item etc.) and another Kafka queue for features. 
私たちの設計では、ユーザーのアクション（例：アイテムをクリックする、アイテムを好むなど）を記録するために1つのKafka [13]キューを使用し、特徴用に別のKafkaキューを使用します。
At the core of the engine is a Flink [4] streaming job for online feature Joiner. 
エンジンの中心には、オンラインフィーチャージョイナーのためのFlink [4]ストリーミングジョブがあります。
The online joiner concatenates features with labels from user actions and produces training examples, which are then written to a Kafka queue. 
オンラインジョイナーは、ユーザーアクションからのラベルと特徴を連結し、トレーニング例を生成し、それをKafkaキューに書き込みます。
The queue for training examples is consumed by both online training and batch training:
トレーニング例のためのキューは、オンライントレーニングとバッチトレーニングの両方によって消費されます：
For online training, the training worker directly reads data from the Kafka queue;
オンライントレーニングの場合、トレーニングワーカーはKafkaキューから直接データを読み取ります；
For batch training, a data dumping job will first dump data to HDFS [18]; 
バッチトレーニングの場合、データダンプジョブは最初にデータをHDFS [18]にダンプします；
After data in HDFS accumulated to certain amount, training worker will retrieve data from HDFS and perform batch training.
HDFSにデータが一定量蓄積された後、トレーニングワーカーはHDFSからデータを取得し、バッチトレーニングを実行します。
Updated parameters in training PS will be pushed to serving PS according to the parameter synchronization schedule.
トレーニングPSの更新されたパラメータは、パラメータ同期スケジュールに従ってサービングPSにプッシュされます。
_2.2.2_ _Online Joiner. In real-world applications, user actions log_ and features are streamed into the online joiner (Figure 5) without guarantee in time order. 
_2.2.2_ _オンラインジョイナー。実世界のアプリケーションでは、ユーザーアクションログ_ と特徴がオンラインジョイナー（図5）に時間順に保証されることなくストリーミングされます。
Therefore we use a unique key for each request so that user action and features could correctly pair up.
したがって、各リクエストに対して一意のキーを使用し、ユーザーアクションと特徴が正しくペアリングされるようにします。
The lag of user action could also be a problem. 
ユーザーアクションの遅延も問題になる可能性があります。
For example, a user may take a few days before they decide to buy an item they were presented days ago. 
例えば、ユーザーは数日前に提示されたアイテムを購入する決定をするまでに数日かかることがあります。
This is a challenge for the joiner because if all features are kept in cache, it would simply not fit in memory.
これはジョイナーにとっての課題です。なぜなら、すべての特徴がキャッシュに保持されている場合、単にメモリに収まらなくなるからです。
In our system, an on-disk key-value storage is utilized to store features that are waiting for over certain time period. 
私たちのシステムでは、一定の時間待機している特徴を保存するために、ディスク上のキー-バリューストレージが利用されます。
When a user action log arrives, it first looks up the in-memory cache, and then looks up the key-value storage in case of a missing cache.  
ユーザーアクションログが到着すると、最初にメモリ内キャッシュを検索し、キャッシュが見つからない場合はキー-バリューストレージを検索します。  
Training Example
Kafka  
0.5. Log Kafka  
-----
Found in Cache
On-disk
KV-Store
Read from KV-Store  
Negative
Sampling  
On-disk
KV-Store  
Join  
Another problem that arise in real-world application is that the distribution of negative and positive examples are highly uneven, where number of the former could be magnitudes of order higher than the latter. 
実世界のアプリケーションで発生する別の問題は、負の例と正の例の分布が非常に不均一であり、前者の数が後者よりも桁違いに多くなる可能性があることです。
To prevent positive examples from being overwhelmed by negative ones, a common strategy is to do negative sampling. 
正の例が負の例に圧倒されないようにするための一般的な戦略は、負のサンプリングを行うことです。
This would certainly change the underlying distribution of the trained model, tweaking it towards higher probability of making positive predictions. 
これは、トレーニングされたモデルの基礎となる分布を確実に変更し、正の予測を行う確率を高める方向に調整します。
As a remedy, we apply log odds correction [19] during serving, making sure that the online model is an unbiased estimator of the original distribution.
その対策として、サービング中にログオッズ補正[19]を適用し、オンラインモデルが元の分布のバイアスのない推定量であることを確認します。
_2.2.3_ _Parameter Synchronization. During online training, the Mono-_ lith training cluster keeps receiving data from the online serving module and updates parameters on the training PS. 
_2.2.3_ _パラメータ同期。オンライントレーニング中、Monolithトレーニングクラスターはオンラインサービングモジュールからデータを受信し続け、トレーニングPSのパラメータを更新します。
A crucial step to enable the online serving PS to benefit from these newly trained parameters is the synchronization of updated model parameters. 
オンラインサービングPSがこれらの新しくトレーニングされたパラメータの恩恵を受けるための重要なステップは、更新されたモデルパラメータの同期です。
In production environment, we are encountered by several challenges:
プロダクション環境では、いくつかの課題に直面します：
Models on the online serving PS must not stop serving when updating. 
オンラインサービングPSのモデルは、更新時にサービスを停止してはなりません。
Our models in production is usually several terabytes in size, and as a result replacing all parameters takes a while
私たちのプロダクションのモデルは通常数テラバイトのサイズであり、その結果、すべてのパラメータを置き換えるのには時間がかかります。



. Our models in production is usually several terabytes in size, and as a result replacing all parameters takes a while. 
私たちの本番環境でのモデルは通常数テラバイトのサイズであり、その結果、すべてのパラメータを置き換えるのには時間がかかります。

It would be intolerable to stop an online PS from serving the model during the replacement process, and updates must be made on-the-fly; 
置き換えプロセス中にオンラインPSがモデルの提供を停止することは耐えられず、更新はリアルタイムで行う必要があります。

Transferring a multi-terabyte model of its entirety from training PS to the online serving PS would pose huge pressure to both the network bandwidth and memory on PS, 
トレーニングPSからオンラインサービングPSにマルチテラバイトのモデル全体を転送することは、ネットワーク帯域幅とPSのメモリの両方に大きな負担をかけるでしょう、

since it requires doubled model size of memory to accept the newly arriving model. 
新しく到着するモデルを受け入れるためには、メモリのモデルサイズが2倍必要になるからです。

For the online training to scale up to the size of our business scenario, we designed an incremental on-the-fly periodic parameter synchronization mechanism in Monolith based on several noticeable characteristic of our models:  
私たちのビジネスシナリオのサイズに合わせてオンライントレーニングを拡張するために、私たちはMonolithにおいて、モデルのいくつかの顕著な特性に基づいたインクリメンタルなリアルタイムの定期パラメータ同期メカニズムを設計しました：

Training Example
トレーニング例

Kafka  
Kafka  

(1) Sparse parameters are dominating the size of recommendation models; 
(1) スパースパラメータが推薦モデルのサイズを支配しています；

(2) Given a short range of time window, only a small subset of IDs gets trained and their embeddings updated; 
(2) 短い時間ウィンドウを考慮すると、トレーニングされるのはごく少数のIDのみであり、それらの埋め込みが更新されます；

(3) Dense variables move much slower than sparse embeddings. 
(3) 密な変数はスパース埋め込みよりもはるかに遅く動きます。

This is because in momentum-based optimizers, the accumulation of momentum for dense variables is magnified by the gigantic size of recommendation training data, 
これは、モメンタムベースの最適化手法では、密な変数のモメンタムの蓄積が巨大な推薦トレーニングデータのサイズによって増幅されるためです、

while only a few sparse embeddings receives updates in a single data batch. 
一方で、単一のデータバッチではごく少数のスパース埋め込みのみが更新されます。

(1) and (2) allows us to exploit the sparse updates across all feature IDs. 
(1) と (2) により、すべての特徴IDにわたるスパース更新を活用することができます。

In Monolith, we maintain a hash set of touched keys, representing IDs whose embeddings get trained since the last parameter synchronization. 
Monolithでは、最後のパラメータ同期以降にトレーニングされた埋め込みを持つIDを表すタッチされたキーのハッシュセットを維持します。

We push the subset of sparse parameters whose keys are in the touched-keys set with a minute-level time interval from the training PS to the online serving PS. 
タッチされたキーセットにあるキーを持つスパースパラメータのサブセットを、トレーニングPSからオンラインサービングPSに対して分単位の時間間隔でプッシュします。

This relatively small pack of incremental parameter update is lightweight for network transmission and will not cause a sharp memory spike during the synchronization. 
この比較的小さなインクリメンタルパラメータ更新パックはネットワーク伝送に対して軽量であり、同期中に急激なメモリスパイクを引き起こすことはありません。

We also exploit (3) to further reduce network I/O and memory usage by setting a more aggressive sync schedule for sparse parameters, 
私たちはまた、スパースパラメータのためにより攻撃的な同期スケジュールを設定することにより、ネットワークI/Oとメモリ使用量をさらに削減します、

while updating dense parameters less frequently. 
一方で、密なパラメータの更新頻度は低くします。

This could render us a situation where the dense parameters we serve is a relatively stale version compared to sparse part. 
これにより、私たちが提供する密なパラメータがスパース部分に比べて比較的古いバージョンになる可能性があります。

However, such inconsistency could be tolerated due to the reason mentioned in (3) as no conspicuous loss has been observed. 
しかし、そのような不整合は、(3)で述べた理由により許容される可能性があります。なぜなら、顕著な損失は観察されていないからです。

#### 0.5.0.1. 2.3 Fault Tolerance
#### 0.5.0.2. 2.3 フォールトトレランス

As a system in production, Monolith is designed with the ability to recover a PS in case it fails. 
本番環境のシステムとして、MonolithはPSが失敗した場合に回復する能力を持つように設計されています。

A common choice for fault tolerance is to snapshot the state of a model periodically, and recover from the latest snapshot when PS failure is detected. 
フォールトトレランスの一般的な選択肢は、モデルの状態を定期的にスナップショットし、PSの障害が検出されたときに最新のスナップショットから回復することです。

The choice of snapshot frequency has two major impacts: 
スナップショットの頻度の選択には2つの主要な影響があります：

(1) Model quality. 
(1) モデルの品質。

Intuitively, model quality suffers less from loss of recent history with increased snapshot frequency. 
直感的に、スナップショットの頻度が増すことで最近の履歴の喪失によるモデルの品質への影響は少なくなります。

(2) Computation overhead. 
(2) 計算オーバーヘッド。

Snapshotting a multi-terabyte model is not free. 
マルチテラバイトのモデルのスナップショットは無料ではありません。

It incurs large chunks of memory copy and disk I/O. 
それは大きなメモリコピーとディスクI/Oを伴います。

As a trade-off between model quality and computation overhead, Monolith snapshots all training PS every day. 
モデルの品質と計算オーバーヘッドのトレードオフとして、MonolithはすべてのトレーニングPSのスナップショットを毎日取得します。

Though a PS will lose one day’s worth of update in case of a failure, we discover that the performance degradation is tolerable through our experiments. 
PSが障害が発生した場合、1日の更新を失うことになりますが、私たちの実験を通じてパフォーマンスの低下は許容できることがわかりました。

We will analyze the effect of PS reliability in the next section. 
次のセクションでは、PSの信頼性の影響を分析します。

Output
出力

MLP
MLP

FM
FM

#### 0.5.0.3. . . .
#### 0.5.0.4. . . .

Embeddings
埋め込み

IDs . . .
ID . . .

**Figure 6: DeepFM model architecture.**
**図6: DeepFMモデルアーキテクチャ。**

#### 0.5.0.5. 3 EVALUATION
#### 0.5.0.6. 3 評価

For a better understanding of benefits and trade-offs brought about by our proposed design, we conducted several experiments at production scale and A/B test with live serving traffic to evaluate and verify Monolith from different aspects. 
私たちの提案した設計によってもたらされる利点とトレードオフをよりよく理解するために、私たちは本番規模でいくつかの実験を行い、ライブサービングトラフィックを用いたA/Bテストを実施して、Monolithをさまざまな側面から評価し検証しました。

We aim to answer the following questions by our experiments: 
私たちの実験では、以下の質問に答えることを目指しています：

(1) How much can we benefit from a collisionless HashTable? 
(1) 衝突のないハッシュテーブルからどれだけの利益を得ることができるか？

(2) How important is realtime online training? 
(2) リアルタイムのオンライントレーニングはどれほど重要か？

(3) Is Monolith’s design of parameter synchronization robust enough in a large-scale production scenario? 
(3) Monolithのパラメータ同期の設計は、大規模な生産シナリオで十分に堅牢か？

In this section, we first present our experimental settings and then discuss results and our findings in detail. 
このセクションでは、まず実験設定を提示し、その後結果と私たちの発見について詳しく議論します。

#### 0.5.0.7. 3.1 Experimental Setup
#### 0.5.0.8. 3.1 実験設定

_3.1.1_ _Embedding Table. As described in Section 2.1, embedding_ tables in Monolith are implemented as collisionless HashTables. 
_3.1.1_ _埋め込みテーブル。セクション2.1で説明したように、Monolithの埋め込みテーブルは衝突のないハッシュテーブルとして実装されています。

To prove the necessity of avoiding collisions in embedding tables and to quantify gains from our collisionless implementation, we performed two groups of experiments on the Movielens dataset and on our internal production dataset respectively: 
埋め込みテーブルでの衝突を避ける必要性を証明し、衝突のない実装からの利益を定量化するために、私たちはMovielensデータセットと内部の生産データセットでそれぞれ2つのグループの実験を行いました：

(1) MovieLens ml-25m dataset [11]. 
(1) MovieLens ml-25mデータセット[11]。

This is a standard public dataset for movie ratings, containing 25 million ratings that involves approximately 162000 users and 62000 movies. 
これは映画の評価のための標準的な公開データセットであり、約162,000人のユーザーと62,000本の映画を含む2500万件の評価が含まれています。

- Preprocessing of labels. 
- ラベルの前処理。

The original labels are ratings from 0.5 to 5.0, while in production our tasks are mostly receiving binary signals from users. 
元のラベルは0.5から5.0の評価ですが、本番環境では私たちのタスクは主にユーザーからのバイナリ信号を受け取ることです。

To better simulate our production models, we convert scale labels to binary labels  
私たちの生産モデルをよりよくシミュレートするために、スケールラベルをバイナリラベルに変換します。

by treating scores ≥ 3.5 as positive samples and the rest as negative samples. 
スコアが≥ 3.5のものを正のサンプルとし、残りを負のサンプルとします。

- Model and metrics. 
- モデルとメトリクス。

We implemented a standard DeepFM 
私たちは標準的なDeepFMを実装しました。

[9] model, a commonly used model architecture for recommendation problems. 
[9] モデルで、推薦問題に一般的に使用されるモデルアーキテクチャです。

It consist of an FM component and a dense component (Figure 6). 
それはFMコンポーネントと密なコンポーネント（図6）で構成されています。

Predictions are evaluated by AUC [2] as this is the major measurement for real models. 
予測はAUC [2]によって評価されます。これは実際のモデルの主要な測定基準です。

- Embedding collisions. 
- 埋め込みの衝突。

This dataset contains approximately 160K user IDs and 60K movie IDs. 
このデータセットには約160KのユーザーIDと60Kの映画IDが含まれています。

To compare with the collisionless version of embedding table implementation, we performed another group of experiment where IDs are preprocessed with MD5 hashing and then mapped to a smaller ID space. 
衝突のない埋め込みテーブル実装と比較するために、IDがMD5ハッシュ化され、その後小さなID空間にマッピングされる別のグループの実験を行いました。

As a result, some IDs will share their embedding with others. 
その結果、一部のIDは他のIDと埋め込みを共有します。

Table 1 shows detailed statistics of user and movie IDs before and after hashing. 
表1は、ハッシュ化前後のユーザーIDと映画IDの詳細な統計を示しています。

**User IDs** **Movie IDs** 
**ユーザーID** **映画ID**

# 1. Before Hashing 162541 59047 
# 2. ハッシュ化前 162541 59047 

# 3. After Hashing 149970 57361 
# 4. ハッシュ化後 149970 57361 

Collision rate 7.73% 2.86% 
衝突率 7.73% 2.86%

**Table 1: Statistics of IDs Before and After Hashing.** 
**表1: ハッシュ化前後のIDの統計。**

(2) Internal Recommendation dataset. 
(2) 内部推薦データセット。

We also performed experiments on a recommendation model in production environment. 
私たちはまた、本番環境での推薦モデルに関する実験を行いました。

This model generally follows a multi-tower architecture, with each tower responsible for learning to predict a specialized kind of user behavior. 
このモデルは一般的にマルチタワーアーキテクチャに従い、各タワーは特定の種類のユーザー行動を予測するための学習を担当します。

Each model has around 1000 embedding tables, and distribution of size of embedding tables are very uneven; 
各モデルには約1000の埋め込みテーブルがあり、埋め込みテーブルのサイズの分布は非常に不均一です；

- The original ID space of embedding table was 2[48]. 
- 埋め込みテーブルの元のID空間は2[48]でした。

In our baseline, we applied a hashing trick by decomposing to curb the size of embedding table. 
私たちのベースラインでは、埋め込みテーブルのサイズを抑えるために分解によるハッシングトリックを適用しました。

To be more specific, we use two smaller embedding tables instead of a gigantic one to generate a unique embedding for each ID by vector combination: 
より具体的には、巨大な1つの埋め込みテーブルの代わりに2つの小さな埋め込みテーブルを使用して、ベクトルの組み合わせによって各IDのユニークな埋め込みを生成します：

_𝐼𝐷𝑟_ = 𝐼𝐷 % 2[24] 
_𝐼𝐷𝑞_ = 𝐼𝐷 ÷ 2[24] 
_𝐸_ = 𝐸𝑟 + 𝐸𝑞, 
ここで、𝐸𝑟_, 𝐸𝑞_は𝐼𝐷𝑟_, 𝐼𝐷𝑞_に対応する埋め込みです。これにより、埋め込みテーブルのサイズが2[48]から2[25]に効果的に削減されます。

This model is serving in real production, and the performance of this experiment is measured by online AUC with real serving traffic. 
このモデルは実際の生産環境で提供されており、この実験のパフォーマンスは実際のサービングトラフィックを用いたオンラインAUCで測定されます。

_3.1.2_ _Online Training. During online training, we update our on-_ line serving PS with the latest set of parameters with minute-level intervals. 
_3.1.2_ _オンライントレーニング。オンライントレーニング中、私たちは最新のパラメータセットでオンラインサービングPSを分単位の間隔で更新します。

We designed two groups of experiments to verify model quality and system robustness. 
モデルの品質とシステムの堅牢性を検証するために、2つのグループの実験を設計しました。

(1) Update frequency. 
(1) 更新頻度。

To investigate the necessity of minute-level update frequency, we conducted experiments that synchronize parameters from training model to prediction model with different intervals. 
分単位の更新頻度の必要性を調査するために、トレーニングモデルから予測モデルにパラメータを異なる間隔で同期させる実験を行いました。

#### 4.0.0.1. . . .  
#### 4.0.0.2. . . .  

-----
Monolith: Real Time Recommendation System With Collisionless Embedding Table 
Monolith: 衝突のない埋め込みテーブルを用いたリアルタイム推薦システム

ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA 
ORSUM@ACM RecSys 2022, 2022年9月23日、シアトル、ワシントン州、アメリカ

**Algorithm 1 Simulated Online Training.** 
**アルゴリズム1 シミュレートされたオンライントレーニング。**

1: Input: 𝐷[𝑏𝑎𝑡𝑐ℎ] ; /* Data for batch training. */ 
1: 入力: 𝐷[𝑏𝑎𝑡𝑐ℎ] ; /* バッチトレーニング用のデータ。 */

2: Input: 𝐷𝑖[𝑜𝑛𝑙𝑖𝑛𝑒]=1···𝑁 [;] /* Data for online training, split into 𝑁 shards. */ 
2: 入力: 𝐷𝑖[𝑜𝑛𝑙𝑖𝑛𝑒]=1···𝑁 [;] /* オンライントレーニング用のデータ、𝑁のシャードに分割。 */

3: 𝜃𝑡𝑟𝑎𝑖𝑛 ← _𝑇𝑟𝑎𝑖𝑛(𝐷[𝑏𝑎𝑡𝑐ℎ],𝜃𝑡𝑟𝑎𝑖𝑛) ;_ /* Batch training. */ 
3: 𝜃𝑡𝑟𝑎𝑖𝑛 ← _𝑇𝑟𝑎𝑖𝑛(𝐷[𝑏𝑎𝑡𝑐ℎ],𝜃𝑡𝑟𝑎𝑖𝑛) ;_ /* バッチトレーニング。 */

4: for 𝑖 = 1 · · · 𝑁 **do** 
4: for 𝑖 = 1 · · · 𝑁 **する** 

5: _𝜃𝑠𝑒𝑟𝑣𝑒_ ← _𝜃𝑡𝑟𝑎𝑖𝑛_ ; /* Sync training parameters to serving model. */ 
5: _𝜃𝑠𝑒𝑟𝑣𝑒_ ← _𝜃𝑡𝑟𝑎𝑖𝑛_ ; /* トレーニングパラメータをサービングモデルに同期。 */

6: _𝐴𝑈𝐶𝑖_ = Evaluate(𝜃𝑠𝑒𝑟𝑣𝑒, 𝐷𝑖[𝑜𝑛𝑙𝑖𝑛𝑒] ) ; /* Evaluate online prediction on new data. */ 
6: _𝐴𝑈𝐶𝑖_ = Evaluate(𝜃𝑠𝑒𝑟𝑣𝑒, 𝐷𝑖[𝑜𝑛𝑙𝑖𝑛𝑒] ) ; /* 新しいデータに対するオンライン予測を評価。 */

7: _𝜃𝑡𝑟𝑎𝑖𝑛_ ← _𝑇𝑟𝑎𝑖𝑛(𝐷𝑖[𝑜𝑛𝑙𝑖𝑛𝑒],𝜃𝑡𝑟𝑎𝑖𝑛) ;_ /* Train with new data. */ 
7: _𝜃𝑡𝑟𝑎𝑖𝑛_ ← _𝑇𝑟𝑎𝑖𝑛(𝐷𝑖[𝑜𝑛𝑙𝑖𝑛𝑒],𝜃𝑡𝑟𝑎𝑖𝑛) ;_ /* 新しいデータでトレーニング。 */

8: end for  
8: 終了  

The dataset we use is the Criteo Display Ads Challenge dataset[3], a large-scale standard dataset for benchmarking CTR models. 
私たちが使用するデータセットはCriteo Display Ads Challengeデータセット[3]で、CTRモデルのベンチマーク用の大規模な標準データセットです。

It contains 7 days of chronologically ordered data recording features and click actions. 
それは特徴とクリックアクションを記録した7日間の時系列データを含んでいます。

For this experiment, we use a standard DeepFM [9] model as described in 6. 
この実験では、6で説明されている標準的なDeepFM [9]モデルを使用します。

To simulate online training, we did the following preprocessing for the dataset. 
オンライントレーニングをシミュレートするために、データセットに対して以下の前処理を行いました。

We take 7 days of data from the dataset, and split it to two parts: 5 days of data for batch training, and 2 days for online training. 
データセットから7日間のデータを取り出し、バッチトレーニング用の5日間のデータとオンライントレーニング用の2日間のデータに分割します。

We further split the 2 days of data into 𝑁 shards chronologically. 
さらに、2日間のデータを時系列で𝑁のシャードに分割します。

Online training is simulated by algorithm 1. 
オンライントレーニングはアルゴリズム1によってシミュレートされます。

As such, we simulate synchronizing trained parameters to online serving PS with an interval determined by number of data shards. 
このようにして、トレーニングされたパラメータをオンラインサービングPSに同期させることを、データシャードの数によって決定される間隔でシミュレートします。

We experimented with 𝑁 = 10, 50, 100, which roughly correspond to update interval of 5ℎ𝑟, 1ℎ𝑟, and 30𝑚𝑖𝑛. 
私たちは𝑁 = 10, 50, 100で実験を行い、これはおおよそ5時間、1時間、30分の更新間隔に対応します。

(2) Live experiment. 
(2) ライブ実験。

In addition, we also performed a live experiment with real serving traffic to further demonstrate the importance of online training in real-world application. 
さらに、私たちは実際のサービングトラフィックを用いたライブ実験も行い、実世界のアプリケーションにおけるオンライントレーニングの重要性をさらに示しました。

This A/B experiment compares online training to batch training one one of our Ads model in production. 
このA/B実験は、オンライントレーニングとバッチトレーニングを本番環境の広告モデルの1つで比較します。

#### 4.0.0.3. 3.2 Results and Analysis
#### 4.0.0.4. 3.2 結果と分析

_3.2.1_ _The Effect of Embedding Collision. Results from MovieLens_ dataset and the Internal recommedation dataset both show that embedding collisions will jeopardize model quality. 
_3.2.1_ _埋め込み衝突の影響。MovieLensデータセットと内部推薦データセットの結果は、埋め込み衝突がモデルの品質を危うくすることを示しています。

(1) Models with collisionless HashTable consistently outperforms those with collision. 
(1) 衝突のないハッシュテーブルを持つモデルは、常に衝突のあるモデルを上回ります。

This conclusion holds true regardless of Increase of number of training epochs. 
この結論は、トレーニングエポックの数の増加に関係なく成り立ちます。

As shown in Figure 7, the model with collisionless embedding table has higher AUC from the first epoch and converges at higher value; 
図7に示すように、衝突のない埋め込みテーブルを持つモデルは、最初のエポックからより高いAUCを持ち、より高い値に収束します；

Change of distribution with passage of time due to Con cept Drift. 
時間の経過による分布の変化は概念ドリフトによるものです。

As shown in Figure 8, models with collisionless embedding table is also robust as time passes by and users/items context changes. 
図8に示すように、衝突のない埋め込みテーブルを持つモデルは、時間が経つにつれてユーザーやアイテムのコンテキストが変化しても堅牢です。

(2) Data sparsity caused by collisionless embedding table will not lead to model overfitting 
(2) 衝突のない埋め込みテーブルによって引き起こされるデータのスパース性は、モデルの過剰適合を引き起こすことはありません。



As shown in Figure 7, a model with collisionless embedding table does not overfit after it converges.
図7に示すように、衝突のない埋め込みテーブルを持つモデルは、収束した後に過学習しません。

**Figure 7: Effect of Embedding Collision On DeepFM,** **MovieLens**
**図7: DeepFMおよびMovieLensにおける埋め込み衝突の影響**

0.790 hash w/ collision
衝突のあるハッシュ

collisionless hash table
衝突のないハッシュテーブル

0.785
0.780
0.775
0.770
2 4 6 8 10 12
Day
日

**Figure 8: Effect of Embedding Collision On A** **Recommendation Model In Production**
**図8: 実運用における推薦モデルにおける埋め込み衝突の影響**

_We measure performance of this recommendation model by online serving AUC,_ _which is fluctuating across different days due to concept-drift._
_この推薦モデルの性能はオンラインサービングAUCによって測定され、概念の漂流により異なる日で変動します。_

-----
ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA Zhuoran, Leqi, Xuan, Caihua, Biao, Da, Bolin, Yijie, Peng, Ke, and Youlong  
**(a) Online training with 5 hrs sync interval**  
**(b) Online training with 1 hr sync interval**  
**(c) Online training with 30 min sync interval**

**Figure 9: Online training v.s. Batch training on Criteo dataset.**
**図9: Criteoデータセットにおけるオンライン学習とバッチ学習の比較。**

_Blue lines: AUC of models with online training; Yellow lines: AUC of batch training models evaluated against streaming data._
_青い線: オンライン学習モデルのAUC; 黄色い線: ストリーミングデータに対して評価されたバッチ学習モデルのAUC。_

_3.2.2_ _Online Training: Trading-off Reliability For Realtime. We dis-_ 
_3.2.2 オンライン学習: リアルタイムのための信頼性のトレードオフ。私たちは発見しました_

covered that a higher parameter synchronization frequency is always conducive to improving online serving AUC, and that online serving models are more tolerant with loss of a few shard of PS than we expect.
より高いパラメータ同期頻度は常にオンラインサービングAUCの改善に寄与し、オンラインサービングモデルは予想以上にPSの一部の損失に対して寛容であることがわかりました。

(1) The Effect of Parameter Synchronization Frequency.
(1) パラメータ同期頻度の影響。

In our online streaming training experiment (1) with Criteo Display Ads Challenge dataset, model quality consistently improves with the increase of parameter synchronization frequency, as is evident by comparison from two perspectives: 
Criteo Display Ads Challengeデータセットを用いたオンラインストリーミング学習実験(1)では、モデルの品質はパラメータ同期頻度の増加に伴って一貫して改善され、2つの視点からの比較によって明らかです。

Models with online training performs better than models without.
オンライン学習を行ったモデルは、行っていないモデルよりも性能が良いです。

Figure 9a, 9b, 9c compares AUC of online training models evaluated by the following shard of data versus batch training models evaluated by each shard of data;  
図9a、9b、9cは、次のデータのシャードによって評価されたオンライン学習モデルのAUCと、各データのシャードによって評価されたバッチ学習モデルのAUCを比較します。

Models with smaller parameter synchronization interval performs better that those with larger interval.
パラメータ同期間隔が小さいモデルは、大きい間隔のモデルよりも性能が良いです。

Figure 10 and Table 2 compares online serving AUC for models with sync interval of 5ℎ𝑟, 1ℎ𝑟, and 30𝑚𝑖𝑛 respectively.
図10および表2は、同期間隔が5時間、1時間、30分のモデルのオンラインサービングAUCを比較します。

**Sync Interval** **Average AUC (online)** **Average AUC (batch)**
**同期間隔** **平均AUC (オンライン)** **平均AUC (バッチ)**

5 hr 79.66 ± 0.020 79.42 ± 0.026  
1 hr 79.78 ± 0.005 79.44 ± 0.030  
30 min 79.80 ± 0.008 79.43 ± 0.025  

**Table 2: Average AUC comparison for DeepFM model on** **Criteo dataset.**
**表2: CriteoデータセットにおけるDeepFMモデルの平均AUC比較。**

-----
Monolith: Real Time Recommendation System With Collisionless Embedding Table ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA  
**Day** 1 2 3 4 5 6 7  
**AUC Improvement %** 14.443 16.871 17.068 14.028 18.081 16.404 15.202  
**Table 3: Improvement of Online Training Over Batch Training from Live A/B Experiment on an Ads Model.**
**表3: 広告モデルにおけるオンライン学習のバッチ学習に対する改善。**

model quality. We also did quite some exploration in this regard and to our surprise, model quality is more robust than expected.
モデルの品質についてもかなりの探求を行い、驚いたことに、モデルの品質は予想以上に堅牢です。

With a 0.01% failure rate of PS machine per day, 
1日のPSマシンの故障率が0.01%の場合、

we find a model from the previous day works embarrassingly well.
前日のモデルが驚くほどうまく機能することがわかります。

This is explicable by the following calculation: 
これは以下の計算によって説明できます。

Suppose a model’s parameters are sharded across 1000 PS, and they snapshot every day.
モデルのパラメータが1000のPSに分割され、毎日スナップショットを取得すると仮定します。

Given 0.01% failure rate, one of them will go down every 10 days and we lose all updates on this PS for 1 day.
0.01%の故障率を考えると、10日ごとに1つのPSがダウンし、そのPSのすべての更新が1日失われます。

Assuming a DAU of 15 Million and an even distribution of user IDs on each PS, we lose 1 day’s feedback from 15000 users every 10 days.
DAUが1500万で、各PSにユーザーIDが均等に分配されていると仮定すると、10日ごとに15000ユーザーから1日のフィードバックを失います。

This is acceptable because 
これは受け入れ可能です。

(a) For sparse features which is user-specific, this is equiv 0.790 equivalent to losing a tiny fraction of 0.01% DAU; 
(a) ユーザー固有のスパース特徴に関しては、これは0.01%のDAUのわずかな部分を失うことに相当します。

(b) For dense variables, since they are updated slowly as we discussed in 2.2.3, losing 1 day’s update out of 1000 PS is negligible.
(b) 密な変数については、2.2.3で議論したように、更新が遅いため、1000のPSのうち1日の更新を失うことは無視できます。

Based on the above observation and calculation, we radically lowered our snapshot frequency and thereby saved quite a bit in computation overhead.
上記の観察と計算に基づいて、私たちはスナップショットの頻度を大幅に下げ、計算オーバーヘッドをかなり節約しました。

**Figure 10: Comparison of different sync intervals for** **online training.**
**図10: オンライン学習のための異なる同期間隔の比較。**

The live A/B experiment between online training and batch training on an Ads model in production also show that there is a significant bump in online serving AUC (Table 3).
実運用の広告モデルにおけるオンライン学習とバッチ学習のライブA/B実験でも、オンラインサービングAUCに大きな向上が見られました（表3）。

Inspired by this observation, we synchronize sparse parameters to serving PS of our production models as frequent as possible (currently at minute-level), to the extent that the computation overhead and system reliability could endure.
この観察に触発されて、私たちはスパースパラメータを可能な限り頻繁に（現在は分単位で）実運用モデルのサービングPSに同期させ、計算オーバーヘッドとシステムの信頼性が耐えられる範囲で行います。

Recall that dense variables requires a less frequent update as discussed in 2.2.3, we update them at day-level.
密な変数は2.2.3で議論したように、更新頻度が低くて済むため、日単位で更新します。

By doing so, we can bring down our computation overhead to a very low level.
こうすることで、計算オーバーヘッドを非常に低いレベルに抑えることができます。

Suppose 100,000 IDs gets updated in a minute, and the dimension of embedding is 1024, the total size of data need to be transferred is 4𝐾𝐵 × 100, 000 ≈ 400𝑀𝐵 per minute.
10万のIDが1分で更新され、埋め込みの次元が1024の場合、転送する必要があるデータの総サイズは$4KB \times 100,000 \approx 400MB$です。

For dense parameters, since they are synchronized daily, we choose to schedule the synchronization when the traffic is lowest (e.g. midnight).
密なパラメータについては、日次で同期されるため、トラフィックが最も少ない時間（例: 真夜中）に同期をスケジュールすることを選択します。

(2) The Effect of PS reliability.
(2) PSの信頼性の影響。

With a minute-level parameter synchronization, we initially expect a more frequent snapshot of training PS to match the realtime update.
分単位のパラメータ同期により、リアルタイムの更新に合わせてトレーニングPSのスナップショットをより頻繁に取得することを期待していました。

To our surprise, we enlarged the snapshot interval to 1 day and still observed nearly no loss of model quality.
驚いたことに、スナップショットの間隔を1日に拡大しても、モデルの品質にほとんど損失がないことが観察されました。

Finding the right trade-off between model quality and computation overhead is difficult for personalized ranking systems since users are extremely sensitive on recommendation quality.
モデルの品質と計算オーバーヘッドの間の適切なトレードオフを見つけることは、ユーザーが推薦の品質に非常に敏感であるため、パーソナライズされたランキングシステムにとって難しいです。

Traditionally, large-scale systems tend to set a frequent snapshot schedule for their models, which sacrifices computation resources in exchange for minimized loss in 
従来、大規模システムはモデルのために頻繁なスナップショットスケジュールを設定する傾向があり、計算リソースを犠牲にして損失を最小限に抑えます。

#### 4.0.0.5. 4 RELATED WORK
#### 4.0.0.6. 4 関連研究

Ever since some earliest successful application of deep learning to industry-level recommendation systems [6, 10], researchers and engineers have been employing various techniques to ameliorate issues mentioned in Section 1.
深層学習が産業レベルの推薦システムに成功裏に適用されて以来[6, 10]、研究者やエンジニアはセクション1で言及された問題を改善するためにさまざまな技術を採用してきました。

To tackle the issue of sparse feature representation, [3, 6] uses fixed-size embedding table with hash-trick.
スパース特徴表現の問題に対処するために、[3, 6]はハッシュトリックを用いた固定サイズの埋め込みテーブルを使用しています。

There are also attempts in improving hashing to reduce collision [3, 7].
衝突を減らすためにハッシュを改善する試みもあります[3, 7]。

Other works directly utilize native key-value hash table to allow dynamic growth of table size [12, 15, 20, 21].
他の研究では、ネイティブのキー-バリューハッシュテーブルを直接利用してテーブルサイズの動的成長を可能にしています[12, 15, 20, 21]。

These implementations builds upon TensorFlow but relies either on specially designed software mechanism [14, 15, 20] or hardware [21] to access and manage their hash-tables.
これらの実装はTensorFlowに基づいていますが、ハッシュテーブルにアクセスし管理するために特別に設計されたソフトウェアメカニズム[14, 15, 20]またはハードウェア[21]に依存しています。

Compared to these solutions, Monolith’s hash-table is yet another native TensorFlow operation.
これらの解決策と比較して、Monolithのハッシュテーブルは別のネイティブTensorFlow操作です。

It is developer friendly and has higher cross-platform interoperability, which is suitable for ToB scenarios.
開発者に優しく、より高いクロスプラットフォームの相互運用性を持ち、ToBシナリオに適しています。

An organic and tight integration with TensorFlow also enables easier optimizations of computation performance.
TensorFlowとの有機的で緊密な統合は、計算性能の最適化を容易にします。

Bridging the gap between training and serving and alleviation of Concept Drift [8] is another topic of interest.
トレーニングとサービングのギャップを埋め、概念の漂流を軽減すること[8]は、もう一つの関心のあるトピックです。

To support online update and avoid memory issues, both [12] and [20] designed feature eviction mechanisms to flexibly adjust the size of embedding tables.
オンライン更新をサポートし、メモリの問題を回避するために、[12]と[20]は埋め込みテーブルのサイズを柔軟に調整するための特徴排除メカニズムを設計しました。

Both [12] and [14] support some form of online training, where learned parameters are synced to serving with a relatively short interval compared to traditional batch training, with fault tolerance mechanisms.
[12]と[14]の両方は、学習したパラメータが従来のバッチ学習と比較して比較的短い間隔でサービングに同期されるオンライン学習のいくつかの形式をサポートしており、フォールトトレランスメカニズムを備えています。

Monolith took similar approach to elastically admit and evict features, while it has a more lightweight parameter synchronization mechanism to guarantee model quality.
Monolithは、特徴を弾力的に受け入れ排除するために同様のアプローチを取りましたが、モデルの品質を保証するためにより軽量なパラメータ同期メカニズムを持っています。

-----
ORSUM@ACM RecSys 2022, September 23rd, 2022, Seattle, WA, USA Zhuoran, Leqi, Xuan, Caihua, Biao, Da, Bolin, Yijie, Peng, Ke, and Youlong  
#### 4.0.0.7. 5 CONCLUSION
#### 4.0.0.8. 5 結論

In this work, we reviewed several most important challenges for industrial-level recommendation systems and present our system in production, Monolith, to address them and achieved best performance compared to existing solutions.
本研究では、産業レベルの推薦システムにおけるいくつかの最も重要な課題をレビューし、それに対処するために実運用中のシステムMonolithを提示し、既存のソリューションと比較して最良のパフォーマンスを達成しました。

We proved that a collisionless embedding table is essential for model quality, and demonstrated that our implementation of Cuckoo HashMap based embedding table is both memory efficient and helpful for improving online serving metrics.
衝突のない埋め込みテーブルがモデルの品質に不可欠であることを証明し、Cuckoo HashMapに基づく埋め込みテーブルの実装がメモリ効率が良く、オンラインサービングメトリクスの改善に役立つことを示しました。

We also proved that realtime serving is crucial in recommendation systems, and that parameter synchronization interval should be as short as possible for an ultimate model performance.
リアルタイムサービングが推薦システムにおいて重要であり、パラメータ同期間隔は最終的なモデル性能のためにできるだけ短くするべきであることも証明しました。

Our solution for online realtime serving in Monolith has a delicately designed parameter synchronization and a fault tolerance mechanism: 
Monolithにおけるオンラインリアルタイムサービングのための私たちのソリューションは、精巧に設計されたパラメータ同期とフォールトトレランスメカニズムを持っています。

In our parameter synchronization algorithm, we showed that consistency of version across different parts of parameters could be traded-off for reducing network bandwidth consumption; 
私たちのパラメータ同期アルゴリズムでは、パラメータの異なる部分間でのバージョンの一貫性がネットワーク帯域幅の消費を削減するためにトレードオフできることを示しました。

In fault tolerance design, we demonstrated that our strategy of trading-off PS reliability for realtime-ness is a robust solution.
フォールトトレランス設計において、リアルタイム性のためにPSの信頼性をトレードオフする私たちの戦略が堅牢な解決策であることを示しました。

To conclude, Monolith succeeded in providing a general solution for production scale recommendation systems.
結論として、Monolithは生産規模の推薦システムに対する一般的な解決策を提供することに成功しました。

#### 4.0.0.9. ACKNOWLEDGMENTS
#### 4.0.0.10. 謝辞

Hanzhi Zhou provided useful suggestions on revision of this paper.
Hanzhi Zhouはこの論文の改訂に関して有用な提案を提供しました。

#### 4.0.0.11. REFERENCES
#### 4.0.0.12. 参考文献

[1] Martín Abadi, Paul Barham, Jianmin Chen, Z. Chen, Andy Davis, Jeffrey Dean, Matthieu Devin, Sanjay Ghemawat, Geoffrey Irving, Michael Isard, Manjunath Kudlur, Josh Levenberg, Rajat Monga, Sherry Moore, Derek Gordon Murray, Benoit Steiner, Paul A. Tucker, Vijay Vasudevan, Pete Warden, Martin Wicke, Yuan Yu, and Xiaoqiang Zhang. 2016. TensorFlow: A system for large-scale machine learning. ArXiv abs/1605.08695 (2016).
[1] Martín Abadi, Paul Barham, Jianmin Chen, Z. Chen, Andy Davis, Jeffrey Dean, Matthieu Devin, Sanjay Ghemawat, Geoffrey Irving, Michael Isard, Manjunath Kudlur, Josh Levenberg, Rajat Monga, Sherry Moore, Derek Gordon Murray, Benoit Steiner, Paul A. Tucker, Vijay Vasudevan, Pete Warden, Martin Wicke, Yuan Yu, and Xiaoqiang Zhang. 2016. TensorFlow: 大規模機械学習のためのシステム。ArXiv abs/1605.08695 (2016)。

[2] Andrew P. Bradley. 1997. The use of the area under the ROC curve in the evaluation of machine learning algorithms. Pattern Recognit. 30 (1997), 1145– 1159.
[2] Andrew P. Bradley. 1997. 機械学習アルゴリズムの評価におけるROC曲線の下の面積の使用。パターン認識。30 (1997), 1145–1159。

[3] Thomas Bredillet. 2019. Core modeling at Instagram. [https://instagram-](https://instagram-engineering.com/core-modeling-at-instagram-a51e0158aa48) [engineering.com/core-modeling-at-instagram-a51e0158aa48](https://instagram-engineering.com/core-modeling-at-instagram-a51e0158aa48)
[3] Thomas Bredillet. 2019. Instagramにおけるコアモデリング。[https://instagram-](https://instagram-engineering.com/core-modeling-at-instagram-a51e0158aa48) [engineering.com/core-modeling-at-instagram-a51e0158aa48](https://instagram-engineering.com/core-modeling-at-instagram-a51e0158aa48)

[4] Paris Carbone, Asterios Katsifodimos, Stephan Ewen, Volker Markl, Seif Haridi, and Kostas Tzoumas. 2015. Apache Flink™: Stream and Batch Processing in a Single Engine. IEEE Data Eng. Bull. 38 (2015), 28–38.
[4] Paris Carbone, Asterios Katsifodimos, Stephan Ewen, Volker Markl, Seif Haridi, and Kostas Tzoumas. 2015. Apache Flink™: 単一エンジンでのストリームおよびバッチ処理。IEEEデータ工学。38 (2015), 28–38。

[5] Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra, Hrishikesh B. Aradhye, Glen Anderson, Gregory S



. IEEE Data Eng. Bull. 38 (2015), 28–38.
. IEEEデータ工学バルテン 38 (2015), 28–38.

[5] Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra, Hrishikesh B. Aradhye, Glen Anderson, Gregory S. Corrado, Wei Chai, Mustafa Ispir, Rohan Anil, Zakaria Haque, Lichan Hong, Vihan Jain, Xiaobing Liu, and Hemal Shah. 2016. Wide & Deep Learning for Recommender Systems. Proceedings _of the 1st Workshop on Deep Learning for Recommender Systems (2016)._
[5] Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra, Hrishikesh B. Aradhye, Glen Anderson, Gregory S. Corrado, Wei Chai, Mustafa Ispir, Rohan Anil, Zakaria Haque, Lichan Hong, Vihan Jain, Xiaobing Liu, および Hemal Shah. 2016. 推薦システムのためのWide & Deep Learning. 第1回深層学習推薦システムワークショップの議事録 (2016).

[6] Paul Covington, Jay K. Adams, and Emre Sargin. 2016. Deep Neural Networks for YouTube Recommendations. Proceedings of the 10th ACM Conference on _Recommender Systems (2016)._
[6] Paul Covington, Jay K. Adams, および Emre Sargin. 2016. YouTube推薦のための深層ニューラルネットワーク. 第10回ACM推薦システム会議の議事録 (2016).

[7] Alexandra Egg. 2021. Online Learning for Recommendations at Grubhub. Fif_teenth ACM Conference on Recommender Systems (2021)._
[7] Alexandra Egg. 2021. Grubhubにおける推薦のためのオンライン学習. 第15回ACM推薦システム会議 (2021).

[8] João Gama, Indre Žliobait˙ e, Albert Bifet, Mykola Pechenizkiy, and A. Bouchachia.˙ 2014. A survey on concept drift adaptation. ACM Computing Surveys (CSUR) 46 (2014), 1 – 37.
[8] João Gama, Indre Žliobait˙ e, Albert Bifet, Mykola Pechenizkiy, および A. Bouchachia. 2014. 概念ドリフト適応に関する調査. ACMコンピューティングサーベイ (CSUR) 46 (2014), 1 – 37.

[9] Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, and Xiuqiang He. 2017. DeepFM: A Factorization-Machine based Neural Network for CTR Prediction. In _IJCAI._
[9] Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, および Xiuqiang He. 2017. DeepFM: CTR予測のための因子分解機に基づくニューラルネットワーク. _IJCAI_において.

[10] Udit Gupta, Xiaodong Wang, Maxim Naumov, Carole-Jean Wu, Brandon Reagen, David M. Brooks, Bradford Cottel, Kim M. Hazelwood, Bill Jia, Hsien-Hsin S. Lee, Andrey Malevich, Dheevatsa Mudigere, Mikhail Smelyanskiy, Liang Xiong, and Xuan Zhang. 2020. The Architectural Implications of Facebook’s DNN-Based Personalized Recommendation. 2020 IEEE International Symposium on High _Performance Computer Architecture (HPCA) (2020), 488–501._
[10] Udit Gupta, Xiaodong Wang, Maxim Naumov, Carole-Jean Wu, Brandon Reagen, David M. Brooks, Bradford Cottel, Kim M. Hazelwood, Bill Jia, Hsien-Hsin S. Lee, Andrey Malevich, Dheevatsa Mudigere, Mikhail Smelyanskiy, Liang Xiong, および Xuan Zhang. 2020. FacebookのDNNベースのパーソナライズ推薦のアーキテクチャ的影響. 2020 IEEE国際高性能コンピュータアーキテクチャシンポジウム (HPCA) (2020), 488–501.

[11] F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Trans. Interact. Intell. Syst. 5 (2015), 19:1–19:19.
[11] F. Maxwell Harper および Joseph A. Konstan. 2015. MovieLensデータセット: 歴史と文脈. ACMトランザクション インタラクティブ インテリジェンス システム 5 (2015), 19:1–19:19.

[12] Biye Jiang, Chao Deng, Huimin Yi, Zelin Hu, Guorui Zhou, Yang Zheng, Sui Huang, Xinyang Guo, Dongyue Wang, Yue Song, Liqin Zhao, Zhi Wang, Peng Sun, Yu Zhang, Di Zhang, Jinhui Li, Jian Xu, Xiaoqiang Zhu, and Kun Gai. 2019. XDL: an industrial deep learning framework for high-dimensional sparse data. _Proceedings of the 1st International Workshop on Deep Learning Practice for High-_ _Dimensional Sparse Data (2019)._
[12] Biye Jiang, Chao Deng, Huimin Yi, Zelin Hu, Guorui Zhou, Yang Zheng, Sui Huang, Xinyang Guo, Dongyue Wang, Yue Song, Liqin Zhao, Zhi Wang, Peng Sun, Yu Zhang, Di Zhang, Jinhui Li, Jian Xu, Xiaoqiang Zhu, および Kun Gai. 2019. XDL: 高次元スパースデータのための産業用深層学習フレームワーク. _高次元スパースデータのための深層学習実践に関する第1回国際ワークショップの議事録 (2019)._

[13] Jay Kreps. 2011. Kafka : a Distributed Messaging System for Log Processing.
[13] Jay Kreps. 2011. Kafka: ログ処理のための分散メッセージングシステム.

[14] Xiangru Lian, Binhang Yuan, Xuefeng Zhu, Yulong Wang, Yongjun He, Honghuan Wu, Lei Sun, Haodong Lyu, Chengjun Liu, Xing Dong, Yiqiao Liao, Mingnan Luo, Congfei Zhang, Jingru Xie, Haonan Li, Lei Chen, Renjie Huang, Jianying Lin, Chengchun Shu, Xue-Bo Qiu, Zhishan Liu, Dongying Kong, Lei Yuan, Hai bo Yu, Sen Yang, Ce Zhang, and Ji Liu. 2021. Persia: An Open, Hybrid System Scaling Deep Learning-based Recommenders up to 100 Trillion Parameters. ArXiv abs/2111.05897 (2021).
[14] Xiangru Lian, Binhang Yuan, Xuefeng Zhu, Yulong Wang, Yongjun He, Honghuan Wu, Lei Sun, Haodong Lyu, Chengjun Liu, Xing Dong, Yiqiao Liao, Mingnan Luo, Congfei Zhang, Jingru Xie, Haonan Li, Lei Chen, Renjie Huang, Jianying Lin, Chengchun Shu, Xue-Bo Qiu, Zhishan Liu, Dongying Kong, Lei Yuan, Hai bo Yu, Sen Yang, Ce Zhang, および Ji Liu. 2021. Persia: 深層学習ベースの推薦システムを100兆パラメータまでスケーリングするオープンハイブリッドシステム. ArXiv abs/2111.05897 (2021).

[15] Meituan. 2021. Distributed Training Optimization for TensorFlow in Recom[mender Systems (in Chinese). https://tech.meituan.com/2021/12/09/meituan-](https://tech.meituan.com/2021/12/09/meituan-tensorflow-in-recommender-systems.html) [tensorflow-in-recommender-systems.html](https://tech.meituan.com/2021/12/09/meituan-tensorflow-in-recommender-systems.html)
[15] Meituan. 2021. 推薦システムにおけるTensorFlowの分散トレーニング最適化 (中国語). https://tech.meituan.com/2021/12/09/meituan-tensorflow-in-recommender-systems.html

[16] R. Pagh and Flemming Friche Rodler. 2001. Cuckoo Hashing. In ESA.
[16] R. Pagh および Flemming Friche Rodler. 2001. カッコウハッシング. ESAにおいて.

[17] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Köpf, Edward Yang, Zach DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala. 2019. PyTorch: An Imperative Style, High-Performance Deep Learning Library. In NeurIPS.
[17] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Köpf, Edward Yang, Zach DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, および Soumith Chintala. 2019. PyTorch: 命令型スタイルの高性能深層学習ライブラリ. NeurIPSにおいて.

[18] Konstantin V. Shvachko, Hairong Kuang, Sanjay R. Radia, and Robert J. Chansler. 2010. The Hadoop Distributed File System. 2010 IEEE 26th Symposium on Mass _Storage Systems and Technologies (MSST) (2010), 1–10._
[18] Konstantin V. Shvachko, Hairong Kuang, Sanjay R. Radia, および Robert J. Chansler. 2010. Hadoop分散ファイルシステム. 2010 IEEE第26回大容量ストレージシステムおよび技術シンポジウム (MSST) (2010), 1–10.

[19] HaiYing Wang, Aonan Zhang, and Chong Wang. 2021. Nonuniform Negative Sampling and Log Odds Correction with Rare Events Data. In Advances in Neural _Information Processing Systems._
[19] HaiYing Wang, Aonan Zhang, および Chong Wang. 2021. 非均一ネガティブサンプリングと希少イベントデータによる対数オッズ補正. 神経情報処理システムの進歩において.

[20] Minhui Xie, Kai Ren, Youyou Lu, Guangxu Yang, Qingxing Xu, Bihai Wu, Jiazhen Lin, Hongbo Ao, Wanhong Xu, and Jiwu Shu. 2020. Kraken: Memory-Efficient Continual Learning for Large-Scale Real-Time Recommendations. SC20: Inter_national Conference for High Performance Computing, Networking, Storage and_ _Analysis (2020), 1–17._
[20] Minhui Xie, Kai Ren, Youyou Lu, Guangxu Yang, Qingxing Xu, Bihai Wu, Jiazhen Lin, Hongbo Ao, Wanhong Xu, および Jiwu Shu. 2020. Kraken: 大規模リアルタイム推薦のためのメモリ効率の良い継続学習. SC20: 高性能コンピューティング、ネットワーキング、ストレージおよび分析に関する国際会議 (2020), 1–17.

[21] Weijie Zhao, Jingyuan Zhang, Deping Xie, Yulei Qian, Ronglai Jia, and Ping Li. 2019. AIBox: CTR Prediction Model Training on a Single Node. Proceedings of the _28th ACM International Conference on Information and Knowledge Management_ (2019).
[21] Weijie Zhao, Jingyuan Zhang, Deping Xie, Yulei Qian, Ronglai Jia, および Ping Li. 2019. AIBox: 単一ノードでのCTR予測モデルのトレーニング. 第28回ACM国際情報および知識管理会議の議事録 (2019).
