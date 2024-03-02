## link リンク

https://confidence.spotify.com/blog/ab-tests-and-rollouts
https://confidence.spotify.com/blog/ab-tests-and-rollouts

# Experiment like Spotify: A/B Tests and Rollouts Spotifyのような実験： A/Bテストとロールアウト

This post is part of a series that showcases how you can use Confidence.
この記事は、コンフィデンスの使い方を紹介するシリーズの一部です。
Make sure to check out our earlier post Experiment like Spotify: With Confidence.
Spotifyのような実験： 自信を持って。

At Spotify, we've been exercising our experimentation muscle for more than 10 years.
スポティファイでは、**10年以上にわたって実験力を鍛えてきた**。
We now have over 300 teams running tens of thousands of experiments annually.
現在、300を超えるチームが年間数万件の実験を実施している。
Experimentation is integral to the way we develop the Spotify experience — but it's a lot more than just running A/B tests to find the winning ideas.
実験は、私たちがSpotifyのエクスペリエンスを開発する上で欠かせないものです。しかし、それは単にA/Bテストを実施して勝てるアイデアを見つけるだけではありません。
This post talks about A/B tests and rollouts, how they're used at Spotify, and how you can use them in Confidence.
この投稿では、A/Bテストとロールアウト、Spotifyでの使用方法、およびConfidenceでの使用方法について説明します。
(rollout = treatmentを段階的に展開するプロセス。全ユーザに対して一気にではなく...!)

## The dual purpose of experimentation 実験の二重の目的

The workhorse of experimentation is the A/B test, which lets you test your new ideas with users.
実験の主力はA/Bテストで、新しいアイデアをユーザとテストすることができます。
You randomly give the new experience to one set of users, while another set of users gets the current experience.
あるユーザにはランダムに新しいエクスペリエンスを提供し、別のユーザーには現在のエクスペリエンスを提供する。
The A/B test evaluates how these users react after they've been subjected to one of the experiences.
A/Bテストでは、ユーザがどちらかの体験をした後にどのような反応を示すかを評価する。
You compare the groups with a test metric, like minutes of music played in the Spotify case.
Spotifyの場合、音楽の再生時間のようなテスト指標でグループを比較する。(=これがOECか...!)
You conclude whether your new idea was a hit based on this experiment.
あなたはこの実験に基づいて、自分の新しいアイデアがヒットしたかどうかを結論づける。

The A/B test fits into the larger product development narrative of think it, build it, ship it, tweak it.
A/Bテストは、考え、作り、出荷し、微調整するという、より大きな製品開発の物語に適合する。
With A/B tests, we come up with new ideas, both big and small, and build simpler versions of them that we test with users.
A/Bテストでは、大小さまざまな新しいアイデアを思いつき、そのシンプルなバージョンを作ってユーザとテストする。
Based on feedback, we tweak and repeat continuously to improve the product.
**フィードバックに基づき、私たちは絶えず微調整を繰り返し、製品を改良していく**。

![]()

A/B testing and online experimentation is often narrowly described from this perspective only — as a tool for evaluating new, untested ideas.
A/Bテストとオンライン実験は、しばしばこの観点からだけ、つまり新しい、テストされていないアイデアを評価するためのツールとして、狭く説明される。
In practice, the product development phase that uses A/B tests to validate good ideas is more of an inner loop within a larger, outer loop.
実際には、優れたアイデアを検証するためにA/Bテストを使用する製品開発段階は、より大きな外側のループの中の内側のループである。
In fact, at Spotify, experimentation serves an equally important second purpose: it's the way we release changes to our users.
実際、Spotifyでは、実験は同様に重要な第二の目的も果たしている： それは、私たちがユーザーに変更をリリースする方法です。

## Ship changes safely with rollouts ロールアウトで変更を安全に送る

