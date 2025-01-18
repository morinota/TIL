# Choreography vs Orchestration in the land of serverless
# サーバーレスの世界におけるコレオグラフィーとオーケストレーション
Yan Cui
ヤン・クイ

I help clients go faster for less using serverless technologies.
私は、サーバーレス技術を使用して、クライアントがより速く、より少ないコストで進むのを助けます。

Choreography and Orchestration are two modes of interaction in a microservices architecture.
コレオグラフィーとオーケストレーションは、マイクロサービスアーキテクチャにおける二つの相互作用のモードです。

In orchestration, there is a controller (the ‘orchestrator’) that controls the interaction between services.
オーケストレーションでは、**サービス間の相互作用を制御するコントローラー（「オーケストレーター」）**があります。
It dictates the control flow of the business logic and is responsible for making sure that everything happens on cue.
それはビジネスロジックの制御フローを指示し、すべてがタイミングよく発生することを保証する責任があります。
This follows the request-response paradigm.
これはリクエスト-レスポンスのパラダイムに従います。

In choreography, every service works independently.
コレオグラフィーでは、各サービスが独立して動作します。
There are no hard dependencies between them, and they are loosely coupled only through shared events.
**それらの間には厳密な依存関係はなく、共有イベントを通じてのみ緩やかに結合**されています。
Each service listens for events that it’s interested in and does its own thing.
各サービスは、自分が興味のあるイベントをリッスンし、自分の役割を果たします。
This follows the event-driven paradigm.
これはイベント駆動型のパラダイムに従います。

As always, neither is necessarily better than the other.
いつものように、どちらが必ずしも優れているわけではありません。
Depending on the context, one might be more appropriate than the other.
文脈によっては、一方が他方よりも適切である場合があります。
And since Lambda itself is inherently event-driven, the choreography approach has become very popular in the serverless community.
そして、**Lambda自体が本質的にイベント駆動型であるため、コレオグラフィーアプローチはサーバーレスコミュニティで非常に人気があります**。
I’m a huge fan of this approach and have built many event-driven systems using services such as EventBridge, SNS and Kinesis.
私はこのアプローチの大ファンであり、EventBridge、SNS、Kinesisなどのサービスを使用して多くのイベント駆動型システムを構築してきました。

However, in this post, I want to talk about when it’s not a good idea and when you should consider the orchestration approach instead.
しかし、この記事では、コレオグラフィーが良いアイデアでない場合や、代わりにオーケストレーションアプローチを考慮すべき時について話したいと思います。

The TL;DR is that, when it comes to implementing workflows, you should prefer orchestration within the bounded context of a microservice, but prefer choreography between bounded contexts.
**要約すると、ワークフローを実装する際には、マイクロサービスの制約されたコンテキスト内ではオーケストレーションを好むべきですが、制約されたコンテキスト間ではコレオグラフィーを好むべき**です。(制約されたコンテキストの中と間??:thinking_face:)


<!-- ここまで読んだ -->

### The Choreography approach 振付アプローチ

Imagine you’re building a food ordering service where customers can order takeaways from their favourite restaurants. 
顧客がお気に入りのレストランからテイクアウトを注文できるフードオーダリングサービスを構築していると想像してください。

A typical order flow might involve the following five steps. 
典型的な注文フローは、以下の5つのステップを含むかもしれません。

We can model these five steps as events: 
これらの5つのステップをイベントとしてモデル化できます。

- order_placed 注文を受け付ける
- restaurant_notified レストランに通知する
- order_accepted 注文を受け入れる
- user_notified ユーザーに通知する
- order_completed 注文を完了する

With these events, we can implement the order flow using an event-driven approach. 
これらのイベントを使用して、イベント駆動型アプローチで注文フローを実装できます。

