## refs

- hiranoさんの書いてくれたやつ=[AWS CDKにテストを導入する](https://zenn.dev/enterrocken/articles/e60a2f267f385b#%E3%81%82%E3%81%A8%E6%9B%B8%E3%81%8D)
- AWSのエンジニアさんの短い資料[CDKテスト入門](https://pages.awscloud.com/rs/112-TZM-766/images/CDK%E3%81%A7%E3%82%82%E3%83%86%E3%82%B9%E3%83%88%E3%81%8C%E3%81%97%E3%81%9F%E3%81%84.pdf)
- これが公式のドキュメントっぽい? [コンストラクトのテスト](https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/testing.html)

# CDKのテストとassertionsモジュール

- AWS CDKを使用すると、インフラストラクチャは、他のコードと同様にテスト可能になる。
  - AWS CDKのassertionsモジュールは全言語に対応してる。
- テストの流れ:
  - 1. テスト対象のstackインスタンスを作成
  - 2. stackインスタンスからCloudFormationテンプレートを作成
  - 3. Assertする
- 二種類のテスト手法:
  - 手法1 **Fine-grained Assertions**:
    - 生成されたCFnのリソースやアウトプットが、期待通りのものかをテストする手法。
    - 最もよく使われる
    - 主にAssertionsモジュールのfunctionを使う。
    - (通常の単体テストのようなイメージ...!)
      - regressionを検出したり、テスト駆動開発で新機能を開発する際のも便利。
  - 手法2 **Snapshot Testing**:
    - 生成されたAWS CloudFormationテンプレートを、以前に保存されたbaselineテンプレートと比較する手法。(cdk diffと同じ?? リファクタリング目的みたいな??:thinking:)
    - リファクタリングされたコードが、オリジナルとまったく同じように動作することを確認できるため、リファクタリングに便利。

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

# 手順:

- 1. テストフレームワークをインストール
  - `npm install --save-dev @aws-cdk/assertions`
- 2．テスト用のディレクトリを追加する
  - `mkdir test`
- 3. プロジェクトの`package.json`を編集して、NPMにテストの実行方法を知らせる。

```json
{
  ...
  "scripts": {
    ...
    "test": "jest"
  },
  "devDependencies": {
    ...
    "@types/jest": "^24.0.18",
    "jest": "^24.9.0"
  },
  "jest": {
    "moduleFileExtensions": ["js"]
  }
}
```

- 4. stackを定義する。
- 5. Fine-grained Assertionテストを記述する。

(state machine stackというのが、期待するリソースを定義したもの??)

```typescript
import { Capture, Match, Template } from "aws-cdk-lib/assertions";
import * as cdk from "aws-cdk-lib";
import * as sns from "aws-cdk-lib/aws-sns";
import { StateMachineStack } from "../lib/state-machine-stack";

describe("StateMachineStack", () => {
  test("synthesizes the way we expect", () => {
    const app = new cdk.App();

    // Since the StateMachineStack consumes resources from a separate stack
    // (cross-stack references), we create a stack for our SNS topics to live
    // in here. These topics can then be passed to the StateMachineStack later,
    // creating a cross-stack reference.
    const topicsStack = new cdk.Stack(app, "TopicsStack");

    // Create the topic the stack we're testing will reference.
    const topics = [new sns.Topic(topicsStack, "Topic1", {})];

    // Create the StateMachineStack.
    const stateMachineStack = new StateMachineStack(app, "StateMachineStack", {
      topics: topics, // Cross-stack reference
    });
    // Prepare the stack for assertions.
    const template = Template.fromStack(stateMachineStack);
    // Assert it creates the function with the correct properties...
    template.hasResourceProperties("AWS::Lambda::Function", {
      Handler: "handler",
      Runtime: "nodejs14.x",
    });
    // Creates the subscription...
    template.resourceCountIs("AWS::SNS::Subscription", 1);

}
```

- 5. テストの実行
  - `tsc && npm test`
