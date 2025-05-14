refs: https://andrewchen.com/growth-stalls/


Andrew Chen Archives  
# What to do when product growth stalls プロダクトの成長が停滞したときに何をすべきか

## The crisis arrives slowly, then all at once 危機はゆっくりと訪れ、そして一気にやってくる。

At first, everything seems rosy. The growth rate of a new product is spiking, and growing quickly, maybe even hundreds of percentage points a year.  
最初はすべてが順調に見える。新製品の成長率は急上昇し、急速に成長している。年間で数百パーセントの成長もあり得る。
But weirdly, a year or two in, there’s some softness in the latest numbers.  
しかし奇妙なことに、1年か2年経つと、最新の数字に若干の軟化が見られる。
Maybe it’s seasonality, or maybe something else. But worryingly, it keeps slowing.  
それは季節性かもしれないし、他の何かかもしれない。しかし心配なことに、成長は鈍化し続ける。
First to 300% a year, then 200%. Then 100% – a mere doubling annually in a startup ecosystem that demands a much faster target.  
最初は年間300%、次に200%。そして100% – スタートアップエコシステムでは、年間の倍増は非常に遅い目標である。
More features are planned, and some are even shipped. Eventually, there’s a back-to-back where things are completely flat.  
さらに多くの機能が計画され、一部は実装される。しかし最終的には、すべてが完全に横ばいになる。
What starts as a slow boil – where the team has a well-planned roadmap and a big vision – becomes a sudden crisis.  
チームがよく計画されたロードマップと大きなビジョンを持っている状態から始まるゆっくりとした沸騰は、突然の危機に変わる。
There are late evening phone calls and emergency sessions.  
遅い時間の電話や緊急会議が行われる。
Analytics dashboards are pulled and re-pulled, to figure out what’s going on.  
分析ダッシュボードが引き出され、何が起こっているのかを把握するために再度引き出される。
The team needs a new plan.  
チームは新しい計画を必要としている。

There’s a saying that no military plan survives first contact with the enemy, and similarly — no product roadmap survives first contact with stalled growth.  
「どんな軍事計画も敵との初接触を生き延びることはない」という言葉があるが、同様に、成長が停滞した際に製品のロードマップも生き延びることはない。
Instead, a crisis ensues, and the entire roadmap has to be rewritten.  
その代わりに危機が発生し、全体のロードマップを再作成しなければならない。
Particularly for startups, where continual growth is life and death.  
**特にスタートアップにとっては、継続的な成長が生死に関わる問題である**。

When this crisis hits, the question is, what to do about it?  
**この危機が訪れたとき、問題はどう対処するかである**。
How do you come up with a plan?  
どのように計画を立てるのか？

For better or worse, I’ve had this conversation with product managers and entrepreneurs many times over the years.  
良いことでも悪いことでも、私はこれまでに何度もプロダクトマネージャーや起業家とこの会話を交わしてきた。
The easy answer that people generally want to hear either falls into the camp of:  
人々が一般的に聞きたい簡単な答えは、次のようなものに分類される。

- This next magic feature will fix all our growth problems –The PM  
- この次の魔法の機能が私たちの成長の問題をすべて解決するだろう – プロダクトマネージャー

- We need to spend more money on marketing –The Marketer  
- もっとマーケティングにお金を使う必要がある – マーケター

- Have you considered adding more AI? –The Investor  
- もっとAIを追加することを考えたことはありますか？ – 投資家

Don’t listen to these people :)  
これらの人々の言うことを聞いてはいけない :)

Instead, I offer the idea that you can analyze growth stalls systematically.  
代わりに、**成長の停滞を体系的に分析**できるという考えを提案する。
You can ask questions, gather data, and assess the stall to zero in on the problems that are driving the metrics downwards.  
質問をし、データを集め、停滞を評価して、指標を下げている問題に焦点を当てることができる。

<!-- ここまで読んだ! -->

## Assessing the stall – starting with retention 停滞の評価 – リテンションから始める

First off, let me explain what’s happening during a growth stall.  
まず、**成長の停滞中に何が起こっているのか**を説明させてください。
Yes, of course, it’s when a top-line number (like revenue or active users, or otherwise) stops growing.  
はい、もちろん、**トップラインの数字（収益やアクティブユーザーなど）が成長を止めるとき**のことです。
But what’s happening under the covers?  
しかし、裏では何が起こっているのか？
At its core, a product stalls when its churn catches up with its customer acquisition.  
**本質的には、顧客の流出が顧客獲得に追いつくときに製品が停滞する**。

