## 0.1. link リンク

- https://arxiv.org/abs/2305.06566 https://arxiv.org/abs/2305.06566

## 0.2. title タイトル

A First Look at LLM-Powered Generative News Recommendation
LLMによる生成的ニュース推薦の初見

## 0.3. abstract 抄録

Personalized news recommendation systems have become essential tools for users to navigate the vast amount of online news content, yet existing news recommenders face significant challenges such as the cold-start problem, user profile modeling, and news content understanding.
パーソナライズされたニュース推薦システムは、ユーザーが膨大なオンラインニュースコンテンツをナビゲートするために不可欠なツールとなっているが、既存のニュース推薦システムは、コールドスタート問題、ユーザープロファイルのモデリング、ニュースコンテンツの理解など、大きな課題に直面している。
Previous works have typically followed an inflexible routine to address a particular challenge through model design, but are limited in their ability to understand news content and capture user interests.
これまでの研究は、モデル設計を通じて特定の課題に対処するための柔軟性に欠けるルーチンに従うのが一般的であったが、ニュースの内容を理解し、ユーザーの関心を捉える能力には限界があった。
In this paper, we introduce GENRE, an LLM-powered generative news recommendation framework, which leverages pretrained semantic knowledge from large language models to enrich news data.
本稿では、**LLMを活用した生成的ニュース推薦フレームワークであるGENRE**を紹介する。GENREは、大規模な言語モデルから事前に学習された意味知識を活用し、ニュースデータを充実させる.
Our aim is to provide a flexible and unified solution for news recommendation by moving from model design to prompt design.
モデル設計からプロンプト設計に移行することで、ニュース推薦のための柔軟で統一されたソリューションを提供することを目的としています。
We showcase the use of GENRE for personalized news generation, user profiling, and news summarization.
パーソナライズされたニュースの生成、ユーザのプロファイリング、ニュースの要約にGENREを使用した例を紹介する。
Extensive experiments with various popular recommendation models demonstrate the effectiveness of GENRE.
様々な一般的な推薦モデルを用いた広範な実験により、GENREの有効性が実証されている。
We will publish our code and data for other researchers to reproduce our work.
我々は、他の研究者が我々の研究を再現できるように、コードとデータを公開する。

# 1. Introduction はじめに

Online news platforms, such as Google News, play a vital role in disseminating information worldwide.
グーグルニュースのようなオンラインニュースプラットフォームは、世界中に情報を発信する上で重要な役割を果たしている。
However, the sheer volume of articles available on these platforms can be overwhelming for users.
しかし、これらのプラットフォームで利用可能な記事の膨大な量は、ユーザーを圧倒する可能性がある。
Hence, news recommender systems have become an essential component, guiding users navigate through a vast amount of content and pinpointing articles that align with their interests.
それゆえ、ニュース推薦システムは、膨大なコンテンツの中からユーザーをナビゲートし、ユーザーの興味に沿った記事をピンポイントで紹介する、不可欠な要素となっている。
Nonetheless, present news recommendation systems face several major challenges.
それにもかかわらず、現在のニュース推薦システムはいくつかの大きな課題に直面している。
One such challenge is the well-known cold-start problem, a scenario where many long-tail or new users have limited browsing history, making it difficult to accurately model and understand their interests.
このような課題のひとつが、よく知られているコールドスタート問題である。ロングテールユーザーや新規ユーザーの多くは閲覧履歴が限られているため、彼らの興味を正確にモデル化して理解することが難しいというシナリオである。
User profile modeling poses another challenge, since user profiles consist of highly condensed information, such as geographic location or topics of interest, which are frequently withheld from datasets due to privacy concerns.
ユーザープロファイルは、地理的な位置や関心のあるトピックなど、非常に凝縮された情報で構成されているため、プライバシーの問題からデータセットに含まれないことが多い。
Additionally, there is the unique challenge of news content understanding in the field of news recommendation.
さらに、ニュース推薦の分野では、ニュース内容の理解というユニークな課題がある。
Due to limited and unaligned text information in news datasets, it can be challenging for models to capture the deeper semantics of news articles.
ニュースデータセットのテキスト情報は限られており、整合性がとれていないため、モデルがニュース記事の深い意味を捉えることは困難である。
For instance, in an article (in the MIND [48] dataset) with the title “Here’s Exactly When To Cook Every Dish For Thanksgiving Dinner”, the main idea may be “guidance” or “instructions” rather than the specific terms mentioned in the title.
例えば、「Here's Exactly When To Cook Every Dish For Thanksgiving Dinner」というタイトルの記事（MIND [48]データセット内）では、タイトルで言及されている特定の用語ではなく、「ガイダンス」や「指示」が主なアイデアかもしれない。
However, accurately identifying key concepts or themes in news articles can be challenging, which in turn affects the ability of news recommender systems to provide personalized recommendations to users.
しかし、**ニュース記事中の主要な概念やテーマを正確に特定すること**は困難であり、それはニュース推薦システムがユーザーにパーソナライズされた推薦を提供する能力に影響する。
Previous works [19, 41, 45] have proposed various recommendation models to tackle the aforementioned challenges.
先行研究[19, 41, 45]では、前述の課題に取り組むために様々な推薦モデルが提案されている。
However, due to the limited data and knowledge available in the training dataset, these models are limited in their ability to understand news content and capture user interests.
しかし、学習データセットに含まれるデータや知識には限りがあるため、これらのモデルでは、ニュースの内容を理解し、ユーザーの関心を把握する能力に限界がある。
Although some methods [37] have attempted to incorporate external sources, such as knowledge graphs, their performance is often constrained by the size of the knowledge graphs.
いくつかの手法[37]は、知識グラフのような外部ソースを組み込むことを試みているが、その性能は知識グラフのサイズによって制約を受けることが多い。

