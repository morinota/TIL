## refs: refs：

- https://continuousdelivery.com/principles/ https://continuousdelivery.com/principles/

# Principles プリンシプル

There are five principles at the heart of continuous delivery:
継続的デリバリーの中心には**5つの原則**がある：

- Build quality in (品質を組み込む)
- Work in small batches (小さいロットで作業する)
- Computers perform repetitive tasks, people solve problems (コンピュータは反復タスクをこなし、人は問題を解決する)
- Relentlessly pursue continuous improvement (絶え間ない改善を追求する)
- Everyone is responsible (みんなに責任がある)

It’s easy to get bogged down in the details of implementing continuous delivery—tools, architecture, practices, politics—if you find yourself lost, try revisiting these principles and you may find it helps you refocus on what’s important.
ツール、アーキテクチャ、プラクティス、政治など、継続的デリバリーを実施するための細部にとらわれがちだが、もし迷いが生じたら、これらの原則を再確認してみてほしい。

## 原則1: Build quality in

Edwards Deming, a key figure in the history of the Lean movement, offered 14 key principles for management.
リーン運動の歴史における重要人物であるエドワーズ・デミングは、**マネジメントのための14の主要原則**を提示した。
Principle three states, “Cease dependence on inspection to achieve quality. Eliminate the need for inspection on a mass basis by building quality into the product in the first place.”
第3原則は、「**品質を達成するために検査に依存するのをやめよ。最初から製品に品質を組み込むことによって、大量の検査を必要としないようにする**」と述べている。(プロダクトに品質保証の振る舞いを組み込む、みたいな...??:thinking:)

It’s much cheaper to fix problems and defects if we find them immediately—ideally before they are ever checked into version control, by running automated tests locally.
ローカルで自動テストを実行することで、問題や欠陥をすぐに見つけることができれば、それを修正するコストははるかに安くつく。
Finding defects downstream through inspection (such as manual testing) is time-consuming, requiring significant triage.
検査(手動テストなど)を通じて下流で欠陥を見つけることは、時間がかかり、大規模なトリアージが必要となる。(トリアージ = 整理すること??)
When we find a defect in production, we must first find the defect in our version control system.
本番環境で欠陥を見つける場合、まずバージョン管理システムで欠陥を見つけなければならない。(あ、これは欠陥の原因となったPRやcommitを見つけるってことか...!:thinking:)
Then we must fix the defect, trying to recall what we were thinking when we introduced the problem days or perhaps even weeks ago.
そして、数日前、あるいは数週間前に問題を起こしたときに考えていたことを思い出しながら、不具合を修正しなければならない。

Creating and evolving feedback loops to detect problems as early as possible is essential and never-ending work in continuous delivery.
**問題を可能な限り早期に発見するためのフィードバック・ループを作り、進化させることは、継続的デリバリーにおいて不可欠であり、終わりのない作業である**。(うんうん、高速なfeedback loopの仕組みは、CDのイメージがある...!:thinking:)
If we find a problem in our exploratory testing, we must not only fix it, but then ask: How could we have caught the problem with an automated acceptance test? When an acceptance test fails, we should ask: Could we have written a unit test to catch this problem?
探索的テスト(=開発者による不具合発生後のテスト??)で問題を見つけた場合、それを修正するだけでなく、次に尋ねる必要がある：**自動受け入れテストでその問題を検出することができたのか？ 受け入れテストが失敗した場合、この問題をキャッチするためにユニットテストを書くことができたか?** (質問の答えがYesなのであれば、次回以降はその問題を自動テストで検知できるようにしていく...!:thinking:)

## Work in Small Batches ♪小ロットで仕事をする

In traditional phased approaches to software development, handoffs from dev to test or test to IT operations consist of whole releases: months worth of work by teams consisting of tens or hundreds of people.
従来の段階的なソフトウェア開発アプローチでは、開発からテスト、またはテストからIT運用へのハンドオフは、リリース全体で構成される： 数十人から数百人からなるチームによる、数カ月分の作業だ。

In continuous delivery, we take the opposite approach, and try and get every change in version control as far towards release as we can, getting comprehensive feedback as rapidly as possible.
継続的デリバリーでは、逆のアプローチを取る。**可能な限りすべての変更をバージョン管理に取り込み、できるだけ迅速に包括的なフィードバックを得ることを目指す**。

Working in small batches has many benefits.
小ロットでの作業には多くの利点がある。
It reduces the time it takes to get feedback on our work, makes it easier to triage and remediate problems, increases efficiency and motivation, and prevents us from succumbing to the sunk cost fallacy.
**仕事にフィードバックを得る時間を短縮**し、問題のトリアージと解決を容易にし(なるほど...!このPRが原因だってすぐに分かる!)、効率とモチベーションを高め(確かに! PR mergeできると嬉しい)、沈没コストの誘惑から守る。(柔軟に方向転換できる、みたいな??:thinking:)

The reason we work in large batches is because of the large fixed cost of handing off changes.
私たちが大ロットで仕事をするのは、変更を引き渡すための固定費が大きいからだ。
A key goal of continuous delivery is to change the economics of the software delivery process to make it economically viable to work in small batches so we can obtain the many benefits of this approach.
**継続的デリバリーの主要な目標のひとつは、ソフトウェアデリバリープロセスの経済を変え、小ロットでの作業が経済的に可能になるようにすることで、このアプローチの多くの利点を得ることである。**

