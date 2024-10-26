# STAR: A Simple Training-free Approach for Recommendations using Large Language Models STAR： 大規模言語モデルを用いた推薦のための訓練不要のシンプルなアプローチ

## abstract 抄録

Recent progress in large language models (LLMs) offers promising new approaches for recommendation system (RecSys) tasks.
最近の大規模言語モデル（LLM）の進歩は、推薦システム（RecSys）タスクに有望な新しいアプローチを提供する。
While the current state-of-the-art methods rely on fine-tuning LLMs to achieve optimal results, this process is costly and introduces significant engineering complexities.
**現在のSOTA（最先端技術）は、最適な結果を得るためにLLMをfine-tuneすることに依存している**が、このプロセスはコストがかかり、著しいエンジニアリングの複雑さを導入する。
Conversely, methods that bypass fine-tuning and use LLMs directly are less resource-intensive but often fail to fully capture both semantic and collaborative information, resulting in sub-optimal performance compared to their fine-tuned counterparts.
逆に、ファインチューニングをバイパスし、**LLMを直接使用する方法は、リソースを少なく済ませるが、しばしば意味的情報と協調情報の両方を十分に捉えることができず、ファインチューニングされたモデルと比較して最適なパフォーマンスを発揮しない**。
In this paper, we propose a Simple Training-free Approach for Recommendation (STAR), a framework that utilizes LLMs and can be applied to various recommendation tasks without the need for fine-tuning.
本論文では、**ファインチューニングを必要とせず、LLMを利用してさまざまな推薦タスクに適用できるフレームワーク**であるSimple Training-free Approach for Recommendation (STAR)を提案する。
Our approach involves a retrieval stage that uses semantic embeddings from LLMs combined with collaborative user information to retrieve candidate items.
我々のアプローチでは、**LLMからの意味的埋め込みと協調的ユーザ情報を組み合わせて候補アイテムを取得する検索ステージ**が含まれている。(2-stages推薦の1段階目。これだけでも推薦としては機能する。2段階目をモジュールっぽく柔軟に取り外し可能だといいな:thinking:)
We then apply an LLM for pairwise ranking to enhance next-item prediction.
次に、ペアワイズ・ランキングにLLMを適用し、next-item predictionを強化する。
Experimental results on the Amazon Review dataset show competitive performance for next item prediction, even with our retrieval stage alone.
Amazon Reviewデータセットでの実験結果は、我々の検索ステージだけでも、次のアイテム予測で競争力のある性能を示している。
Our full method achieves Hits@10 performance of +23.8% on Beauty, +37.5% on Toys and Games, and -1.8% on Sports and Outdoors relative to the best supervised models.
我々の完全な方法は、最高の教師ありモデルに対して、Beautyで+23.8%、Toys and Gamesで+37.5%、Sports and Outdoorsで-1.8%のHits@10性能を達成している。(まあここは結局オフライン評価だから、我々のユースケースではなんとも言えない。というか、多分この結果の部分はあんまり本論文で重要なところではないはずなので、4章と5章は飛ばして良さそう:thinking:)
This framework offers an effective alternative to traditional supervised models, highlighting the potential of LLMs in recommendation systems without extensive training or custom architectures.
このフレームワークは、従来の教師ありモデルに対する効果的な代替手段を提供し、**大規模なトレーニングやカスタムアーキテクチャを必要とせずに、推薦システムにおけるLLMの可能性**を示している。

<!-- ここまで読んだ! -->

## Introduction

Personalized recommendation systems have become indispensable tools for enhancing user experiences and driving engagement across a wide range of online platforms.
パーソナライズされたレコメンデーションシステムは、幅広いオンラインプラットフォームにおいて、ユーザ体験を向上させ、エンゲージメントを促進するために欠かせないツールとなっている。
Recent advances in large language models (LLMs) present new opportunities for addressing recommendation tasks .
大規模言語モデル（LLM）の最近の進歩は、推薦タスクに取り組む新しい機会を提供している。
Current strategies primarily involve utilizing LLMs as either feature encoders, or as scoring and ranking functions.
**現在の戦略では、主にLLMを特徴エンコーダとして使用するか、スコアリングおよびランキング機能として使用するかのいずれか**である。
When LLMs are employed as feature encoders, there is potential for transfer learning and cross-domain generalization by initializing embedding layers with LLM embeddings, although this approach requires extensive training.
LLMを特徴エンコーダとして採用する場合、LLM埋め込みで埋め込み層を初期化することで、転移学習やクロスドメインの汎化の可能性があるが、このアプローチには大規模なトレーニングが必要である。
On the other hand, using LLMs for scoring and ranking demonstrates the ability to leverage their reasoning capabilities to address recommendation tasks.
一方、LLMをスコアリングおよびランキングに使用することで、推薦タスクに対処するために推論能力を活用する能力が示される。
However, these models still lag behind the performance of fine-tuned models due to a lack of collaborative knowledge.
しかし、これらのモデルは、**協調的知識の不足により、fine-tuningされたモデルの性能に遅れをとっている**。

