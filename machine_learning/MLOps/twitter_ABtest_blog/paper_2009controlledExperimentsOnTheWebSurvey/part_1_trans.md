## 0.1. link リンク

https://ai.stanford.edu/~ronnyk/2009controlledExperimentsOnTheWebSurvey.pdf
https://ai.stanford.edu/~ronnyk/2009controlledExperimentsOnTheWebSurvey.pdf

## 0.2. title タイトル

Controlled experiments on the web: survey and practical guide
ウェブ上での制御実験： サーベイと実践ガイド

## 0.3. abstract 抄録

The web provides an unprecedented opportunity to evaluate ideas quickly using controlled experiments, also called randomized experiments, A/B tests (and their generalizations), split tests, Control/Treatment tests, MultiVariable Tests (MVT) and parallel flights.
ウェブは、無作為化実験、A/Bテスト（およびその一般化）、スプリットテスト、コントロール/トリートメントテスト、マルチバリアブルテスト（MVT）、パラレルフライトとも呼ばれる**controlled experiments(統制実験)**を用いて、アイデアを迅速に評価する前例のない機会を提供する。
Controlled experiments embody the best scientific design for establishing a causal relationship between changes and their influence on user-observable behavior.
対照実験は、変化とそれがユーザーの観察可能な行動に及ぼす影響との間の因果関係を確立するための最良の科学的デザインを具現化するものである。
We provide a practical guide to conducting online experiments, where endusers can help guide the development of features.
エンドユーザーが機能開発の指針となるオンライン実験を実施するための実践的なガイドを提供する。
Our experience indicates that significant learning and return-on-investment (ROI) are seen when development teams listen to their customers, not to the Highest Paid Person’s Opinion (HiPPO).
私たちの経験によれば、開発チームが**Highest Paid Person’s Opinion(高給取りの意見, HiPPO)**ではなく、顧客の意見に耳を傾けることで、大きな学びと**return-on-investment(投資対効果, ROI)**が得られる。
We provide several examples of controlled experiments with surprising results.
意外な結果をもたらした対照実験の例をいくつか紹介する。
We review the important ingredients of running controlled experiments, and discuss their limitations (both technical and organizational).
対照実験を実施するための重要な要素をレビューし、その限界（技術的、組織的な両方）について議論する。
We focus on several areas that are critical to experimentation, including statistical power, sample size, and techniques for variance reduction.
我々は、統計的検出力、サンプルサイズ、分散削減のテクニックなど、実験にとって重要ないくつかの分野に焦点を当てている。
We describe common architectures for experimentation systems and analyze their advantages and disadvantages.
実験システムの一般的なアーキテクチャを説明し、その長所と短所を分析する。
We evaluate randomization and hashing techniques, which we show are not as simple in practice as is often assumed.
我々はランダム化とハッシュ化技術を評価するが、これらは一般に考えられているほど実際には単純ではないことを示す。
Controlled experiments typically generate large amounts of data, which can be analyzed using data mining techniques to gain deeper understanding of the factors influencing the outcome of interest, leading to new hypotheses and creating a virtuous cycle of improvements.
対照実験は通常、大量のデータを生成し、データマイニング技術を用いて、興味のある結果に影響を与える要因についての深い理解を得ることができ、新しい仮説を立て、改善の好循環を生み出すことができる。
Organizations that embrace controlled experiments with clear evaluation criteria can evolve their systems with automated optimizations and real-time analyses.
明確な評価基準を持つ対照実験を受け入れる組織は、自動最適化とリアルタイム分析を用いてシステムを進化させることができる。
Based on our extensive practical experience with multiple systems and organizations, we share key lessons that will help practitioners in running trustworthy controlled experiments.
複数のシステムと組織での豊富な実践経験に基づいて、実践者が信頼性のある対照実験を実施するのに役立つ重要な教訓を共有する。

# 1. Introduction はじめに

One accurate measurement is worth more than a thousand expert opinions – Admiral Grace Hopper In the 1700s, a British ship’s captain observed the lack of scurvy among sailors serving on the naval ships of Mediterranean countries, where citrus fruit was part of their rations.
**正確な測定は、1000人の専門家の意見に値する** - グレース・ホッパー提督 18世紀、イギリスの船長は、地中海諸国の海軍艦船で勤務する船員たちの間で壊血病が見られないことに気づいた。地中海諸国の船員の食事には柑橘類が含まれていた。
He then gave half his crew limes (the Treatment group) while the other half (the Control group) continued with their regular diet.
そして、乗組員の半数（治療グループ）にライムを与え、残りの半数（対照グループ）は通常の食事を続けた。
Despite much grumbling among the crew in the Treatment group, the experiment was a success, showing that consuming limes prevented scurvy.
治療グループの乗組員からは不満の声が上がったが、実験は成功し、ライムの摂取が壊血病を予防することが示された。
While the captain did not realize that scurvy is a consequence of vitamin C deficiency, and that limes are rich in vitamin C, the intervention worked.
壊血病がビタミンC欠乏の結果であること、ライムがビタミンCを豊富に含んでいることを船長は知らなかったが、介入は功を奏した。
British sailors eventually were compelled to consume citrus fruit regularly, a practice that gave rise to the still-popular label limeys (Rossi et al.2003; Marks 2000).
イギリスの船員たちは、やがて柑橘類を常食するようになり、この習慣が今でも人気のあるライムというラベルを生んだ（Rossi et al.2003; Marks 2000）。

Some 300 years later, Greg Linden at Amazon created a prototype to show personalized recommendations based on items in the shopping cart (Linden 2006a, b).
それから約300年後、アマゾンのグレッグ・リンデンは、**ショッピングカート内の商品に基づいてパーソナライズされた推薦を表示するプロトタイプ**を作成した（リンデン2006a、b）。
You add an item, recommendations show up; add another item, different recommendations show up.
アイテムを追加するとおすすめが表示され、別のアイテムを追加すると別のおすすめが表示される。
Linden notes that while the prototype looked promising, “a marketing senior vice-president was dead set against it,” claiming it will distract people from checking out.
リンデンは、プロトタイプは有望に見えたが、「マーケティング担当の上級副社長は、チェックアウトの気をそらせるとして、断固反対した」と指摘する。
Greg was “forbidden to work on this any further.” Nonetheless, Greg ran a controlled experiment, and the “feature won by such a wide margin that not having it live was costing Amazon a noticeable chunk of change.
グレッグは「これ以上このプロジェクトに取り組むことを禁じられた」。それにもかかわらず、グレッグは対照実験を実施し、「その機能は圧倒的な差で勝利し、**それを実装していないことがアマゾンにかなりの損失をもたらしていた**」と述べている。
With new urgency, shopping cart recommendations launched.” Since then, multiple sites have copied cart recommendations.
新たな緊急性をもって、ショッピングカートの推薦が開始された。それ以来、複数のサイトがカート推薦をコピーしている。

The authors of this paper were involved in many experiments at Amazon, Microsoft, Dupont, and NASA.
この論文の著者たちは、アマゾン、マイクロソフト、デュポン、NASAで多くの実験に携わった。
The culture of experimentation at Amazon, where data trumps intuition (Kohavi et al.2004), and a system that made running experiments easy, allowed Amazon to innovate quickly and effectively.
データが直感を凌駕するアマゾンの実験文化（Kohavi et al.2004）と、実験を容易に実行できるシステムが、アマゾンの迅速かつ効果的なイノベーションを可能にした。
At Microsoft, there are multiple systems for running controlled experiments.
マイクロソフトでは、管理された実験を実行するための複数のシステムがある。
We describe several architectures in this paper with their advantages and disadvantages.
本稿では、いくつかのアーキテクチャについて、それぞれの長所と短所を説明する。
A unifying theme is that controlled experiments have great return-on-investment (ROI) and that building the appropriate infrastructure can accelerate innovation.
統一されたテーマは、**対照実験は大きな投資対効果（ROI）を持ち、適切なインフラを構築することでイノベーションを加速させることができる**ということである。
Stefan Thomke’s book title is well suited here: Experimentation Matters (Thomke 2003).
ステファン・トムケの著書のタイトルは、ここにぴったりである：実験は重要である（Thomke 2003）。

The web provides an unprecedented opportunity to evaluate ideas quickly using controlled experiments, also called randomized experiments (single-factor or factorial designs), A/B tests (and their generalizations), split tests, Control/Treatment, and parallel flights.
ウェブは、無作為化実験（単一要因または因子設計）、A/Bテスト（およびその一般化）、スプリットテスト、コントロール/トリートメント、パラレルフライトとも呼ばれる**controlled experiments(統制実験)**を用いて、アイデアを迅速に評価する前例のない機会を提供する。
In the simplest manifestation of such experiments, live users are randomly assigned to one of two variants: (i) the Control, which is commonly the “existing” version, and (ii) the Treatment, which is usually a new version being evaluated.
このような実験の最も単純な表現では、ライブユーザは、2つのvariantのうちの1つにランダムに割り当てられる：（i）コントロール、通常は「既存」のバージョンであり、（ii）トリートメント、通常は評価されている新しいバージョンである。
Metrics of interest, ranging from runtime performance to implicit and explicit user behaviors and survey data, are collected.
実行時のパフォーマンスから暗黙的および明示的なユーザーの行動、調査データまで、関心のあるmetricsが収集される。
Statistical tests are then conducted on the collected data to evaluate whether there is a statistically significant difference between the two variants on metrics of interest, thus permitting us to retain or reject the (null) hypothesis that there is no difference between the versions.
そして、収集されたデータに対して統計的検定が行われ、関心のあるmetricsにおいて2つのバリアントの間に統計的に有意な差があるかどうかを評価し、バージョン間に差がない（null）仮説を採択または棄却することができる。
In many cases, drilling down to segments of users using manual (e.g., OLAP) or machine learning and data mining techniques, allows us to understand which subpopulations show significant differences, thus helping improve our understanding and progress forward with an idea.
多くの場合、**手動（例：OLAP）または機械学習およびデータマイニング技術を使用してユーザのセグメントに掘り下げることで、どのサブポピュレーションが有意な差を示すかを理解し、アイデアを進めるための理解を深めることができる**。(推薦のABテストの場合、全体で見ると差がないが、新規ユーザには効果がありそう...みたいな?:thinking)

Controlled experiments provide a methodology to reliably evaluate ideas.
管理された実験は、アイデアを確実に評価するための方法論を提供する。
Unlike other methodologies, such as post-hoc analysis or interrupted time series (quasi experimentation) (Charles and Melvin 2004), this experimental design methodology tests for causal relationships (Keppel et al.1992, pp.5–6).
他の方法論（例：事後分析や中断された時間系列（準実験）（Charles and Melvin 2004））とは異なり、この実験デザイン方法論は因果関係をテストする（Keppel et al.1992, pp.5–6）。(RCTだからか...!)
Most organizations have many ideas, but the return-on-investment (ROI) for many may be unclear and the evaluation itself may be expensive.
たいていの組織は多くのアイデアを持っているが、その多くは投資対効果（ROI）が不明確であり、評価自体が高コストであることがある。
As shown in the next section, even minor changes can make a big difference, and often in unexpected ways.
次のセクションで示すように、**些細な変更であっても大きな違いを生むことがあり、それはしばしば予期せぬ方法**である。
A live experiment goes a long way in providing guidance as to the value of the idea.
実戦的な実験は、アイデアの価値について指針を与えてくれる。
Our contributions include the following.
私たちの貢献は以下の通り。

- In Sect.3 we review controlled experiments in a web environment and provide a rich set of references, including an important review of statistical power and sample size, which are often missing in primers.
  第3節では、ウェブ環境での対照実験をレビューし、**入門書では不足しがちな統計的検出力とサンプルサイズに関する重要なレビュー**を含む、豊富な参考文献を提供する。
  We then look at techniques for reducing variance that we found useful in practice.
  続いて、**実際に役立つと思われる分散を減らすテクニック**を紹介する。
  We also discuss extensions and limitations so that practitioners can avoid pitfalls.
  また、実務家が落とし穴を回避できるよう、拡張性と限界についても議論する。
