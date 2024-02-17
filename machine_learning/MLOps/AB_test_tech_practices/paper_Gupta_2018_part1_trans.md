## 0.1. link 0.1.リンク

https://www.researchgate.net/publication/333136404_Top_Challenges_from_the_first_Practical_Online_Controlled_Experiments_Summit
https://www.researchgate.net/publication/333136404_Top_Challenges_from_the_first_Practical_Online_Controlled_Experiments_Summit

## 0.2. title # 0.2.title

Top Challenges from the first Practical Online Controlled Experiments Summit
第1回実践的オンライン対照実験サミットのトップチャレンジ

## 0.3. abstract # 0.3.abstract

**Online controlled experiments (OCEs), also known as A/B tests**, have become ubiquitous in evaluating the impact of changes made to software products and services.
A/Bテストとしても知られるオンライン対照実験（OCE）は、ソフトウェア製品やサービスに加えられた変更の影響を評価する上で、どこにでもあるようになった。
While the concept of online controlled experiments is simple, there are many practical challenges in running OCEs at scale and encourage further academic and industrial exploration.
オンライン制御実験のコンセプトは単純だが、OCEを大規模に実行するには多くの現実的な課題があり、学術的・産業的な探求がさらに進むことが望まれる。
To understand the top practical challenges in running OCEs at scale, representatives with experience in large-scale experimentation from thirteen different organizations (Airbnb, Amazon, Booking.com, Facebook, Google, LinkedIn, Lyft, Microsoft, Netflix, Twitter, Uber, Yandex, and Stanford University) were invited to the first Practical Online Controlled Experiments Summit.
OCEを大規模に実行する上での実践的な最重要課題を理解するため、1**3の異なる組織(Airbnb、Amazon、Booking.com、Facebook、Google、LinkedIn、Lyft、Microsoft、Netflix、Twitter、Uber、Yandex、Stanford University)から大規模実験の経験を持つ代表者を招き、第1回実践的オンライン対照実験サミットを開催**した。
All thirteen organizations sent representatives.
全13団体が代表を派遣した。
Together these organizations tested more than one hundred thousand experiment treatments last year.
これらの組織は昨年、合わせて10万件以上の実験治療をテストした。
Thirty-four experts from these organizations participated in the summit in Sunnyvale, CA, USA on December 13-14, 2018.
2018年12月13日から14日にかけて米国カリフォルニア州サニーベールで開催されたサミットには、これらの組織から34人の専門家が参加した。
While there are papers from individual organizations on some of the challenges and pitfalls in running OCEs at scale, this is the first paper to provide the top challenges faced across the industry for running OCEs at scale and some common solutions.
OCEを大規模に運営する上での課題や落とし穴については、各組織から論文が出ているが、**OCEを大規模に運営する上で業界全体が直面する最重要課題と共通の解決策を示した論文**はこれが初めてである。

# 1. Introduction 1. はじめに

The Internet provides developers of connected software, including web sites, applications, and devices, an unprecedented opportunity to accelerate innovation by evaluating ideas quickly and accurately using OCEs.
インターネットは、ウェブサイト、アプリケーション、デバイスなど、接続されたソフトウェアの開発者に、OCEを使用してアイデアを迅速かつ正確に評価することにより、イノベーションを加速させる前例のない機会を提供する。
At companies that run OCEs at scale, the tests have very low marginal cost and can run with thousands to millions of users.
OCEを大規模に実行する企業では、テストの余剰コストは非常に低く、数千から数百万人のユーザで実行できる。
As a result, OCEs are quite ubiquitous in the technology industry.
その結果、OCEはテクノロジー業界のいたるところで見られるようになった。
From front-end user-interface changes to backend algorithms, from search engines (e.g., Google, Bing, Yandex) to retailers (e.g., Amazon, eBay, Etsy) to media service providers (e.g.Netflix, Amazon) to social networking services (e.g., Facebook, LinkedIn, Twitter) to travel services (e.g., Lyft, Uber, Airbnb, Booking.com), OCEs now help make data-driven decisions [7, 10, 12, 27, 30, 40, 41, 44, 51, 58, 61, 76].
フロントエンドのユーザーインターフェイスの変更からバックエンドのアルゴリズムまで、検索エンジン（例：Google、Bing、Yandex）から小売業者（例：Amazon、eBay、Etsy）まで、メディアサービスプロバイダ（例：Netflix、Amazon）まで、ソーシャルネットワーキングサービス（例：Facebook、LinkedIn、Twitter）まで、旅行サービス（例：Lyft、Uber、Airbnb、Booking.com）まで、**OCEは今やデータ駆動型の意思決定を支援している**[7, 10, 12, 27, 30, 40, 41, 44, 51, 58, 61, 76]。

## 1.1. First Practical Online Controlled Experiments Summit, 2018 1.1. 2018年第1回実践的オンライン対照実験サミット

To understand the top practical challenges in running OCEs at scale, representatives with experience in large-scale experimentation from thirteen different organizations (Airbnb, Amazon, Booking.com, Facebook, Google, LinkedIn, Lyft, Microsoft, Netflix, Twitter, Uber, Yandex, and Stanford University) were invited to the first Practical Online Controlled Experiments Summit.
OCEを大規模に実行する上での実践的な最重要課題を理解するため、13の異なる組織（Airbnb、Amazon、Booking.com、Facebook、Google、LinkedIn、Lyft、Microsoft、Netflix、Twitter、Uber、Yandex、Stanford University）から大規模実験の経験を持つ代表者を招き、第1回実践的オンライン対照実験サミットを開催した。
All thirteen organizations sent representatives.
全13団体が代表を派遣した。
Together these organizations tested more than one hundred thousand experiment treatments last year.
これらの組織は昨年、合わせて10万件以上の実験治療をテストした。
Thirty-four experts from these organizations participated in the summit in Sunnyvale, CA, USA on December 13-14, 2018.
2018年12月13日から14日にかけて米国カリフォルニア州サニーベールで開催されたサミットには、これらの組織から34人の専門家が参加した。
The summit was chaired by Ronny Kohavi (Microsoft), Diane Tang (Google), and Ya Xu (LinkedIn).
サミットの議長は、ロニー・コハヴィ（マイクロソフト）、ダイアン・タン（グーグル）、ヤ・シュウ（リンクトイン）が務めた。
During the summit, each company presented an overview of experimentation operations and the top three challenges they faced.
サミットでは、各社が実験業務の概要と直面する課題のトップ3を発表した。
Before the summit, participants completed a survey of topics they would like to discuss.
サミットに先立ち、参加者は話し合いたいテーマについてアンケートに答えた。
Based on the popular topics, there were nine breakout sessions detailing these issues.
人気の高いトピックに基づき、これらの問題を詳述する9つの分科会が開かれた。
Breakout sessions occurred over two days.
分科会は2日間にわたって行われた。
Each participant could participate in at least two breakout sessions.
参加者は少なくとも2つの分科会に参加できる。
Each breakout group presented a summary of their session to all summit participants and further discussed topics with them.
各分科会グループは、サミット参加者全員にセッションの概要を発表し、さらに参加者とトピックについて話し合った。
This paper highlights top challenges in the field of OCEs and common solutions based on discussions leading up to the summit, during the summit, and afterwards.
本稿では、サミットに向けた議論、サミット期間中、そして**サミット後の議論に基づき、OCEs分野における最重要課題と共通の解決策を紹介**する。

