## これは何?

- chip huyenさんのブログ記事 [Self-serve feature platforms: architectures and APIs](https://huyenchip.com/2023/01/08/self-serve-feature-platforms.html) を読んだメモ。

## 特徴量に関連する各コンポーネントの用語の整理

- 特徴量ストア(Feature store): 特徴量を保存/再利用
- モデルプラットフォーム(Model platform): モデルをパッケージ化/デプロイ
- 本ブログにおける、**特徴量プラットフォーム(Feature platform)**って??
  - 特徴量の設計/計算/推論サービスへの特徴量の提供を行うコンポーネント。
  - ex. LinkedInにおける特徴量プラットフォーム「Feathr」
    - 検索、フィード、広告を含む数十のアプリケーションに対して、Feathrが特徴量を提供してるらしい。
    - Feathrにより、新しい特徴量の追加や実験に必要な工数を、数週間から数日へ短縮し、既存の特徴量処理パイプラインよりも最大50%高速に動作したらしい。

## 特徴量プラットフォームの進化, モデルレジストリや特徴量ストアとの違い

### 三種類のレイテンシー最適化

- バッチ推論からリアルタイム推論への移行の流れ 
  - -> 特徴量プラットフォームの必要性が増加。
- リアルタイム推論のユースケースにとっての課題はレイテンシーである。
  - 具体的には、以下の**3種類のレイテンシー最適**化が求められるようになった
    - **特徴量計算レイテンシー(Feature computation latency)**
      - 生データから特徴量を生成するのにかかる時間。
      - モデルがバッチ特徴量のみを使用する場合は、このmetricは推論時はゼロになる。
    - **特徴量取得レイテンシー(Feature retrieval latency)**
      - 推論サービスが特徴量を取得するのにかかる時間。
    - **推論計算レイテンシー(prediction computation latency)**
      - モデルが予測結果を生成するのにかかる時間。
      - このレイテンシーはよく研究されてる。
  - 特徴量プラットフォームは、1つ目と2つ目のレイテンシーを最適化するように設計されてるらしい。

### 特徴量ストアとの違い

- 一般的に**特徴量ストアは特徴量プラットフォームの一部**と言って良いはず。
- 特徴量ストアの主な目的は以下。(うんうん、納得できる...!:thinking:)
  - 特徴量取得レイテンシーを削減すること
  - 計算された特徴量を再利用のために保存し、計算コストを削減すること。
    - **同じ特徴量を必要とする複数のモデルは、冗長な計算なしにその特徴量を再利用できるべき**。(うんうん...!わかる:thinking:)
- 特徴量ストアの最も単純な形 = 計算された特徴量をメモリ内に保存するkey-value型ストア!
  - key-value型ストアの例 = DynamoDB, Redis, Bigtable
  - 特徴量ストアのやや複雑な形では、**特徴量をディスクにも永続化**して、学習でも扱いやすいようにする
    - (学習時と推論時の特徴量の一貫性の話だ...!:thinking:)
    - (オンラインストアだけじゃなくてオフラインストア的な機能...!:thinking:)
      - オンラインストアがOLTP(Online Transaction Processing)的な特徴量のやり取りを担当して、オフラインストアがOLAP(Online Analytical Processing)的な特徴量のやり取りを担当するイメージ...!:thinking:
- 一方、**特徴量プラットフォームは、Feature retrievalだけじゃなくてfeature computationも役割として含む**。
  - (なので、Feature Pipelines + Feature Storeみたいなイメージ...!:thinking:)
  - 特徴量プラットフォームの有名な事例: 
    - LinkedInのFeathr(オープンソース)と、AirbnbのChronon (以前はZiplineと呼ばれていた)。
    - 例えば、Sagemaker Feature Store, Vertex AI Feature Storeは特徴量ストアであり、feature computationは扱わないので特徴量プラットフォームとは言えない。

### モデルプラットフォームとの違い

- まずモデルプラットフォームってなに??
  - モデルをパッケージ化してサーブするための役割。
    - (あ、じゃあ推論サービスっぽい役割なのか。FTI PipelinesでいうTとIが混ざった概念っぽい:thinking:)
  - ざっくり3つの主要コンポーネント
    - モデルデプロイAPI (model deployment API)
    - モデルレジストリ (model registry)
    - 推論サービス (prediction service)
  - (うーん、FTI Pipelinesアーキテクチャとはそもそも少し思想が異なる感じがする。1つ目はTだし、2つ目は境界となる永続化層だし、3つ目はIなので...!:thinking:)
- オンライン予測のユースケースが成熟するにつれて、企業は特徴量プラットフォームとモデルプラットフォームを分離する傾向が強まってるらしい。
  - -> 責務と要件が異なるから! (そりゃそうな感じがする...! FTI Pipelinesと同じような話かな...!!:thinking:)

## 特徴量タイプの分類

- バッチ特徴量(Batch features):
  - 計算方法

## 自社で特徴量プラットフォームを構築する際の課題

## appendix: 3種類の特徴量(Batch features vs. real-time features vs. near real-time features)