- In Sect.4, we present several alternatives to MultiVariable Tests (MVTs) in an online setting.
  第4節では、オンライン設定における多変量検定（MVT）の代替案をいくつか紹介する。(variantが3つ以上のテスト??)
  In the software world, there are sometimes good reasons to prefer concurrent uni-variate tests over traditional MVTs.
  ソフトウェアの世界では、伝統的なMVTよりもコンカレント単変量テストを好む正当な理由が存在することがある。
- In Sect.5, we present generalized architectures that unify multiple experimentation systems we have seen, and we discuss their pros and cons.
  第5節では、これまで見てきた複数の実験システムを統合する**一般化されたアーキテクチャ**を提示し、その長所と短所について議論する。
  We show that some randomization and hashing schemes fail conditional independence tests required for statistical validity.
  我々は、いくつかのランダム化とハッシュ化スキームが、統計的妥当性に必要な条件付き独立性テストに失敗することを示す。
- In Sect.6 we provide important practical lessons.
  第6節では、重要な実践的教訓を示す。

When a company builds a system for experimentation, the cost of testing and experimental failure becomes small, thus encouraging innovation through experimentation.
**企業が実験のためのシステムを構築すれば、テストや実験の失敗にかかるコストは小さくなり、実験によるイノベーションが促進される**。
Failing fast and knowing that an idea is not as great as was previously thought helps provide necessary course adjustments so that other more successful ideas can be proposed and implemented.
**素早く失敗**し、そのアイデアが以前考えられていたほど素晴らしいものではないことを知ることで、より成功する他のアイデアを提案し、実行できるよう、必要な軌道修正を行うことができる。(うんうん、高速なフィードバック...!)

# 2. Motivating examples やる気を起こさせる例

The fewer the facts, the stronger the opinion – Arnold Glasow
事実が少なければ少ないほど、意見は強くなる - アーノルド・グラソー

The following examples present surprising results in multiple areas.
以下の例は、複数の分野で驚くべき結果を示している。
The first two deal with small UI changes that result in dramatic differences.
最初の2つは、劇的な違いをもたらす小さなUIの変更を扱ったものだ。
The third example shows how controlled experiments can be used to make a tradeoff between short-term revenue from ads and the degradation in the user experience.
3つ目の例は controlled experimentsが、**広告からの短期的な収益とユーザーエクスペリエンスの低下とのトレードオフを行うためにどのように使用されるか**を示している。
The fourth example shows the use of controlled experiments in backend algorithms, in this case search at Amazon.
4つ目の例は、バックエンドのアルゴリズム(この場合はアマゾンの検索)における対照実験の利用を示している。

## 2.1. Checkout page at Doctor FootCare

The conversion rate of an e-commerce site is the percentage of visits to the website that include a purchase.
Eコマースサイトの**コンバージョン率とは、ウェブサイトへの訪問のうち、購入に至った割合のことである**。
The following example comes from Bryan Eisenberg’s articles (Eisenberg 2003a, b).
次の例は、ブライアン・アイゼンバーグの論文（Eisenberg 2003a、b）から引用したものである。

Can you guess which one has a higher conversion rate and whether the difference is significant? There are nine differences between the two variants of the Doctor FootCare checkout page shown in Fig.1.If a designer showed you these and asked which one should be deployed, could you tell which one results in a higher conversion rate? Could you estimate what the difference is between the conversion rates and whether that difference is significant? We encourage you, the reader, to think about this experiment before reading the answer.
どちらがコンバージョン率が高いか、またその差が有意かどうか、**あなたは推測できますか？**図1に示すドクターフットケアのチェックアウトページの2つのバリエーションには9つの違いがあります。もしデザイナーがこれらをあなたに見せて、どちらを展開すべきかと尋ねたら、どちらがより高いコンバージョン率になるか分かりますか？コンバージョン率の差はどれくらいか、またその差は有意かどうか推定できますか？読者の皆さんには、答えを読む前に、この実験について考えてみていただきたい。
Can you estimate which variant is better and by how much? It is very humbling to see how hard it is to correctly predict the answer.
どのバリアントがどれだけ優れているか予想できますか？**答えを正しく予測することがいかに難しいか**を目の当たりにして、とても身が引き締まる思いです。
Please, challenge yourself!
どうぞ、挑戦してください！

Variant A in Fig.1 outperformed variant B by an order of magnitude.
図1のバリエーションAは、バリエーションBを桁違いに上回った。
In reality, the site “upgraded” from the A to B and lost 90% of their revenue! Most of the changes in the upgrade were positive, but the coupon code was the critical one: people started to think twice about whether they were paying too much because there are discount coupons out there that they do not have.
実際には、このサイトはAからBに "アップグレード "し、収益の90％を失った！アップグレードの変更のほとんどは肯定的なものだったが、クーポンコードは決定的なものだった： 人々は、自分たちが持っていない割引クーポンが世の中に出回っているため、払いすぎていないかどうか、よく考えるようになったのだ。
By removing the discount code from the new version (B), conversion-rate increased 6.5% relative to the old version (A) in Fig.2.
新バージョン(B)から割引コードを削除することで、コンバージョン率は図2の旧バージョン(A)に対して6.5％増加した。

## 2.2. Ratings of Microsoft Office help articles Microsoft Office ヘルプ記事の評価