## 1.2. Online Controlled Experiments

Online Controlled Experiments, A/B tests or simply experiments, are widely used by data-driven companies to evaluate the impact of software changes (e.g.new features).
オンライン対照実験、A/Bテスト、または単に実験は、データ駆動型の企業がソフトウェアの変更（新機能など）の影響を評価するために広く使用されています。
In the simplest OCE, users are randomly assigned to one of the two variants: Control (A) or Treatment (B).
最も単純なOCEでは、ユーザーは無作為に2つのvariantのいずれかに割り当てられます：Control（A）またはTreatment（B）。
Usually, Control is the existing system and Treatment is the system with the new feature, say, feature X.
通常、Controlは既存のシステムで、Treatmentは新しい機能、例えば機能Xを持つシステムである。
User interactions with the system are recorded and from that, metrics computed.
システムに対するユーザのinteractionが記録され、その結果、メトリクスが計算されます。
If the experiment was designed and executed correctly, the only thing consistently different between the two variants is feature X.
もし実験が正しく設計され、実行されたのであれば、2つのvariantの間で一貫して異なるのは機能Xだけです。
External factors such as seasonality, impact of other feature launches, or moves by the competition, are evenly distributed between Control and Treatment, which means that we can hypothesize that any difference in metrics between the two groups can be attributed to either feature X or due to chance resulting from the random assignment to the variants.
季節性、他の機能の発売の影響、競合他社の動きなどの外部要因は、ControlとTreatmentの間で均等に分布されているため、2つのグループ間のメトリクスの違いは、機能Xまたはvariantへの無作為な割り当てによる偶然の結果のいずれかに帰属できると仮定できます。
The latter hypothesis is ruled out (probabilistically) using statistical tests such as a t-test [21].
後者の仮説は、t検定[21]などの統計検定を使って（確率的に）除外される。
This establishes a causal relationship (with high probability) between the feature change and changes in user behavior, which is a key reason for the widespread use of controlled experiments.
これにより、**ユーザの行動の変化と機能の変更との間に因果関係が（高い確率で）確立され、これが制御実験の広範な使用の主な理由**です。

## 1.3. Contribution 1.3.Contribution

OCEs rely on the same theory as randomized controlled trials (RCTs).
OCEはランダム化比較試験（RCT）と同じ理論に依拠している。
(ちゃんと設計されたOCE \in RCT?)
The theory of a controlled experiment dates back to Sir Ronald A.Fisher’s experiments at the Rothamsted Agricultural Experimental Station in England in the 1920s.
制御実験の理論は、1920年代のイギリスのロサムステッド農業実験所でのロナルド・A・フィッシャー卿の実験にさかのぼる。
While the theory is simple, deployment and evaluation of OCEs at scale (100s of concurrently running experiments) across variety of web sites, mobile apps, and desktop applications presents many pitfalls and research challenges.
理論は単純だが、多様なウェブサイト、モバイルアプリ、デスクトップアプリケーションでの**大規模なOCE（100以上の同時実行実験）の展開と評価には、多くの落とし穴と研究課題がある**。
Over the years some of these challenges and pitfalls have been described by authors from different companies along with novel methods to address some of those challenges [16, 23, 43, 48, 50, 61].
長年にわたり、これらの課題や落とし穴のいくつかが、それらの課題のいくつかに対処するための新しい方法とともに、さまざまな企業の著者によって説明されてきた[16, 23, 43, 48, 50, 61]。
This is the first time that OCE experts from thirteen organizations with some of the largest scale experimentation platforms have come together to identify the top challenges facing the industry and the common methods for addressing these challenges.
これは、**最大規模の実験プラットフォームを持つ13の組織からOCEの専門家が集まり、業界が直面する最重要課題と、これらの課題に対処するための共通の方法を特定する初めての機会**である。
This is the novel contribution of this paper.
これが本稿の斬新な貢献である。
We hope that this paper provides researchers a clear set of problems currently facing the industry and spurs further research in these areas in academia and industry.
本稿が、現在の業界が直面している明確な問題のセットを研究者に提供し、これらの分野における学界と産業界のさらなる研究を促進することを願っている。
It is our wish to continue this cross-company collaboration to help advance the science of OCEs.
OCEsの科学的発展に貢献するため、このような企業間のコラボレーションを継続することが我々の願いである。
Section 2 presents an overview of top challenges currently faced by companies across the industry.
セクション2では、**業界全体にわたって企業が現在直面している最重要課題の概要**を紹介する。
Later sections discuss specific problems in more detail, how these problems have an impact on running OCEs in different products, and common solutions for dealing with them
この後のセクションでは、具体的な問題の詳細、これらの問題がさまざまな製品で OCE を実行する際に どのような影響を及ぼすか、そしてこれらの問題に対処するための一般的な解決策について説明する。

<!-- ここまで読んだ -->

# 2. Top Challenges 2. トップチャレンジ