Figure 1.Retrieval pipeline uses scoring rules that combine semantic and collaborative information with temporal, weight, and rating factors to score unseen items without requiring any fine-tuning.
図1.検索パイプラインは、意味情報と協調情報を時間的、重み、および評価要素と組み合わせたスコアリングルールを使用して、微調整を必要とせずに未見のアイテムをスコアリングする。

The primary motivation of this work is to develop a general framework that serves as a generalist across multiple recommendation domains.
この研究の第一の動機は、**複数のレコメンデーション領域にわたってジェネラリストとして機能する一般的なフレームワークを開発すること**である。
We demonstrate that recent advancements in LLMs align with this vision, effectively functioning as generalists without requiring any domain-specific fine-tuning.
我々は、最近のLLMの進歩がこのビジョンと一致しており、**ドメイン固有の微調整を必要とせずにジェネラリストとして効果的に機能する**ことを示す。
Based on our findings, we present a Simple Training-free Approach for Recommendation (STAR) framework using LLMs.
我々の発見に基づいて、LLMを用いた推薦のためのSimple Training-free Approach for Recommendation (STAR)フレームワークを提案する。
The STAR framework involves two stages: Retrieval and Ranking.
**STARフレームワークには2つの段階がある： 検索とランキング**である。
The Retrieval stage scores new items using a combination of semantic similarity and collaborative commonality to the items in a user’s history.
検索ステージでは、ユーザの履歴にあるアイテムとの意味的類似性と協調的共通性の組み合わせを使って、新しいアイテムをスコアリングする。
Here, we utilize LLM-based embeddings to determine semantic similarity.
ここでは、LLMに基づく埋め込みを利用して、意味的類似性を決定する。
Additionally, a temporal factor gives priority to user’s recent interactions, and a rating factor aligns with user preferences to rank items within a specific set (See Figure 1 and Section 3.2).
さらに、temporal factor (時間的要素) はユーザの最近の相互作用に優先度を与え、rating factor (評価要素) は特定のセット内のアイテムをランク付けするためにユーザの嗜好に合わせる（図1とセクション3.2を参照）。(まだわからん!:thinking:)
The Ranking stage leverages the reasoning capabilities of LLMs to adjust the rankings of the initially retrieved candidates.
**ランキング・ステージでは、LLMの推論能力を活用して、最初に取得した候補のランキングを調整する**。
Specifically, we assess various LLM-based ranking approaches, including point-wise, pair-wise, and list-wise methods, while also determining the key information needed for the LLM to better understand user preferences and make accurate predictions (Section 3.3).
具体的には、ポイント・ワイズ法、ペア・ワイズ法、リスト・ワイズ法など、さまざまなLLMベースのランキング・アプローチを評価するとともに、LLMがユーザの嗜好をよりよく理解し、正確な予測を行うために必要な主要情報を決定する（セクション3.3）。
Our experimental evaluation shows competitive performance across a diverse range of recommendation datasets, all without the need for supervised training or the development of custom-designed architectures.
我々の実験評価では、様々な推薦データセットにおいて、教師あり学習やカスタム設計アーキテクチャの開発を必要としない、競争力のある性能を示している。
（プロンプトで、簡単に推薦戦略を調整できたらいいなぁ...:thinking:）

We present extensive experimental results on the Amazon Review dataset (mcauley2015image,; he2016ups,).
Amazon Reviewデータセット(mcauley2015image,; he2016ups,)を用いた広範な実験結果を示す。
Our findings are as follow: (1) Our retrieval pipeline, comprised of both semantic relationship and collaborative information, demonstrates competitive results compared to a wide range of fine-tuned methods.
我々の発見は以下の通りである： **(1)意味関係と協調情報の両方から構成される我々の検索パイプラインは、様々な微調整された手法と比較して競争力のある結果を示す**。(ほーん:thinking:)
LLM embeddings allow for an effective method to calculate semantic similarity; (2) We show that pair-wise ranking further improves upon our retrieval performance, while point-wise and list-wise methods struggle to achieve similar improvements; and (3) We illustrate that collaborative information is a critical component that adds additional benefits to the semantic information throughout our system, in both the retrieval and ranking stages.
LLM埋め込みは、意味的類似性を計算するための効果的な手法を提供することができる；(2) ペア・ワイズ法は、検索パフォーマンスをさらに向上させる一方、ポイント・ワイズ法とリスト・ワイズ法は同様の改善を達成するのに苦労することを示す；(3) 協調情報は、検索およびランキングの両段階で、システム全体に追加の利益をもたらす重要な要素であることを示す。

<!-- ここまで読んだ! -->

