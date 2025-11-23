refs: https://multithreaded.stitchfix.com/blog/2019/03/11/FullStackDS-Generalists/

# Beware the data science pin factory: The power of the full-stack data science generalist and the perils of division of labor through function
# データサイエンスのピン工場に注意せよ：フルスタックデータサイエンスのゼネラリストの力と機能による労働分業の危険性

In The Wealth of Nations, Adam Smith demonstrates how the division of labor is the chief source of productivity gains using the vivid example of a pin factory assembly line: “One [person] draws out the wire, another straights it, a third cuts it, a fourth points it, a fifth grinds it.” 
『国富論』において、アダム・スミスは、**労働分業が生産性向上の主要な源であること**を、ピン工場の組立ラインの鮮やかな例を用いて示しています。「一人はワイヤーを引き出し、別の人はそれをまっすぐにし、三人目はそれを切り、四人目は先を尖らせ、五人目はそれを研磨します。」
With specialization oriented around function, each worker becomes highly skilled in a narrow task leading to process efficiencies. 
機能に基づく専門化により、各作業者は狭いタスクにおいて高度なスキルを持つようになり、プロセスの効率化が進みます。
Output per worker increases many fold; the factory becomes extremely efficient at producing pins. 
作業者一人あたりの生産量は何倍にも増加し、工場はピンの生産において非常に効率的になります。

This division of labor by function is so ingrained in us even today that we are quick to organize our teams accordingly. 
**この機能による労働分業は、今日でも私たちに深く根付いており、私たちはそれに応じてチームを迅速に編成します。**
Data science is no exception. 
データサイエンスも例外ではありません。
An end-to-end algorithmic business capability requires many data functions and companies usually create teams of specialists: research scientist, data engineers, machine learning engineers, causal inference scientists, and so on. 
エンドツーエンドのアルゴリズムビジネス機能は多くのデータ機能を必要とし、企業は通常、研究科学者、データエンジニア、機械学習エンジニア、因果推論科学者などの専門家チームを作成します。
Specialists’ work is coordinated by a product manager, with hand-offs between the functions in a manner resembling the pin factory: “one person sources the data, another models it, a third implements it, a fourth measures it” and on and on. 
専門家の作業はプロダクトマネージャーによって調整され、ピン工場に似た方法で機能間の引き継ぎが行われます。「一人はデータを調達し、別の人はそれをモデル化し、三人目はそれを実装し、四人目はそれを測定する」といった具合です。

Alas, we should not be optimizing our data science teams for productivity gains; that is what you do when you know what it is you’re producing—pins or otherwise—and are merely seeking incremental efficiencies. 
**残念ながら、私たちはデータサイエンスチームを生産性向上のために最適化すべきではありません。それは、生産するものが何であるか（ピンであれその他であれ）を知っていて、単に漸進的な効率を求めているときに行うことです。**
The goal of assembly lines is execution. 
**組立ラインの目標は実行(execution)**です。
We know exactly what we want—pins in Smith’s example, but one can think of any product or service in which the requirements fully describe all aspects of the product and its behavior. 
私たちは何を求めているのかを正確に知っています。スミスの例ではピンですが、要件が製品とその動作のすべての側面を完全に説明する任意の製品やサービスを考えることができます。
The role of the workers is then to execute on those requirements as efficiently as possible. 
したがって、作業者の役割は、その要件をできるだけ効率的に実行することです。