Software applications and services run at a very large scale and serve tens to hundreds of millions of users.
ソフトウェア・アプリケーションやサービスは非常に大規模で、数千万から数億のユーザにサービスを提供している。
It is relatively low cost to update software to try out new ideas.
新しいアイデアを試すためにソフトウェアを更新するコストは比較的低い。(これがソフトウェアプロダクトの特徴だよね...!)
Hundreds of changes are made in a software product during a short period of time.
ソフトウェア製品には、短期間に何百もの変更が加えられる。
This provides OCEs a unique set of opportunities and challenges to help identify the good changes from the bad to improve products.
このことは、OCEに、製品を改善するために良い変化と悪い変化を識別するためのユニークな機会と課題を提供する。
Our compiled list of top challenges comes from three sources: the pre-summit survey to collect the list of topics to discuss, the top challenges presented by each company at the start of the summit, and the post-summit survey on top takeaways and list of topics to discuss in future.
私たちがまとめたトップ・チャレンジのリストは、3つの情報源から得られたものである： すなわち、サミット前のアンケート調査による討議すべきトピックのリスト、サミット開始時に各社から提示されたトップ・チャレンジ、そしてサミット後のアンケート調査によるトップ・テイクアウェイと今後討議すべきトピックのリストである。
The relative order of prevalence remained roughly the same across these sources.
これらの情報源において、相対的な頻度の順序はおおむね同じであった。
These top challenges reflect the high level of maturity and scale of OCE operations in these companies.
これらの最重要課題は、これらの企業におけるOCE業務の高い成熟度と規模を反映している。
There is literature out there on the challenges and pitfalls some of these companies faced and solved during the early years of their operations [32].
このような企業が**運営を開始した初期の数年間に直面し、解決した課題や落とし穴についての文献**が存在している[32]。(これ有用そう??)
The challenges mentioned here are at the frontier of research in academia and industry.
ここに挙げた課題は、学界と産業界における研究の最前線にある。
While there are some solutions to existing challenges, there is a lot of scope for further advancement in these areas.
既存の課題に対する解決策はいくつかあるが、これらの分野にはさらなる進歩の余地が多くある。

## 1.Analysis:

There are many interesting and challenging open questions for OCE results analysis.
OCEの結果分析には、多くの興味深く、挑戦的なオープンな問題がある。
While most experiments in the industry run for 2 weeks or less, we are really interested in detecting the long-term effect of a change.
**業界のほとんどの実験は2週間以下で実行される**が、変更の長期的な影響を検出することに本当に興味がある。
How do long-term effects differ from short-term outcomes? How can we accurately measure those long term factors without having to wait a long time in every case?
長期的な影響は短期的な結果とどう違うのか？どのような場合にも長い時間をかけることなく、そのような長期的要因を正確に測定するにはどうすればよいのか？
What should be the overall evaluation criterion (OEC) for an experiment?
実験の総合評価基準（OEC）はどうあるべきか？
How can we make sure that the OEC penalizes things like clickbaits that increase user dissatisfaction?
OECが、ユーザーの不満を増大させるクリックベイトのようなものにペナルティを与えるようにするにはどうすればいいのか？
While there are methods to test an OEC based on a set of labelled experiments [24], how to best collect such set of experiments for evaluation of the OEC and other metrics?
ラベル付けされた実験セットに基づいてOECをテストする方法はあるが[24]、OECや他の評価基準を評価するために、そのような実験セットをどのように収集するのがベストなのだろうか？
While, there are models for estimating the long-term value (LTV) of a customer that may be a result of a complex machine learning model, can we leverage such models to create OEC metrics?
複雑な機械学習モデルの結果であるかもしれない、顧客の長期的価値（LTV）を推定するモデルがある一方で、OECの測定基準を作成するためにそのようなモデルを活用することはできるでしょうか？
Once we have OEC metrics and a Treatment improves or regresses the OEC metric, how can we best answer why the OEC metric improved or regressed and uncover the underlying causal mechanism or root cause for it?
OEC測定基準ができ、ある治療がOEC測定基準を改善または後退させたとしたら、なぜOEC測定基準が改善または後退したのか、そしてその根本的な原因メカニズムや根本原因を明らかにするにはどうすればよいのでしょうか？

Running experiments at a large scale introduces another set of issues.
大規模な実験を実行することは、別の問題を導入する。
It is common for large products serving millions of users to have 100s of experiments running concurrently, where each experiment can include millions of users.
数百万人のユーザーにサービスを提供する大規模な製品では、100以上の実験が同時に実行されるのが一般的で、各実験には数百万人のユーザーが含まれることもある。
For products running so many experiments, most of the low-hanging fruit get picked quickly and many Treatments may then cause a very small change in OEC metrics.
多くの実験を実行している製品では、大部分の簡単な問題はすぐに解決され、多くの治療がOEC指標にごくわずかな変化を引き起こすかもしれない。
It is important to detect these types of changes.
こうした変化を察知することが重要だ。
A very small change in a per-user metric may imply a change of millions of dollars in product revenue.
**ユーザーあたりのメトリクスのごくわずかな変化は、製品の収益の数百万ドルの変化を意味するかもしれない**。
How can we best increase the sensitivity of OECs and other experiments metrics without hurting the accuracy of these metrics to discern between good and bad Treatments [18, 42, 75]?
良い治療と悪い治療[18, 42, 75]を見分けるためのOECsや他の実験指標の正確さを損なわずに、OECsや他の実験指標の感度を高めるにはどうすれば良いでしょうか？
If we are running 100s of experiments concurrently how do we handle the issue of interaction between two treatments?
もし100以上の実験を同時に行う場合、2つの治療間の相互作用の問題をどのように扱うか？
How can we learn more from analyzing multiple experiments together and sharing learnings across experiments? For a product with millions of users, there are many ways to segment users.
複数の実験を一緒に分析し、実験間で学習を共有するためにはどうすればよいか？数百万人のユーザを持つ製品では、ユーザをセグメント化する方法は多岐にわたる。
Even a small fraction of users is very significant.
たとえごく一部のユーザーであっても、それは非常に大きな意味を持つ。
Just understanding the average treatment effect on the entire population is not enough.
母集団全体に対する平均的な治療効果を理解するだけでは十分ではない。
How can we best identify heterogenous Treatment effects in different segments?
異なるセグメントの異なるtreatment効果を最もよく特定するにはどうすればよいか？

## Engineering and Culture:

