## refs: refs：

- https://medium.com/airbnb-engineering/airbnb-brandometer-powering-brand-perception-measurement-on-social-media-data-with-ai-c83019408051

# Airbnb Brandometer: Powering Brand Perception Measurement on Social Media Data with AI Airbnb Brandometer： AIでソーシャルメディアデータを活用したブランド認知度測定を強化

How we quantify brand perceptions from social media platforms through deep learning
ディープラーニングによってソーシャルメディア・プラットフォームからブランド認知を定量化する方法

## Introduction

At Airbnb, we have developed Brandometer, a state-of-the-art natural language understanding (NLU) technique for understanding brand perception based on social media data.
Airbnbでは、ソーシャルメディアデータに基づいてブランド認知を理解するための最先端の自然言語理解(natural language understanding, NLU)技術であるBrandometerを開発しています。

Brand perception refers to the general feelings and experiences of customers with a company.
**Brand perception(ブランド認知)**とは、顧客が企業との一般的な感情や経験を指す。
Quantitatively, measuring brand perception is an extremely challenging task.
定量的にブランド認知を測定することは、極めて困難な作業である。
Traditionally, we rely on customer surveys to find out what customers think about a company.
従来、私たちは、顧客が企業についてどう考えているかを知るために、顧客調査に頼ってきた。(ex. ユーザインタビュー的な??)
The downsides of such a qualitative study is the bias in sampling and the limitation in data scale.
このような質的研究の欠点は、サンプリングのバイアスとデータ規模の制限である。
Social media data, on the other hand, is the largest consumer database where users share their experiences and is the ideal complementary consumer data to capture brand perceptions.
一方、ソーシャルメディアデータは、ユーザーが自分の経験を共有する最大の消費者データベースであり、ブランド認知を捉えるための理想的な補完的消費者データである。

Compared to traditional approaches to extract concurrency and count-based top relevant topics, Brandometer learns word embeddings and utilizes embedding distances to measure relatedness of brand perceptions (e.g., ‘belonging’, ‘connected’, ‘reliable’).
Brandometerは、concurrency(共起性)とcount-based(カウントベース)のトップ関連トピックを抽出する従来のアプローチと比較して、**単語埋め込みを学習し、埋め込み距離を利用してブランド認知（例：「belonging」、「connected」、「reliable」）の関連性を測定する**。
Word embedding represents words in the form of real-valued vectors, and it performs well in reserving semantic meanings and relatedness of words.
単語埋め込みは、実数値ベクトルの形式で単語を表し、単語の意味と関連性を保持するのに優れている。
Word embeddings obtained from deep neural networks are arguably the most popular and evolutionary approaches in NLU.
**ディープ・ニューラル・ネットワークから得られる単語埋め込みは、NLUにおいて最も人気があり進化的なアプローチの一つと言える。**(人気あるよね...!)
We explored a variety of word embedding models, from quintessential algorithms Word2Vec and FastText, to the latest language model DeBERTa, and compared them in terms of generating reliable brand perception scores.
私たちは、Word2VecやFastTextといった典型的なアルゴリズムから最新の言語モデルDeBERTaまで、**さまざまな単語埋め込みモデルを探求し、信頼性の高いブランド認知スコアを生成する点で比較した**。

For concepts represented as words, we use similarity between its embedding and that of “Airbnb” to measure how important the concept is with respect to the Airbnb brand, which is named as Perception Score.
単語で表される概念たちについて、**その埋め込みと「Airbnb」の埋め込みとの類似性を使用**して、各概念がAirbnbブランドにとってどれだけ重要かを測定し、これを**Perception Score**と呼ぶ。(固有名詞「Airbnb」の埋め込みを使うってことは、SNSの色んなテキストを学習させる必要がありそう...??)
Brand Perception is defined as Cosine Similarity between Airbnb and the specific keyword:
ブランド認知は、Airbnbと特定のキーワードのコサイン類似度として定義される：