But the goal of data science is not to execute. 
しかし、データサイエンスの目標は実行することではありません。
Rather, the goal is to learn and develop profound new business capabilities. 
むしろ、目標は**学び、深い新しいビジネス能力を開発すること**です。
Algorithmic products and services like recommendation systems, client engagement bandits, style preference classification, size matching, fashion design systems, logistics optimizers, seasonal trend detection, and more can’t be designed up-front. 
推薦システム、クライアントエンゲージメントバンディット、スタイルの好みの分類、サイズマッチング、ファッションデザインシステム、ロジスティクス最適化、季節的トレンド検出などのアルゴリズム製品やサービスは、事前に設計することができません。
They need to be learned. 
それらは学ぶ必要があります。
There are no blueprints to follow; these are novel capabilities with inherent uncertainty. 
**従うべきblueprint(=設計図的なやつ?)はなく、これらは固有の不確実性を持つ新しい能力**です。
Coefficients, models, model types, hyper parameters, all the elements you’ll need must be learned through experimentation, trial and error, and iteration. 
**係数、モデル、モデルタイプ、ハイパーパラメータ、必要なすべての要素は、実験、試行錯誤、反復を通じて学ばれなければなりません。**
With pins, the learning and design are done up-front, before you produce them. 
ピンの場合、学びと設計は事前に行われ、生産する前に完了します。
With data science, you learn as you go, not before you go. 
**データサイエンスでは、出発する前ではなく、進むにつれて学びます。**

In the pin factory, when learning comes first we do not expect, nor do we want, the workers to improvise on any aspect of the product, except to produce it more efficiently. 
ピン工場では、学習が最初に来るとき、私たちは作業者が製品のあらゆる側面で即興することを期待せず、また望みません。ただし、より効率的に生産することを除いてです。
Organizing by function makes sense since task specialization leads to process efficiencies and production consistency (no variations in the end product). 
機能による組織化は、タスクの専門化がプロセスの効率化と生産の一貫性（最終製品の変動がない）につながるため、理にかなっています。

But when the product is still evolving and the goal is to learn, specialization hinders our goals in several ways: 
しかし、**プロダクトがまだ進化していて、目標が学ぶことである場合**、専門化は私たちの目標をいくつかの方法で妨げます：

1. **It increases coordination costs**. 調整コストが増加します。
Those are the costs that accrue in time spent communicating, discussing, justifying, and prioritizing the work to be done. 
それは、コミュニケーション、議論、正当化、優先順位付けに費やされる時間にかかるコストです。
These costs scale super-linearly with the number of people involved. 
これらのコストは、関与する人数に対して超線形にスケールします。
When data scientists are organized by function the many specialists needed at each step, and with each change, and each handoff, and so forth, make coordination costs high. 
データサイエンティストが機能によって組織されると、各ステップ、各変更、各引き継ぎに必要な多くの専門家が高い調整コストを生み出します。
For example, a data science specialist focused on statistical modeling will have to coordinate with a data engineer any time a dataset needs to be augmented in order to experiment with new features. 
例えば、統計モデリングに焦点を当てたデータサイエンスの専門家は、新しい機能を試すためにデータセットを拡張する必要があるたびに、データエンジニアと調整しなければなりません。

Similarly, any time new models are trained the research scientist will have to coordinate with a machine learning engineer to deploy them to production, etc. 
同様に、新しいモデルがトレーニングされるたびに、研究科学者はそれらを本番環境に展開するために機械学習エンジニアと調整しなければなりません。
These coordination costs act as a tax on iteration and can hamper learning. 
**これらの調整コストは反復に対する税金として機能し、学びを妨げる可能性があります。**

2. **It exacerbates wait-time.** 待機時間が悪化します。
Even more nefarious than coordinate costs is the time that elapses between work. 
調整コストよりもさらに厄介なのは、作業間に経過する時間です。
While coordination costs can typically be measured in hours—the time it takes to hold meetings, discussions, design reviews—wait-times are commonly measured in days or weeks or even months! 
調整コストは通常、会議、議論、設計レビューを行うのにかかる時間で時間単位で測定されますが、待機時間は通常、日、週、あるいは月単位で測定されます！
Schedules of functional specialists are difficult to align as each specialist is allocated to several initiatives. 
**機能専門家のスケジュールは、各専門家がいくつかのイニシアティブに割り当てられているため、調整が難しい**です。
A one-hour meeting to discuss changes may take weeks to line up. 
変更を議論するための1時間の会議を調整するのに数週間かかることがあります。
And, once aligned on the changes, the actual work itself also needs to be scheduled in the context of multiple other projects vying for specialists’ time. 
そして、一度変更に合意すると、実際の作業自体も専門家の時間を争う他の複数のプロジェクトの文脈でスケジュールされる必要があります。
Work like code changes or research that requires just a few hours or days to complete still may sit undone much longer before the resources are available. 
数時間または数日で完了するコード変更や研究の作業は、リソースが利用可能になるまで長い間未完のままである可能性があります。
Until then, iteration and learning languish. 
それまでの間、反復と学習は停滞します。