Culture is the tacit social order of an organization: It shapes attitudes and behaviors in wide-ranging and durable ways.
文化は組織の暗黙の社会秩序であり、態度や行動を幅広くかつ持続的な方法で形作る。
Cultural norms define what is encouraged, discouraged, accepted, or rejected within a group [35].
**文化的規範は、集団の中で何が奨励され、何が落胆され、何が受け入れられ、何が拒否されるかを規定するもの**である［35］。
How do we build a culture to one that uses OCEs at scale to ensure we get a trustworthy estimate of the impact of every change made to a product and bases ship decisions on the outcome of OCEs [46]?
プロダクトに加えられたすべての変更の影響を信頼できる推定値を得るために、OCEを大規模に使用する文化をどのように構築すればよいか？また、OCEの結果に基づいてデプロイの決定を下すことが重要である[46]。
Engineering systems and tools are critical aspects to enable OCEs at scale.
OCEを大規模に実行するためには、エンジニアリングシステムとツールが重要な要素である。
What are some good development practices, data logging and data engineering patterns that aid trustworthy experimentation at scale?
大規模な実験における信頼性の高い実験を支援するいくつかの良い開発プラクティス、データロギング、データエンジニアリングパターンは何か？

## Deviations from Traditional A/B Tests:

従来のA/Bテストからの乖離：

Traditional A/B tests depend on a stable unit treatment value assumption(SUTVA) [39], that is, the response of any experiment unit (user) under treatment is independent of the response of another experiment unit under treatment.
**従来のA/Bテストは、stable unit treatment value assumption(SUTVA) [39]に依存**しており、つまり、治療下の実験単位（ユーザ）の応答は、治療下の別の実験単位の応答とは独立しているという仮定である。(複数のABテストの相互作用の話??)
There are cases where this assumption does not hold true, such as network interactions or interactions between multiple experiments.
ネットワークの相互作用や複数の実験間の相互作用など、この仮定が成り立たない場合もある。
If this issue is ignored, we may get a biased estimate of the treatment effect.
この問題を無視すると、治療効果の推定値に偏りが生じる可能性がある。
How can we detect such deviation? Where deviations are unavoidable, what is the best method to obtain a good estimate of the treatment effect? 4.
そのような乖離を検出するにはどうしたらよいか？乖離が避けられない場合、治療効果の良好な推定値を得るための最良の方法は何か？

## Data quality:

Trustworthiness of the results of an OCE depend on good data quality.
OCEの結果の信頼性は、良好なデータ品質に依存している。
What are some best practices to ensure good data quality?
良好なデータ品質を確保するためのベストプラクティスにはどのようなものがあるか？
While the sample Ratio Mismatch test is a standard industry test to indicate data quality issues in OCEs [13, 22, 23, 45], what are other critical data quality tests to perform during OCE results analysis?
**sample ratio mismatch test**(??)は、OCEにおけるデータ品質の問題を示すための標準的な業界テストである[13, 22, 23, 45]が、OCEの結果分析中に実行する他の重要なデータ品質テストは何か？

<!-- ここまで読んだ! -->

# 3. Estimating the long-term effect 3. 長期的効果の推定

## 3.1. Problem # 3.1.Problem

Though it only takes a few days to change a part of a software product or service, the impact of that change may take a long time to materialize in terms of key product indicators (KPIs) and can vary across products and scenarios.
ソフトウェア製品やサービスの一部を変更するには数日しかかからないが、その変更の影響がkey product indicators（KPIs）の観点で具体化するのには長い時間がかかることがあり、製品やシナリオによって異なる。
This makes it challenging to estimate the long-term impact of a change.
このため、**長期的な影響を見積もるのは難しい**。
For instance, the impact of a change of ranking results in an online travel service on customer satisfaction may not be fully understood until customers stay in a vacation rental or hotel room months after booking.
例えば、オンライン旅行サービスにおけるランキング結果の変化が顧客満足度に与える影響は、顧客が予約から数ヶ月後にバケーションレンタルやホテルの部屋に滞在するまで、完全には理解できないかもしれない。
Increasing the number of ads and hence decreasing their quality on a search results page may bring in more revenue in the first few weeks, but might have the opposite impact months later due to user attrition and users learning that ad results are less useful and ignoring them [38].
検索結果ページで広告の数を増やし、その質を下げると、最初の数週間は収益が増えるかもしれないが、数カ月後にはユーザーの減少や、ユーザーが広告結果があまり役に立たないことを学習して無視するため、逆の影響が出るかもしれない[38]。
Investing in user retention and satisfaction through better user experience can be more beneficial over the long term than what short term measurements indicate.
**より良いユーザー・エクスペリエンスを通じてユーザの維持と満足に投資することは、短期的な測定が示すよりも長期的に有益**である。
Introduction of clickbaits on a content provider service may cause increase in clicks due to the novelty effect but may induce larger dissatisfaction in the long term as users learn about poor content quality.
コンテンツプロバイダーのサービスにクリックベイトを導入すると、目新しさ効果でクリック数は増えるかもしれないが、コンテンツの質の低さをユーザーが知ることで、長期的にはより大きな不満を誘発する可能性がある。
Further, in twosided markets [71], some changes like pricing in ads, ride-sharing services, or home-sharing services may introduce a market effect with a shift in either demand or supply in the eco-system and it may take a long time before the market finds a new equilibrium.
さらに、two-sided markets(=wantedlyさんとか!) [71]では、広告、ライドシェアリングサービス、またはホームシェアリングサービスの価格設定などの変更が、エコシステム内の需要または供給のシフトとともに市場効果を導入し、市場が新しい均衡を見つけるまでには長い時間がかかるかもしれない。

<!-- ここまで読んだ! -->

## 3.2. Common Solutions and Challenges

### 3.2.1. Long-term Experiments or Holdouts 3.2.1. 長期的な実験か、保留か