## Related Work 関連作品

### LLM as a Feature Encoder for RecSys RecSysのフィーチャー・エンコーダーとしてのLLM

Recommendation systems typically leverage feature encoders to transform item and user profiles into suitable representations for model training.
レコメンデーションシステムは通常、特徴エンコーダを活用してアイテムやユーザープロファイルをモデル学習に適した表現に変換する。
Traditionally, ID-based systems relied on one-hot encoding for structured features (zhou2018deep,; wang2021dcn,).
従来、IDベースのシステムは、構造化特徴のワンホットエンコーディングに依存していた（zhou2018deep,; wang2021dcn,）。
However, recent advancements in LLMs have enabled the utilization of text encoders to capture rich semantic information from item metadata and user profiles (reimers2019sentence,; cer-etal-2018-universal,; ni2021sentence,; lee2024gecko,) To further optimize these representations for specific applications, researchers have explored several approaches: (1) mapping continuous LLM embeddings into discrete tokens using vector quantization and training a subsequent generative model (hou2023learning,; singh2023better,; rajput2024recommender,; zheng2024adapting,); (2) training sequential models by initializing the embedding layer with LLM embeddings (sun2019bert4rec,; yuan2023go,; hu2024enhancing,); and (3) training models to directly compute the relevance between item and user embeddings (i.e., embeddings of user selected items) (Ding2022,; hou2022towards,; gong2023unified,; li2023text,; liu2024once,; li2024enhancing,; ren2024representation,; sheng2024language,).
しかし、最近のLLMの進歩により、アイテムのメタデータやユーザープロファイルから豊富な意味情報を取得するためにテキストエンコーダを利用することが可能になった（reimers2019sentence,; cer-etal-2018-universal,; ni2021sentence,; lee2024gecko, ）特定のアプリケーションのためにこれらの表現をさらに最適化するために、研究者はいくつかのアプローチを模索してきた： (1)ベクトル量子化を用いて連続的なLLM埋め込みを離散的なトークンにマッピングし、その後に生成モデルを学習する(hou2023learning,; singh2023better,; rajput2024recommender,; zheng2024adapting,)； (2)埋め込み層をLLM埋め込みで初期化し、逐次モデルを学習する(sun2019bert4rec,; yuan2023go,; hu2024enhancing,)、(3)アイテムとユーザの埋め込み間の関連性を直接計算するモデルを学習する(i. e., の埋め込み）（Ding2022,; hou2022towards,; gong2023unified,; li2023text,; liu2024once,; li2024enhancing,; ren2024representation,; sheng2024language, ）。
While optimizing representations can improve recommendation performance, this often comes at the cost of increased training expenses and reduced generalizability.
表現を最適化することで、推薦のパフォーマンスを向上させることができるが、その代償として学習コストが増加し、汎化性が低下することが多い。
In this work, we demonstrate that LLM embeddings can be directly used as effective item representations, yielding strong results in sequential recommendation tasks without requiring extensive optimization.
本研究では、LLM埋め込みが効果的なアイテム表現として直接利用でき、大規模な最適化を必要とせずに逐次推薦タスクにおいて強力な結果をもたらすことを実証する。
This finding aligns with those of (harte2023leveraging,), but differs by usage of novel scoring rules that incorporates collaborative and temporal information.
この発見は(harte2023leveraging,)のものと一致するが、協調的・時間的情報を組み込んだ新しいスコアリング・ルールを用いる点で異なる。

### LLM as a Scoring and Ranking function for RecSys RecSysのスコアリングおよびランキング機能としてのLLM

Recent studies show that LLMs can recommend items by understanding user preferences or past interactions in natural language.
最近の研究によれば、LLMは自然言語によるユーザーの嗜好や過去のやり取りを理解することで、アイテムを推薦することができる。
This is achieved through generative selection prompting, where the model ranks and selects top recommended items from a set of candidates (wang2023zero,; wang2023drdt,; hou2024large,; wang-etal-2024-recmind,; xu2024prompting,; zhao2024let,; liang2024taxonomy,).
これは生成的選択プロンプトによって達成され、モデルが候補の集合から上位の推奨項目をランク付けして選択する（wang2023zero,; wang2023drdt,; hou2024large,; wang-etal-2024-recmind,; xu2024prompting,; zhao2024let,; liang2024taxonomy, ）。
However, these studies show that LLMs alone are less effective than models fine-tuned on user-item interaction data, which leverage collaborative knowledge.
しかし、これらの研究は、LLMだけでは、協調的知識を活用する、ユーザーとアイテムの相互作用データに基づいて微調整されたモデルよりも効果が低いことを示している。
To bridge the gap between collaborative knowledge and the semantic understanding of LLMs, recent efforts have focused on fine-tuning the models with interaction data, though this approach is also costly (geng2022recommendation,; zhang2023recommendation,; bao2023tallrec,; xu2024openp5,; tan2024idgenrec,; kim2024large,).
協調的知識とLLMの意味理解とのギャップを埋めるために、最近の取り組みでは、相互作用データを使ってモデルを微調整することに焦点が当てられているが、このアプローチにもコストがかかる（geng2022recommendation,; zhang2023recommendation,; bao2023tallrec,; xu2024openp5,; tan2024idgenrec,; kim2024large,）。

### LLM as a Ranker for Information Retrieval 情報検索のランカーとしてのLLM

Ranking using LLMs has been widely adopted in document retrieval (zhu2023large,; wang2024large,).
LLMを用いたランキングは文書検索で広く採用されている（zhu2023large,; wang2024large,)。
Recent studies indicate that LLMs surpass traditional supervised cross-encoders in zero-shot passage ranking.
最近の研究では、LLMが従来の教師ありクロスエンコーダよりもゼロショット通過ランキングで優れていることが示されている。
Three prompting approaches have emerged: (1) point-wise: LLMs directly evaluate relevance using numerical scores or binary judgments (liang2022holistic,; zhuang2023beyond,), but this method struggles with capturing the relative importance of passages; (2) pair-wise: LLMs express preferences between item pairs, which is effective but inefficient due to the high number of calls required (qin-etal-2024-large,); (3) list-wise: LLMs compare multiple passages simultaneously (sun2023chatgpt,), but performance heavily relies on the model’s semantic prior and reasoning capabilities (qin-etal-2024-large,).
3つのプロンプティング・アプローチが登場した： (1) ポイント方式： (1)ポイント・ワイズ：LLMは数値スコアや二値判断を用いて関連性を直接評価するが(liang2022holistic,; zhuang2023beyond,)、この方法ではパッセージの相対的な重要性を捉えるのに苦労する： (2)ペアワイズ: LLMは項目ペア間の選好を表現するが、これは効果的であるが、必要な呼び出し回数が多いため非効率的である(qin-etal-2024-large,)： LLMは複数のパッセージを同時に比較するが(sun2023chatgpt,)、性能はモデルの意味的事前評価と推論能力に大きく依存する(qin-etal-2024-large,)。
In this paper, we investigate the potential of LLM ranking for recommendation tasks, which are subjective in nature, unlike the deterministic nature of document retrieval.
本稿では、文書検索の決定論的な性質とは異なり、主観的な性質を持つ推薦タスクに対するLLMランキングの可能性を調査する。