1. A customer places an order. 
1. 顧客が注文を行います。
2. place-order function publishes an order_placed event. 
2. place-order関数がorder_placedイベントを発行します。
3. notify-restaurant function is triggered by the order_placed event. 
3. notify-restaurant関数がorder_placedイベントによってトリガーされます。
4. notify-restaurant function sends a message to the restaurant via SNS. 
4. notify-restaurant関数がSNSを介してレストランにメッセージを送信します。
5. notify-restaurant function publishes a restaurant_notified event. 
5. notify-restaurant関数がrestaurant_notifiedイベントを発行します。
6. The restaurant receives the new order notification in its mobile app. 
6. レストランはモバイルアプリで新しい注文通知を受け取ります。
7. The restaurant clicks Accept Order in the app, which calls the orders API. 
7. レストランはアプリで「注文を受け入れる」をクリックし、これがorders APIを呼び出します。
8. accept-order function publishes an order_accepted event. 
8. accept-order関数がorder_acceptedイベントを発行します。
9. notify-user function is triggered by the order_accepted event. 
9. notify-user関数がorder_acceptedイベントによってトリガーされます。
10. notify-user function sends an order confirmation email to the customer. 
10. notify-user関数が顧客に注文確認メールを送信します。
11. notify-user function publishes a user_notified event. 
11. notify-user関数がuser_notifiedイベントを発行します。
12. The customer sees the order confirmation and is eagerly waiting for the food to arrive. 
12. 顧客は注文確認を見て、食べ物が届くのを楽しみに待っています。
13. The restaurant delivers the food to the customer. 
13. レストランは顧客に食べ物を配達します。
14. The restaurant clicks the Complete Order in the app to confirm order has been delivered. This calls the orders API. 
14. レストランはアプリで「注文を完了する」をクリックして、注文が配達されたことを確認します。これがorders APIを呼び出します。
15. complete-order function publishes an order_completed event. 
15. complete-order関数がorder_completedイベントを発行します。

Every function acted completely independently. 
**すべての関数は完全に独立して動作**しました。

None of them had the notion of the overall order flow, they each only cared about: 
**どの関数も全体の注文フローの概念を持っておらず**、それぞれが気にしていたのは以下のことだけです。

- What events they are interested in. どのイベントに興味があるか。
- What they should do. 何をすべきか。
- What events they should publish when they complete their task. タスクを完了したときにどのイベントを発行すべきか。

Pros 利点

- Each step of the flow can be changed independently. フローの各ステップは独立して変更できます。
- Each step of the flow can be scaled independently. フローの各ステップは独立してスケールできます。
- No single point of failure. 単一障害点はありません。
- Other systems can build on these events – e.g. a promo-code service might be interested in the order_completed event and send out discount vouchers to the customer. 他のシステムはこれらのイベントを基に構築できます。例えば、プロモコードサービスはorder_completedイベントに興味を持ち、顧客に割引券を送信するかもしれません。
- The events are useful artefacts on their own, and can be fed into a data lake to generate business intelligence reports. **イベントはそれ自体で有用なアーティファクト**であり、データレイクに取り込んでビジネスインテリジェンスレポートを生成できます。(なるほど「イベントはそれ自体で有用なアーティファクト」:thinking_face:)

Cons 欠点

- End-to-end monitoring and reporting are difficult. エンドツーエンドの監視と報告は困難です。
- Difficult to implement timeouts. タイムアウトを実装するのが難しいです。
- The order flow is not explicitly modelled and exists only as an emergent property of what system does.  注文フローは明示的にモデル化されておらず、システムが行うことの出現的特性としてのみ存在します。
- As such, it’s only captured in the mental model of someone who understands the system end-to-end. **そのため、システムをエンドツーエンドで理解している人のメンタルモデルにのみ捉えられます**。(なるほど、オーケストレーションの方が全体像を理解しやすいんだ...!:thinking_face:)

From a business point-of-view, it also begs the question “are these really separate processes? Or are they different steps within one process?”. 
ビジネスの観点から見ると、「これらは本当に別々のプロセスですか？それとも一つのプロセス内の異なるステップですか？」という疑問を投げかけます。
For business-critical workflows like this, wouldn’t you want someone or some team to take ownership of and be responsible for it? 
このようなビジネスクリティカルなワークフローに対して、誰かまたはチームがそれを所有し、責任を持つことを望みませんか？
When something goes wrong and you lose millions by the hour, do you want a room full of people looking at each other because no one understands the process end-to-end? 
何かがうまくいかず、時間あたり何百万も失うとき、**プロセスをエンドツーエンドで理解している人がいない**ために、互いに見つめ合う部屋にいることを望みますか？