Running experiments for a long duration is not usually a good answer.
長期間実験を続けることは、通常は良い答えではない。
Most software companies have very short development cycles for planning, developing, testing, ultimately shipping new features.
ほとんどのソフトウェア会社は、新機能の計画、開発、テスト、最終的な出荷までの開発サイクルが非常に短い。
Short development cycles enable companies to be agile and quickly adapt to customer needs and the market.
短い開発サイクルによって、企業は機敏になり、顧客のニーズや市場に素早く適応することができる。
Long testing phases for understanding the impact of changes could harm a company’s agility and are not usually desirable.
変更の影響を理解するための長いテスト段階は、企業の敏捷性を損なう可能性があり、通常は望ましくない。
Another option is a long-term holdout group consisting of a random sample of users who do not get updates.
もう一つの選択肢は、アップデートを受けないユーザーの無作為サンプルで構成される長期保留グループである。
This holdout group acts as the Control against the set of features shipping to everyone else.
この保留グループは、他のすべての人に出荷される一連の機能に対するコントロールの役割を果たす。
This option usually incurs a lot of engineering cost.
このオプションには通常、多くのエンジニアリング・コストがかかる。
The product development team must maintain a code fork that is not updated for a long time.
製品開発チームは、長期間更新されないコードフォークを維持しなければならない。
All upstream and downstream components to this code must support this fork as well.
このコードの上流および下流のコンポーネントはすべて、このフォークをサポートしなければならない。
This still does not solve the challenges of non-persistent user tracking and network interactions described below.
それでも、以下に述べる非永続的なユーザー追跡とネットワーク相互作用の課題を解決することはできない。
In many products and services, the first visit and subsequent visits of users is tracked using a non-persistent user identifier, like a random GUID [72] stored in a browser cookie.
多くの製品やサービスでは、ブラウザのクッキーに保存されたランダムなGUID [72]のような永続的でないユーザー識別子を使用して、ユーザーの初回訪問とその後の訪問が追跡されます。
This way of tracking users is not very durable over a long time as users churn their cookies and we are left with tracking a biased sample of all users exposed to the variants [23].
ユーザを追跡するこの方法は、ユーザがクッキーを破棄してしまうので、長い間あまり長続きせず、バリアント[23]にさらされた全ユーザの偏ったサンプルを追跡することになります。
Further, a user may access the same service from multiple devices, and the user’s friends and family may access the same service.
さらに、ユーザーは複数のデバイスから同じサービスにアクセスする可能性があり、ユーザーの友人や家族も同じサービスにアクセスする可能性がある。
As time goes on, a user or their friends or family may be exposed to both the treatment and control experience during an experiment, which dilutes the impact of the treatment being measured in the experiment.
時間が経つにつれて、利用者やその友人や家族は、実験中に治療と対照の両方の体験にさらされる可能性があり、実験で測定される治療の影響が薄れてしまう。
There is some value in running experiments a little longer when we suspect that there is a short-term novelty or user learning effect.
短期的な新規性効果やユーザー学習効果があると思われる場合、実験を少し長めに行うことには価値がある。
At Microsoft, while most experiments do not run for more than two weeks, it is recommended to run an experiment longer if novelty effects are suspected and use data from the last week to estimate the long-term treatment effect [23].
マイクロソフトでは、ほとんどの実験が2週間以上実施されることはないが、新規性効果が疑われる場合は、実験を長く実施し、最後の週のデータを使用して長期的な治療効果を推定することが推奨されている[23]。
At Twitter, a similar practice is followed.
ツイッターでも同様の慣行がある。
An experiment at Twitter may run for 4 weeks and data from last two weeks is analyzed.
ツイッターでの実験は4週間行われ、最後の2週間のデータが分析される。
If a user exposed in the first two weeks does not appear in the last two weeks, values are imputed for that user when possible (like imputing 0 clicks).
最初の2週間に露出したユーザーが最後の2週間に現れなかった場合、可能な限りそのユーザーの値がインプットされる（0クリックのインプットのように）。
However, it may not be possible to impute values for metrics, like ratio or performance metrics.
しかし、比率やパフォーマンスメトリクスのようなメトリクスの値をインプットすることはできないかもしれない。

### 3.2.2. Proxies 3.2.2. プロキシ

Good proxies that are predictive of the long-term outcome of interest are commonly used to estimate the long-term impact.
長期的な影響を推定するためには、対象となる長期的な結果を予測できる優れた指標が一般的に使用される。
For instance, Netflix has used logistic regression to find good predictors for user retention.
例えば、ネットフリックスはロジスティック回帰を使って、ユーザー維持のための良い予測因子を見つけた。
Netflix also used survival analysis to take censoring of user data into account.
また、ネットフリックスは生存分析を用いて、ユーザーデータの打ち切りを考慮に入れている。
LinkedIn created metrics based on a lifetime value model.
LinkedInは、生涯価値モデルに基づいて指標を作成した。
For treatments that effect the overall market, Uber found some macro-economic models to be useful in finding good proxies.
市場全体に影響を与える治療法については、ユーバーはマクロ経済モデルが適切なプロキシを見つけるのに有用であることを発見した。
There can be downsides to this approach as correlation may not imply causation, and such proxies could be susceptible to misuse, where a treatment may cause an increase in the proxy metric, but ends up having no effect or regression in the long-term outcome.
相関関係は因果関係を意味しないかもしれず、このような代用指標は、治療が代用指標を増加させるかもしれないが、長期的な結果では結局効果がなかったり、後退してしまったりするような、誤用の影響を受けやすい可能性があるため、このアプローチには欠点がある。
It may be better to develop a mental causal structure model to find good proxies.
良いプロキシを見つけるためには、精神的因果構造モデルを開発する方が良いかもしれない。
Bing and Google have found proxies for user satisfaction and retention by having a mental causal structure model that estimates the utility of an experience to users.
ビングとグーグルは、ユーザーにとっての経験の有用性を推定する心的因果構造モデルを持つことで、ユーザーの満足度とリテンションのプロキシを発見した。

### 3.2.3. Modeling User Learning 3.2.3. ユーザー学習のモデリング

Another approach followed by Google is to explicitly model the user learning effects using some long duration experiments [38].
グーグルが採用しているもう一つのアプローチは、長時間の実験を用いてユーザーの学習効果を明示的にモデル化することである[38]。
In long duration experiments, there are multiple and exclusive random samples of users exposed to the treatment.
長期間の実験では、治療にさらされるユーザーの複数の排他的無作為サンプルが存在する。
One group is exposed to the treatment from the start of the experiment.
一方のグループは、実験開始時から治療にさらされる。
A second group has a lagged start, being exposed to the treatment at some point after the start, and so on.
もう1つのグループはスタートが遅れており、スタート後のある時点で治療を受けている。
Comparing these groups a day after the second group is exposed to the treatment provides an estimate of user learning from the treatment.
2番目のグループが治療を受けた1日後にこれらのグループを比較することで、治療によるユーザーの学習の推定値が得られる。
Google also used cookie-cookie day randomization to get an estimate of user learning for any duration (in days) since the experiment started.
Googleはまた、実験開始からの任意の期間（日単位）のユーザー学習の推定値を得るために、クッキー・クッキーの日ランダム化を使用した。
In these experiments and in the subsequent analysis, the authors carefully designed the experiments and did careful analysis to ensure that they were not seeing many confounding effects (e.g., other system changes, system learning, concept drift, as well as selection bias issues due to cookie churn/short cookie lifetimes).
これらの実験とその後の分析において、著者たちは実験を注意深く設計し、多くの交絡効果（たとえば、他のシステム変更、システム学習、コンセプト・ドリフト、またクッキーの解約/短いクッキー寿命による選択バイアスの問題）が見られないことを確実にするために、注意深い分析を行いました。
They took this information and modeled user learning as an exponential curve, which allowed them to predict the long-term outcome of a treatment using the short-term impact of the treatment directly measured in the experiment and the prediction of the impact of the treatment on user learning.
彼らはこの情報をもとに、ユーザーの学習を指数関数曲線としてモデル化し、実験で直接測定された治療の短期的な影響と、治療のユーザー学習への影響の予測を用いて、治療の長期的な結果を予測できるようにした。