LLM-powered generative news recommendation: a novel perspective.
LLMを利用した生成的ニュース推薦：新しい視点。
The advancement of large language models (LLMs), such as ChatGPT2 or LLaMA [32], has revolutionized the field of natural language processing.
ChatGPT2やLLaMA [32]のような大規模言語モデル（LLM）の進歩は、自然言語処理の分野に革命をもたらした。
The exceptional language modeling capability of LLMs enables them to understand complex patterns and relationships in language.
LLMの卓越した言語モデリング能力により、言語の複雑なパターンや関係を理解することができる。
As powerful few-shot learners, they can quickly learn the distribution of news data and incorporate relevant contextual information to improve their understanding of the data.
強力な数発学習者として、ニュースデータの分布を素早く学習し、関連する文脈情報を取り入れてデータの理解を深めることができる。
This makes LLMs a suitable tool for addressing the challenges of news recommendation systems, including the cold-start problem, user profile modeling, and news content understanding.
このためLLMは、コールドスタート問題、ユーザープロファイルのモデリング、ニュース内容の理解など、ニュース推薦システムの課題に取り組むのに適したツールとなっている。

In this work, we introduce a novel perspective for news recommendation by using LLMs to generate informative knowledge and news data such as synthetic news content tailored to cold-start users, user profiles, and refined news titles, which can be utilized to enhance the original dataset and tackle the aforementioned challenges.
本研究では、LLMを用いて、コールドスタートユーザに合わせた合成ニュースコンテンツ、ユーザプロファイル、洗練されたニュースタイトルなど、有益な知識とニュースデータを生成することで、**オリジナルのデータセットを拡張**し、前述の課題に取り組むために利用できる、ニュース推薦のための新しい視点を紹介する。