## STAR: Smart Training-free Approach STAR スマート・トレーニング・フリー・アプローチ

Figure 2.STAR Framework overview.
図2.STAR フレームワークの概要。
We use the semantic relationship scores in R S and the collaborative relationship scores in R C to score the items in the user history compared to new items to recommend.
R Sの意味関係スコアとR Cの協調関係スコアを用いて、ユーザー履歴にあるアイテムと新しいアイテムを比較してスコアリングし、レコメンドする。
The final score for one new item is a weighted average from the semantic relationship and collaborative relationship scores, with additional weights from the user’s ratings r and a temporal decay λ < 1 which prioritize recent interactions.
新しいアイテムの最終的なスコアは、意味関係スコアと協調関係スコアから加重平均され、さらにユーザーの評価rと時間的減衰λ<1から加重平均され、最近の相互作用を優先する。
The top scoring retrieved items are sent to the LLM Ranking, where we can use point-wise, pair-wise, or list-wise ranking approaches to further improve upon the scoring of recommended items.
検索されたアイテムのスコアの上位は、LLMランキングに送られ、推奨アイテムのスコアリングをさらに向上させるために、ポイントワイズ、ペアワイズ、リストワイズのランキングアプローチを使用することができる。

This section initially outlines the problem formulation (Section 3.1).
このセクションでは、まず問題定式化の概要を述べる（セクション3.1）。
Subsequently, we detail the proposed retrieval (Section 3.2) and ranking pipelines (Section 3.3).
続いて、提案する検索パイプライン（セクション3.2）とランキングパイプライン（セクション3.3）について詳述する。

### Sequential Recommendation 順次推薦

Figure 2.STAR Framework overview.
図2.STAR フレームワークの概要。
We use the semantic relationship scores in R S and the collaborative relationship scores in R C to score the items in the user history compared to new items to recommend.
R Sの意味関係スコアとR Cの協調関係スコアを用いて、ユーザー履歴にあるアイテムと新しいアイテムを比較してスコアリングし、レコメンドする。
The final score for one new item is a weighted average from the semantic relationship and collaborative relationship scores, with additional weights from the user’s ratings r and a temporal decay λ < 1 which prioritize recent interactions.
新しいアイテムの最終的なスコアは、意味関係スコアと協調関係スコアから加重平均され、さらにユーザーの評価rと時間的減衰λ<1から加重平均され、最近の相互作用を優先する。
The top scoring retrieved items are sent to the LLM Ranking, where we can use point-wise, pair-wise, or list-wise ranking approaches to further improve upon the scoring of recommended items.
検索されたアイテムのスコアの上位は、LLMランキングに送られ、推奨アイテムのスコアリングをさらに向上させるために、ポイントワイズ、ペアワイズ、リストワイズのランキングアプローチを使用することができる。

