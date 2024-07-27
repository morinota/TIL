## refs: refs：

- [Managed Spot Training: Save Up to 90% On Your Amazon SageMaker Training Jobs](https://aws.amazon.com/jp/blogs/aws/managed-spot-training-save-up-to-90-on-your-amazon-sagemaker-training-jobs/) マネージド・スポット・トレーニング： Amazon SageMakerトレーニングジョブを最大90%割引](https://aws.amazon.com/jp/blogs/aws/managed-spot-training-save-up-to-90-on-your-amazon-sagemaker-training-jobs/)

# Managed Spot Training: Save Up to 90% On Your Amazon SageMaker Training Jobs マネージド・スポット・トレーニング： Amazon SageMakerトレーニングジョブを最大90%節約

Amazon SageMaker is a fully-managed, modular machine learning (ML) service that enables developers and data scientists to easily build, train, and deploy models at any scale.
Amazon SageMakerはfully-managedなモジュール式の機械学習（ML）サービスで、開発者やデータサイエンティストがあらゆる規模のモデルを簡単に構築、トレーニング、デプロイできるようにします。
With a choice of using built-in algorithms, bringing your own, or choosing from algorithms available in AWS Marketplace, it’s never been easier and faster to get ML models from experimentation to scale-out production.
ビルトインアルゴリズムの使用、独自のアルゴリズムの持ち込み、AWS Marketplaceで利用可能なアルゴリズムからの選択により、MLモデルを実験からスケールアウト本番まで、かつてないほど簡単かつ迅速に導入できます。

One of the key benefits of Amazon SageMaker is that it frees you of any infrastructure management, no matter the scale you’re working at.
Amazon SageMakerの主な利点の1つは、**どのような規模で作業していても、インフラ管理から解放されること**です。
For instance, instead of having to set up and manage complex training clusters, you simply tell Amazon SageMaker which Amazon Elastic Compute Cloud (Amazon EC2) instance type to use, and how many you need: the appropriate instances are then created on-demand, configured, and terminated automatically once the training job is complete.
例えば、複雑なトレーニングクラスタを設定して管理する必要がなく、**Amazon SageMakerに使用するAmazon Elastic Compute Cloud（Amazon EC2）インスタンスタイプと必要な数を教えるだけで、適切なインスタンスがオンデマンドで作成され、構成され、トレーニングジョブが完了すると自動的に終了**します。(うんうん...!)
As customers have quickly understood, this means that they will never pay for idle training instances, a simple way to keep costs under control.
顧客がすぐに理解したように、これはアイドル状態のトレーニング・インスタンスに料金を支払う必要がないことを意味し、**コストを抑制するシンプルな方法**である。
(ちなみに、idle状態= 顧客が実際には利用してないが、稼働している仮想マシンやサーバ)

## Introducing Managed Spot Training

マネージド・スポット・トレーニングの紹介

Going one step further, we’re extremely happy to announce Managed Spot Training for Amazon SageMaker, a new feature based on Amazon EC2 Spot Instances that will help you lower ML training costs by up to 90% compared to using on-demand instances in Amazon SageMaker.
さらに一歩進んで、**Amazon EC2 Spot Instancesに基づいた新機能であるAmazon SageMakerのマネージド・スポット・トレーニング**を発表できることを非常にうれしく思います。これにより、Amazon SageMakerのオンデマンドインスタンスを使用した場合と比較して、MLトレーニングコストを最大90％削減できます。(本番環境でも使い所多そうだよね...!特に学習処理は、batch処理である事が多いし...!:thinking:)
Launched almost 10 years ago, Spot Instances have since been one of the cornerstones of building scalable and cost-optimized IT platforms on AWS.
**約10年前に発表されたSpot Instances**は、以来、スケーラブルでコスト最適化されたITプラットフォームをAWS上に構築するための基盤の1つとなっています。
Starting today, not only will your Amazon SageMaker training jobs run on fully-managed infrastructure, they will also benefit from fully-managed cost optimization, letting you achieve much more with the same budget.
本日より、Amazon SageMaker のトレーニングジョブは、フルマネージドのインフラストラクチャで実行されるだけでなく、**フルマネージドのコスト最適化**も受けられ、同じ予算でより多くのことを達成できます。
Let’s dive in!
さあ、飛び込もう！

Managed Spot Training is available in all training configurations:
マネージド・スポット・トレーニングは、すべてのトレーニング構成でご利用いただけます：

- All instance types supported by Amazon SageMaker,
  Amazon SageMakerがサポートするすべてのインスタンスタイプ、

- All models: built-in algorithms, built-in frameworks, and custom models,
  すべてのモデル： 組み込みアルゴリズム、組み込みフレームワーク、カスタムモデル、

- All configurations: single instance training, distributed training, and automatic model tuning.
  すべての構成： シングルインスタンストレーニング、分散トレーニング、自動モデルチューニング。

Setting it up is extremely simple, as it should be when working with a fully-managed service:
フルマネージド・サービスを利用する場合、そうであるべきなのだが、設定は極めて簡単だ：

- If you’re using the console, just switch the feature on.
  コンソールを使っている場合は、**この機能をオンにするだけでいい**。

- If you’re working with the Amazon SageMaker SDK, just set the train_use_spot_instances to true in the Estimator constructor.
  Amazon SageMaker SDKを使用している場合は、**Estimatorコンストラクタでtrain_use_spot_instancesをtrueに設定するだけ**です。

That’s all it takes: do this, and you’ll save up to 90%.
これだけです： **これだけで、最大90％の節約になります**。
Pretty cool, don’t you think?
かなりクールだと思わないか？

## Interruptions and Checkpointing 中断とチェックポイント

There’s an important difference when working with Managed Spot Training.
マネージド・スポット・トレーニングで働く場合、**重要な違い**がある。
Unlike on-demand training instances that are expected to be available until a training job completes, Managed Spot Training instances may be reclaimed at any time if we need more capacity.
**トレーニングジョブが完了するまで利用可能であると予想されるオンデマンドトレーニングインスタンス**とは異なり、必要に応じて容量を増やすために、**マネージド・スポット・トレーニング・インスタンスはいつでも回収される可能性**があります。
(通常のインスタンスは、on-demandインスタンスって言うんだ...!:thinking:)

With Amazon Elastic Compute Cloud (Amazon EC2) Spot Instances, you would receive a termination notification 2 minutes in advance, and would have to take appropriate action yourself.
**Amazon Elastic Compute Cloud（Amazon EC2）Spot Instancesでは、2分前に終了通知を受け取り、適切な対応を自分で取る必要がある**。(そうなのか...! 急いで対応しないといけないじゃん...!:thinking:)
Don’t worry, though: as Amazon SageMaker is a fully-managed service, it will handle this process automatically, interrupting the training job, obtaining adequate spot capacity again, and either restarting or resuming the training job.
しかしご心配なく： Amazon SageMakerはフルマネージドサービスであるため、このプロセスを自動的に処理し、トレーニングジョブを中断し、適切なスポット容量を再取得し、トレーニングジョブを再開または再開します。
This makes Managed Spot Training particularly interesting when you’re flexible on job starting time and job duration.
このため、**ジョブの開始時刻とジョブの期間に柔軟性がある場合、マネージド・スポット・トレーニングは特に興味深く検討の余地がある**。(Spot Instanceと機械学習のbatch処理って相性いいな...!そんなに頻繁に学習させ直すわけでもないし...!:thinking:)
You can also use the MaxWaitTimeInSeconds parameter to control the total duration of your training job (actual training time plus waiting time).
また、`MaxWaitTimeInSeconds`パラメータを使用して、トレーニングジョブの合計期間（実際のトレーニング時間と待機時間）を制御することもできます。
(これって、Spot Instanceが回収された場合の待機時間ね、そんなに長い時間回収されたままになるのかな...!:thinking:)

To avoid restarting a training job from scratch should it be interrupted, we strongly recommend that you implement checkpointing, a technique that saves the model in training at periodic intervals.
トレーニングが中断された場合、トレーニングジョブを最初からやり直すことを避けるため、**checkpointing**を実装することを強くお勧めします。**これは、トレーニング中のモデルを定期的な間隔で保存**する技術です。
(i.e. 学習途中のモデルを保存しておくことね...!:thinking:)
Thanks to this, you can resume a training job from a well-defined point in time, continuing from the most recent partially trained model:
このおかげで、トレーニングジョブを特定の時点から再開し、最新の部分的にトレーニングされたモデルから続行できます。

- Built-in frameworks and custom models: you have full control over the training code.
  内蔵フレームワークとカスタムモデル: トレーニングコードを完全にコントロールできます。
  Just make sure that you use the appropriate APIs to save model checkpoints to Amazon Simple Storage Service (Amazon S3) regularly, using the location you defined in the CheckpointConfig parameter and passed to the SageMaker Estimator.
  SageMaker Estimatorに渡された `CheckpointConfig` パラメータで定義された場所を使用して、定期的にモデルのチェックポイントをAmazon Simple Storage Service（Amazon S3）に保存するための適切なAPIを使用してください。
  Please note that TensorFlow uses checkpoints by default.
  TensorFlowはデフォルトでチェックポイントを使用することに注意してください。
  For other frameworks, you’ll find examples in our sample notebooks and in the documentation.
  その他のフレームワークについては、サンプルノートブックやドキュメントに例があります。

- Built-in algorithms: computer vision algorithms support checkpointing (Object Detection, Semantic Segmentation, and very soon Image Classification).
  内蔵アルゴリズム： コンピュータビジョンアルゴリズムはチェックポイントをサポートします（オブジェクト検出、セマンティックセグメンテーション、そして近いうちに画像分類）。
  As they tend to train on large data sets and run for longer than other algorithms, they have a higher likelihood of being interrupted.
  大規模なデータセットでトレーニングし、他のアルゴリズムよりも長時間実行される傾向があるため、中断される可能性が高いです。
  Other built-in algorithms do not support checkpointing for now.
  他の組み込みアルゴリズムは、今のところチェックポイントをサポートしていない。

Alright, enough talk, time for a quick demo!
さて、話はこのくらいにして、簡単なデモの時間だ！

## Training a Built-in Object Detection Model with Managed Spot Training マネージド・スポット・トレーニングによる内蔵物体検出モデルのトレーニング

Reading from this sample notebook, let’s use the AWS console to train the same job with Managed Spot Training instead of on-demand training.
このサンプルノートブックを参考に、AWSコンソールを使って同じジョブをオンデマンドトレーニングではなく、マネージドスポットトレーニングでトレーニングしてみましょう。
As explained before, I only need to take care of two things:
先に説明したように、私は**2つのことに気をつけるだけでいい**：

- Enable Managed Spot Training (obviously).
  マネージド・スポット・トレーニングの有効化（当然）。

- Set `MaxWaitTimeInSeconds`.
  MaxWaitTimeInSecondsを設定する。

First, let’s name our training job, and make sure it has appropriate AWS Identity and Access Management (IAM) permissions (no change).
まず、トレーニングジョブに名前を付け、適切なAWS Identity and Access Management（IAM）権限を持っていることを確認しましょう（変更なし）。

Then, I select the built-in algorithm for object detection.
そして、オブジェクト検出の内蔵アルゴリズムを選択する。

Then, I select the instance count and instance type for my training job, making sure I have enough storage for the checkpoints.
それから、トレーニングジョブのインスタンス数とインスタンスタイプを選択し、checkpoint用の十分なストレージがあることを確認する。

The next step is to set hyper parameters, and I’ll use the same ones as in the notebook.
次のステップはハイパーパラメータを設定するこです。ノートブックと同じものを使います。
I then define the location and properties of the training data set.
次に、**トレーニングデータセットの場所とプロパティを定義**する。うんうん。

I do the same for the validation data set.
検証データセットも同じようにする。

I also define where model checkpoints should be saved.
また、モデルのcheckpointを保存する場所を定義する。
This is where Amazon SageMaker will pick them up to resume my training job should it be interrupted.
ここでAmazon SageMakerは、私のトレーニングの仕事が中断された場合に再開するために、それらをピックアップする。

This is where the final model artifact should be saved.
最終的ななmodel artifactを保存する場所を指定する。

Good things come to those who wait! This is where I enable Managed Spot Training, configuring a very relaxed 48 hours of maximum wait time.
待つ者には良いことがある！ここで、**マネージド・スポット・トレーニングを有効にし、最大待ち時間を48時間に設定**する。

I’m done, let’s train this model.
もう終わったから、このモデルをトレーニングしよう。
Once training is complete, cost savings are clearly visible in the console.
トレーニングが完了すれば、コスト削減はコンソールではっきりと確認できる。

As you can see, my training job ran for 2423 seconds, but I’m only billed for 837 seconds, saving 65% thanks to Managed Spot Training! While we’re on the topic, let me explain how pricing works.
ご覧のように、**私のトレーニングジョブは2423秒間実行されましたが、課金されたのは837秒間だけで、Managed Spot Trainingのおかげで65％節約できました**！ついでに、料金の仕組みについても説明しましょう。

## Pricing 価格

A Managed Spot training job is priced for the duration for which it ran before it completed, or before it was terminated.
マネージド・スポット・トレーニング・ジョブは、**完了する前、または終了する前に実行された期間**、料金が設定されます。

For built-in algorithms and AWS Marketplace algorithms that don’t use checkpointing, we’re enforcing a maximum training time of 60 minutes (MaxWaitTimeInSeconds parameter).
ビルトインアルゴリズムとcheckpointingを使用しないAWS Marketplaceアルゴリズムについては、最大トレーニング時間を60分に制限しています。（`MaxWaitTimeInSeconds`パラメータ）

Last but not least, no matter how many times the training job restarts or resumes, you only get charged for data download time once.
最後になりましたが、**何度トレーニングが再開されても、データのダウンロードにかかる費用は1回分のみ**です。

## Now Available!

現在発売中！

This new feature is available in all regions where Amazon SageMaker is available, so don’t wait and start saving now!
この新機能は、Amazon SageMakerが利用可能なすべての地域で利用可能です！

As always, we’d love to hear your feedback: please post it to the AWS forum for Amazon SageMaker, or send it through your usual AWS contacts.
いつも通り、フィードバックをお待ちしております： Amazon SageMakerのAWSフォーラムに投稿していただくか、いつものAWSコンタクトを通してお送りください。

<!-- ここまで読んだ! -->
