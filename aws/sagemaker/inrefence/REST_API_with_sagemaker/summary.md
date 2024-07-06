## refs:

- AWS公式のブログ: [Creating a machine learning-powered REST API with Amazon API Gateway mapping templates and Amazon SageMaker](https://aws.amazon.com/jp/blogs/machine-learning/creating-a-machine-learning-powered-rest-api-with-amazon-api-gateway-mapping-templates-and-amazon-sagemaker/)
- Nishikaさんのブログ: [API Gatewayを利用したSageMaker runtime（Multipart/Form-data）の外部公開のための構築](https://zenn.dev/team_nishika/articles/8735aaaa460b45)

# API GatewayとSagemakerエンドポイントを組み合わせたREST APIの構築

## API Gatewayについてメモ:

- 利用料金は、受信したAPIコールの分だけ。API Gatewayのリクエスト数に応じて課金される。
  - 月間、最初の3億3300万リクエストまで: 東京リージョンで　4.25USD/100万リクエスト (=680円くらい)
  - それ以降はどんどん安くなる感じ。

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