### Retrieval Pipeline 検索パイプライン

The retrieval pipeline aims to assign a score to an unseen item x ∈ I given the sequence S u .
検索パイプラインの目的は、シーケンス S u が与えられたときに、未見の項目 x∈I にスコアを割り当てることである。
To achieve this, we build two scoring components: one that focuses on the semantic relationship between items and another that focuses on the collaborative relationship.
これを実現するために、2つのスコアリング・コンポーネントを構築する： 1つはアイテム間の意味的関係に注目するもので、もう1つは協調関係に注目するものである。

#### Semantic Relationship 意味上の関係

Understanding how similar a candidate item is to the items in a user’s interaction history s i ∈ S u is key to accurately gauging how well candidate items align with user preferences.
候補アイテムがユーザーの対話履歴s i∈S uのアイテムとどの程度似ているかを理解することは、候補アイテムがユーザーの嗜好とどの程度一致しているかを正確に測定するための鍵となる。
Here we leverage LLM embedding models, where we pass in custom text prompts representing items and collect embedding vectors of dimension d e .
ここではLLM埋め込みモデルを活用し、項目を表すカスタムテキストプロンプトを渡し、次元d eの埋め込みベクトルを収集する。
We construct a prompt based on the item information and metadata, including the title, description, category, brand, sales ranking, and price.
タイトル、説明文、カテゴリー、ブランド、売上ランキング、価格などのアイテム情報とメタデータに基づいてプロンプトを作成する。
We omit metadata fields like Item ID and URL, as those fields contain strings that can contain spurious lexical similarity (e.g., IDs: “000012”, “000013’ or URLs: “<https://abc.com/uxrl”>, “<https://abc.com/uxrb”>) and can reduce the uniformity of the embedding space and make it difficult to distinguish between semantically different items (See Appendix A.1 for the full prompt).
アイテムIDやURLのようなメタデータフィールドは、偽の字句の類似性を含む可能性のある文字列を含むため、省略する（例えば、ID： 「000012「、」000013'、またはURL： 「<https://abc.com/uxrl「>、」<https://abc.com/uxrb">）、埋め込み空間の均一性を低下させ、意味的に異なるアイテムの区別を困難にする可能性があります（完全なプロンプトについては付録A.1を参照してください）。
We collect embeddings for each item i ∈ I , resulting in E ∈ ℝ n × d e , where n is number of items in I .
各アイテムi ∈ I の埋め込みを集めると、E ∈ ℝ n × d e となる。
The semantic relationship between two items ( i a , i b ) is then calculated using the cosine similarity between their embeddings E i a , E i b ∈ E .
そして、2つの項目（ i a , i b ）の間の意味的関係は、それらの埋め込み E i a , E i b ∈ E の余弦類似度を用いて計算される。
This measure provides a numerical representation of how closely related the items are in semantic space.
この尺度は、意味空間において項目がどれだけ密接に関連しているかを数値で表したものである。
For our experiments, we precompute the entire semantic relationship matrix R S ∈ ℝ n × n .
実験では、意味関係行列R S ∈ ℝ n × n全体を事前に計算する。
For many domains, this is a practical solution.
多くのドメインにとって、これは現実的な解決策である。
However, if | I | is very large, Approximate Nearest Neighbor methods (guo2020accelerating,; sun2024soar,) are efficient approaches to maintain quality and reduce computation.
 I

#### Collaborative Relationship 協力関係

Collaborative relationship.
協力関係。
Semantic similarity between a candidate item and items in a user’s interaction history is a helpful cue for assessing the similarity of items based on the item information.
候補アイテムとユーザーの対話履歴内のアイテムとの間の意味的類似性は、アイテム情報に基づいてアイテムの類似性を評価するための有用な手がかりとなる。
However, this alone does not fully capture the engagement interactions of items by multiple users.
しかし、これだけでは、複数のユーザーによるアイテムのエンゲージメント・インタラクションを完全に捉えることはできない。
To better understand the collaborative relationship, we consider how frequently different combinations of items are interacted with by users.
協調関係をよりよく理解するために、異なるアイテムの組み合わせがユーザーによってどれだけ頻繁に相互作用されるかを検討する。
These shared interaction patterns can provide strong indicators of how likely the candidate item is to resonate with a broader audience with similar preferences.
これらの共有インタラクションパターンは、候補となるアイテムが、同じような嗜好を持つより広範なオーディエンスに響く可能性がどれだけ高いかを示す強力な指標となる。
For each item i ∈ I , we derive an interaction array that represents user interactions, forming a set of sparse user-item interaction arrays C ∈ ℝ n × m , where m is number of users in U .
各アイテム i ∈ I に対して、ユーザーとの相互作用を表す相互作用配列を導出し、疎なユーザー・アイテム相互作用配列の集合 C ∈ ℝ n × m を形成する。
The collaborative relationship between two items ( i a , i b ) is then computed by using the cosine similarity between their sparse arrays C i a , C i b ∈ C , capturing the normalized co-occurrence of the items.
2つのアイテム（i a , i b）間の協調関係は、アイテムの正規化された共起をキャプチャする、それらの疎な配列C i a , C i b∈C間の余弦類似度を使用して計算される。
To streamline the process, we pre-compute and store these values in a collaborative relationship matrix R C ∈ ℝ n × n , which is typically very sparse.
プロセスを効率化するために、これらの値を事前に計算し、一般的に非常に疎な協調関係行列R C∈ℝ n×nに格納する。

#### Scoring rules 得点ルール

The score for an unseen item x ∈ I is calculated by averaging both the semantic and collaborative relationships between items in S u = { s 1 , s 2 , … , s n } as follows:
未見の項目x∈Iのスコアは、S u = { s 1 , s 2 , ... , s n }の項目間の意味的関係と協調的関係の両方を平均することにより、以下のように計算される：

where R S x ⁢ j and R C x ⁢ j represent the semantic and collaborative relationships between the unseen item x and item s j ∈ S u , respectively.
ここで、R S x jとR C x jはそれぞれ、未見項目xと項目s j∈S uの間の意味的関係と協調的関係を表す。
In this equation, r j is the rating given by user u to item s j , and λ t j is an exponential decay function applied to the temporal order t j of s j in the sequence S u .
この式において、r j はアイテム s j に対してユーザー u が与えた評価であり、λ t j はシーケンス S u における s j の時間的順序 t j に対して適用される指数減衰関数である。
Here, t j is set to 1 for the most recent item in S u and increments by 1 up to n for the oldest item.
ここで、t jは、S uの中で最も新しい項目については1に設定され、最も古い項目についてはnまで1ずつインクリメントされる。
The framework, illustrated in Figure 2, outputs the top k items in descending order based on their scores.
図2に示すフレームワークは、スコアの降順で上位k項目を出力する。

### Ranking Pipeline ランキング・パイプライン

Figure 3.Prompt overview for the ranking pipeline.
図3.ランキングパイプラインのプロンプト概要。
The prompt includes history items, candidate items, and instructions for the ranking strategy.
プロンプトには、履歴項目、候補項目、ランキング戦略の指示が含まれる。
Each item is represented by metadata, along with additional details such as popularity and co-occurrence, formatted in JSON.
各アイテムは、人気度や共起度などの追加情報とともに、JSONでフォーマットされたメタデータで表現される。
Full prompt is available in Appendix A.2.
完全なプロンプトは付録A.2に掲載されている。

After retrieving the top k items, denoted as I k , from the initial retrieval process, a LLM is employed to further rank these items to enhance the overall ranking quality.
最初の検索プロセスから上位k項目（I kと表記）を検索した後、LLMを使用してこれらの項目をさらにランク付けし、全体的なランク付けの質を高める。
The items in I k are already ordered based on scores from the retrieval framework, which reflect semantic, collaborative, and temporal information.
I kの項目は、すでに検索フレームワークからのスコアに基づいて順序付けされており、意味的、協調的、時間的情報を反映している。
We intentionally incorporate this initial order into the ranking process to enhance both efficiency and effectiveness.
私たちは、効率と効果の両方を高めるために、この最初の順序を意図的にランキングプロセスに組み込んでいる。
This framework then leverages the capabilities of the LLM to better capture user preference, complex relationships and contextual relevance among the items.
そして、このフレームワークはLLMの機能を活用し、ユーザーの嗜好、アイテム間の複雑な関係、文脈上の関連性をよりよく捉える。

#### Rank schema ランクスキーマ

We present three main strategies for ranking: (1) Point-wise evaluates each item x ∈ I k independently, based on the user sequence S u , to determine how likely it is that user u will interact with item x .
我々は、ランキングのための3つの主要な戦略を提示する： (1) ユーザーシーケンス S u に基づいて、各アイテム x ∈ I k を独立にポイントワイズ評価し、ユーザー u がアイテム x と相互作用する可能性を決定する。
If two items receive the same score, their rank follows the initial order from I k ; (2) Pair-wise evaluates the preference between two items x i , x j ∈ I k based on the user sequence S u .
(2) ユーザ配列 S u に基づいて、2つの項目 x i , x j ∈ I k の嗜好性をペアワイズ評価する。
We adopt a sliding window approach, starting from the items with the lowest retrieval score at the bottom of the list (qin-etal-2024-large,).
スライディング・ウインドウ方式を採用し、検索スコアが最も低いものから順に検索していく（qin-etal-2024-large,)。
The LLM compares and swaps adjacent pairs, while iteratively stepping the comparison window one element at a time.(3) List-wise evaluates the preference among multiple items x i , … , x i + w ∈ I k based on the user sequence S u .
LLMは、比較ウィンドウを1要素ずつ反復的にステップさせながら、隣接するペアを比較し、入れ替える。(3) リスト・ワイズは、ユーザー・シーケンスS uに基づいて、複数の項目x i , ... , x i + w ∈ I kの間の選好度を評価する。
This method also uses a sliding window approach, with a window size w and a stride d to move the window across the list, refining the ranking as it passes (sun2023chatgpt,).
この方法もまた、スライディング・ウインドウ・アプローチを用いており、ウインドウ・サイズwとストライドdでウインドウをリスト全体に移動させ、通過するたびにランキングを洗練させていく（sun2023chatgpt,)。
In this setup, pair-wise is a special case of list-wise with w = 2 and d = 1 .
このセットアップでは、ペアワイズは、w = 2、d = 1のリストワイズの特別な場合である。

