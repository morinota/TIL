## refs 審判

<https://arxiv.org/html/2405.13007v1>
<https://arxiv.org/html/2405.13007v1>

## title タイトル

News Recommendation with Category Description by a Large Language Model
大規模言語モデルによるカテゴリ記述付きニュース推薦

## abstract 抄録

Personalized news recommendations are essential for online news platforms to assist users in discovering news articles that match their interests from a vast amount of online content.
パーソナライズされたニュースレコメンデーションは、オンラインニュースプラットフォームにとって、ユーザーが膨大なオンラインコンテンツから自分の興味に合ったニュース記事を発見するのを支援するために不可欠である。
Appropriately encoded content features, such as text, categories, and images, are essential for recommendations.
テキスト、カテゴリー、画像など、適切にエンコードされたコンテンツの特徴は、レコメンデーションに不可欠である。
Among these features, news categories, such as tv-golden-globe, finance-real-estate, and news-politics, play an important role in understanding news content, inspiring us to enhance the categories’ descriptions.
これらの特徴のうち、テレビ-ゴールデングローブ、金融-不動産、ニュース-政治などのニュースカテゴリは、ニュース内容を理解する上で重要な役割を果たしており、カテゴリの記述を強化するよう促している。
In this paper, we propose a novel method that automatically generates informative category descriptions using a large language model (LLM) without manual effort or domain-specific knowledge and incorporates them into recommendation models as additional information.
本稿では、大規模言語モデル(LLM)を用いて、人手やドメイン固有の知識なしに、有益なカテゴリ記述を自動生成し、付加情報として推薦モデルに組み込む新しい手法を提案する。
In our comprehensive experimental evaluations using the MIND dataset, our method successfully achieved 5.8% improvement at most in AUC compared with baseline approaches without the LLM’s generated category descriptions for the state-of-the-art content-based recommendation models including NAML, NRMS, and NPA.
MINDデータセットを用いた包括的な実験評価において、本手法は、NAML、NRMS、NPAを含む最先端のコンテンツベース推薦モデルにおいて、LLMが生成したカテゴリ記述を用いないベースラインアプローチと比較して、最大で5.8%のAUCの改善に成功した。
These results validate the effectiveness of our approach.
これらの結果は、我々のアプローチの有効性を証明するものである。
The code is available at <https://github.com/yamanalab/gpt-augmented-news-recommendation>.
コードは<https://github.com/yamanalab/gpt-augmented-news-recommendation>にある。

# Introduction はじめに

In recent years, online news platforms have gained widespread popularity, making it commonplace for users to consume news articles on their mobile devices.
近年、オンライン・ニュース・プラットフォームが広く普及し、ユーザーがモバイル端末でニュース記事を閲覧することが当たり前になった。
These platforms deliver a large amount of news content to users daily, leading to an information overload problem, making it challenging to discover articles that align with user’s interests.
これらのプラットフォームでは、毎日大量のニュースコンテンツがユーザーに配信されるため、情報過多の問題が生じ、ユーザーの関心に沿った記事を発見することが難しくなっている。
Therefore, personalized news recommendations have become essential for online news platforms.
そのため、パーソナライズされたニュース推薦がオンライン・ニュース・プラットフォームにとって不可欠となっている。

Many proposed news recommendation models use deep neural networks, which achieve high performance (lstur; nrecsurvey2023; naml; npa; nrms; nrecsurvey2021).
提案されているニュース推薦モデルの多くはディープニューラルネットワークを使用しており、高いパフォーマンスを達成している（lstur; nrecsurvey2023; naml; npa; nrms; nrecsurvey2021）。
As shown in Figure 1, most neural news recommendation models adopt a common approach that consists of three core modules:
図1に示すように、ほとんどのニューラル・ニュース推薦モデルは、3つのコア・モジュールからなる共通のアプローチを採用している：

(1) News encoder: it generates a news vector that captures the semantic information from the news content.
(1) ニュース・エンコーダ： ニュースの内容から意味情報を取り込んだニュースベクトルを生成する。

(2) User encoder: it generates a user vector that captures the user preferences based on browsing history.
(2) ユーザーエンコーダ： 閲覧履歴からユーザーの嗜好をとらえたユーザーベクトルを生成する。

