## これは何??

- AWS Lake Formationをよく知らなかったので、概要を調査したメモ

## refs

- [AWS Lake Formationの概要を図と用語で整理する](https://qiita.com/sot528/items/8a4c3adf9ba5c2da3fa9)

## ざっくりAWS Lake Formationとは?

- AWSでデータレイクを構築・管理するためのマネージドサービス。
  - 実体は、ほぼAWSの各種サービス(Glue, IAM, S3, etc.)をwrapしたもの。
  - **データレイク専用にアクセス制御を行うために、IAMとは別に独自の権限管理機構を持つ**。
- **Lake FormationはGlueとデータカタログを共有する**。