$$
A(irbnb) \cdot K(eyword) = |A| \cdot |K| \cdot \cos(\theta)
$$

where
ここで、

$$
\cos(\theta) = \frac{A \cdot K}{|A| \cdot |K|}
= \frac{\sum_{i=1}^{n} A_i \cdot K_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \cdot \sqrt{\sum_{i=1}^{n} K_i^2}}
$$

In this blog post, we will introduce how we process and understand social media data, capture brand perceptions via deep learning and how to ‘convert’ the cosine similarities to calibrated Brandometer metrics.
**このブログポストでは、私たちがどのようにソーシャルメディアデータを処理し、理解し、ディープラーニングによってブランド認知を捉え、コサイン類似度を校正されたブランドメトリクスに「変換」するかを紹介**します。
We will also share the insights derived from Brandometer metrics.
また、Brandometerの指標から得られた洞察も共有します。

## Brandometer Methodology

### Problem Setup and Data 問題の設定とデータ

In order to measure brand perception on social media, we assessedall Airbnb related mentions from 19 platforms (e.g., X — formerly known as Twitter, Facebook, Reddit, etc) and generated word embeddings with state-of-the-art models.
ソーシャルメディア上のブランド認知を測定するために、私たちは**19のプラットフォーム（例：X — 以前はTwitterとして知られていたもの、Facebook、Redditなど）からすべてのAirbnb関連の言及を評価し、最先端のモデルで単語埋め込みを生成**した。
(やっぱり! 単に学習済みモデルで単語埋め込みを使うだけじゃなく、ソーシャルメディアのテキストデータを学習させているよね...!)

In order to use Social media data to generate meaningful word embeddings for the purpose of measuring brand perception, we conquered two challenges:
ソーシャルメディアデータを使って、**ブランド認知を測定する目的で意味のある単語埋め込みを生成するため**に、2つの課題に取り組んだ：

- Quality: Social media posts are mostly user-generated with varying content such as status sharing and reviews, and can be very noisy.
  質： ソーシャルメディアの投稿は、ステータスの共有やレビューなど、さまざまなコンテンツを含むユーザ生成のものがほとんどであり、非常にノイズが多い場合がある。
- Quantity: Social media post sparsity is another challenge.
  量： ソーシャルメディアの投稿がまばらであることも課題である。
  Considering that it typically requires some time for social media users to generate data in response to certain activities and events, a monthly rolling window maintains a good balance of promptness and detectability.
  ソーシャルメディアユーザが特定の活動や出来事に反応してデータを生成するには、通常ある程度の時間が必要であることを考慮すると、毎月のローリングウィンドウは、迅速性と検出可能性の良いバランスを維持する。
  Our monthly dataset is relatively small (around 20 million words) as compared to a typical dataset used to train good quality word embeddings (e.g., about 100 billion words for Google News Word2Vec model).
  **私たちの月次データセットは、良質な単語埋め込みを学習するために使われる典型的なデータセット（例えば、Google News Word2Vecモデルでは約1000億語）に比べて比較的小さい(約2000万語)**。
  Warm-start from pre-trained models didn’t help since the in-domain data barely moved the learned embeddings.
  **事前学習済みモデルからのウォームスタートは助けにならなかった。なぜなら、ドメイン内データが学習された埋め込みをほとんど動かさなかったからだ。**(なるほど、0->1で言語モデルを学習させる必要があったってことか...! fine-tuningしても、学習済みモデルの埋め込みが変わらないってことかな...?:thinking_face:)

We developed multiple data cleaning processes to improve data quality.
データ品質を向上させるため、複数のデータクリーニングプロセスを開発した。
At the same time, we innovated the modeling techniques to mitigate the impact on word embedding quality due to data quantity and quality.
同時に、データの量と品質による単語埋め込み品質への影響を緩和するためのモデリング技術を革新した。

In addition to data, we explored and compared multiple word embedding training techniques with the goal to generate reliable brand perception scores.
データだけでなく、信頼性の高いブランド認知スコアを生成することを目的として、複数の単語埋め込みトレーニング技術を探求し、比較した。