(3) Similarity calculator: it computes the similarity score between the news vector and the user vector, estimating that news items with higher similarity scores are more likely to match the user’s interests.
(3) 類似度計算機： ニュース・ベクトルとユーザー・ベクトルの類似度スコアを計算し、類似度スコアが高いニュース・アイテムほどユーザーの興味にマッチする可能性が高いと推定する。

Previous studies have focused on investigating which neural network structures to apply in the user and news encoder modules, resulting in various proposed architectures for news recommendation models.
これまでの研究では、どのニューラルネットワーク構造をユーザーモジュールとニュースエンコーダーモジュールに適用するかを調査することに焦点が当てられており、その結果、ニュース推薦モデルのためのさまざまなアーキテクチャが提案されている。
Recent methods incorporate pre-trained language models (PLMs) into the news encoder to learn news representations.
最近の手法では、ニュース表現を学習するために、事前に訓練された言語モデル（PLM）をニュースエンコーダに組み込んでいる。
These PLM-based approaches have achieved high performance (once; nrecsurvey2023; reduceCross; nrecsurvey2021; plmnr).
これらのPLMベースのアプローチは、高いパフォーマンスを達成している（once; nrecsurvey2023; reduceCross; nrecsurvey2021; plmnr）。

Simultaneously, a crucial source for understanding news content is the news category.
同時に、ニュースの内容を理解するための重要な情報源は、ニュースのカテゴリーである。
For example, the MIND (mind) dataset, a well-known dataset in the news recommendation field, contains news categories such as tv-golden-globes.
例えば、ニュース推薦分野で有名なデータセットであるMIND（マインド）データセットには、tv-golden-globesのようなニュースカテゴリーが含まれている。
The naïve way to use categories in recommendation models is to adopt predefined templates (e.g., The news category is {category}) followed by combining them with original news recommendation models.
推薦モデルにカテゴリーを使用するナイーブな方法は、あらかじめ定義されたテンプレート（例えば、ニュースのカテゴリーは{category}である）を採用し、オリジナルのニュース推薦モデルと組み合わせることである。
However, these templates are too generic to be applied to all news categories, resulting in insufficient information.
しかし、これらのテンプレートは、すべてのニュースカテゴリーに適用するには汎用性が高すぎるため、情報量が不十分となる。
Constructing detailed descriptions for each news category and using them as input can be beneficial for enabling recommendation models to recognize news content accurately.
ニュースカテゴリーごとに詳細な説明を構築し、それを入力として利用することは、推薦モデルがニュースコンテンツを正確に認識するために有益である。

However, manually constructing detailed descriptions for each news category is costly.
しかし、ニュースのカテゴリーごとに詳細な説明を手作業で作成するのはコストがかかる。
To address this issue, we propose automatically generating descriptive text for news categories using large language models (LLMs).
この問題に対処するために、我々は大規模言語モデル（LLM）を用いてニュースカテゴリーの説明テキストを自動生成することを提案する。
Since LLMs are pre-trained on vast amounts of text data and have extensive knowledge across diverse topics, the LLM-generated detailed descriptions are expected to enhance the recommendation performance.
LLMは膨大なテキストデータに対して事前に訓練されており、多様なトピックにわたる幅広い知識を持っているため、LLMが生成する詳細な説明は推薦性能を高めることが期待される。
The contributions of this paper are as follows:
本稿の貢献は以下の通りである：

(1) We first propose the adoptation of LLM-generated news category descriptions to enhance news recommendations.
(1)まず、LLMによって生成されたニュースカテゴリ記述の採用を提案し、ニュース推薦を強化する。

(2) Comprehensive experimental evaluations on the MIND dataset confirmed that our proposed method consistently outperforms baseline approaches across multiple recommendation models, achieving up to 5.8% improvement in AUC compared to methods without category descriptions.
(2)MINDデータセットを用いた包括的な実験評価により、提案手法は複数の推薦モデルにおいてベースラインアプローチを一貫して上回り、カテゴリー記述を行わない手法と比較してAUCで最大5.8%の改善を達成することが確認された。

