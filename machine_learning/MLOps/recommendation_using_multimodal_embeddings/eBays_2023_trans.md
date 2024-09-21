## refs 審判

<https://innovation.ebayinc.com/tech/engineering/beyond-words-how-multimodal-embeddings-elevate-ebays-product-recommendations/>
<https://innovation.ebayinc.com/tech/engineering/beyond-words-how-multimodal-embeddings-elevate-ebays-product-recommendations/>

# Beyond Words: How Multimodal Embeddings Elevate eBay's Product Recommendations 言葉を超えて： マルチモーダル・エンベッディングがeBayの商品推薦をどのように向上させるか

By integrating information from different modalities of eBay listings such as titles and images, we greatly improved the buyer experience and relevance of the recommended items on eBay’s listing pages.
タイトルや画像など、eBayのリスティングのさまざまなモダリティからの情報を統合することで、eBayのリスティングページの推薦アイテムのバイヤー体験と関連性を大幅に向上させました。

## Introduction

eBay is committed to providing a seamless and enjoyable buying experience for its customers.
eBayは、お客様にシームレスで楽しい購入体験を提供することをお約束します。(読み進めていくと、メルカリみたいな形式のサービスであることがわかった...!:thinking_face:)
One area that we’re continuously looking to improve is the quality of our listings, particularly with regards to images and text.
私たちが継続的に改善を求めている分野のひとつが、特に画像とテキストに関するリスティングの品質です。
In the past, the presence of low-quality images could lead to inaccurate product representation and, in a worst-case scenario, disappointed buyers.
**これまでは、低品質の画像が存在すると、製品の表現が不正確になり**、最悪の場合、購入者を失望させることになりかねなかった。
Additionally, text and image embeddings derived respectively from listing titles and images were stored in separate spaces, making it challenging to create a unified and accurate recommendation system.
**さらに、リストタイトルと画像からそれぞれ得られるテキストと画像の埋め込みは、別々のスペースに保存されていたため、統一された正確なレコメンデーションシステムを作成するのは困難だった**。(別のデータソースで管理されてたってこと??もしくは埋め込み空間が別だったってこと??:thinking_face:)
eBay's deep learning models were not able to process both types of information efficiently.
イーベイのディープラーニング・モデルは、両方のタイプの情報を効率的に処理することができなかった。

To address these challenges, we've created a new system for contextual recommendation by integrating different modalities and custom-built modules, including image-text mismatch detection and triplet loss with TransH, into the recall module.
このような課題を解決するために、画像とテキストの不一致検出やTransHによるトリプレットロスなど、異なるモダリティや特注モジュールを想起モジュールに統合することで、文脈推薦のための新しいシステムを構築した。
Our approach enables eBay's recommendation system to deliver highly accurate recommendations and drives about a 15% percent increase in buyer engagement.
私たちのアプローチは、eBayのレコメンデーションシステムが精度の高いレコメンデーションを提供することを可能にし、バイヤーのエンゲージメントを約15％向上させます。

<!-- ここまで読んだ! -->

## Information Retrieval: Recall Module in eBay's Recommendation System 情報検索 eBayのレコメンデーションシステムにおけるリコールモジュール

The recall module is a crucial component of the eBay recommendation system.
リコール・モジュールは、eBay推薦システムの重要な構成要素である。
Its primary function is to retrieve from various perspectives a set of items that are most relevant to the main listing on the View Item Page.
**その主な機能は、ビューアイテムページのメインリストに最も関連するアイテムのセットをさまざまな観点から検索すること**です。(つまり、item2itemの推薦タスクっぽい...??)
The recall module is the first step in the recommendation process, and it plays a critical role in making sure that the items are the most appropriate, relevant and high-quality to our users.
リコール・モジュールは推薦プロセスの最初のステップであり、ユーザーにとって最も適切で、関連性があり、質の高いアイテムであることを確認する上で重要な役割を果たします。

In the past, the recall module within the recommendation system primarily depended on information from a single modality, such as the item title and item image.
これまでリコメンデーションシステム内のリコールモジュールは、**主にアイテムタイトルやアイテム画像といった単一のモダリティからの情報に依存していた**。(うんうん...!)
While this approach proved useful for retrieving relevant results, it had its limitations.
このアプローチは、関連する結果を検索するのに有用であることがわかったが、限界があった。
The unimodal method lacked signals from other modalities, which made it difficult to provide accurate recommendations for more complex scenarios, such as distinguishing between a toy car and a real car.
**ユニモーダル法には他のモダリティからの信号が欠けていたため、おもちゃの車と本物の車を区別するなど、より複雑なシナリオに対して正確な推薦を提供することが難しかった。**(なるほど、確かに...:thinking_face:)

