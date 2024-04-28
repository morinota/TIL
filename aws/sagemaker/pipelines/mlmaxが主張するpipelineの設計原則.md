## refs

- awslabs/mlmaxのドキュメント: [ML Training and Inference Pipeline](https://mlmax.readthedocs.io/en/latest/INFERENCE.html)
- [awslabs/mlmaxのPRFAQ](https://github.com/awslabs/mlmax/blob/main/PRFAQ.md)

## awslabsってなんだ?

- awslabs(Amazon Web Services - Labs)とは、

## mlmaxってなんだ??

MLエンジニアやデータサイエンティストは、AWS上で本番環境に対応したMLソリューションを素早く作成し、利用することができる。mlmaxは、**カスタムMLソリューションを本番環境に提供するためのテンプレート例を提供**しているので、設計の選択をあまりすることなく、すぐに始めることができる。

- mlmaxのモチベーションは?
  - ML solutionを本番環境にdeliverするのは難しい。
    - 何から始めればいいのか、どんなツールを使えばよいのか、そしてそれが正しいのかどうかを知るのは難しい。
  - 多くの場合、各専門家がそれぞれの経験に基づいて異なる方法で行うか、社内で開発された所定のツールを使用する。
  - -> いずれの選択肢をとっても、まず何をすべきか決め、次にインフラを実装し維持するために多くの時間を費やす必要がある。
    - 既存のツールは数多くあるが、それらを組み合わせてrobustな本番用インフラを構築するのは時間がかかる...!
- mlmaxはなに?
  - **カスタムMLソリューションを本番環境に提供するための example templates**。

## mlmaxが主張するML pipelineのDesign principles(設計原則)

- 1. Separate definition and runtime for training/inference pipelines (訓練/推論パイプラインの定義と実行を分離する)
  - hogehoge
- 2. Use the same code for pre-processing in training and inference (訓練と推論で前処理に同じコードを使用する)
  - hogehoge
- 3. Traceability between components of the training and inference pipelines (訓練と推論パイプラインのcomponent間のトレーサビリティ)
  - Traceabilityってなんだ?
- 4. Code should provide consistent results whereever it is run(コードはどこで実行されても一貫した結果を提供する)
  - hogehoge
- 5. Promote modularity in the development of Training and Inference solutions(訓練と推論ソリューションの開発においてモジュール性を促進する)
- 6. Use on-demand compute, only paying for it when you need it for a specific job(必要なときにのみコンピューティングをオンデマンドで使用し、特定のジョブに必要なときにのみ支払う)