### Word2Vec ワード2ベック

Word2Vec is by far the simplest and most widely used word embedding model since 2013.
Word2Vecは、2013年以降、**圧倒的にシンプルで最も広く使われている単語埋め込みモデル**だ。
We started with building CBOW-based Word2Vec models using Gensim.
私たちはまず、Gensimを使ってCBOWベースのWord2Vecモデルを構築した。
Word2Vec produced decent in-domain word embeddings, and more importantly, the concept of analogies.
Word2Vecは**適切なin-domain word embeddings(ドメイン内 単語埋め込み)を生成**し、さらに、**アナロジーの概念**を生み出した。(analogy = ある事柄をもとに他の事柄を類推すること...!:thinking:)
In our domain-specific word embeddings, we are able to capture analogies in the Airbnb domain, such as “host” — “provide” + “guest” ~= “need”, “city” — “mall” + “nature” ~= “park”.
ドメイン固有の単語埋め込みでは、「ホスト」 — 「提供」 + 「ゲスト」 ≈ 「必要」、「都市」 — 「モール」 + 「自然」 ≈ 「公園」など、**Airbnbドメインのアナロジーを捉えることができる**。

### FastText ファストテキスト

FastText takes into account the internal structure of words, and is more robust to out-of-vocabulary words and smaller datasets.
FastTextは単語の内部構造を考慮し、語彙のない単語やデータセットの規模が小さい場合により強くなります。
Moreover, as inspired by Sense2Vec, we associate words with sentiments (i.e., POSITIVE, NEGATIVE, NEUTRAL), which forms brand perception concepts on the sentiment levels.
さらに、Sense2Vecにインスパイアされるように、単語をsentiments（POSITIVE、NEGATIVE、NEUTRAL）と関連付け、これにより**感情レベルでのブランド認知概念**が形成される。

### DeBERTa デバート

Recent progress in transformer-based language models (e.g., BERT) has significantly improved the performance of NLU tasks with the advantage of generating contextualized word embeddings.
Transformerベースの言語モデル（例：BERT）の最近の進歩は、**コンテキストを生成する利点を持つ単語埋め込みを生成することで、NLUタスクのパフォーマンスを大幅に向上させた**。
We developed DeBERTa based word embeddings, which works better with smaller dataset and pays more attention to surrounding context via disentangled attention mechanisms.
我々はDeBERTaに基づく単語埋め込みを開発した。これは、より少ないデータセットでより良く機能し、分離されたattentionメカニズムを介して周囲のコンテキストにより多くのattentionを払う。
We trained everything from scratch (including tokenizer) using Transformers, and the concatenated last attention layer embeddings resulted in the best word embeddings for our case.
私たちはTransformersを使って（トークナイザーを含む）**すべてをゼロから学習し**、最後のattentionレイヤー埋め込みを連結した結果、私たちのケースに最適な単語埋め込みが得られた。

<!-- ここまで読んだ! -->

### Brand Perception Score Stabilization and Calibration ブランド知覚スコアの安定化と校正

The variability of word embeddings has been widely studied (Borah, 2021).
**単語埋め込みのばらつき**は広く研究されている（Borah, 2021）。
The causes range from the underlying stochastic nature of deep learning models (e.g., random initialization of word embeddings, embedding training which leads to local optimum for global optimization criteria) to the quantity and quality changes of data corpus across time.
その原因は、ディープラーニング・モデルの根底にある確率的な性質（例：単語埋め込みのランダム初期化、ローカル最適解に導く埋め込みトレーニング、グローバル最適化基準）から、時間の経過に伴うデータコーパスの量と品質の変化まで多岐にわたる。

