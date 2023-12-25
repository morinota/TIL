## 0.1. link リンク

- https://arxiv.org/pdf/2104.07413.pdf https://arxiv.org/pdf/2104.07413.pdf

## 0.2. title タイトル

Empowering News Recommendation with Pre-trained Language Models
事前学習済み言語モデルによるニュース推薦の強化

## 0.3. abstract 抄録

Personalized news recommendation is an essential technique for online news services.
パーソナライズされたニュースレコメンデーションは、オンラインニュースサービスにとって不可欠な手法である。
News articles usually contain rich textual content, and accurate news modeling is important for personalized news recommendation.
ニュース記事には通常、豊富なテキストコンテンツが含まれており、パーソナライズされたニュース推薦には正確なニュースモデリングが重要である。
Existing news recommendation methods mainly model news texts based on traditional text modeling methods, which is not optimal for mining the deep semantic information in news texts.
既存のニュース推薦手法は、主に伝統的なテキストモデリング手法に基づいてニューステキストをモデル化するが、これはニューステキストに含まれる深い意味情報のマイニングには最適ではない。
Pre-trained language models (PLMs) are powerful for natural language understanding, which has the potential for better news modeling.
事前に訓練された言語モデル（PLM）は自然言語理解に強力であり、より良いニュースモデリングの可能性を秘めている。
However, there is no public report that show PLMs have been applied to news recommendation.
しかし、PLMがニュース推薦に適用されたという公的な報告はない。
In this paper, we report our work on exploiting pre-trained language models to empower news recommendation.
本稿では、ニュース推薦を強化するために、事前に訓練された言語モデルを利用する研究について報告する。
Offline experimental results on both monolingual and multilingual news recommendation datasets show that leveraging PLMs for news modeling can effectively improve the performance of news recommendation.
単言語と多言語のニュース推薦データセットを用いたオフライン実験の結果、ニュースのモデリングにPLMを活用することで、ニュース推薦のパフォーマンスを効果的に改善できることが示された。
Our PLM-empowered news recommendation models have been deployed to the Microsoft News platform, and achieved significant gains in terms of both click and pageview in both English-speaking and global markets.
当社のPLMを活用したニュース推薦モデルは、Microsoft Newsプラットフォームに導入され、英語圏とグローバル市場の両方で、クリック数とページビュー数の両方で大幅な増加を達成した。

# 1. Introduction はじめに

News recommendation techniques have played critical roles in many online news platforms to alleviate the information overload of users [15].
ニュース推薦技術は、ユーザの情報過多を緩和するために、多くのオンラインニュースプラットフォームで重要な役割を果たしている[15]。
News modeling is an important step in news recommendation, because it is a core technique to understand the content of candidate news and a prerequisite for inferring user interests from clicked news.
ニュースモデリング(=要はアイテムの特徴量を抽出する、って認識:thinking:)はニュース推薦の重要なステップである。なぜなら、ニュースモデリングはニュース候補の内容を理解するための核となる技術であり、クリックされたニュースからユーザの興味を推測するための前提条件だからである。
Since news articles usually have rich textual information, news texts modeling is the key for understanding news content for news recommendation.
**通常、ニュース記事は豊富なテキスト情報を持っているため、ニューステキストのモデリングは、ニュース推薦のためにニュースコンテンツを理解するための鍵となる**。
Existing news recommendation methods usually model news texts based on traditional NLP models [15, 19, 20, 22, 23, 25, 26].
既存のニュース推薦手法は通常、伝統的なNLPモデルに基づいてニューステキストをモデル化する[15, 19, 20, 22, 23, 25, 26]。
For example, Wang et al.[20] proposed to use a knowledge-aware CNN network to learn news representations from embeddings of words and entities in news title.
例えば、Wangら[20]は、ニュースタイトルに含まれる単語とエンティティの埋め込みからニュース表現を学習するために、knowledge-aware CNNネットワークを使用することを提案している。
Wu et al.[23] proposed to use multi-head self-attention network to learn news representations from news titles.
Wuら[23]は、ニュースのタイトルからニュース表現を学習するために、multi-head self-attentionネットワークを使用することを提案した。
However, it is difficult for these shallow models to understand the deep semantic information in news texts [18].
しかし、このような**浅いモデルでは、ニューステキストに含まれる深い意味情報を理解することは難しい**[18]。
In addition, their models are only learned from the supervisions in the news recommendation task, which may not be optimal for capturing the semantic information.
加えて、彼らのモデルはニュース推薦タスクのスーパービジョン(=教師ラベル?)から学習されるだけであり、意味情報を捉えるには最適ではないかもしれない。