By integrating multimodal information from items, we have developed a high-performance recall module that significantly improves the recommendation system's accuracy for more complex scenarios.
アイテムからのマルチモーダルな情報を統合することで、より複雑なシナリオに対して推薦システムの精度を大幅に向上させる高性能なリコールモジュールを開発しました。
This innovative approach ensures a more relevant and personalized user experience.
この革新的なアプローチは、より適切でパーソナライズされたユーザー体験を保証する。
As illustrated in Figure 1, relying solely on the text modality for retrieving relevant listings may result in the inclusion of items within the recommendation system that are not as relevant or have low quality.
図1に示されているように、関連するリスティングを取得するために**テキストモダリティだけに依存すると**、推薦システムには関連性が低いか品質が低いアイテムが含まれる可能性があります。(関連性と品質って何が違うんだろ...品質は、前述の例のおもちゃの車と本物の車の違いを指してるのかな...:thinking_face:)
This occurs because the similarity of their titles to the hero item on the page is high, but this disregards cover image relevance and quality.
これは、ページ上のヒーロー・アイテムとのタイトルの類似性が高いために起こるが、カバー画像の関連性と品質は無視される。

![]()

<!-- ここまで読んだ! -->

## Multimodal Item Embedding Solution マルチモーダル　アイテム埋め込みソリューション

To solve these problems, we recently launched a new Multimodal Item Embedding solution that can now effectively combine information from different modalities to obtain rich feature information.
これらの問題を解決するために、我々は最近、**異なるモダリティからの情報を効果的に組み合わせて豊富な特徴情報を得ることができる**新しいマルチモーダルアイテム埋め込みソリューションを立ち上げました。
This integration allows the team to better understand listings on eBay and create a more accurate and efficient recall set for the recommendation system.
この統合により、チームはeBayの出品をよりよく理解し、レコメンデーションシステムのより正確で効率的なリコールセットを作成することができる。
Additionally, by detecting mismatches between the image and title of a listing, the team can provide an opportunity to filter out low-quality results.
さらに、**リスティングの画像とタイトルの不一致を検出することで、チームは低品質の結果をフィルタリングする機会を提供することができます**。(これは推薦システムのモニタリングの話だろうか??:thinking_face:)

Our Multimodal Item Embedding solution uses pretrained embeddings from the Search team (Text embedding with BERT as the base model) and Computer Vision team (Image embedding with Resnet-50 as the base model) teams.
私たちのマルチモーダルアイテム埋め込みソリューションは、検索チーム（ベースモデルとしてBERTを使用したテキスト埋め込み）とコンピュータビジョンチーム（ベースモデルとしてResnet-50を使用した画像埋め込み）のチームから事前に訓練された埋め込みを使用しています。
(うんうん、タイトルと画像がそれぞれ異なる埋め込みモデルでencodeされてるやつ...!これが入力データになるのかな:thinking_face:)
It includes a Siamese two-tower model trained on the Machine Learning training platform to predict the co-click probability of two items.
これには、2つのアイテムの共クリック確率を予測するために、機械学習トレーニングプラットフォームでトレーニングされた Siamese 2タワーモデルが含まれています。
(下側の方が次元数が多いからタワーモデル。ターゲットアイテムの埋め込みを作るタワーと、関連アイテムの埋め込みを作るタワーの2本があるのでtwo-tower model...!:thinking_face:)
The model uses triplet loss with TransH to ensure that text and image embeddings are projected into the same embedding space.
**このモデルは、テキストと画像の埋め込みが同じ埋め込み空間に投影されることを保証するために、TransHによるtriplet lossを使用しています。** (うんうん、埋め込み空間を共通化するための手法としてcontrastive leaningを使ってる...!:thinking_face:)
The title-image mismatch detection module uses mismatch embeddings to predict the probability of clicks on an item with mismatched pictures and titles.
タイトルと画像の不一致検出モジュールは、不一致埋め込みを使用して、画像とタイトルが不一致のアイテムがクリックされる確率を予測する。(??)