3. **It narrows context.** 文脈が狭まります。
Division of labor can artificially limit learning by rewarding people for staying in their lane. 
労働分業は、人々が自分の役割に留まることを奨励することで、学びを人工的に制限する可能性があります。
For example, the research scientist who is relegated to stay within her function will focus her energy towards experimenting with different types algorithms: gradient boosting, neural nets, random forest, and so on. 
例えば、彼女の機能に留まることを余儀なくされた研究科学者は、勾配ブースティング、ニューラルネット、ランダムフォレストなど、さまざまなタイプのアルゴリズムの実験にエネルギーを注ぎます。
To be sure, good algorithm choices could lead to incremental improvements. 
確かに、良いアルゴリズムの選択は漸進的な改善につながる可能性があります。
But there is usually far more to gain from other activities like integrating new data sources. 
しかし、**通常は新しいデータソースを統合するような他の活動から得られるものがはるかに多いです。**
Similarly, she may develop a model that exhausts every bit of explanatory power inherent to the data. 
同様に、彼女はデータに固有の説明力をすべて使い果たすモデルを開発するかもしれません。
Yet, her biggest opportunity may lie in changing the objective function or relaxing certain constraints. 
しかし、彼女の最大の機会は、目的関数を変更したり、特定の制約を緩和したりすることにあるかもしれません。
This is hard to see or do when her job function is limited. 
彼女の職務が制限されているとき、これは見たり行ったりするのが難しいです。
Since the research scientist is specialized in optimizing algorithms, she’s far less likely to pursue anything else, even when it carries outsized benefits. 
**研究科学者はアルゴリズムの最適化に特化しているため、たとえそれが大きな利益をもたらす場合でも、他の何かを追求する可能性ははるかに低くなります。**

Telling symptoms can surface when data science teams are run like pin factories, for example in simple status updates: “waiting on ETL changes” and “waiting on ML Eng resources” are common blockers. 
**データサイエンスチームがピン工場のように運営されると、例えば単純なステータス更新において、明らかな症状が現れます。「ETLの変更を待っています」と「MLエンジニアのリソースを待っています」は一般的な障害**です。
However, I believe the more insidious impact lies in what you don’t hear, because you can’t lament what you haven’t yet learned. 
しかし、私が考えるに、より陰湿な影響は、あなたが聞かないことにあります。なぜなら、あなたはまだ学んでいないことを嘆くことができないからです。
Perfect execution on requirements and complacency brought on by achieving process efficiencies can mask the difficult truth, that the organization is blissfully unaware of the valuable learnings they are missing out on. 
**要件の完璧な実行とプロセスの効率を達成することによってもたらされる自己満足**は、組織が見逃している貴重な学びに無自覚であるという厳しい真実を隠すことができます。

The solution to this problem is, of course, to get rid of the pin factory. 
この問題の解決策は、もちろん、ピン工場を排除することです。
In order to encourage learning and iteration, data science roles need to be made more general, with broad responsibilities agnostic to technical function. 
**学習と反復を促進するために、データサイエンスの役割はより一般的にし、技術的機能に依存しない広範な責任を持たせる必要があります**。
That is, organize the data scientists such that they are optimized to learn. 
つまり、データサイエンティストを学びに最適化されるように組織します。
This means hiring “full stack data scientists”—generalists—that can perform diverse functions: from conception to modeling to implementation to measurement. 
これは、「フルスタックデータサイエンティスト」、つまり多様な機能を実行できるゼネラリストを雇うことを意味します：概念からモデリング、実装、測定まで。
With fewer people to keep in the loop, coordination costs plummet. 
関与する人数が少なくなることで、調整コストは急落します。
The generalist moves fluidly between functions, extending the data pipeline to add more data, trying new features in the model, deploying new versions to production for causal measurement, and repeating the steps as quickly as new ideas come to her. 
**ゼネラリストは機能間を流動的に移動する。データパイプラインを拡張してデータを追加し、モデルに新しい特徴量を試し、因果測定のために新しいバージョンを本番環境に展開(オンラインテスト)し、新しいアイデアが彼女に浮かぶとすぐにそのステップを繰り返します**。
Of course, the generalist performs the different functions sequentially rather than in parallel—she is just one person after all. 
もちろん、ゼネラリストは異なる機能を並行してではなく、順次実行します。彼女は結局一人の人間ですから。
However, doing the work typically takes just a fraction of the wait-time it would take for another specialist resource to come available. 
**しかし、作業を行うのに通常は、他の専門家リソースが利用可能になるまでの待機時間のほんの一部で済みます。**
So, iteration time goes down. 
したがって、反復時間は短縮されます。