With Brandometer, we need to reduce the variability in embedding distances to generate stable time series tracking.
ブランドメーターでは、安定した時系列追跡を行うために、埋め込み距離のばらつきを抑える必要があります。
Stable embedding distances helped preserve the inherent patterns and structures present in the time series data, and hence it contributes to better predictability of the tracking process.
安定した埋め込み距離は、時系列データに存在する固有のパターンと構造を保持するのに役立ち、その結果、追跡プロセスの予測性が向上します。
Additionally, it made the tracking process more robust to noisy fluctuations.
さらに、トラッキング・プロセスがノイズの多い変動に対してよりロバストになった。
We studied the influential factors and took the following steps to reduce:
私たちはその影響要因を調査し、以下のような削減策を講じた：

1. Score averaging over repetitive training with bootstrap sampling
   ブートストラップサンプリングによる反復トレーニングのスコア平均化
2. Rank-based perception score
   順位ベースのperceptionスコア

#### Score averaging over repetitive training with upsampling アップサンプリングによる反復トレーニングのスコア平均化

For each month’s data, we trained N models with the same hyper-parameters, and took the average of N perception scores as the final score for each concept.
各月のデータについて、同じハイパーパラメータで $N$ モデルをトレーニングし、各概念の最終スコアとして $N$ のperceptionスコアの平均を取った。
Meanwhile, we did upsampling to make sure that each model iterated on an equal number of data points across months.
その一方で、各モデルが月をまたいで同数のデータポイントを反復するように、アップサンプリングを行った。

We defined variability as:
変動性を次のように定義した：

$$
Variability(A, M, V) = S(A, M, V|N) - S(A, M, V|N-1)
$$

where
ここで、

$$
S(A, M, V|n) = \sum_{w \in V} \frac{\sum_{i=1}^{n} CosSim(w)}{n} / |V|
$$

CosSim(w) refers to the cosine similarity based perception score defined in Eq.1, A refers to the algorithm, M refers to the time window (i.e.month), V refers to the vocabulary and |V| is the vocabulary size, and n refers to the number of repetitively trained models.
$CosSim(w)$は、式1で定義されたコサイン類似度に基づく知覚スコアを指し、$A$はアルゴリズム、$M$ は時間ウィンドウ（つまり月）、$V$ は語彙を指し、$|V|$ は語彙のサイズを指し、$n$は反復的にトレーニングされたモデルの数を指す。

As N approaches 30, the score variability values converge and settle within a narrow interval.
Nが30に近づくにつれ、スコアの変動値は収束し、狭い間隔に収まる。
Hence, we picked N = 30 for all.
したがって、N＝30とした。

#### Rank-based perception score 順位ベースの知覚スコア

Based on Maria Antoniak’s work, we used the overlap between nearest neighbors to measure the stability of word embeddings, since the relative distances matter more than the absolute distance values in downstream tasks.
Maria Antoniakの研究に基づき、**下流のタスクでは絶対的な距離値よりも相対的な距離の方が重要であるため**、単語埋込みの安定性を測定するために最近傍同士の重なりを使用した。
Therefore, we also developed rank-based scores, which shows greater stability as compared to similarity-based scores.
そこで、**類似度ベースのスコアと比較して安定性の高いランクベースのスコア**も開発した。

For each word, we first ranked them in descending order of cosine similarity via Eq.1.The rank-based similarity score is then computed as 1/rank(w) where w∈V.
各単語について、まず式.1によってコサイン類似度の降順にランク付けした。ランクに基づく類似度スコアは、$w \in V$ であるとき $1/rank(w)$ として計算される。
More relevant concepts will have higher rank-based perception scores.
より関連性の高い概念は、ランクベースの知覚スコアが高くなる。

The score variability is defined the same as Variability(A, M, V) in Eq.2 except that
スコアのばらつきは、式2の Variability(A, M, V)と同様に定義される。

$$
S(A, M, V|n) = \sum_{w \in V} \frac{\sum_{i=1}^{n} RankSim(w)}{n} / |V|
$$

