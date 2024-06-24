## refs:

- [awsの開発者ガイド](https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/train-vpc.html)

# TrainingJobとVPC

## 既存のVPC上でTrainingJobを実行させる方法

- TrainingJobへのアクセスを制御するためには、インターネットにアクセスできないprivate subnetを持つAmazon VPCでそれらを実行させると良い。
  - VPC上でTrainingJobを実行させるには、`VpcConfig`に`Subnets`と`SecurityGroupIds`を指定すれば良い...!

```json
VpcConfig: {
      "Subnets": [
          "subnet-0123456789abcdef0",
          "subnet-0123456789abcdef1",
          "subnet-0123456789abcdef2"
          ],
      "SecurityGroupIds": [
          "sg-0123456789abcdef0"
          ]
        }
```

- 上記を指定することにより...
  - Sagemakerは、サブネットとセキュリティグループの詳細を使用してnetwork interfaceを作成し、TrainingJobを実行するコンテナインスタンスにアタッチする。
  - network interfaceは、指定されたサブネット内のIPアドレスを持ち、指定されたセキュリティグループのルールに従ってトラフィックを制御する。
  - **TrainingJobは、VPC内に存在するリソースに接続できるようになる**。