In the example below, the “Embedding Distance” in the last column is a unified score that reflects the similarity to the seed item from both the item title and cover image perspectives.
以下の例では、最後の列の「埋め込み距離」は、アイテムのタイトルとカバー画像の両方の観点から、シードアイテムとの類似性を反映した統一スコアです。
The new unified score is more accurate than the "Title Similarity" score, which relies only on title texts.
**新しい統一スコアは、タイトルテキストのみに依存する「タイトル類似度」スコアよりも正確**である。

## Siamese Two-Tower Model シャム2タワーモデル

A Siamese two-tower model is a neural network architecture that uses two identical subnetworks (or towers) to process two different inputs and is commonly used for tasks that involve comparing or matching two inputs, such as similarity analysis, duplicate detection, and recommendation systems.
シャム2タワーモデルは、2つの異なる入力を処理するために2つの同一のサブネットワーク（またはタワー）を使用するニューラルネットワークアーキテクチャであり、類似性分析、重複検出、推薦システムなど、2つの入力を比較または照合するタスクによく使用される。
In the case of the Multimodal Item Embedding solution, each tower represents a listing, and the inputs to each tower are the concatenated pre-trained image and text embeddings for that listing.
Multimodal Item Embeddingソリューションの場合、各タワーはリスティングを表し、**各タワーへの入力は、そのリスティングのために事前に訓練された画像とテキストの埋め込みを連結したもの**である。(うんうん、入力層が長く出力層に向かって次元数が小さくなっていくのでタワーモデル)

The key benefit of using a Siamese two-tower model is that it allows the model to learn a similarity function between the two different listings based on their image and text embeddings in an end-to-end manner without relying on handcrafted features or intermediate representations.
**シャム2タワーモデルを使用する主な利点は、手作業の特徴や中間表現に頼ることなく、エンドツーエンドで**2つの異なるリスト間の類似性関数(i.e. two-towerモデルのこと??)を、画像とテキストの埋め込みに基づいて学習できることである。
(シャムってなんなんだろう。two-tower modelの種類の一つなのかな...:thinking_face:)
This makes the model more flexible and adaptable to different types of input data.
これにより、モデルはより柔軟になり、さまざまなタイプの入力データに適応できるようになる。
By calculating the affinity score between the two item embeddings, we can predict whether they are likely to be co-clicked or not.
2つのアイテム埋め込み間の親和性スコアを計算することで(=画像とテキスト、ではなく、2つのアイテムの比較の話!)、それらが共クリックされる可能性が高いかどうかを予測することができる。
Moreover, the shared weights in the two towers can help prevent overfitting as they constrain the model to learn representations that are useful for both inputs.
**さらに、2つのタワーで重みを共有することで、モデルが両方の入力に有用な表現を学習するよう制約されるため、オーバーフィッティングを防ぐことができる。**
(これはuserとitemのtwo-tower modelと異なる特徴かも...!:thinking_face:)

<!-- ここまで読んだ! -->

## Triplet Loss with TransH トランスHによるトリプレット損失

In the Multimodal Item Embedding solution, one of the challenges was ensuring that both the image and text embeddings for each listing were distributed in the same embedding space so that they could be easily integrated together.
Multimodal Item Embeddingソリューションでは、**各リストの画像とテキストの埋め込みを同じ埋め込み空間に分散させ、簡単に統合できるようにすることが課題の1つでした**。
To address this challenge, the team used a technique called triplet loss.
この課題に対処するため、研究チームはTriplet lossという技術を使用した。(Triplet loss勉強しててよかった〜:thinking_face:)

Triplet loss is a type of loss function commonly used in deep learning to train models for tasks such as image recognition, face verification, and more.
トリプレットロスとは、ディープラーニングにおいて、画像認識や顔認証などのタスクのモデル学習によく使われる損失関数の一種だ。
The idea behind triplet loss is to learn an embedding function that maps input data points to a common embedding space, where they can be compared using a distance metric like Euclidean distance.
トリプレットロスの背後にある考え方は、入力データ点を共通の埋め込み空間にマッピングする埋め込み関数を学習することであり、そこでユークリッド距離のような距離メトリックを使って比較することができる。
The triplet loss function is designed to ensure that the distance between similar listings (e.g., co-clicked listings) is minimized, while the distance between dissimilar listings is maximized.
トリプレット損失関数は、類似リスティング（例えば、コ・クリックされたリスティング）間の距離が最小化され、非類似リスティング間の距離が最大化されるように設計されている。