Our generalist may not be as adept as a specialist in any one function. 
**私たちのゼネラリストは、特定の機能において専門家ほど熟練していないかもしれません**。
But we are not seeking functional excellence or small incremental improvements. 
しかし、私たちは機能的な卓越性や小さな漸進的改善を求めているわけではありません。
Rather, we seek to learn and discover all-new business capabilities with step-change impact. 
むしろ、私たちは学び、段階的な影響を持つ全く新しいビジネス能力を発見することを求めています。
With full context for the holistic solution she sees opportunities that a narrow specialist won’t. 
**全体的な解決策の完全な文脈を持つことで、彼女は狭い専門家が見逃す機会を見出します。**
She has more ideas and tries more things. 
彼女はより多くのアイデアを持ち、より多くのことを試みます。
She fails more, too. 
彼女は失敗も多くなります。
However, the cost of failure is low and the benefits of learning are high. 
しかし、失敗のコストは低く、学びの利益は高いです。
This asymmetry favors rapid iteration and rewards learning. 
この非対称性は迅速な反復を促進し、学びに報います。

It is important to note that this amount of autonomy and diversity in skill granted to the full-stack data scientists depends greatly on the assumption of a solid data platform on which to work. 
**フルスタックデータサイエンティストに与えられるこの程度の自律性とスキルの多様性は、作業するための堅固なデータプラットフォームの前提に大きく依存していることに注意することが重要**です。
A well constructed data platform abstracts the data scientists from the complexities of containerization, distributed processing, automatic failover, and other advanced computer science concepts.
**適切に構築されたデータプラットフォーム**は、データサイエンティストをコンテナ化、分散処理、自動フェイルオーバー、その他の高度なコンピュータサイエンスの概念の複雑さから**抽象化**します。
In addition to abstraction, a robust data platform can provide seamless hooks into an experimentation infrastructure, automate monitoring and alerting, provide auto-scaling, and enable visualization of debugging output and algorithmic results. 
抽象化に加えて、堅牢なデータプラットフォームは、実験インフラストラクチャへのシームレスなフックを提供し、監視とアラートを自動化し、オートスケーリングを提供し、デバッグ出力とアルゴリズム結果の可視化を可能にします。
These components are designed and built by data platform engineers, but to be clear, there is not a hand-off from the data scientist to a data platform team. 
**これらのコンポーネントはデータプラットフォームエンジニアによって設計され構築**されますが、明確にするために、**データサイエンティストからデータプラットフォームチームへの引き継ぎはありません。**
It’s the data scientist that is responsible for all the code that is deployed to run on top of the platform. 
**プラットフォーム上で実行されるすべてのコードに責任を持つのはデータサイエンティスト**です。(なるほど...!:thinking:)
And, for the love of everything sacred and holy in the profession, don’t hand-off ETL for engineers to write. 
そして、職業におけるすべての神聖で聖なるもののために、エンジニアにETLを書くように引き継がないでください。
(データサイエンティストが自分でETLを書くべきであって、エンジニアに任せるな、ということっぽい。)

<!-- ここまで読んだ -->

