## refs:

- [Boto3 を使ってコンパイル済みモデルをデプロイする](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/neo-deployment-hosting-services-boto3.html)
- [満たすべき前提条件](https://docs.aws.amazon.com/sagemaker/latest/dg/neo-deployment-hosting-services-prerequisites.html)
- [Inference Container Images](https://docs.aws.amazon.com/sagemaker/latest/dg/neo-deployment-hosting-services-container-images.html)

## 満たすべき前提条件

- その1:
  - DockerイメージのAmazon ECR URI。Inference Container Imagesのリストからニーズに合ったものを選択できる。
- その2:エントリーポイントのスクリプトファイル
  - 2-1 PyTorchとMXNetモデルの場合:
    - 2-1-1 Sagemakerを使用してモデルを学習した場合:
      - hogehoge
    - 2-1-2 Sagemakerを使用せずにモデルを学習した場合:
      - 推論時に使用できるエントリーポイントのスクリプト(例: `inference.py`)ファイルを提供する必要がある。
      - **フレームワークに応じて、推論スクリプトの場所は準拠する必要がある**。(これがエラーの原因っぽい...!)
      - 推論スクリプトは以下の関数を実装する必要がある:
        - `model_fn`
        - `input_fn`
        - `predict_fn`
        - `output_fn`
        - (もしくは下3つの代わりに、`input_fn`、`predict_fn`、`output_fn`を組み合わせた`transform_fn`を実装してもOKらしい...!)
  - 2-2 inf1インスタンスまたはoonx, xgboost, kerasコンテナイメージを使用する場合:
    - その他のNeo Inference-optimized container imageを使用する場合、エントリーポイントのスクリプトは、Neo Deep Learning Runtime用の以下の関数を実装する必要がある:
      - `neo_preprocess`: 入力されたリクエストペイロードを前処理する関数。
      - `neo_postprocess(result)`: Neo Deep Learning Runtimeからの予測出力をレスポンスボディに変換する関数。
  - 2-3 TensorFlowモデルの場合:
    - データがモデルに送られる前後に、カスタムの前処理&後処理ロジックを必要とする場合、推論時に使用できるエントリーポイントのスクリプト(例: `inference.py`)ファイルを提供する必要がある。
    - その場合は、以下の関数を実装する必要がある:
      - `input_handler`
      - `output_handler`
- その3:
  - コンパイル済みのmodel artifactsを含む S3 URI。

## Pytorch imageを使う場合に準拠すべきディレクトリ構造

- 参考: [Model Directory Structure for PyTorch](https://sagemaker.readthedocs.io/en/stable/frameworks/pytorch/using_pytorch.html#model-directory-structure)

PyTorchのバージョン1.2以降では、`model.tar.gz`の中身は以下のように整理されているべき:

- model filesは、top-level directoryに配置される。
- 推論スクリプト(と他のsource files)は、`code/` directory以下に配置される。
  - 推論スクリプトの適切なルールは、[The SageMaker PyTorch Model Server](https://sagemaker.readthedocs.io/en/stable/frameworks/pytorch/using_pytorch.html#id4)を参照。
- optionの 依存関係 fileは、`code/requirments.txt`に配置される。
  - 詳細は、[Using third-party libraries](https://sagemaker.readthedocs.io/en/stable/frameworks/pytorch/using_pytorch.html#using-third-party-libraries)を参照。

例えば以下。

```
model.tar.gz/
|- model.pth
|- code/
  |- inference.py
  |- requirements.txt  # only for versions 1.3.1 and higher
```
  
`Pytorch`クラスと`PytorchModel`クラスは、framework version 1.2 以上に設定されてる限り、推論スクリプト(と他のsource files)を含むように `model.tar.gz`を構築する。


## Pytorch imageを使う場合の推論スクリプトのルール:

- 参考:[The SageMaker PyTorch Model Server](https://sagemaker.readthedocs.io/en/stable/frameworks/pytorch/using_pytorch.html#id4)

- デプロイされたPyTorchエンドポイントはは、**Sagemaker Pytorch Model Server**を実行する。
  - モデルサーバは、保存されたモデルをloadし、Sagemaker InvokeEndpoint API呼び出しに応答して、推論を実行する。
- Sagemaker Pytorch Model Serverは2つのComponentを設定できる:
  - 1つ目: model loading: 保存したモデルをdeserializeする。
  - 2つ目: model serving: InvokeEndpoint APIリクエストを、loadされたモデル呼び出しに変換する。
  
PyTorchコンストラクタに渡したPythonソースファイルに関数を定義することで、Pytorchモデルサーバを構成できる:

###  Load a Model

- SageMaker PyTorch Model Serverは、`model_fn`関数を呼び出して、保存されたモデルをloadする。
- `model_fn`関数は、以下のsignatureを持つ必要がある:
  - `model_fn(model_dir, context):
    - contextはオプションの引数。GPU IDやbatch sizeなどの追加serving情報を含む。
  - model_fn関数は、model servingに使用できるモデルオブジェクトを返す必要がある。

### Serve a PyTorch Model

- Sagemaker PyTorch Model Serverは、3つのステップ`input_fn`, `predict_fn`, `output_fn`関数を呼び出して、InvokeEndpoint APIリクエストを処理する。
- Pytorch Model Server内部では、以下のように呼び出される:

```python
# Deserialize the Invoke request body into an object we can perform prediction on
# Invokeリクエストボディをデシリアライズして、予測を実行できるオブジェクトに変換する
input_object = input_fn(request_body, request_content_type, context)

# Perform prediction on the deserialized object, with the loaded model
# デシリアライズされたオブジェクトに対して、ロードされたモデルで予測を実行する
prediction = predict_fn(input_object, model, context)

# Serialize the prediction result into the desired response content type
# 予測結果を、希望のレスポンスコンテンツタイプにシリアライズする
output = output_fn(prediction, response_content_type, context)
```

SageMaker PyTorch モデルサーバは、上記の関数のデフォルト実装を提供する。
かつ独自の実装を提供することもできる。