### 3.2.4. Surrogates 3.2.4. サロゲート

Surrogate modeling is another way to find good estimates of longterm outcome.
サロゲート・モデリングは、長期転帰の良い推定値を見つけるもう一つの方法である。
A statistical surrogate lies on the causal path between the treatment and the long-term outcome.
統計的サロゲートは、治療と長期的転帰の間の因果経路にある。
It satisfies the condition that treatment and outcome are independent conditional on the statistical surrogate.
これは、治療と結果が統計的代用物を条件として独立であるという条件を満たす。
You can use observational data and experiment data to find good surrogates.
観測データや実験データを使って、良いサロゲートを見つけることができる。
Even if no individual proxy satisfies the statistical surrogacy criterion, a highdimensional vector of proxies may collectively satisfy the surrogacy assumption [8].
たとえ個々のプロキシが統計的サロガシー基準を 満たさないとしても、プロキシの高次元のベクトルは、集合的 にサロガシーの仮定を満たすかもしれない[8]。
Having a rich set of surrogates reduces the risk of affecting only a few surrogates and not the long-term outcome.
豊富なサロゲートのセットを持つことで、少数のサロゲートだけに影響を与え、長期的な転帰に影響を与えないリスクを減らすことができる。
Facebook used this approach with some success to find good surrogates of the 7-day outcome of an experiment by just using 2-3-day experiment results.
フェイスブックは、2〜3日の実験結果を使うだけで、7日間の実験結果の良い代用品を見つけることに成功した。
They used quantile regression and a gradient-boosted regression tree to rank feature importance.
彼らは、特徴の重要度をランク付けするために、分位回帰と勾配ブースト回帰木を使用した。
Note that there is still a risk that having too many surrogates for the long term may make this approach less interpretable.
長期的なサロゲートの数が多すぎると、このアプローチが解釈しにくくなる危険性があることに注意してほしい。

# 4. OEC: Overall Evaluation Criterion Metric 4. OEC： 総合評価基準

## 4.1. Problem # 4.1.Problem

One key benefit of evaluating new ideas through OCEs is that we can streamline the decision-making process and make it more objective.
OCEを通じて新しいアイデアを評価することの重要な利点のひとつは、意思決定プロセスを合理化し、より客観的なものにできることだ。
Without understanding the causal impact of an idea on customers, the decision-making process requires a lot of debate.
あるアイデアが顧客に与える因果関係を理解しなければ、意思決定プロセスには多くの議論が必要となる。
The proponents and opponents of the idea advance their arguments regarding the change only relying on their own experience, recall, and interpretation of certain business reports and user comments.
賛成派も反対派も、自分たちの経験や記憶、特定のビジネスレポートやユーザーのコメントの解釈だけを頼りに、この変更に関する議論を進めている。
Eventually the team leader makes a call on whether to ship the idea.
最終的にチームリーダーは、そのアイデアを出荷するかどうかの判断を下す。
This style of decision making is based on the HiPPO (Highest Paid Person’s Opinion) [37] and is fraught with many cognitive biases [2].
このような意思決定のスタイルは、HiPPO（高給取りの意見）[37]に基づいており、多くの認知バイアスをはらんでいる[2]。
To help change HiPPO decisions to more objective, data-driven decisions based on the causal impact of an idea from customer response [5], we recommend establishing the OEC for all experiments on your product.
HiPPOの決定を、顧客の反応[5]からアイデアの因果的影響に基づく、より客観的なデータ主導の決定に変えるために、製品に関するすべての実験についてOECを設定することを推奨する。
Not all metrics computed to analyze the results of an experiment are part of the OEC.
実験結果を分析するために計算されるすべてのメトリクスがOECの一部というわけではない。
To analyze experiment results, we require different types of metrics [22].
実験結果を分析するには、さまざまな種類のメトリクスが必要である[22]。
First, we need to know if the results of an experiment are trustworthy.
まず、実験結果が信頼できるかどうかを知る必要がある。
A set of data quality metrics, like a sample ratio, help raise red flags on critical data quality issues.
サンプル比率のような一連のデータ品質指標は、重大なデータ品質問題の赤旗を掲げるのに役立つ。
After checking the data quality metrics, we want to know the outcome of the experiment.
データ品質メトリクスをチェックした後、実験の結果を知りたい。
Was the treatment successful and what was its impact? This set of metrics comprise the OEC.
治療は成功したのか、その影響はどうだったのか。この一連の指標がOECを構成する。
In addition to OEC metrics, we have found that there is a set of guardrail metrics which are not clearly indicative of success of the feature being tested, but metrics that we do not want to harm.
OECメトリクスに加えて、私たちは、テストされる機能の成功を明確に示すものではないが、私たちが害を及ぼしたくないメトリクスのガードレールメトリクスのセットがあることを発見した。
The remaining bulk of the metrics for an experiment are diagnostic, feature or local metrics.
実験のメトリクスの残りの大部分は、診断、特徴、または局所的なメトリクスである。
These metrics help you understand the source of OEC movement (or the lack of).
これらの指標は、OECの動きの原因（またはその欠如）を理解するのに役立ちます。
It is hard to find a good OEC.
良いOECを見つけるのは難しい。
Here are a few key properties [19, 24, 55] to consider.
以下に、考慮すべきいくつかの重要な特性 [19, 24, 55] を示す。
First, a good OEC must be indicative of the long-term gain in key product indicators (KPIs).
第一に、優れたOECは、主要製品指標（KPI）の長期的な向上を示すものでなければならない。
At the very least make it directionally accurate in estimating the impact on the longterm outcome.
少なくとも、長期的な結果に対する影響を推定する上で、方向性を正確にすること。
Second, OEC must be hard to game and it should incentivize the right set of actions in the product team.
第二に、OECはゲームになりにくく、製品チームの適切な行動にインセンティブを与えるものでなければならない。
It should not be easy to satisfy the OEC by doing the wrong thing.
間違ったことをしてOECを満足させることは容易ではないはずだ。
For instance, if the OEC is limited to a part or feature of the product, you may be able to satisfy the OEC by cannibalizing other parts or features.
例えば、OECが製品の一部や機能に限定されている場合、他の部品や機能を共食いさせることでOECを満たすことができるかもしれません。
Third, OEC metrics must be sensitive.
第三に、OECの指標は敏感でなければならない。
Most changes that impact the long-term outcome should also have a statistically significant movement in OEC metrics so it is practical to use the OEC to distinguish between good and bad changes to the product.
長期的な結果に影響を与えるほとんどの変更は、OEC測定基準においても統計的に有意な動きを示すはずなので、OECを使用して製品の良い変更と悪い変更を区別することは実用的である。
Fourth, the cost of computing OEC metrics cannot be too expensive.
第四に、OECメトリクスの計算コストは高すぎてはならない。
OEC metrics must be computed for 100s of the experiments and be run on millions of users each and every week.
OECの指標は、毎週、何百万人ものユーザーに対して、100回もの実験で計算され、実行されなければならない。
Methods that involve costly computation or costly procedures like human surveys or human judges may not scale well.
コストのかかる計算や、人間による調査や人間の審判のようなコストのかかる手続きを伴う方法は、うまくスケールしない可能性がある。
Fifth, OEC metrics must account for a diverse set of scenarios that may drive the key product goals.
第五に、OECの指標は、主要な製品目標を推進する可能性のある多様なシナリオを考慮しなければならない。
Finally, OEC should be able to accommodate new scenarios.
最後に、OECは新たなシナリオに対応できなければならない。
For instance, direct answers to queries like current time would provide a good user experience in a search engine, but if you only base the OEC metrics on clicks, those metrics will miss this scenario.
例えば、現在時刻のようなクエリに対する直接的な回答は、検索エンジンにおいて良いユーザーエクスペリエンスを提供するだろうが、OECメトリクスのベースをクリック数だけに置くと、そのメトリクスはこのシナリオを見逃すことになる。

