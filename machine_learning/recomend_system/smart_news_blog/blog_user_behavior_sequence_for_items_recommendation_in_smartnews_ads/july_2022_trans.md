## link リンク

- https://medium.com/smartnews-inc/user-behavior-sequence-for-items-recommendation-in-smartnews-ads-2376622f6192 https

## title タイトルです。

User Behavior Sequence for Items Recommendation in SmartNews Ads.
スマートニュース広告におけるアイテム推薦のためのユーザ行動Sequence.

## NLP vs. Recommendation 

User historical behavior sequences give us objective data about a user, regardless of his/her gender/age/income, which is ultimately reflected in what he/she has seen and purchased.
**ユーザの過去のbehavior sequencesは、性別や年齢、収入に関係なく、そのユーザに関する客観的なデータとなり**、最終的にはそのユーザが見たもの、買ったものに反映される.
Therefore, how to mine user preferences from behavioral sequences is a hot area in recommendation systems..
そのため、behavior sequencesからどのようにユーザの嗜好を掘り起こすかは、推薦システムのホットな分野である.

The traditional approach is to process these sequences statistically, e.g.
従来のアプローチは、これらのsequencesを統計的に処理するものであった.
collaborative filtering, which calculates the probability that a user who has bought item A will buy item B as a recommendation score.
協調フィルタリングで、アイテムAを購入したユーザーがアイテムBを購入する確率を推薦スコアとして算出する.
Or calculating the average number of times a user has viewed a category/store, the number of activities in a certain time interval for feature modeling, and so on.
あるいは、ユーザがカテゴリ／ストアを閲覧した平均回数や、フィーチャーモデリングのためのある時間間隔でのアクティビティ数などを算出することもできる.
However, when it comes to sequences, natural language processing (NLP) is essentially solving this type of problem.
しかし、**sequencesに関しては、自然言語処理（NLP）がこの種の問題を本質的に解決している**.
A sentence is a sequence, and a conversation is a combination of sequences of sentences.
文はsequenceであり、会話は文のsequenceの組み合わせである.
So in the NLP domain, researchers have been thinking about how to effectively characterize sentences or even strings of conversations (paragraphs)..
そこで、NLPの領域では、文や会話の文字列（パラグラフ）を効果的に特徴付ける方法について研究者が考えてきた.