Figure 1 illustrates our proposed LLM-powered GEnerative News REcommendation (GENRE) framework.
図1は、我々が提案するLLMを利用した**GEnerative News REcommendation（GENRE）フレームワーク**を示している。
The main idea is to utilize the available news data, such as the title, abstract, and category of each news article, to construct prompts or guidelines, which can then be fed into an LLM for producing informative news information.
主なアイデアは、各ニュース記事のタイトル、抄録、カテゴリなどの利用可能なニュースデータを利用して、プロンプトやガイドラインを構築し、それをLLMに入力して有益なニュース情報を作成することである。
Due to its extensive pretrained semantic knowledge, the LLM can comprehend the underlying distribution of news data, even with very limited information provided in the original dataset, and generate enriched news data and information.
LLMは、事前に訓練された広範な意味的知識により、元のデータセットで提供される情報が非常に限られていても、ニュースデータの根本的な分布を理解し、充実したニュースデータと情報を生成することができる。
These generated news data and information can be integrated back into the original dataset for the next round of knowledge generation in an iterative fashion, or utilized to train downstream news recommendation models.
これらの生成されたニュースデータや情報は、次の知識生成のために元のデータセットに繰り返し統合したり、下流のニュース推薦モデルの学習に利用したりすることができる。
In this study, we explore GENRE for 1) personalized news generation, 2) user profiling, and 3) news summarization, to address the three challenges mentioned above.
本研究では、上記の3つの課題を解決するために、1）パーソナライズされたニュースの生成、2）ユーザのプロファイリング、3）ニュースの要約のためのGENREを探求する。
To validate the effectiveness of our proposed GENRE framework, we perform comprehensive experiments on IM-MIND [50], a multimodal news recommendation dataset derived from MIND [48].
提案するGENREフレームワークの有効性を検証するために、MIND [48]から派生したマルチモーダルニュース推薦データセットであるIM-MIND [50]を用いて包括的な実験を行った。
We employ GPT-3.5 as the LLM and collect the generated data through API calls.
**LLMとしてGPT-3.5を採用し、APIコールによって生成データを収集**する。(お金たくさんかかりそう...!)
Our evaluation involves four matching-based news recommendation models and four ranking-based CTR models, all of which are typical and widely used in industrial recommender systems.
我々の評価では、4つのマッチングベースのニュース推薦モデルと4つのランキングベースのCTRモデルを評価した。
We observe that GENRE improves the performance of the base models significantly.
我々は、**GENREがベースモデルのパフォーマンスを大幅に向上させる**ことを確認した。
To summarize, our contributions are listed as follows:
要約すると、我々の貢献は以下の通りである：

- To our knowledge, this work is the first attempt to exploit LLMs for generative news recommendation. 我々の知る限り、この研究はLLMを生成的なニュース推薦に利用する最初の試みである。

- We propose GENRE, an LLM-based generative news recommendation framework. Compared to traditional methods that require designing individual models for different tasks, GENRE offers a flexible and unified solution by introducing pretrained semantic knowledge to the training data through prompt design. 我々は、LLMベースの生成的ニュース推薦フレームワークであるGENREを提案する。 タスクごとに個別のモデルを設計する必要がある従来の手法に比べ、GENREはプロンプト設計を通じて訓練データに事前訓練された意味知識を導入することで、柔軟かつ統一的なソリューションを提供する。

- We demonstrate the effectiveness of GENRE through extensive experimentation and evaluation on three tasks: 1) personalized news generation, 2) user profiling, and 3) news summarization. GENREの有効性を、3つのタスクに関する広範な実験と評価を通じて実証する： 1）パーソナライズされたニュースの生成、2）ユーザーのプロファイリング、3）ニュースの要約である。

# 2. Preliminaries 前哨戦

## 2.1. Notations and Problem Statement

Before delving into the details of our proposed method, we first introduce basic notations and formally define the news recommendation task.
提案手法の詳細に入る前に、まず基本的な記法を紹介し、ニュース推薦タスクを正式に定義する。
Let N be a set of news articles, where each news 𝑛 ∈ N is represented by a multi-modal feature set including the title, category, and cover image.
$N$ をニュース記事の集合とし、各ニュース $n \in N$ はタイトル、カテゴリ、カバー画像を含むマルチモーダル特徴量セットで表される.
Let U be a set of users, where each user 𝑢 ∈ U has a history of reading news articles ℎ (𝑢) .
$U$ をユーザ集合とし、各ユーザ $u \in U$ はニュース記事を読んだ履歴 $h (u)$ を持つ.
Let D be a set of click data, where each click 𝑑 ∈ D is a tuple (𝑢, 𝑛, 𝑦) indicating whether user 𝑢 clicked on news article 𝑛 with label 𝑦 ∈ {0, 1}.
各クリック $d \in D$ は、ラベル $y \in {0, 1}$ を持つニュース記事 $n$ をユーザ $u$ がクリックしたかどうかを示すタプル $(u, n, y)$ である。
The task of the news recommendation is to infer the user’s interest in a candidate news article.
ニュース推薦のタスクは、**候補となるニュース記事に対するユーザのinterestを推測すること**である。