## 4.2. Common Solutions and Challenges

### 4.2.1. Search vs. Discovery 4.2.1. 検索対検索 ディスカバリー

Measuring the success of a search experience in search engines has been a research subject for a long time in academia and for many products including Bing, Google and Yandex.
検索エンジンにおける検索体験の成功を測定することは、アカデミアや、Bing、Google、Yandexを含む多くの製品において、長い間研究課題となってきた。
It is well established that metrics, like queries per user, cannot be a good OEC because queries per user may go up when search ranking degrades.
ユーザーあたりのクエリのような指標は、良いOECにはなり得ないことはよく知られている。
Sessions per user or visits per user are considered better OEC metrics [49].
ユーザーあたりのセッションやユーザーあたりの訪問は、より良いOECメトリックと考えられている[49]。
In general there is an appreciation of focusing on HEART (Happiness, Engagement, Adoption, Retention, and Task success) metrics for the OEC and use PULSE (Page views, Uptime, Latency, Seven-day active users [i.e., the number of unique users who used the product at least once in the last week], and Earnings) metrics as your guardrail metrics [62].
一般的に、OECのHEART（Happiness、Engagement、Adoption、Retention、Task success）メトリクスに注目し、PULSE（Page views、Uptime、Latency、Seven-day active users [つまり、過去1週間に少なくとも1回製品を使用したユニークユーザーの数]、Earnings）メトリクスをガードレールメトリクスとして使用することが評価されている[62]。
Over time, different methods have been proposed to measure HEART metrics in search engines and other goal-directed activities [36, 54].
サーチエンジンやその他の目標指向活動において、HEARTメトリクスを測定するためのさまざまな方法が提案されてきた[36, 54]。
It is still challenging to find metrics similar to HEART metrics to work for discovery- or browsing-related scenarios, like news articles shown on the Edge browser homepage, or Google mobile homepage, or Yandex homepage.
Edgeブラウザのホームページ、Googleモバイルのホームページ、Yandexのホームページに表示されるニュース記事のような、発見やブラウジングに関連するシナリオで機能するHEARTメトリクスに似たメトリクスを見つけることは、まだ困難です。
The challenge is to understand user intent.
課題は、ユーザーの意図を理解することだ。
Sometimes users will come with a goal-oriented intent and would like to quickly find what they are looking for.
時には、ユーザーが目的志向の意図を持ってやってきて、探しているものを素早く見つけたいと思うこともある。
Other times users may have a more browsing or discovering-newinformation intent where they are not looking for something specific but just exploring a topic.
また、ユーザーが特定の何かを探しているのではなく、ただトピックを探求しているような、よりブラウジング的な、あるいは新しい情報を発見するような意図を持っている場合もある。
In this case it is not clear if lack of a click on an article link with a summary snippet can be viewed as a negative experience or positive because users got the gist of the article and did not have to click further.
この場合、要約スニペット付きの記事リンクをクリックしなかったことをネガティブな経験と見るか、ユーザーが記事の要点を理解し、それ以上クリックする必要がなかったことをポジティブな経験と見るかは明らかではない。
Further the two intents (goal-oriented and browsing) can compete.
さらに、2つの意図（目標志向と閲覧）は競合する可能性がある。
If a user came with a goal-oriented intent but got distracted and ended up browsing more, it may cause dissatisfaction in the long term.
目的があって来たのに、気が散ってもっと見てしまったというのでは、長期的には不満が残る。

### 4.2.2. Product Goals and Tradeoffs 4.2.2. 製品の目標とトレードオフ

