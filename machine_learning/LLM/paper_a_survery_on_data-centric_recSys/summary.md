# (仮) Data-centricな推薦システムの論文を読んだ!

## ざっくり本論文のまとめ

## ざっくり背景

- 背景: 推薦システムの重要性と進化
- 制約の変化: データの重要性の増加
- トレンド: Data-Centric Recommender Systemsの登場
  - モデル改善だけじゃなく、データをどうよくするかが重要という潮流。
- Data-Centric Recommender Systemsの基本的な考え方
  - モデルの性能はデータの質と量に依存する
  - 他分野でのData-Centricなアプローチの成功事例
    - NLP: 
    - CV:
  - →RecSysでも同様に良い・多いデータが肝！
    - 質
    - 量
- 研究上のギャップと本論文の貢献
  - 既に研究は活発だが、「Data-Centric RSs全体を整理・体系化したレビュー論文はまだ無い」
- 本論文が提供する4つの視点
Section 2	推薦に使えるデータの種類、Data-Centric RSの形式化
Section 3	推薦データの3つの課題：不完全性・ノイズ・バイアス
Section 4	上記の課題ごとに既存研究を分類・整理
Section 5	将来の有望な研究方向の提案

## 視点1: 推薦に使えるデータの種類、Data-Centric RSの定式化

- 推薦に使われる3つの主要データ:
  - User Profiles:
    - ユーザに関する静的・動的な情報全般（例：年齢、性別、行動履歴、好みなど）
    - ユーザの「特性・ニーズ・興味」を理解するのに重要！
  - Item Profiles:
    - 商品・コンテンツ側の情報（例：ジャンル、ブランド、価格、素材など）
    - アイテムの識別やカテゴリ分類に活用される
  - User-Item Interactions:
    - 行動ログ（例：閲覧、クリック、購入、評価、レビュー）
    - 文脈情報（タイムスタンプ・デバイスなど）も含めて、**ユーザの興味の表れを捉える中心的なデータ**
- Data-Centric Recommender Systemsとは??
  - 定義と基本構造: 
    - Model-Centric RS（モデル改善主軸）とは逆に、**DCRSは「データそのものの改善」によって性能を高めるアプローチ。**
    - 数式で表すと...$D' = f(D)$
      - ここで、$D$は元のデータ、$D'$は改善されたデータ、$f$はデータ改善戦略。
    - Data-Centric RSは、**改善されたデータを既存の任意の推薦モデルで利用できるのが特徴。**
- Data-Centric Recommender Systemsに関する3つのFAQ的問いと回答
  - Q1: Data-Centric RS (データ中心RS)とData-Driven RS (データ駆動RS)は同じなの??
    - 違う!
      - データ駆動RS（Data-Driven）は「データをもとにモデルを設計する」けど、データ自体は変えない。
      - 一方で、DCRSはデータを**“変えて”改善する**ことがコア。
      - → データ駆動RSは本質的にModel-Centricの範疇である（Zha et al. 2023）
  - Q2: なぜData-Centric RSが必要なの??
    - モデルはデータにフィットするように設計される。
    - **データにノイズやバイアスがあると、モデルがそれを学習・強化してしまう**（Zhang et al. 2023a）
    - → モデルだけ改善しても限界があり、データ改善が必要不可欠！
  - Q3: Data-Centric RSはModel-Centric RSに取って代わるの?
    - No! 両者は対立構造ではなく、補完的な関係。
      - DCRSでデータを強化 -> モデル性能UP
      - モデル側の技術を使ってデータを改善することも可能。

## 視点2: 推薦データの3つの課題：不完全性・ノイズ・バイアス

- 推薦データに潜む**3大課題**:
  - Data Incompleteness（不完全性）
  - Data Noise（ノイズ）
  - Data Bias（バイアス）
- Data Incompleteness（不完全性）
  - 主なパターン:
    - ユーザプロフィールの欠落
    - アイテム属性の欠落
    - ユーザ-アイテムインタラクションのsparsity（疎性）
    - 文脈情報の欠如
      - タイムスタンプ、レビュー、場所情報などが抜けている
      - プライバシーやUX上の制約が原因になる（Chae et al. 2019）
- Data Noise（ノイズ）
  - 主なパターン:
    - 冗長データ(Redundant)
      - 同一データの重複 (スクレイピングやログ重複)
      - 例：同じアイテムへの何回ものアクセスが別々の行として記録される
    - 矛盾データ(Inconsistent)
      - ユーザの誤クリック、誤評価
    - スパム・偽データ(Spam/Fake)
      - ボットによる不正データ（例：review bombing）
      - 本物のデータを汚染し、システム全体の信頼性を下げる（Wu et al. 2023）
- Data Bias（バイアス）
  - 主なパターン:
    - ユーザ嗜好の変化(Temporal Shift)
    - アイテム人気の変化(Item Trend Shift)

## 視点3: 上記の課題ごとに既存研究を分類・整理

## 視点4: 将来の有望な研究方向の提案
