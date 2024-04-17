## refs

- hiranoさんの書いてくれたやつ=[AWS CDKにテストを導入する](https://zenn.dev/enterrocken/articles/e60a2f267f385b#%E3%81%82%E3%81%A8%E6%9B%B8%E3%81%8D)
- AWSのエンジニアさんの短い資料[CDKテスト入門](https://pages.awscloud.com/rs/112-TZM-766/images/CDK%E3%81%A7%E3%82%82%E3%83%86%E3%82%B9%E3%83%88%E3%81%8C%E3%81%97%E3%81%9F%E3%81%84.pdf)
- これが公式のドキュメントっぽい? [コンストラクトのテスト](https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/testing.html)

# CDKのテストとassertionsモジュール

- CDKはインフラのコードに対してテストを書ける。
  - assertionsモジュールは全言語に対応してる。
- テストの流れ:
  - 1. テスト対象のstackインスタンスを作成
  - 2. CloudFormationのテンプレートを生成
  - 3. Assertする
    - A. Snapshot Testing:
      - 生成されたCFnテンプレートを以前のものと比較し、両者に差分があるかをテストする手法
      - cdk diffと同じ?? リファクタリング目的みたいな??
    - B. Fine-grained Assertions:
      - 生成されたCFnのリソースやアウトプットが、期待通りのものかをテストする手法。
      - 主にAssertionsモジュールのfunctionを使う。
      - (通常の単体テストのようなイメージ...!)

例:

```typescript
import { Stack } from "aws-cdk-lib";
import { Template } from "@aws-cdk/assertions";

// Act
const stack = new Stack();
const template = Template.fromStack(stack);

// Assert
// Functionが2つ作られていることを確認
template.resourceCountIs("AWS::Lambda::Function", 2);
// Resource Matching & Retrieval
// Propertyが期待通りのものかを確認
template.hasResourceProperties("AWS::S3::Bucket", {
  BucketName: "myBucket",
});
```
