## link リンク

- https://neptune.ai/blog/organizing-ml-monorepo-with-pants https://neptune.ai/blog/organizing-ml-monorepo-with-pants

# Organizing ML Monorepo With Pants パンツでMLモノレポを整理する

Have you ever copy-pasted chunks of utility code between projects, resulting in multiple versions of the same code living in different repositories? Or, perhaps, you had to make pull requests to tens of projects after the name of the GCP bucket in which you store your data was updated?
プロジェクト間でユーティリティコードの塊をコピーペーストした結果、同じコードの複数のバージョンが異なるリポジトリに存在することになったことはありませんか？あるいは、データを保存しているGCPバケットの名前が更新された後、何十ものプロジェクトにプルリクエストを行わなければならなかったことはありませんか？

Situations described above arise way too often in ML teams, and their consequences vary from a single developer’s annoyance to the team’s inability to ship their code as needed.
上記のような状況は、MLチームではあまりに頻繁に起こり、その結果は、一人の開発者の迷惑から、チームがコードを必要なときに出荷できなくなることまで、様々である。
Luckily, there’s a remedy.
幸い、救済策はある。

Let’s dive into the world of monorepos, an architecture widely adopted in major tech companies like Google, and how they can enhance your ML workflows.
Googleのような大手ハイテク企業で広く採用されているアーキテクチャであるmonoreposの世界に飛び込み、MLワークフローをどのように強化できるかを考えてみよう。
A monorepo offers a plethora of advantages which, despite some drawbacks, make it a compelling choice for managing complex machine learning ecosystems.
モノレポは、いくつかの欠点はあるものの、複雑な機械学習のエコシステムを管理する上で説得力のある選択肢となる、多くの利点を提供する。

We will briefly debate monorepos’ merits and demerits, examine why it’s an excellent architecture choice for machine learning teams, and peek into how BigTech is using it.
monoreposのメリットとデメリットを簡単に議論し、機械学習チームにとって優れたアーキテクチャーの選択肢である理由を検証し、BigTechがどのように利用しているかを覗き見る。
Finally, we’ll see how to harness the power of the Pants build system to organize your machine learning monorepo into a robust CI/CD build system.
最後に、Pantsビルドシステムのパワーを利用して、機械学習モノレポを堅牢なCI/CDビルドシステムに編成する方法を紹介する。

Strap in as we embark on this journey to streamline your ML project management.
MLプロジェクト管理を効率化する旅に出かけましょう。

# What is a monorepo? モノレポとは？

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2023/08/Monorepo.png?resize=1536%2C1536&ssl=1)

A monorepo (short for monolithic repository) is a software development strategy where code for many projects is stored in the same repository.
モノレポ（モノリシック・リポジトリの略）とは、多くのプロジェクトのコードを同じリポジトリに格納するソフトウェア開発戦略のことである。
The idea can be as broad as all of the company code written in a variety of programming languages stored together (did somebody say Google?) or as narrow as a couple of Python projects developed by a small team thrown into a single repository.
そのアイデアは、さまざまなプログラミング言語で書かれた会社のコードがすべて一緒に保存されているような広範なものから（誰かがGoogleと言ったか）、小さなチームが開発したPythonのプロジェクトが2つほど1つのリポジトリに放り込まれているような狭いものまである。

In this blog post, we focus on repositories storing machine learning code.
このブログでは、機械学習コードを格納するリポジトリに焦点を当てる。

# Monorepos vs. polyrepos モノレポス対モノレポス ポリレポス

Monorepos are in stark contrast to the polyrepos approach, where each individual project or component has its own separate repository.
モノレポは、個々のプロジェクトやコンポーネントがそれぞれ独立したリポジトリを持つポリレポアプローチとは対照的だ。
A lot has been said about the advantages and disadvantages of both approaches, and we won’t go down this rabbit hole too deep.
この2つのアプローチの長所と短所については多くのことが語られているので、あまり深入りするつもりはない。
Let’s just put the basics on the table.
テーブルの上に基本的なことを並べよう。