#### Item information アイテム情報

We represent the metadata (e.g., Item ID, title, category, etc.) for each item in the user sequence s j ∈ S u and each candidate item to be ranked x ∈ I k as JSON format in the input prompt.
入力プロンプトでは、ユーザシーケンスs j∈S uの各アイテムと、ランク付け候補x∈I kの各アイテムのメタデータ（アイテムID、タイトル、カテゴリなど）をJSON形式で表現する。
Additionally, we incorporate two more types of information that can help the reasoning capabilities of the LLM: (1) Popularity is calculated as the number of users who have interacted with the item x , simply by counting the occurrences in the training data.
さらに、LLMの推論能力を支援する2つのタイプの情報を組み込む： (1) 人気度（Popularity）は、学習データ中の出現回数を数えるだけで、アイテムxと対話したユーザーの数として計算される。
This popularity value is then included in the prompt for both the items in the user sequence s j ∈ S u and the candidate item to be ranked x ∈ I k as “Number of users who bought this item: ###”; (2) Co-occurrence is calculated as the number of users who have interacted with both item x and item s j ∈ S u .
(1)人気度：この人気度の値は、ユーザー列 s j ∈ S u のアイテムと、ランク付け候補アイテム x ∈ I k の両方に、「このアイテムを購入したユーザー数」としてプロンプトに含まれる： ###(2)共起は、アイテムxとアイテムs j∈S uの両方とインタラクションしたユーザー数として計算される。
The resulting value is then included for candidate items x ∈ I k as “Number of users who bought both this item and item s j : ###”.
その結果、候補アイテムx∈I kに対して、「このアイテムとアイテムs jの両方を購入したユーザー数」として値が含まれる： ###」.

