- refs:
  - NNだと基本Entity Embeddingをするって書かれてた! [序盤に試すテーブルデータの特徴量エンジニアリング](https://zenn.dev/colum2131/articles/fffac4654e7c7c)
  - 元論文を日本語翻訳したやつ! ["Entity Embedding of Categorical Variables"の日本語翻訳<前編>](https://qiita.com/meamon/items/8dff8568498014d3f4f3)

## Entity Embedding って何??

- Entity Embeddingはカテゴリカル特徴量を埋め込みベクトルに変換する手法で、特にNNモデルの入力として利用される。
- 2016年の論文「Entity Embeddings of Categorical Variables」で提案された。(Googleのチームが書いた論文)
- One-hotエンコーディングとの比較:
  - One-hotエンコーディングはNNの入力として有効な選択肢だが、2つの欠点がある。
  - 1つ目: カテゴリーの種類が非常に多い特徴量を扱う場合、非現実的なコンピュータリソースを要求すること。
  - 2つ目: 二つ目はカテゴリ間の相互関係を扱えず、有益な関係性を無視してしまうことがあること。

## Entity Embeddingの手段として、事前学習済みのsemantic埋め込みモデルを使うのはあり??

- IDが意味持ってるっぽいなら、semantic embeddingを使うのは全然あり! っていうか結構主流っぽい!
  - 事前学習済みの言語モデル（BERTやLUKE、Sentence-Transformers系など）をentity embedding（エンティティ埋め込み）に使うのは、今や王道の一つ。
- 有効性: なぜ使われてるのか??
  - 汎用性・転移学習の強さ
    - 事前学習済みモデルは大量データでトレーニング済みだから、新しいタスクや馴染みのない
    - 下流タスク（検索・リンク・クラスタリングetc）で**そのままor微調整（ファインチューニング）するだけで高精度出るケースが多い！**エンティティでも「それっぽい意味」ごとベクトル化できる。
      - まあ最初は固定(freeze)しておけば良さそう!
  - 意味的繋がりの反映
  - 少ないデータでも精度高め
- **カテゴリ特徴はsemantic embedding＋独自embeddingで連結（concatenate）してタワーに入れるチューニングも主流っぽい!**
- 事例:
  - Alibabaの商品推薦システムでは、商品名・属性名・検索クエリをBERT系でembedding。
    - 利点: 新商品も説明文があればembeddingできる！ (**→コールドスタート耐性up!**) 商品IDがない or sparse でも推薦可能
  - Facebook - DeepText / DeepEntity
  - Amazon - 商品レコメンド（Product2Vec + Text）
    - 使ってるentity embeddingは2種類 (行動ベースの学習 + 言語モデルの合わせ技!)
      - 商品ID：Product2Vec（行動ベース） (Item2Vec的なやつ??)
      - 商品タイトル/説明文：FastText/BERTなどによるsemanticな埋め込み (こっちは事前学習済み言語モデルによる埋め込み!)
        - **特にsemanticな埋め込みは cold start対策、関連性向上に特に効く！**
  - 