In addition to triplet loss, the team also borrowed the TransH idea from knowledge graphs to project listings onto a hyperplane.
トリプレットロスに加えて、チームは知識グラフからTransHのアイデア(=知識グラフに基づく埋め込みだっけ??:thinking_face:)を借りて、超平面上にリストを投影した。
TransH is a model in the knowledge graph embedding realm that represents entities and relations as vectors in a continuous space.
TransHは知識グラフ埋め込み領域のモデルで、entitiesとrelationsを連続空間のベクトルとして表現する。
TransH projects entities and relations onto a hyperplane before computing the inner product to capture complex interactions between them.
TransHは、entitiesとrelationsを超平面上に投影してから内積を計算し、それらの間の複雑な相互作用を捉える。
The team adapted this idea to project the DNN-encoded image and text embeddings for each listing onto a hyperplane, ensuring that the two embeddings represented the same listing.
研究チームはこのアイデアを適応して、各リスティングのDNNエンコードされた**画像とテキストの埋め込みを超平面上に投影し、2つの埋め込みが同じリスティングを表していることを保証した**。(知識グラフ自体を使ってる訳じゃなくて、知識グラフの埋め込み手法TransHのアイデアを使ってるってことか...!:thinking_face:)

![TransHの概念図]()

By using triplet loss with TransH, the team was able to effectively combine information from different modalities and obtain rich feature information for each listing.
**TransHによるtriplet loss関数**を使用することで、チームは異なるモダリティからの情報を効果的に組み合わせ、各リストの豊富な特徴情報を得ることができた。
Combining the triplet loss and TransH techniques, the loss of the two-tower model turns out to be:
トリプレットロスとTransHのテクニックを組み合わせると、2タワーモデルの損失関数は次のようになる:

$$
TripletLoss(transH) =
$$

Offline training comparison: triplet loss with different projection methods
オフライントレーニングの比較： 異なる投影法によるトリプレットロス

<!-- ここまで読んだ! -->

## Mismatch Detection Module 不一致検出モジュール

As an online marketplace, eBay accommodates a vast array of pre-loved items listed by individual sellers.
**オンライン・マーケットプレイスであるeBayは、個人出品者によって出品された膨大な数の中古品に対応している。**(なるほど...! メルカリみたいな感じだ!:thinking_face:)
However, the image quality, and thus the accurate representation, of these images can sometimes vary.
しかし、これらの画像の品質、そしてそれによる正確な表現は、時に異なることがあります。

Figure 6: An instance of mismatched product titles and cover images for the search term "Sony headphone"
図6：検索語「Sony headphone」に対するタイトルとカバー画像が一致しない製品の例

Upon identifying this problem, we applied a sophisticated module to address it.
この問題を特定した上で、我々は洗練されたモジュールを適用して対処した。
Detailed data analysis revealed that products exhibiting discrepancies between images and descriptions yielded lower click-through and purchase rates.
**詳細なデータ分析により、画像と説明文の間に不一致がある商品は、クリックスルー率と購入率が低いことが明らかになった。**(i.e. いまいちな出品を検出する話か...!:thinking_face:)
Users typically avoided items displaying such inconsistencies.
ユーザーは通常、このような矛盾を示すアイテムを避ける。
Aiming to address this issue, we used the discrepancy between the image embedding and title embedding mapped in the TransH hyperplane as the model input.
この問題を解決するために、**TransH超平面に写像された画像埋め込みとタイトル埋め込みの間の不一致をモデルの入力として使用した。**
Our predictive target was set to the probability of an item not receiving a click, which represents the extent of incongruity between the image and title and how it influences the potential for the item to be clicked on.
予測ターゲットは、クリックされない確率に設定された。これは、画像とタイトルの不一致の程度を表し、アイテムがクリックされる可能性にどのような影響を与えるかを表している。

Figure 7: Illustration of mismatch module’s prediction target
図7：不一致モジュールの予測ターゲットのイラスト

Figure 8: Depiction of the mismatch module's results, where a higher mismatch score indicates the occurrence of a mismatch scenario
図8：不一致モジュールの結果の描写。高い不一致スコアは、不一致シナリオの発生を示す。