where RankSim(w) refers to the rank based perception score.
ここで、RankSim(w)はランクに基づく知覚スコアを指す。
With rank-based scores, when N approaches to 30, the score variability values converge to a much narrower interval especially for DeBERTa.
ランク・ベースのスコアでは、Nが30に近づくと、スコアの変動値は、特にDeBERTaではかなり狭い区間に収束する。

### Selection of Score Output by Designed Metrics 設計された指標による得点出力の選択

One challenge of this project was that we didn’t have a simple and ultimate way to conclude which score output was better since there is no objective ‘truth’ of brand perception.
**ブランド認知には客観的な"truth" (=正解?) がないため、どのスコア出力がより良いかを簡単に結論付ける方法がないという課題があった**。(うんうん...!)
Instead, we defined a new metric to learn some characteristics of the score.
その代わりに、スコアの特徴を知るための新しい指標を定義した。

#### Average Variance Across Different Period (AVADP) 異なる期間における平均分散 (AVADP)

We first picked the group of top relevant brand perceptions for Airbnb: ‘host,’ ‘vacation,’ ‘rental,’ ‘love,’ ‘stay,’ ‘home,’ ‘booking,’ ‘travel,’ ‘guest’.
まず、Airbnbに関連するブランド認知の上位グループをピックアップした: "host"、"vacation"、"rental"、"love"、"stay"、"home"、"booking"、"travel"、"guest"。

Higher value indicates more fluctuations across different periods — likely a bad thing, because the selected brand perception is assumed to be relatively stable and hence should not vary too much month by month.
(ACADPの)高い値は、異なる期間にわたる変動が多いことを示す。**選択されたブランド認知は比較的安定していると想定されるため、月ごとにあまり変動しないはず**である。(なるほど...! こういう仮説を使って評価するのか...! 推薦タスクの評価にオフライン評価においても参考になりそう...:thinking:)

We checked these statistics on the calibrated results as shown above.
上記のように校正された結果について、これらの統計量をチェックした。
We can see that the ranked-based score is the winner as compared to similarity-based scores:
類似度ベースのスコアと比較して、ランクベースのスコアが勝っていることがわかる：

- Lower AVADP: More fluctuations than the non-ranked across a different period — likely a good thing, because the selected brand perception is assumed to be relatively stable and hence should not vary too much month by month.
  AVADPが低い： 異なる期間にわたる変動が非ランク化よりも小さいこと。選択されたブランド認知は比較的安定していると想定されるため、月ごとにあまり変動しないはずなので、これはおそらく良いことである。

## Use Cases of Brandometer Brandometer の使用例

Though we set out to solve the problem of brand measurement, we believe use cases can go above and beyond:
私たちはブランド計測の問題を解決することを目的としていますが、 ユースケースはそれ以上のものになると信じています。

### Use Cases Deep Dive ユースケースのディープダイブ

#### Industry Analysis: Top Brand Perception among Key Players [Monthly Top Perception] 業界分析： 主要プレーヤーのトップブランド認知【月次トップ認知

With top perceptions such as “Stay” and “Home,” Airbnb provides a brand image of “belonging”, echoing our mission statement and unique supply inventory, while other companies have “Rental,” “Room,” “Booking,” a description of functionality, not human sensation.
Airbnbは 「Stay」や「Home」などのトップ認知を提供し、「belonging」というブランドイメージを提供しており、これは私たちのミッションステートメントと独自の供給在庫を反映しています。一方、他の企業は「Rental」、「Room」、「Booking」といった機能の説明をしており、人間の感覚ではない。

#### Top Emerging Perception reveals major events discussed online [Monthly Top Perception] トップ・エマージング・パーセプションは、ネット上で議論されている主要な出来事を明らかにする。

The Top 10 Perceptions are generally stable month to month.
上位10個のperceptionは、月ごとに一般的に安定している。
The top standing perceptions include
上位の認識は以下の通りである。

- Home, Host, Stay, Travel, Guest, Rental, etc.
  ホーム、ホスト、ステイ、トラベル、ゲスト、レンタルなど。