## 2.2. General News Recommendation Model 一般ニュース推薦モデル

A news recommendation model generally involves three modules: a news encoder, a user encoder, and an interaction module.
ニュース推薦モデルには一般的に、**ニュースエンコーダ、ユーザーエンコーダ、インタラクションモジュールの3つのモジュール**が含まれる。
The news encoder, as depicted in Figure 2, is designed to encode the multimodal features of each news article into a unified 𝑑-dimension news vector v𝑛.
図2に示すように、ニュースエンコーダは、各ニュース記事のマルチモーダルな特徴を統一された $d$ 次元のニュースベクトル $v_n$ にエンコードするように設計されている.
The user encoder, as shown in Figure 3a, is designed on the top of the news encoder, generating a unified 𝑑-dimension user vector v𝑢 from the sequence of browsed news vectors.
図3aに示すように、**ユーザエンコーダはニュースエンコーダの上に設計(はいはい確かに...基本的にはそう)**されており、閲覧されたニュースのベクトル列から統一された $d$ 次元のユーザベクトル $v_u$ を生成する。
Finally, the interaction modules in ranking models (such as DCN [39]) and matching models (such as NAML [43]) have some differences.
最後に、ランキングモデル(DCN [39]など)とマッチングモデル(NAML [43]など)の相互作用モジュールにはいくつかの違いがある.
For ranking models, the click-through probability is directly calculated based on the candidate news vector v𝑐 and the user vector v𝑢, which is a regression problem.
ランキングモデルの場合、クリックスルー確率はニュース候補ベクトル$v_c$とユーザーベクトル $v_u$ に基づいて直接計算されるが、これは回帰問題である.
In contrast, for matching models, the interaction module needs to identify the positive sample that best matches the user vector v𝑢 among multiple candidate news vectors V𝑐 = [v (1) 𝑐 , ..., v (𝑘+1) 𝑐 ] where 𝑘 is the number of negative samples, which is a classification problem.
対照的に、マッチング・モデルの場合、相互作用モジュールは、複数の候補ニュース・ベクトル $V_{c} = [v(1)_c, \cdots, v(k+1)_c]$ (kはネガティブ・サンプルの数)の中から、ユーザ・ベクトル $v_u$ に最もマッチするポジティブ・サンプルを特定する必要があり、これは分類問題である.
(最もシンプルなmatching modelが、ベクトル間の類似度で特定する方法なのかな.)

The design of the news encoder, user encoder, and interaction module varies across different news recommendation models.
ニュースエンコーダ、ユーザエンコーダ、インタラクションモジュールの設計は、ニュース推薦モデルによって異なる.

# 3. Proprsed Framework: GENRE ジャンル

## 3.1. Overview 概要

Figure 1 illustrate the our proposed GENRE framework for LLMpowered generative news recommendation, which consists of the following four steps.1) Prompting: create prompts or instructions to harness the capability of a LLM for data generation for diverse objectives.2) Generating: the LLM generates new knowledge and data based on the designed prompts.3) Updating: use the LLMgenerated data to update the current data for the next round of prompting and generation, which is optional.4) Training: leverage the LLM-generated data to train news recommendation models.
図1は、LLMを活用した生成的ニュース推薦のためのGENREフレームワークの提案であり、以下の4つのステップから構成される。

- 1）プロンプティング：多様な目的のためのデータ生成のためにLLMの能力を活用するプロンプトや指示を作成する。
- 2）ジェネレーティング：LLMは設計されたプロンプトに基づいて新しい知識とデータを生成する。
- 3）アップデーティング：LLMが生成したデータを使用して、次のプロンプティングと生成のラウンドのために現在のデータを更新する。

Prompt design forms the foundation of GENRE, and the iterative generation and updating mechanism allows for an expansive and complex design space.
プロンプト・デザインはGENREの基礎を形成し、反復的な生成と更新のメカニズムが広大で複雑なデザイン空間を可能にする。
In the following, we show examples of prompts designed under GENRE for news summarization, user profile modeling, and personalized news generation.
以下では、ニュースの要約、ユーザプロファイルのモデリング、およびパーソナライズされたニュースの生成のためにGENREの下で設計されたプロンプトの例を示す。

