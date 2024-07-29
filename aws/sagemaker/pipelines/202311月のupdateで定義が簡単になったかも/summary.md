<!-- title: Sagemaker Python SDKのstepデコレータは機械学習パイプラインのグルーコードを減らすか? -->

# はじめに

AWS re:Invent 2023では、Amazon Sagemakerについても多数のアップデートが発表されました。
その中の1つに、**Sagemaker Python SDKの`step`デコレータ**があります。

AWS公式のポストでは以下のように述べられています: [Amazon SageMaker Pipelines now provide a simplified developer experience for AI/ML workflows](https://aws.amazon.com/about-aws/whats-new/2023/11/amazon-sagemaker-pipelines-developer-ai-ml/?nc2=h_mo-lang)

(deepLによる翻訳)

> 新しい Amazon SageMaker Pipelines の開発者エクスペリエンスでは、数分でMLコードを様々なMLステップの自動化されたDAG（Directed Acyclic Graph）に変換することができます。ML ワークフローを作成するには、既存の Python 関数を '@step' デコレーターでアノテートし、最終ステップをパイプライン作成 API に渡します。Amazon SageMaker は、アノテーションされた Python 関数間の依存関係を自動的に解釈し、それぞれのカスタムパイプラインステップを作成し、パイプライン DAG を生成します。

また、classmethodさんのブログでも以下のように紹介されていました: [AWS re:Invent 2023 で発表されたAmazon SageMakerに関するアップデートや記事をまとめてみた #AWSreInvent](https://dev.classmethod.jp/articles/update-reinvent2023-sagemaker-summary/)

> Python SDK(SageMaker SDK)が改良され、カスタムステップとして@stepデコレータを使ったstepの構築が可能となりました。また前述の通り、Notebook Job用のstepも追加となっています。 @stepデコレータはかなり興味深いアップデートでして、パイプラインに組み込みたい関数にデコレータを付与するだけで、従来の記述よりかなり簡素化した表現でpipelinesに組み込むことが可能そうな機能となっています。

僕はこれらを見て、なんとなく step デコレータに興味が出てきました!
機械学習を使ってプロダクトに価値を与えたいと考える上で、新しいアイデアをより高速により簡単にプロダクトに乗せて実験できるようにすることは非常に重要だと思っています。
それを踏まえて、stepデコレータが本当にpipelineの定義を簡単にしてくれるのであれば、機械学習パイプラインを開発・運用する上で魅力的な選択肢になるのかもと考えました。

# Sagemaker Pipelinesとは? stepデコレータとは?

## 機械学習パイプライン

## SageMaker Pipelinesとは

## stepデコレータとは??

- Python関数をpipelineの1つのstepに変換するデコレータ。
- 変換されたstepは、pipeline実行時にTrainingJobとして実行される。

たとえば以下のように、stepデコレータは任意のPython関数にデコレートします。

```python
@step(name="PreprocessStep")
def preprocess(raw_data_s3uri: str)->pl.DataFrame:
    import polars as pl
    # rawデータの読み込み
    df = pl.read_parquet(raw_data_s3uri)

    # 必要に応じてなんらかの前処理
    # ...

    # 学習するための準備が整ったデータを返す
    return df

@step(name="TrainStep")
def train(train_df: pl.DataFrame)->Model:
    # モデルの学習
    model = HogehogeModel()
    model.fit(train_df)

    # 学習したモデルを返す
    return model

@step(name="EvaluateStep")
def evaluate(model: Model)->dict[str,float]:
    # モデルの評価
    metrics = evaluate(model)
    report_dict = {
        "hoge_metric": metrics["hoge_metric"]
        "fuga_metric": metrics["fuga_metric"]
    }

    # モデルの評価結果を返す
    return report_dict
```

stepデコレータをつけた関数は`DelayedReturn`オブジェクトを返すようになる

- `DelayedReturn`の意味合い: 「関数は即座に実行はされず、パイプライン実行時にステップが走るタイミングに実行されて結果を返す」
- 各ステップの`DelayedReturn`オブジェクトはそのステップの出力を表し、**他のステップの入力として使うことができる**
  - これにより、**パイプライン内の各ステップ間の依存関係を簡単に表現できる**。
- デコレートするPython関数の返り値は、単数型でも、tuple型やlist型やdict型などのコレクション型でもOK
  - コレクション型の場合は以下のように参照できる
    - `a_member = a_delayed_return[2]`
    - `a_member = a_delayed_return['a_key']`
    - `a_member = a_delayed_return[2]['a_key']`

感想メモ:thinking:
- 各ステップはTrainingJobとして実行される事になるが、`DelayedReturn`オブジェクトのおかげで、**各ステップ間の接続方法の実装を開発者が意識する必要がなくなる**気がする。
  - ここがstepデコレータの特徴?? **ステップ間の接続方法が抽象化・情報隠蔽されてる感じ**...!
  - stepデコレータを使わない場合は、ステップ間のデータの接続というか受け渡しを開発者自身が認識する必要があった...!:thinking:
    - ex. 「前のステップがS3のここに成果物を出力するから、次のステップの入力としてこのS3 uriを指定して...」


そして、pipeline step化した関数たちを1つのPipelineとして定義します。

```python
from sagemaker.workflow.pipeline import Pipeline

raw_data_s3_uri = "s3://my-bucket/path/to/raw_data.parquet"

preprocess_step = preprocess(raw_data_s3_path=raw_data_s3_uri)
train_step = train(train_df=preprocess_step)
evaluate_step = evaluate(model=train_step)

pipeline = Pipeline(
    name="my-sample-pipeline",
    steps=[
        preprocess_step,
        train_step,
        evaluate_step,
    ],
    sagemaker_session=pipeline_session,
)

# pipelineの定義を出力
print(pipeline.definition())
# pipelineをデプロイ
pipeline.upsert()
# pipelineをon-demand実行 (なんらかtriggerを元に実行させる場合はEventBridgeのルールを追加する)
pipeline.start()
```

ざっくり上記のような感じで、1本の機械学習パイプラインを定義できるようです。
なんとなく、各ステップのビジネスロジックのコード以外のパイプラインを定義するためのコードの量はかなり少なくて済みそう...??

# 実際に触ってみる: stepデコレータを使うver.と使わないver.の比較



## 実装するパイプラインの問題設定

## stepデコレータを使わないver.

## stepデコレータを使うver.


# 気づき: stepデコレータによってSagemaker PipelinesによるML Pipelineの定義が簡単になったのか??


## 参考文献

- AWS公式のポスト: [Amazon SageMaker Pipelines now provide a simplified developer experience for AI/ML workflows](https://aws.amazon.com/about-aws/whats-new/2023/11/amazon-sagemaker-pipelines-developer-ai-ml/?nc2=h_mo-lang)
- classmethodさんのブログ: [AWS re:Invent 2023 で発表されたAmazon SageMakerに関するアップデートや記事をまとめてみた #AWSreInvent](https://dev.classmethod.jp/articles/update-reinvent2023-sagemaker-summary/)
- step decoratorの公式ドキュメント:[@step decorator](https://sagemaker.readthedocs.io/en/stable/workflows/pipelines/sagemaker.workflow.pipelines.html#step-decorator)
- サンプルnotebook: [Basic Pipeline for Batch Inference using Low-code Experience for SageMaker Pipelines](https://github.com/aws/amazon-sagemaker-examples/blob/main/sagemaker-pipelines/step-decorator/batch-examples/basic-pipeline-batch-inference.ipynb)
- AWS communiryのstepデコレータの記事: [Sagemaker Pipelines using step decorators](https://community.aws/content/2bFfwOMvMaWfOuwUy30HMF1qgGb/sagemaker)