And if there are few people in the company understands how this critical flow works, then it creates an existential risk to the business if these people ever left the company. 
そして、会社にこの重要なフローがどのように機能するかを理解している人が少ない場合、これらの人々が会社を離れたときにビジネスにとって存在的リスクを生じます。

<!-- ここまで読んだ -->

### The Orchestration approach オーケストレーションアプローチ

To implement the orchestration approach, I will probably use something like Step Functions and model the order flow as a state machine.  
オーケストレーションアプローチを実装するために、私はおそらくStep Functionsのようなものを使用し、注文フローを状態遷移機械としてモデル化します。

![]()

It’s also worth remembering that, although we no longer need to use events to trigger the next step of the order flow, those events are still useful artefacts on their own.  
次のステップの注文フローをトリガーするためにイベントを使用する必要がなくなったとはいえ、**それらのイベントはそれ自体で有用なアーティファクトである**ことを思い出す価値があります。
So we should publish those same events from Task states in the state machine.  
したがって、状態遷移機械のタスク状態から同じイベントを公開する必要があります。
For example, after the Notify User state notifies the user via SES, the Task should also publish the user_notified event.  
例えば、Notify User状態がSESを介してユーザーに通知した後、タスクはuser_notifiedイベントも公開する必要があります。

This means we can still decouple the order flow from other business units that wish to build features on top of events related to an order.  
これは、注文に関連するイベントの上に機能を構築したい他のビジネスユニットから注文フローを依然として切り離すことができることを意味します。
The aforementioned promo-code service can still rely on the order_completed event as before.  
前述のプロモコードサービスは、以前と同様にorder_completedイベントに依存することができます。

Pros 利点

- End-to-end monitoring and reporting are trivial since Step Functions gives you built-in visualization and audit histories.  
- エンドツーエンドの監視と報告は簡単です。なぜなら、Step Functionsは組み込みの可視化と監査履歴を提供するからです。
- Easy to implement timeout – e.g. for a restaurant to accept an order, or for the total duration of the order.  
- タイムアウトの実装が簡単です。例えば、レストランが注文を受け入れるためのものや、注文の総時間のためです。
- Business logic is in one place, and it’s easy to maintain and manage.  
- **ビジネスロジックは一箇所にあり、保守と管理が容易**です。
- The order flow is modelled and source controlled. You can literally see it in the Step Functions console.  
- 注文フローはモデル化され、ソース管理されています。実際にStep Functionsコンソールで見ることができます。
- The order flow is modelled and source controlled. Yes, it’s that important that it should count as two pros!  
- 注文フローはモデル化され、ソース管理されています。はい、それは非常に重要なので、2つの利点として数えるべきです！

Cons 欠点

- Have to learn yet another AWS service.  さらに別のAWSサービスを学ぶ必要があります。
- At $25 per million state transitions (which counts Start and End by the way), Step Functions is a pricey service.  100万回の状態遷移ごとに25ドル（ちなみにStartとEndもカウントされます）で、Step Functionsは高価なサービスです。
- If Step Functions is down, then no orders can be processed. **Step Functions (i.e. オーケストレーたー) がダウンしている場合、注文は処理できません。** Although the same might be said about Lambda, EventBridge, or any services that are critical to the working of this order flow. **Lambda、EventBridge、またはこの注文フローの機能に重要なサービスについても同じことが言える**かもしれません。(これが単一障害点、みたいな話...??)


<!--  ここまで読んだ! -->

### The hybrid approach ハイブリッドアプローチ