Pre-trained language models (PLMs) have achieved great success in NLP due to their strong ability in text modeling [2, 5, 6, 11, 12, 14, 28].
事前訓練された言語モデル（PLM）は、テキストモデリングにおける強力な能力により、自然言語処理において大きな成功を収めている[2, 5, 6, 11, 12, 14, 28]。
Different from traditional models that are usually directly trained with labeled data in specific tasks, PLMs are usually first pre-trained on a large unlabeled corpus via self-supervision to encode universal text information [5].
通常、特定のタスクにおいてラベル付きデータで直接訓練される従来のモデルとは異なり、**PLMは通常、普遍的なテキスト情報を符号化するために、自己教師を通じてラベルなしの大規模なコーパスで事前に訓練される**[5]。(うんうん:thinking:)
Thus, PLMs can usually provide better initial point for finetuning in downstream tasks [16].
したがって、PLMは通常、**下流のタスクでfine-tuningを行うための、より良い初期ポイントを提供することができる**[16]。(うんうん...!)
In addition, different from many traditional NLP methods with shallow models [9, 10, 24, 29], PLMs are usually much deeper with a huge number of parameters.
さらに、浅いモデル [9, 10, 24, 29] を持つ多くの伝統的なNLP手法とは異なり、PLMは通常、膨大な数のパラメータを持つ、より深いものである。
For example, the BERT-Base model contains 12 Transformer layers and up to 109M parameters [5].
例えば、BERT-Base モデルには、12 のトランスフォーマー層と最大 109M のパラメータが含まれる[5]。
Thus, PLMs may have greater ability in modeling the complicated contextual information in news text, which have the potentials to improve news text modeling for news recommendation.
このように、PLMはニューステキストに含まれる複雑な文脈情報をモデル化する能力が高い可能性があり、ニュース推薦のためのニューステキストのモデル化を改善する可能性がある。