![](https://miro.medium.com/v2/resize:fit:1400/0*DslE4AF44bC9PnwX)

As shown above, around 2015, we can observe a series of model breakthroughs, from RNN -> LSTM/GRU -> Attention -> Transformer -> Bert -> Bert variants, and watch the SOTA list keep rotating and breaking, while the techniques of these models are also starting to ferment in other domains.
このように、2015年あたりから、RNN→LSTM/GRU→Attention→Transformer→Bert→Bert亜種と、一連のモデルのブレイクスルーを観察し、SOTAリストが回転しながら壊れ続けるのを見守り、またこれらのモデルの技術が他のドメインで発酵し始めるのを見ることができる.
For example, in the field of vision, the Transformer has been used for different tasks, e.g. DETR-based improvements in Object Detection have also yielded SOTA results.
例えば、視覚の分野では、トランスフォーマーは様々なタスクに使用されてきた. 例えばDETRによる物体検出の改善も、SOTAの成果を生んでいる.
In the field of speech, the presence of Transformer can be seen in speech recognition, speech synthesis and text-to-speech.
音声の分野では、音声認識、音声合成、音声合成でTransformerの存在を確認することができる.
In the field of search and push, it is also following the evolution of NLP.
検索やプッシュの分野では、NLPの進化も追いかけている.
From GRU4Rec -> NARM -> SASRec -> Bert4Rec, it has been in public testing and breakthroughs.
GRU4Rec→NARM→SASRec→Bert4Recと、公開テストやブレークスルーで活躍してきた.
The same is true for news recommendation, which is more relevant to NLP, and furthermore, finetune through PLM (Pretrained Language Model) has achieved very good results..
**NLPとの関連性が高いニュース推薦も同様**で、さらにPLM（Pretrained Language Model）によるfinetuneは非常に良い結果を出している.

However, beyond academics, it is important to know whether it can really bring improvements in business scenarios.
しかし、**学術的なこと以上に、ビジネスシーンで本当に改善をもたらすことができるのかどうかが重要**である.
In particular, NLP features are simple, consisting mainly of sentences and words, with some scenarios adding keywords and lexical properties.
特にNLPの特徴は、文と単語を中心に構成されるシンプルなもので、シナリオによってはキーワードや字句のプロパティを追加するものもある.
However, in the case of recommendations, there are many other features that affect user clicks and purchases (e.g. super sales day/product prices/discount etc.).
しかし、レコメンデーションの場合、ユーザのクリックや購入に影響を与える機能は他にもたくさんある（例：スーパーセール日／商品価格／割引など）.
Imagine that we often buy things that we wouldn’t normally buy because of a discount on a Black Friday..
ブラックフライデーの割引で普段買わないようなものを買うことが多いと想像してください.

Today we’re going to take a look at how we’re using SmartNews user historical behavior data in an advertising scenario, and share our tips on how to do this in practice..
本日は、**SmartNewsのユーザ履歴行動データを広告シナリオに活用する方法**を紹介し、実践するためのヒントをお伝えする.

## SmartNews Ads Scenario SmartNews Ads のシナリオ

In SmartNews Ads, there are a lot of advertisers who want to advertise products that will be exposed to interested users and lead to purchases or app installs.
SmartNews Adsでは、**興味のあるユーザに商品を露出し、購入やアプリのインストールにつなげたい広告主が多く存在する**.
For example, like e-commerce advertisers, there may be tens of millions of items, and our platform has to recommend the right items to different users to achieve the advertiser’s CPA/ROAS expectations based on different optimization goals..
例えば、Eコマースの広告主のように、数千万点のアイテムが存在する場合があり、私たちのプラットフォームは、広告主のCPAを達成するために、さまざまなユーザに適切なアイテムを推薦する必要がある.

![](https://miro.medium.com/v2/resize:fit:1400/0*eXQQUCRpjM5eOvJE)

It is necessary to use the user’s behavioral data on the SmartNews to better understand the user and achieve better recommendations.
ユーザをより理解し、より良いレコメンデーションを実現するために、SmartNews上でユーザの行動データを利用することが必要である.
Basic recommendations, such as what users have seen recently, or recommending similar items based on CF, are already very effective in their own right.
**ユーザが最近見たもの、CFに基づいて似たようなものを勧めるなど、基本的なレコメンデーションは、それ自体ですでに非常に効果的である**.
But now that we have the user behavioral sequence data, we try to incorporate the sequence recommendation modeling approach to see if it can lead to better recommendation results and user experience..
しかし、ユーザのbehavioral sequenceデータを手に入れた今、**sequence recommendation modeling のアプローチを取り入れる**ことで、より良いレコメンデーション結果とユーザ体験につながるかどうか試している.

The diagram below shows the scenario we want to model.
下図は、モデル化したいシナリオを示したもの.
When we know the user’s historical behavior, can we guess what items the user will be most interested in next!.
**ユーザの過去の行動がわかると、そのユーザが次にどんなアイテムに最も興味を持つかを推測することができる**.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*uJrnTI2Sm0VdVba0.png)

## Tech Detail / Trick Tech Detail

### Model Selection モデル選択。

As mentioned before, there are a range of models in the recommendation domain that also attempt to deal with sequences.
前述したように、推薦の領域でも sequences を扱おうとする様々なモデルが存在する.
Here we have chosen SASRec as the basis for our experiments, which is a Self-Attention based model architecture with the clear idea of using the past N product sequences to predict the N+1th product.
**SASRec** は、**過去N個の商品sequences を用いてN+1個目の商品を予測するという明確なアイデアを持ったSelf-Attentionベースのモデルアーキテクチャ**であり、ここでは実験の基礎としてSASRecを選択した.
The overall structure is shown in the figure below, using the Multi-head Attention mechanism to obtain a vector of the first N items, hoping that the inner product of the vector with the next item is greater than the other negative sample items.
全体の構成は下図のとおりで、**Multi-head Attention機構**を用いて、最初のNアイテムのベクトルを取得し、次のアイテムとのベクトルの内積が他の負のサンプルアイテムより大きいことを期待する.
The inference is made by putting the user’s historical behavior into the model, obtaining the vector, and using the ANN to find the next most likely TopK item from a pool of 10 million items..
推論は、ユーザの過去の行動をモデルに落とし込んでベクトルを取得し、ANN(?)を使って1000万アイテムのプールから次のTop-Kアイテムの可能性が高いものを探し出すというものある.

![](https://miro.medium.com/v2/resize:fit:1400/0*YGRlGEFLL1p_wNj3)

###  Improve Training Speed トレーニングスピードを向上させる

In order to use sequential modeling, a common training framework resembles a double tower (as shown in Fig.5), with the left tower being the User Representation, i.e.the past historical behavior of the user.
逐次モデリングを行うために、一般的な学習フレームワークは、図5に示すような二重の塔のような形をしており、左の塔はユーザー表現（ユーザの過去の履歴行動）である。.
The right tower is the next item, which is finally compared to the label (positive or negative), using dot or cosine.
右の塔は次のアイテムで、最後にラベル（正または負）とドット(=ドット積?)またはコサイン(cosine類似度?)で比較される.
If there are 10M users, and each user takes 50 different historical behavior sequences, and 3 negative samples, then there are 2 billion (10M * 50 * (1+3)) samples in total, which is a very high training time and iteration cost..
仮に10Mのユーザーがいて、各ユーザが50種類の過去の behavior sequences と3種類のネガティブサンプル(explicitなネガティブ??)を取る場合、合計で20億（10M * 50 * (1+3)）ものサンプルが必要となり、これは非常に高い学習時間と反復コストである.

An optimization point here is that much of the historical behavior data of the same user is calculated repeatedly.
ここでの**最適化ポイントは、同じユーザの過去の行動データの多くが繰り返し計算される**こと.
For example, the first sample sequence is T0 to T50, the second sample sequence is T1 to T51, and the middle sequence (T2 to T50) is actually the same.
例えば、第1サンプル配列はT0～T50、第2サンプル配列はT1～T51、中間配列（T2～T50）は実際には同じ.
SASRec’s training approach solves this problem considerably.
SASRecのトレーニング方法は、この問題をかなり解決している.
For each user, we take a sequence of historical behaviors (e.g. T0 to T50, then T0 predicts T1, T0 to T1 predicts T2, and so on).
各ユーザーについて、過去の行動（例えば、T0からT50まで、次にT0がT1を予測し、T0からT1がT2を予測する、など）を連続的に取得する.
Since Self Attention looks at the entire sequence, a Mask is introduced to mask the items to the right of the Target Item in order to avoid message traversal due to future click behaviors.
Self Attentionはシーケンス全体を見るので、将来のクリック行動によるメッセージトラバースを避けるために、Target Itemの右側のアイテムをマスクするMaskが導入されている.
Thus, by walking through Attention, we actually get a vector of N different sequences and train N samples.
このように、**Attentionを歩くことで、実際にはN種類のsequencesのベクトルが得られ、N個のサンプルを訓練することができる**.
This way of training makes the overall training speed shorter, for a billion levels of click data, it only takes 3~4 hours to get a good convergence result, and it is also convenient for us to do parameter fine-tuning and model iteration..
この学習方法は、全体の学習速度を短くし、10億レベルのクリックデータに対して、3〜4時間で良い収束結果を得ることができ、パラメータの微調整やモデルの反復を行うのにも都合が良いのである.

![](https://miro.medium.com/v2/resize:fit:1400/0*aJHT3_bGIvERfhaY)

### K+1 Cross-entropy 

The original Loss Function was trained to discriminate binary classification, assuming the target is whether the user clicks or not, and the label is click/no click.
元の損失関数は、ターゲットがユーザがクリックしたかどうかであり、**ラベルがclick/no click**であると仮定して、2値分類を識別するように訓練されたものである.
However, because in advertising, our scenario is first used in the recall phase, we do not need to consider the accuracy of the CTR value, but rather the accuracy of the recommended sequence.
しかし、広告では、我々のシナリオはまず想起の段階で使われるため、**CTR値の精度を考慮する必要はなく、推奨シーケンスの精度を考慮すればよ**いのである.
Therefore, in order to speed up the learning of the model, the loss function is also used in a way like DSSM, where each positive sample is combined with K negative samples, and then these K+1 scores are passed through a Softmax, which judges whether the prediction of the positive samples is correct.
そこで、モデルの学習を高速化するために、損失関数もDSSMのように、各陽性サンプルとK個の陰性サンプルを組み合わせ、このK+1個のスコアをSoftmaxに通して、陽性サンプルの予測が正しいかどうかを判定する方法を採用している.
This approach allows for faster convergence and saves training time while ensuring the correctness of the sequence (hopefully maximizing the score of the positive samples).
このアプローチにより、シーケンスの正しさを確保しながら（うまくいけば正サンプルのスコアを最大化できる）、収束を早め、学習時間を短縮することができる.
This training approach is often used in other scenarios as well.
このトレーニング方法は、他の場面でもよく使われる.
For example, in an NLP task, where we want to know what the next sentence in the sentence is most likely to follow, the same can be converted into a classification task and trained with great effect..
例えば、文中の次の文が何に続く可能性が高いかを知りたいというNLPタスクでは、同様に分類タスクに変換して学習することで大きな効果を得ることができる.

![](https://miro.medium.com/v2/resize:fit:1064/0*9xLTuBWZoGxXioHK)

### Integrate Other Features その他の機能を統合する。

SASRec only uses the item id as a feature.
**SASRecはアイテムIDのみを特徴量として使用する.**
However, there is a lot of side information that can be used to help with training, such as title / description / image / category and other multimodal features that may be able to better characterize the items.
しかし、タイトル / 説明 / 画像 / カテゴリなどのマルチモーダルな特徴など、トレーニングに役立つサイド情報がたくさんあり、アイテムをよりよく特徴付けることができるかもしれない.
The easiest way to do this is to concatenate these features and turn them into a fixed vector after an MLP.
**最も簡単な方法は、これらの特徴を連結し、MLPの後に固定ベクトルにすること**である.
In this paper, FDSA introduces an attention mechanism, with the idea that attention is used to learn which features most influence user choice.
本論文では、FDSAがアテンション機構を導入し、どの特徴がユーザーの選択に最も影響を与えるかをアテンションで学習することを考えた.
In our experiments, however, most of the id features are quick to train and work well.
しかし、**我々の実験では、ほとんどのid特徴が短時間で学習でき、うまく機能することがわかった**.
However, in some verticals, such as real estate/used cars, the addition of some features can improve the conversion rate a lot.
しかし、不動産/中古車など一部のバーティカルでは、いくつかの機能を追加することでコンバージョン率を大きく向上させることができる.
For example, the type of house/price/distance from the metro station, etc., and the mileage/brand/price of a used car are all important variables for conversion.
例えば、家のタイプ/価格/地下鉄駅からの距離など、中古車の走行距離/ブランド/価格などは、変換のための重要な変数となる.
Also in the cold start of an item, it is helpful to generalize the item’s features..
また、アイテムのコールドスタートでは、アイテムの機能を一般化することが有効.

![](https://miro.medium.com/v2/resize:fit:1400/0*46i0gnC0EZWWZEhu)

### Auto Tuning オートチューニング

Although the overall training time can be compressed to 3–4 hours, it is particularly time-consuming to do tuning (e.g.
全体の学習時間は3～4時間に圧縮できますが、特にチューニングに時間がかかるため（例．
dimension / dropout rate / learning rate / multi-head / blocks, etc.) if it cannot be done in parallel.
次元
Thanks to the SmartNews AI-Infra team, which has adopted Microsoft’s NNI to support fast Auto Tuning, the framework is able to automatically get the best parameters from a defined range of parameters, through a number of Search Algorithms, and supports parallel training.
高速なAuto TuningをサポートするためにMicrosoftのNNIを採用したSmartNews AI-Infraチームにより、フレームワークは、定義されたパラメータの範囲から、多数のSearch Algorithmにより最適なパラメータを自動的に取得することができ、並列トレーニングにも対応しています。
Experimental results also show that the appropriate parameters vary in different vertical domains and data sizes.
また、実験結果から、適切なパラメータは、垂直領域やデータサイズが異なると変化することがわかります。
With this training, the CTR can be increased by 5–10%.
このトレーニングで、CTRを5～10％アップさせることができます。
The user’s Reject Rate is also reduced by another 10%..
また、ユーザーの不合格率もさらに10％低下します。

![](https://miro.medium.com/v2/resize:fit:1400/0*Z2KcvFq7M7K4vugw)

## Cold Start Scenario コールドスタートシナリオ

We have two types of Cold Start, new items and new users.
コールドスタートには、新商品と新ユーザーの2種類を用意しています。
In fact, the retention rate is different for different items in different areas.
実は、地域によってアイテムによって保持率が違うんです。
For example, in the e-commerce scenario, the rate of new items is relatively low compared to old items.
例えば、Eコマースのシナリオでは、新商品の割合は旧商品に比べて相対的に低くなっています。
So even if we only use product ids for modeling, we can still get good results.
ですから、製品IDだけを使ったモデリングでも、良い結果を得ることができるのです。
However, in an auction scenario, such as eBay, where many items are auctioned off and gone, the ratio of new items is particularly high as new items are constantly being auctioned.
しかし、eBayのように多くの商品が競売にかけられ消えていくオークションの場面では、常に新しい商品が競り落とされるため、特に新品の比率が高くなるのです。
This requires the use of multimodality to generalize the items to make recommendations for new items (e.g.
そのためには、マルチモダリティを利用してアイテムを一般化し、新たなアイテムのレコメンドを行う必要がある（例：。
FDSA with multimodal features)..
マルチモーダル特徴量を用いたFDSA)...

For new users, it is relatively difficult, as they need to have a cold start period to collect user behavior to understand their interests.
新規ユーザーの場合は、コールドスタート期間を設けてユーザーの行動を収集し、興味を把握する必要があるため、比較的難しい。
If you only look at advertising behavior, the data collection takes even longer.
広告行動だけを見れば、データ収集にはさらに時間がかかる。
In the absence of sufficient user historical behavior sequences, the sequence model is not applicable.
十分なユーザー履歴の行動シーケンスがない場合、シーケンスモデルは適用できない。
Another idea is to use the user’s news click sequence on the APP (which is easier to collect) to establish a relationship with the product, which is another interesting challenge..
また、ユーザーのAPP上でのニュースのクリックシーケンス（収集しやすい）を利用して、製品との関係性を構築するというアイデアもあり、これも面白いチャレンジです。

## Performance パフォーマンス

We trained individual models for different domains, such as e-commerce/property/automotive/auction, and were able to increase click-through rates by 10–20% compared to the original CF i2i model.
電子商取引など、ドメインごとに個別のモデルを学習させました。
Some small advertisers in some verticals were even able to increase their CVR by around 30%, which was very impressive, even though the models were not specifically optimized for CVR.
一部のバーティカルな小規模広告主は、CVRに特化して最適化されたモデルではないにもかかわらず、CVRを30％程度向上させることができたこともあり、非常に印象的でした。
However, in the case of large e-merchants with more than 10M products, the advantage is not so obvious.
しかし、10M以上の商品を扱う大規模なe-マーチャントの場合、その優位性はあまり明らかではありません。
The click-through rate only increases by about 5%.
クリック率は5％程度しか上がりません。
But another significant improvement is the user reject rate, which can be reduced by about 10–20%.
しかし、もう一つの大きな改善点は、ユーザーの拒否率を約10〜20％削減できることです。
We interpret this as the model recommending products that are more in line with the user’s interests, so that the user does not feel annoyed by the ads, making the overall user experience better..
これは、モデルがユーザーの興味に沿った商品を推薦することで、ユーザーが広告に煩わしさを感じることなく、全体的なユーザー体験をより良いものにするためだと解釈しています。

## Future work 今後の課題

### News to Ads 広告へのニュースです。

SmartNews is an information app and has a lot of user news reading sequences.
SmartNewsは情報アプリであり、ユーザーニュースの閲覧配列が多いのが特徴です。
If we could model the user’s news viewing behavior and transfer it to item recommendations, this could be very helpful for new users and be of greater value to advertisers.
ユーザーのニュース閲覧行動をモデル化し、それをアイテムのレコメンデーションに転用できれば、新規ユーザーにとって非常に有益であり、広告主にとってもより大きな価値を持つことができるだろう。
Intuitively, the correlation between news and purchase is weak most of the time, but it would be particularly valuable if user interests could be tapped from the news sequence and then transferred to merchandise to bring new users to advertisers..
直感的には、ニュースと購買の相関は弱いことが多いが、ニュースの系列からユーザーの興味を引き出し、それを商品に転嫁して新規ユーザーを広告主に呼び込むことができれば、特に価値があると思うのだが。

### How to Add Any Features 任意の機能を追加する方法。

More features are better.
機能は多い方がいい。
However, adding all of the features doesn’t necessarily pay off for the model results.
しかし、すべての機能を追加しても、必ずしもモデルの結果が報われるわけではありません。
Many statistical features in recommendations are also very effective.
レコメンデーションにおける多くの統計的特徴も非常に有効です。
If you add them all to the attention, sometimes they tend to skew the model, and can’t get much effect.
全部を注目させると、モデルが歪みがちで、あまり効果が得られないこともあります。
So for statistical features, it is possible to train them separately and finally fuse individual scores in an MLP to get better results.
そのため、統計的な特徴量については、別々に学習させ、最終的にMLPで個々のスコアを融合させることで、より良い結果を得ることが可能です。
At the moment, there is no significant gain in all aspects through FDSA, but the cost of training is much higher..
現時点では、FDSAを通じてすべての面で大きな利益を得ることはできませんが、トレーニングにかかる費用ははるかに高くなります。

### PLM Model PLMモデル。

In the NLP domain, it is a common paradigm to use Bert to do large-scale training and then fine-tune for downstream tasks.
NLPの領域では、Bertを使って大規模な学習を行い、その後、下流のタスクのために微調整を行うというのが一般的なパラダイムです。
In recommendation, if the amount of data is large enough, we can also try to train a base model by self-data and use self-supervised training to train the model as a pre-train model for downstream tasks, which can accelerate the convergence and also bring benefits to some small advertisers.
レコメンデーションでは、データ量が十分であれば、自己データでベースモデルを訓練し、自己教師付き訓練を使って、下流タスクのプレトレーニングモデルとして訓練することも試み、収束を早め、一部の小規模広告主にも利益をもたらすことができる。
For example, much new research in News Recommendation uses the NLP pre-train model to finetune, which can get better results..
例えば、ニュースレコメンデーションの新しい研究の多くは、NLPのプレトレーニングモデルを使用して微調整を行い、より良い結果を得ることができます。