The rest of this paper is organized as follows.
本稿の残りの部分は以下のように構成されている。
In Section 2, we reviews state-of-the-art news recommendations and use of LLM-generated text.
セクション2では、最新のニュース推薦とLLM生成テキストの使用についてレビューする。
We propose a new recommendation method enhanced by an LLM in Section 3, followed by evaluations in Section 4.
セクション3では、LLMによって強化された新しい推薦手法を提案し、セクション4ではその評価を行う。
In Section 5, we discuss the limitations of the proposed method.
セクション5では、提案手法の限界について述べる。
Finally, In Section 6, we conclude this paper.
最後に、セクション6で本稿を締めくくる。

# Related Work 関連作品

2.Related Work
2.関連作品

In this section, we review related work on news recommendations and the use of LLM-generated text.
このセクションでは、ニュース推薦とLLM生成テキストの使用に関する関連研究をレビューする。

2.1.News Recommendations
2.1.ニュース推薦

News recommendations have been extensively studied through various models (nrecsurvey2023; nrecsurvey2021).
ニュースの推奨は、さまざまなモデルによって広く研究されている（nrecsurvey2023; nrecsurvey2021）。
Neural network-based models have achieved state-of-the-art performance by encoding news content and user preferences to capture the complex interactions between users and news items (lstur; mccm; naml; npa; nrms).
ニューラルネットワークベースのモデルは、ニュースの内容とユーザーの嗜好を符号化し、ユーザーとニュース項目の間の複雑な相互作用を捉えることで、最先端の性能を達成している（LSTUR; MCCM; NAML; NPA; NRMS）。
For instance, NRMS (nrms) employs multi-head attention to acquire news and user vectors, while LSTUR (lstur) adopts GRU for to obtain user vectors.
例えば、NRMS(nrms)はニュースとユーザーベクトルを取得するためにマルチヘッドアテンションを採用し、LSTUR(lstur)はユーザーベクトルを取得するためにGRUを採用している。
Other models, such as MCCM (mccm), NAML (naml), and NPA (npa), leverage CNN and attention mechanisms to generate user and news vectors.
MCCM（mccm）、NAML（naml）、NPA（npa）などの他のモデルは、CNNとアテンション・メカニズムを活用して、ユーザーとニュースのベクトルを生成する。

Particularly, the models adopting PLMs, such as BERT (bert) and RoBERTa (roberta), to obtain news vectors have achieved notably high performance (once; nrecsurvey2023; reduceCross; nrecsurvey2021; plmnr; mmrec).
特に、ニュースベクトルを得るためにBERT（bert）やRoBERTa（roberta）などのPLMを採用したモデルは、顕著に高いパフォーマンスを達成している（once; nrecsurvey2023; reduceCross; nrecsurvey2021; plmnr; mmrec）。
For instance, Wu et al.(plmnr) proposed a framework incorporating PLMs into news recommendations, demonstrating 2.63% improvement in the pageview rate through online experiments.
例えば、Wuら(plmnr)は、ニュースのレコメンデーションにPLMを組み込んだフレームワークを提案し、オンライン実験によってページビュー率が2.63%向上したことを実証している。
In the ONCE (once), proposed by Liu et al., showed that using large-scale language models such as LLaMa (llama) can improve news recommendation performance.
Liuらによって提案されたONCE（一度）では、LLaMa（ラマ）のような大規模な言語モデルを使用することで、ニュース推薦のパフォーマンスを改善できることが示された。

Several neural recommendation models use different architectures from the model shown in Figure 1.
いくつかのニューラル推薦モデルは、図1に示したモデルとは異なるアーキテクチャを使用している。
For instance, Zhang et al.introduced UNBERT (unbert), which feeds a candidate news article and a list of previously viewed news articles into a single language model to predict click-through rates.
例えば、Zhangらは、クリックスルー率を予測するために、候補のニュース記事と以前に閲覧されたニュース記事のリストを単一の言語モデルにフィードするUNBERT（アンバート）を紹介した。
Another notable work by Zhang et al.(prompt4nr) is Prompt4NR, a news recommendation approach using prompt learning with PLMs.
Zhangら(prompt4nr)によるもう一つの注目すべき研究は、PLMを用いたプロンプト学習を用いたニュース推薦アプローチであるPrompt4NRである。