I too was once lured to a function-based division of labor by the attraction of process efficiencies. 
**私もかつてはプロセスの効率性の魅力によって機能ベースの労働分業に引き寄せられました。**
(まあプロダクトのフェーズ次第でもあったりするのかな...! フルスタックデータサイエンティストが効果的に機能するのは、堅牢なMLプラットフォームがあることが前提条件だろうし...!:thinking:)
But, through trial and error (is there no better way to learn?) I’ve found that more generalized roles better facilitate learning and innovating, and provide the right kinds of scaling: to discover and build many more business capabilities than a specialist approach. 
しかし、試行錯誤を通じて（学ぶためのより良い方法はないのでしょうか？）、私はより一般的な役割が学習と革新を促進し、専門家アプローチよりも多くのビジネス能力を発見し構築するための適切なスケーリングを提供することを発見しました。
And, while there are some important considerations that may make this approach to organization more or less tenable in some companies (see footnote), I believe the full stack data scientist model provides a better starting place. 
そして、この組織へのアプローチが、**いくつかの企業でより実行可能または実行不可能にする重要な考慮事項がある一方で（脚注を参照）**、私はフルスタックデータサイエンティストモデルがより良い出発点を提供すると信じています。
Start with them, and then consciously (grudgingly) move toward a function-based division of labor only when clearly necessary. 
それらから始めて、**明確に必要な場合にのみ、意識的に（しぶしぶ）機能ベースの労働分業に移行**してください。

## Final thought. 最後の考え。

There is further downside to functional specialization. 
機能的専門化にはさらなる欠点があります。
It can lead to loss of accountability and passion from the workers. 
それは**作業者の責任感と情熱の喪失につながる可能性**があります。
Smith himself criticizes the division of labor, suggesting that it leads to the dulling of talent—that workers become ignorant and insular as their roles are confined to a few repetitive tasks. 
スミス自身は労働分業を批判し、それが才能の鈍化につながることを示唆しています。つまり、作業者は自分の役割がいくつかの反復的なタスクに制限されると無知で内向的になります。
While specialization may provide process efficiencies it is less likely to inspire workers. 
専門化はプロセスの効率を提供するかもしれませんが、作業者を鼓舞する可能性は低くなります。

By contrast, generalist roles provide all the things that drive job satisfaction: autonomy, mastery, and purpose. 
対照的に、ゼネラリストの役割は、仕事の満足度を高めるすべての要素を提供します：自律性、習熟度、目的です。
Autonomy in that they are not dependent on someone else for success. 
**自律性は、彼らが成功のために他の誰かに依存していないこと**です。
Mastery in that they know the business capability from end-to-end. 
**習熟度は、彼らがビジネス能力を端から端まで知っていること**です。
And, purpose in that they have a direct connection to the impact on the business they’re making. 
そして、目的は、彼らがビジネスに与える影響に直接的なつながりを持っていることです。
If we succeed in getting people to be passionate about their work and making a big impact on the company, then the rest falls into place naturally. 
もし私たちが人々に自分の仕事に情熱を持たせ、会社に大きな影響を与えることに成功すれば、残りは自然に整います。

<!-- ここまで読んだ -->

## Footnotes and References 脚注と参考文献

[1]↩I took the liberty of modernizing Smith’s use of pronouns.  
    [1]↩私はスミスの代名詞の使い方を現代化する自由を取った。

[2]↩As J. Richard Hackman taught us, the number of relationships (r) grows as a function number of members (n) per this equation: r = (n^2-n) / 2. And, each relationship bares some amount of coordination costs. See: Hackman, J. Richard. Leading teams: setting the stage for great performances. Boston, Mass.: Harvard Business School Press, 2002. Print.  
[2]↩J. リチャード・ハックマンが教えてくれたように、関係の数（r）はこの方程式に従ってメンバーの数（n）の関数として増加します：$r = \frac{n^2-n}{2}$。また、各関係には一定の調整コストが伴います。参照：ハックマン, J. リチャード. 『チームを導く：素晴らしいパフォーマンスのための舞台を整える』. ボストン, マサチューセッツ州：ハーバードビジネススクールプレス, 2002年。印刷。

