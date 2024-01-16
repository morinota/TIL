## link リンク

https://confidence.spotify.com/blog/ab-tests-and-rollouts
https://confidence.spotify.com/blog/ab-tests-and-rollouts

# Experiment like Spotify: A/B Tests and Rollouts Spotifyのような実験： A/Bテストとロールアウト

This post is part of a series that showcases how you can use Confidence.
この記事は、コンフィデンスの使い方を紹介するシリーズの一部です。
Make sure to check out our earlier post Experiment like Spotify: With Confidence.
Spotifyのような実験： 自信を持って。

At Spotify, we've been exercising our experimentation muscle for more than 10 years.
スポティファイでは、10年以上にわたって実験力を鍛えてきた。
We now have over 300 teams running tens of thousands of experiments annually.
現在、300を超えるチームが年間数万件の実験を実施している。
Experimentation is integral to the way we develop the Spotify experience — but it's a lot more than just running A/B tests to find the winning ideas.
実験は、私たちがSpotifyのエクスペリエンスを開発する上で欠かせないものです。しかし、それは単にA/Bテストを実施して勝てるアイデアを見つけるだけではありません。
This post talks about A/B tests and rollouts, how they're used at Spotify, and how you can use them in Confidence.
この投稿では、A/Bテストとロールアウト、Spotifyでの使用方法、そしてConfidenceでの使用方法について説明する。

## The dual purpose of experimentation 実験の二重の目的

The workhorse of experimentation is the A/B test, which lets you test your new ideas with users.
実験の主力はA/Bテストで、新しいアイデアをユーザーとテストすることができます。
You randomly give the new experience to one set of users, while another set of users gets the current experience.
あるユーザーにはランダムに新しいエクスペリエンスを提供し、別のユーザーには現在のエクスペリエンスを提供する。
The A/B test evaluates how these users react after they've been subjected to one of the experiences.
A/Bテストでは、ユーザーがどちらかの体験をした後にどのような反応を示すかを評価する。
You compare the groups with a test metric, like minutes of music played in the Spotify case.
Spotifyの場合、音楽の再生時間のようなテスト指標でグループを比較する。
You conclude whether your new idea was a hit based on this experiment.
あなたはこの実験に基づいて、自分の新しいアイデアがヒットしたかどうかを結論づける。

The A/B test fits into the larger product development narrative of think it, build it, ship it, tweak it.
A/Bテストは、考え、作り、出荷し、微調整するという、より大きな製品開発の物語に適合する。
With A/B tests, we come up with new ideas, both big and small, and build simpler versions of them that we test with users.
A/Bテストでは、大小さまざまな新しいアイデアを思いつき、そのシンプルなバージョンを作ってユーザーとテストする。
Based on feedback, we tweak and repeat continuously to improve the product.
フィードバックに基づき、私たちは絶えず微調整を繰り返し、製品を改良していく。

A/B testing and online experimentation is often narrowly described from this perspective only — as a tool for evaluating new, untested ideas.
A/Bテストとオンライン実験は、しばしばこの観点からだけ、つまり新しい、テストされていないアイデアを評価するためのツールとして、狭く説明される。
In practice, the product development phase that uses A/B tests to validate good ideas is more of an inner loop within a larger, outer loop.
実際には、優れたアイデアを検証するためにA/Bテストを使用する製品開発段階は、より大きな外側のループの中の内側のループである。
In fact, at Spotify, experimentation serves an equally important second purpose: it's the way we release changes to our users.
実際、Spotifyでは、実験は同様に重要な第二の目的も果たしている： それは、私たちがユーザーに変更をリリースする方法です。

## Ship changes safely with rollouts ロールアウトで変更を安全に送る

After you've found the winning variant and verified that it's a success with users, you still need to release it.
勝てるバリアントを見つけ、それがユーザーにとって成功であることを確認したら、それをリリースする必要があります。
Your earlier tests indicate a success — but the unknown unknowns of releasing your new experience to everyone can make users react in unexpected ways.
以前のテストは成功を示していた。しかし、新しいエクスペリエンスをすべての人にリリースするという未知の未知数は、ユーザーを予想外の方法で反応させる可能性がある。
For example, maybe your systems aren't able to handle the increased load when releasing the new experience fully, which you failed to detect in your earlier tests on only a subset of users.
例えば、新しいエクスペリエンスを完全にリリースする際に、システムが負荷の増加に対応できていない可能性があります。

Luckily, there's no need to be in the dark when you're rolling out the experience.
幸いなことに、体験を展開する際に暗闇の中にいる必要はない。
With rollouts in Confidence, you can be in full control of what percentage of your users receive the new experience — all while you're monitoring the impact on the metrics you care about.
コンフィデンスのロールアウトでは、ユーザーの何パーセントが新しいエクスペリエンスを受け取るかを完全にコントロールすることができます。
Concerned that there's a risk your new experience could increase the share of users that have their app crash? Just add it as a metric to understand how it evolves as you gradually increase the proportion of users that get the new experience.
新しいエクスペリエンスによって、アプリがクラッシュするユーザーの割合が増えるリスクを懸念していますか？新しいエクスペリエンスを取得するユーザーの割合を徐々に増やすにつれて、それがどのように変化するかを理解するための指標として追加するだけです。
All the while Confidence summarizes the results for you, recommending what to do next.
その間、コンフィデンスはあなたのために結果を要約し、次に何をすべきかを提案する。