In summary, various methods with neural network-based models have been proposed for news recommendation.
まとめると、ニュースの推薦にはニューラルネットワークベースのモデルを用いた様々な手法が提案されている。
The use of PLMs shows particularly high performance; however, PLMs lack sufficient knowledge to interpret category names.
PLMの使用は特に高いパフォーマンスを示しているが、PLMはカテゴリー名を解釈するのに十分な知識がない。
Thus, a space exists to enhance the performance of news recommendations by adding detailed category information, which inspires us to adopt LLM-generated category descriptions as additional features.
このように、詳細なカテゴリー情報を追加することによって、ニュース推薦のパフォーマンスを向上させるスペースが存在するため、LLMによって生成されたカテゴリー記述を追加特徴として採用することになった。

2.2.Use of LLM-Generated Texts
2.2.LLMが作成したテキストの利用

The use of text generated by LLMs, which have acquired extensive knowledge on a wide range of topics through pre-training, has improved the performance in various natural language processing tasks, such as text classification and question answering (qagen; cupl; gpt3mix).
事前学習によって幅広いトピックに関する知識を獲得したLLMによって生成されたテキストを使用することで、テキスト分類や質問応答（qagen; cupl; gpt3mix）などの様々な自然言語処理タスクの性能が向上している。

Yoo et al.(gpt3mix) proposed GPT3Mix, which applies GPT-3-based (gpt3) data augmentation to text classification tasks by generating additional training examples.
Yooら(gpt3mix)はGPT3Mixを提案した。GPT3MixはGPT-3ベース(gpt3)のデータ拡張をテキスト分類タスクに適用するもので、追加の学習例を生成する。
For question answering tasks, Liu et al.(qagen) used knowledge expansion using GPT-3 to augment the context and improve the performance of the question answering model.
Liuら（qagen）は、質問応答タスクのために、GPT-3を用いた知識拡張を用いてコンテキストを補強し、質問応答モデルの性能を向上させた。
Pratt et al.(cupl) introduced CuPL, a method that leverages image captions generated by LLMs for zero-shot image classification using CLIP (clip).
Prattら(cupl)は、CLIP(clip)を用いたゼロショット画像分類のために、LLMによって生成された画像キャプションを活用する手法であるCuPLを紹介した。
They automatically generated image captions using LLMs and used them as text inputs for CLIP.
彼らはLLMを使って画像のキャプションを自動生成し、CLIPのテキスト入力として使用した。

These studies demonstrated the effectiveness of utilizing texts generated by LLMs in various tasks.
これらの研究は、LLMによって生成されたテキストを様々なタスクに活用することの有効性を実証した。
Inspired by this, we aims to improve news recommendation performance by generating news category descriptions using LLMs.
そこで、LLMを用いてニュースのカテゴリ記述を生成することで、ニュースの推薦性能を向上させることを目指す。

# Proposed Method 提案された方法

Figure 2 shows our proposed novel news recommendation method enhanced by LLM-generated category descriptions, consisting of two steps: 1) automatic generation of news category descriptions, and 2) integration of the generated category descriptions with the recommendation model as additional input features.
図2は、LLMによって生成されたカテゴリ記述によって強化された新しいニュース推薦方法を示している： 1)ニュースカテゴリ記述の自動生成、2)生成されたカテゴリ記述を推薦モデルに追加入力特徴として統合する。

## Generation of Category Descriptions カテゴリー記述の生成

In this step, we generate the descriptions for news categories using an LLM without any manual effort.
このステップでは、人手をかけずにLLMを使ってニュースカテゴリーの記述を生成する。
We employ GPT-4 (gpt4) as the LLM for generating category descriptions, as it has demonstrated high performance across various domains and tasks (sparkGpt4).
カテゴリ記述生成のためのLLMとして、様々なドメインやタスクで高い性能を発揮しているGPT-4（gpt4）を採用する（sparkGpt4）。

Figure 3 shows the prompts for the LLM to generate descriptions for news categories.
図3は、LLMがニュース・カテゴリの説明を生成するためのプロンプトを示している。
Although the prompts need to be prepared manually, they do not require any manual effort once they have been prepared.
プロンプトは手作業で準備する必要があるが、一度準備してしまえば手作業は必要ない。