## 3.2. LLM as News Summarizer ニュース要約としてのLLM

Large language models are capable of summarizing news content into concise phrases or sentences, due to their training on vast amounts of natural language data and summarization tasks.
大規模な言語モデルは、膨大な量の自然言語データと要約タスクに対する学習により、ニュースコンテンツを簡潔なフレーズやセンテンスに要約することができる。
Moreover, large language models possess remarkable skills in comprehending text, allowing them to identify noun entities like the names of individuals and locations.
さらに、大規模な言語モデルは、テキストを理解する上で卓越したスキルを持っており、個人名や場所のような名詞エンティティを識別することができる。
These entities may have appeared infrequently in the original dataset, making it challenging to learn their representations.
これらのエンティティは、元のデータセットでは出現頻度が低く、その表現を学習することが困難である。
However, large language models can associate them more effectively with knowledge learned during pre-training.
しかし、大規模な言語モデルは、事前学習で学んだ知識をより効果的に関連付けることができる。

Therefore, we design a prompt for news title enhancement, as shown in Figure 4a.
そこで、図4aに示すように、ニュースのタイトルを強調するプロンプトをデザインする。
By providing the news title, abstract, and category as input, the large language model produces a more informative news title as output.
ニュースのタイトル、アブストラクト、カテゴリーを入力として提供することで、大規模言語モデルはより情報量の多いニュースのタイトルを出力として生成する。
As shown by the provided sample, the enhanced title not only summarizes the news information but also highlights the main topic of the news – “guide”, which is missing from the original title.
提供されたサンプルで示されているように、強化されたタイトルはニュース情報を要約するだけでなく、ニュースの主要なトピックである「ガイド」を強調している。

During the training of the recommendation model, the enhanced news title will replace the original title and be used as one of the input features, together with other multi-modal features, for the news encoder (Figure 2).
推薦モデルの学習中、**強化されたニュースタイトルは元のタイトルに置き換えられ**、他のマルチモーダル特徴とともに、ニュースエンコーダの入力特徴の1つとして使用される（図2）。
The green news vectors in Figure 3b represent the news vectors with the enhanced titles.
図3bの緑色のニュース・ベクトルは、タイトルが強調されたニュース・ベクトルである。

## 3.3. LLM as User Profiler ユーザー・プロファイラとしてのLLM

The user profile generally refers to their preferences and characteristics, such as age, gender, topics of interest, and geographic location.
ユーザープロファイルとは一般的に、年齢、性別、興味のある話題、地理的な場所など、ユーザーの嗜好や特徴を指す。
These explicit preferences often serve as important features for click-through rate (CTR) recommendation models.
このような明示的な嗜好は、クリックスルー率（CTR）推奨モデルの重要な特徴として機能することが多い。
However, these information are usually not provided in the anonymized dataset for training recommendation models, due to privacy policies.
しかし、推薦モデルを学習するための匿名化されたデータセットでは、プライバシーポリシーのため、これらの情報は通常提供されない。
Large language models are capable of understanding a user’s reading history through their ability to model long sequences, enabling them to analyze and create an outline of the user’s profile.
大規模な言語モデルは、**長いシーケンスをモデル化する能力**を通じて、ユーザの読書履歴を理解することができ、ユーザのプロファイルを分析し、概要を作成することができます。
Hence, we design a prompt for user profiles modeling, as depicted in Figure 4b.
そこで、図4bに示すように、ユーザープロファイルをモデリングするためのプロンプトをデザインする。
Given a user’s reading history, the large language model produces a user profile that includes his/her interested topics and regions.
**ユーザの読書履歴が与えられると、大規模な言語モデルは、そのユーザーが興味を持っているトピックや地域を含むユーザープロファイルを作成**する。
In this example, the LLM infers that the user may be interested in the region of Florida, based on the word “Miami” in the news.
この例では、LLMはニュースの中の「マイアミ」という単語から、ユーザーがフロリダという地域に興味があるのではないかと推測する。
Although “Miami” may have a low occurrence in the dataset, “Florida” is more frequently represented and therefore more likely to be connected to other news or users for collaborative filtering.
マイアミ」はデータセットでは出現率が低いかもしれないが、「フロリダ」はより頻繁に出現するため、協調フィルタリングのために他のニュースやユーザーと結び付けられる可能性が高い。
The summarized user profile will be fed into an interest fusion module which produces a interest vector v𝑖 (the pink vector in Figure 3c), defined by
要約されたユーザープロファイルはインタレスト・フュージョン・モジュールに供給され、インタレスト・ベクトルv𝑖（図3cのピンクのベクトル）を生成する。