Within a bounded context, I have a specific set of responsibilities that are aligned with a business area. 
限られたコンテキスト内では、私はビジネス領域に沿った特定の責任のセットを持っています。 
And there are hopefully a small number of components that they can all fit inside my head at the same time. 
そして、できればそれらすべてを同時に私の頭の中に収めることができる少数のコンポーネントがあります。 
Since they all work together to achieve some specific business capability such as processing payments, they form a highly cohesive unit. 
それらはすべて、支払い処理などの特定のビジネス機能を達成するために協力しているため、高度に結束したユニットを形成します。 
And since I own everything within this microservice’s bounded context, I’m free to change and reorganize things so long I don’t break my contract with external services. 
このマイクロサービスの限られたコンテキスト内のすべてを私が所有しているため、外部サービスとの契約を破らない限り、物事を変更したり再編成したりする自由があります。 

I often see workflows within a bounded context being choreographed through messages in SQS/SNS/EventBridge. 
私はしばしば、**限られたコンテキスト内のワークフローがSQS/SNS/EventBridgeのメッセージを通じて調整されている**のを見ます。 
Generally speaking, I think that’s a bad idea. 
一般的に言って、それは**悪いアイデア**だと思います。 

![]()

I love using events to integrate different services together in a loosely-coupled way. 
私は、異なるサービスを緩やかに結合された方法で統合するためにイベントを使用するのが大好きです。 
But I think it’s a bad idea when it’s done inside the same bounded context because the workflow doesn’t exist as a standalone concept that is explicitly captured and source controlled. 
しかし、同じ限られたコンテキスト内で行われると、それは悪いアイデアだと思います。なぜなら、ワークフローは明示的にキャプチャされ、ソース管理される独立した概念として存在しないからです。 

In these choreographed workflows, the workflow only exists as the sum of loosely connected functions. 
これらの調整されたワークフローでは、**ワークフローは緩やかに接続された関数の合計としてのみ存在**します。(**要するに、コレオグラフィ的にDAGを構築するのが、悪いアイデアってことだろうか...!!:thinking_face:**)
As we discussed above with the food delivery example, this makes them very difficult to reason about and debug. 
上記のフードデリバリーの例で議論したように、これにより、それらは非常に理解しにくく、デバッグが難しくなります。 
And there’s no easy way to implement even simple things like workflow level timeouts, or even task level tasks for that matter (e.g. timeout the order if the restaurant doesn’t accept or reject the order within 10 minutes). 
さらに、ワークフローのレベルのタイムアウトや、たとえばレストランが10分以内に注文を受け入れない場合の注文のタイムアウトのような単純なことを実装する簡単な方法はありません。 

If this is what you have today, you should consider moving these workflows to Step Functions instead. 
もしこれが現在の状況であれば、これらのワークフローを代わりにStep Functions(i.e. オーケストレーションパターン)に移動することを検討すべきです。 

But, between bounded contexts, I’ll publish and subscribe to events through SNS/EventBridge/Kinesis, etc. 
しかし、コンテキスト間では、私はSNS/EventBridge/Kinesisなどを通じてイベントを発行し、購読します。 
This is so that different parts of the larger system can stay loosely coupled and only build on each other’s events and can evolve and fail independently. 
これは、より大きなシステムの異なる部分が緩やかに結合されたままであり、お互いのイベントに基づいて構築し、独立して進化し、失敗できるようにするためです。 

Orchestration and choreography don’t have to be mutually exclusive. 
オーケストレーションと振り付けは、相互に排他的である必要はありません。 
Whenever I’m introducing state changes inside a state machine (such as changing the status of an order from pending to processed), I’ll publish those state changes as events. 
状態遷移を持つ状態マシン内で状態変更を導入するたびに（たとえば、注文のステータスを保留から処理済みに変更する場合）、私はそれらの状態変更をイベントとして発行します。 
Other services can listen and react to these state changes, and bringing choreography into the picture. 
他のサービスはこれらの状態変更をリッスンし、反応することができ、振り付けを取り入れることができます。 

Let me leave you with my rule-of-thumb when it comes to implementing business workflows: use orchestration within the bounded context of a microservice, but use choreography between bounded-contexts. 
ビジネスワークフローを実装する際の私の経験則をお伝えします：**マイクロサービスの限られたコンテキスト内ではオーケストレーションを使用し、限られたコンテキスト間では振り付けを使用**してください。 