After you've found the winning variant and verified that it's a success with users, you still need to release it.
**勝てるバリアントを見つけ、それがユーザにとって成功であることを確認したら、それをリリースする必要があります**。
Your earlier tests indicate a success — but the unknown unknowns of releasing your new experience to everyone can make users react in unexpected ways.
以前のテストは成功を示していた。しかし、新しいエクスペリエンスをすべてのユーザにリリースすることのunknown unknows(??)の部分は、ユーザが予期しない方法で反応する可能性があります。
For example, maybe your systems aren't able to handle the increased load when releasing the new experience fully, which you failed to detect in your earlier tests on only a subset of users.
たとえば、新しいエクスペリエンスを完全にリリースする際に、システムが増加した負荷を処理できない可能性があります。これは、ユーザの一部に対する以前のテストで検出できなかったものです。

Luckily, there's no need to be in the dark when you're rolling out the experience.
幸いなことに、体験を展開する際に暗闇にいる必要はありません。
With rollouts in Confidence, you can be in full control of what percentage of your users receive the new experience — all while you're monitoring the impact on the metrics you care about.
Confidenceのロールアウトでは、新しいエクスペリエンスを受け取るユーザの割合を完全にコントロールすることができます。そして、あなたが気にしているメトリクスへの影響を監視しながらです。(あ、ConfidenceはSpotifyのABテストプラットフォームの名前なのかな...!:thinking_face:)
Concerned that there's a risk your new experience could increase the share of users that have their app crash? Just add it as a metric to understand how it evolves as you gradually increase the proportion of users that get the new experience.
新しいエクスペリエンスによって、アプリのクラッシュが増加する可能性があると心配ですか？新しいエクスペリエンスを受け取るユーザの割合を徐々に増やすにつれて、それがどのように進化するかを理解するために、それをメトリクスとして追加するだけです。
All the while Confidence summarizes the results for you, recommending what to do next.
その間、コンフィデンスはあなたのために結果を要約し、次に何をすべきかを提案する。

## Differences between A/B tests and rollouts A/Bテストとロールアウトの違い

Just like an A/B test, a rollout is an experiment that randomizes users into a control or a treatment group.
A/Bテストと同じように、ロールアウトはユーザを無作為にコントロールグループとトリートメントグループに分ける実験である。(ほうほう...?)
In contrast to an A/B test, a rollout has an adjustable reach — a percentage that determines what share of users should receive the new treatment.
**A/Bテストとは対照的に、ロールアウトには調整可能なreach（到達率）があり**、新しいトリートメントを受け取るユーザの割合を決定する。
You can adjust the level of reach up and down when the rollout is live.
ロールアウトがライブのときに、reachのレベルを上げたり下げたりすることができる。

While an A/B test is a product development tool that sets out to find evidence that a new idea is successful, the rollout is about releasing changes safely.
A/Bテストは、新しいアイデアが成功しているという証拠を見つけるために設定された製品開発ツールであるのに対し、ロールアウトは変更を安全にリリースすることについてのツールである。(うんうん...!)
For this reason, an A/B test has a fixed allocation that you can't change, while the flexible allocation of the rollout is its main perk.
このため、A/Bテストは割り当てが固定されており、変更することができない。
A/B tests track both success and guardrail metrics, whereas rollouts only use guardrail metrics.
A/Bテストは成功指標とガードレール指標の両方を追跡するが、**ロールアウトはガードレール指標のみを使用する**。
The table below shows the main differences between A/B tests and rollouts in Confidence.
下の表は、A/BテストとConfidenceにおけるロールアウトの主な違いを示しています。

- A/B test
  - Treatments = Can have multiple
  - Allocation = Fixed
  - Control group experience = Fixed variant
  - Metrics = Success and guardrail
  - Inference = Fixed horizon or sequential
    - Fixed horizon approach は「A fixed period of time」を意味し、データ収集の期間を固定し、その期間が終了した後に一度だけデータ分析を行い、テストの結果を評価する。p値の計算など統計的手法の適用が直接的。(peakingとかはfalse positiveのリスクを高めちゃうもんね...!基本p値に基づいて評価するならfixed horizonか...!:thinking_face:)
    - Sequential approach は「Sequential testing」を意味し、データを段階的に分析し、特定の基準が満たされた時点でテストを早期に終了するか決定する。(false positiveのリスク増加を考慮する必要があり、専門的な知識が必要...!:thinking_face:)
