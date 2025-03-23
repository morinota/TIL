## これは何

- Github actionsを雰囲気で使ってたので、ざっくり調査します

## refs

- [GitHub Actions ドキュメント](https://docs.github.com/ja/actions)

## GitHub Actionsの概要

- ビルド、テスト、デプロイのパイプラインを自動化できる**継続的インテグレーションと継続的デリバリー (CI/CD) のためのプラットフォーム**。
  - リポジトリに対するすべての pull request をビルドしてテストしたり、マージされた pull request を運用環境にデプロイしたりするワークフローを作成できる。(うんうん、認識あってる...!)
- 実行されるインスタンス。
  - Github actionsのワークフローの実行には、**Linux、Windows、macOS の仮想マシンが提供**される。(後述されるRunnerという概念!)
  - もしくは、自社のクラウドインフラなどで独自のself-hostされたインスタンスを使うこともできる。

## Github Actionsにおける概念(コンポーネント)たち

- 4つの概念(コンポーネント)が出てくる
  - ワークフロー
  - イベント
  - ジョブ
  - アクション
  - ランナー

### ワークフロー

- 1つ以上のジョブで構成される自動化プロレス。
- リポジトリ内の `.github/workflows` ディレクトリ内のyamlファイルによって定義される。
- リポジトリ内のイベントによってトリガーされる。
- また、**手動でトリガーしたり、指定されたスケジュールでトリガー**することもできる。(あ、そうなのか...!:thinking:)
- **1つのリポジトリ内で複数のワークフローを定義できる**。
  - あるワークフローから別のワークフローを参照することもできるっぽい??

### イベント

- ワークフロー実行をトリガーする、リポジトリ内の特定のactivity。
  - ex. PR作成時、issue作成時、リポジトリにcommitがpushされた時、など。
  - [トリガー可能なイベント一覧](https://docs.github.com/ja/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows)

### ジョブ

- 同じランナーで実行される、ワークフロー内の一連のステップ(**じゃあジョブはステップ集合ってことか!**)。
  - 各ステップは、シェルスクリプト、またはアクション(後述)のいずれか。
- **同じジョブ内の各ステップは同じランナー(i.e. インスタンス?)で実行されるため、あるステップから別のステップにデータを共有できる**。
  - ex. アプリをビルドするステップの後に、ビルドされたアプリをテストするステップを繋げられる。
    - **データを共有させたい場合は、同じジョブに両ステップを含める必要があるってことか**...!:thinking:
- 必要に応じて、ジョブ間に依存関係を持たせられる。
  - **デフォルトでは、ジョブ間に依存関係はなく、並列で実行される**。(あ、じゃあ別ランナーで実行されるのか...!:thinking:)
  - あるジョブBが別のジョブAに依存する場合、ジョブBはジョブAの完了後に実行される。
  - 並列と直列を混ぜたりもあり!
    - ex.) まず複数のビルドジョブを並列で実行して、それらのジョブ達に依存するパッケージ化ジョブを実行する。
  
### アクション

- GitHub Actions専用のカスタムアプリケーション。ジョブの中身として指定できる。
  - たぶんutils的な処理をわざわざコード書かなくて済むように、GitHubがwrapperを提供してくれてるやつ...! :thinking:
- 独自のアクションを記述することも、GitHub Marketplaceからアクションを見つけることもできる。

### ランナー

- ワークフローがトリガーされると起動するサーバー(i.e. リソース?)
  - 各ワークフロー実行は、新しくプロビジョニングされた仮想マシンで実行される。
- **各ランナーは一度に1つのジョブを実行する**。(not 1つのワークフロー...!)
  - 並列の2つのジョブを持つワークフローは、2つのランナーで実行されるってこと?? :thinking:

## ワークフローファイルのyamlの書き方

- ワークフローファイル達は`.yml`もしくは`.yaml`で記述され、リポジトリの `.github/workflows` ディレクトリ以下に保存する必要がある。
- 0から書かなくても、ワークフローテンプレートを使って最小限の書き換えで始められるらしい。
  - **まあ大体やりたいことのパターンは決まってる感あるので、既存リポジトリのコピペで大抵のことは事足りそう**...!:thinking:

### ワークフローファイルの構文

- `name`キー: ワークフローの名前を指定。
- `run-name`キー: ある一回のワークフロー実行の名前。(式とか含められる!)
- `on`キー: ワークフローをトリガーするイベントを指定。
  - 色々設定方法のレパートリーがありそう: https://docs.github.com/ja/actions/writing-workflows/workflow-syntax-for-github-actions#on
- `permissions`キー: ワークフロー内のジョブに対する特定のアクセス権限たちを指定する。
  - 最上位に指定してワークフロー内のすべてのジョブに適用することもできるし、個別のジョブに対して指定することもできる。
  - refs: https://docs.github.com/ja/actions/writing-workflows/workflow-syntax-for-github-actions#permissions
- `env`キー: ワークフロー内のジョブに渡す環境変数を指定する。map形式 `KEY: VALUE` で指定する。
  - 任意の粒度(ワークフロー全体、ジョブ全体、ジョブ内のステップ)に対して設定できる。

#### `jobs`キー: ワークフローに含まれるジョブの集合

- 各ジョブは`runs-on`で指定されたランナー環境で実行される。

例:

```yaml
name: ワークフロー名
on: [push]
env:
  KEY1: VALUE1
  KEY2: VALUE2
jobs:
    job名1:
        runs-on: ubuntu-latest
        steps:
            - name: ステップ名1(シェルスクリプト使う場合)
              run: echo Hello, world!
            - name: ステップ名2(アクション使う場合)
              uses: actions/setup-python@v5
              with:
                  python-version: 3.12
    job名2:
        ...
```


## Github Actionsでのシークレット値の使用

refs: [GitHub Actions でのシークレットの使用](https://docs.github.com/ja/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)

- **シークレット値は3種類の粒度で設定できる: organization単位、repository単位、repository environment単位**。
  - organization単位のシークレットは、organizationのオーナーのみが作成or編集できる。
  - repository単位、repository environment単位のシークレットは、**repositoryのオーナーのみ**が作成or編集できる。
- シークレット値は、GitHubのWeb UI上で設定できる。
- ちなみに、シークレット値に関する制限:
  - 個数制限: 最大1000個のorganizationシークレット、100個のrepositoryシークレット、100個のrepository environmentシークレットを作成できる。
  - サイズの制限: 最大48KBのシークレット値を保存できる。
- ワークフローファイル内では `${{secrets.XXX}}` という記法でシークレット値を参照できる。(secretsコンテキスト)
  - 参照先のシークレット値が存在しない場合、空文字列が返される。

```yaml
steps:
  - name: Hello world action
    with: # Set the secret as an input
      super_secret: ${{ secrets.SuperSecret }}
    env: # Or as an environment variable
      super_secret: ${{ secrets.SuperSecret }}
```

- 注目: **セキュリティの観点で、可能であればCLIではなく環境変数としてシークレット値を渡すことが推奨されるらしい...!!**