Figure 4 shows a specific example of the generated news category descriptions for the tv-golden-globes category, one of the categories that appeared in the MIND dataset (mind).
図4は、MINDデータセット（mind）に現れたカテゴリの1つであるtv-golden-globesカテゴリについて、生成されたニュースカテゴリの記述の具体例を示している。
The average word count of the generated category descriptions is 57.7 for all 270 news categories within the MIND dataset used in our experiment.
生成されたカテゴリー説明文の平均単語数は、実験に使用したMINDデータセット内の270のニュースカテゴリーすべてについて57.7である。

## Integration of Category Descriptions into News Recommendation Models ニュース推薦モデルへのカテゴリー記述の統合

After generating the category descriptions, we train the news recommendation model by leveraging the generated descriptions.
カテゴリの説明文を生成した後、生成された説明文を活用してニュース推薦モデルを学習する。
Let D t ⁢ i ⁢ t ⁢ l ⁢ e denote the news title text and D d ⁢ e ⁢ s ⁢ c represent the generated category description.
D t i t l e をニュースのタイトルテキスト、D d e s c を生成されたカテゴリの説明を表すとする。
During the inference phase of the recommendation model, we concatenate D t ⁢ i ⁢ t ⁢ l ⁢ e and D d ⁢ e ⁢ s ⁢ c using the special SEP token from BERT (bert), and feed the resulting text into the news encoder
推薦モデルの推論段階では、BERTの特別なSEPトークン（bert）を使用してD t i t l eとD d e s cを連結し、結果のテキストをニュースエンコーダに入力する。

# Experiments and Results 実験と結果

In this section, we describe our experiments.
このセクションでは、私たちの実験について説明する。
First, we present the dataset, evaluation metrics, baselines, and hyperparameters used in our experiments.
まず、データセット、評価指標、ベースライン、実験に使用したハイパーパラメータを示す。
Second, we present the results and then discuss the effectiveness of the proposed method.
次に、結果を示し、提案手法の有効性について議論する。

## Experimental Setting 実験設定

We used the MIND (mind) dataset, a widely used dataset for the news recommendation field.
ニュース推薦の分野で広く使われているMIND（マインド）データセットを使用した。
The MIND dataset, whose statistics are shown in Table 1, was constructed from the news click records of the Microsoft News1 service between October 12, 2019 and November 22, 2019.
表1に統計情報を示すMINDデータセットは、2019年10月12日から2019年11月22日までのMicrosoft News1サービスのニュースクリックレコードから構築された。

To evaluate the effectiveness of our proposed method, we adopted three state-of-the-art content-based recommendation models: NAML (naml), NRMS (nrms), and NPA (npa).
提案手法の有効性を評価するために、3つの最先端のコンテンツベース・レコメンデーション・モデルを採用した： NAML（naml）、NRMS（nrms）、NPA（npa）である。
We used the pre-trained models DistilBERT-base (distilbert-base-uncased) (distilbert) and BERT-base (bert-base-uncased) (bert) for the news encoder component.
ニュースエンコーダーコンポーネントには、事前に訓練されたモデルDistilBERT-base（distilbert-base-uncased）（distilbert）とBERT-base（bert-base-uncased）（bert）を使用した。
AdamW (adamw) was used as the optimization function with a learning rate of 1e-4, a batch size of 128, and 3 epochs.
AdamW（adamw）を最適化関数として使用し、学習率は1e-4、バッチサイズは128、エポックは3回とした。
Following the previous studies (mccm; npa; plmnr; prompt4nr), the maximum number of recently viewed articles, which was used to capture user preference information, was set to 50.
先行研究(mccm; npa; plmnr; prompt4nr)に従い、ユーザーの嗜好情報を取得するために使用される最近閲覧した記事の最大数は50に設定された。
We set the number of negative samples in the training phase to 4.
トレーニング段階での負サンプル数は4とした。
All experiments are conducted on a Tesla V100 GPU.
実験はすべてTesla V100 GPUで行った。
For implementation, we used PyTorch v2.1.0 (pytorch) and Transformers v4.35.0 (transformers) libraries.
実装にはPyTorch v2.1.0(pytorch)とTransformers v4.35.0(transformers)のライブラリを使用しました。
As performance metrics, we used the average AUC, MRR, nDCG@5, and nDCG@10 for all impressions.
パフォーマンス指標として、すべてのインプレッションの平均AUC、MRR、NDCG@5、NDCG@10を使用した。