The monorepo architecture offers the following advantages:
モノレポ・アーキテクチャーには次のような利点がある：

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2023/08/Monorepos-vs.-polyrepos-1.png?resize=1536%2C804&ssl=1)

- Single CI/CD pipeline, meaning no hidden deployment knowledge spread across individual contributors to different repositories; 単一のCI/CDパイプラインは、異なるリポジトリへの個々の貢献者にまたがる隠れたデプロイの知識がないことを意味する；

- Atomic commits, given that all projects reside in the same repository, developers can make cross-project changes that span across multiple projects but are merged as a single commit; アトミックコミットでは、すべてのプロジェクトが同じリポジトリに存在するため、開発者は複数のプロジェクトにまたがる変更を、単一のコミットとしてマージすることができます；

- Easy sharing of utilities and templates across projects;Easy unification of coding standards and approaches; プロジェクト間でユーティリティやテンプレートを簡単に共有できる。コーディング標準やアプローチを簡単に統一できる；

- Better code discoverability. より良いコード発見性。

Naturally, there are no free lunches.
当然、フリーランチはない。
We need to pay for the above goodies, and the price comes in the form of:
その代償は次のようなものだ：

- Scalability challenges: As the codebase grows, managing a monorepo can become increasingly difficult. At a really large scale, you’ll need powerful tools and servers to handle operations like cloning, pulling, and pushing changes, which can take a significant amount of time and resources. スケーラビリティの課題： コードベースが大きくなるにつれ、モノレポの管理はますます難しくなる可能性がある。 本当に大規模になると、クローン作成、プル、変更のプッシュなどのオペレーションを処理するための強力なツールとサーバーが必要になり、かなりの時間とリソースを費やすことになる。

- Complexity: A monorepo can be more complex to manage, particularly with regard to dependencies and versioning. A change in a shared component could potentially impact many projects, so extra caution is needed to avoid breaking changes. 複雑さ： モノレポは、特に依存関係やバージョン管理に関して、管理が複雑になる可能性がある。 共有コンポーネントの変更は、多くのプロジェクトに影響を与える可能性があるため、変更を壊さないように細心の注意が必要である。

- Visibility and access control: With everyone working out of the same repository, it can be difficult to control who has access to what. While not a disadvantage as such, it could pose problems of a legal nature in cases where code is subject to a very strict NDA. 可視性とアクセス制御： 全員が同じリポジトリで作業しているため、誰が何にアクセスできるかを管理するのが難しい場合がある。 そのようなデメリットはないが、コードが非常に厳格なNDAの対象となる場合、法的な問題を引き起こす可能性がある。

The decision as to whether the advantages a monorepo offers are worth paying the price is to be determined by each organization or team individually.
モノレポが提供する利点が対価を払うに値するかどうかは、各組織やチームが個別に判断することである。
However, unless you are operating at a prohibitively large scale or are dealing with top-secret missions, I would argue that – at least when it comes to my area of expertise, the machine learning projects – a monorepo is a good architecture choice in most cases.
しかし、法外に大規模な運用や極秘ミッションを扱うのでなければ、少なくとも私の専門分野である機械学習プロジェクトに関しては、ほとんどの場合モノレポが良いアーキテクチャの選択だと主張したい。

Let’s talk about why that is.
その理由について話そう。

# Machine learning with monorepos モノレポによる機械学習

There are at least six reasons why monorepos are particularly suitable for machine learning projects.
モノレポが機械学習プロジェクトに特に適している理由は、少なくとも6つある。

1. Data pipeline integration データパイプラインの統合

2. Consistency across experiments 実験間の一貫性

3. Simplified model versioning 簡易モデル・バージョニング

4. Cross-functional collaboration 部門を超えたコラボレーション

5. Atomic changes 原子の変化

6. Unification of coding standards コーディング標準の統一

## Data pipeline integration データパイプラインの統合