Users of Microsoft Office who request help (or go through the Office Online website at http://office.microsoft.com) are given an opportunity to rate the articles they read.
マイクロソフト・オフィスのユーザーで、ヘルプをリクエストした人（またはオフィス・オンラインのウェブサイトhttp://office.microsoft.com）には、読んだ記事を評価する機会が与えられている。
The initial implementation presented users with a Yes/No widget.
最初の実装では、Yes/Noのウィジェットがユーザーに表示された。
The team then modified the widget and offered a 5-star ratings.
その後、チームはウィジェットを修正し、5つ星の評価を提供した。

The motivations for the change were the following:
変更の動機は以下の通りである：
1.The 5-star widget provides finer-grained feedback, which might help better evaluate content writers.
1.5つ星ウィジェットは、より細かいフィードバックを提供し、コンテンツライターをよりよく評価するのに役立つかもしれない。
2.The 5-star widget improves usability by exposing users to a single feedback box as opposed to two separate pop-ups (one for Yes/No and another for Why).
2.5つ星ウィジェットは、2つの別々のポップアップ（1つは「はい/いいえ」、もう1つは「なぜ」）ではなく、1つのフィードバックボックスにユーザーをさらすことで、ユーザビリティを向上させます。

Can you estimate which widget had a higher response rate, where response is any interaction with the widget? The surprise here was that number of ratings plummeted by about 90%, thus significantly missing on goal #2 above.
どのウィジェットの回答率が高かったか推定できますか？ここで、回答とはウィジェットとのインタラクションのことです。ここでの驚きは、評価の数が約90%も激減したことで、上記のゴール#2を大幅に逃してしまったことである。
Based on additional tests, it turned out that the two-stage model helps in increasing the response rate.
追加テストによると、2段階モデルは回答率の向上に役立つことが判明した。
Specifically, a controlled experiment showed that the widget shown in Fig.3, which was a two-stage model and also clarified the 5-stars direction as “Not helpful” to “Very helpful” outperformed the one in Fig.4 by a factor of 2.2, i.e., the response rate was 2.2 times higher.
具体的には、対照実験により、2段階モデルであり、5つ星の方向を「役に立たなかった」から「とても役に立った」まで明確化した図3のウィジェットが、図4のウィジェットを2.2倍、すなわち回答率が2.2倍上回ることが示された。
Even goal #1 was somewhat of a disappointment as most people chose the extremes (one or five stars).
ほとんどの人が両極端（1つ星か5つ星）を選んだため、ゴール1でもやや期待外れだった。
When faced with a problem for which you need help, the article either helps you solve the problem or it does not! The team finally settled on a yes/no/I-don’t-know option, which had a slightly lower response rate than just yes/no, but the additional information was considered useful.
助けが必要な問題に直面したとき、その記事は問題解決に役立つか、そうでないかのどちらかである！最終的にチームは、「はい／いいえ／わからない」という選択肢に落ち着き、回答率は「はい／いいえ」よりも若干低かったが、追加情報は有用であると考えられた。

## 2.3. MSN home page ads MSNホームページ広告

A critical question that many site owners face is how many ads to place.
多くのサイトオーナーが直面する重大な問題は、どれだけの広告を掲載するかということだ。
In the short-term, increasing the real-estate given to ads can increase revenue, but what will it do to the user experience, especially if these are non-targeted ads? The tradeoff between increased revenue and the degradation of the end-user experience is a tough one to assess, and that’s exactly the question that the MSN home page team at Microsoft faced in late 2007.
**短期的には、広告に割く面積を増やすことで収益を増やすことができるが、特にターゲット広告でない場合、ユーザー・エクスペリエンスにどのような影響を与えるだろうか？**収益の増加とエンドユーザ体験の低下とのトレードオフを評価するのは難しいもので、マイクロソフトのMSNホームページ・チームが2007年後半に直面したのは、まさにこの問題だった。

The MSN home page is built out of modules.
MSNのホームページはモジュールで構成されている。
The Shopping module is shown on the right side of the page above the fold.
ショッピング・モジュールは、ページの右側、折り目の上に表示されます。
The proposal was to add three offers right below it, as shown in Fig.5, which meant that these offers would show up below the fold for most users.
この提案は、図5に示すように、そのすぐ下に3つのオファー(i.e. 広告?)を追加するというもので、ほとんどのユーザーにとって、これらのオファーは折り目の下に表示されることになる。
The Display Ads marketing team estimated they could generate tens of thousands of dollars per day from these additional offers.
ディスプレイ広告のマーケティングチームは、これらの追加オファーから1日あたり数万ドルを生み出すことができると見積もっていた。

The interesting challenge here is how to compare the ad revenue with the “user experience.” In Sect.3.1, we refer to this problem as the OEC, or the Overall Evaluation Criterion.
ここでの興味深い課題は、**広告収入と "ユーザ体験 "をどのように比較するか**である。Sect.3.1では、この問題を**OEC(Overall Evaluation Criterion, 総合評価基準)**と呼ぶ。
In this case, we decided to see if page views and clicks decreased, and assign a monetary value to each.
この場合、ページビューとクリック数が減少したかどうかを確認し、それぞれに金銭的価値を割り当てることにした。
(No statistically significant change was seen in visit frequency for this experiment.) Page views of the MSN home page have an assigned value based on ads; clicks to destinations from the MSN home page were estimated in two ways: 1.
(この実験では、訪問頻度に統計的に有意な変化は見られなかった)。MSNホームページのページビューは、広告に基づいた値が割り当てられている。MSNホームページからの目的地へのクリックは、2つの方法で推定された：

1. Monetary value that the destination property assigned to a click from the MSN home page.
   MSNホームページからのクリックに対して、デスティネーション・プロパティが割り当てた金額。
   These destination properties are other sites in the MSN network.
   これらのデスティネーション・プロパティは、MSNネットワーク内の他のサイトである。
   Such a click generates a visit to an MSN property (e.g., MSN Autos or MSN Money), which results in multiple page views.
   このようなクリックは、MSNのプロパティ（MSN AutosやMSN Moneyなど）への訪問を生み、その結果、複数のページビューをもたらす。
2. The cost paid to search engines for a click that brings a user to an MSN property but not via the MSN home page (Search Engine Marketing).
   2.MSNのホームページを経由せずにMSNのプロパティにユーザーを誘導するクリックに対して検索エンジンに支払われる費用（検索エンジンマーケティング）。
   If the home page is driving less traffic to the properties, what is the cost of regenerating the “lost” traffic?
   トップページから物件へのトラフィックが減少している場合、「失われた」トラフィックを再生するためのコストはいくらか？

As expected, the number from #2 (SEM) was higher, as additional value beyond direct monetization is assigned to a click that may represent a new user, but the numbers were close enough to get agreement on the monetization value to use.
予想通り、#2（SEM）の数値の方が高かった。新規ユーザを表すクリックには、直接的な収益化以上の付加価値が割り当てられるためである。
A controlled experiment was run on 5% of the MSN US home page users for 12 days.
MSN USのホームページ利用者の5％を対象に、対照実験を12日間行った。
Clickthrough rate decreased by 0.38% (relative change), and the result was statistically significant (p-value = 0.02).
クリック率は0.38％減少し（相対変化）、その結果は統計的に有意であった（p値=0.02）。
Translating the lost clicks to their monetary value, it was higher than the expected ad revenue, so the idea of adding more ads to the MSN home page was scrapped.
**失われたクリック数を金額に換算すると、予想された広告収入よりも高かったため、MSNのホームページに広告を追加するというアイデアは破棄された。**

## 2.4. Behavior-Based Search at Amazon アマゾンの行動ベース検索

The examples above changed User-Interface (UI) elements.
上記の例では、ユーザインターフェース（UI）要素を変更した。
This example deals with a backend algorithmic change, which is often overlooked as an area to apply controlled experiments.
この例では、**バックエンドのアルゴリズム変更を扱っているが、これは対照実験を適用する領域として見過ごされがち**である。(今は全然見過ごされたりしてなさそう...!)

Back in 2004, when several of the authors were in the Data Mining and Personalization department at Amazon, there already existed a good algorithm for making recommendations based on two sets.
著者の何人かがアマゾンのデータマイニングとパーソナライゼーション部門にいた2004年当時、2つのセットに基づいて推薦を行う優れたアルゴリズムがすでに存在していた。
The signature feature for Amazon’s recommendation is “People who bought item X bought item Y,” but this was generalized to “People who viewed item X bought item Y” and “People who viewed item X viewed item Y.” A proposal was made to use the same algorithm for “People who searched for X bought item Y.”
アマゾンの推薦の特徴は、**「商品Xを購入した人は商品Yを購入した」**というものだが、これは「商品Xを見た人は商品Yを購入した」と「商品Xを見た人は商品Yを見た」というものに一般化された。同じアルゴリズムを「商品Xを検索した人は商品Yを購入した」というものに使用する提案がなされた。
We called it Behavior-Based Search (BBS).
これを行動ベース検索（BBS）と呼んだ。

In fact, the idea was to surface this in search results with no visible changes to the user interface.
実際、このアイデアは、ユーザインターフェイスに目に見える変更を加えることなく、検索結果に表示することだった。
If a user searched for a string that was common, and there was a strong signal that people who searched for that string bought one of several items, these items would surface at the top of the search results.
**ユーザが一般的な文字列を検索し、その文字列を検索した人々がいくつかのアイテムのいずれかを購入したという強いシグナルがあった場合、これらのアイテムは検索結果の上位に表示される**。
Note that this algorithm has no semantic understanding of the searched phrase, which was its strength and weakness.
**このアルゴリズムは、検索されたフレーズを意味的に理解していないことに注意**してほしい。(なるほど...!)

Proponents of the algorithm gave examples of underspecified searches, such as “24,” which most humans associated with the TV show starring Kiefer Sutherland.
アルゴリズムの支持者は、Kiefer Sutherland主演のテレビ番組と関連付けられる「24」といった不十分な指定の検索の例を挙げた。
Amazon’s search was returning poor results, shown in Fig.6, such as CDs with 24 Italian Songs, clothing for 24-month old toddlers, a 24-inch towel bar, etc.
アマゾンの検索は、図6に示すように、24のイタリアの歌を収録したCD、24ヶ月の幼児用の服、24インチのタオルバーなど、悪い結果を返していた。
(These results are still visible on Amazon today if you add an advanced search qualifier like “-foo” to the search phrase since this makes the search phrase unique and no mappings will exist from people who searched for it to products.)
（これらの結果は、検索フレーズに"-foo "のような高度な検索修飾子を加えると、今日でもアマゾンで見ることができる。これは、検索フレーズがユニークになり、**検索した人から商品へのマッピングが存在しなくなるから**である）
The BBS algorithm gave top-notch results with the DVDs of the show and with related books, i.e., things that people purchased after searching for “24” as shown in Fig.6.
BBSアルゴリズムは、図6に示すように、番組のDVDや関連書籍、つまり「24」を検索した後に購入されたもので、最高の結果を出した。
The weakness of the algorithm was that some items surfaced that did not contain the words in the search phrase.
アルゴリズムの弱点は、検索フレーズに含まれていない単語が含まれているアイテムが表示されることだった。
For example, if one searches for “Sony HD DVD Player” (this example is recent as of January 2008), Toshiba HD DVDs will show up fairly high.
例えば、「ソニーHD DVDプレーヤー」と検索すると（この例は2008年1月現在のものである）、東芝のHD DVDがかなり上位に表示される。
The reason is that Sony makes Blu-Ray DVD players, not HD players, and that many users who search for Sony HD DVD players end up purchasing a Toshiba player.
というのも、ソニーはHDプレーヤーではなくブルーレイDVDプレーヤーを製造しており、ソニーのHD DVDプレーヤーを探したユーザの多くが東芝のプレーヤーを購入してしまうからだ。(うんうんなるほど...!)
Given the pros and cons for the idea of Behavior-Based search, Amazon ran a controlled experiment.
**行動ベースの検索というアイデアに対する賛否両論**を踏まえ、アマゾンは対照実験を行った。

In a UW iEdge Seminar talk by Amazon in April 2006, it was disclosed that the feature increased Amazon’s revenue by 3%, which translates into several hundreds of millions of dollars.
2006年4月のアマゾンによるUW iEdgeセミナーでの講演では、この機能がアマゾンの収益を3％増加させ、それは数億ドルに相当すると明らかにされた。
(行動ベースの検索が負けて、treatmentのアルゴリズムが収益を増加させたってことかな)

<!-- ここまで読んだ! -->

# 3. Controlled experiments 対照実験

Enlightened trial and error outperforms the planning of flawless execution – David Kelly, founder of Ideo
完璧な実行計画を凌駕するためには、啓蒙された試行錯誤が必要である - デビッド・ケリー、アイデオの創設者
To have a great idea, have a lot of them – Thomas A.
偉大なアイデアを持つためには、たくさんのアイデアを持つことが必要である - トーマス・A・エジソン

![figure7]()

In the simplest controlled experiment, often referred to as an A/B test, users are randomly exposed to one of two variants: Control (A), or Treatment (B) as shown in Fig.7 (Mason et al.1989; Box et al.2005; Keppel et al.1992).
最も単純な対照実験では、A/Bテストと呼ばれることが多く、ユーザは図7に示すように、コントロール（A）またはトリートメント（B）の2つのバリアントのいずれかにランダムにさらされる（Mason et al.1989; Box et al.2005; Keppel et al.1992）。
The key here is “random.” Users cannot be distributed “any old which way” (Weiss 1997); no factor can influence the decision.
**ここで重要なのは "ランダム"である**。ユーザーを "どの方向にも "分布させることはできない（Weiss 1997）。
Based on observations collected, an Overall Evaluation Criterion (OEC) is derived for each variant (Roy 2001).
収集された観察結果に基づき、各バリアントについてOverall Evaluation Criterion(総合評価基準, OEC)が導き出される（Roy 2001）。
For example, in Checkout Example (Sect.2.1), the OEC can be the conversion rate, units purchased, revenue, profit, expected lifetime value, or some weighted combination of these.
例えば、チェックアウトの例（Sect.2.1）では、OECは、コンバージョン率、購入個数、収益、利益、期待生涯価値、または**これらの重み付けされた組み合わせ**とすることができる。(なるほど、複数のmetricsを結合した合成metricを用意するケースもあるのか...!)
Analysis is then done to determine if the difference in the OEC for the variants is statistically significant.
その後、各バリアントのOECの差が統計的に有意かどうかを判定するための分析が行われる。
If the experiment was designed and executed properly, the only thing consistently different between the two variants is the change between the Control and Treatment, so any differences in the OEC are inevitably the result of this assignment, establishing causality (Weiss 1997, p.215).
実験が適切に設計され、実行されていれば、2つのvariantの間で一貫して異なるのはコントロールとトリートメントの変更だけであるため、OECの違いは必然的にこの割り当ての結果であり、因果関係が確立される（Weiss 1997, p.215）。
There are several primers on running controlled experiments on the web (Peterson 2004, pp.76–78; Eisenberg and Eisenberg 2005, pp.283–286; Chatham et al.2004; Eisenberg 2005, 2004; Quarto-vonTivadar 2006; Miller 2007, 2006; Kaushik 2006; Peterson 2005, pp.248–253; Tyler and Ledford 2006, pp.213–219; Sterne 2002, pp.116–119).
ウェブ上で対照実験を行うための入門書がいくつかある（Peterson 2004, pp.76-78; Eisenberg and Eisenberg 2005, pp.283-286; Chatham et al.2004; Eisenberg 2005, 2004; Quarto-vonTivadar 2006; Miller 2007, 2006; Kaushik 2006; Peterson 2005, pp.248-253; Tyler and Ledford 2006, pp.213-219; Sterne 2002, pp.116-119）。

While the concept is easy to understand and basic ideas echo through many references, there are important lessons that we share here that are rarely discussed.
コンセプトは理解しやすく、基本的な考え方は多くの文献で紹介されているが、ここで紹介するのは、**あまり語られることのない重要な教訓**である。
These will help experimenters understand the applicability, limitations, and how to avoid mistakes that invalidate the results.
これらは、実験者が適用可能性、制限、および結果を無効にする間違いを避ける方法を理解するのに役立つだろう。

## 3.1. Terminology 用語

The terminology for controlled experiments varies widely in the literature.
対照実験の用語は、文献によって大きく異なる。
Below we define key terms used in this paper and note alternative terms that are commonly used.
以下では、本稿で使用する主要な用語を定義し、一般的に使用される代替用語を記す。

### Overall Evaluation Criterion (OEC) (Roy 2001).

総合評価基準（OEC）（Roy 2001）。

A quantitative measure of the experiment’s objective.
実験目的の定量的な指標。(=つまりprimary decision metric? もしくはprimary decision metricに加えてsecondary metricsやguardrail metricsも含めたもの?:thinking:)
In statistics this is often called the Response or Dependent Variable (Mason et al.1989;Box et al.2005); other synonyms includeOutcome,Evaluation metric, Performance metric, or Fitness Function (Quarto-vonTivadar 2006).
統計学では、これはしばしば応答または従属変数と呼ばれる（Mason et al.1989;Box et al.2005）; 他の類義語にはOutcome,Evaluation metric, Performance metric, or Fitness Function (Quarto-vonTivadar 2006)がある。
Experiments may have multiple objectives and a scorecard approach might be taken (Kaplan and Norton 1996), although selecting a single metric, possibly as a weighted combination of such objectives is highly desired and recommended (Roy 2001, p.50).
実験には複数の目的があり、スコアカードアプローチが取られるかもしれない（Kaplan and Norton 1996）が、単一の指標を選択すること、場合によってはそのような目的の重み付けされた組み合わせとして選択することは、非常に望ましく、推奨される（Roy 2001, p.50）。
A single metric forces tradeoffs to be made once for multiple experiments and aligns the organization behind a clear objective.
**単一の指標は、複数の実験に対してトレードオフを一度だけ行うことを強制し、明確な目的のために組織を一致させる**。
A good OEC should not be short-term focused (e.g., clicks); to the contrary, it should include factors that predict long-term goals, such as predicted lifetime value and repeat visits.
それどころか、予測される生涯価値やリピート訪問など、長期的なゴールを予測する要素を含むべきである。
Ulwick describes some ways to measure what customers want (although not specifically for the web) (Ulwick 2005).
ウルウィック氏は、（ウェブに特化したものではないが）顧客が何を求めているかを測定する方法をいくつか紹介している（Ulwick 2005）。

### Factor.

A controllable experimental variable that is thought to influence the OEC.
OECに影響を与えると考えられる制御可能な実験変数。(control or treatmentみたいな??)
Factors are assigned Values, sometimes called Levels or Versions.
ファクターには値が割り当てられ、levelsやversionsと呼ばれることもある。
(例えばpush通知のパーソナライスするか否かのABテストの場合、factor = is_personalized, value = true or false、みたいな?:thinking:)
Factors are sometimes called Variables.
因子は変数と呼ばれることもある。
In simple A/B tests, there is a single factor with two values: A and B.
**単純なA/Bテストでは、2つの値を持つ単一のfactorがある： AとBです**。

### Variant.

A user experience being tested by assigning levels to the factors; it is either the Control or one of the Treatments.
**factorにlevelを割り当てる**ことで、ユーザ体験がテストされる。
Sometimes referred to as Treatment, although we prefer to specifically differentiate between the Control, which is a special variant that designates the existing version being compared against and the new Treatments being tried.
トリートメント(reatment)と呼ばれることもあるが、特に比較対象となる既存のバージョンを指定する特別なvariantであるcontrolと、試される新しいtreatmentを明確に区別することを好む。
In case of a bug, for example, the experiment is aborted and all users should see the Control variant.
例えばバグがあった場合、実験は中止され、すべてのユーザがコントロールの variant を見ることになります。

### Experimental unit. 実験単位。

The entity over which metrics are calculated before averaging over the entire experiment for each variant.
**各variantの実験全体を平均化する前に、metricsが計算されるentity**。(?? 後述の例を読んだらよく理解できた...!) (異なる日付の同じユーザで、それぞれmetricを算出する場合は、experimental unitはuser-day)
Sometimes called an item.
アイテムと呼ばれることもある。
The units are assumed to be independent.
各ユニットは独立していると仮定する。
On the web, the user is a common experimental unit, although some metrics may have user-day, user-session or page views as the experimental units.
**ウェブ上では、ユーザが一般的な実験単位であるが、metricsによっては、user-day、user-session、page viewsを実験単位とするものもある**
For any of these randomization by user is preferred.
いずれの場合も、ユーザによるランダム化が望ましい。(実験単位がuser-sessionだったとしても、ランダム化はあくまでもユーザ単位のほうがいいってこと??:thinking:)
It is important that the user receive a consistent experience throughout the experiment, and this is commonly achieved through randomization based on user IDs stored in cookies.
**ユーザが実験を通して一貫した体験を受けることが重要**であり、これは一般的にクッキーに保存されたユーザーIDに基づくランダム化によって達成される。
We will assume that randomization is by user with some suggestions when randomization by user is not appropriate in Appendix.
付録では、ユーザーによる無作為化が適切でない場合にいくつかの提案を行うが、ここではユーザによる無作為化を仮定する。

### Null hypothesis. 帰無仮説。

The hypothesis, often referred to as H0, that the OECs for the variants are not different and that any observed differences during the experiment are due to random fluctuations.
しばしばH0と呼ばれる仮説は、variant間のOECは異なっておらず、実験中に観察された違いはランダムな揺らぎによるものであるというものである。

### Confidence level. 信頼度。

The probability of failing to reject (i.e., retaining) the null hypothesis when it is true.
帰無仮説が真である場合に、帰無仮説が棄却されない(保持される)確率。(つまり、1 - significance level...!:thinking:)

### Power

The probability of correctly rejecting the null hypothesis, H0, when it is false.
帰無仮説H0が偽である場合に、それを正しく棄却する確率。
Power measures our ability to detect a difference when it indeed exists.
検出力は、実際に差が存在する場合にそれを検出する能力を測るものである。

### A/A test.

Sometimes called a Null Test (Peterson 2004).
**Null Test**と呼ばれることもある（Peterson 2004）。
Instead of an A/B test, you exercise the experimentation system, assigning users to one of two groups, but expose them to exactly the same experience.
A/Bテストの代わりに、実験システムを行使し、ユーザを2つのグループのいずれかに割り当てるが、まったく同じ体験をさせる。
An A/A test can be used to (i) collect data and assess its variability for power calculations, and (ii) test the experimentation system (the Null hypothesis should be rejected about 5% of the time when a 95% confidence level is used).
A/A検定は、(i)データを収集し、検出力計算のためにその変動性(i.e. OEC metricの分散??)を評価するために使用することができ、(ii)実験システムをテストするために使用することができる（95%信頼度が使用される場合、帰無仮説は約5%の確率で棄却されるべきである）。

### Standard deviation (Std-Dev). 標準偏差（Std-Dev）。

A measure of variability, typically denoted by σ.
一般的にσで示される変動性の尺度。

### Standard error (Std-Err). 標準誤差（Std-Err）。

For a statistic, it is the standard deviation of the sampling distribution of the sample statistic (Mason et al.1989).
統計量の場合、標本統計量の標本分布の標準偏差である（Mason et al.1989）。
For a mean of n independent observations, it is σ /ˆ √n where σˆ is the estimated standard deviation.
n 個の独立したオブザベーションの平均では，$\frac{\hat{\sigma}}{\sqrt{n}}$ であり，$\hat{\sigma}$ は標準偏差の推定値である。

## 3.2. Hypothesis testing and sample size 仮説の検定とサンプルサイズ

To evaluate whether one of the treatments is different than the Control, a statistical test can be done.
コントロールと比較して、treatmentのODC metricが異なるかどうかを評価するために、統計的検定が行われる。
We accept a Treatment as being statistically significantly different if the test rejects the null hypothesis, which is that the OECs are not different.
検定が帰無仮説（OECは異ならない）を棄却した場合、統計的に有意差があるとして処遇を受け入れる。(うんうん)
We will not review the details of the statistical tests, as they are described very well in many statistical books (Mason et al.1989; Box et al.2005; Keppel et al.1992).
統計的検定の詳細については、多くの統計書（Mason et al.1989、Box et al.2005、Keppel et al.1992）に記載されているので、ここでは省略する。
What is important is to review the factors that impact the test:
重要なのは、テストに影響を与える要因を見直すことである：

- 1. Confidence level. 信頼度。
     Commonly set to 95%, this level implies that 5% of the time we will incorrectly conclude that there is a difference when there is none (Type I error).
     一般的に95%に設定されるこの水準は、差がないにもかかわらず差があると誤って結論づけることが5%あるということを意味する（タイプIエラー）。
     All else being equal, increasing this level reduces our power (below).
     他の条件が同じであれば、このレベルを上げるとパワーが落ちる（以下略）。
- 2. Power 検出力
     Commonly desired to be around 80–95%, although not directly controlled.
     直接コントロールはできないが、一般的には80～95％程度が望ましい。
     If the Null Hypothesis is false, i.e., there is a difference in the OECs, the power is the probability of determining that the difference is statistically significant.
     もし帰無仮説が偽であれば、つまりOECに差があれば、検出力とはその差が統計的に有意であると判断できる確率である。
     (A Type II error is one where we retain the Null Hypothesis when it is false.)
     (第二種の過誤とは、帰無仮説が偽であるにもかかわらず、帰無仮説を維持する過誤のことである)
- 3. Standard error. 標準誤差。
     The smaller the Std-Err, the more powerful the test.
     Std-Errが小さければ小さいほど、テストはより強力になる。

There are three useful ways to reduce the Std-Err: a.
Std-Errを減らすのに有効な方法が3つある：

- The estimated OEC is typically a mean of large samples.
  推定OECは通常、大きなサンプルの平均値である。
  As shown in Sect.3.1, the Std-Err of a mean is inversely proportional to the square root of the sample size, so increasing the sample size, which usually implies running the experiment longer, reduces the Std-Err and hence increases the power for most metrics.
  3.1節で示したように、平均値のStd-Errはサンプルサイズの平方根に反比例するので、サンプルサイズを大きくすることは、通常実験を長く行うことを意味し、Std-Errを減少させ、したがってほとんどの測定基準で検出力を増加させる。
  See the example in 3.2.1.
  3.2.1の例を参照のこと。 - b. Use OEC components that have inherently lower variability, i.e., the StdDev, σ, is smaller.
- **本質的にばらつきが小さい、すなわち標準偏差σが小さいOEC componentsを使用する**。(なるべく安定したmetricを選べってことかな:thinking:)
  For example, conversion probability (0–100%) typically has lower Std-Dev than number of purchase units (typically small integers), which in turn has a lower Std-Dev than revenue (real-valued).
  **例えば、コンバージョン確率（0-100％）は、通常、購入ユニット数（通常、小さな整数）よりもStd-Devが低く**、その結果、収益（実数値）よりもStd-errも小さくなる。(Std-ErrはStd-Devの推定値なので...!)
  See the example in 3.2.1.
  3.2.1の例を参照のこと。
- c. Lower the variability of the OEC by filtering out users who were not exposed to the variants, yet were still included in the OEC.
  **OECに含まれているが、variantにさらされていないユーザーを除外することで、OECのばらつきを減らす**。(これはTrigger分析的なことっぽい:thinking:)
  For example, if you make a change to the checkout page, analyze only users who got to the page, as everyone else adds noise, increasing the variability.
  例えば、チェックアウトページに変更を加えた場合、そのページにたどり着いたユーザだけを分析する。
  See the example in 3.2.3.
  3.2.3の例を参照のこと。

- 4. Effect.
     The difference in OECs for the variants, i.e.the mean of the Treatment minus the mean of the Control.
     すなわち、トリートメントの平均からコントロールの平均を引いたものである。(これはtrue effect sizeのことっぽい:thinking:)
     Larger differences are easier to detect, so great ideas will unlikely be missed.
     大きな差は発見しやすいので、素晴らしいアイデアが見逃される可能性は低い。
     Conversely, Type II errors are more likely when the effects are small.
     逆に、効果が小さいとtype IIエラーがより起こりやすい。

Two formulas are useful to share in this context.
この文脈では、2つの公式が役に立つ。
The first is the t-test, used in A/B tests (single factor hypothesis tests):
1つ目は、A/Bテスト(single factor hypothesis tests)で使われるt検定である:

$$
t = \frac{\bar{O_{B}} - \bar{O_{A}}}{\hat{\sigma_{d}}}
\tag{1}
$$

where OA and OB are the estimated OEC values (e.g., averages), σ*d is the estimated standard deviation of the difference between the two OECs, and t is the test result.
ここで、$\bar{O*{A}}$ と $\bar{O_{B}}$ は推定されたOECの値(例：平均値)、$\hat{\sigma_{d}}$ は2つのOECの差の推定標準偏差であり、tは検定結果である。
Based on the confidence level, a threshold t is established (e.g., 1.96 for large samples and 95% confidence) and if the absolute value of t is larger than the threshold, then we reject the Null Hypothesis, claiming the Treatment’s OEC is therefore statistically significantly different than the Control’s OEC.
信頼水準に基づき、閾値 t が設定され（たとえば、大きな標本と95%の信頼度では1.96）、tの絶対値がしきい値より大きければ、処理（Treatment）のOECはコントロール（Control）のOECより統計的に有意に異なると主張し、帰無仮説を棄却する。(ex. 閾値の例 = 標準正規分布における 1 - cdf(confidence level)の値とか...!:thinking:)
We assume throughout that the sample sizes are large enough that it is safe to assume the means have a Normal distribution by the Central Limit Theorem (Box et al.2005, p.29; Boos and Hughes-Oliver 2000) even though the population distributions may be quite skewed.
母集団の分布がかなり歪んでいても、中心極限定理（Box et al.2005, p.29; Boos and Hughes-Oliver 2000）により、平均値が正規分布に従うと仮定しても安全であるということを前提としている。
(サンプルサイズが十分に大きければ、標本平均の分布は正規分布に近づくという話か:thinking:)

A second formula is a calculation for the minimum sample size, assuming the desired confidence level is 95% and the desired power is 80% (van Belle 2002, p.31)
2番目の公式は、希望するconfidence levelが95%であり、希望するpowerが80%であると仮定した場合の**最小サンプルサイズの計算**である。(van Belle 2002, p.31)
(これって公式なのか??)

$$
n = \frac{16 \sigma^2}{\delta^2}
\tag{2}
$$

where n is the number of users in each variant and the variants are assumed to be of equal size, σ2 is the variance of the OEC, and is the sensitivity, or the amount of change you want to detect.
ここで、nは各variantのユーザ数であり、**各variantのユーザ数は同じ大きさであると仮定**されている。$\sigma^2$ はOECの分散であり、$\delta$ は 感度、または検出したい変化の量である。(=検出したい効果の大きさ...! = 想定してるcontrolとtreatmentそれぞれのOECの期待値の差)
(It is well known that one could improve the power of comparisons of the treatments to the control by making the sample size of the control larger than for the treatments when there is more than one treatment and you are only interested in the comparison of each treatment to the control.
If, however, a primary objective is to compare the treatments to each other then all groups should be of the same size as given by Formula 2.)
(1つ以上のtreatmentがある場合、そして各treatmentとcontrolの比較に興味がある場合、controlのサンプルサイズをtreatmentよりも大きくすることで、treatmentとcontrolの比較の検出力を向上させることができることはよく知られている。
しかし、もしtreatment同士を比較することが主な目的である場合、すべてのグループは式2で与えられるのと同じサイズでなければならない。)
(=これは3つ以上のvariantのテストの話:thinking:)
The coefficient of 16 in the formula provides 80% power, i.e., it has an 80% probability of rejecting the null hypothesis that there is no difference between the Treatment and Control if the true mean is different than the true Control by .
式の $16$ の係数は80%の検出力を提供し、つまり、(treatmentのOECの)真の平均が真のcontrolのものと(指定した効果量の条件で...!)異なる場合、treatmentとcontrolの間に差がないという帰無仮説を棄却する確率が80%である。
Even a rough estimate of standard deviation in Formula 2 can be helpful in planning an experiment.
式2で標準偏差を大まかに見積もるだけでも、実験計画の参考になる。
Replace the 16 by 21 in the formula above to increase the power to 90%.
上の式の16を21で置き換え、パワーを90%にする。
A more conservative formula for sample size (for 90% power) has been suggested (Wheeler 1974):
より保守的な(検出力90％の)サンプルサイズの公式が提案されている(Wheeler 1974):

$$
n = (4r \sigma / \delta)^2
\tag{3}
$$

where r is the number of variants (assumed to be approximately equal in size).
ここで $r$ はvariantの数であり（大体同じ大きさであると仮定されている）、
The formula is an approximation and intentionally conservative to account for multiple comparison issues when conducting an analysis of variance with multiple variants per factor (Wheeler 1975; van Belle 2002).
この式は近似値であり、**複数のvariantがある場合**の分散分析を行う際の多重比較問題を考慮して意図的に保守的になっている(Wheeler 1975; van Belle 2002)。
The examples below use the first formula.
以下の例では、最初の式を使用している。

<!-- ここまで読んだ -->

### 3.2.1. Example: impact of lower-variability OEC on the sample size 例 低変動性OECの標本サイズへの影響

Suppose you have an e-commerce site and 5% of users who visit during the experiment period end up purchasing.
Eコマースサイトがあり、実験期間中に訪問したユーザの5％が購入に至ったとする。
Those purchasing spend about $75.
購入する人は75ドルほど使う。
The average user therefore spends $3.75 (95% spend $0).
そのため、平均的な利用者は3.75ドル（95％は0ドルを使うので）を使う。
Assume the standard deviation is $30.
標準偏差を30ドルとする。(=OECの変動性、ばらつき度合い)(=これは実験期間中のデータを使って推定してるっぽい...!:thinking:)
If you are running an A/B test and want to detect a 5% change to revenue, you will need over 409,000 users to achieve the desired 80% power, based on the above formula: 16 ∗ 302/(3.75 ∗ 0.05)2.
A/Bテストを実施し、収益に対する5%の変化 (=treatmentにより期待する効果量...!) を検出したい場合、上記の式に基づき、望ましい80%の検出力を達成するためには、409,000人以上のユーザが必要となります： $16 \times \frac{30^2}{(3.75 \times 0.05)}^2$。

If, however, you were only looking for a 5% change in conversion rate (not revenue), a lower variability OEC based on point 3.b can be used.
しかし、もし、収益ではなく、**コンバージョン率 (=つまりbinary metric...!:thinking:) の5%の変化(=効果量)を検出したい場合**、3.bのポイントに基づいて、低変動性(=標準偏差の低い!)のOECを使用することができる。
Purchase, a conversion event, is modeled as a Bernoulli trial with p = 0.05 being the probability of a purchase.
**コンバージョンイベントである購入は、ベルヌーイ試行としてモデル化され、p = 0.05が購入の確率となる**。(うんうん...!)
The standard deviation of a Bernoulli is √p(1 − p) and thus you will need less than 122,000 users to achieve the desired power based on 16 ∗ (0.05 · (1 − 0.05))/(0.05 · 0.05)2.
ベルヌーイ試行の標準偏差は $\sqrt{p(1-p)}$ であり、したがって、 $16 \times \frac{0.05 \times (1-0.05)}{0.05 \times 0.05}^2$ に基づいて、望ましい検出力を達成するためには、122,000人以下のユーザが必要となります。

Using conversion as the OEC instead of purchasing spend can thus reduce the sample size required for the experiment by a factor of 3.3.
したがって、購入額ではなくコンバージョンをOECとして使用することで、実験に必要なサンプルサイズを 1/3.3 倍に減らすことができる。
Because the number of site visitors is approximately linear in the running time for the experiment (the number of distinct users is sublinear due to repeat visitors, but a linear approximation is reasonable for most sites), this can reduce the running time of the experiment from 6 weeks to 2 weeks, and thus is worth considering.
サイト訪問者数は実験の実行時間に対してほぼ線形であるため(繰り返し訪問者のため、ユニークユーザ数は亜線形であるが、ほとんどのサイトにとって線形近似は合理的である)、**これにより実験の実行時間を6週間から2週間に短縮することができ、したがって検討する価値がある**。
(要は毎日同じ数だけユーザが訪問すると仮定して...! あれ? この場合のサンプルサイズって、同一ユーザが異なる日に訪問したら2って考えていいのかな。実験単位はユーザだとして。)

<!-- ここまで読んだ! -->

### 3.2.2. Example: impact of reduced sensitivity on the sample size 例 感度(=検出したい効果量だっけ?)の低下がサンプルサイズに与える影響

Because the sensitivity, , is squared in the formula for sample size, if the desired sensitivity is reduced to support detecting a 20% change in conversion instead of 5% (a factor of 4), the number of users needed drops by a factor of 16 to 7,600.
サンプルサイズの公式では、感度(=検出したい、期待するeffect size) $\delta$ が2乗されているため、もし望ましい感度が5%ではなく20%(=4倍)のコンバージョンの変化を検出したいとなった場合、 必要なユーザ数は16分の1に減少し、7,600人になる。

As will be discussed later on, this is the reason that detecting a bug in the implementation can be done quickly.
後述するが、これが実装のバグを素早く検出できる理由である。(??実装のバグはマイナスのtrue effect sizeがめちゃでかいからってこと...??:thinking:)
Suppose you plan an experiment that will allow detecting a 1% change in the OEC, but a bug in the implementation exposes users to a bad experience and causes the OEC to drop by 20%.
OECの1％の変化を検出できるような実験を計画したが、実装にバグがあり、ユーザが悪い経験にさらされ、OECが20％低下したとする。
Such a bug can be detected not in 1/20th of the planned running time, but in 1/400th of the running time.
**このようなバグは、予定された走行時間の20分の1ではなく、400分の1で検出される可能性がある**。(sensitivityが20倍だから...!:thinking:)(ユーザ体験の悪化からの検出...!) (でもバグをいきなり全体適用してたら気づかないよな...!:thinking:)
If the experiment was planned to run for two weeks, you can detect an egregious problem in the first hour!
実験が2週間行われる予定だったとしたら、最初の1時間で重大な問題を発見することができる！

### 3.2.3. Example: filtering users not impacted by the change 例 変更の影響を受けないユーザのフィルタリング

(たぶんTriggered Analysisの話...!:thinking:)

If you made a change to the checkout process, you should only analyze users who started the checkout process (point 3.c), as others could not see any difference and therefore just add noise.
もしチェックアウトプロセスに変更を加えた場合、他のユーザは違いを見ることができないため、ノイズを加えるだけであるため、チェックアウトプロセスを開始したユーザのみを
Assume that 10% of users initiate checkout and that 50% of those users complete it.
10%のユーザがチェックアウトを開始し、そのうちの50%のユーザがチェックアウトを完了すると仮定します。
This user segment is more homogenous and hence the OEC has lower variability.
このユーザ層はより均質であるため、OECのばらつきは小さい。
Using the same numbers as before, the average conversion rate is 0.5, the std-dev is 0.5, and thus you will need only 6,400 users going through checkout to detect a 5% change based on 16 ∗ (0.5(1 − 0.5))/(0.5 · 0.05)2.
先ほどと同じ数字を使用すると、平均コンバージョン率は0.5、標準偏差は0.5(=こっちは平均コンバージョン率で決まる!)であるため、$16 \times \frac{0.5 \times (1-0.5)}{0.5 \times 0.05}^2$ に基づいて、5%の変化(改善)を検出するためには、チェックアウトを通過するユーザが6,400人しか必要ありません。
(**つまりTriggerを考慮したことで分散が小さくなって、必要なサンプルサイズが減ったってことか**...!:thinking:)
(たしかに $\Delta$ って、controlのOECの期待値 ×そのx%の改善って表記するとわかりやすいかも...!:thinking:)
(**あと分子で出てくる標準偏差は、controlの方の値で良いんだ...!:thinking:**)
Since we excluded the 90% who do not initiate, the total number of users to the website should be 64,000, which is almost half the previous result of 122,000, thus the experiment could run for half the time and yield the same power.
したがって、開始しない90％を除外したため、ウェブサイトへの合計ユーザ数は64,000人であり、これはほぼ前回の122,000人の半分であるため、実験を半分の時間で実行し、同じ検出力を得ることができる。

### 3.2.4. The choice of OEC must be made in advance OECの選択は事前に行わなければならない。

When running experiments, it is important to decide in advance on the OEC (a planned comparison); otherwise, there is an increased risk of finding what appear to be significant results by chance (familywise type I error) (Keppel et al.1992).
**実験を実施する際には、事前にOECを決定することが重要(計画された比較)であり、そうでないと偶然に有意な結果が得られるリスク(familywise type I error)が高まる**(Keppel et al.1992)。(複数のOECで何回も統計的仮説検定しちゃうと、多重検定になるから??)
Several adjustments have been proposed in the literature (e.g., Fisher’s least-significant-difference, Bonferroni adjustment, Duncan’s test, Scheffé’s test, Tukey’s test, and Dunnett’s test), but they basically equate to increasing the 95% confidence level and thus reducing the statistical power (Mason et al.1989; Box et al.2005; Keppel et al.1992).
いくつかの調整が文献で提案されている（例：フィッシャーの最小有意差、ボンフェローニ補正、ダンカンの検定、シェフェの検定、トゥーキーの検定、ダンネットの検定）が、基本的には95%信頼度を上げて統計的パワーを下げることに等しい(Mason et al.1989; Box et al.2005; Keppel et al.1992)。

## 3.3. Confidence intervals for absolute and percent effect 絶対効果およびパーセント効果の信頼区間

It is useful to give a confidence interval for the difference in the means of the Treatment and Control in addition to the results of the hypothesis test.
仮説検定の結果に加えて、treatmentとcontrolの平均値の差についての信頼区間を与えることは有用である。
The confidence interval gives a range of plausible values for the size of the effect of the Treatment whereas the hypothesis test only determines if there is a statistically significant difference in the mean.
信頼区間は、仮説検定が平均値に統計的に有意な差があるかどうかを決定するだけであるのに対して、treatmentの効果の大きさについてもっともらしい値の範囲を与える。

### 3.3.1. Confidence intervals for absolute effect 絶対効果の信頼区間

The formula for the confidence interval for the difference in two means is fairly straightforward.
2つの平均値の差の信頼区間の公式は非常に簡単である。
Using the notation developed previously, the upper and lower bounds for a 95% confidence interval are
先に開発した表記法を用いると、95%信頼区間の上界と下界は次のようになる。

$$
\text{CI Limits} = \bar{O_{B}} - \bar{O_{A}} \pm 1.96 \times \hat{\sigma_{d}}
\tag{4}
$$

One could use the confidence interval for the absolute affect to conduct a hypothesis test—if zero is in the interval you would not reject H0, otherwise reject H0 and conclude the Treatment has an effect.
absolute effect(=controlとtreatmentのOEC期待値の差)の信頼区間を使用して仮説検定を行うことができる。もし区間にゼロが含まれている場合、H0を棄却しない。それ以外の場合はH0を棄却し、Treatmentに効果があると結論づける。

### 3.3.2. Confidence intervals for percent effect 効果パーセントの信頼区間

For many online metrics, the difference in the means is so small that percent change has much more intuitive meaning than the absolute difference.
**多くのオンライン指標では、平均値の差は非常に小さいため、絶対的な差よりも変化率の方が直感的な意味を持つ**。(これがpercent effectっていうのね...!)
For example, for a recent experiment, the treatment effect for specific clickthrough rate was 0.00014.
例えば、最近の実験では、特定のクリック率に対するトリートメント効果は0.00014であった。(こっちはabsolute effect...!)
This translated to a 12.85% change due to the Treatment.
これはtreatmentによる12.85%の変化に相当する。(こっちはpercent effect...!)
The latter number was much more meaningful to decision makers.
**意思決定者にとっては、後者の数字の方がはるかに意味がある**。
The percent difference is calculated by
パーセンテージの差は次式で計算される。

$$
\text{Pct Diff} = \frac{\bar{O_{B}} - \bar{O_{A}}}{\bar{O_{A}}} \times 100 %
\tag{5}
$$

However, forming a confidence interval around the percent change is not a straightforward extension of the confidence interval for the absolute effect.
しかし、percent changeの信頼区間を形成することは、絶対効果の信頼区間の直感的な拡張ではない。(なるほど、じゃあ難しいんだ...! :thinking:)
This is because we are now dividing by a random variable.
**これは確率変数で割っているから**である。
The initial derivation of this interval is due to Fieller (Willan and Briggs 2006).
この区間の最初の導出はフィエラーによるものである（Willan and Briggs 2006）。
Note that if the denominator is stochastically close to zero one or both endpoints will not exist.
分母が確率的にゼロに近い場合、一方または両方の端点が存在しないことに注意。
In practice, you shouldn’t calculate this interval if the confidence interval for the denominator contains zero.
実際には、分母の信頼区間がゼロを含む場合は、この区間を計算すべきではありません。

<!-- ここは飛ばそう! まだ必要性がよくわからんから! -->

Define the coefficient of variation of the two groups to be
2つのグループの変動係数を次のように定義する。

$$
\tag{}
$$

The lower and upper bounds for a 95% confidence interval for the percent difference are
パーセント差の95％信頼区間の下限と上限は以下の通りである。

$$
\tag{}
$$

These formulas assume the covariance between the Treatment and Control mean is zero which will be true in a controlled experiment when the randomization is carried out properly
これらの公式は、治療平均とコントロール平均の間の共分散がゼロであることを仮定している。

<!-- ここまで読んだ! -->

## 3.4. Effect of robots on experimental results ロボットが実験結果に与える影響

Robots can introduce significant skew into estimates, enough to render assumptions invalid.
**ロボットは推定値に大きな歪みをもたらし、仮定を無効にしてしまう**ほどだ。(え、そうなの?? :thinking:) (自動でクリックするようなロボットのこと?? スクレイピングとかクローラーとかも含まれそう??)
We have seen cases where robots caused many metrics to be significant when they should not have been (e.g., much more than 5% false positives for an A/A test).
私たちは、**ロボットが多くのメトリクスを有意であるべきでないにもかかわらず有意にしてしまったケースを見たことがある**（例えば、A/Aテストで5％をはるかに超える偽陽性が出た）。
For the purpose of experimentation, it is especially important to remove some types of robots, those that interact with the user-id.
実験の目的上、特に重要なのは、ユーザIDと相互作用するタイプのロボットを取り除くことである。
For some websites robots are thought to provide up to half the pageviews on the site(Kohavi et al.2004).
サイトによっては、ページビューの半分をロボットが占めていることもある（Kohavi et al.2004）。
Since many robots have the same characteristics as human users it is difficult to clearly delineate between the two.
**多くのロボットが人間のユーザと同じような特性を持っているため、両者を明確に区別することは難しい**。
Benign or simple robots can often be filtered by basic characteristics (e.g.user agent, IP address) but many modern robots use sophisticated techniques to escape detections and filtering (Tan and Kumar 2002).
良性のロボットや単純なロボットは、基本的な特徴(ユーザーエージェントやIPアドレスなど)によってフィルタリングできることが多いが、最近のロボットの多くは、検出やフィルタリングを逃れるために高度なテクニックを使っている（Tan and Kumar 2002）。

<!-- ここまで読んだ! -->

<!-- ここは一旦飛ばす! -->

### 3.4.1. JavaScript versus server-side call JavaScript対サーバーサイド・コール

It is generally thought that very few robots will be included in the experiment if the treatment assignment is called by JavaScript so those experimental setups shouldn’t be affected as much by robots.
一般に、JavaScriptによって治療割り当てが呼び出される場合、実験に参加するロボットはほとんどいないと考えられているので、そのような実験設定はロボットの影響をあまり受けないはずである。
This should be validated by the experimenter.
これは実験者によって検証されるべきである。

### 3.4.2. Robots that reject cookies クッキーを拒否するロボット

We recommend excluding unidentified requests from the analysis, so that robots that reject cookies will not be part of the experimental results.
クッキーを拒否するロボットが実験結果の一部とならないように、未確認のリクエストを分析から除外することを推奨します。
If the treatment assignment and data collection is based only on users with a user ID stored in the user’s cookie, these robots will not be counted in the number of users or in the data that is collected on user behavior.
治療の割り当てやデータ収集が、ユーザーのクッキーに保存されたユーザーIDを持つユーザーのみに基づいて行われる場合、これらのロボットはユーザー数やユーザー行動に関する収集データにはカウントされません。

### 3.4.3. Robots that accept cookies クッキーを受け入れるロボット

If a robot accepts cookies and does not delete them, the effect can be profound, especially if the robot has a large number of actions on the site.
ロボットがクッキーを受け入れ、それを削除しない場合、特にそのロボットがサイト上で大量のアクションを起こした場合、その影響は甚大なものとなります。
We have found that there are usually a relatively small number of these robots but their presence in the Treatment or Control can seriously bias the comparison.
通常、こうしたロボットの数は比較的少ないが、トリートメントまたはコントロールに存在すると、比較に深刻な偏りが生じることがわかった。
For example, we have found some robots that have up to 7,000 clicks on a page in an hour or more than 3,000 page views in a day.
例えば、1時間に7,000回クリックされたり、1日に3,000回以上ページビューされるようなロボットも見つかっています。
Any hypothesis test comparing Treatment and Control when these robots are present can be very misleading.
このようなロボットが存在する場合、治療と対照を比較する仮説検定は非常に誤解を招く可能性がある。
These robots will not only bias the estimate of the effect, they also increase the standard deviation of many metrics, thus reducing the power.
これらのロボットは効果の推定に偏りを与えるだけでなく、多くの指標の標準偏差を増加させるため、検出力を低下させる。
Therefore, we need to aggressively filter out robots that do not delete cookies and have a large number of actions (e.g.pageviews or clickthroughs (triggered by onclick JavaScript handlers)) for a single user-id.
したがって、クッキーを削除せず、1つのユーザーIDに対して多数のアクション（例えば、ページビューやクリックスルー（onclick JavaScriptハンドラによってトリガーされる））を持つロボットを積極的にフィルタリングする必要があります。
Robots that either do not accept cookies or clear cookies after one or only a few actions will not have much of an effect on the comparison of Treatment to Control.
クッキーを受け入れないか、1回または数回のアクションの後にクッキーをクリアするロボットは、トリートメントとコントロールの比較にあまり影響を与えません。
Robot filtering can be accomplished through a combination of omitting users whose user agent is on a list of known robots and through the use of heuristics (Kohavi 2003).
ロボット・フィルタリングは、ユーザー・エージェントが既知のロボット・リストにあるユーザーを除外する方法と、ヒューリスティックを利用する方法を組み合わせることで実現できる（Kohavi 2003）。
The heuristics may vary depending on the website.
ヒューリスティックはウェブサイトによって異なる場合がある。

<!-- ここまで読んだ! -->

## 3.5. Extensions for online settings オンライン設定の拡張機能

Several extensions to basic controlled experiments are possible in an online setting (e.g., on the web).
基本的な対照実験に対するいくつかの拡張は、オンライン環境（例えばウェブ上）でも可能である。

### 3.5.1. Treatment ramp-up(立ち上げ)

An experiment can be initiated with a small percentage of users assigned to the Treatment(s), and then that percentage can be gradually increased.
**実験は、トリートメントに割り当てるユーザの割合を少なくして開始することができ、その後、その割合を徐々に増やしていくことができる**。(うんうん)
For example, if you plan to run an A/B test at 50%/50%, you might start with a 99.9%/0.1% split, then rampup the Treatment from 0.1% to 0.5% to 2.5% to 10% to 50%.
例えば、A/Bテストを50%/50%で実施する場合、99.9%/0.1%のスプリットから始め、0.1%→0.5%→2.5%→10%→50%とトリートメントをアップしていく。
At each step, which could run for, say, a couple of hours, you can analyze the data to make sure there are no egregious problems with the Treatment before exposing it to more users.
各ステップ（例えば2、3時間）でデータを分析し、処理に重大な問題がないことを確認してから、より多くのユーザに公開することができる。
The square factor in the power formula implies that such errors could be caught quickly on small populations and the experiment can be aborted before many users are exposed to the bad Treatment.
検出力の公式の2乗因子は、このようなエラーが小規模な集団で迅速に捉えられ、多くのユーザが悪いトリートメントにさらされる前に実験を中止することができることを意味している。(??)

### 3.5.2. Automation オートメーション

Once an organization has a clear OEC, it can run experiments to optimize certain areas amenable to automated search.
**一旦組織が明確なOECを持てば**、自動検索に適した特定の領域を最適化するための実験を行うことができる。
For example, the slots on the home page at Amazon are automatically optimized (Kohavi et al.2004).
例えば、アマゾンのホームページのスロットは自動的に最適化される（Kohavi et al.2004）。
If decisions have to be made quickly (e.g., headline optimizations for portal sites), these could be made with lower confidence levels because the cost of mistakes is lower.
迅速な意思決定が必要な場合（ポータルサイトのヘッドライン最適化など）、ミスのコストが低いため、より低い信頼性レベルで決定することができる。
Multi-armed bandit algorithms (Wikepedia 2008) and Hoeffding Races (Maron and Moore 1994) can be used for such optimizations.
このような最適化には、多腕バンディット・アルゴリズム（Wikepedia 2008）やHoeffding Races（Maron and Moore 1994）を用いることができる。

### 3.5.3. Software migrations ソフトウェアの移行

Experiments can be used to help with software migration.
実験はソフトウェアの移行に役立つ。
If a feature or a system is being migrated to a new backend, new database, or a new language, but is not expected to change user-visible features, an A/B test can be executed with the goal of retaining the Null Hypothesis, which is that the variants are not different.
ある機能やシステムが、新しいバックエンド、新しいデータベース、新しい言語に移行されるが、**ユーザーの目に見える機能は変更されないと予想される場合、A/Bテストは帰無仮説を維持することを目標に実行することができます**。
We have seen several such migrations, where the migration was declared complete, but an A/B test showed significant differences in key metrics, helping identify bugs in the port.
移行が完了したと宣言されたものの、A/Bテストでは主要な指標に大きな違いが見られ、ポートのバグを特定するのに役立った。
Because the goal here is to retain the Null Hypothesis, it is crucial to make sure the experiment has enough statistical power to actually reject the Null Hypothesis if it false.
ここでの目標は「帰無仮説」を維持することなので、実験が「帰無仮説」を棄却するのに十分な統計的検出力があることを確認することが重要である。
(OECがx%変動しちゃったらだめだよね、それを検出力80%で検出できる程度のサンプルサイズにしよう、みたいな?)

## 3.6. Limitations 制限事項

Despite significant advantages that controlled experiments provide in terms of causality, they do have limitations that need to be understood.
**対照実験には、因果関係という点で大きな利点があるにもかかわらず、理解されなければならない限界**がある。
Some, which are noted in the Psychology literature are not relevant to the web (Rossi et al.2003, pp.252–262; Weiss 1997), but some limitations we encountered are certainly worth noting.
心理学の文献で指摘されているものの中には、ウェブとは関係ないものもあるが（Rossi et al.2003, pp.252-262; Weiss 1997）、我々が遭遇したいくつかの限界は、確かに注目に値する。

### Quantitative metrics, but no explanations. 数値指標だけで説明はない。

It is possible to know which variant is better, and by how much, but not “why.” In user studies, for example, behavior is often augmented with users’ comments, and hence usability labs can be used to augment and complement controlled experiments (Nielsen 2005).
どのvariantがどれだけ良いかはわかるが、「なぜ」はわからない。例えば、ユーザースタディでは、**行動に加えてユーザのコメントがよく使われるため、ユーザビリティラボは対照実験を補完するために使うことができる**（Nielsen 2005）。(ユーザインタビューか!)

### Short term versus long term effects. 短期効果と長期効果。

Controlled experiments measure the effect on the OEC during the experimentation period, typically a few weeks.
対照実験では、実験期間中（通常は数週間）のOECへの影響を測定する。
While some authors have criticized that focusing on a metric implies short-term focus (Quarto-vonTivadar 2006; Nielsen 2005), we disagree.
指標を重視することは短期集中を意味すると批判する著者もいるが（Quarto-vonTivadar 2006; Nielsen 2005）、私たちはそうは思わない。
Long-term goalsshould be part of the OEC.
長期目標はOECの一部であるべきだ。(i.e. そもそもOECを選択する時点で、長期効果をなるべく考慮したmetricにすべき :thinking:)
Let us take search ads as an example.
検索広告を例にとってみよう。
If your OEC is revenue, you might plaster ads over a page, but we know that many ads hurt the user experience, so a good OEC should include a penalty term of usage of real-estate for ads that are not clicked, and/or should directly measure repeat visits and abandonment.
もし、あなたのOECが収益であれば、ページ上に広告を貼り付けるかもしれないが、多くの広告はユーザエクスペリエンスを損なうことを知っているので、**良いOECは、クリックされなかった広告のリアルエステートの使用量のペナルティ期間を含むべき**であり、そして/または、**リピート訪問と放棄を直接測定するべき**である。
Likewise, it is wise to look at delayed conversion metrics, where there is a lag from the time a user is exposed to something and take action.
同様に、ユーザが何かに触れてから行動を起こすまでにタイムラグがある、**遅延コンバージョンの指標を見ることも賢明**である。
These are sometimes called latent conversions (Miller 2006; Quarto-vonTivadar 2006).
これらは潜在的コンバージョンと呼ばれることもある（Miller 2006; Quarto-vonTivadar 2006）。
Coming up with good OECs is hard, but what is the alternative? The key point here is to recognize this limitation, but avoid throwing the baby out with the bathwater.
良いOECを考えるのは難しいが、その代わりに何があるだろうか？ここでの重要なポイントは、この限界を認識しつつも、風呂の水と一緒に赤ん坊を投げ出さないようにすることである。

### Primacy and newness effects. プライマシー効果と新しさ効果。

These are opposite effects that need to be recognized.
これらは相反する効果であり、認識する必要がある。
If you change the navigation on a web site, experienced users may be less efficient until they get used to the new navigation, thus giving an inherent advantage to the Control.
ウェブサイトのナビゲーションを変更すると、**経験豊富なユーザは新しいナビゲーションに慣れるまで効率が低下する可能性があり、そのためにコントロールに固有の利点が生じる**。(=これがprimacy effectか!:thinking:)
Conversely, when a new design or feature is introduced, some users will investigate it, click everywhere, and thus introduce a “newness” bias.
**逆に、新しいデザインや機能が導入されると、それを調べたり、あちこちをクリックしたりするユーザもいるので、「新しさ」バイアスがかかる**。(=これがnewness effectか!:thinking:)
This bias is sometimes associated with the Hawthorne effect (2007).
このバイアスは、ホーソン効果と関連付けられることがある（2007年）。
Both primacy and newness concerns imply that some experiments need to be run for multiple weeks.
プライマシーと新しさの両方の懸念は、**いくつかの実験を複数週にわたって実施する必要があること**を意味する。

One analysis that can be done is to compute the OEC only for new users on the different variants, since they are not affected by either factor.
行うことができる分析の1つは、**異なるvariantの新規ユーザに対してのみOECを計算することである。なぜなら、彼らはどちらの要因にも影響を受けないから**である。

### Features must be implemented. 機能は実装されなければならない。

A live controlled experiment needs to expose some users to a Treatment different than the current site (Control).
ライブの対照実験では、一部のユーザを現在のサイト（対照）とは異なる待遇にさらす必要がある。
The feature may be a prototype that is being tested against a small portion, or may not cover all edge cases (e.g., the experiment may intentionally exclude 20% of browser types that would require significant testing).
その機能はプロトタイプで、ごく一部に対してテストされている場合もあれば、すべてのエッジケースをカバーしていない場合もある（例えば、実験では重要なテストを必要とするブラウザの種類の20％を意図的に除外することがある）。
Nonetheless, the feature must be implemented and be of sufficient quality to expose users to it.
とはいえ、その機能は実装されなければならないし、ユーザにそれを見せるのに十分な品質でなければならない。
Nielsen (2005) correctly points out that paper prototyping can be used for qualitative feedback and quick refinements of designs in early stages.
Nielsen (2005)は、ペーパー・プロトタイピングが初期段階におけるデザインの質的フィードバックと迅速な改良のために使用できることを正しく指摘している。
We agree and recommend that such techniques complement controlled experiments.
我々はこれに同意し、このような手法が対照実験を補完することを推奨する。

### Consistency. 一貫性。

Users may notice they are getting a different variant than their friends and family.
ユーザは、友人や家族と異なるvariantが表示されていることに気づくかもしれません。
It is also possible that the same user will see multiple variants when using different computers (with different cookies).
また、同じユーザが異なるコンピューター（異なるクッキー）を使用している場合、複数のvariantが表示される可能性もあります。
It is relatively rare that users will notice the difference.
ユーザがその違いに気づくことは比較的稀である。

### Parallel experiments. 並行実験。

Our experience is that strong interactions are rare in practice (van Belle 2002), and we believe this concern is overrated.
我々の経験では、実際には強い相互作用は稀であり（van Belle 2002）、この懸念は過大評価されていると考えている。
Raising awareness of this concern is enough for experimenters to avoid tests that can interact.
この懸念に対する意識を高めるだけで、実験者は相互作用の可能性があるテストを避けることができる。
Pairwise statistical tests can also be done to flag such interactions automatically.
ペアワイズ統計検定を行うことで、このような相互作用を自動的に検出することもできる。

### Launch Events and Media Announcements. ローンチイベントとメディア発表。

If there is a big announcement made about a new feature, such that the feature is announced to the media, all users need to see it.
新機能についてメディアに発表するような大きな発表があった場合、すべてのユーザーがそれを見る必要がある。

<!-- ここまで読んだ! -->

# 4. MultiVariable Testing 多変量テスト

An experiment that includes more than one factor is often called a MultiVariable test (MVT) (Alt and Usborne 2005).
複数のfactorを含む実験は、**多変量テスト(MultiVariable test)（MVT）**と呼ばれることが多い（Alt and Usborne 2005）。
For example, consider testing five factors on the MSN homepage in a single experiment.
例えば、MSNのホームページで**5つのfactorを1回の実験でテストする**ことを考えてみよう。
A screenshot of the MSN homepage showing the control for each of these factors is given in Fig.8.
MSNのホームページのスクリーンショットを図8に示す。(画像を見た感じ、要は、1ユーザなどの実験単位に対して、複数の施策を同時に実験するってことか...!まさに複数のテスト間の相互作用の話...!)

![figure8]()

In a single test we can estimate the (main) effects of each factor as well as the interactive effects between factors.
1回の検定で、各factorの(主)効果だけでなく、factor間の相互作用効果も推定できる。
First, we will consider the benefits and limitations of MVT versus one-factor-at-a-time, or A/B tests.
まず、**MVTとone-factor-at-a-time(A/B)テストの利点と限界**を検討する。
Then we will discuss three approaches to online MVTs and how each approach takes advantage of the potential benefits and mitigates the limitations.
次に、**オンラインMVTの3つのアプローチ**と、それぞれのアプローチが潜在的な利点をどのように生かし、制限をどのように緩和するかについて説明する。
There are two primary benefits of a single MVT versus multiple sequential A/B tests to test the same factors: 1.
同じ要素をテストする複数の連続したA/Bテストに対して、単一の**MVTの主な利点**は2つある：

1. You can test many factors in a short period of time, accelerating improvement.
   短期間で多くの要素をテストすることができ、改善を加速させることができる。
   For example, if you wanted to test five changes to the website and you need to run each A/B test four weeks to achieve the power you need, it will take at least five months to complete the A/B tests.
   例えば、ウェブサイトを5回変更し、それぞれのA/Bテストを4週間実施し、必要なパワーを得ようとした場合、A/Bテストを完了するには少なくとも5ヶ月かかる。
   However, you could run a single MVT with all five factors in one month with the same power as with the five A/B tests.
   しかし、5つのA/Bテストと同じ検出力で、1ヶ月に5つの要因すべてを使って1つのMVTを実施することができる。

2. You can estimate interactions between factors. 2.要因間の相互作用を推定することができる。
   Two factors interact if their combined effect is different from the sum of the two individual effects.
   2つの要因が相互作用するのは、それらの複合効果が2つの個別効果の合計と異なる場合である。
   If the two factors work together to enhance the outcome the interaction is synergistic.
   この2つの要素が相乗効果を発揮して結果を向上させるのであれば、その相互作用は相乗的である。
   If instead they work against each other to dampen the effect, the interaction is antagonistic.
   その代わり、互いに作用しあって効果を減衰させるのであれば、その相互作用は拮抗的である。

Three common limitations are: 1.
一般的な**制限は3つ**ある：

1. **Some combinations of factors may give a poor user experience**.
   factorの組み合わせによっては、ユーザーエクスペリエンスが低下することもある。
   For example, two factors being tested for an online retailer may be enlarging a product image or providing additional product detail.
   例えば、あるオンライン小売業者がテストする2つの要素は、商品画像の拡大や商品詳細の追加提供かもしれない。
   Both may improve sales when tested individually, but when both are done at the same time the “buy box” is pushed below the fold and sales decrease.
   どちらも個別にテストすれば売上を向上させるかもしれないが、両方を同時に行うと「購入ボックス」がフォールドの下に押し込まれ、売上が減少する。
   This would be a large antagonistic interaction.
   これは大きな**antagonistic interaction(拮抗的相互作用)**となるだろう。
   This interaction should be caught in the planning phase so that these two factors would not be tested at the same time.
2. **Analysis and interpretation are more difficult**. 2.分析と解釈はより難しい。
   For a single factor test you typically have many metrics for the Treatment-Control comparison.
   単一因子のテストでは、通常、治療とコントロールの比較のために多くの測定基準があります。
   For an MVT you have the same metrics for many Treatment-Control comparisons (at least one for each factor being tested) plus the analysis and interpretation of the interactions between the factors.
   MVTでは、多くの治療とコントロールの比較のために同じ測定基準があります（少なくともテストされている各因子について1つ）プラス、因子間の相互作用の分析と解釈があります。
   Certainly, the information set is much richer but it can make the task of assessing which treatments to roll out more complex.
   確かに、情報セットははるかに豊かですが、**どの治療を展開するかを評価するタスクはより複雑になる**かもしれません。

3. It can take longer to begin the test.
   テストを開始するのに時間がかかる。
   If you have five factors you want to test and plan to test them one at a time you can start with any of those that are ready to be tested and test the others later.
   テストしたい要素が5つあり、それらを1つずつテストする計画であれば、テストの準備ができたものから始めて、他の要素は後でテストすることができる。
   With an MVT you must have all five ready for testing at the beginning of the test.
   MVTの場合、試験開始時に5つすべてを準備しておかなければならない。
   If any one is delayed, this would delay the start of the test.
   誰か一人でも遅れれば、テストの開始が遅れることになる。

We don’t believe any of the limitations are serious ones in most cases, but they should be recognized before conducting an MVT.
ほとんどの場合、どの制限も重大なものではないと考えるが、MVTを実施する前に認識しておくべきである。
Generally, we believe the first experiment one does should be an A/B test mainly due to the complexity of testing more than one factor in the same test.
**一般的に、最初に行う実験はA/Bテストであるべき**だと私たちは考えていますが、その主な理由は、同じテストで複数の要素をテストすることの複雑さにあります。
There are three overarching philosophies to conducting MVTs with online properties.
オンライン環境でMVTを実施するには、**3つの包括的な哲学**がある。

<!-- ここまで読んだ -->

## 4.1. Traditional MVT 伝統的MVT

This approach uses designs that are used in manufacturing and other offline applications.
このアプローチでは、製造業やその他のオフライン・アプリケーションで使用されている設計が使用される。
These designs are most often fractional factorial (Davies and Hay 1950) and Plackett and Burman (1946) designs that are specific subsets of full factorial designs (all combinations of factor levels).
これらのデザインは、最も頻繁に分数階乗（Davies and Hay 1950）やプラケット・バーマン（1946）のデザインであり、完全階乗デザイン（因子レベルのすべての組み合わせ）の特定の部分集合である。
These designs were popularized by Genichi Taguchi and are sometimes known as Taguchi designs.
これらの設計は田口玄一によって広められたもので、**タグチ・デザイン**として知られることもある。
The user must be careful to choose a design that will have sufficient resolution to estimate the main effects and interactions that are of interest.
ユーザは、興味のある主要な効果と相互作用を推定するのに十分な解像度を持つ設計を選ぶことに注意する必要がある。

For our MSN example we show designs for a test of these five factors with a full factorial, a fractional factorial or a Plackett-Burman design.
MSNの例では、これらの**5つのfactor**のテストのための完全階乗、分数階乗、プラケット・バーマン設計を示す。

Full factorial has all combinations of the factors which would be 25 = 32 user groups.
**Full factorial(完全階乗?)**では、すべてのfactorの組み合わせが2^5 = 32のユーザーグループになる。
A fractional factorial is a fraction of the full factorial that has 2K user groups and each column is orthogonal to the other four columns.
**fractional factorial(分数階乗)**は、完全階乗の一部で、2^Kのユーザグループがあり、各列が他の4つの列と直交している。
There are obviously many such fractions with 8 and 16 user groups.
このような分数は、8人、16人のユーザーグループによって多数存在する。
One fractional factorial for K = 3 is given in Table 1 where −1 denotes the control and 1 denotes the treatment.
K = 3に対する1つの分数階乗を表1に示し、-1がコントロール、1がトリートメントを表す。

![table1]()

Plackett–Burman designs can be constructed where the factors are all at two levels with the number of user groups being a multiple of 4, so 4, 8, 12, 16, 20, etc.
**Plackett–Burman designs(プラケット・バーマン計画)**は、factorがすべて2つのレベルで構成され、ユーザーグループの数が4の倍数であるため、4、8、12、16、20などが構成される。
The number of factors that can be tested for any of these designs is the number of user groups minus one.
これらのデザインでテストできる因子の数は、ユーザーグループの数から1を引いた数である。
If the number of user groups is a power of two the Plackett–Burman design is also a fractional factorial.
ユーザーグループの数が2のべき乗である場合、プラケット・バーマン計画も分数階乗となる。
As with the fractional factorials, there are usually many Plackett–Burman designs that could be used for a given number of user groups.
分数階乗と同様に、通常、与えられた数のユーザーグループに使用できる多くのプラケット・バーマン設計がある。
In the statistical field of Design of Experiments, a major research area is to find designs that minimize the number of user groups needed for the test while allowing you to estimate the main effects and interactions with little or no confounding.
実験計画法の統計分野では、主要な研究領域は、交絡がほとんどない状態で主効果と交互作用を推定できるようにしながら、検定に必要なユーザーグループの数を最小にする計画を見つけることである。
The fractional factorial in Table 1 can estimate all five main effects but cannot estimate interactions well (Box et al.2005, pp.235–305).
表1の分数階乗は、5つの主効果をすべて推定できるが、交互作用はうまく推定できない（Box et al.2005, pp.235-305）。
For many experimenters one of the primary reasons for running an MVT is to estimate the interactions among the factors being tested.
多くの実験者にとって、MVTを実施する主な理由の1つは、テストされる要因間の相互作用を推定することである。
You cannot estimate any interactions well with this design since all interactions are totally confounded with main effects or other two-factor interactions.
この計画では、すべての交互作用が主効果や他の2因子交互作用と完全に交絡してしまうので、交互作用をうまく推定することはできない。
No amount of effort at analysis or data mining will allow you to estimate these interactions individually.
どんなに分析やデータマイニングに取り組んでも、これらの相互作用を個別に推定することはできない。
If you want to estimate all two factor interactions with five factors you will need a fractional factorial design with 16 treatment combinations.
もし、5つの因子ですべての2因子交互作用を推定したい場合は、16の処理の組み合わせからなる分数要因計画が必要である。
The Placket–Burman design in Table 2 has all two factor interactions partially confounded with main effects and other two factor interactions.
表2のプラケット・バーマン計画では、すべての2因子交互作用が主効果や他の2因子交互作用と部分的に交絡している。
This makes the estimation of these two factor interactions challenging.
このため、これら2つの要因の相互作用の推定は困難である。
We recommend two alternatives that we believe are better than the traditional MVT approach for online tests.
私たちは、オンラインテストにおいて、従来のMVTアプローチよりも優れていると思われる2つの選択肢を推奨する。
The one you prefer will depend on how highly you value estimating interactions.
どちらを選ぶかは、相互作用の見積もりをどの程度重視するかによって変わってくる。

<!-- セクション4は、一旦飛ばそう...! 現時点でmulti variable testingについての理解が浅いので、次のセクションに進もう...! 必要性も高くない-->

## 4.2. MVT by running concurrent tests 同時実行テストによる MVT

Fractions of the full factorial are used in offline testing because there is usually a cost to using more treatment combinations even when the number of experimental units does not increase.
オフライン試験では、完全階乗の端数が使用される。これは、実験ユニットの数が増えなくても、通常、より多くの処理の組み合わせを使用するにはコストがかかるからである。
This does not have to be the case with tests conducted with web sites.
ウェブサイトを使ったテストでは、このようなことはない。
If we set up each factor to run as a one-factor experiment and run all these tests concurrently we can simplify our effort and get a full factorial in the end.
各要因を1要因実験として設定し、これらすべてのテストを同時に実行すれば、労力を簡略化し、最終的に完全な階乗を得ることができる。
In this mode we start and stop all these one-factor tests at the same time on the same set of users with users being independently randomly assigned to each experiment.
このモードでは、ユーザーを各実験に独立にランダムに割り当て、同じユーザーセットに対して、これらすべての1因子テストを同時に開始し、停止する。
The end result is you will have a full factorial experiment in all the factors you are testing.
最終的な結果は、あなたがテストしているすべての要因で完全な要因実験を行うことになる。
Of course, with a full factorial you will be able to estimate any interaction you want.
もちろん、完全階乗を使えば、どんな交互作用も推定することができる。
A side benefit of this approach is that you can turn off any factor at any time (for example if a treatment for a factor is disastrous) without affecting the other factors.
このアプローチの副次的な利点は、他のファクターに影響を与えることなく、いつでも（例えば、あるファクターの治療が悲惨なものであった場合など）ファクターをオフにできることである。
The experiment that includes the remaining factors is not affected.
残りの要素を含む実験は影響を受けない。
It is commonly thought that the power of the experiment decreases with the number of treatment combinations (cells).
一般的に、実験の検出力は治療の組み合わせ（セル）の数とともに低下すると考えられている。
This may be true if the analysis is conducted by comparing each individual cell to the Control cell.
これは、個々のセルをコントロール・セルと比較して分析する場合に当てはまる。
However, if the analysis is the more traditional one of calculating main effects and interactions using all the data for each effect, little or no power is lost.
しかし、各効果の全データを使って主効果と交互作用を計算するという、より伝統的な分析であれば、検出力はほとんど失われない。
(A very slight loss of power could occur if one of the factors of combination of factors increases the variation of the response.
(要因の組み合わせの1つが、レスポンスのばらつきを大きくする場合、ごくわずかなパワーロスが生じる可能性がある）。
Using a pooled estimate for experimental error will minimize any loss of power.) If your sample size (e.g.number of users) is fixed, it doesn’t matter if you are testing a single factor or many or whether you are conducting an eight run MVT or a full factorial the power to detect a difference for any main effect is the same (Box et al.2005).
実験誤差のプール推定値を使用することで、検出力の損失を最小限に抑えることができます)。標本サイズ（例：ユーザー数）が固定されている場合、単一因子を検定するのか多数因子を検定するのか、8回のMVTを実施するのか完全階乗を実施するのかは関係なく、どの主効果についても差を検出する検出力は同じです（Box et al.2005）。
There are two things that will decrease your power, though.
しかし、パワーを低下させるものが2つある。
One is increasing the number of levels (variants) for a factor.
一つは、因子のレベル（バリアント）の数を増やすことである。
This will effectively decrease the sample size for any comparison you want to make, whether the test is an MVT or an A/B test.
これは、テストがMVTであろうとA/Bテストであろうと、あなたが行いたい比較のサンプルサイズを効果的に減少させる。
The other is to assign less than 50% of the test population to the treatment (if there are two levels).
もう1つは、（2つの水準がある場合）試験集団の50％未満を治療に割り当てることである。
It is especially important for treatments in an MVT to have the same percentage of the population as the Control.
MVTにおける治療は、対照と同じ割合で行われることが特に重要である。

## 4.3. Overlapping experiments オーバーラップする実験

This approach is to simply test a factor as a one-factor experiment when the factor is ready to be tested with each test being independently randomized.
このアプローチは、因子をテストする準備ができたら、各テストを独立にランダム化して、単純に1因子実験として因子をテストすることである。
It is distinct from the previous Sect.
前セクトとは異なる。
(4.2) in that here each experiment turns on when the treatment is ready to go rather than launching all factors of a factorial design at once.
(4.2)では、各実験は、要因計画の全要因を一度に開始するのではなく、処理の準備ができた時点で開始される。
In an agile software development world, there are significant benefits to running more tests frequently, as they are ready to be deployed.
アジャイルソフトウェア開発の世界では、デプロイ準備が整った段階で、より多くのテストを頻繁に実行することに大きなメリットがある。
These tests can be going on simultaneously if there is no obvious user experience issue with the combinations that could be shown to any visitor.
どの訪問者にも表示される可能性のある組み合わせで、ユーザー・エクスペリエンスに明らかな問題がなければ、これらのテストは同時に行うことができる。
This is the approach you should take if you want to maximize the speed with which ideas are tested and you are not interested in or concerned with interactions.
これは、アイデアをテストするスピードを最大限に高めたい場合や、相互作用に興味や関心がない場合にとるべきアプローチである。
Large interactions between factors are actually rarer than most people believe, unless they are already known, such as with the buy box example.
要因の間に大きな相互作用があることは、ほとんどの人が思っている以上に稀である。
This is a much better alternative than the traditional approach mentioned first.
これは、最初に述べた伝統的な方法よりもはるかに良い選択肢である。
With the traditional approach you have the limitation that you can’t test until all the factors are ready to be tested.
従来のアプローチでは、すべての要素が揃うまでテストできないという制約があった。
In addition, when you’re done (with many test designs that are recommended) you won’t be able to estimate interactions well if at all.
加えて、（推奨される多くのテストデザインでは）終わった後、相互作用をうまく見積もることができない。
With overlapping experiments you test the factors more quickly and, if there is sufficient overlap in any two factors, you can estimate the interaction between those factors.
重複実験では、より迅速に因子をテストし、2つの因子に十分な重複があれば、それらの因子間の相互作用を推定することができる。
If you are especially interested in the interaction between two specific factors you can plan to test those factors at the same time.
2つの特定の要因間の相互作用に特に興味がある場合は、それらの要因を同時にテストする計画を立てることができる。
We believe the two alternatives presented above are better than the traditional MVT approach for online experiments.
我々は、上記の2つの選択肢は、オンライン実験のための従来のMVTアプローチよりも優れていると考えている。
The one you use would depend on your priorities.
どれを使うかは、あなたの優先順位によるだろう。
If you want to test ideas as quickly as possible and aren’t concerned about interactions, use the overlapping experiments approach.
できるだけ早くアイデアをテストしたい、相互作用を気にしないのであれば、重複実験アプローチを使う。
If it is important to estimate interactions run the experiments concurrently with users being independently randomized into each test effectively giving you a full factorial experiment.
交互作用の推定が重要な場合は、実験を同時並行で行い、ユーザーは各試験に独立して無作為に割り付けられ、効果的に完全要因実験を行うことができる。