Meanwhile, we use Brandometer to monitor emerging perceptions that jump to the top list, which may reflect major events associated with the brand or user preference changes.
一方、ブランドメーターは、**ブランドに関連する大きな出来事やユーザーの嗜好の変化を反映する可能性のある、トップリストに急上昇する新たな認知を監視するために**使用される。

#### Major Campaign Monitor (Time Series Tracking) 主要キャンペーンモニター（時系列トラッキング）

Businesses create campaigns to promote products and expand the brand image.
企業は商品を宣伝し、ブランドイメージを拡大するためにキャンペーンを行う。
We were able to capture a perception change on one specific Brand Theme after a related campaign.
私たちは、ある特定のブランドテーマに関連するキャンペーン後に、認識の変化を捉えることができた。
(キャンペーンの度に言語モデルを学習し直すのかな??:thinking:)

These use cases are just the beginning.
これらの使用例はほんの始まりに過ぎない。
Essentially, this is an innovative way of gathering massive online input as we learn the needs and perception of the community.
基本的に、これは地域社会のニーズと認識を知るために、オンラインで大規模な意見を集める革新的な方法である。
We will constantly reflect on how we leverage these insights to continually improve the Airbnb experience for our community.
私たちは、Airbnbのコミュニティでの体験を継続的に向上させるために、これらの洞察をどのように活用していくかを常に考えていきます。

## Next Steps 次のステップ

Airbnb’s innovative Brandometer has already demonstrated success in capturing brand perception from social media data.
Airbnbの革新的なBrandometerは、ソーシャルメディアデータからブランド認知を把握することにすでに成功している。
There are several directions for future improvement:
今後の改善の方向性はいくつかある：

Better content segmentation for clearer and more concise insights.
より明確で簡潔な洞察のための、より良いコンテンツのセグメンテーション。

Develop more metrics reflecting social media brand perception.
ソーシャルメディアにおけるブランド認知を反映した、より多くの指標を開発する。

Enhance data foundation, not just Airbnb, but other companies in the same market segment to get more comprehensive insights.
Airbnbだけでなく、同じ市場セグメントに属する他の企業のデータ基盤を強化し、より包括的なインサイトを得る。

If this kind of work sounds appealing to you, check out our open roles — we’re hiring!
このような仕事に魅力を感じる方は、募集中の職種をご覧ください！

## Acknowledgments

Thanks to Mia Zhao, Bo Zeng, Cassie Cao for contributing the best ideas on improving and landing Airbnb Brandometer.
ミア・チャオ、ボー・ゼン、キャシー・カオには、Airbnb Brandometerの改善と着陸に関する最高のアイデアを提供してもらった。
Thanks to Jon Young, Narin Leininger, Allison Frelinger for the support of social media data consolidation.
ジョン・ヤング、ナリン・レイニンガー、アリソン・フレリンガーのソーシャルメディア・データ統合サポートに感謝する。
Thanks to Linsha Chen, Sam Barrows, Hannah Jeton, and Irina Azu who provide feedback and suggestions.
フィードバックと提案を提供してくれたLinsha Chen、Sam Barrows、Hannah Jeton、Irina Azuに感謝する。
Thanks to Lianghao Li, Kelvin Xiong, Nathan Triplett, Joy Zhang, Andy Yasutake for reviewing and polishing the blog post content and all the great suggestions.
Lianghao Li、Kelvin Xiong、Nathan Triplett、Joy Zhang、Andy Yasutakeには、ブログ記事の内容を見直し、推敲してもらった。
Thank Joy Zhang, Tina Su, Andy Yasutake for leadership support!
ジョイ・チャン、ティナ・スー、アンディ・ヤスタケに感謝する！

Special thanks to Joy Zhang, who initiated the idea, for all the inspiring conversations, continuous guidance and support!
このアイディアの発案者であるジョイ・チャンには、刺激的な会話、継続的な指導とサポートに感謝する！

<!-- ここまで読んだ! -->