- Rollout
  - Treatments = Only one
  - Allocation = Adjustable
  - Control group experience = Default experience
  - Metrics = Only guardrail
  - Inference = Only sequential

## Rollouts are the appetizers of experimentation ロールアウトは実験の前菜です

At Spotify, we've seen an incredible increase in the use of rollouts.
Spotifyでは、ロールアウトの利用が驚くほど増えている。
If you've been working on building your experimentation culture, you know it's a challenging job — not everyone is as bought in to evaluating all their ideas with A/B tests as you are.
**もし実験文化を構築しているなら、それが難しい仕事であることを知っているだろう**。すべてのアイデアをA/Bテストで評価することに賛同している人は、あなたほど多くはいない。
Rollouts are different, though, and releasing changes safely and gradually while monitoring metrics resonates with almost everyone.
**しかし、ロールアウトは異なり、メトリクスを監視しながら変更を安全に、徐々にリリースすることは、ほとんどの人に共感を呼び起こします**。(なるほど...! 賛同しない人はいないよね...!:thinking_face:)
A lot of teams at Spotify have begun their experimentation journey with rollouts and have later, after having gotten a taste of data-informed decision making, moved on to more traditional A/B testing.
**Spotifyの多くのチームは、ロールアウトで実験の旅を始め、データに基づいた意思決定(=guradrail metricsが低下したら割合を下げるとか...??)の味を知った後、より伝統的なA/Bテストに移行しています**。(実験文化の浸透のための初期のステップとして、ロールアウトが有効なのかも...??:thinking_face:)
The ratio of new rollouts to new A/B tests continues to grow at Spotify, and has shown a steady increase throughout 2023:
新しいABテストに対する新しいロールアウトの比率は、Spotifyで増加し続け、2023年を通じて着実に増加しています。

## Experiment on your own terms with Confidence Confidenceを使って自分の条件で実験する

Don't agree with how we define and separate A/B tests and rollouts? Maybe you want to use success metrics in rollouts, or make the total allocation of A/B tests adjustable for a live test.
A/Bテストとロールアウトの定義と分離に同意しない？ロールアウトで成功指標を使用したいかもしれませんし、ライブテストのためにA/Bテストの総割り当てを調整可能にしたいかもしれません。
One of the best aspects of Confidence is that you set your own practices and that you're not forced to experiment like we do.
Confidenceの最大の利点の1つは、自分自身の実践を設定できることであり、私たちのように実験することを強制されることはありません。
With the custom workflows that Confidence offers, you can define your own experiment designs.
Confidenceが提供するカスタムワークフローを使用すると、独自の実験設計を定義できます。
Use our implementation of A/B tests and rollouts as a starting point, and adjust them so they fit your needs.
A/Bテストとロールアウトの実装を出発点として使用し、それらを自分のニーズに合わせて調整してください。
No one knows better what works for you than you.
あなたにとって何がうまくいくかを知っている人はあなただけです。
Confidence lets you run high-quality experiments on your own terms.
Confidenceは、あなたの条件で高品質の実験を実行することができます。

## What's next ＃次は何だ？

This post is part of a series that showcases how you can use Confidence.
この投稿は、Confidenceの使い方を紹介するシリーズの一部です。
Make sure to check out our earlier post Experiment like Spotify: With Confidence.
Spotifyのような実験： 自信を持って。
Coming up in the series are posts on flags, analysis of experiments, metrics, workflows, and more.
このシリーズでは、フラッグ、実験の分析、メトリクス、ワークフローなどについての投稿を予定している。

Confidence is currently available in private beta.
コンフィデンスは現在プライベート・ベータ版として提供されている。
If you haven't signed up already, sign up today and we'll be in touch.
まだご登録がお済みでない方は、今すぐご登録ください。

<!-- ここまで読んだ! Rolloutいいね! -->
