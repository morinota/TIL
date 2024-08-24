## refs

- AWS公式のブログ: [Creating a machine learning-powered REST API with Amazon API Gateway mapping templates and Amazon SageMaker](https://aws.amazon.com/jp/blogs/machine-learning/creating-a-machine-learning-powered-rest-api-with-amazon-api-gateway-mapping-templates-and-amazon-sagemaker/)
- Nishikaさんのブログ: [API Gatewayを利用したSageMaker runtime（Multipart/Form-data）の外部公開のための構築](https://zenn.dev/team_nishika/articles/8735aaaa460b45)
- 柏木さんのブログ! これは自前コンテナでSagemakerエンドポイントを作ってる例(クライアントとの接続は、API GatewayではなくECS FargateでML APIを立ててる感じ!): [SageMakerとStep Functionsを用いた機械学習パイプラインで構築した検閲システム（後編）](https://tech.connehito.com/entry/2022/03/28/190436)
- [AWS CDKがなにもわからないので、勉強の為にAPI GatewayとLambdaをデプロイしてみた](https://zenn.dev/ncdc/articles/e900f7a18d3506)

# API GatewayとSagemakerエンドポイントを組み合わせたREST APIの構築

## API Gatewayについてメモ

- 利用料金は、受信したAPIコールの分だけ。API Gatewayのリクエスト数に応じて課金される。
  - 月間、最初の3億3300万リクエストまで: 東京リージョンで　4.25USD/100万リクエスト (=680円くらい)
  - それ以降はどんどん安くなる感じ。
- API Gatewayにおける **Deployment Stage** という概念:
  - ステージは、APIの異なるバージョンや環境(ex. dev, staging, prod)を表現するために使用される。
  - deployment stageの主要なポイント
    - APIの異なるバージョンを簡単に管理できる!
    - APIの環境を分離できる!
    - エンドポイントURLの生成(各ステージには独自のURLが割り当てられる)
      - ex. APIの名前が`my-api`で、ステージ名が`prod`の場合
        - ->エンドポイントURLは`https://<api-id>.execute-api.<region>.amazonaws.com/prod/my-api`

# API GatewayとSagemakerエンドポイントの間にLambdaを挟む必要ある? なくない??

- Nishikaさんのブログによると、「API GatewayではSagemaker Runtimeと直接接続することができるが、**何か込み入ったことをやろうとすると途端に間にLambdaを挟もうと誘惑される**」とのこと...!
  - ちなみにSagemaker Runtimeって??:thinking:
    - **SageMakerエンドポイントとのインターフェースを提供するサービス**。Saegmaker RuntimeのAPIを介して、SageMakerエンドポイントの機能を使える。
    - SageMakerエンドポイントは、モデルをホストするための実体（インフラストラクチャとスケーリング機能を含む）。Sagemaker Runtimeは、エンドポイントにリクエストを送信するためのAPIを提供するサービス。

## API Keyを利用した接続制限

- API Gateway側で設定できるっぽい。
  - 正しいAPIキーを持っていないクライアントからのリクエストを拒否できる。
    - リクエストヘッダーに`X-API-Key`を含めてもらって、API Gateway側でそのキーをチェックすることで制限する感じっぽい。

## カスタムヘッダーを用いた識別子の渡し方

- あんまりusecaseがわかってない...!:thinking:

## 動作確認

- パスパラメータ
  - user_id=U:114521
- クエリパラメータ
  - k=10&inference_type=deterministic
  - k=10&inference_type=stochastic_plackett_luce
  - k=10&inference_type=stochastic_plackett_luce_cached
  - k=10&inference_type=stochastic_gumbel_softmax_trick
  - k=10&inference_type=stochastic_epsilon_greedy
- リクエストヘッダ:

```yml
content-type:application/json
accept:application/json
```

最後にcurlコマンドで動作確認

```shell
curl -X GET "https://z81h3onefa.execute-api.ap-northeast-1.amazonaws.com/temp/recommended-movies/U:114521?k=10&inference_type=deterministic" -H "accept: application/json" -H "content-type: application/json" | jq
```

## cdkから同様のIntegration設定を定義する

一旦、AWS ConsoleからMapping Templateを定義して動作することを確認できた。
あとはそれをcdkで定義すれば良い。

cdk側で定義したリソースと、AWS Consoleでポチポチ定義したリソースを比較して、状態にどのような差異があるのかを確認し、cdk側を調整して両者をほぼ一致させることができた。