I encourage y’all reading the entire thing, but I’ve written about this in the past in the deckThe Red Flags and Magic Numbers That Investors Look For, which shows this growth of the underlying dynamics:  
皆さんに全体を読んでいただきたいが、私は過去に「[投資家が探す赤旗と魔法の数字](https://andrewchen.com/investor-metrics-deck/)」というデッキでこれについて書いたことがあり、基礎的なダイナミクスの成長を示している。

![]()

That is, a stall occurs when a product is churning enough users that it overpowers the counterforce – the product attracting new users and reactivating users (though this latter term is less important for startups).  
つまり、製品が十分なユーザーを流出させて、反対の力（新しいユーザーを引き付け、ユーザーを再活性化する製品）を上回るときに停滞が発生する（ただし、この後者の用語はスタートアップにとってはあまり重要ではない）。
This happens because typically churn happens to a % of the user base, as anyone who’s seen cohort retention curves knows.  
これは、通常、流出はユーザーベースのa%に発生するため、コホートリテンションカーブを見たことがある人なら誰でも知っている。
But unfortunately, new customer growth channels tend to be fairly linear — most marketing channels don’t scale up as the user base scales up, and even the channels that do, like viral marketing, eventually saturate and slow down.  
しかし残念ながら、新しい顧客成長チャネルはかなり線形的である傾向がある – ほとんどのマーケティングチャネルはユーザーベースが拡大するにつれてスケールアップせず、バイラルマーケティングのようにスケールアップするチャネルでさえ、最終的には飽和し、鈍化する。
All while churn continues to creep up over time as a percentage.  
その間、流出は時間とともに%として徐々に増加し続ける。

Because of these dynamics, I start by asking questions about retention to establish a baseline.  
これらのダイナミクスのために、私は**リテンションに関する質問をして基準を確立すること**から始める。

These questions are just a starting point, because once you ask them, the question is — what do you do with the answers?  
これらの質問は出発点に過ぎない。なぜなら、質問をした後は、答えをどうするかが問題だからだ。

- What is the D1/D7/D30 of the product? (if consumer?) How does it compare to other products in its category?  
- 製品のD1/D7/D30は何ですか？（消費者の場合）それは同じカテゴリの他の製品と比較してどうですか？

- If it’s a workplace product, how many days per week does the typical user engage? (This is the Power User Curve)  
- もしそれが職場向けの製品であれば、典型的なユーザーは週に何日関与しますか？（これは[パワーユーザーカーブ](https://andrewchen.com/power-user-curve/)です）

- Are people as active and engaged as you expect them to be? If it’s a daily-use product, does your DAU/MAU ratio reflect that?  
- 人々はあなたが期待するほどアクティブで関与していますか？それが日常的に使用される製品であれば、あなたのDAU/MAU比はそれを反映していますか？

There are many benchmarks out there for all the product categories, but as a very rough guideline, you need a D1/D7/D30 of 60/30/15% to be at respectable numbers for a social app.  
すべての製品カテゴリには多くのベンチマークがありますが、**非常に粗いガイドラインとして、ソーシャルアプリにとってはD1/D7/D30が60/30/15%である必要があります**。
You need DAU/MAU over 20%, and if subscription based, you want churn <5% if SMB (and free acquisition).  
**DAU/MAUは20%以上必要であり、サブスクリプションベースの場合、SMB（および無料獲得）の場合は流出率を5%未満にしたい**。
There are equivalent numbers for net revenue retention, session lengths, and lots of other metrics too.  
ネット収益維持率、セッションの長さ、その他多くの指標にも同様の数値があります。

A marketplace company might look at a different set of metrics.  
マーケットプレイス企業は異なる指標セットを見るかもしれません。
Often the demand side can have heavy churn, but the supply side should retain well (>50% YoY).  
需要側は大きな流出があることが多いが、供給側は良好に維持されるべきである（前年比50%以上）。
An enterprise SaaS product would have its own set of metrics.  
エンタープライズSaaS製品には独自の指標がある。
It’s important to benchmark, to see if there are successful products with similar metrics that have gotten to scale.  
ベンチマークを行い、スケールに達した同様の指標を持つ成功した製品があるかどうかを確認することが重要である。
If you have similar numbers, then probably these underlying retention metrics are not the problem.  
もしあなたが同様の数値を持っているなら、おそらくこれらの基礎的なリテンション指標が問題ではない。

Let’s look there first, but understand that you might find a devastating truth.  
まずそこを見てみましょうが、壊滅的な真実を見つけるかもしれないことを理解してください。

<!-- ここまで読んだ! -->

## Admit it when people don’t want your product 人々があなたの製品を欲しがらないときはそれを認める

There’s an ugly truth that when most products are put under a microscope, most of them simply don’t have the retention to sustain growth over time — this is “pouring water into a leaky bucket.”  
ほとんどの製品が顕微鏡で見られるとき、**ほとんどの製品は単に成長を持続するためのリテンションがないという醜い真実がある – これは「漏れたバケツに水を注ぐ」こと**だ。(この例え、たまに聞くな...!:thinking:)
A slow growth rate is inevitable because products start at a mega disadvantage of needing to replace all their existing users who churn, in addition to building new marketing channels that grow the overall number significantly.  
成長率が遅いのは避けられない。なぜなら、製品は流出する既存のユーザーをすべて置き換える必要があるという大きな不利な立場から始まり、全体の数を大幅に増やす新しいマーケティングチャネルを構築する必要があるからだ。

But “my product is not retaining” is also sometimes a fancy phrase for “people don’t want to use my product.”  
**しかし「私の製品はリテンションがない」というのは、「人々は私の製品を使いたくない」ということを表す洗練された表現でもある**。
I say this because it’s a blunt way of stating what’s often true – that a new product is too experimental, too unpolished, or so poorly positioned, or underdeveloped, that no one wants to use it.  
私はこれを言うのは、しばしば真実であることを率直に述べる方法だからだ – 新しい製品はあまりにも実験的で、あまりにも未完成で、またはあまりにも不適切に位置づけられているか、未発達であるため、誰もそれを使いたくない。
I think this was especially a problem in the Web 2.0 days when folks would combine their favorite random set of product mechanics — disappearing text messages sent to strangers near you, but you can only reply with a video — and launch them as the latest app (Disappr! – gotta love those 2010 app names).  
私は、特にWeb 2.0の時代に、皆が自分のお気に入りのランダムな製品メカニクスを組み合わせて（近くの見知らぬ人に送られる消えるテキストメッセージ、しかし返信はビデオだけ）、最新のアプリとして立ち上げたことが問題だったと思う（Disappr! – 2010年のアプリ名が好きだ）。
When people don’t want your product, no amount of new customer acquisition is going to solve that.  
人々があなたの製品を欲しがらないとき、新しい顧客獲得の量がそれを解決することはない。
Yes, you can sometimes generate very fast growth rates for a few weeks or months, but eventually, it catches up to you.  
はい、時には数週間または数ヶ月の間に非常に速い成長率を生み出すことができるが、最終的にはそれがあなたに追いつく。
And then the product stalls, per the graph above.  
そして、製品は停滞する、上のグラフの通りに。

Instead, when initial product/market fit is low (yes, another fancy way to say people don’t get it), I usually recommend the exercise of positioning more closely to existing product categories.  
代わりに、初期のプロダクト/マーケットフィットが低いとき（はい、これは人々が理解していないと言う別の洗練された方法です）、私は通常、既存の製品カテゴリにより近い位置づけを行うことを推奨する。
As I argue in Zero to Product/Market Fit, any founder can instantly get to product/market fit by simply going after an existing category — of course, we all know how to build and design a coffee cup such that there’s product/market fit.  
**私が[「Zero to Product/Market Fit」](https://andrewchen.com/zero-to-productmarket-fit-presentation/)で主張するように、どの創業者も既存のカテゴリを追求することで瞬時にプロダクト/マーケットフィットに到達できる** – もちろん、私たちは皆、プロダクト/マーケットフィットがあるようにコーヒーカップを作り、デザインする方法を知っている。

You incur other problems, of course, such as competitive differentiation, but if you combine a well-known product category with innovation, and picking at the right time and place in the innovation cycle, it can work.  
もちろん、競争の差別化などの他の問題が発生するが、よく知られた製品カテゴリと革新を組み合わせ、革新サイクルの適切なタイミングと場所を選ぶことで、うまくいくことがある。

There are major questions to ask here:  
ここで尋ねるべき重要な質問がある：

- Does my product have a clear, successful competitor? Is there a there there? (and do I have strong differentiation?)  
- 私の製品には明確で成功した競合がいますか？そこに何かありますか？（そして、私は強い差別化を持っていますか？）

- When I ask people to describe my product back to me — without the jargon — what do they say?  
- 人々に私の製品を専門用語なしで説明してもらうと、彼らは何と言いますか？

- When I ask people during user tests what kind of people might use the product, and what they’d use instead, do the answers make sense?  
- ユーザーテスト中に人々にどのような人がその製品を使うか、そして代わりに何を使うかを尋ねたとき、答えは意味がありますか？

- Do people actually like my product, or are they just being nice to me? And a famous question- is it a painkiller or a vitamin?  
- 人々は実際に私の製品が好きですか、それともただ私に優しくしているだけですか？そして有名な質問 – それは痛み止めですか、それともビタミンですか？

- Are there any well-known product categories I could position against? Is there a way for me to test that positioning in user testing or otherwise?  
- 私が対抗できるよく知られた製品カテゴリはありますか？その位置づけをユーザーテストなどで試す方法はありますか？

- Is my growth the fault of shitty retention? Or do I need better user acquisition?  
- 私の成長はひどいリテンションのせいですか？それとも、より良いユーザー獲得が必要ですか？

When retention sucks, but you haven’t growth hacked yet  
リテンションが悪いとき、しかしまだグロースハックしていない場合

What if retention sucks, but you haven’t added email notifications yet?  
リテンションが悪いとき、しかしまだメール通知を追加していない場合はどうしますか？

What if you can just do a big marketing push, and that might spike the numbers?  
大規模なマーケティングプッシュを行うことができ、その結果数字が急増するかもしれない場合はどうしますか？

I can tell you as someone who has seen many underlying metrics for a wide variety of products, moving the retention number is the very hardest thing to move.  
私は、さまざまな製品の多くの基礎的な指標を見てきた者として、リテンションの数値を動かすことが最も難しいことだと言えます。

Usually, the initial numbers are a ceiling, and it only goes down from there.  
通常、初期の数値は上限であり、そこから下がるだけです。

So if your numbers are bad, don’t think that adding notification emails will solve it.  
したがって、あなたの数値が悪い場合、通知メールを追加することで解決できるとは思わないでください。

There is a very very narrow set of situations where I will take this back:  
私がこれを撤回する非常に狭い状況がある：

First, long-term retention is often most improved by better initial user activation.  
まず、長期的なリテンションは、より良い初期ユーザーアクティベーションによって最も改善されることが多い。

A few years ago, in Losing 80% of mobile users is normal, and why the best apps do better, I show that the biggest difference in the retention curves of the best apps and mildly good apps wasn’t as much in their long-term retention curves, as much as their ability to get the numbers in the first 7 days up higher than others.  
数年前、「モバイルユーザーの80%を失うのは普通であり、なぜ最高のアプリがより良いのか」で、最高のアプリとやや良いアプリのリテンションカーブの最大の違いは、長期的なリテンションカーブにあるのではなく、最初の7日間の数値を他よりも高くする能力にあったことを示しました。

So I often will ask the question to product leaders- what differentiates someone who’s activated versus not, in your product?  
したがって、私はしばしばプロダクトリーダーに質問します – あなたの製品において、アクティベートされた人とそうでない人を区別するものは何ですか？

What % of users become activated? And how do you make that 100%?  
何%のユーザーがアクティベートされますか？そして、それを100%にするにはどうすればよいですか？

Second, there’s a narrow class of products that have network effects — social apps, workplace collaboration tools, dating apps, marketplaces, etc — and they will often have a “smile curve” when retention goes up as time passes, and the network fills in.  
次に、ネットワーク効果を持つ製品の狭いクラスがある – ソーシャルアプリ、職場のコラボレーションツール、デーティングアプリ、マーケットプレイスなど – そして、リテンションが時間とともに上昇し、ネットワークが充実する際に「スマイルカーブ」を持つことが多い。

I wrote a whole book about this so I won’t belabor the point, but the main point is, if a product is more useful when more of your friends (or colleagues) are using it, then retention will naturally float up as the product grows.  
私はこれについての本を一冊書いたので、詳細には触れませんが、主なポイントは、製品がより多くの友人（または同僚）が使用しているときにより便利であれば、製品が成長するにつれてリテンションは自然に上昇するということです。

Thus, a product that has poor retention in the early days might just need more network density.  
したがって、初期にリテンションが悪い製品は、単にネットワークの密度が必要なだけかもしれません。

For these situations, I might suggest the team do a completely manual, hands-on build of a network — launching at a high school or a single office — and measure retention there.  
これらの状況では、チームにネットワークの完全に手動での構築を提案するかもしれません – 高校や単一のオフィスで立ち上げ、そこでリテンションを測定します。

Sometimes it’s much higher, which means there’s a there there, and the product just needs to be launched in a network-by-network manner as some of the great companies have done via college campuses, cities, workplaces, or otherwise.  
時にはそれがはるかに高くなることがあり、それはそこに何かがあることを意味し、製品は単にネットワークごとに立ち上げる必要がある、いくつかの偉大な企業が大学キャンパス、都市、職場などを通じて行ったように。

Whatever you do, don’t fall for the idea that you can fix your retention by simply adding features:  
何をしても、単に機能を追加することでリテンションを修正できるという考えに騙されないでください：

The Next Feature Fallacy: the fallacy that the next feature you add will suddenly make people want to use the entire product. -@bokardo  
次の機能の誤謬：次に追加する機能が突然人々に製品全体を使いたいと思わせるという誤謬。 -@bokardo

There’s a longer explanation of the idea here, but the TLDR is that when you add features that engage hardcore users, that’s going to be such a small % when in reality you need to stem the bleed in D1/D2/…D7.  
ここにはこのアイデアの長い説明がありますが、要するに、ハードコアユーザーを引き付ける機能を追加すると、それは非常に小さな%になるが、実際にはD1/D2/…D7の流出を止める必要があるということです。

That is, in the activation step of the product.  
つまり、製品のアクティベーションステップにおいてです。

If you get 10% of your hardcore users to engage more deeply, the reality is that it won’t move the needle enough mathematically to lift your entire retention curve.  
もしハードコアユーザーの10%がより深く関与するようになったとしても、実際にはそれが全体のリテンションカーブを持ち上げるのに十分な影響を与えないということです。

This means that you need to listen to the “silent majority” of users who churn, rather than the core users who stay and are highly vocal.  
これは、残っているコアユーザーの声が大きいのではなく、流出する「静かな多数」のユーザーの声に耳を傾ける必要があることを意味します。

Thus, I’d ask myself the following questions:  
したがって、私は自分に次の質問をします：

- How is my retention? Am I counting on the ability to move metrics far beyond what’s reasonable? (You can increase 20%, but probably not 100%)  
- 私のリテンションはどうですか？私は指標を合理的な範囲を超えて動かす能力に頼っていますか？（20%は増やせますが、おそらく100%は無理です）

- Am I betting the farm on some product magic that hardcore users want? Or am I working on things that cause more newbies to love the product more quickly?  
- 私はハードコアユーザーが望む製品の魔法に全てを賭けていますか？それとも、より多くの新規ユーザーが製品をより早く好きになるようなことに取り組んでいますか？

- Is my product in the category where network effects might substantially grow retention? Is that reasonable to think?  
- 私の製品はネットワーク効果がリテンションを大幅に成長させる可能性のあるカテゴリにありますか？それは合理的に考えられますか？

Top of funnel  
ファネルの上部

It makes me happy when I see strong retention numbers with a flat growth curve.  
強いリテンション数値が横ばいの成長曲線とともに見えると、私は嬉しくなります。

Funny enough, I consider this a very good thing.  
面白いことに、私はこれを非常に良いことだと考えています。

The history of fixing these situations is much better, and the approach is usually quite simple: Find more marketing channels, and scale existing ones.  
これらの状況を修正する歴史ははるかに良好であり、アプローチは通常非常にシンプルです：より多くのマーケティングチャネルを見つけ、既存のものをスケールアップします。

And if you can, find a self-repeating growth loop where users sign up for your product, use it, and then help generate more signups over time.  
そして、可能であれば、ユーザーがあなたの製品にサインアップし、それを使用し、時間の経過とともにさらに多くのサインアップを生成する自己反復的な成長ループを見つけてください。

Just avoid the random lightning strikes.  
ただし、ランダムな雷のような出来事は避けてください。

This could be from tech news coverage, a viral TikTok video, or a one-time email blast.  
これは、テクノロジーニュースの報道、バイラルTikTokビデオ、または一度限りのメール配信から来る可能性があります。

You feel good for a moment, and when the excitement (and growth curve) dies down, then the crisis begins.  
一瞬気分が良くなりますが、興奮（と成長曲線）が収まると、危機が始まります。

It might be a fine way to solve a cold start problem or to get your first few hundred users.  
それはコールドスタートの問題を解決したり、最初の数百人のユーザーを獲得するための良い方法かもしれません。

But it’s not a real growth strategy and leads to a product that’s lurching from crisis to crisis.  
しかし、それは本当の成長戦略ではなく、危機から危機へと揺れ動く製品につながります。

Instead, the focus needs to be on repeatability, particularly once retention is established.  
その代わりに、特にリテンションが確立された後は、再現性に焦点を当てる必要があります。

The easiest way to find a repeatable strategy is by simply fast-following other companies in your space.  
再現可能な戦略を見つける最も簡単な方法は、単にあなたの分野の他の企業を迅速に追随することです。

Finding and scaling marketing channels is typically pretty easy.  
マーケティングチャネルを見つけてスケールアップすることは通常非常に簡単です。

If they are doing paid marketing, then go into those channels and test for CAC and measure payback periods.  
彼らが有料マーケティングを行っている場合は、そのチャネルに入り、CACをテストし、回収期間を測定します。

If they are marketing via Twitch creators or Instagram influencers, try that too.  
彼らがTwitchクリエイターやInstagramインフルエンサーを通じてマーケティングしている場合も、それを試してみてください。

This method of simply experimenting and copying the competition goes a long way and often leads to success.  
単に実験し、競争を模倣するこの方法は大きな効果があり、しばしば成功につながります。

Testing marketing channels, alongside ad creatives and call-to-actions, requires an entrepreneurial spirit.  
マーケティングチャネル、広告クリエイティブ、コールトゥアクションをテストするには、起業家精神が必要です。

There’s a huge advantage to testing a lot of different ideas, creatives, and landing pages and experimenting with messaging.  
さまざまなアイデア、クリエイティブ、ランディングページをテストし、メッセージングを実験することには大きな利点があります。

Growth loops scale and scale  
成長ループはスケールし続ける

Figuring out a growth loop is even more powerful.  
成長ループを見つけることはさらに強力です。

The idea here is that the loop helps attract users, who take actions that attract even more users, and so on.  
ここでのアイデアは、ループがユーザーを引き付け、そのユーザーがさらに多くのユーザーを引き付ける行動を取るということです。

Thus a product with 10,000 users will grow quickly, but when it hits 1M actives, it can go even faster.  
したがって、10,000人のユーザーを持つ製品は迅速に成長しますが、1Mのアクティブユーザーに達すると、さらに速く成長することができます。

This means user acquisition is a function of the size of the user base, and thus, it will keep up with the churn curve that’s stalking just behind it.  
これは、ユーザー獲得がユーザーベースのサイズの関数であり、したがって、流出曲線に追いつくことを意味します。

I have a few examples in my Magic Numbers deck, where I illustrate these as some of the classic and ideal growth loops:  
私の「Magic Numbers」デッキにはいくつかの例があり、これらを古典的で理想的な成長ループのいくつかとして示しています：

Above: Viral loops are important because they are extremely scalable, free, and don’t require a formal partnership.  
上記：バイラルループは重要です。なぜなら、それらは非常にスケーラブルで、無料であり、正式なパートナーシップを必要としないからです。

This is based on users directly or indirectly sharing a product with their friends/colleagues, and having that loop repeat itself.  
これは、ユーザーが友人や同僚と製品を直接または間接的に共有し、そのループが繰り返されることに基づいています。

Above: A product like Yelp or Houzz fundamentally is a UGC SEO driven loop.  
上記：YelpやHouzzのような製品は、基本的にUGC SEO駆動のループです。

New users find content through Google, a small % of them generate more content, which then gets indexed by Google, and then the loop repeats.  
新しいユーザーはGoogleを通じてコンテンツを見つけ、そのうちの小さな%がさらに多くのコンテンツを生成し、それがGoogleにインデックスされ、ループが繰り返されます。

Reddit is also like this. So is Glassdoor. And so on.  
Redditもこのようなものです。Glassdoorもそうです。そしてそのように続きます。

The process of figuring out these growth loops is not an easy task- it’s a form of product-led growth that requires an understanding of marketing, product, and sometimes growth hacking the underlying platforms/APIs to get a leg up (as Zynga did on Facebook, and Paypal did on eBay).  
これらの成長ループを見つけるプロセスは簡単な作業ではありません – それはマーケティング、製品の理解を必要とし、時には基盤となるプラットフォーム/APIをグロースハックする形の製品主導の成長です（ZyngaがFacebookで、PaypalがeBayで行ったように）。

But it’s very powerful when done well.  
しかし、うまく行われたときには非常に強力です。

Polish your the UX flows that matter to growth — signup, inviting, payment — and ignore your hardcore user features  
成長に重要なUXフローを磨く – サインアップ、招待、支払い – そしてハードコアユーザーの機能を無視する

For teams that are focused on growth, it’s uncomfortable but necessary to ignore your best users and instead focus on UX targeted at users who may not be vocal at all.  
成長に焦点を当てているチームにとって、最良のユーザーを無視し、声を上げない可能性のあるユーザーに焦点を当てることは不快ですが必要です。

If you can polish your new user flow, then you can often make 20-50% gains to conversion, which then fall straight into the bottom line (whether that’s revenue or an active users count).  
新しいユーザーフローを磨くことができれば、通常はコンバージョンを20-50%向上させることができ、それが直接的に利益（収益またはアクティブユーザー数）に繋がります。

When you polish your friend invite flows or referral flows, then you might get 20% of users to invite 100% more of their friends.  
友人招待フローやリファラルフローを磨くと、ユーザーの20%が友人を100%多く招待することができるかもしれません。

And then that larger group of invitees will invite each more friends, and so on, with a larger viral factor.  
そして、その大きな招待者グループがさらに多くの友人を招待し、そのように続き、より大きなバイラル要因を持つことになります。

This is why when I assess product UX, I tend to focus on the less sexy stuff: Signup flows, invitations/referrals, and payment.  
これが、私が製品のUXを評価する際に、あまり魅力的でないものに焦点を当てる理由です：サインアップフロー、招待/リファラル、そして支払い。

And even surface areas like the lost password flow, which is for larger products, often block engaged users from getting back into their accounts.  
そして、より大きな製品のためのパスワードを忘れたフローのような表面領域でさえ、しばしば関与しているユーザーがアカウントに戻るのを妨げます。

Unfortunately, this is a product surface area that isn’t considered particularly sexy.  
残念ながら、これは特に魅力的とは見なされない製品の表面領域です。

If you’re at a large company, you may not get promoted to the next level of PM for delivering this type of project.  
大企業にいる場合、この種のプロジェクトを提供することで次のPMレベルに昇進することはないかもしれません。

In these settings, PMs are often rewarded more often for coordinating massive cross-functional projects than to move the needle on growth, by simply testing dozens of variations of signup flows.  
これらの環境では、PMはしばしば成長を促進するために、サインアップフローの数十のバリエーションをテストすることよりも、大規模なクロスファンクショナルプロジェクトを調整することで報酬を得ることが多いです。

And yet, this is often what matters!  
それでも、これはしばしば重要なことです！

There are a couple of key things I’ll often assess when looking at these growth-critical user flows:  
これらの成長に重要なユーザーフローを見ているときに、私がしばしば評価するいくつかの重要な点があります：

- Are the value props clear, the headlines crisp, and generating urgency for the user?  
- 価値提案は明確で、見出しは鮮明で、ユーザーに緊急性を生み出していますか？

- Are all critical elements — buttons, form fields, etc — above the fold?  
- すべての重要な要素（ボタン、フォームフィールドなど）は、折り返し線の上にありますか？

- Are extraneous links removed, to not divert the user, or otherwise moved to below the fold?  
- 不要なリンクは削除されており、ユーザーを逸らさないように、または折り返し線の下に移動されていますか？

- Instead of asking users to scroll, can content turn into a video, animated GIF, or slideshow?  
- ユーザーにスクロールを求める代わりに、コンテンツをビデオ、アニメーションGIF、またはスライドショーに変えることができますか？

- How does it look on desktop versus mobile?  
- デスクトップとモバイルではどのように見えますか？

- If the signup process is multi-step, can some steps be skipped for now, and done later?  
- サインアッププロセスが複数のステップである場合、今は一部のステップをスキップし、後で行うことができますか？

- Is the order of the signup right? Can you bring forward the magic moment, rather than asking people to fill out form after form?  
- サインアップの順序は正しいですか？人々にフォームを次々と記入させるのではなく、魔法の瞬間を前に持ってくることができますか？

- Are there critical asks — getting a credit card, asking people to invite friends — that should be baked into the first few steps of the signup flow?  
- クレジットカードを取得する、友人を招待するように求めるなど、サインアップフローの最初の数ステップに組み込むべき重要な要求はありますか？

- Does the signup flow activate people correctly? Should the user be “forced” to activate in any way, by adding required signup steps?  
- サインアップフローは人々を正しくアクティベートしますか？ユーザーは、必要なサインアップステップを追加することで「強制的に」アクティベートされるべきですか？

- … and on and on  
- … そして続く

For new user flows, I try to get more users that hit the landing page to ultimately become activated users.  
新しいユーザーフローでは、ランディングページにアクセスしたユーザーが最終的にアクティベートされたユーザーになるように努めています。

I use tons of A/B testing and experiments in messaging to make this happen.  
これを実現するために、私は多くのA/Bテストとメッセージングの実験を使用します。

For invite flows, I often try to stick them to the end of sessions so that users repeatedly see them as they engage the product.  
招待フローでは、ユーザーが製品に関与する際に繰り返し見ることができるように、セッションの最後にそれらを配置するように努めます。

Maybe they create content, and you ask them if they want to share their newly created content with friends/coworkers.  
彼らがコンテンツを作成し、あなたが彼らに新しく作成したコンテンツを友人や同僚と共有したいかどうかを尋ねるかもしれません。

Do that every time, and you’ll be generating viral factor as you go, rather than just at the beginning.  
毎回それを行うと、最初だけでなく、進行中にバイラル要因を生成することになります。

Payment is similarly important for products that focus on paid marketing to grow.  
支払いも、成長のために有料マーケティングに焦点を当てる製品にとって同様に重要です。

The earlier you harvest purchase intent — often in the signup flow — the more you can plow that money into growth programs.  
購入意図を早く収穫するほど（通常はサインアップフローで）、そのお金を成長プログラムに投入することができます。

There are these flows and more, and they are the unsexy product features that drive growth.  
これらのフローやその他があり、これらは成長を促進する魅力的ではない製品機能です。

Some final thoughts  
いくつかの最終的な考え

Even great products stall growth.  
優れた製品でさえ成長が停滞する。

Famously, Facebook grew in its early years to take over colleges, but then saw a stall as saturation effects took over, and the product needed to be expanded past universities.  
有名なことに、Facebookは初期の数年間で大学を制圧するほど成長したが、その後、飽和効果が現れ、製品は大学を超えて拡張する必要があった。

Then there was another period of flatness, just before they expanded internationally.  
その後、国際的に拡張する直前に再び横ばいの期間があった。

And another, before mobile.  
そして、モバイルの前にも別の期間があった。

The same was true for Dropbox in its early years, as it saw a spike on Digg and Hacker News, but it needed a referral system and shared folders to push it to the next level.  
Dropboxも初期の数年間で同様で、DiggやHacker Newsで急増したが、次のレベルに進むためにはリファラルシステムと共有フォルダが必要だった。

And in recent years, TikTok stalled as a platform for dance videos before it was acquired, and a very large paid marketing effort helped push it over the top based on building out a massive library of content.  
最近では、TikTokはダンスビデオのプラットフォームとして停滞し、その後買収され、大規模な有料マーケティング努力が膨大なコンテンツライブラリを構築することでそれを押し上げた。

These stories are common because successful products inevitably saturate a market, or need to jump from one acquisition channel to another, or any number of problems.  
これらの物語は一般的であり、成功した製品は必然的に市場を飽和させるか、あるいは一つの獲得チャネルから別のチャネルに移行する必要があるか、またはさまざまな問題があるからです。

When this crisis happens, it’s easy and reflexive to simply try to spend more on marketing.  
この危機が発生したとき、マーケティングにもっとお金を使おうとするのは簡単で反射的です。

Or to try to develop more features.  
または、より多くの機能を開発しようとすることです。

Or some other simplistic rule like that, sometimes based on the natural ability and interests of the product team.  
または、そのような単純なルール、時には製品チームの自然な能力や興味に基づくものです。

Keep yourself from doing that.  
それを避けるようにしてください。

Instead, consider that every stalled growth curve has its idiosyncratic issues.  
代わりに、すべての停滞した成長曲線には特有の問題があることを考慮してください。

Sometimes it’s poor activation.  
時には、アクティベーションが不十分です。

Sometimes the novelty has worn off.  
時には新しさが失われています。

Or perhaps the product is seasonal, or a marketing channel has been saturated.  
あるいは、製品が季節的であるか、マーケティングチャネルが飽和している可能性があります。

For better or worse, finding the levers to correct the stall requires patience, analytical abilities, and deep customer empathy.  
良いことでも悪いことでも、停滞を修正するためのレバーを見つけるには、忍耐、分析能力、そして深い顧客への共感が必要です。

It’s hard, and every stalled product has its own story.  
それは難しく、すべての停滞した製品にはそれぞれの物語があります。

But to identify the problem, fix it, and see the graph return to its previous glory — well, that’s just an amazing thing.  
しかし、問題を特定し、修正し、グラフが以前の栄光に戻るのを見ることは – それは本当に素晴らしいことです。

I write a high-quality, weekly newsletter covering what's happening in Silicon Valley, focused on startups, marketing, and mobile.  
私は、スタートアップ、マーケティング、モバイルに焦点を当てたシリコンバレーで起こっていることをカバーする高品質の週刊ニュースレターを書いています。

Views expressed in “content” (including posts, podcasts, videos) linked on this website or posted in social media and other platforms (collectively, “content distribution outlets”) are my own and are not the views of AH Capital Management, L.L.C. (“a16z”) or its respective affiliates.  
このウェブサイトにリンクされた「コンテンツ」（投稿、ポッドキャスト、ビデオを含む）や、ソーシャルメディアや他のプラットフォームに投稿されたもの（総称して「コンテンツ配信アウトレット」）に表明された見解は私自身のものであり、AH Capital Management, L.L.C.（「a16z」）やその関連会社の見解ではありません。

AH Capital Management is an investment adviser registered with the Securities and Exchange Commission.  
AH Capital Managementは、証券取引委員会に登録された投資顧問です。

Registration as an investment adviser does not imply any special skill or training.  
投資顧問としての登録は、特別なスキルやトレーニングを意味するものではありません。

The posts are not directed to any investors or potential investors, and do not constitute an offer to sell -- or a solicitation of an offer to buy -- any securities, and may not be used or relied upon in evaluating the merits of any investment.  
これらの投稿は、いかなる投資家や潜在的な投資家に向けられたものではなく、いかなる証券を売るためのオファーや、買うためのオファーの勧誘を構成するものではなく、いかなる投資のメリットを評価する際に使用または依存することはできません。

The content should not be construed as or relied upon in any manner as investment, legal, tax, or other advice.  
このコンテンツは、投資、法的、税務、またはその他のアドバイスとして解釈されるべきではなく、依存されるべきでもありません。

You should consult your own advisers as to legal, business, tax, and other related matters concerning any investment.  
いかなる投資に関する法的、ビジネス、税務、その他の関連事項については、あなた自身のアドバイザーに相談するべきです。

Any projections, estimates, forecasts, targets, prospects and/or opinions expressed in these materials are subject to change without notice and may differ or be contrary to opinions expressed by others.  
これらの資料に表明された予測、推定、予測、目標、見通しおよび/または意見は、予告なしに変更される可能性があり、他の人が表明した意見と異なる場合や反する場合があります。

Any charts provided here are for informational purposes only, and should not be relied upon when making any investment decision.  
ここに提供されるチャートは情報提供の目的のみであり、いかなる投資決定を行う際に依存すべきではありません。

Certain information contained in here has been obtained from third-party sources.  
ここに含まれる特定の情報は、第三者の情報源から取得されています。

While taken from sources believed to be reliable, I have not independently verified such information and makes no representations about the enduring accuracy of the information or its appropriateness for a given situation.  
信頼できると考えられる情報源から取得されたものであるが、私はその情報を独自に検証しておらず、その情報の持続的な正確性や特定の状況に対する適切性については何の表明も行っていません。

The content speaks only as of the date indicated.  
このコンテンツは、示された日付のみに基づいています。

Under no circumstances should any posts or other information provided on this website -- or on associated content distribution outlets -- be construed as an offer soliciting the purchase or sale of any security or interest in any pooled investment vehicle sponsored, discussed, or mentioned by a16z personnel.  
このウェブサイト上で提供される投稿やその他の情報は、いかなる状況においても、a16zのスタッフがスポンサー、議論、または言及したいかなる証券やプール投資ビークルの購入または販売を勧誘するオファーとして解釈されるべきではありません。

Nor should it be construed as an offer to provide investment advisory services; an offer to invest in an a16z-managed pooled investment vehicle will be made separately and only by means of the confidential offering documents of the specific pooled investment vehicles -- which should be read in their entirety, and only to those who, among other requirements, meet certain qualifications under federal securities laws.  
また、投資顧問サービスを提供するオファーとして解釈されるべきではありません；a16zが管理するプール投資ビークルへの投資のオファーは、別途、特定のプール投資ビークルの機密提供文書によってのみ行われるものであり、これらは完全に読み、他の要件の中で連邦証券法の下で特定の資格を満たす者のみに提供されるべきです。

Such investors, defined as accredited investors and qualified purchasers, are generally deemed capable of evaluating the merits and risks of prospective investments and financial matters.  
そのような投資家は、認定投資家および適格購入者として定義され、一般的に将来の投資および財務問題のメリットとリスクを評価する能力があると見なされます。

There can be no assurances that a16z’s investment objectives will be achieved or investment strategies will be successful.  
a16zの投資目標が達成されることや、投資戦略が成功することを保証することはできません。

Any investment in a vehicle managed by a16z involves a high degree of risk including the risk that the entire amount invested is lost.  
a16zが管理するビークルへの投資は、投資した全額が失われるリスクを含む高いリスクを伴います。

Any investments or portfolio companies mentioned, referred to, or described are not representative of all investments in vehicles managed by a16z and there can be no assurance that the investments will be profitable or that other investments made in the future will have similar characteristics or results.  
言及された、参照された、または説明された投資やポートフォリオ企業は、a16zが管理するビークルにおけるすべての投資を代表するものではなく、投資が利益を生むことや、将来行われる他の投資が同様の特性や結果を持つことを保証することはできません。

A list of investments made by funds managed by a16z is available at https://a16z.com/investments/.  
a16zが管理するファンドによって行われた投資のリストは、https://a16z.com/investments/ で入手できます。

Excluded from this list are investments for which the issuer has not provided permission for a16z to disclose publicly as well as unannounced investments in publicly traded digital assets.  
このリストには、発行者がa16zに公開開示の許可を与えていない投資や、発表されていない上場デジタル資産への投資は含まれていません。

Past results of Andreessen Horowitz’s investments, pooled investment vehicles, or investment strategies are not necessarily indicative of future results.  
Andreessen Horowitzの投資、プール投資ビークル、または投資戦略の過去の結果は、必ずしも将来の結果を示すものではありません。

Please see https://a16z.com/disclosures for additional important information.  
追加の重要な情報については、https://a16z.com/disclosures をご覧ください。

About  
について

Andrew Chen is a partner at Andreessen Horowitz, where he invests in games, AR/VR, metaverse, and consumer tech startups.  
Andrew ChenはAndreessen Horowitzのパートナーであり、ゲーム、AR/VR、メタバース、消費者向けテクノロジースタートアップに投資しています。

He is the author of The Cold Start Problem, a book on starting and growing new startups via network effects.  
彼は「The Cold Start Problem」の著者であり、ネットワーク効果を通じて新しいスタートアップを立ち上げ、成長させることに関する本です。

He resides in Venice, California(more)  
彼はカリフォルニア州ヴェニスに住んでいます（詳細）。