Machine learning projects often involve data pipelines that preprocess, transform, and feed data into the model.
機械学習プロジェクトでは、データを前処理し、変換し、モデルに送り込むデータ・パイプラインが使われることが多い。
These pipelines might be tightly integrated with the ML code.
これらのパイプラインは、MLコードと緊密に統合されているかもしれない。
Keeping the data pipelines and ML code in the same repo helps maintain this tight integration and streamline the workflow.
データパイプラインとMLコードを同じリポジトリに置くことは、この緊密な統合を維持し、ワークフローを合理化するのに役立つ。

## Consistency across experiments 実験間の一貫性

Machine learning development involves a lot of experimentation.
機械学習の開発には多くの実験が伴う。
Having all experiments in a monorepo ensures consistent environment setups and reduces the risk of discrepancies between different experiments due to varying code or data versions.
すべての実験をmonorepoで行うことで、一貫した環境のセットアップが保証され、コードやデータのバージョンが異なることによる、異なる実験間の不一致のリスクを減らすことができる。

## Simplified model versioning 

In a monorepo, the code and model versions are in sync because they are checked into the same repository.
モノレポでは、コードとモデルのバージョンは同じリポジトリにチェックインされるため、同期している。
This makes it easier to manage and trace model versions, which can be especially important in projects where ML reproducibility is critical.
これにより、モデルのバージョンの管理とトレースが容易になり、MLの再現性が重要なプロジェクトでは特に重要になります。

Just take the commit SHA at any given point in time, and it gives the information on the state of all models and services.
任意の時点でコミットSHAを取るだけで、すべてのモデルとサービスの状態に関する情報が得られる。

## Cross-functional collaboration 部門を超えたコラボレーション

Machine learning projects often involve collaboration between data scientists, ML engineers, and software engineers.
機械学習プロジェクトでは、データサイエンティスト、MLエンジニア、ソフトウェアエンジニアが協力することが多い。
A monorepo facilitates this cross-functional collaboration by providing a single source of truth for all project-related code and resources.
モノレポは、プロジェクトに関連するすべてのコードとリソースのための単一の真実のソースを提供することによって、この部門横断的なコラボレーションを促進する。

## Atomic changes 原子レベルの変化

In the context of ML, a model’s performance can depend on various interconnected factors like data preprocessing, feature extraction, model architecture, and post-processing.
MLの文脈では、モデルの性能は、データの前処理、特徴抽出、モデル・アーキテクチャ、後処理など、相互に関連するさまざまな要因に依存する可能性がある。
A monorepo allows for atomic changes – a change to multiple of these components can be committed as one, ensuring that interdependencies are always in sync.
モノレポはアトミックな変更を可能にする。複数のコンポーネントへの変更を1つとしてコミットすることができ、相互依存関係が常に同期していることを保証する。

## Unification of coding standards コーディング標準の統一

Finally, machine learning teams often include members without a software engineering background.
最後に、機械学習チームには、ソフトウェア・エンジニアリングのバックグラウンドを持たないメンバーが含まれることが多い。
These mathematicians, statisticians, and econometricians are brainy folks with brilliant ideas and the skills to train models that solve business problems.
これらの数学者、統計学者、計量経済学者は、ビジネス上の問題を解決するモデルを開発するスキルを持ち、素晴らしいアイデアを持つ頭脳派である。
However, writing code that is clean, easy to read, and maintain might not always be their strongest side.
しかし、きれいで、読みやすく、保守しやすいコードを書くことは、必ずしも得意分野ではないかもしれない。

A monorepo helps by automatically checking and enforcing coding standards across all projects, which not only ensures high code quality but also helps the less engineering-inclined team members learn and grow.
モノレポは、すべてのプロジェクトでコーディング標準を自動的にチェックし、実施することで、高いコード品質を保証するだけでなく、エンジニア志向の低いチームメンバーの学習と成長にも役立つ。

# How they do it in industry: famous monorepos ♪業界ではどうなのか：有名なモノレポ