OEC metrics usually indicate improvement in product KPIs or goals in the long term.
OECの指標は通常、長期的には製品のKPIや目標の改善を示す。
This assumes that product goals are clear.
これは、製品の目標が明確であることを前提としている。
This is not a trivial problem.
これは些細な問題ではない。
It takes a lot of effort and energy to have clarity on product goals and strategy alignment across the entire team.
製品目標を明確にし、チーム全体で戦略を一致させるには、多くの努力とエネルギーが必要だ。
This includes decisions like defining who the customer is and how best to serve them.
これには、顧客が誰なのか、どのように顧客にサービスを提供するのがベストなのかを定義するような決定も含まれる。
Further, your team must also create a monetization strategy for the product.
さらに、チームは製品の収益化戦略も立てなければならない。
In absence of such clarity, each sub team in the product group may set their own goals that may not align with other teams’ or corporate goals.
このような明確さがない場合、製品グループの各サブチームは、他のチームや企業の目標と一致しない独自の目標を設定する可能性がある。
Even after the product goals are clear, in most companies you end up with a handful of key metrics of interest.
製品目標が明確になっても、ほとんどの企業では、関心のある主要な指標はほんの一握りである。
It is challenging how to weigh these metrics relative to each other.
これらの指標をどう相対的に評価するかは難しい。
For instance, a product may have goals around revenue and user happiness.
例えば、ある製品には収益やユーザーの幸福度に関する目標があるかもしれない。
If a feature increases user happiness but losses revenue, in what case is it desirable to ship this feature? This decision is often made on a caseby-case basis by leadership.
ある機能がユーザーの幸福度を高めるが、収益が減少する場合、どのような場合にこの機能を出荷するのが望ましいか？この決定は、リーダーシップによってケースバイケースでなされることが多い。
Such an approach is susceptible to a lot of cognitive biases, and also may result in an incoherent application of the overall strategy.
このようなアプローチは多くの認知バイアスの影響を受けやすく、また全体的な戦略の適用が支離滅裂になる可能性もある。
Some product teams like at Bing, tried to come up with weights on different goals to make this tradeoff align with the overall product strategy and help ensure that consistent decision-making processes are used across multiple experiments.
Bingのように、このトレードオフを全体的な製品戦略と整合させ、複数の実験にわたって一貫した意思決定プロセスが使用されるようにするために、異なる目標に対する重みを考え出そうとする製品チームもあった。

### 4.2.3. Evaluating Methods 4.2.3. メソッドの評価

We mentioned that OEC metrics help decision making more objective.
OECの指標が意思決定をより客観的なものにすると述べた。
For it to be widely adopted, it is important to establish a process to evaluate any changes to the OEC metrics.
OECが広く採用されるためには、OECの評価基準に対する変更を評価するプロセスを確立することが重要である。
In some cases, there may be an expert review team that examines changes to the OEC and ensure that it retains the properties of a good OEC.
場合によっては、OECへの変更を検討し、それが優れたOECの特性を保持していることを確認する専門家レビューチームが存在することもある。
To make this process even more objective, we can have a corpus of past experiments widely seen to have a positive, negative or neutral impact.
このプロセスをさらに客観的なものにするために、ポジティブ、ネガティブ、あるいはニュートラルな影響を与えたと広く見られている過去の実験のコーパスを用意することができる。
Changes to the OEC were evaluated on this corpus to ensure sensitivity and directional correctness [24].
OECの変更は、感度と方向性の正しさを保証するために、このコーパスで評価された[24]。
Microsoft and Yandex successfully used this approach to update OEC metrics.
マイクロソフトとヤンデックスは、OECの指標を更新するために、このアプローチを使用することに成功した。
The challenge here is to create a scalable corpus of experiments with trustworthy labels.
ここでの課題は、信頼できるラベルを持つスケーラブルな実験コーパスを作成することである。
Other approaches include doing degradation experiments, where you intentionally degrade the product in a treatment and evaluate if the OEC metrics can detect this degradation.
他のアプローチとしては、意図的に製品を劣化させ、OECメトリクスがこの劣化を検出できるかどうかを評価する劣化実験がある。
One well known example are experiments that slow down the user experience performed at Microsoft and Google [63, 64].
よく知られている例としては、マイクロソフトやグーグルで行われたユーザー体験を遅くする実験がある[63, 64]。
This is also a good thought exercise to go through while designing and evaluating OEC metrics to ensure that they are not gameable.
これはまた、OECの測定基準を設計し評価する際に、それがゲームにならないようにするために行う良い思考訓練でもある。

### 4.2.4. Using Machine Learning in Metrics 4.2.4. メトリクスにおける機械学習の活用

Some product teams tried to incorporate machine learning models (MLMs) to create a metric.
機械学習モデル（MLM）を組み込んで指標を作ろうとする製品チームもあった。
For instance, using sequences of user actions to create a score metric based on the likelihood of user satisfaction [36, 54, 57] or creating more sensitive OEC metrics by combining different metrics [25, 42, 59].
例えば、ユーザー満足の可能性に基づいたスコア・メトリックを作成するために、ユーザー・アクションのシーケンスを使用したり[36, 54, 57]、異なるメトリックを組み合わせることによって、より感度の高いOECメトリックを作成したり[25, 42, 59]。
Also, good proxies for long-term outcomes are often used to find good OEC metrics.
また、長期的なアウトカムの良い指標は、OECの良い指標を見つけるためによく使われる。
This area of experimentation is relatively new.
この分野の実験は比較的新しい。
Many product teams are carefully trying to test these methods in limited areas.
多くの製品チームは、限られた地域で慎重にこれらの方法を試している。
These methods are more commonly used in mature product areas, like search, where most of the low-hanging fruit is picked and we need more complex models to detect smaller changes.
このような方法は、検索のような成熟した製品分野でより一般的に使用されている。
For new products, it is usually better to use simple metrics as the OEC.
新製品の場合、通常はOECのような単純な指標を使う方がよい。
There are some concerns with using machine learning models to create metrics.
メトリクスの作成に機械学習モデルを使うことには、いくつかの懸念がある。
MLM based metrics can be harder to interpret and can appear as a blackbox, which reduces trustworthiness and makes it hard to understand why a metric may have moved.
MLMベースの指標は解釈が難しく、ブラックボックスのように見える可能性があるため、信頼性が低下し、指標が動いた理由を理解するのが難しくなる。
Refreshing MLMs by training them on most recent data may lead to an abrupt change in the metric that would hard to account for.
最新のデータでMLMをトレーニングすることによってMLMをリフレッシュさせると、メトリックが突然変化する可能性があり、それを考慮するのは難しい。
If the MLM is being refreshed while an experiment is running, it can create bias in the metric.
実験の実行中にMLMが更新されると、指標に偏りが生じる可能性がある。
Further, there are concerns these metrics are easily gamed by optimizing for the underlying model that created these metrics, which may or may not lead to improvement in the longterm outcome of interest.
さらに、これらの測定基準は、これらの測定基準を作成した基礎モデルに対して最適化することで、簡単にゲーム化される懸念がある。