## Experimental Setup 実験セットアップ

### Datasets データセット

### Dataset Construction and Evaluation Metrics データセットの構築と評価指標

### Compared Methods 比較方法

### Implementation Details 実施内容

## Experimental Results 実験結果

### Retrieval Pipeline 検索パイプライン

#### Q1. How do semantic and collaborative information affect predictions? Q1. 意味情報と協調情報は予測にどのような影響を与えるのか？

#### Q2. How does the number of user history items l and recency factor λ affect predictions? Q2. ユーザー履歴アイテムの数lと再帰性係数λは予測にどのような影響を与えるか？

#### Q3. Does incorporating more user feedback improve results? Q3. より多くのユーザーからのフィードバックを取り入れることで、結果は向上するのか？

## Conclusion 結論

In this paper, we introduced a Simple Training-free Approach for Recommendation (STAR) that uses the power of large language models (LLMs) to create a generalist framework applicable across multiple recommendation domains.
本稿では、大規模言語モデル(LLM)の力を利用して、複数の推薦ドメインに適用可能な汎化フレームワークを構築する、推薦のためのシンプルなトレーニングフリーアプローチ(STAR)を紹介する。
Our method comprises two key stages: a retrieval phase and a ranking phase.
我々の方法は2つの重要な段階からなる： 検索段階とランキング段階である。
In the retrieval stage, we combine semantic embeddings from LLMs with collaborative user information to effectively select candidate items.
検索段階では、LLMからの意味埋め込みと協調的なユーザ情報を組み合わせて、候補項目を効果的に選択する。
In the ranking stage, we apply LLMs to enhance next-item prediction and refine the recommendations.
ランキングの段階では、LLMを適用して次のアイテムの予測を強化し、レコメンデーションを洗練させる。
Experimental results on a large-scale Amazon review dataset demonstrate that our retrieval method alone outperforms most supervised models.
大規模なアマゾンのレビューデータセットでの実験結果は、我々の検索手法のみがほとんどの教師ありモデルを上回ることを実証している。
By employing LLMs in the ranking stage, we achieve further improvements.
ランキングの段階でLLMを採用することで、さらなる改善を実現した。
Importantly, our study highlights that incorporating collaborative information is critical in both stages to maximize performance.
重要なことは、我々の研究が、パフォーマンスを最大化するためには、両ステージにおいて協力的な情報を取り入れることが重要であることを強調していることである。
Our findings reveal that LLMs can effectively function as generalists in recommendation tasks without requiring any domain-specific fine-tuning.
我々の発見は、LLMが推薦タスクにおいて、領域特有の微調整を必要とすることなく、ジェネラリストとして効果的に機能することを明らかにした。
This opens up exciting possibilities for developing versatile and efficient recommendation systems that are readily adaptable across diverse domains.
これは、多様なドメインに容易に適応可能な、多用途で効率的な推薦システムを開発するためのエキサイティングな可能性を開くものである。