## Results 結果

Table 2 summarizes the comparison of our proposed recommendation method with the baselines.
表2は、我々の提案する推薦方法とベースラインとの比較をまとめたものである。
The proposed method, title+generated-description, demonstrates the highest performance compared with the baselines across all recommendation models and achieved up to 5.6% and 5.8% improvements in AUC compared with the title only and title+template-based baselines, respectively.
提案手法であるtitle+generated-descriptionは、全ての推薦モデルにおいてベースラインと比較して最も高い性能を示し、titleのみ、title+テンプレートベースのベースラインと比較して、それぞれ最大5.6%、5.8%のAUCの改善を達成した。

Furthermore, title + template-based shows insignificant improvement in performance compared with the title only in most cases.
さらに、タイトル＋テンプレートベースは、ほとんどの場合、タイトルのみと比較して、パフォーマンスの向上はわずかである。
This result suggests that simply fitting the category name into a predefined template is ineffective for representing the category information.
この結果は、カテゴリー名をあらかじめ定義されたテンプレートに当てはめるだけでは、カテゴリー情報を表現するのに有効でないことを示唆している。
The results also indicate that for relatively small-scale language models like BERT, using only the category names as input does not provide sufficient information for the recommendation models to properly interpret the category information.
また、BERT のような比較的小規模な言語モデルの場合、カテゴリ名のみを入力として使用することは、推薦 モデルがカテゴリ情報を適切に解釈するために十分な情報を提供しないことを示している。

# Limitations 制限事項

To explore the limitations, we performed a manual inspection of the category descriptions.
限界を探るため、カテゴリーの説明を手作業で検査した。
Although GPT-4 generally produces high-quality descriptions, it occasionally fails to generate accurate descriptions.
GPT-4は一般的に高品質な記述を生成するが、時折正確な記述を生成できないことがある。

Figure 5 shows an example in which the generated description for the tunedin category focuses on entertainment, music, and television.
図5は、チューニングカテゴリの生成された説明が、エンターテインメント、音楽、テレビに焦点を当てている例を示している。
However, the actual article titles in Table 3 reflect a wider range of to"pics, including technology and trends.
しかし、表3の実際の記事タイトルは、技術やトレンドなど、より幅広い 「写真 」を反映している。
A more accurate description would be that the tunedin category casually provides news on various topics such as entertainment, technology, and business, keeping readers updated on the latest trends.
より正確には、エンターテインメント、テクノロジー、ビジネスなど、さまざまなトピックのニュースをさりげなく提供し、読者に最新のトレンドを伝えるのが「チューンドイン」カテゴリーだ。
This discrepancy highlights the model’s inability to accurately capture the category’s broad scope.
この食い違いは、このカテゴリーが持つ広範な範囲を正確に捉えることができないというモデルの欠点を浮き彫りにしている。

This example, along with other similar instances, suggests that the model may struggle to generate accurate category descriptions when the input lacks sufficient background knowledge or context.
この例は、他の同様の例とともに、入力に十分な背景知識や文脈がない場合、モデルが正確なカテゴリー記述を生成するのに苦労する可能性があることを示唆している。

# Conclusion 結論

In this study, we proposed a method to automatically generate news category descriptions using LLMs and incorporate them into news recommendation models.
本研究では、LLMを用いてニュースカテゴリ記述を自動生成し、ニュース推薦モデルに組み込む手法を提案した。
The experiments on the MIND dataset demonstrated that our method outperformed the baselines across all metrics for multiple models.
MINDデータセットでの実験では、我々の手法が、複数のモデルにおいて、全てのメトリクスでベースラインを上回ることが実証された。
Our main contribution is a novel approach to enhance news recommendation models’ understanding of category information using LLMs.
我々の主な貢献は、LLMを用いてニュース推薦モデルのカテゴリー情報の理解を強化する新しいアプローチである。
Our future work will include enhancing the recommendation performance by improving the generated descriptions.
今後の課題としては、生成された記述を改良することにより、推薦性能を向上させることである。