In the software development landscape, some of the largest and most successful companies in the world use monorepos.
ソフトウェア開発の現場では、世界で最も成功した大企業のいくつかがモノレポを使っている。
Here are a few notable examples.
いくつか注目すべき例を挙げよう。

- Google: Google has long been a staunch advocate for the monorepo approach. Their entire codebase, estimated to contain 2 billion lines of code, is contained in a single, massive repository. They even published a paper about it. グーグル グーグルは長い間、モノレポ・アプローチを支持してきた。 20億行と推定されるコードベース全体が、単一の巨大なリポジトリに収められている。 論文も発表している。

- Meta: Meta also employs a monorepo for their vast codebase. They created a version control system called “Mercurial” to handle the size and complexity of their monorepo. メタ Metaもまた、膨大なコードベースに対してmonorepoを採用している。 彼らはモノレポのサイズと複雑さを処理するために「Mercurial」というバージョン管理システムを作った。

- Twitter: Twitter has been managing their monorepo for a long time using Pants, the build system we will talk about next! ツイッター Twitterは長い間、次に説明するビルドシステムPantsを使ってモノレポを管理してきた！

Many other companies such as Microsoft, Uber, Airbnb, and Stripe are using the monorepo approach at least for some parts of their codebases, too.
マイクロソフト、ウーバー、Airbnb、ストライプなど他の多くの企業も、少なくともコードベースの一部にモノレポ・アプローチを採用している。

Enough of the theory! Let’s take a look at how to actually build a machine learning monorepo.
理論はもう十分だ！実際に機械学習モノレポを作る方法を見てみよう。
Because just throwing what used to be separate repositories into one folder does not do the job.
以前は別々のリポジトリだったものを1つのフォルダに放り込むだけでは仕事にならないからだ。

# How to set up ML monorepo with Python? PythonでMLモノレポをセットアップするには？

Throughout this section, we will base our discussion on a sample machine learning repository I’ve created for this article.
このセクションでは、この記事のために作成したサンプルの機械学習リポジトリに基づいて議論する。
It is a simple monorepo holding just one project, or module: a hand-written digits classifier called mnist, after the famous dataset it uses.
それは、有名なデータセットにちなんでmnistと呼ばれる手書きの数字分類器である。

All you need to know right now is that in the monorepo’s root there is a directory called mnist, and in it, there is some Python code for training the model, the corresponding unit tests, and a Dockerfile to run training in a container.
今知っておく必要があるのは、monorepoのルートにmnistというディレクトリがあり、その中にモデルをトレーニングするためのPythonコード、対応するユニットテスト、そしてコンテナでトレーニングを実行するためのDockerファイルがあるということだけだ。

We will be using this small example to keep things simple, but in a larger monorepo, mnist would be just one of the many project folders in the repo’s root, each of which will contain source code, tests, dockerfiles, and requirement files at the least.
この小さな例では、物事をシンプルに保つために使いますが、より大きなモノレポでは、mnistはレポのルートにある多くのプロジェクトフォルダのひとつに過ぎず、それぞれのフォルダには少なくともソースコード、テスト、dockerfile、要件ファイルが含まれることになります。

## Build system: Why do you need one and how to choose it? ビルドシステム： なぜ必要なのか、どう選ぶのか？

### The Why? その理由は？

Think about all the actions, other than writing code, that the different teams developing different projects within the monorepo take as part of their development workflow.
モノレポ内の異なるプロジェクトを開発する異なるチームが、開発ワークフローの一環として取る、コードを書く以外のすべての行動について考えてみよう。
They would run linters against their code to ensure adherence to style standards, run unit tests, build artifacts such as docker containers and Python wheels, push them to external artifact repositories, and deploy them to production.
彼らはコードに対してリンターを実行し、スタイル標準への準拠を確認し、ユニットテストを実行し、DockerコンテナやPythonホイールなどの成果物をビルドし、それらを外部の成果物リポジトリにプッシュし、本番環境にデプロイする。

### Take testing. テストを受ける。