## Limitations & Future Work 限界と今後の課題

The STAR framework presents an effective alternative to traditional supervised models, showcasing the potential of LLMs in recommendation systems without the need for extensive training or custom architectures.
STARフレームワークは、従来の教師ありモデルに代わる効果的なモデルを提示し、大規模なトレーニングやカスタムアーキテクチャを必要としない推薦システムにおけるLLMの可能性を示す。
However, several limitations remain, which also indicate directions for future improvement:
しかし、いくつかの限界も残っており、今後の改善の方向性も示している：

### Importance of item modality and enriched item meta-data 項目モダリティと充実した項目メタデータの重要性

The STAR framework’s ability to capture semantic relationships between items relies significantly on the presence of rich item text meta-data.
STARフレームワークのアイテム間の意味的関係を捉える能力は、リッチアイテムのテキストメタデータの存在に大きく依存している。
Without such meta-data and with only user-item interaction data available, the framework’s semantic relationship component will be less effective.
このようなメタデータがなく、ユーザーとアイテムの相互作用データしか利用できない場合、フレームワークの意味的関係コンポーネントの効果は低くなる。
To maximize the use of semantic relationships between items, future work should explore incorporating additional modalities, such as visual or audio data, to generate more comprehensive semantic representations of items, fully utilizing all the available information.
アイテム間の意味的関係を最大限に利用するために、今後の研究では、視覚データや音声データなどの追加モダリティを組み込んで、利用可能なすべての情報を完全に活用して、アイテムのより包括的な意味表現を生成することを検討すべきである。

### Improving Retrieval Simplicity and Scalability 検索の簡素化と拡張性の向上

Although our work demonstrates the effectiveness of a general training-free framework, the current method requires different choices for parameters.
我々の研究は、一般的な訓練不要のフレームワークの有効性を実証しているが、現在の手法では、パラメータに異なる選択が必要である。
In future work, we will explore ways to either reduce the number of parameters choices or select values more easily.
今後の研究では、パラメータの選択肢を減らすか、より簡単に値を選択する方法を検討する。
In our current implementation, we compute the full set of item-item comparisons for both the semantic and collaborative information.
現在の実装では、意味情報と協調情報の両方について、項目-項目比較のフルセットを計算する。
This computation is infeasible if the item set is too large.
アイテムセットが大きすぎる場合、この計算は実行不可能である。
In future work, we will run experiments to measure how effective approximate nearest neighbor methods are at reducing computation and maintaining retrieval quality.
今後の研究では、近似最近傍法が計算量を削減し、検索品質を維持するのにどれだけ効果的かを測定する実験を行う予定である。

### Beyond LLM ranking ビヨンドLLMランキング

The importance of our work highlights that high quality results can be achieved without additional fine-tuning.
我々の研究の重要性は、微調整を加えなくても質の高い結果が得られることを強調している。
However, in the current method, our STAR ranking pipeline utilizes costly LLM calls that would result in high latency.
しかし、現在の方法では、STARランキング・パイプラインはコストのかかるLLMコールを使用するため、待ち時間が長くなる。
This may be a suitable solution to use in offline scenarios, but would be prohibitive to serve large-scale and real-time user traffic.
これは、オフラインのシナリオで使用するには適切なソリューションかもしれないが、大規模でリアルタイムのユーザートラフィックに対応するのは困難である。
Future work needs to explore how we can improve efficiency, such as using a mix of pair-wise and list-wise ranking.
今後の研究では、ペアワイズ・ランキングとリストワイズ・ランキングを混在させるなど、効率を向上させる方法を探る必要がある。
Our work shows a promising first step to creating high quality, training-free, and general recommendation systems.
我々の研究は、高品質でトレーニング不要の一般的な推薦システムを作るための有望な第一歩を示している。