I hope you’ve found this post useful. 
この投稿が役に立ったことを願っています。 
If you want to learn more about running serverless in production and what it takes to build production-ready serverless applications then check out my upcoming workshop, Production-Ready Serverless! 
プロダクションでサーバーレスを実行することや、プロダクション対応のサーバーレスアプリケーションを構築するために必要なことについてもっと学びたい場合は、私の今後のワークショップ「Production-Ready Serverless」をチェックしてください！ 

In the workshop, I will give you a quick introduction to AWS Lambda and the Serverless framework, and take you through topics such as: 
ワークショップでは、AWS LambdaとServerlessフレームワークの簡単な紹介を行い、次のようなトピックを取り上げます： 
- testing strategies 
- テスト戦略 
- how to secure your APIs 
- APIを安全に保つ方法 
- API Gateway best practices 
- API Gatewayのベストプラクティス 
- CI/CD 
- CI/CD 
- configuration management 
- 構成管理 
- security best practices 
- セキュリティのベストプラクティス 
- event-driven architectures 
- イベント駆動型アーキテクチャ 
- how to build observability into serverless applications 
- サーバーレスアプリケーションに可観測性を組み込む方法 
and much more! 
などなど！ 

<!-- ここまで読んだ! -->

### Related Posts 関連投稿

Whenever you’re ready, here are 3 ways I can help you:
準備ができたら、私があなたを助ける3つの方法を紹介します。

1. Production-Ready Serverless: Join 20+ AWS Heroes & Community Builders and 1000+ other students in levelling up your serverless game. This is your one-stop shop for quickly levelling up your serverless skills.
   プロダクション対応のサーバーレス：20人以上のAWSヒーローやコミュニティビルダー、1000人以上の他の学生と共に、あなたのサーバーレススキルを向上させましょう。これは、サーバーレススキルを迅速に向上させるためのワンストップショップです。

2. I help clients launch product ideas, improve their development processes and upskill their teams. If you’d like to work together, then let’s get in touch.
   私はクライアントが製品アイデアを立ち上げ、開発プロセスを改善し、チームのスキルを向上させる手助けをします。もし一緒に働きたいのであれば、ぜひご連絡ください。

3. Join my community on Discord, ask questions, and join the discussion on all things AWS and Serverless.
   私のDiscordコミュニティに参加し、質問をし、AWSやサーバーレスに関するすべての議論に参加してください。


# まとめメモ

- 結論
  - **1つのコンテキストの中ではオーケストレーション！**
    - つまり、**1つのマイクロサービス内で何か作業するときは、「全部管理するオーケストレーター（Step Functionsとか）を使いな〜！**」ってこと。
    - 理由は、タイムアウトとかエラーの管理とか、ワークフロー全体を見える化するのがめっちゃ簡単だから。これでトラブル起きたときも冷静に対応できる
  - **コンテキストの間ではコレオグラフィ!**
    - 逆に、**マイクロサービス同士の連携では、「各サービスが独立して、イベント経由で繋がってればいいじゃん？」って感じ！**
    - SNSとかEventBridgeとかで「このイベント来たら動く〜！」みたいにゆる〜く繋げておくのが大事。これなら、どれか1個壊れても他のサービスには影響ないし、拡張もラクちん。
- MLOps的な例:
  - コンテキストの中(=>オーケストレーション)
    - たとえば、MLモデルの学習プロセスを管理するなら...
      - 前処理
      - 学習
      - ハイパラ調整
      - モデル評価
      - モデル保存
    - ↑を一個ずつ順番にやらないといけないから、オーケストレーターで状態を管理しながら進めるのがベスト！途中で失敗しても、どのステップで止まったかわかるから安心！
  - コンテキストの間(->コレオグラフィ)
    - 学習したモデルを他のサービスで使う場面では...
      - モデルデプロイ完了通知をEventBridgeで発行
      - 推論サービス「お、新しいモデルきた!」って感じで、推論APIを更新
      - データドリフト検出サービスも「OK！監視スタート!」って感じ。
    - 各サービスが独立して動いてるから、1つがダウンしても他は普通に動くし、めっちゃスケーラブル!