You’ve made a change in a utility function you maintain, ran the tests, and all’s green.
あなたが保守しているユーティリティ関数に変更を加え、テストを実行したところ、すべてがグリーンだった。
But how can you be sure your change is not breaking code for other teams that might be importing your utility? You should run their test suite, too, of course.
しかし、あなたの変更が、あなたのユーティリティをインポートしているかもしれない他のチームのコードを壊していないことを、どうやって確認できるでしょうか？もちろん、彼らのテスト・スイートも実行すべきです。

But to do this, you need to know exactly where the code you changed is being used.
しかしそのためには、変更したコードがどこで使われているかを正確に知る必要がある。
As the codebase grows, finding this out manually doesn’t scale well.
コードベースが大きくなるにつれ、手作業でこれを見つけるのはうまくスケールしない。
Of course, as an alternative, you can always execute all the tests, but again: that approach doesn’t scale very well.
もちろん、別の方法として、常にすべてのテストを実行することもできるが、繰り返すが、この方法はあまりうまくスケールしない。

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2023/08/2.png?resize=1536%2C804&ssl=1)

### Another example, production deployment. 別の例として、本番配備。

Whether you deploy weekly, daily, or continuously, when the time comes, you would build all the services in the monorepo and push them to production.
毎週、毎日、あるいは継続的にデプロイするにしても、その時が来たら、モノレポですべてのサービスを構築し、本番環境にプッシュすることになる。
But hey, do you need to build all of them on each occasion? That could be time-consuming and expensive at scale.
しかし、その都度、すべてを構築する必要があるのだろうか？規模が大きくなれば、時間もコストもかかるだろう。

Some projects might not have been updated for weeks.
何週間も更新されていないプロジェクトもあるかもしれない。
On the other hand, the shared utility code they use might have received updates.
一方、彼らが使用している共有ユーティリティ・コードが更新されているかもしれない。
How do we decide what to build? Again, it’s all about dependencies.
何を作るかはどうやって決めるのか？繰り返すが、依存関係がすべてだ。
Ideally, we would only build services that have been affected by the recent changes.
理想的には、最近の変更の影響を受けたサービスだけを構築することだ。