$$
\tag{1}
$$

where POOL is the average pooling operation, Etopics and Eregions are the embedding matrices of the interested topics and regions, and [; ] is the vector concatenation operation.
ここで、POOLは平均プーリング演算、EtopicsとEregionsは関心のあるトピックと地域の埋め込み行列、[; ]はベクトル連結演算である。
The interest vector v𝑖 will be combined with the user vector v𝑢 (the blue vector in Figure 3c) learned by the user encoder to form the interest-aware user vector v𝑖𝑢 (the purple vector in Figure 3c) as follows:
関心ベクトルv𝑖は、ユーザエンコーダが学習したユーザベクトルv_46（図3cの青ベクトル）と結合され、以下のように関心対応ユーザベクトルv𝑖ᑢ（図3cの紫ベクトル）を形成する：

$$

\tag{2}
\tag{2}タグ


$$

where MLP is a multi-layer perceptron with ReLU activation.

## 3.4. LLM as Personalized News Generator

The cold-start problem, which is well-known for its difficulties, occurs when new users3 have limited interaction data, making it difficult for the user encoder to capture their characteristics and ultimately weakening its ability to model warm users 4 . Recent studies [7, 33] have shown that LLMs possess exceptional capabilities to learn from few examples. Hence, we propose to use an LLM to model the distribution of user-interested news given very limited user historical data. Specifically, we use it as a personalized news generator to generate synthetic news that may be of interest to new users, enhancing their historical interactions and allowing the user encoder to learn effective user representations. The prompt displayed in Figure 4c serves as a guide for the personalized news generator, allowing the LLM to create synthetic news pieces tailored to the user’s interests. The generated news pieces (indicated by the yellow news vectors in Figure 3d) are incorporated into the user historical sequence, which will be encoded and fed to the user encoder to generate the user vector.

## 3.5. Chain-based Generation

While we have shown several examples of “one-pass generation” (Figure 4) under our GENRE framework, it is worth noting that the design space of GENRE is vast and of a high-order complexity. As illustrated by the diagram in Figure 1, GENRE enables iterative generation and updating. The data generated by the LLM can be leveraged to enhance the quality of current data, which can subsequently be utilized in the next round of generation and prompting in an iterative fashion. We refer to this type of generation as “chainbased generation”, in contrast to “one-pass generation”. We design a chain-based personalized news generator by combining the one-pass user profiler and personalized news generator. As illustrated in Figure 5, we first use the LLM to generate the interested topics and regions of a user, which are then combined with the user history news list to prompt the LLM to generate synthetic news pieces. The user profile helps the LLM to engage in chain thinking, resulting in synthetic news that better matches the user’s interests than the one-pass generator. The prompt for the chain-based generator is provided in the supplementary materials.

## 3.6. Downstream Training

Our GENRE framework can be applied with any news recommendation model. Existing news recommendation models mainly include matching-based models such as NAML [43], LSTUR [1], NRMS [45], and PLMNR [46], and ranking-based deep CTR models, such as BST [4], DCN [39], PNN [26], and DIN [55]. Since ranking-based models directly calculate the click-through rate, they place greater emphasis on the design of multiple feature interactions, compared to the relatively straightforward design of the news encoder and user encoder (Table 2). These models are trained with the binary cross-entropy loss defined as:

$$

\tag{3}
\tag{3}タグ


$$

where 𝑧 is the batch size, 𝑦𝑖 is the label of the 𝑖-th sample (can be 0 or 1), and 𝑦ˆ𝑖 is the predicted probability of the 𝑖-th sample. In contrast, matching-based models concentrate on capturing semantic information from news features and user interests. Therefore, they prioritize the design of news encoder and user encoder and use a relatively simple interaction module (Table 2). These models are trained using the cross-entropy loss:

$$

\tag{4}
\4}タグ
$$