In this paper, we present our work on empowering large-scale news recommendation with pre-trained language models.
Different from existing news recommendation methods that use shallow NLP models for news modeling, we explore to model news with pre-trained language models and finetune them with the news recommendation task.
本稿では、**事前学習された言語モデルを用いて大規模なニュース推薦を実現**する我々の研究を紹介する。(コード:t https://github.com/wuch15/PLM4NewsRec.)
ニュースのモデリングに浅い自然言語処理モデルを使用する既存のニュース推薦手法とは異なり、我々は**事前学習された言語モデルを用いてニュースをモデリングし、ニュース推薦タスクに合わせてそれらをfine-tuningすることを探求している**。
Offline experiments on real-world English and multilingual news recommendation datasets validate that incorporating PLMs into news modeling can consistently improve the news recommendation performance.
実世界の英語および多言語ニュース推薦データセットを用いた**オフライン実験**(オフラインかぁ...)により、ニュースモデリングにPLMを組み込むことで、ニュース推薦のパフォーマンスを一貫して改善できることが検証された。
In addition, our PLM-empowered news recommendation models have been deployed to the Microsoft News platform.
さらに、私たちのPLMを活用したニュース推薦モデルは、**Microsoft Newsプラットフォームに導入されている**(ほうほう。https://www.msn.com/ja-jp/feed 本番導入されてるのか。)。
To our best knowledge, this is the first reported effort to empower large-scale news recommender systems with PLMs.
私たちの知る限り、これは大規模なニュース推薦システムをPLMで強化する最初の取り組みである。
The online flight experiments show that our PLM-empowered news recommendation models achieved 8.53% click and 2.63% pageview gains in English-speaking markets, and 10.68% click and 6.04% pageview gains in other 43 global markets.
**オンライン実験によると、私たちのPLMを利用したニュース推薦モデルは、英語圏の市場で8.53%のクリックと2.63%のページビュー増加を達成し、その他の43のグローバル市場で10.68%のクリックと6.04%のページビュー増加を達成した**。(あ、ちゃんとオンラインテストもやってるのね。)

# 2. Methodology 方法論

In this section, we introduce the details of PLM-empowered news recommendation.
ここでは、PLMを活用したニュース推薦の詳細を紹介する。
We first introduce the general news recommendation model framework, and then introduce how to incorporate PLMs into this framework to empower news modeling.
まず一般的なニュース推薦モデルのフレームワークを紹介し、次にこのフレームワークにPLMを組み込んでニュースのモデリングを強化する方法を紹介する。

## 2.1. General News Recommendation Framework 一般的なニュース推薦フレームワーク

![fig1]()

The general framework of news recommendation used in many existing methods [1, 15, 21, 23] is shown in Fig.1.
多くの既存手法[1, 15, 21, 23]で使われているニュース推薦の一般的な枠組みを図1に示す。
The core components in this framework include a news encoder that aims to learn the embeddings of news from their texts, a user encoder that learns user embedding from the embeddings of clicked news, and a click prediction module that computes personalized click score for news ranking based on the relevance between user embedding and candidate news embedding.
このフレームワークの中心的な構成要素には、ニュース埋め込みをテキストから学習することを目的とした**news encoder**、クリックされたニュースの埋め込み(のinteraction sequence or set!)からユーザの埋め込みを学習する**user encoder**、ユーザの埋め込みとニュースの埋め込み候補の間の関連性に基づいてニュースのランキングのためのパーソナライズされたクリックスコアを計算する**click prediction module**が含まれる[1, 15, 21, 23]。
We assume a user has 𝑇 historical clicked news, which are denoted as $[D_1, D_2, \cdots,  D_T]$.
あるユーザが過去にクリックしたニュースを $[D_1, D_2, \cdots,  D_T]$ として、$T$ 個持っていると仮定する。
The news encoder processes these clicked news of a user and each candidate news $D_c$ to obtain their embeddings, which are denoted as $[h_1, h_2, \cdots, h_T]$ and $h_c$, respectively.
ニュースエンコーダは、ユーザのクリックされたニュースと各候補ニュース $D_c$ を処理し、それらの埋め込みを求め、それぞれを $[h_1, h_2, \cdots, h_T]$ および $h_c$ とする。
It can be implemented by various NLP models, such as CNN [10] and self-attention [18].
(news encoderは)CNN[10]やself-attention[18]など、さまざまなNLPモデルによって実装できる。

The user encoder receives the sequence of clicked news embeddings as input, and outputs a user embedding $\mathbf{u}$ that summarizes user interest information.
ユーザエンコーダは、クリックされたニュースの埋め込み**シーケンス**(=setではなくsequenceとして扱う事を想定してるのかな...!)を入力として受け取り、ユーザの関心情報を要約したユーザ埋め込み $\mathbf{u}$ を出力する。
It can also be implemented by various models, such as the GRU network used in [15], the attention network used in [21] and the combination of multi-head self-attention and additive attention networks used in [23].
また、[15]で使用されているGRUネットワーク、[21]で使用されているattentionネットワーク、[23]で使用されているmulti-head self-attentionネットワークとadditive attentionネットワークの組み合わせなど、様々なモデルによって実装することができる。

The click prediction module takes the user embedding u and h𝑐 as inputs, and compute the click score 𝑦ˆ by evaluating their relevance.
クリック予測モジュールは、ユーザ埋め込み $\mathbf{u}$ と $\mathbf{h}_{c}$ を入力とし、それらの関連性を評価することでクリックスコア $\hat{y}$ を計算する。
It can also be implemented by various methods such as inner product [15], neural network [20] and factorization machine [7].
また、内積[15]、ニューラルネットワーク[20]、因数分解マシン[7]など、さまざまな方法で実装することもできる。(**dot-product以外のclick prediction module気になる...!**:thinking:)

## 2.2. PLM Empowered News Recommendation PLM

Next, we introduce the framework of PLM empowered news recommendation, as shown in Fig.2.
次に、図2に示すように、PLMを活用したニュース推薦のフレームワークを紹介する。
We instantiate the news encoder with a pre-trained language model to capture the deep contexts in news texts and an attention network to pool the output of PLM.
ニュースエンコーダには、ニューステキストに含まれる深い文脈を捉えるために事前学習された言語モデルと、**PLMの出力をプールするためのattetionネットワーク**をインスタンス化する。(PLMで出力される word embedding達を集約してnews text embeddingを作る為という認識:thinking: この方法を採用した理由は実験セクションで後述されていた...!)
We denote an input news text with $M$ tokens as $[w_1,w_2, \cdots,w_M]$.
ここでは、$M$ 個のトークンを持つ入力ニューステキストを $[w_1,w_2, \cdots,w_M]$ とします。
The PLM converts each token into its embedding, and then learns the hidden representations of words through several Transformer [18] layers.
PLMは各トークンを埋め込みに変換し、いくつかのTransformer [18]層を通して単語のhidden representationを学習する。
We denote the hidden token representation sequence as $[r_1, r_2, \cdots, r_M]$.
hiddenトークン表現sequenceを $[r_1, r_2, \cdots, r_M]$ とする。
We use an attention [29] network to summarize the hidden token representations into a unified news embedding.
アテンション[29]ネットワークを使って、hiddenトークン表現sequenceを統一されたニュース埋め込みに要約する。
(なんとなく、特殊トークン $[CLS]$ のhiddenトークン表現を、文の埋め込みとみなしてそれをそのままニュース埋め込みとして使う想像だったが、事前学習モデルとは別でattentionに通してニュース埋め込みを作るのかな...?:thinking:この方法を採用した理由は後述されてた。)
The news embeddings learned by the PLM and attention network are further used for user modeling and candidate matching.
PLMとアテンション・ネットワークによって学習されたニュース埋め込みは、さらにユーザモデリング(=fig2の右側?)と候補マッチング(=fig2の左側?)に使用される。

## 2.3. Model Training モデルトレーニング

Following [22, 23], we also use negative sampling techniques to build labeled samples from raw news impression logs, and we use the cross-entropy loss function for model training by classifying which candidate news is clicked.
また、[22, 23]に倣い、ネガティブサンプリング技術(=教師あり学習におけるnegative exampleを作る手法。)を用いて生のニュースimpression (i.e. interaction?:thinking:) ログからラベル付きサンプルを作成し、どの候補のニュースがクリックされたかを分類することで、モデルの学習にクロスエントロピー損失関数を用いる。(=**next item prediction的なタスクを学習させる想定なのかな**??:thinking:)
By optimizing the loss function via backward-propagation, the parameters in the recommendation model and PLMs can be tuned for the news recommendation task.
逆誤差伝搬法によって損失関数を最適化することで、**推薦モデル(=user encoderと click prediction module?) とPLMのパラメータをニュース推薦タスクに合わせてチューニング**することができる。

# 3. Experiments 実験

## 3.1. Datasets and Experimental Settings データセットと実験設定

Our offline experiments are conducted on two real-world datasets.
我々のオフライン実験は、2つの実世界データセットで行われた。
The first one is MIND [27], which is an English dataset for monolingual news recommendation.
最初のものは MIND [27]であり、**単言語ニュース推薦のための英語データセット**である。
It contains the news click logs of 1 million users on Microsoft News in six weeks.3
マイクロソフトニュースの6週間における100万ユーザーのニュースクリックログが含まれている。

The second one is a multilingual news recommendation dataset (denoted as Multilingual) collected by ourselves on MSN News platform from Dec.1, 2020 to Jan.14, 2021.
2つ目は、2020年12月1日から2021年1月14日まで、MSN Newsプラットフォームで収集した**多言語ニュース推薦データセット**（Multilingualと表記）である。
It contains users from 7 countries with different language usage, and their market language codes are EN-US, DE-DE, FR-FR, IT-IT, JA-JP, ES-ES and KO-KR, respectively.
異なる言語を使用する7カ国のユーザが含まれており、その市場言語コードはそれぞれEN-US、DE-DE、FR-FR、IT-IT、JA-JP、ES-ES、KO-KRである。
We randomly sample 200,000 impression logs in each market.
各市場で20万件のインプレッション・ログを無作為に抽出。
The logs in the last week are used for test and the rest are used for training and validation (9:1 split).
直近1週間のログをテストに使用し、残りをトレーニングと検証に使用する（9:1の割合）。
The detailed statistics of the two datasets are shown in Table 1.
2つのデータセットの詳細な統計は表1に示されている。

![table1]()

In our experiments, we used the “Base” version of different pretrained language models if not specially mentioned.
実験では、特に言及されていない限り、さまざまな事前学習済み言語モデルの「ベース」バージョンを使用した。
We finetuned the last two Transformer layers because we find there is only a very small performance difference between finetuning all layers and the last two layers.
すべてのレイヤーをfine-tuningするのと、最後の2つのレイヤーをfine-tuningするのとでは、パフォーマンスにごくわずかな差しかないことがわかったからだ。
Following [27], we used the titles of news for news modeling.
[27]に従い、**ニュースのタイトルをニュースのモデリングに使用**した。
We used Adam [3] as the optimization algorithm and the learning rate was 1e-5.
最適化アルゴリズムにはAdam [3]を使用し、学習率は1e-5とした。
The batch size was 128.4 These hyperparameters are developed on the validation sets.
バッチサイズは128.4で、これらのハイパーパラメータは検証セットで開発された。
We used average AUC, MRR, nDCG@5 and nDCG@10 over all impressions as the performance metrics.
すべてのimpressionの平均AUC、MRR、NDCG@5、NDCG@10をパフォーマンス指標として使用した。
We repeated each experiment 5 times independently and reported the average performance.
各実験を独立に5回繰り返し、その平均値を報告した。

## 3.2. Offline Performance Evaluation オフライン性能評価

We first compare the performance of several methods on the MIND dataset to validate the effectiveness of PLM-based models in monolingual news recommendation.
まず、単言語ニュース推薦におけるPLMベースのモデルの有効性を検証するために、MINDデータセットでいくつかの手法のパフォーマンスを比較する。
We compared several recent news recommendation methods including EBNR [15], NAML [21], NPA [22], LSTUR [1], NRMS [23] and their variants empowered by different pre-trained language models, including BERT [5], RoBERTa [14] and UniLM [2].
EBNR[15]、NAML[21]、NPA[22]、LSTUR[1]、NRMS[23]、およびBERT[5]、RoBERTa[14]、UniLM[2]など、さまざまな事前学習済み言語モデルによって強化されたそれらの変種(=手法+news encoderをPLMに!)を含む、最近のニュース推薦手法を比較した。

![table2]()

The results are shown in Table 2.
結果を表2に示す。
Referring to this table, we find that incorporating pre-trained language models can consistently improve the performance of basic models.5
この表を参照すると、PLMを組み込むことで、基本モデルのパフォーマンスを一貫して向上させることができることがわかる5。
This is because pre-trained language models have stronger text modeling ability than the shallow models learned from scratch in the news recommendation.
これは、**PLMがニュース推薦でゼロから学習された浅いモデルよりも強力なテキストモデリング能力を持つため**である。
In addition, we find that the models based on RoBERTa are better than those based on BERT.
さらに、RoBERTa(=PLMの一つ)に基づくモデルは、BERTに基づくモデルよりも優れていることがわかった。
This may be because RoBERTa has better hyperparameter settings than BERT and is pre-trained on larger corpus for a longer time.
これは、RoBERTaがBERTよりも優れたハイパーパラメータ設定を持っており、より大きなコーパスでより長い時間事前訓練されているためと考えられる。
Besides, the models based on UniLM achieve the best performance.
さらに、UniLM(=これもPLMの一つ)に基づくモデルは最高のパフォーマンスを達成した。
This may be due to UniLM can exploit the self-supervision information in both text understanding and generation tasks, which can help learn a higher-quality PLM.
これは、UniLMがテキスト理解と生成タスクの両方で自己教師情報を利用できるため、より質の高いPLMを学習できるためと考えられる。

In addition, we conduct experiments on the Multilingual dataset to validate the effectiveness of PLMs in multilingual news recommendation.
さらに、多言語ニュース推薦におけるPLMの有効性を検証するため、多言語データセットを用いた実験を行う。
We compare the performance of EBNR, NAML, NPA, LSTUR and NRMS with different multilingual text modeling methods, including:
我々は、EBNR、NAML、NPA、LSTUR、NRMSの性能を、以下のような異なる**多言語テキストモデリング手法(=多言語対応のPLMって意味?:thinking:)**と比較する:
(1) MUSE [13], using modularizing unsupervised sense embeddings; (2) Unicoder [8], a universal language encoder pre-trained by cross-lingual self-supervision tasks; and (3) InfoXLM [4], a contrastively pre-trained cross-lingual language model based on information-theoretic framework.
(1)教師なしセンス埋め込み(?)をモジュール化したMUSE [13]、
(2)ユニコーダ[8]、クロスリンガル自己教師タスクで事前訓練されたユニバーサル言語エンコーダ、
(3)情報理論的フレームワークに基づくcontrastiveに事前学習されたクロスリンガル言語モデル、InfoXLM [4]。
In these methods, following [8] we mix up the training data in different languages.
これらの方法では、[8]に従い、異なる言語の学習データを混在させる。
In addition, we also compare the performance of independently learned monolingual models based on MUSE for each market (denoted as Single).
さらに、MUSEをベースに独自に学習した各市場の単言語モデル（Singleと表記）の性能も比較した。

![table3]()

The results of different methods in terms of AUC are shown in Table 3.
AUCの観点からの異なる方法の結果を表3に示す。
We find that multilingual models usually outperform the independently learned monolingual models.
我々は、**多言語モデルが通常、独立して学習された単言語モデルよりも優れていることを発見**した。
This may be because different languages usually have some inherent relatedness and users in different countries may also have some similar interests.
これは、異なる言語には固有の関連性があり、異なる国のユーザもまた、同じような関心を持っている可能性があるからだろう。
Thus, jointly training models with multilingual data can help learn a more accurate recommendation model.
このように、**多言語データを用いてモデルを共同学習することで、より精度の高い推薦モデルを学習することができる**。
It also provides the potential to use a unified recommendation model to serve users in different countries with diverse language usage (e.g., IndoEuropean and Altaic), which can greatly reduce the computation and memory cost of online serving.
また、異なるmarket(=異なる言語域)で統合された推薦モデルを使用することで、多様な言語（例えば、印欧語とアルタイ語）を使用するさまざまな国のユーザにサービスを提供できる可能性があり、**オンライン・サービスの計算コストとメモリー・コストを大幅に削減できる**。(各market毎に、言い換えれば異なるusecase毎に異なるモデルを運用するよりも...!:thinking:)
In addition, the performance methods based on multilingual PLMs are better than those based on MUSE embeddings.
さらに、多言語PLMに基づく方法は、MUSE埋め込み(=単言語PLMだっけ?)に基づく方法よりも性能が良い。
This may be because PLMs are also stronger than word embeddings in capturing the complicated multilingual semantic information.
これは、PLMが複雑な多言語の意味情報を捉える上で、単語埋め込みよりも強いからかもしれない。(MUSEがどんな手法なのか良くわかってない...!:thinking:)
In addition, InfoXLM can better empower multilingual news recommendation than Unicoder.
さらに、InfoXLMは、Unicoderよりも多言語ニュース推薦を強化することができます。
This may be because InfoXLM uses better contrastive pre-training strategies than Unicoder to help learn more accurate models.
これは、InfoXLMがUnicoderよりも優れたcontrastive事前学習戦略を使って、より正確なモデルを学習しているためと思われる。

## 3.3. Influence of Model Size モデルサイズの影響

![fig3]()

Next, we explore the influence of PLM size on the recommendation performance.
次に、**PLMのサイズが推薦性能に与える影響**を探る。
We compare the performance of two representative methods (i.e., NAML and NRMS) with different versions of BERT, including BERT-Base (12 layers), BERT-Medium (8 layers), BERTSmall (4 layers) and BERT-Tiny (2 layers).
BERT-Base（12 層）、BERT-Medium（8 層）、BERTSmall（4 層）、および BERT-Tiny（2 層）を含む BERT のさまざまなバージョンと、代表的な 2 つの手法（NAML および NRMS）の性能を比較する。
The results on MIND are shown in Fig.3.
MINDでの結果を図3に示す。
We find that using larger PLMs with more parameters usually yields better recommendation performance.
**通常、より大きなPLMとより多くのパラメータを使用することで、より良い推薦性能が得られる**ことがわかる。
This may be because larger PLMs usually have stronger abilities in capturing the deep semantic information of news, and the performance may be further improved if more giant PLMs (e.g., BERT-Large) are incorporated.
これは、**通常、大型の PLM の方が、ニュースの深い意味情報を捕捉する能力が高い**ためであり、より巨大な PLM（BERT-Large など）を組み込めば、パフォーマンスがさらに向上する可能性がある。
However, since huge PLMs are too cumbersome for online applications, we prefer the base version of PLMs.
**しかし、巨大なPLMはオンラインアプリケーションには面倒なので、私たちは基本版のPLMを好む**。

## 3.4. Influence of Different Pooling Methods 異なるプーリング方法の影響

We also explore using different pooling methods for learning news embeddings from the hidden states of PLMs.
また、PLMの隠れトークン表現のsequenceからニュースの埋め込みを学習するために、異なるプーリング方法を使用することも検討する。(PLMの出力をattentionで集約するやつ!:thinking:)
We compare three methods, including:
以下の3つの方法を比較する：

(1) CLS, using the representation of the “[CLS]” token as news embedding, which is a widely used method for obtaining sentence embedding;
(1)CLS：ニュース埋め込みとして"[CLS]"トークンの表現を用いる。これは、文の埋め込みを得るために広く使われている方法である。(=PLMを使う方法として真っ先にこれを想像した!:thinking:)
(2) Average, using the average of hidden states of PLM;
(2) PLMの隠された状態の平均を使用した平均；
(3) Attention, using an attention network to learn news embeddings from hidden states.
(3) アテンション・ネットワークを使って、隠れた状態からニュースの埋め込みを学習する。(これが本論文で提案してるアプローチだよね??)

![fig4]()

The results of NAML-BERT and NRMS-BERT on MIND are shown in Fig.4.
MIND における NAML-BERT および NRMS-BERT の結果を図 4に示す。
We find it is very interesting that the CLS method yields the worst performance.
我々は、**CLS法が最悪のパフォーマンスをもたらしたことが非常に興味深い**ことに気づいた。
This may be because it cannot exploit all output hidden states of the PLM.
これは、PLMのすべての出力hidden state(=全てのtokenの隠れトークン表現の事だよね??)を利用できないからかもしれない。(そうなの...??)
In addition, Attention outperforms Average.
さらに、**アテンションはアベレージを上回る**。
This may be because attention networks can distinguish the informativeness of hidden states, which can help learn more accurate news representations.
これは、self-attentionネットワークが**hidden stateの情報性を区別する**ことができ、より正確なニュース表現を学習するのに役立つからかもしれない。(=たぶんmulti-headアテンションなのかな??)
Thus, we choose attention mechanism as the pooling method.
よって、プーリング方法としてアテンション・メカニズムを選択する。

## 3.5. Visualization of News Embedding ニュースの埋め込みの可視化

We also study the differences between the news embeddings learned by shallow models and PLM-empowered models.
また、**浅いモデルで学習されたニュース埋め込みと、PLMを利用したモデルの違い**についても研究している。
We use t-SNE [17] to visualize the news embeddings learned by NRMS and NRMSUniLM, and the results are shown in Fig.5.
NRMSとNRMSUniLMによって学習された**ニュース埋め込みを可視化するためにt-SNE [17]を用い**(t-SNEが気になる...!!:thinking:)、その結果を図5に示す。
We find an interesting phenomenon that the news embeddings learned by NRMS-UniLM are much more discriminative than NRMS.
**NRMS-UniLMによって学習されたニュース埋め込みは、NRMSよりもはるかに識別性が高いという興味深い現象を発見した**。(=この埋め込みベクトルの識別性の高さの評価は、モデルの推論結果のモニタリングとか評価とかに良いかも...! booking.comが採用してた応答分布分析と同様に、教師ラベルに依存してない評価方法だし...!!:thinking:)
This may be because the shallow self-attention network in NRMS cannot effectively model the semantic information in news texts.
これは、NRMSの浅いself-attentionネットワークでは、ニューステキストの意味情報を効果的にモデル化できないからかもしれない。
Since user interests are also inferred from embeddings of clicked news, it is difficult for NRMS to accurately model user interests from non-discriminative news representations.
ユーザの興味はクリックされたニュースの埋め込みからも推測されるため、**NRMSのはっきりと識別できてないニュース表現からユーザの興味を正確にモデル化することは難しい**。
In addition, we observe that the news embeddings learned by NRMS-UniLM form several clear clusters.
さらに、NRMS-UniLMによって学習されたニュース埋め込みは、いくつかの**明確なクラスターを形成**していることがわかる。
This may be because the PLM-empowered model can disentangle different kinds of news for better user interest modeling and news matching.
これは、PLMを活用したモデルが、より良いユーザの関心モデリングとニュースマッチングのために、異なる種類のニュースを区別することができるためであろう。
These results demonstrate that deep PLMs have greater ability than shallow NLP models in learning discriminative text representations, which is usually beneficial for accurate news recommendation.
これらの結果は、ディープPLMが浅いNLPモデルよりも**識別的なテキスト表現を学習する能力が高い**ことを示しており、これは通常、**正確なニュース推薦に有益**である。

## 3.6. Online Flight Experiments オンライン飛行実験

We have deployed our PLM-empowered news recommendation models into the Microsoft News platform.
私たちは、PLMを活用したニュース推薦モデルをMicrosoft Newsプラットフォームに導入しました。
Our NAML-UniLM model was used to serve users in English-speaking markets, including EN-US, EN-GB, EN-AU, EN-CA and EN-IN.
当社のNAML-UniLMモデルは、EN-US、EN-GB、EN-AU、EN-CA、EN-INを含む**英語圏市場**のユーザーにサービスを提供するために使用された。
The online flight experimental results have shown a gain of 8.53% in click and 2.63% in pageview against the previous news recommendation model without pre-trained language model.
オンラインフライトの実験結果は、PLMを使用しない従来のニュース推薦モデルに対して、クリック数で8.53%、ページビューで2.63%の利得を示しました。
In addition, our NAML-InfoXLM model was used to serve users in other 43 markets with different languages.
さらに、我々のNAML-InfoXLMモデルは、言語の異なる他の43の市場のユーザにサービスを提供するためにも使用された。
The online flight results show an improvement of 10.68% in click and 6.04% in pageview.
オンライン・フライトの結果は、クリック数で10.68%、ページビューで6.04%の改善を示している。
These results validate that incorporating pre-trained language models into news recommendation can effectively improve the recommendation performance and user experience of online news services.
これらの結果は、PLMをニュース推薦に組み込むことで、オンラインニュースサービスの推薦パフォーマンスとユーザーエクスペリエンスを効果的に改善できることを検証している。

# 4. Conclusion 結論

In this paper, we present our work on empowering personalized news recommendation with pre-trained language models.
本稿では、事前に学習された言語モデルを用いて、パーソナライズされたニュース推薦を実現するための我々の研究を紹介する。
We conduct extensive offline experiments on both English and multilingual news recommendation datasets, and the results show incorporating pre-trained language models can effectively improve news modeling for news recommendation.
英語と多言語のニュース推薦データセットでオフライン実験を行った結果、事前に訓練された言語モデルを組み込むことで、ニュース推薦のためのニュースモデリングを効果的に改善できることがわかった。
In addition, our PLM-empowered news recommendation models have been deployed to a commercial news platform, which is the first public reported effort to empower real-world large-scale news recommender systems with PLMs.
さらに、私たちのPLMを利用したニュース推薦モデルは、商業的なニュースプラットフォームに導入されており、これは、PLMを利用して実際の大規模なニュース推薦システムを強化する最初の取り組みとして公に報告されている。
The online flight results show significant improvement in both click and pageview in a large number of markets with different languages.
オンライン・フライトの結果は、クリック数、ページビュー数ともに、言語の異なる多くの市場で大幅な改善を示している。

## 参考

- EBNR: Embedding-based news recommendation for millions of users
- NAML: Neural News Recommendation with Attentive Multi-View
Learning. 
- NPA: Neural news recommendation with personalized attention.
- LSTUR: Neural News Recommendation with Long-and Short-term User Representations.
- NRMS: Neural News Recommendation with Multi-Head Self-Attention.

ニュース推薦用のコンテンツベース推薦モデルをあんまり知らないので、年末年始でざっくり調べようと思ってる。
2021のhttps://arxiv.org/pdf/2104.07413.pdf にて、最近のコンテンツベースのニュース推薦モデルとして以下の5つを挙げていたので、この辺りを漁ってみようかな。

- [EBNR: Embedding-based news recommendation for millions of users](http://library.usc.edu.ph/ACM/KKD%202017/pdfs/p1933.pdf)
- [NAML: Neural News Recommendation with Attentive Multi-View Learning.](https://arxiv.org/abs/1907.05576)
- [NPA: Neural news recommendation with personalized attention.](https://arxiv.org/abs/1907.05559)
- [LSTUR: Neural News Recommendation with Long-and Short-term User Representations.](https://aclanthology.org/P19-1033/)
- [NRMS: Neural News Recommendation with Multi-Head Self-Attention.](https://aclanthology.org/D19-1671/)

ニュースの埋め込みを作る部分というよりは、ユーザの埋め込みを作る部分 (i.e. user encoder) と、ニュースとユーザの埋め込みから推薦スコアを算出する部分 (i.e. click prediction module) を参考にしたい...!