![](https://i0.wp.com/neptune.ai/wp-content/uploads/2023/08/1.png?resize=1536%2C804&ssl=1)

All of this can be handled with a simple shell script with a small codebase, but as it scales and projects start sharing code, challenges emerge, many of which revolve around dependency management.
しかし、規模が大きくなり、プロジェクトがコードを共有し始めると、依存関係管理にまつわる課題が浮かび上がってくる。

### Picking the right system 正しいシステムを選ぶ

All of the above is not a problem anymore if you invest in a proper build system.
適切なビルド・システムに投資すれば、上記のすべてはもう問題ではない。
A build system’s primary task is to build code.
ビルドシステムの主な仕事は、コードをビルドすることだ。
And it should do so in a clever way: the developer should only need to tell it what to build (“build docker images affected by my latest commit”, or “run only those tests that cover code which uses the method I’ve updated”), but the how should be left for the system to figure out.
開発者は、何をビルドするか（「私の最新コミットの影響を受けたドッカーイメージをビルドする」とか、「私が更新したメソッドを使用するコードをカバーするテストだけを実行する」とか）を指示するだけでよく、どのようにビルドするかはシステムに任せるべきである。

There are a couple of great open-source build systems out there.
素晴らしいオープンソースのビルドシステムがいくつかある。
Since most machine learning is done in Python, let’s focus on the ones with the best Python support.
ほとんどの機械学習はPythonで行われるので、Pythonのサポートが充実しているものに焦点を当てよう。
The two most popular choices in this regard are Bazel and Pants.
この点で最もポピュラーなのは、バゼルとパンツだ。

Bazel is an open-source version of Google’s internal build system, Blaze.
Bazelは、グーグルの内部ビルドシステムであるBlazeのオープンソース版だ。
Pants is also heavily inspired by Blaze and it aims for similar technical design goals as Bazel.
パンツもまた、ブレイズに大きな影響を受けており、バゼルと同様の技術的なデザインゴールを目指している。
An interested reader will find a good comparison of Pants vs.
興味のある読者には、パンツとパンツの良い比較が見つかるだろう。
Bazel in this blog post (but keep in mind it comes from the Pants devs).
このブログ記事のバゼル（ただし、パンツの開発者からの情報であることに留意してほしい）。
The table at the bottom of monorepo.tools offers yet another comparison.
monorepo.toolsの下部にある表は、さらに別の比較を提供している。

Both systems are great, and it is not my intention to declare a “better” solution here.
どちらのシステムも素晴らしいものであり、ここで「より良い」解決策を宣言する意図はない。
That being said, Pants is often described as easier to set up, more approachable, and well-optimized for Python, which makes it a perfect fit for machine learning monorepos.
とはいえ、Pantsはセットアップが簡単で、より親しみやすく、Pythonに最適化されているとよく言われる。

In my personal experience, the decisive factor that made me go with Pants was its active and helpful community.
私の個人的な経験では、パンツを選んだ決定的な要因は、活発で親切なコミュニティだった。
Whenever you have questions or doubts, just post on the community Slack channel, and a bunch of supportive folks will help you out soon.
質問や疑問があるときはいつでも、コミュニティのSlackチャンネルに投稿してください。

## Introducing Pants 

Alright, time to get to the meat of it! We will go step by step, introducing different Pants’ functionalities and how to implement them.
さて、そろそろ本題に入ろう！パンツのさまざまな機能とその実装方法を順を追って紹介していこう。
Again, you can check out the associated sample repo here.
ここでも、関連するサンプル・レポをチェックできる。

### Setup セットアップ

Pants is installable with pip.
パンツはpipでインストールできる。
In this tutorial, we will use the most recent stable version as of this writing, 2.15.1.
このチュートリアルでは、この記事を書いている時点での最新の安定版である2.15.1を使用します。

```
pip install pantsbuild.pants==2.15.1
```

Pants is configurable through a global master config file named pants.toml.
Pantsは、pants.tomlというグローバルなマスター設定ファイルを通して設定できる。
In it, we can configure Pants’ own behavior as well as the settings of downstream tools it relies on, such as pytest or mypy.
この中で、Pants自身の動作や、pytestやmypyのようなPantsが依存する下流のツールの設定を行うことができる。

Let’s start with a bare minimum pants.toml:
まずは最低限のパンツから：

```
[GLOBAL]
pants_version = "2.15.1"
backend_packages = [
    "pants.backend.python",
]

[source]
root_patterns = ["/"]

[python]
interpreter_constraints = ["==3.9.*"]
```

In the global section, we define the Pants version and the backend packages we need.
グローバルセクションでは、Pantsのバージョンと必要なバックエンドパッケージを定義する。
These packages are Pants’ engines that support different features.
これらのパッケージは、さまざまな機能をサポートするパンツのエンジンである。
For starters, we only include the Python backend.
手始めに、Pythonのバックエンドのみを紹介する。

In the source section, we set the source to the repository’s root.
ソースセクションでは、ソースをリポジトリのルートに設定します。
Since version 2.15, to make sure this is picked up, we also need to add an empty BUILD_ROOT file at the repository’s root.
バージョン 2.15 以降では、これを確実にピックアップするために、リポジトリのルートに空の BUILD_ROOT ファイルを追加する必要もあります。

Finally, in the Python section, we choose the Python version to use.
最後に、Pythonセクションで、使用するPythonのバージョンを選択する。
Pants will browse our system in search of a version that matches the conditions specified here, so make sure you have this version installed.
Pantsは、ここで指定された条件に一致するバージョンを探してシステムをブラウズしますので、このバージョンがインストールされていることを確認してください。

That’s a start! Next, let’s take a look at any build system’s heart: the BUILD files.
これがスタートだ！次に、ビルド・システムの心臓部である BUILD ファイルを見てみましょう。

### Build files ビルドファイル

Build files are configuration files used to define targets (what to build) and their dependencies (what they need to work) in a declarative way.
ビルド・ファイルは、ターゲット（何をビルドするか）とその依存関係（動作に必要なもの）を宣言的に定義するための設定ファイルである。

You can have multiple build files at different levels of the directory tree.
ディレクトリツリーの異なるレベルに複数のビルドファイルを持つことができる。
The more there are, the more granular the control over dependency management.
数が多ければ多いほど、依存関係の管理はより細かくなる。
In fact, Google has a build file in virtually every directory in their repo.
実際、グーグルは彼らのレポのほぼすべてのディレクトリにビルドファイルを持っている。

In our example, we will use three build files:
この例では、3つのビルドファイルを使用する：

- mnist/BUILD – in the project directory, this build file will define the python requirements for the project and the docker container to build; mnist/BUILD - プロジェクトディレクトリにあるこのビルドファイルは、プロジェクトの python 要件とビルドする docker コンテナを定義します；

- mnist/src/BUILD – in the source code directory, this build file will define python sources, that is, files to be covered by python-specific checks; mnist/src/BUILD - ソース・コード・ディレクトリにあるこのビルド・ファイルは、pythonソース、つまりpython固有のチェックの対象となるファイルを定義します；

- mnist/tests/BUILD – in the tests directory, this build file will define which files to run with Pytest and what dependencies are needed for these tests to run. mnist/tests/BUILD - tests ディレクトリにあるこのビルドファイルは、Pytest で実行するファイルと、これらのテストを実行するために必要な依存関係を定義します。

Let’s take a look at the mnist/src/BUILD:
mnist/src/BUILDを見てみよう：

```
python_sources(
    name="python",
    resolve="mnist",
    sources=["**/*.py"],
)
```

At the same time, mnist/BUILD looks like this:
同時に、mnist/BUILDは次のようになる：

```
python_requirements(
    name="reqs",
    source="requirements.txt",
    resolve="mnist",
)
```

The two entries in the build files are referred to as targets.
ビルドファイルの2つのエントリーはターゲットと呼ばれる。
First, we have a Python sources target, which we aptly call python, although the name could be anything.
まず、Pythonソース・ターゲットを用意する。名前は何でもいいが、ここでは適当にpythonと呼ぶことにする。
We define our Python sources as all .py files in the directory.
Pythonのソースをディレクトリ内の全ての.pyファイルと定義します。
This is relative to the build file’s location, that is: even if we had Python files outside of the mnist/src directory, these sources only capture the contents of the mnist/src folder.
つまり、mnist/srcディレクトリの外側にPythonファイルがあったとしても、これらのソースはmnist/srcフォルダの中身だけを取り込む。
There is also a resolve filed; we will talk about it in a moment.
これについては後で説明する。

Next, we have the Python requirements target.
次に、Pythonの要件ターゲットである。
It tells Pants where to find the requirements needed to execute our Python code (again, relative to the build file’s location, which is in the mnist project’s root in this case).
これは、Pythonコードを実行するために必要な要件がどこにあるかをPantsに指示します（繰り返しますが、ビルドファイルの場所からの相対位置で、この場合はmnistプロジェクトのルートにあります）。

This is all we need to get started.
これだけでスタートできる。
To make sure the build file definition is correct, let’s run:
ビルドファイルの定義が正しいことを確認するために、実行してみよう：

```
pants tailor --check update-build-files --check ::
```

As expected, we get: “No required changes to BUILD files found.” as the output.
予想通り、こうなった： 「BUILDファイルに必要な変更は見つかりませんでした。
Good!
いいね！

Let’s spend a bit more time on this command.
このコマンドにはもう少し時間をかけよう。
In a nutshell, a bare pants tailor can automatically create build files.
一言で言えば、ベアパンツテーラーが自動的にビルドファイルを作成できる。
However, it sometimes tends to add too many for one’s needs, which is why I tend to add them manually, followed by the command above that checks their correctness.
そのため、私は手動で追加し、その後に上記のコマンドでその正しさをチェックすることが多い。

The double semicolon at the end is a Pants notation that tells it to run the command over the entire monorepo.
最後のダブル・セミコロンは、モノレポ全体でコマンドを実行するように指示するパンツの表記法である。
Alternatively, we could have replaced it with mnist: to run only against the mnist module.
あるいは、これをmnist:に置き換えて、mnistモジュールに対してのみ実行させることもできる。

### Dependencies and lockfiles 依存関係とロックファイル

To do efficient dependency management, pants relies on lockfiles.
効率的な依存関係の管理を行うために、パンツはロックファイルに依存している。
Lockfiles record the specific versions and sources of all dependencies used by each project.
ロックファイルは、各プロジェクトで使用されるすべての依存関係の特定のバージョンとソースを記録します。
This includes both direct and transitive dependencies.
これには直接依存と推移的依存の両方が含まれる。

By capturing this information, lockfiles ensure that the same versions of dependencies are used consistently across different environments and builds.
この情報をキャプチャすることで、ロックファイルは、異なる環境やビルド間で一貫して同じバージョンの依存関係が使用されることを保証する。
In other words, they serve as a snapshot of the dependency graph, ensuring reproducibility and consistency across builds.
言い換えれば、依存関係グラフのスナップショットとして機能し、ビルド間の再現性と一貫性を保証する。

To generate a lockfile for our mnist module, we need the following addition to pants.toml:
mnistモジュールのロック・ファイルを生成するには、pants.tomlに以下の項目を追加する必要がある：

```
[python]
interpreter_constraints = ["==3.9.*"]
enable_resolves = true
default_resolve = "mnist"

[python.resolves]
mnist = "mnist/mnist.lock"
```

We enable the resolves (Pants term for lockfiles’ environments) and define one for mnist passing a file path.
resolves（ロックファイルの環境を表すパンツ用語）を有効にし、mnistにファイルパスを渡すものを定義する。
We also choose it as the default one.
私たちもデフォルトとしてこれを選んだ。
This is the resolve we have passed to Python sources and Python requirements target before: this is how they know what dependencies are needed.
これは、以前PythonソースとPython要件ターゲットに渡したresolveである。
We can now run:
これで走れる：

to get:
を手に入れる：

This has created a file at mnist/mnist.lock.
これにより、mnist/mnist.lockにファイルが作成された。
This file should be checked with git if you intend to use Pants for your remote CI/CD.
リモートCI/CDにPantsを使用する場合は、このファイルをgitでチェックする必要があります。
And naturally, it needs to be updated every time you update the requirements.txt file.
そして当然ながら、requirements.txtファイルを更新するたびに更新する必要がある。

With more projects in the monorepo, you would rather generate the lockfiles selectively for the project that needs it, e.g.pants generate-lockfiles mnist: .
monorepoにプロジェクトが増えれば、むしろロックファイルを必要とするプロジェクトに対して選択的に生成することになる。例えば、pants generate-lockfiles mnist: .

That’s it for the setup! Now let’s use Pants to do something useful for us.
設定は以上だ！では、Pantsを使って何か便利なことをしてみよう。

### Unifying code style with Pants パンツでコードスタイルを統一する

Pants natively supports a number of Python linters and code formatting tools such as Black, yapf, Docformatter, Autoflake, Flake8, isort, Pyupgrade, or Bandit.
Pantsは、Black、yapf、Docformatter、Autoflake、Flake8、isort、Pyupgrade、Banditなど、多くのPythonリンターやコード整形ツールをネイティブにサポートしています。
They are all used in the same way; in our example, let’s implement Black and Docformatter.
この例では、BlackとDocformatterを実装してみよう。

To do so, we add appropriate two backends to pants.toml:
そのために、適切な2つのバックエンドをpants.tomlに追加する：