[3]↩It’s important to note that I am not suggesting that hiring full-stack data scientists results in fewer people overall. Rather, I am merely suggesting that when organized differently, their incentives are better aligned with learning vs. efficiency gains. Consider the following contrasting deptarment/team structures, each with 3 people. Fractional estimates and summed team sizes are illustrative only.  
    [3]↩フルスタックデータサイエンティストを雇うことが全体的に人を減らす結果になるとは言っていないことに注意することが重要です。むしろ、異なる組織化を行うことで、彼らのインセンティブが学習と効率の向上の間でより良く調整されることを示唆しています。以下の対照的な部門/チーム構造を考えてみてください。それぞれ3人のメンバーがいます。部分的な推定値と合計チームサイズは、あくまで例示的なものです。  
    Specialist Model:organized for functional efficiency. Workers are not dedicated to any one business capability, rather their time is allocated to many.  
    専門家モデル：機能的効率のために組織化されています。労働者は特定のビジネス機能に専念するのではなく、彼らの時間は多くの機能に割り当てられます。  
    Generalists Model:Full-stack Data Scientists optimized for learning. Workers are fully dedicated to a business capability and perform all the functions.  
    一般化モデル：学習のために最適化されたフルスタックデータサイエンティスト。労働者はビジネス機能に完全に専念し、すべての機能を実行します。

[4]↩A more efficient way to learn about this approach to organization vs the trial and error I went through is to read the book by Amy C. Edmondson called “Teaming: How Organizations Learn, Innovate, and Compete in the Knowledge Economy” (Jossey-Bass, 2014).  
    [4]↩私が経験した試行錯誤に対するこの組織アプローチを学ぶより効率的な方法は、エイミー・C・エドモンドソンの著書『Teaming: How Organizations Learn, Innovate, and Compete in the Knowledge Economy』(ジョセイ・バス, 2014年)を読むことです。

[5]↩This process of iteration assumes low cost of trial and error. If the cost of error is high you may want to rethink (i.e., it is not advised for medical or manufacturing). In addition, data volume and system availability requirements should also be considered. If you are dealing with petabytes or exabytes of data, specialization in data engineering may be warranted. Similarly, system availability (ie. uptime) and innovation are tradeoffs. If availability is paramount, functional excellence may trump learning. Finally, the full-stack data science model relies on the assumption of great people. They are not unicorns; they can be found as well as made. But they are in high demand and it will require certain conditions in order to attract and retain them (competitive compensation, company values, interesting work, etc.). Be sure your company culture can support this.  
    [5]↩**この反復プロセスは、試行錯誤のコストが低いことを前提としています。**エラーのコストが高い場合は、再考することをお勧めします（つまり、医療や製造業には推奨されません）。さらに、データ量とシステムの可用性要件も考慮する必要があります。ペタバイトやエクサバイトのデータを扱う場合、データエンジニアリングの専門化が必要かもしれません。**同様に、システムの可用性（すなわち稼働時間）と革新はトレードオフです。可用性が最も重要であれば、機能的な優秀さが学習を上回る可能性があります**。最後に、フルスタックデータサイエンスモデルは優れた人材の存在を前提としています。彼らはユニコーンではなく、見つけることも作り出すこともできます。しかし、彼らは高い需要があり、彼らを引き付け、維持するためには特定の条件が必要です（競争力のある報酬、企業の価値観、興味深い仕事など）。あなたの会社の文化がこれをサポートできることを確認してください。

[6]↩Smith, Adam. An inquiry into the nature and causes of the wealth of nations. Dublin: Printed for Messrs. Whitestone, 1776. Print. Page 464.  
    [6]↩スミス, アダム. 『国富論』. ダブリン：ウィットストーン社のために印刷, 1776年。印刷。ページ464。

[7]↩Pink, Daniel H.. Drive: the surprising truth about what motivates us. New York, NY: Riverhead Books, 2009.  
    [7]↩ピンク, ダニエル・H. 『Drive: 私たちを動機づける驚くべき真実』. ニューヨーク, NY：リバーヘッドブックス, 2009年。

<!-- ここまで読んだ -->