## Differences between A/B tests and rollouts A/Bテストとロールアウトの違い

Just like an A/B test, a rollout is an experiment that randomizes users into a control or a treatment group.
A/Bテストと同じように、ロールアウトはユーザーを無作為にコントロールグループとトリートメントグループに分ける実験である。
In contrast to an A/B test, a rollout has an adjustable reach — a percentage that determines what share of users should receive the new treatment.
A/Bテストとは対照的に、ロールアウトには調整可能なリーチがあります。
You can adjust the level of reach up and down when the rollout is live.
ロールアウトのライブ時に、リーチのレベルを上下に調整できる。

While an A/B test is a product development tool that sets out to find evidence that a new idea is successful, the rollout is about releasing changes safely.
A/Bテストは、新しいアイデアが成功する証拠を見つけるための製品開発ツールである一方、ロールアウトは変更を安全にリリースすることである。
For this reason, an A/B test has a fixed allocation that you can't change, while the flexible allocation of the rollout is its main perk.
このため、A/Bテストは割り当てが固定されており、変更することができない。
A/B tests track both success and guardrail metrics, whereas rollouts only use guardrail metrics.
A/Bテストは成功指標とガードレール指標の両方を追跡するのに対し、ロールアウトはガードレール指標のみを使用する。
The table below shows the main differences between A/B tests and rollouts in Confidence.
下の表は、A/BテストとConfidenceにおけるロールアウトの主な違いを示しています。

## Rollouts are the appetizers of experimentation ♪ロールアウトは実験の前菜

At Spotify, we've seen an incredible increase in the use of rollouts.
Spotifyでは、ロールアウトの利用が驚くほど増えている。
If you've been working on building your experimentation culture, you know it's a challenging job — not everyone is as bought in to evaluating all their ideas with A/B tests as you are.
もしあなたが実験文化の構築に取り組んでいるのであれば、それが困難な仕事であることを知っているだろう。
Rollouts are different, though, and releasing changes safely and gradually while monitoring metrics resonates with almost everyone.
しかし、ロールアウトは異なるものであり、メトリクスを監視しながら安全かつ徐々に変更をリリースすることは、ほとんどすべての人の共感を得る。
A lot of teams at Spotify have begun their experimentation journey with rollouts and have later, after having gotten a taste of data-informed decision making, moved on to more traditional A/B testing.
Spotifyの多くのチームは、ロールアウトから実験の旅を始め、データに基づいた意思決定を味わった後、より伝統的なA/Bテストに移行した。
The ratio of new rollouts to new A/B tests continues to grow at Spotify, and has shown a steady increase throughout 2023:
Spotifyでは、新しいA/Bテストに対する新しい展開の割合が増え続けており、2023年を通して安定した増加を見せている：

## Experiment on your own terms with Confidence ♪自信をもって、自分らしく実験しよう

Don't agree with how we define and separate A/B tests and rollouts? Maybe you want to use success metrics in rollouts, or make the total allocation of A/B tests adjustable for a live test.
A/Bテストとロールアウトを定義し、分離する方法に同意できませんか？ロールアウトで成功指標を使用したり、A/Bテストの合計割り当てをライブテストで調整可能にしたいかもしれません。
One of the best aspects of Confidence is that you set your own practices and that you're not forced to experiment like we do.
コンフィデンスのいいところは、練習方法を自分で決められること、そして私たちのように実験を強制されないことだ。
With the custom workflows that Confidence offers, you can define your own experiment designs.
Confidenceが提供するカスタム・ワークフローを使えば、独自の実験デザインを定義することができる。
Use our implementation of A/B tests and rollouts as a starting point, and adjust them so they fit your needs.
A/Bテストとロールアウトの実施を出発点として、貴社のニーズに合うように調整してください。
No one knows better what works for you than you.
何が自分に合っているか、自分以上によく知っている人はいない。
Confidence lets you run high-quality experiments on your own terms.
Confidenceを使えば、質の高い実験を自分の判断で行うことができる。

## What's next ＃次は何だ？

This post is part of a series that showcases how you can use Confidence.
この記事は、コンフィデンスの使い方を紹介するシリーズの一部です。
Make sure to check out our earlier post Experiment like Spotify: With Confidence.
Spotifyのような実験： 自信を持って。
Coming up in the series are posts on flags, analysis of experiments, metrics, workflows, and more.
このシリーズでは、フラッグ、実験の分析、メトリクス、ワークフローなどについての投稿を予定している。

Confidence is currently available in private beta.
コンフィデンスは現在プライベート・ベータ版として提供されている。
If you haven't signed up already, sign up today and we'll be in touch.
まだご登録がお済みでない方は、今すぐご登録ください。