After adding the loss for image-text mismatch, we conducted a case analysis on the results after the model training was completed.
画像とテキストの不一致に対する損失を追加した後、モデルの学習が完了した後の結果についてケース分析を行った。
From the results, we found that the model's prediction accuracy for image-text mismatch of the products was well-aligned with reality, indicating that our image-text mismatch module is effective.
その結果、商品の画像とテキストの不一致に対するモデルの予測精度は現実とよく一致しており、我々の画像とテキストの不一致モジュールが有効であることを示している。

Table 2: Offline training metrics for mismatch module plus triplet loss
表2：不一致モジュールとトリプレット損失のオフライントレーニングメトリクス

Below are the offline experimental results of the multimodal approach.
以下は、マルチモーダル・アプローチのオフライン実験結果である。
After adding the embedding space triplet loss and image-text mismatch loss to the model, both factors had a positive influence on the model's metric performance.
埋め込み空間トリプレット損失と**画像-テキストミスマッチ損失**をモデルに追加した後、両方の要因がモデルのメトリック性能にプラスの影響を与えた。(損失関数にこの項目を加えたってことか...!:thinking_face:)

<!-- ここまで読んだ! -->

## Online Experiment Results オンライン実験結果

Multimodal embedding-based recall has been deployed on several eBay pages where our recommendations are shown, such as the listing page, add-to-cart page, order detail page, and watch page.
マルチモーダル埋め込みに基づくリコールは、リスティングページ、カートに追加ページ、注文詳細ページ、ウォッチページなど、eBayのいくつかのページに展開されています。
A/B tests have shown a significant improvement in key business metrics:up to a 15.9% increase in CTR (Click Through Rate) and a 31.5% increase in PTR (Purchase Through Rate).
A/Bテストでは、**主要なビジネスメトリクスが大幅に改善**されており、CTR（クリックスルー率）が最大15.9％、PTR（購入スルー率）が31.5％向上しています。
Starting in February 2023, our Multimodal recall has been deployed online and is serving site traffic in eBay's website and app.
2023年2月より、当社のマルチモーダルリコールはオンラインで展開され、eBayのウェブサイトとアプリでサイトトラフィックを提供しています。

The A/B test results validate that integrating multimodal techniques to retrieve information from different dimensions of listings in our recommendation recall module drives better conversion and buyer engagement.
A/Bテストの結果は、リコメンデーションリコールモジュールでリスティングの異なる次元から情報を取得するためにマルチモーダル技術を統合することが、より良いコンバージョンと購買者のエンゲージメントを促進することを検証しています。
From data analysis, we found that Multimodal embedding is able to recall more items than relying on a single modality alone and can detect mismatches between text descriptions and cover images.
データ解析の結果、マルチモーダル埋め込みは、単一のモダリティだけに依存するよりも多くのアイテムをリコールし、テキストの説明とカバー画像の不一致を検出することができることがわかりました。

## Summary 要約

​​In this blog post, we've discussed how eBay has advanced its listing recommendations with a Multimodal Item Embedding solution.
このブログポストでは、eBayがマルチモーダルアイテム埋め込みソリューションでどのように出品レコメンデーションを進化させたかについて説明しました。
Our approach integrates various modalities of eBay listings, which benefits the buyer experience and the relevance of suggested listings.
私たちのアプローチは、eBayのリスティングの様々なモダリティを統合し、買い手の経験と提案されたリスティングの関連性に利益をもたらします。
We delved into the issues of low-quality images and the disconnect between image and text embeddings, and how these influenced the development of our solution.
私たちは、低品質の画像と画像とテキストの埋め込みの不一致の問題について掘り下げ、これらが私たちのソリューションの開発にどのように影響を与えたかについて説明しました。
The approach is an example of how eBay is committed to continually improving the buying experience by leveraging advanced technologies and data-driven insights.
**このアプローチは、eBayが先進技術とデータ駆動の洞察を活用して、購入体験を継続的に改善することに取り組んでいることの一例です。**(この表現いいね...!:thinking_face:)

In the next step, we will initiate the development of the NRT pipeline, focusing on integrating user-specific information and the LLM prompt module to enhance personalization and relevance of multimodal item embedding in recommendations.
次のステップでは、ユーザー固有の情報を統合し(あ、確かに。今回の話はパーソナライズはしてないもんね:thinking:)、LLMプロンプトモジュールを活用して、レコメンデーションにおけるマルチモーダルアイテム埋め込みのパーソナライゼーションと関連性を向上させることに焦点を当てたNRTパイプラインの開発を開始します。

<!-- ここまで読んだ! -->