<!-- ここまで読んだ! -->

## Computers Perform Repetitive Tasks, People Solve Problems ♪コンピュータは反復タスクをこなし、人は問題を解決する

One of the earliest philosophical ideas of the Toyota tradition is jidoka, sometimes translated as “automation with a human touch.” The goal is for computers to perform simple, repetitive tasks, such as regression testing, so that humans can focus on problem-solving.
トヨタ伝統の最も古い哲学的思想のひとつに「自動化（jidoka）」がある。その目的は、**リグレッション・テストのような単純で反復的な作業をコンピューターに行わせ、人間が問題解決に集中できるようにすること**である。
Thus computers and people complement each other.
このように、**コンピューターと人間は互いに補完し合っている**。

Many people worry that automation will put them out of a job.
オートメーション化によって仕事がなくなるのではないかと心配する人は多い。
This is not the goal.
これはゴールではない。
There will never be a shortage of work in a successful company.
成功している会社で仕事が不足することはない。
Rather, people are freed up from mindless drudge-work to focus on higher value activities.
むしろ、人々は頭を使わない雑務から解放され、より価値の高い活動に集中することができる。
This also has the benefit of improving quality, since humans are at their most error-prone when performing mindless tasks.
人間は頭を使わない作業をするときに最もミスを犯しやすいからだ。

## Relentlessly Pursue Continuous Improvement ♪ 絶え間ない改善を追求する

Continuous improvement, or kaizen in Japanese, is another key idea from the Lean movement.
継続的改善、日本語ではカイゼンもリーン運動の重要な考え方である。
Taiichi Ohno, a key figure in the history of the Toyota company, once said,
トヨタ自動車の歴史における重要人物、大野耐一はかつてこう言った、

Kaizen opportunitites are infinite.
カイゼンの機会は無限にある。
Don’t think you have made things better than before and be at ease… This would be like the student who becomes proud because they bested their master two times out of three in fencing.
**以前よりも良くなったと思って安心してはいけない**...これは、剣術で3回中2回師匠に勝ったという生徒が誇りに思うのと同じだ。(心にしみる...!:thinking:)
Once you pick up the sprouts of kaizen ideas, it is important to have the attitude in our daily work that just underneath one kaizen idea is yet another one.
カイゼンアイデアの芽を摘むと、日常の仕事の中で、**1つのカイゼンアイデアのすぐ下にもう1つのカイゼンアイデアがある**という態度を持つことが重要である。

Don’t treat transformation as a project to be embarked on and then completed so we can return to business as usual.
変革を取り組むべきプロジェクトとして扱い、**それを完了して日常業務に戻るべきではない**。(ほうほう...!:thinking:)
The best organizations are those where everybody treats improvement work as an essential part of their daily work, and where nobody is satisfied with the status quo.
**最良の組織とは、全員が改善活動を日常業務の不可欠な一部として扱い、誰も現状に満足しない組織**である。

<!-- ここまで読んだ! -->

## Everyone is Responsible ♪みんなに責任がある

In high performing organizations, nothing is “somebody else’s problem.” Developers are responsible for the quality and stability of the software they build.
**高い業績を上げている組織では、"誰か他の人の問題"は存在しない。開発者は、自分たちが構築したソフトウェアの品質と安定性に責任を持つ**。
Operations teams are responsible for helping developers build quality in.
オペレーション・チームは、開発者の品質構築を支援する責任がある。
Everyone works together to achieve the organizational level goals, rather than optimizing for what’s best for their team or department.
自分のチームや部署に最適なものを最適化するのではなく、**組織全体の目標を達成するためにみんなで協力する**。(うーん、これはABテストで最適化すべきmetricsについても言えることだよなぁ...:thinking:)

When people make local optimizations that reduce the overall performance of the organization, it’s often due to systemic problems such as poor management systems such as annual budgeting cycles, or incentives that reward the wrong behaviors.
人々が局所的な最適化を行うことで組織全体のパフォーマンスが低下する場合、それはしばしば、年次予算サイクルなどの管理システムの問題や、間違った行動を報酬とするインセンティブなどのシステム的な問題が原因である。
A classic example is rewarding developers for increasing their velocity or writing more code, and rewarding testers based on the number of bugs they find.
典型的な例は、開発者に対して速度を上げることやコードを書くことを報酬とし、テスターには見つけたバグの数に基づいて報酬を与えることである。(これはよく例で挙げられてるやつ! :thinking:)

Most people want to do the right thing, but they will adapt their behaviour based on how they are rewarded.
たいていの人は正しいことをしたいと思っているが、報酬に基づいて行動を適応させるだろう。
Therefore, it is very important to create fast feedback loops from the things that really matter: how customers react to what we build for them, and the impact on our organization.
従って、顧客が私たちが彼らのために構築したものにどのように反応し、組織に与える影響など、**本当に重要なことから迅速なフィードバック・ループを作ることが非常に重要**である。(何かしらのアクションを評価するためのmetricsの決め方大事だよね...!:thinking:)

<!-- ここまで読んだ! -->
