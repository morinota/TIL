## 0.1. link 0.1. リンク

- [page](https://arxiv.org/abs/2209.09125) ページ](https:

- [pdf](https://arxiv.org/pdf/2209.09125.pdf) pdf](https:

## 0.2. title 0.2. タイトル

Operationalizing Machine Learning:
機械学習の運用化.
An Interview Study
インタビュー調査

## 0.3. abstract 0.3. 抽象的

Organizations rely on machine learning engineers (MLEs) to operationalize ML, i.e., deploy and maintain ML pipelines in production.
企業はMLを運用するために**機械学習エンジニア（MLE）**に頼っている. つまり、**MLパイプラインを本番環境に導入し、維持すること**である.
The process of operationalizing ML, or MLOps, consists of a continual loop of (i) data collection and labeling, (ii) experimentation to improve ML performance, (iii) evaluation throughout a multi-staged deployment process, and (iv) monitoring of performance drops in production.
MLを運用するプロセス（**MLOps**）は、（i）データの収集とラベリング、（ii）MLのパフォーマンスを向上させるための実験、（iii）多段階のデプロイプロセスを通じた評価、（iv）運用中のパフォーマンス低下の監視の継続的なループから構成されている.
When considered together, these responsibilities seem staggering—how does anyone do MLOps, what are the unaddressed challenges, and what are the implications for tool builders?
これらの責任をまとめて考えると、どのようにMLOpsを行うのか、未解決の課題は何か、ツールビルダーにとってどのような意味があるのか、など途方もないことに思える.
We conducted semi-structured ethnographic interviews with 18 MLEs working across many applications, including chatbots, autonomous vehicles, and finance.
私たちは、チャットボット、自律走行車、金融など、さまざまなアプリケーションで活躍する18人のMLEに、半構造化エスノグラフィック・インタビューを実施した.
Our interviews expose three variables that govern success for a production ML deployment:
インタビューでは、**ML の本番展開の成功を左右する 3 つの変数**が明らかになった.
Velocity, Validation, and Versioning.
**ベロシティ**、**バリデーション**、**バージョニング**である.
We summarize common practices for successful ML experimentation, deployment, and sustaining production performance.
我々は、**MLの実験、デプロイメント、そして本番パフォーマンスを維持するための一般的なプラクティスを要約している**.
Finally, we discuss interviewees’ pain points and anti-patterns, with implications for tool design.
最後に、インタビューに答えてくれた人たちのペインポイントやアンチパターンについて、ツールデザインへの示唆を含めて議論する.

# 1. Introduction 1. はじめに

As Machine Learning (ML) models are increasingly incorporated into software, a nascent sub-field called MLOps (short for ML Operations) has emerged to organize the “set of practices that aim to deploy and maintain ML models in production reliably and efficiently” [4, 77].
機械学習（ML）モデルがますますソフトウェアに組み込まれるようになるにつれて，**MLOps（ML Operationsの略）**と呼ばれる新しいsub-fieldが，"**生産中のMLモデルを確実かつ効率的に展開・維持することを目的とした一連のpractice(実践)**"を組織するために出現している[4, 77]．
It is widely agreed that MLOps is hard.
MLOpsが難しいことは広く知られている.
Anecdotal reports claim that 90% of ML models don’t make it to production [76]; others claim that 85% of ML projects fail to deliver value [69].
逸話的な報告によれば，**90%のMLモデルが本番環境に移行できていない[76]，また，85%のMLプロジェクトが価値を提供できていない[69]と主張しているものもある**.
At the same time, it is unclear why MLOps is hard.
同時に、なぜMLOpsが難しいのかは不明である.
Our presentday understanding of MLOps is limited to a fragmented landscape of white papers, anecdotes, and thought pieces [14, 18, 20, 21, 34, 45], as well as a cottage industry of startups aiming to address MLOps issues [27].
MLOpsに関する我々の現在の理解は、白書、逸話、考察[14、18、20、21、34、45]の断片的な風景と、MLOpsの問題に取り組むことを目指すスタートアップの家内工業[27]に限られている.
Early work by Sculley et al. attributes MLOps challenges to “technical debt”, due to which there is “massive ongoing maintenance costs in real-world ML systems” [64].
Sculleyらによる初期の研究は，**MLOpsの課題を "技術的負債 "とし**，その原因は "実世界のMLシステムにおける膨大な継続的メンテナンスコスト "であるとしている[64]．
Most successful ML deployments seem to involve a “team of engineers who spend a significant portion of their time on the less glamorous aspects of ML like maintaining and monitoring ML pipelines” [54].
**ほとんどの成功したMLデプロイメントは、"MLパイプラインの保守や監視のようなMLのあまり華やかでない側面に彼らの時間のかなりの部分を費やすエンジニアのチーム"[54]を含む**ようである.
Prior work has studied general practices of data analysis and science [30, 49, 62, 82], without considering MLOps challenges of productionizing models.
先行研究は、モデルを生産化するMLOpsの課題を考慮することなく、データ分析と科学の一般的なプラクティス[30, 49, 62, 82]を研究している.

There is thus a pressing need to bring clarity to MLOps, specifically in identifying what MLOps typically involves—across organizations and ML applications.
このため、MLOpsを明確にすることが急務となっている. 特に、組織やMLアプリケーションの違いを超えて、MLOpsにはどのようなものがあるのかを明らかにすることが必要である.
A richer understanding of best practices and challenges in MLOps can surface gaps in present-day processes and better inform the development of next-generation tools.
MLOpsのベストプラクティスと課題をより深く理解することで、現在のプロセスにおけるギャップを明らかにし、次世代ツールの開発により良い情報を提供することができる.
Therefore, we conducted a semi-structured interview study of ML engineers (MLEs), each of whom has worked on ML models in production.
そこで、我々は、実運用中のMLモデルの開発に携わった経験のあるMLエンジニア（MLE）を対象に、半構造化インタビュー調査を実施した.
We sourced 18 participants from different organizations and applications (Table 1) and asked them open-ended questions to understand their workflow and day-to-day challenges.
異なる組織やアプリケーションから18名の参加者を募り（表1）、彼らのワークフローや日々の課題を理解するために自由形式の質問を行った.

We find that MLEs perform four routine tasks, shown in Figure 1: (i) data collection, (ii) experimentation, (iii) evaluation and deployment, and (iv) monitoring and response.
MLEは、図1に示すように、(i)データ収集、(ii)実験、(iii)評価と展開、(iv)モニタリングと対応という**4つのルーチンワーク**を行うことが分かっている.
Across tasks, we observe three variables that dictate success for a production ML deployment:
各タスクにおいて、我々はML導入の成功を決定付ける3つの変数を観察している.
Velocity, Validation, and Versioning.1 We describe common MLOps practices, grouped under overarching findings:
ここでは、MLOpsの一般的なプラクティスを、包括的な発見の下にグループ化して説明する.

ML engineering is very experimental in nature (Section 4.3).
**MLエンジニアリングは非常に実験的な性質を持っている**(セクション4.3)．
As mentioned earlier, various articles claim that it is a problem for 90% of models to never make it to production [76], but we find that this statistic is misguided.
先に述べたように、様々な記事で、90%のモデルが製品化されないのは問題である とされているが [76]、この統計は見当違いであることがわかる.
The nature of constant experimentation is bound to create many versions, a small fraction of which (i.e. “the best of the best”) will make it to production.
絶え間ない実験の性質上，多くのバージョンが作られるはずであるが，生産に至るのはそのうちのごく一部（すなわち「ベスト・オブ・ザ・ベスト」）である．
Thus it is beneficial to prototype ideas quickly, by making minimal changes to existing workflows, and demonstrate practical benefits early—so that bad models never make it far.
したがって、**既存のワークフローに最小限の変更を加えることでアイデアを素早くプロトタイプ化し、早期に実用的な利点を実証することは有益**であり、悪いモデルが遠くに行ってしまうことはないのである.

Operationalizing model evaluation requires an active organizational effort (Section 4.4).
モデル評価の運用には、積極的な組織的取り組みが必要(セクション4.4).
Popular model evaluation “best practices” do not do justice to the rigor with which organizations think about deployments: they generally focus on using one typically-static held-out dataset to evaluate the model on [38] and a single ML metric choice (e.g., precision, recall) [1, 2].
一般的なモデル評価の「ベストプラクティス」は、組織が展開について考える厳しさを正当に評価しない. 一般的には、モデルを評価するために、一般的に固定された一つのデータセット[38]と一つのMLメトリックの選択（例えば、精度、リコール）[1、2]に焦点を当てている.
We find that MLEs invest significant resources in maintaining multiple up-todate evaluation datasets and metrics over time—especially ensuring that data sub-populations of interest are adequately covered.
私たちは、**MLEが複数の最新の評価データセットと評価指標を長期間にわたって維持するために、特に関心のあるデータ部分集団が十分にカバーされていることを保証するために、重要なリソースを投入している**ことを発見した.

Non-ML rules and human-in-the-loop practices keep models reliable in production (Section 4.5).
**非MLルールと人間がループに参加することで、生産時のモデルの信頼性が保たれる**（セクション4.5）.
We find that MLEs prefer simple ideas, even if it means handling multiple versions: for example, rather than leverage advanced techniques to minimize distribution shift errors [15, 83], MLEs would simply create new models, retrained on fresh data.
例えば、分布シフト誤差を最小化する**高度な技術 [15, 83] を活用するよりも、MLE は単に新しいモデルを作成し、新しいデータで再トレーニングを行う**ことを選択した.
MLEs ensured that deployments were reliable via strategies such as on-call rotations, model rollbacks, or elaborate rule-based guardrails to avoid incorrect outputs.
MLEは、オンコールローテーション、モデルのロールバック、または不正確な出力を回避するための精巧なルールベースのガードレールなどの戦略によって、配備の信頼性を確保した.

In Section 5, we discuss recurring MLOps challenges across all tasks.
セクション 5 では、すべてのタスクで繰り返し発生する MLOps の課題について説明する.
We express these pain points as tensions and synergies between our three “V” variables—for example, undocumented “tribal knowledge” about pipelines (Section 5.2.4) demonstrates a tension between velocity (i.e., quickly changing the pipeline in response to a bug) and well-executed versioning (i.e., documenting every change).
たとえば、パイプラインに関する文書化されていない"**tribal knowledge(部族の知識)**"（セクション5.2.4）は、 **Velocity(バグに対応してパイプラインを迅速に変更すること)**とよく実行される **Versioning(すべての変更を文書化すること)**の間の緊張を実証している.
We conclude the description of each pain point with a discussion of opportunities for future tools.
各ペインポイント(?)の説明は、将来のツールの可能性についての議論によって締めくくられる.

# 2. Related Work 2. 関連作品

Several books and papers in the traditional software engineering literature describe the need for DevOps, a combination of software developers and operations teams, to streamline the process of delivering software in organizations [13, 37, 39, 40].
従来のソフトウェア工学の文献には，組織におけるソフトウェアの提供プロセスを合理化するために，**ソフトウェア開発者と運用チームの組み合わせであるDevOps**の必要性を述べた書籍や論文がいくつかある[13, 37, 39, 40]．
Similarly, MLOps, or DevOps principles applied to machine learning, has emerged from the rise of machine learning (ML) application development in software organizations.
同様に，MLOps，すなわち機械学習に適用されるDevOpsの原則は，ソフトウェア組織における機械学習（ML）アプリケーション開発の台頭から生まれたものである．
MLOps is a nascent field, where most existing papers give definitions and overviews of MLOps, as well as its relation to ML, software engineering, DevOps, and data engineering [28, 34, 44, 73].
MLOpsはまだ始まったばかりの分野であり，既存の論文の多くはMLOpsの定義と概要，そしてML，ソフトウェア工学，DevOps，データ工学との関連性を述べている[28, 34, 44, 73]．
MLOps poses unique challenges because of its focus on developing, deploying, and sustaining models, or artifacts that need to reflect data as data changes over time [59, 65, 67].
**MLOpsは，時間の経過とともに変化するデータを反映する必要があるモデルや成果物を開発，展開，維持することに重点を置いているため，独自の課題を提起している**[59, 65, 67]．
We discuss work related to MLOps workflows, challenges and interview studies for ML.
我々は、MLOpsのワークフロー、課題、MLのためのインタビュー研究に関連する仕事を議論する.

MLOps Workflow.
MLOpsのワークフロー
The MLOps workflow involves supporting data collection and processing, experimentation, evaluation and deployment, and monitoring and response, as shown in Figure 1.
MLOps のワークフローは，図 1 に示すように，データの収集と処理，実験，評価と配備，監視と対応 を支援するものである．
Several research papers and companies have proposed tools to accomplish various tasks in the workflow, such as data pre-processing [22, 58, 60] and experiment tracking [6, 74, 81].
いくつかの研究論文や企業が，データの前処理 [22，58，60]や実験の追跡 [6，74，81]など，ワークフローにおけるさまざまなタスクを実現するツールを提案している．
Crankshaw et al. studied the problem of model deployment and low-latency prediction serving [12].
Crankshaw らは、モデルの展開と低遅延予測サービングの問題を研究している[12].
With regards to validating changes in production systems, some researchers have studied CI (Continuous Integration) for ML and proposed preliminary solutions—for example, ease.ml
本番環境における変更の検証に関しては，MLのためのCI（Continuous Integration）を研究し，予備的な解決策を提案している研究者がいる-例えば ease.ml

MLOps Challenges.
MLOpsの課題
Sculley et al. were early proponents that production ML systems raise special challenges and can be hard to maintain over time, based on their experience at Google [64].
Sculleyらは、Googleでの経験に基づいて、プロダクションMLシステムは特別な課題を提起し、長期間にわたって維持することが困難であることを、早くから提唱していた[64].
Since then, several research projects have emerged to explore and tackle individual challenges in the MLOps workflow.
それ以来、MLOpsのワークフローにおける個々の課題を探求し、それに取り組むいくつかの研究プロジェクトが出現している.
For example, some discuss the need to manage data provenance and training context for model debugging purposes [8, 17, 24, 50].
例えば、モデルのデバッグのためにデータの出所とトレーニングのコンテキストを管理する必要性について議論しているものがある[8, 17, 24, 50].
Others describe the challenges of handling state and ensuring reproducibility (i.e., “managing messes”) while using computational notebooks [23, 42, 66].
また、計算ノートブックを使用しながら、状態の取り扱いと再現性の確保（すなわち、「混乱の管理」）の課題について述べているものもある[23, 42, 66].
Additionally, data distribution shifts have been technically but not operationally studied—i.e., how humans debug such shifts in practice [46, 51, 57, 71, 78].
さらに、データ分布のシフトは、技術的には研究されていますが、運用的には研究されていない. つまり、人間が実際にそのシフトをどのようにデバッグするかということである[46、51、57、71、78].
Rather than focus on a single pain point, Lee et al. analyze challenges across ML workflows on an open-source ML platform [36].
Leeらは、単一のペインポイントに焦点を当てるのではなく、オープンソースのMLプラットフォームにおけるMLワークフロー全体の課題を分析している[36].
Similarly, Xin et al. [79] analyze ML pipelines at Google to understand typical model configurations and retraining patterns.
同様に、Xinら[79]はGoogleのMLパイプラインを分析し、典型的なモデル構成と再トレーニングのパターンを理解している.
Polyzotis et al. [54, 55] survey challenges centric to data management for machine learning deployments.
Polyzotisら[54, 55]は、機械学習導入のためのデータ管理を中心とした課題を調査している.
Paleyes et al. review published reports of individual ML deployments and survey common challenges [52].
Paleyesらは、個々のML導入に関する公表されたレポートをレビューし、共通の課題を調査しています[52].
Our study instead focuses on issues across the production workflow (i.e., MLOps practices and challenges) as opposed to individual pain-points, identified by interviewing those who are are most affected by it—the ML engineers.
私たちの研究は、個々のペインポイントとは対照的に、生産ワークフロー全体の問題（すなわち、MLOpsの実践と課題）に焦点を当て、その影響を最も受ける人たち-MLエンジニアにインタビューすることで特定しました.

Data Science and ML-Related Interview Studies.
データサイエンスとMLに関連したインタビュー調査.
Kandel et al. [30] interview data analysts at enterprises, focusing on broader organizational contexts like we do; however, MLOps workflows and challenges extend beyond data analysis.
Kandelら[30]は企業のデータアナリストにインタビューし、我々のような広い組織のコンテキストに焦点を当てています. しかし、MLOpsのワークフローと課題はデータ分析にとどまりません.
Other studies build on Kandel et al.’s work, exploring aspects such as collaboration, code practices, and tools [32, 33, 49, 53, 82], all centered on general data analysis and data science, as opposed to transitioning workflows in ML to production.
他の研究はKandelらの研究を基に，コラボレーション，コードプラクティス，ツールなどの側面を調査している[32，33，49，53，82]が，MLのワークフローを生産に移行するとは異なり，一般的なデータ解析とデータサイエンスに重点を置いている．
Many ML-related interview studies focus on a single tool, task, or challenge in the workflow—for example, AutoML [75, 80], data iteration [25], model training [72], minimizing bias in ML models [26, 35, 43], and building infrastructure for ML pipelines [47].
ML関連の多くのインタビュー研究は、ワークフローにおける単一のツール、タスク、または課題に焦点を当てています. 例えば、AutoML [75, 80]、データ反復 [25]、モデルトレーニング [72]、MLモデルにおけるバイアスの最小化 [26, 35, 43] 、MLパイプラインのインフラ構築 [47] などがある.
Sambasivan et al. [62] study data quality issues during machine learning, as opposed to challenges in MLOps.
Sambasivanら[62]は、MLOpsの課題とは対照的に、機械学習中のデータ品質の問題を研究している.
Other ML-related interview studies focus on specific applications of ML, such as medicine [56], customer service [16], and interview processing [7].
他のML関連のインタビュー研究は，医療[56]，顧客サービス[16]，インタビュー処理[7]などのMLの特定のアプリケーションに焦点を当てている.
Some interview studies report on software engineering practices for ML development; however, they focus only on a few applications and primarily on engineering, not operational, challenges [5, 41].
また，ML開発におけるソフトウェア工学の実践を報告するインタビュー研究もある．しかし，それらはいくつかのアプリケーションにのみ焦点を当て，運用上の課題ではなく，主に工学的な課題に焦点を当てている[5, 41]．
Our interview study aims to be both broad and focused: we consider many applications and companies, but is centered around the engineers that perform MLOps tasks, with an eye towards highlighting both engineering and operational practices and challenges.
私たちのインタビュー調査は、広範かつ焦点を絞ることを目的としている. 多くのアプリケーションや企業を考慮しつつ、MLOpsタスクを実行するエンジニアを中心とし、エンジニアリングとオペレーションの両方の実践と課題を強調することを視野に入れています.
Additionally, our focus is on learning how models are deployed and sustained in production—we discover this by interviewing ML practitioners directly.
さらに、私たちの焦点は、ML実践者に直接インタビューすることで、モデルがどのようにプロダクションで展開され、維持されているかを学ぶことです.

# 3. Methods 3. 方法

Following review by our institution’s review board, we conducted an interview study of 18 ML Engineers (MLEs) working across a wide variety of sectors to learn more about their first-hand experiences serving and maintaining models in production.
私たちの機関の審査委員会の審査を経て、さまざまな分野で活躍する18人のMLエンジニア（MLE）にインタビュー調査を行い、実稼働中のモデルのサービスやメンテナンスの実体験を詳しく伺いました.

## 3.1. Participant Recruitment 3.1. 参加者の募集

We recruited persons who were responsible for the development, regular retraining, monitoring and deployment of any ML model in production.
このため、MLモデルの開発、定期的な再トレーニング、モニタリング、実運用への展開を担当する人を採用した.
A description of the 18 MLEs (22% female-identifying2 ) is shown in Table 1.
18 名の MLE（22%が女性2 ）について、表 1 に示す.
The MLEs we interviewed varied in their educational backgrounds, years of experience, roles, team size, and work sector.
インタビューしたMLEは、学歴、経験年数、役割、チームサイズ、業務部門など様々であった.
Recruitment was conducted in rounds over the course of an academic year (2021-2022).
採用は、1学年（2021～2022年）にわたりラウンド方式で行われた.
In each round, between three to five candidates were reached by email and invited to participate.
各ラウンドで、3人から5人の候補者に電子メールで連絡を取り、参加を呼びかけました.
We relied on our professional networks and open calls posted on MLOps channels in Discord3 , Slack4 , and Twitter to compile a roster of candidates.
候補者の名簿を作成するために、私たちの職業上のネットワークと、Discord3、Slack4、TwitterのMLOpsチャンネルに投稿された公募を利用しました.
The roster was incrementally updated roughly after every round of interviews, integrating information gained from the concurrent coding and analysis of transcripts (Section 3.3).
この名簿は、おおよそ面談のたびに更新され、同時進行のコーディングとトランスクリプトの分析（セクション 3.3）から得られた情報を統合していった。
Recruitment rounds were repeated until we reached saturation on our findings [48].
採用は，調査結果が飽和状態になるまで繰り返した [48]。

## 3.2. Interview Protocol 3.2. インタビュープロトコル

With each participant, we conducted semi-structured interviews over video call lasting 45 to 75 minutes each.
それぞれの参加者に対して、45分から75分のビデオ通話による半構造化インタビューを実施した。
Over the course of the interview, we asked descriptive, structural, and contrast questions abiding by ethnographic interview guidelines [68].
インタビューでは、エスノグラフィック・インタビュー・ガイドライン[68]に従って、記述的質問、構造的質問、対比的質問を行った。
The questions are listed in Appendix A.
質問は付録Aに記載されている。
Specifically, our questions spanned six categories: (1) the type of ML task(s) they work on; (2) the approach(es) they use for developing and experimenting on models; (3) how and when they transition from development
具体的には，(1) MLタスクの種類，(2) モデルの開発・実験に用いる手法，(3) 開発から実験への移行方法とその時期，(4)実験から実験への移行方法，(5)実験から実験への移行方法，(6)実験から実験への移行方法について質問させていただいた．

Participants received a written consent form before the interview, and agreed to participate free of compensation.
参加者はインタビューの前に同意書を受け取り、無償で参加することに同意した。
As per our agreement, we automatically transcribed the interviews using Zoom software.
合意に従って、我々はZoomソフトウェアを使用してインタビューを自動的に書き起こしました。
In the interest of privacy and confidentiality, we did not record audio or video of the interviews.
プライバシーと機密保持の観点から、インタビューの音声や映像は記録していません。
Transcripts were redacted of personally identifiable information before being uploaded to a secured drive in the cloud.
テープ起こしは、個人を特定できる情報を削除した上で、クラウド上の安全なドライブにアップロードされました。
More information about the transcripts can be found in Appendix B.
トランスクリプトの詳細については、付録Bをご覧ください。

## 3.3. Transcript COding & Analysis 3.3. トランスクリプトのCOと分析

Following a grounded theory approach [10, 70], we employed open and axial coding to analyze our transcripts.
グラウンデッド・セオリー・アプローチ[10, 70]に従い、オープン・コーディングとアキシャル・コーディングを採用し、トランスクリプトを分析した。
We used MaxQDA, a common qualitative analysis software package for coding and comparative analysis.
コーディングと比較分析には、一般的な質的分析ソフトウェアパッケージであるMaxQDAを使用した。
During a coding pass, two study personnel independently read interview transcripts closely to group passages into codes or categories.
コーディングパスでは、2人の研究担当者が独立してインタビュー原稿を精読し、文章をコードやカテゴリーにグループ分けした。
Coding passes were either top-down or bottom-up, meaning that codes were derived from theory or induced from interview passages, respectively.
コーディング・パスは、トップダウンまたはボトムアップで行われ、それぞれ、コードが理論から導かれるか、インタビュー文から誘発されることを意味する。
Between coding passes, study personnel met to discuss surprises and other findings, and following consensus, the code system was revised to reflect changes to the emerging theory.
コーディングパスの間に、研究担当者は、驚きやその他の発見について話し合うために会合し、コンセンサスが得られた後、出現した理論の変更を反映するためにコードシステムを修正した。
Coding passes were repeated until reaching convergence.
コーディングは、収束するまで繰り返された。
More information about the codes is shown in Appendix C, including a list of the most frequently occurring codes (Table 3) and co-occurring codes (Figure 4).
コードに関するより詳細な情報は、最も頻出するコードのリスト（表3）および共起するコード（図4）を含む付録Cに示されている。

# 4. Mlops Practices: Out Findings 4. MLopsの実践。 アウトファインディング

In this section, we present information about common practices in production ML deployments that we learned from the interviews.
本節では，インタビューから得られた本番用ML導入の共通事例に関する情報を紹介する．
First, we describe common tasks in the production ML workflow in Section 4.1.
まず、**4.1節で本番用MLワークフローにおける一般的なタスク**について説明する.
Next, we introduce the Three Vs of MLOps, grounding both the discussion of findings and the challenges that we will explain in Section 5.
次に、**MLOpsの3つのVs**を紹介し、セクション5で説明する知見や課題の根拠とする.
Then in Section 4.3, we describe the strategies ML engineers leverage to produce successful experiment ideas.
次にセクション4.3では、**MLエンジニアが実験のアイデアを成功させるために活用する戦略**について述べる.
In Section 4.4, we discuss organizational efforts to effectively evaluate models.
セクション4.4では、**モデルを効果的に評価するための組織的な取り組み**について述べる.
Finally, in Section 4.5, we investigate the hacks ML engineers use to sustain high performance in productions ML pipelines.
最後に、セクション4.5では、MLエンジニアが**プロダクションMLパイプラインで高いパフォーマンスを維持するために使用するハック**を調査する.

## 4.1. Tasks in the Production ML Lifecycle 4.1. プロダクションMLのライフサイクルにおけるタスク

We characterized ML engineers’ workflows into four high-level tasks, each of which employ a wide variety of tools.
MLエンジニアのワークフローを4つのハイレベルなタスクに分類し、それぞれで様々なツールを使用することを特徴とする.
We briefly describe each task in turn, and elaborate on them as they arise in our findings below.
各タスクについて簡単に説明し、以下で得られた知見について詳しく説明します.

### 4.1.1. Data Collection and Labeling.データ収集とラベリング。

Data collection spans sourcing new data, wrangling data from sources into a centralized repository, and cleaning data.
データ収集は、新しいデータの調達、ソースからのデータの一元化、およびデータのクリーニングに及びます。
Data labeling can be outsourced (e.g., Mechanical Turk) or performed in-house with teams of annotators.
データのラベリングは、外注（例：Mechanical Turk）することも、アノテーターのチームと社内で行うこともできる。
Since descriptions and interview studies of data collection, analysis, wrangling and labeling activities can be found in related papers [11, 29, 30, 62], we focus our summary of findings on the other three tasks.
データ収集、分析、ラングリング、ラベリングの各作業に関する説明やインタビュー調査は、関連論文 [11, 29, 30, 62] で見ることができるため、ここでは他の3つの作業に焦点を絞って調査結果をまとめる。

### 4.1.2. Feature Engineering and Model Experimentation. 特徴量エンジニアリングとモデル実験。

ML engineers typically focus on improving ML performance, measured via metrics such as accuracy or mean-squared-error.
MLエンジニアは通常、精度や平均二乗誤差のようなメトリクスで測定されるMLのパフォーマンスを向上させることに重点を置いています。
Experiments can be data-driven or model-driven; for example, an engineer can create a new feature or change the model architecture from tree-based to neural network-based.
実験にはデータ駆動型とモデル駆動型があります。例えば、エンジニアは新しい機能を作成したり、モデルのアーキテクチャをツリーベースからニューラルネットワークベースに変更したりすることができます。

### 4.1.3. Model Evaluation and Deployment. モデルの評価と配備

A model is typically evaluated by computing a metric (e.g., accuracy) over a collection of labeled data points hidden at training time, or a validation dataset, to see if its performance is better than what the currently-running production model achieved during its evaluation phase.
モデルの評価は、通常、トレーニング時に隠されたラベル付きデータポイントの集合、または検証データセットに対してメトリック（例えば精度）を計算し、現在実行中の本番モデルがその評価段階で達成した性能よりも優れているかどうかを確認することで行われます。
Deployment involves reviewing the proposed change, possibly staging the change to increasing percentages of the population, or A
展開では、提案された変更をレビューし、場合によっては、母集団のパーセンテージを増加させながら変更をステージングする、あるいはA

### 4.1.4. ML Pipeline Monitoring and Response. MLパイプラインのモニタリングとレスポンス。

Monitoring ML pipelines and responding to bugs involve tracking live metrics (via queries or dashboards), slicing and dicing sub-populations to investigate prediction quality, patching the model with non-ML heuristics for known failure modes, and finding in-the-wild failures and adding them to the evaluation set.
MLパイプラインのモニタリングとバグ対応には、（クエリーやダッシュボードによる）ライブメトリクスの追跡、予測品質を調査するためのサブ集団のスライスとダイシング、既知の故障モードに対する非MLヒューリスティックによるモデルのパッチ、および実環境での故障の発見と評価セットへの追加などが含まれます。

## 4.2. Three Vs of MLOps: Velocity, Validation, Versioning 4.2. MLOpsの3つのV：ベロシティ、バリデーション、バージョニング

When developing and pushing ML models to production, three properties of the workflow and infrastructure dictate how successful deployments will be:
MLモデルを開発し、本番環境に投入する場合、ワークフローとインフラの3つの特性がデプロイの成功を左右する.
Velocity, Validation, and Versioning, discussed in turn.
Velocity、Validation、Versioningについて順番に説明する.

### 4.2.1. Velocity. 速度.

Since ML is so experimental in nature, it’s important to be able to prototype and iterate on ideas quickly (e.g., go from a new idea to a trained model in a day).
MLは実験的な性格を持つため、**アイデアを素早くプロトタイプ化して反復できることが重要**である（例えば、新しいアイデアから1日で学習済みモデルまで到達させる）.
ML engineers attributed their productivity to development environments that prioritized high experimentation velocity and debugging environments that allowed them to test hypotheses quickly (P1, P3, P6, P10, P11, P14, P18).
MLエンジニアは、**高い実験速度を優先する開発環境**と、**仮説を素早く検証できるデバッグ環境**が生産性を高めたと述べている（P1、P3、P6、P10、P11、P14、P18）.

### 4.2.2. Validation. 検証.

Since errors become more expensive to handle when users see them, it’s good to test changes, prune bad ideas, and proactively monitor pipelines for bugs as early as possible (P1, P2, P5, P6, P7, P10, P14, P15, P18).
エラーがユーザーに見られると処理にコストがかかるので、できるだけ早い段階で変更をテストし、悪いアイデアを刈り込み、**パイプラインのバグを積極的に監視**するのがよい（P1、P2、P5、P6、P7、P10、P14、P15、P18).
P1 said:
P1 は次のように述べている.
“The general theme, as we moved up in maturity, is: how do you do more of the validation earlier, so the iteration cycle is faster?”
「成熟度が上がるにつれて、一般的なテーマは、**いかにしてより多くの検証を早期に行い、反復サイクルを高速化するか**ということである」.

### 4.2.3. Versioning. バージョン管理。

Since it’s impossible to anticipate all bugs before they occur, it’s helpful to store and manage multiple versions of production models and datasets for querying, debugging, and minimizing production pipeline downtime.
すべてのバグを事前に予測することは不可能なので、本番モデルとデータセットの複数のバージョンを保存・管理することは、クエリ、デバッグ、本番パイプラインのダウンタイムを最小限に抑えるために有効である.
ML engineers responded to buggy models in production by switching the model to a simpler, historical, or retrained version (P6, P8, P10, P14, P15, 18).
ML エンジニアは、**実運用環境でバグが発生した場合、モデルをよりシンプルなバージョン、履歴バージョン、または再トレーニングバージョンに切り替えて対応**している (P6, P8, P10, P14, P15, 18).

## 4.3. Machine Learning Engineering is Very Experimental, Even in Production 4.3. 機械学習エンジニアリングは、プロダクションでも非常に実験的である

ML engineering, as a discipline, is highly experimental and iterative in nature, especially compared to typical software engineering.
MLエンジニアリングは、一般的なソフトウェアエンジニアリングと比較して、非常に実験的で反復的な性質を持つ分野.
Contrary to popular negative sentiment around the large numbers of experiments and models that don’t make it to production, we found that it’s actually okay for experiments and models not to make it to production.
一般に、大量の実験やモデルが製品化されないという事はネガティブなイメージがある. しかし、私たちは、**実験やモデルが製品化されなくても構わない**ということを発見した.
What matters is making sure ideas can be prototyped and validated quickly—so that bad ones can be pruned away immediately.
重要なのは、**アイデアを素早くプロトタイプ化して検証し、悪いものはすぐに切り捨てること**である.
While there is no substitute for on-the-job experience to learn how to choose successful projects (P5), we document some self-reported strategies from our interviewees.
成功するプロジェクトの選び方（P5）を学ぶには、実地経験に勝るものはありませんが、インタビューに答えてくれた人たちの自己申告による戦略をいくつかご紹介する.

### 4.3.1. 4.3.1 Good project ideas start with collaborators. 4.3.1. 4.3.1 良いプロジェクトのアイデアは、協力者から始まる。

Project ideas, such as new features, came from or were validated early by domain experts, data scientists and analysts who had already performed a lot of exploratory data analysis.
新機能のようなプロジェクトのアイデアは、すでに多くの探索的データ分析を行っていたドメインエキスパート、データサイエンティスト、アナリストから生まれたり、早期に検証されたりしていた.
P14 and P17 independently recounted successful project ideas that came from asynchronous conversations on Slack:
P14とP17は、**Slack上の非同期な会話から生まれたプロジェクトの成功例**を独自に語っている.
P17 said, “I look for features from data scientists, [who have ideas of] things that are correlated with what I’m trying to predict.”
P17は、"私はデータサイエンティストから機能を探す."私が予測しようとしているものと相関しているものについてのアイデアを持っている.
Solely relying on other collaborators wasn’t enough, though—P5 mentioned that they “still need to be pretty proactive about what to search for.”
しかし、他の協力者に頼るばかりでは不十分で、P5は「何を探すかについて、まだかなり積極的になる必要がある」と述べている.

Some organizations explicitly prioritized cross-team collaboration as part of their culture.
**チーム横断的なコラボレーションを文化として明確に優先している組織**もあった.
P11 said:
P11 はこう言っています。

- We really think it’s important to bridge that gap between what’s often, you know, a [subject matter expert] in one room annotating and then handing things over the wire to a data scientist—a scene where you have no communication. So we make sure there’s both data science and subject matter expertise representation [on our teams]. ある部屋で専門家がアノテーションを行い、それをデータサイエンティストに引き継ぐというような、**コミュニケーションのない現場とのギャップを埋めることが重要だ**と考えている. ですから、**私たちのチームにはデータサイエンスと専門知識の両方が存在するようにしている**.
  To foster a more collaborative culture, P16 discussed the concept of “building goodwill” with other teams through tedious tasks that weren’t always explicitly a part of company plans:
  P16は、より協力的な文化を醸成するために、会社の計画には必ずしも明示されていない面倒な仕事を通じて、他のチームと「親善を深める」というコンセプトを打ち出した.

- Sometimes we’ll fix something [here and] there to like build some good goodwill, so that we can call on them in the future...I do this stuff as I have to do it, not because I’m really passionate about doing it. 時には、将来、彼らに声をかけることができるよう、好意を持ってもらうために、あちこちを修理することもあります...私は、本当に情熱を持ってやっているわけではなく、やらなければならないこととしてやっている.

### 4.3.2. 4.3.2 Iterate on the data, not necessarily the model. 4.3.2. 4.3.2 必ずしもモデルではなく、データに対して反復する。

Several participants recommended focusing on experiments that provide additional context to the model, typically via new features (P5, P6, P11, P12, P14, P16, P17, P18, P19).
何人かの参加者は、典型的には新機能によってモデルに追加のコンテキストを提供する実験に焦点を当てることを推奨した（P5, P6, P11, P12, P14, P16, P17, P18, P19）.
P17 mentioned that most ML projects at their organization centered around adding new features.
P17は、組織内のほとんどのMLプロジェクトが新機能の追加を中心にしていると述べた.
P14 mentioned that one of their current projects was to move feature engineering pipelines from Scala to SparkSQL (a language more familiar to ML engineers and data scientists), so experiment ideas could be coded and validated faster.
P14は、現在のプロジェクトの1つは、機能エンジニアリングパイプラインをScalaからSparkSQL（MLエンジニアやデータ科学者に馴染みのある言語）に移行し、実験のアイデアをより速くコード化し、検証できるようにすることであると述べた.
P11 noted that iterating on the data, not the model, was preferable because it resulted in faster velocity:
P11 は、**モデルではなくデータで反復することが、より速い速度につながるため好ましい**と述べている.

- I’m gonna start with a [fixed] model because it means faster [iterations]. And often, like most of the time empirically, it’s gonna be something in our data that we can use to kind of push the boundary...obviously it’s not like a dogmatic We Will Never Touch The Model, but it shouldn’t be our first move. 私は、「固定」モデルから始めることにしている. 経験的に、ほとんどの場合、境界を押し広げるために使えるデータの何かがあるはずです...もちろん、独断で「モデルには絶対に触れない」と決めているわけではないが、それが最初の行動であるべきではない.

Prior work has also identified the importance of data work [62].
先行研究でも、データ作業の重要性が指摘されている[62].

### 4.3.3. Account for diminishing returns. 4.3.3. 収穫逓減を考慮する

At many organizations (especially larger companies), deployment can occur in stages—i.e., first validated offline, then deployed to 1% of production traffic, then validated again before a deployment to larger percentages of traffic.
多くの組織 (特に大企業) では，**まずオフラインで検証し，次に本番トラフィックの 1%に展開し，さらに大きな割合のトラフィックに展開する前に再度検証するといったように，段階的な展開が行われる**ことがある．
Some interviewees (P5, P6, P18) explained that experiment ideas typically have diminishing performance gains in later stages of deployment.
インタビューに答えてくれた人たち（P5、P6、P18）は、**実験のアイデアは、通常、展開の後半になると性能向上が鈍化**すると説明している.
As a result, P18 mentioned that they would initially try multiple ideas but focus only on ideas with the largest performance gains in the earliest stage of deployment; they emphasized the importance of “validat[ing] ideas offline...[to make] productivity higher.”
その結果，P18 は，最初は複数のアイデアを試してみるが，**展開の初期段階で最も大きな性能向上が得られるアイデアのみに焦点を絞る**と述べ，「オフラインでアイデアを検証し...（生産性を）高める」ことの重要性を強調している．
P19 corroborated this by saying end-to-end staged deployments could take several months, making it a high priority to kill ideas with minimal gain in early stages to avoid wasting future time.
P19はこれを裏付けるように、エンドツーエンドの段階的デプロイメントには数ヶ月かかることがあり、将来の時間を無駄にしないために、**初期段階で最小限の利益しか得られないアイデアを潰すことが優先される**、と述べている.
Additionally, to help with validating early, many engineers discussed the importance of a sandbox for stress-testing their ideas (P1, P5, P6, P11, P12, P13, P14, P15, P17, P18, P19).
さらに、早期検証のために、多くのエンジニアが、アイデアをストレステストするためのサンドボックスの重要性について議論しました（P1、P5、P6、P11、P12、P13、P14、P15、P17、P18、P19）.
For some engineers, this was a single Jupyter notebook; others’ organizations had separate sandbox environments to load production models and run ad-hoc queries.
あるエンジニアにとっては、これは単一のJupyterノートブックでしたが、他のエンジニアの組織では、本番モデルをロードし、アドホッククエリを実行するための別のサンドボックス環境を持っていた.

### 4.3.4. Small changes are preferable to larger changes. 4.3.4. 大きな変更より小さな変更が望ましい。

In line with software best practices, interviewees discussed keeping their code changes as small as possible for multiple reasons, including faster code review, easier validation, and fewer merge conflicts (P2, P5, P6, P10, P11, P18, P19).
ソフトウェアのベストプラクティスに沿って、インタビューに応じた人々は、コードレビューの迅速化、検証の容易化、マージの競合の減少など、複数の理由から、**コードの変更をできるだけ小さくすること**を議論した (P2, P5, P6, P10, P11, P18, P19).
Additionally, changes in large organizations were primarily made in config files instead of main application code (P1, P2, P5, P10, P12, P19).
さらに、**大規模な組織における変更は、主にメインアプリケーションのコードではなく、設定ファイルで行われた** (P1、P2、P5、P10、P12、P19).
For example, instead of editing parameters directly in a Python model training script, it was preferable to edit a config file (e.g., JSON or YAML) of parameters instead and link the config file to the model training script.
例えば、Pythonのモデル学習スクリプトで直接パラメータを編集するのではなく、**代わりにパラメータの設定ファイル（JSONやYAMLなど）を編集し**、その設定ファイルをモデル学習スクリプトにリンクすることが望ましいとされた. (user-data.zipやitem-data.zipの生成処理で使えないかな...! methodの指定方法とか、user_idの範囲とか?)

P19 described how, as their team matured, they edited the model code less:
P19は、彼らのチームが成熟するにつれて、モデルコードの編集が少なくなっていったことを説明した.
“Eventually it was the [DAG] pipeline code which changed more...there was no reason to touch the [model] code...everything is config-based.”
「最終的には[DAG]パイプラインのコードがより変更されました...モデルコードに触れる理由はありませんでした...すべては設定ベースである.
P5 mentioned that several of their experiments involved “[taking] an existing model, modify[ing] [the config] with some changes, and deploying it within an existing training cluster.”
P5は、彼らの実験のいくつかは、"[既存の]モデルを取り、いくつかの変更で[設定]を修正し、既存のトレーニングクラスタ内でそれをデプロイする "ことを含んでいると述べた.
Supporting a config-driven development was important, P1 said, otherwise bugs might arise when promoting the experiment idea to production:
P1は、**config-drivenの開発をサポートすることが重要であり、そうでなければ、実験のアイデアを本番に進める際にバグが発生する可能性がある**と述べている.

- People might forget to, when they spawn multiple processes, to do data loading in parallel, they might forget to set different random seeds, especially [things] you have to do explicitly many times...you’re talking a lot about these small, small things you’re not going to be able to catch [at deployment time] and then of course you won’t have the expected performance in production. 複数のプロセスを起動し、並行してデータをロードする際に、異なる乱数種を設定することを忘れるかもしれない. 特に、明示的に何度も行わなければならないことについては、このように小さな、小さなことをたくさん話していると、（デプロイ時に）キャッチできなくなり、当然、本番では期待通りのパフォーマンスが得られない.

Because ML experimentation requires many considerations to yield correct results—e.g., setting random seeds, accessing the same versions of code libraries and data—constraining engineers to configonly changes can reduce the number of bugs.
MLの実験では、ランダムな種の設定、同じバージョンのコードライブラリやデータへのアクセスなど、正しい結果を得るために多くの配慮が必要なため、エンジニアが設定変更のみを行うように制限することで、バグの数を減らすことができる.

## 4.4. Operationalizing Model Evaluation is an Active Effort 4.4. モデル評価の運用は積極的な努力で

We found that MLEs described intensive model evaluation efforts at their companies to keep up with data changes, product and business requirement changes, user changes, and organizational changes.
MLE は、データの変更、製品およびビジネス要件の変更、ユーザーの変更、組織の変更に対応するため、各社で集中的にモデル評価を行っていることを説明した.
The goal of model evaluation is to prevent repeated failures and bad models from making it to production while maintaining velocity— i.e., the ability for pipelines to quickly adapt to change.
モデル評価の目的は、失敗を繰り返したり、悪いモデルが本番稼動するのを防ぐと同時に、パイプラインが変化に迅速に対応する能力を維持することである.

### 4.4.1. Validation datasets should be dynamic. 4.4.1. 検証用データセットは動的であるべきである

Many engineers reported processes to analyze live failure modes and update the validation datasets to prevent similar failures from happening again (P1, P2, P5, P6, P8, P11, P15, P16, P17, P18).
多くのエンジニアが，**実際に発生した故障モードを分析し，同様の故障が再び発生しないように検証データセットを更新するプロセス(??)**を報告している（P1, P2, P5, P6, P8, P11, P15, P16, P17, P18）．
P1 described this process as a departure from what they had learned in academia:
P1は、このプロセスを、彼らがアカデミアで学んだことからの逸脱であると述べている.
“You have this classic issue where most researchers are evaluat[ing] against fixed data sets...[but] most industry methods change their datasets.”
「**ほとんどの研究者は固定されたデータセットに対して評価を行っているが，産業界の手法ではデータセットを変更することが多いのである**」.
We found that these dynamic validation sets served two purposes:
この動的検証セットには、2つの目的があることがわかった:

- (1) the obvious goal of making sure the validation set reflects live data as much as possible, given new learnings about the problem and shifts in the aggregate data distribution, (1）問題についての新たな学習や総データ分布の変化を考慮し、**検証セットが実際のデータを可能な限り反映するようにする**という明白な目標
- (2) the more subtle goal of addressing localized shifts that subpopulations may experience (e.g., low accuracy for a specific label).（2）部分集団が経験する局所的な変化（例えば、特定のラベルに対する精度が低いなど）に対処するというより繊細な目標.

The challenge with (2) is that many subpopulations are typically unforeseen; many times they are discovered post-deployment.
(2)の課題は、**多くのサブ集団が通常予見できないものであり、多くの場合、展開後に発見されること**である.
To enumerate them, P11 discussed how they systematically bucketed their data points based on the model’s error and created validation sets for each underperforming bucket:
これらを列挙するために、P11は、モデルの誤差に基づいてデータポイントを体系的にバケット化し、**パフォーマンスが低いバケットごとに検証セットを作成した方法**について述べた.

- Some [of the metrics in my tool] are standard, like a confusion matrix, but it’s not really effective because it doesn’t drill things down [into specific subpopulations that users care about]. Slices are user-defined, but sometimes it’s a little bit more automated. [During offline evaluation, we] find the error bucket that [we] want to drill down, and then [we] either improve the model in very systematic ways or improve [our] data in very systematic ways. 私のツールの測定基準には）混乱マトリックスのような標準的なものもありますが、（ユーザーが気にする特定の部分集団に）掘り下げることができないので、あまり効果的ではありません。 スライスはユーザーが定義するものですが、もう少し自動化されている場合もあります。 [オフライン評価では、ドリルダウンしたいエラーのバケットを見つけ、非常に体系的な方法でモデルを改善するか、非常に体系的な方法でデータを改善します。

Rather than follow an anticipatory approach of constructing different failure modes in the offline validation phase—e.g., performance drops in subpopulations users might care deeply about—like P11 did, P8 offered a reactive strategy of spawning a new dataset for each observed live failure:
P11 のように、オフラインの検証段階でさまざまな失敗モードを構築するという予測的なアプローチではなく、P8 は、観察されたライブの失敗ごとに新しいデータセットを生成するという反応的な戦略を提案しました。
“Every [failed prediction] gets into the same queue, and 3 of us sit down once a week and go through the queue...then our [analysts] collect more [similar] data.”
「すべての[失敗した予測]は同じキューに入れられ、週に一度、3人でそのキューを調べます...そして、私たち[アナリスト]はさらに[類似した]データを集めます。
This new dataset was then used in the offline validation phase in future iterations of the production ML lifecycle.
この新しいデータセットは、プロダクションMLライフサイクルの将来の反復におけるオフラインの検証フェーズで使用されました。

While processes to dynamically update the validation datasets ranged from human-in-the-loop to frequent synthetic data construction (P6), we found that higher-stakes applications of ML (e.g., autonomous vehicles), created separate teams to manage the dynamic evaluation process.
検証データセットを動的に更新するプロセスは、人間がループに参加するものから、頻繁に合成データを構築するもの（P6）まで様々ですが、より利害関係の強いMLのアプリケーション（例えば、自律走行車）では、動的な評価プロセスを管理する別のチームを作っていることがわかりました。
P1 said:
とP1が言っています。

- We had to move away from only aggregate metrics like MAP towards the ability to curate scenarios of interest, and then validate model performance on them specifically. So, as an example, you can’t hit pedestrians, right. You can’t hit cyclists. You need to work in roundabouts. You have a base layer of ML performance and the performance is not perfect...what you need to be able to do in a mature MLOps pipeline is go very quickly from user recorded bug, to not only are you going to fix it, but you also have to be able to drive improvements to the stack by changing your data based on those bugs. MAPのような集計的な指標だけでなく、関心のあるシナリオをキュレーションし、それに対するモデルのパフォーマンスを具体的に検証することが必要でした。 たとえば、歩行者をはねることはできませんよね。 自転車にもぶつけることはできません。 ラウンドアバウトで動作させる必要があります。 成熟したMLOpsパイプラインで必要なのは、ユーザーが記録したバグから、それを修正するだけでなく、そのバグに基づいてデータを変更し、スタックの改善を推進することまで、非常に迅速に行うことです。

Although the dynamic evaluation process might require many humans in the loop—a seemingly intense organizational effort— engineers thought it was crucial to have.
動的評価プロセスは、多くの人間をループさせる必要があり、一見、組織的な努力のように見えるが、技術者はそれが重要だと考えていた。
When asked why they invested a lot of energy into their dynamic process, P11 said:
なぜ、動的なプロセスに多くのエネルギーを費やしたのか、P11はこう答えた。
“I guess it was always a design principle—the data is [always] changing.”
「データは常に変化するものである、という設計思想があったからです」。

### 4.4.2. Validation systems should be standardized. 4.4.2. バリデーションシステムを標準化すること。

The dynamic nature of validation processes makes it hard to effectively maintain versions of such processes, motivating efforts to standardize them.
検証プロセスの動的な性質は、そのようなプロセスのバージョンを効果的に維持することを困難にし、それらを標準化するための努力を動機づけるものである。
Several participants recalled instances of bugs stemming from inconsistent definitions of successful validation—i.e., where different engineers on their team evaluated models differently, causing unexpected changes to live performance metrics (P1, P3, P4, P5, P6, P7, P17).
何人かの参加者は、検証の成功の定義が一貫していないことに起因するバグの事例、つまり、チーム内の異なるエンジニアが異なる方法でモデルを評価し、実際のパフォーマンス指標に予期せぬ変更をもたらした事例を思い出しました (P1, P3, P4, P5, P6, P7, P17)．
For instance, P4 lamented that every engineer working on a particular model had a cloned version of the main evaluation notebook, with a few changes.
例えば，P4 は，特定のモデルに携わるすべてのエンジニ アが，主要な評価用ノートを少し変更しただけのクローン 版を持っていることを嘆いています．
The inconsistent requirements for promoting a model to production caused headaches while monitoring and debugging, so their company instated a new effort to standardize evaluation scripts.
そこで、評価用ノートを標準化することにしたのです。

Although other MLOps practices highlighted the synergy between velocity and validating early (Section 4.3.3), we found that standardizing the validation system exposed a tension between velocity (i.e., being able to promote models quickly) and validating early, or eliminating the possibility of some bugs at deployment time.
他の MLOps プラクティスでは、ベロシティと早期検証の相乗効果が強調されていますが（セクション 4.3.3 ）、検証システムを標準化すると、ベロシティ（すなわち、モデルを迅速に推進できる）と早期検証、つまり導入時に一部のバグの可能性を排除することの間に緊張関係が生じることがわかっています。
Since many validation systems needed to frequently change, as previously discussed, turnaround times for code review and merges to the main branch often could not keep up with the new tests and collections of data points added to the validation system.
多くの検証システムは頻繁に変更される必要があるため、前述したように、コードレビューやメインブランチへのマージのターンアラウンドタイムが、検証システムに追加される新しいテストやデータポイントのコレクションに追いつかないことがよくありました。
So, it was easier for engineers to fork and modify the evaluation system.
そこで、エンジニアが評価システムをフォークして修正することが容易になった。
However, P2 discussed that the decrease in velocity was worth it for their organization when they standardized evaluation:
しかし、P2 は、評価を標準化したときに速度が低下したことは、組織にとって価値があったと述べています。

- We have guidelines on how to run eval[uation] comprehensively when any particular change is being made. Now there is a merge queue, and we have to make sure that we process the merge queue in order, and that improvements are actually also reflected in subsequent models, so it requires some coordination. We’d much rather gate deploying a model than deploy a model that’s bad. So we tend to be pretty conservative [now]. 特定の変更があった場合に、どのように総合的に評価するかというガイドラインがあります。 現在ではマージキューがあり、マージキューを順番に処理し、改善が後続のモデルにも実際に反映されていることを確認しなければならないので、ある程度の調整が必要です。 私たちは、悪いモデルをデプロイするよりも、むしろモデルのデプロイに失敗することを望んでいます。 ですから、（現在は）かなり保守的になる傾向があります。

A standardized evaluation system also reduced friction in deploying ML in large companies and high-stakes settings.
標準化された評価システムは、大企業や利害関係の強い環境でMLを展開する際の摩擦を減らすことにもなります。
P5 discussed that for some models, deployments needed approvals across the organization, and it was much harder to justify a deployment with a custom or ad-hoc evaluation process:
P5は、モデルによっては、導入には組織全体の承認が必要であり、カスタムまたはアドホックな評価プロセスでは、導入を正当化することがはるかに困難であることを議論しました。
“At the end of the day, it’s all a business-driven decision...for something that has so much revenue riding on it, [you can’t have] a subjective opinion on whether [your] model is better.”
「結局のところ、それはすべてビジネス主導の決定です...多くの収益がかかっているものについては、（あなたの）モデルが優れているかどうかについての主観的な意見を持つことはできません。

### 4.4.3. Spread a deployment across multiple stages, and evaluate at each stage. 4.4.3. 複数のステージに展開し、各ステージで評価する。

Several organizations, particularly those with many customers, had a multi-stage deployment process for new models or model changes, progressively evaluating at each stage (P3, P5, P6, P7, P8, P12, P15, P17, P18, P19).
いくつかの組織、特に多数の顧客を持つ組織では、新モデルやモデルチェンジのために、多段階の展開プロセスを持ち、各段階で段階的に評価を行っていた（P3、P5、P6、P7、P8、P12、P15、P17、P18、P19)。
P6 described the staged deployment process as:
P6 は、段階的な展開プロセスを次のように説明している。

- In [the large companies I’ve worked at], when we deploy code it goes through what’s called a staged deployment process, where we have designated test clusters, [stage 1] clusters, [stage 2] clusters, then the global deployment [to all users]. The idea here is you deploy increasingly along these clusters, so that you catch problems before they’ve met customers. 私が働いてきた大企業では、コードをデプロイする際に、テストクラスタ、[ステージ1]クラスタ、[ステージ2]クラスタ、そして[全ユーザーへの]グローバルデプロイという、いわゆる段階的なデプロイメントプロセスを経ています。 このクラスタに沿ってどんどんデプロイしていくことで、顧客に迷惑をかける前に問題をキャッチするという考え方です。

Each organization had different names for its stages (e.g., test, dev, canary, staging, shadow, A
各組織では、ステージの名称が異なっていた（例：test、dev、canary、staging、shadow、A

We spent a long time very slowly, ramping up the model to very small percentages of traffic and watching what happened.
私たちは長い時間をかけて、非常にゆっくりと、トラフィックのごく小さな割合でモデルを増強し、何が起こるかを観察しました。
[When there was a failure mode,] a product person would ping us and say: hey, this was kind of weird, should we create a rule around this [suggested text] to filter this out?
[失敗モードが発生すると、製品担当者が私たちにこう言うのです。「ちょっと変なんだけど、このテキストを除外するルールを作ろうか？

Of particular note was one type of stage, the shadow stage— where predictions were generated live but not surfaced to users, that came before a deployment to a small fraction of live users.
特に注目すべきは、シャドーステージと呼ばれるステージです。シャドーステージでは、予測はライブで作成されますが、ユーザーには公開されず、ごく一部のライブユーザーへのデプロイメントの前に行われます。
P14 described how they used the shadow stage to assess how impactful new features could be:
P14は、新機能のインパクトの大きさを評価するために、シャドーステージをどのように使用したかを説明しました。

So if we’re testing out a new idea and want to see, what would the impact be for this new set of features without actually deploying that into production, we can deploy that in a type of shadow mode where it’s running alongside the production model and making predictions.
ですから、新しいアイデアをテストして、実際に本番環境に導入することなく、この新しい機能のセットがどのような影響を及ぼすかを確認したい場合、シャドーモードのような形で導入して、本番モデルと並行して動作させ、予測を行うことができるのです。
We track all the metrics for [both] models in [our data lake]...so we can compare them easily.
データレイクでは、両モデルのすべての指標をトラッキングしているので、簡単に比較することができます。

Shadow mode had other use cases—for instance, P15 discussed how shadow mode was used to convince other stakeholders (e.g., product managers, business analysts) that a new model or change to an existing model was worth putting in production.
例えば、P15は、新しいモデルや既存のモデルの変更が生産に移す価値があることを他の利害関係者（プロダクトマネージャやビジネスアナリストなど）に納得させるためにシャドウモードを使用する方法について述べています。
P19 mentioned that they use shadow mode to invalidate experiment ideas that would eventually fail.
P19 は、最終的に失敗するであろう実験のアイデアを無効にするためにシャドウモードを使用することを述べています。
But shadow mode alone wasn’t a substitute for all stages of deployment—P6 said, “[in the early stage], we don’t have a good sample of how the model is going to behave in production”—requiring the multiple stages.
しかし、シャドーモードだけでは、展開のすべての段階を代替することはできません。「（初期段階では）本番環境でモデルがどのように動作するかの良いサンプルがない」ため、複数の段階が必要になります。
Additionally, in products that have a feedback loop (e.g., recommender systems), it is impossible to evaluate the model in shadow mode because users do not interact with shadow predictions.
さらに、フィードバックループを持つ製品（レコメンダーシステムなど）では、ユーザーがシャドウ予測と対話することがないため、シャドウモードでモデルを評価することは不可能です。

### 4.4.4. ML evaluation metrics should be tied to product metrics. 4.4.4. ML評価指標は、製品指標と関連付けるべきである。

Multiple participants stressed the importance of evaluating metrics critical to the product, such as click-through rate or user churn rate, rather than ML-specific metrics alone like MAP (P5, P7, P15, P16, P11, P17, P18, P19).
複数の参加者が、MAP のような ML 固有の指標だけでなく、クリックスルー率やユーザー解約率など、製品にとって重要な指標を評価することの重要性を強調した (P5, P7, P15, P16, P11, P17, P18, P19)．
The need to evaluate product-critical metrics stemmed from close collaboration with other stakeholders, such as product managers and business operators.
プロダクトクリティカルな指標を評価する必要性は、プロダクトマネージャーやビジネスオペレーターなど、他のステークホルダーとの密接な連携から生まれたものである。
P11 felt that a key reason many ML projects fail is that they don’t measure metrics that will yield the organization value:
P11は、多くのMLプロジェクトが失敗する主な理由は、組織の価値をもたらす指標を測定していないことだと感じていた。

Tying [model performance] to the business’s KPIs (key performance indicators) is really important.
モデルのパフォーマンスをビジネスのKPI（重要業績評価指標）に関連付けることは、本当に重要です。
But it’s a process—you need to figure out what [the KPIs] are, and frankly I think that’s how people should be doing AI.
しかし、それはプロセスであり、何が（KPIなのか）理解する必要があります。そして、率直に言って、これこそ人々がAIを行うべき方法だと思います。
It [shouldn’t be] like: hey, let’s do these experiments and get cool numbers and show off these nice precision-recall curves to our bosses and call it a day.
実験をやって、かっこいい数字を出して、上司に精度と想起曲線の美しさを見せびらかしたら終わり、みたいなやり方ではいけないと思います。
It should be like: hey, let’s actually show the same business metrics that everyone else is held accountable to to our bosses at the end of the day.
一日の終わりに、他の誰もが責任を負っているのと同じビジネス指標を実際に上司に見せよう、というようなものであるべきです。

Since product-specific metrics are, by definition, different for different ML models, it was important for engineers to treat choosing the metrics as an explicit step in their workflow and align with other stakeholders to make sure the right metrics were chosen.
製品固有のメトリクスは、定義上、異なるMLモデルで異なるため、エンジニアはメトリクスを選択することをワークフローの明確なステップとして扱い、正しいメトリクスが選択されるように他のステークホルダーと連携することが重要だったのです。
For example, P16 said that for every new ML project they work on, their “first task is to figure out, what are customers actually interested in, or what’s the metric that they care about.”
例えば、P16は、新しいMLプロジェクトに取り組むたびに、「最初のタスクは、顧客が実際に何に興味を持っているのか、または彼らが気にするメトリクスは何なのかを把握すること」だと述べています。
P17 said that every model change in production is validated by the product team:
P17は、生産中のすべてのモデル変更は、製品チームによって検証されると述べました。
“if we can get a statistically significant greater percentage [of] people to subscribe to [the product], then [we can fully deploy].”
「統計的に有意な割合の人々が（製品を）購入することができれば、（完全に）導入することができるのです。

For some organizations, a consequence of tightly coupling evaluation to product metrics was an additional emphasis on important customers during evaluation (P6, P10).
一部の組織では、評価を製品指標と密接に関連付けた結果、評価時に重要な顧客をさらに重視するようになった (P6, P10)。
P6 described how, at their company, experimental changes that increased aggregate metrics could sometimes be prevented from going to production:
P6 は、自社では、総計指標を向上させる実験的な変更が、時には生産に移されなくなることがあると 述べている。

There’s an [ML] system to allocate resources for [our product].
自社製品】のリソースを割り当てる【ML】の仕組みがある。
We have hard-coded rules for mission critical customers.
ミッションクリティカルな顧客に対しては、ハードコーディングされたルールがあります。
Like at the beginning of Covid, there were hospital [customers] that we had to save [resources] for.
例えば、コヴィッドの最初の頃は、病院の顧客のためにリソースを節約しなければなりませんでした。

Participants who came from research or academia noted that tying evaluation to the product metrics was a different experience.
研究機関や大学から来た参加者は、評価を製品の評価指標に結びつけることは、異なる経験であると述べています。
P6 commented:
P6がコメントした。

I think about where the business will benefit from what we’re building.
私たちが作るものが、ビジネスのどこに利益をもたらすかを考えます。
We’re not just shipping off fake wins, like we’re really in the value business.
私たちは、偽りの勝利だけを出荷しているわけではなく、本当に価値のあるビジネスをしているのです。
You’ve got to see value from AI in your organization in order to feel like [our product] was worth it to you, and I guess that’s a mindset that we really ought to have [as a broader community].
私たちの製品が）あなたにとって価値があったと感じるためには、あなたの組織でAIから価値を見出さなければなりません。そして、それは（より広いコミュニティとして）私たちが本当に持つべき考え方なのだと思います。

## 4.5. Sustaining Models Requires Deliberate Software Engineering and Organizational Practices 4.5. モデルを維持するには、熟慮されたソフトウェアエンジニアリングと組織的な実践が必要である

Here, we present a list of strategies ML engineers employed during monitoring and debugging phases to sustain model performance post-deployment.
ここでは、MLエンジニアがモニタリングとデバッグの段階で採用した、デプロイ後のモデル性能を維持するための戦略を紹介します。

### 4.5.1. Create new versions: frequently retrain on and label live data. 4.5.1. 新しいバージョンを作成する：頻繁にライブデータで再トレーニングし、ラベルを付ける。

Production ML bugs can be detected by tracking pipeline performance, measured by metrics like prediction accuracy, and triggering an alert if there is a drop in performance that exceeds some predefined threshold.
本番環境でのMLバグは，パイプラインの性能を予測精度などの指標で追跡し，あらかじめ定義された閾値を超える性能低下があった場合に警告を発することで検知することができる．
On-call ML engineers noted that reacting to an ML-related bug in production often took a long time, motivating them to find alternative strategies to quickly restore performance (P1, P7, P8, P10, P14, P15, P17, P19).
オンコールのMLエンジニアは、本番環境でML関連のバグに対応するのに長い時間がかかることが多いため、パフォーマンスを迅速に回復するための代替戦略を見つける動機付けになったと述べています（P1、P7、P8、P10、P14、P15、P17、P19）。
P14 mentioned automatically retraining the model every day so model performance would not suffer for longer than a day:
P14は、モデルのパフォーマンスが1日以上低下しないように、毎日自動的にモデルを再トレーニングすることに言及しています。

Why did we start training daily?
なぜ、毎日トレーニングを行うようにしたのですか？
As far as I’m aware, we wanted to start simple—we could just have a single batch job that processes new data and we wouldn’t need to worry about separate retraining schedules.
私の知る限り、新しいデータを処理するバッチジョブを1つ用意するだけで、再トレーニングのスケジュールを個別に心配する必要がないため、シンプルに始めたかったのです。
You don’t really need to worry about if your model has gone stale if you’re retraining it every day.
毎日再トレーニングしていれば、モデルが古くなったかどうかを心配する必要はありません。

Retraining cadences ranged from hourly (P18) to every few months (P17) and were different for different models within the same organization (P1).
再教育の周期は、1時間ごと（P18）から数ヶ月ごと（P17）まであり、同じ組織内でも機種ごとに異なっていた（P1）。
None of the participants interviewed reported any scientific procedure for determining the cadence; the retraining cadences were set in a way that streamlined operations for the organization in the easiest way.
どの参加者も、再研修の頻度を決定するための科学的な手順を報告しておらず、再研修の頻度は、組織の業務を最も効率化できる方法で設定されていました。
For example, P18 mentioned that “retraining takes about 3 to 4 hours, so [they] matched the cadence with it such that as soon as [they] finished any one model, they kicked off the next training [job].”
例えば、P18は、「再トレーニングには3～4時間かかるので、一つのモデルが終わるとすぐに次のトレーニング（仕事）を開始するように、ケイデンスを合わせている」と述べています。

Some engineers reported an inability to retrain unless they had freshly labeled data, motivating their organizations to set up a team to frequently label live data (P1, P8, P10, P11, P16).
一部の技術者は、ラベル付けされたばかりのデータがないと再トレーニングができないことを報告し、そのため、組織内で頻繁に生データにラベル付けするチームを立ち上げたと述べている（P1、P8、P10、P11、P16）。
P10 reported that a group within their company periodically collected new documents for their language models to fine-tune on.
P10は、社内のあるグループが定期的に新しい文書を収集し、言語モデルの微調整を行っていると報告しています。
P11 mentioned an inhouse team of junior analysts to annotate the data; however, a problem was that these annotations frequently conflicted and the organization did not know how to reconcile the noise.
P11は、社内の若手アナリストのチームがデータにアノテーションを付けていると述べていますが、問題は、これらのアノテーションが頻繁に衝突し、組織としてノイズを調整する方法を知らないということでした。

### 4.5.2. Maintain old versions as fallback models. 4.5.2. 旧バージョンをフォールバックモデルとして維持する。

Another way to minimize downtime when a model is known to be broken is to have a fallback model to revert to—either an old version or simple version.
モデルが壊れていることが分かっているときのダウンタイムを最小限に抑えるもう一つの方法は、古いバージョンやシンプルなバージョンのどちらかに戻すためのフォールバックモデルを用意することです。
P19 said:
P19はこう言っています。
“if the production model drops and the calibration model is still performing within a [specified] range, we’ll fall back to the calibration model until someone will fix the production model.”
"本番モデルがダウンして、キャリブレーションモデルがまだ[指定した]範囲内で機能している場合、誰かが本番モデルを修正するまで、キャリブレーションモデルにフォールバックします"。
P18 mentioned that it was important to keep some model up and running, even if they “switched to a less economic model and had to just cut the losses.”
P18は、"経済性の低いモデルに切り替えて、ただ損切りするしかない "としても、何らかのモデルを稼働させ続けることが重要であると述べています。

### 4.5.3. Maintain layers of heuristics. 4.5.3. ヒューリスティックのレイヤーを維持する。

P14 and P15 each discussed how their models are augmented with a final, rule-based layer to keep live predictions more stable.
P14とP15はそれぞれ、予測をより安定させるために、最終的にルールベースのレイヤーでモデルを補強する方法について述べている。
For example, P14 mentioned working on an anomaly detection model and adding a heuristics layer on top to filter the set of anomalies that surface based on domain knowledge.
例えば、P14は、異常検出モデルに取り組み、その上にヒューリスティック層を追加して、ドメイン知識に基づいて表面化した異常のセットをフィルタリングすることについて述べています。
P15 discussed one of their language models for a customer support chatbot:
P15は、カスタマーサポートチャットボットのための言語モデルの1つについて述べた。

The model might not have enough confidence in the suggested reply, so we don’t return [the recommendation].
また、言語モデルは、必ずしもそうであってほしくないことを言う可能性があります。
Also, language models can say all sorts of things you don’t necessarily want it to—another reason that we don’t show suggestions.
また、言語モデルは、必ずしもそうであってほしくないことを言う可能性があります（これも、推奨を表示しない理由のひとつです）。
For example, if somebody asks when the business is open, the model might try to quote a time when it thinks the business is open.
たとえば、「いつ営業しているか」と質問された場合、モデルは営業していると思われる時間帯を引用しようとするかもしれません。
[It might say] “9 am”, but the model doesn’t know that.
[午前9時」と答えるかもしれませんが、モデルにはそれがわかりません。
So if we detect time, then we filter that [reply].
そこで、時間を検出したら、その返答をフィルターにかけます。
We have a lot of filters.
私たちはたくさんのフィルターを持っています。

Constructing such filters was an iterative process—P15 mentioned constantly stress-testing the model in a sandbox, as well as observing suggested replies in early stages of deployment, to come up with filter ideas.
このようなフィルタの構築は反復プロセスです。P15は、サンドボックスで常にモデルをストレステストし、展開の初期段階で提案された返信を観察して、フィルタのアイデアを思いついたと述べています。
Creating filters was a more effective strategy than trying to retrain the model to say the right thing; the goal was to keep some version of a model working in production with little downtime.
フィルタを作成することは、正しいことを言うようにモデルを再教育するよりも効果的な戦略でした。目標は、ダウンタイムをほとんど発生させずに、あるバージョンのモデルを本番環境で動作させ続けることでした。
This combination of modern model-driven ML and old-fashioned rule-based AI indicates a need for managing filters (and versions of filters) in addition to managing learned models.
このように、最新のモデル駆動型MLと昔ながらのルールベースAIの組み合わせは、学習済みモデルの管理に加えて、フィルター（およびフィルターのバージョン）の管理の必要性を示しています。
The engineers we interviewed managed these artifacts themselves.
私たちがインタビューしたエンジニアは、これらの成果物を自ら管理していました。

### 4.5.4. Validate data going in and out of pipelines. 4.5.4. パイプラインに出入りするデータを検証する。

While participants reported that model parameters were typically "statically" validated before deploying to full production, features and predictions were continuously monitored for production models (P1, P2, P6, P8, P14, P16, P17, P18, P19).
参加者は、モデルパラメータは通常、本番環境に導入する前に「静的」に検証されると報告しましたが、本番モデルでは機能と予測が継続的に監視されました（P1、P2、P6、P8、P14、P16、P17、P18、P19）。
Several metrics were monitored— P2 discussed hard constraints for feature columns (e.g., bounds on values), P6 talked about monitoring completeness (i.e., fraction of non-null values) for features, P16 mentioned embedding their pipelines with "common sense checks," implemented as hard constraints on columns, and P8 described schema checks—making sure each data item adheres to an expected set of columns and their types.
P2は素性のカラムに対するハードコンストレイント（例：値の境界）、P6は素性の完全性（例：非NULL値の割合）のモニタリング、P16はパイプラインに「コモンセンスチェック」を組み込んでカラムに対するハードコンストレイントとして実装、P8はスキーマチェック（各データアイテムがカラムとそのタイプの期待されるセットに準拠していることを確認）について述べています。

While rudimentary data checks were embedded in most systems, P6 discussed that it was hard to figure out what higher-order data checks to compute:
初歩的なデータチェックはほとんどのシステムに組み込まれているが、どのような高次のデータチェックを計算すればいいのかがわかりにくいというのがP6の議論であった。

Monitoring is both metrics and then a predicate over those metrics that triggers alerts.
モニタリングは、メトリクスと、アラートのトリガーとなるメトリクスの述語の両方が必要です。
That second piece doesn’t exist—not because the infrastructure is hard, but because no one knows how to set those predicate values...for a lot of this stuff now, there’s engineering headcount to support a team doing this stuff.
インフラが難しいからというわけではなく、述語の値をどのように設定すればよいのか、誰も知らないからです...現在、こうしたことの多くには、こうしたことを行うチームをサポートするエンジニアリングの人員が必要です。
This is people’s jobs now; this constant, periodic evaluation of models.
このようなことを行うチームをサポートするエンジニアリングの人数は、現在、人々の仕事になっています。

Some participants discussed using black-box data monitoring services but lamented that their alerts did not prevent failures (P7, P14).
ブラックボックス化したデータ監視サービスの利用を検討する参加者もいたが、そのアラートでは障害を防げないと嘆いていた（P7、P14）。
P7 said:
P7 は次のように述べている。

We don’t find those metrics are useful.
そのような指標は有用とは思えません。
I guess, what’s the point in tracking these?
というのも、これらの指標を追跡することに何の意味があるのでしょうか？
Sometimes it’s really to cover my ass.
時には、本当に自分の尻拭いをするためです。
If someone [hypothetically] asked, how come the performance dropped from X to Y, I could go back in the data and say, there’s a slight shift in the user behavior that causes this.
もし誰かが「どうしてXからYにパフォーマンスが落ちたのか」と質問したら、データをさかのぼって、「ユーザーの行動にわずかな変化があったから、このような結果になった」と言うことができます。
So I can do an analysis of trying to convince people what happened, but can I prevent [the problem] from happening?
つまり、何が起こったのかを納得させるための分析はできますが、（問題が）起こらないようにすることはできるでしょうか。
Probably not.
おそらく無理でしょう。
Is that useful?
それは有用でしょうか？
Probably not.
おそらく無理でしょう。

While basic data validation was definitely useful for the participants, many of the participants expressed pain points with existing techniques and solutions, which we discuss further in Section 5.1.2.
基本的なデータ検証は参加者にとって間違いなく有益であったが、参加者の多くは、既存の技術やソリューションの問題点を指摘しており、これについてはセクション 5.1.2 でさらに説明する。

### 4.5.5. Keep it Simple. 4.5.5. シンプルにすること

Many participants expressed an aversion to complexity, preferring to rely on simple models and algorithms whenever possible (P1, P2, P6, P7, P11, P12, P14, P15, P16, P17, P19).
多くの参加者は、複雑さを嫌い、可能な限り単純なモデルとアルゴリズムに頼ることを好むと述べた（P1、P2、P6、P7、P11、P12、P14、P15、P16、P17、P19）。
P7 described the importance of relying on a simple training and hyperparameter search algorithm:
P7 は、単純な学習とハイパーパラメータ探索アルゴリズムに依存することの重要性を述べている。

In finance, we always split data by time.
金融の世界では、常にデータを時間軸で分割します。
The thing I [learned in finance] is, don’t exactly try to tune the hyperparameters too much, because that just overfits to historic data.
私がファイナンスで学んだことは、ハイパーパラメータをあまり調整しないことです。

P7 discussed choosing tree-based models over deep learning models for their ease of use, which simplified post-deployment maintenance:
P7は、ディープラーニングモデルよりも、導入後のメンテナンスを簡略化できる使い勝手の良さから、ツリーベースのモデルを選択したことについて述べています。
“I can probably do the same thing with neural nets.
"ニューラルネットでも同じことができるかもしれない。
But it’s not worth it.
しかし、その価値はありません。
[After] deployment it just doesn’t make any sense at all.”
[導入後は）まったく意味がないんです"。
However, other participants chose to use deep learning as a means of simplifying their pipelines (P1, P16).
しかし、他の参加者はパイプラインを簡略化する手段としてディープラーニングを使うことを選んだ（P1、P16）。
For instance, P16 described training a small number of higher-capacity models rather than a separate model for each target: “There were hundreds of products that [customers] were interested in, so we found it easier to instead train 3 separate classifiers that all shared the same underlying embedding...from a neural network.”
例えば、P16は、各ターゲットに対して個別のモデルを学習させるのではなく、少数の高容量モデルを学習させることを説明しています。"（顧客が）興味を持っている製品は何百もあったので、代わりにニューラルネットワークから、同じ基礎的な埋め込みを共有する3つの個別の分類器を学習させる方が簡単だと分かりました。"

While there was no universally agreed-upon answer to a question as broad as, “should I use deep learning?" we found a common theme in how participants leveraged deep learning models.
ディープラーニングを使うべきか」という広い問いに対する普遍的な合意はなかったが、参加者がディープラーニングモデルをどのように活用しているかという点では共通のテーマが見出された。
Specifically, for ease of post-deployment maintenance (e.g., an ability to retroactively debug pipelines), outputs of deep learning models were typically human-interpretable (e.g., image segmentation, object recognition, probabilities or likelihoods as embeddings).
具体的には、導入後のメンテナンス（例えば、パイプラインを遡ってデバッグする機能）を容易にするために、深層学習モデルの出力は通常、人間が解釈できるものでした（例えば、画像分割、物体認識、埋め込みとしての確率や尤度）。
P1 described a push at their company to rely more on neural networks:
P1は、彼らの会社でニューラルネットワークにもっと頼ろうとする動きがあることを説明しました。

A general trend is to try to move more into the neural network, and to combine models wherever possible so there are fewer bigger models.
一般的な傾向として、ニューラルネットワークへの移行が進み、可能な限りモデルを組み合わせて、より大きなモデルを少なくすることが求められています。
Then you don’t have these intermediate dependencies that cause drift and performance regressions...you eliminate entire classes of bugs and and issues by consolidating all these different piecemeal stacks.
そうすれば、ドリフトや性能低下の原因となる中間的な依存関係がなくなります。異なる断片的なスタックをすべて統合することで、あらゆる種類のバグや問題を排除することができるのです。

### 4.5.6. Organizationally Supporting ML Engineers Requires Deliberate Practices. 4.5.6. MLエンジニアを組織的にサポートするには、意図的な実践が必要です。

Our interviewees reported various organizational processes for sustaining models as part of their ML infrastructure.
インタビューに答えてくれた人たちは、MLインフラの一部としてモデルを維持するための様々な組織的プロセスを報告してくれました。
P6, P12, P14, P16, P18, and P19 described on-call processes for supervising production ML models.
P6、P12、P14、P16、P18、P19は、MLモデルを監督するためのオンコール・プロセスについて述べています。
For each model, at any point in time, some ML engineer would be on call, or primarily responsible for it.
それぞれのモデルについて、どの時点でも、あるMLエンジニアがオンコールで、あるいは主に担当することになります。
Any bug or incident observed (e.g., user complaint, pipeline failure) would receive a ticket, created by the on-call engineer, and be placed in a queue.
バグやインシデント（ユーザからの苦情やパイプラインの障害など）が発生すると、オンコールエンジニアがチケットを作成し、キューに入れる。
On-call rotations lasted a week or two weeks.
オンコールのローテーションは1週間から2週間。
At the end of a shift, an engineer would create an incident report— possibly one for each bug—detailing major issues that occurred and how they were fixed.
シフトの終わりには、エンジニアがバグごとにインシデントレポートを作成し、発生した主な問題とその解決策を詳細に報告します。

Additionally, P6, P7, P8, P10, P12, P14, P15, P16, P18, and P19 mentioned having a central queue of production ML bugs that every engineer added tickets to and processed tickets from.
さらに、P6、P7、P8、P10、P12、P14、P15、P16、P18、P19 は、すべてのエンジニアがチケットを追加し、チケットを処理する、本番環境のバグの中央キューを持つことに言及しました。
Often this queue was larger than what engineers could process in a timely manner, so they assigned priorities to tickets.
しばしばこのキューは、エンジニアがタイムリーに処理できる量よりも多いので、チケットに優先順位をつけていました。
Finally, P6, P7, P10, and P15 discussed having Service Level Objectives (SLOs), or commitments to minimum standards of performance, for pipelines in their organizations.
最後に，P6，P7，P10，P15 は，組織内のパイプラインにサービスレベル目標 (SLO) を設定すること，つまり最低水準の性能を約束することについて述べています．
For example, an pipeline to classify images could have an SLO of 95% accuracy.
たとえば、画像を分類するパイプラインでは、95%の精度をSLOに設定することができます。
A benefit of using the SLO framework for ML pipelines is a clear indication of whether a pipeline is performing well or not—if the SLO is not met, the pipeline is broken, by definition.
SLOのフレームワークをMLパイプラインに使用する利点は、パイプラインがうまく機能しているか否かを明確に示すことである。

# 5. Mlops Challenges and Opportunities 5. Mlopsの課題と可能性

In this section, we enumerate common pain points and anti-patterns observed across interviews.
本節では、インタビューを通じて観察された共通のペインポイントとアンチパターンを列挙する。
We discuss each pain point as a tension or synergy between the Three Vs (Section 4.2).
各苦情点は、3つのV（セクション4.2）の間の緊張または相乗効果として議論する。
At the end of each pain point, we describe our takeaways of ideas for future tools and research.
各ペインポイントの最後には、今後のツールや研究のためのアイデアとして、我々が得たものを説明する。
Finally, in Section 5.3, we characterize layers of the MLOps tool stack for those interested in building MLOps tools.
最後に、セクション 5.3 では、MLOps ツールの構築に関心を持つ人々のために、MLOps ツールスタックのレイヤーを特徴付ける。

## 5.1. Pain Points in Production ML 5.1. プロダクションMLのペインポイント

We focus on four themes that we didn’t know before the interviews: the mismatch between development and production environments, handling a spectrum of data errors, the ad-hoc nature of ML bugs, and long validation processes.
インタビュー前にはわからなかった、「開発環境と本番環境のミスマッチ」「さまざまなデータエラーへの対応」「MLバグのアドホック性」「検証プロセスの長さ」の4つのテーマに焦点を当てます。

### 5.1.1. Mismatch Between Development and Production Environments. 5.1.1. 開発環境と本番環境の不一致。

While it is important to create a separate development environment to validate ideas before promoting them to production, it is also necessary to minimize the discrepancies between the two environments.
アイデアを本番に進める前に、開発環境を別に作って検証することは重要ですが、2つの環境間の齟齬を最小限に抑えることも必要です。
Otherwise, unanticipated bugs might arise in production (P1, P2, P6, P8, P10, P13, P14, P15, P18).
そうしないと、本番で予期せぬバグが発生する可能性があるからです（P1, P2, P6, P8, P10, P13, P14, P15, P18）。
Creating similar development and production environments exposes a tension between velocity and validating early: development cycles are more experimental and move faster than production cycles; however, if the development environment is significantly different from the production environment, it’s hard to validate (ideas) early.
開発サイクルは実験的であり、生産サイクルよりも速く進みます。しかし、開発環境が生産環境と大きく異なる場合、（アイデアを）早期に検証することは難しくなります。

We discuss three examples of point points caused by the environment mismatch—data leakage, Jupyter notebook philosophies, and code quality.
環境のミスマッチによるポイントとして、データ漏洩、Jupyterノートブック哲学、コード品質の3つの例について説明する。

#### 5.1.1.1. Data Leakage. 5.1.1.1. データの流出

A common issue was data leakage—i.e., assuming during training that there is access to data that does not exist at serving time—an error typically discovered after the model was deployed and several incorrect live predictions were made.
よくある問題は、データリーク、つまり、学習時に、その時点では存在しないデータにアクセスできると仮定してしまうことです。この誤りは、通常、モデルが導入され、いくつかの誤ったライブ予測が行われた後に発見されます。
Anticipating any possible form of data leakage is tedious and hinders velocity; thus, sometimes leakage was retroactively checked during code review (P1).
データ漏えいの可能性を予測するのは面倒であり、スピードアップの妨げになるため、コードレビュー時に漏えいを遡ってチェックすることもありました（P1）。
The nature of data leakage ranged across reported bugs—for example, P18 recounted an instance where embedding models were trained on the same split of data as a downstream model, P2 described a class imbalance bug where they did not have enough labeled data for a subpopulation at training time (compared to its representation at serving time), and P15 described a bug in which feedback delay (time between making a live prediction and getting its ground-truth label) was ignored while training.
例えば、P18は埋め込みモデルが下流モデルと同じデータ分割で学習された例を挙げ、P2はクラスインバランスバグについて、学習時にサブ集団のラベル付きデータが十分でない（サービング時の表現と比較して）、P15はフィードバック遅延（ライブ予測をしてからそのグランドトゥルースのラベルを得るまでの時間）が学習時に無視されたバグについて述べています。
Different types of data leakage resulted in different magnitudes of ML performance drops: for example, in a pipeline with daily retraining, feedback delays could prevent retraining from succeeding because of a lack of new labels.
例えば、毎日再トレーニングを行うパイプラインでは、新しいラベルがないためにフィードバック遅延が発生し、再トレーニングが成功しないことがあるなど、データ漏洩の種類によってMLの性能低下の大きさが異なる。
However, in P18’s embedding leakage example, the resulting model was slightly more overfitted than expected, yielding lower-than-expected performance in production but not completely breaking.
しかし、P18の埋め込みリークの例では、結果として得られるモデルが予想よりわずかにオーバーフィットしており、本番では予想より低い性能となったが、完全に壊れることはなかった。

#### 5.1.1.2. Strong Opinions on Jupyter Notebooks. 5.1.1.2. Jupyter Notebooksに対する強い意見。

Participants described strongly opinionated and different philosophies with respect to how to use Jupyter notebooks in their workflows.
参加者は、ワークフローにおけるJupyter notebookの使用方法に関して、強い意見を持ち、異なる哲学を語っていた。
Jupyter notebooks were heavily used in development to support high velocity, which we did not find surprising.
Jupyterノートブックは、高速化をサポートするために開発で多用されており、これは驚くべきことではありませんでした。
However, we were surprised that although participants generally acknowledged worse code quality in notebooks, some participants preferred to use them in production to minimize the differences between their development and production environments.
しかし、参加者は一般的にノートブックではコード品質が悪いと認識しているものの、開発環境と本番環境の違いを最小化するために本番環境での使用を好む参加者がいることに驚きました。
P6 mentioned that they could debug quickly when locally downloading, executing, and manipulating data from a production notebook run.
P6 は、ローカルでノートブックからデータをダウンロードし、実行し、操作することで、迅速にデバッグできると述べています。
P18 remarked on the modularization benefits of a migration from a single codebase of scripts to notebooks:
P18は、スクリプトの単一コードベースからノートブックへの移行によるモジュール化の利点について述べています。

We put each component of the pipeline in a notebook, which has made my life so much easier.
パイプラインの各コンポーネントをノートブックにまとめることで、私の生活がとても楽になりました。
Now [when debugging], I can run only one specific component if I want, not the entire pipeline...
今では（デバッグの際に）パイプライン全体ではなく、特定のコンポーネントだけを実行することができます...。
I don’t need to focus on all those other components, and this has also helped with iteration.
他のすべてのコンポーネントに注目する必要はありませんし、イテレーションにも役立っています。

On the other hand, some participants strongly disliked the idea of notebooks in production (P10, P15).
一方，生産現場でノートブックを使うことを強く嫌う参加者もいた（P10，P15）。
P15 even went as far as to philosophically discourage the use of notebooks in the development environment:
P15は、開発環境でのノートブック使用を哲学的に否定するほどであった。
“Nobody uses notebooks.
「誰もノートブックを使っていません。
Instead, we all work in a shared code base, which is both the training and serving code base and people kick off jobs in the cloud to train models.”
その代わり，全員が共有コードベースで作業しています．このコードベースは，学習用とサービス用のコードベースでもあり，人々はモデルを学習するためにクラウド上でジョブをキックオフします" と述べています．
Similarly, P10 recounted a shift at their company to move any work they wanted to reproduce or deploy out of notebooks:
同様に、P10は、再現やデプロイしたい作業をノートブックから移動させるように会社でシフトしたことを語っています。

There were all sorts of manual issues.
マニュアルにはいろいろと問題がありました。
Someone would, you know, run something with the wrong sort of inputs from the notebook, and I’m [debugging] for like a day and a half.
誰かがノートブックから間違った入力で何かを実行すると、私は1日半ほどデバッグをすることになるんです。
Then [I’d] figure out this was all garbage.
そして、これがすべてゴミであることを突き止めたのです。
Eight months ago, we [realized] this was not working.
8ヵ月前、私たちはこれがうまくいっていないことに気づきました。
We need[ed] to put in the engineering effort to create [non-notebook] pipelines.
ノートブック以外のパイプラインを作るために、エンジニアリングに力を入れる必要があったのです。

The anecdotes on notebooks identified conflicts between competing priorities: (1) Notebooks support high velocity and therefore need to be in development environments, (2) Similar development and production environments prevents new bugs from being introduced, and (3) It’s easy to make mistakes with notebooks in production, e.g., running with the wrong inputs; copy-pasting instead of reusing code.
ノートブックに関する逸話から、競合する優先事項の間の対立が明らかになった：(1) ノートブックは高速化をサポートするので開発環境にある必要がある、(2) 開発環境と生産環境が似ていると新しいバグが発生しない、 (3) 生産環境でノートブックを使うと間違いを起こしやすい、例えば、間違った入力で実行する、コードの再利用ではなくコピーペーストをする、などです。
Each organization had different rankings of these priorities, ultimately indicating whether or not they used notebooks in production.
これらの優先順位は組織ごとに異なり、最終的にノートブックを本番で使うかどうかの判断材料となりました。

#### 5.1.1.3. Non-standardized Code Quality. 5.1.1.3. 非標準化されたコード品質

We found code quality and review practices to be non-standardized and inconsistent across development and production environments.
コード品質とレビューのやり方は標準化されておらず，開発環境と生産環境間で一貫性がないことがわかった．
Some participants described organization-wide production coding standards for specific languages (P2, P5), but even the most mature organizations did not have ML-specific coding guidelines for experiments.
一部の参加者は、特定の言語のための組織全体の生産コーディング標準を説明したが (P2, P5)、最も成熟した組織でさえ、実験用の ML 固有のコーディングガイドラインを持っていなかった。
Generally, experimental code (in development) was not reviewed, but changes to production went through a code review process (P1, P5).
一般に、実験用のコード（開発中のもの）はレビューされませんが、本番環境への変更はコードレビュープロセスを経ていました（P1, P5）。
Participants felt that code review wasn’t too useful, but they did it to adhere to software best practices (P1, P3, P5, P10).
参加者はコードレビューがあまり役に立たないと感じていたが、ソフトウェアのベストプラクティスを遵守するために行っていた（P1, P3, P5, P10）。
P5 mentioned that “it’s just really not worth the effort; people might catch some minor errors”.
P5は「労力に見合わない。小さなエラーを発見できるかもしれない」と述べています。
P10 hypothesized that the lack of utility came from difficulty of code review:
P10は、有用性の欠如はコードレビューの難しさに起因すると仮定している。

It’s tricky.
難しいですね。
You use a little bit of judgment as to where things might go wrong, and you maybe spend more time sort of reviewing that.
どこが問題なのかを少し判断して、その見直しにもっと時間をかけるかもしれません。
But bugs will go to production, and [as long as they’re not] that catastrophic, [it’s okay.]
でも、バグは本番に出ますし、それほど致命的でない限りは、大丈夫です。

Code review and other good software engineering practices might make deployments less error-prone.
コードレビューや他の優れたソフトウェア工学の実践は、デプロイ時のミスを少なくすることができるかもしれません。
However, because ML is so experimental in nature, they can be significant barriers to velocity; thus, many model developers ignore these practices (P1, P6, P11).
しかし、MLは実験的なものであるため、これらは速度を上げるための大きな障壁となり得ます。したがって、多くのモデル開発者はこれらの慣習を無視しています（P1, P6, P11）。
P6 said:
P6が言う。

I used to see a lot of people complaining that model developers don’t follow software engineering [practices].
以前、私は、モデル開発者がソフトウェア工学のプラクティスに従わないことに不満を抱いている人々をよく見かけました。
At this point, I’m feeling more convinced that they don’t follow software engineering [practices]—[not] because they’re lazy, [but because software engineering practices are] contradictory to the agility of analysis and exploration.
それは、彼らが怠惰だからではなく、ソフトウェア工学の実践が、解析や探索の俊敏性と矛盾しているからです。

#### 5.1.1.4. Takeaway. 5.1.1.4. テイクアウェイ

We believe there’s an opportunity to create virtualized infrastructure specific to ML needs with similar development and production environments.
私たちは、同様の開発環境と本番環境で、MLのニーズに特化した仮想化インフラを構築する機会があると信じています。
Each environment should build on the same foundation but supports different modes of iteration (i.e., high velocity in development).
それぞれの環境は同じ基盤の上に構築されるべきですが、異なる反復のモード（例えば、開発における高い速度）をサポートします。
Such tooling should also track the discrepancies between environments and minimize the likelihood that discrepancy-related bugs arise.
そのようなツールはまた、環境間の不一致を追跡し、不一致に関連するバグが発生する可能性を最小にする必要があります。

### 5.1.2. Handling A Spectrum of Data Errors. 5.1.2. さまざまなデータエラーの処理。

As alluded to in Section 4.5.4, we found that ML engineers struggled to handle the spectrum of data errors: hard → soft → drift (P5, P6, P8, P11, P14, P16, P17, P18, P19).
4.5.4 節で述べたように，ML のエンジニアはハードエラー，ソフトエラー，ドリフト エラーという多様なデータエラーを扱うのに苦労していることがわかった（P5, P6, P8, P11, P14, P16, P17, P18, P19）．
Hard errors are obvious and result in clearly “bad predictions”, such as when mixing or swapping columns or when violating constraints (e.g., a negative age).
ハードエラーは、列の混合や入れ替え、制約条件の違反（例えば、年齢が負）など、明らかに「悪い予測」につながるものです。
Soft errors, such as a few null-valued features in a data point, are less pernicious and can still yield reasonable predictions, making them hard to catch and quantify.
ソフトエラーは、データポイントに数個の空値の特徴がある場合など、それほど悪質ではなく、それでも合理的な予測ができるため、捕捉や定量化が困難なものである。
Drift errors occur when the live data is from a seemingly different distribution than the training set; these happen relatively slowly over time.
ドリフトエラーは、実データがトレーニングセットと一見異なる分布をしている場合に発生するもので、時間の経過とともに比較的ゆっくりと発生します。
One pain point mentioned by the interviewees was that different types of data errors require different responses, and it was not easy to determine the appropriate response.
インタビューに答えてくれた人たちの悩みの種は、異なるタイプのデータエラーには異なる対応が必要であり、適切な対応を決定するのは簡単ではないということでした。
Another issue was that requiring practitioners to manually define constraints on data quality (e.g., lower and upper bounds on values) was not sustainable over time, as employees with this knowledge left the organization.
また、データ品質に関する制約条件（値の下限や上限など）を実務担当者が手作業で定義する必要があり、この知識を持つ従業員が組織を離れると、長期的に持続できないことも問題点として挙げられました。

The most commonly discussed pain point wasfalse-positive alerts, or alerts triggered even when the ML performance is adequate.
最もよく議論されたペインポイントは、偽陽性アラート、またはMLのパフォーマンスが十分であるにもかかわらず引き起こされるアラートでした。
Engineers often monitored and placed alerts on each feature or input column and prediction or output column (P5, P6, P8, P11, P14, P16, P17, P18, P19).
エンジニアは、各特徴（入力列）と予測（出力列）を監視してアラートを出すことがよくありました（P5、P6、P8、P11、P14、P16、P17、P18、P19）。
Engineers automated schema checks and bounds to catch hard errors, and they tracked distance metrics (e.g., KL divergence) between historical and live features to catch soft and drift errors.
エンジニアはスキーマチェックとバウンディングを自動化してハードエラーを検出し、ソフトエラーとドリフトエラーを検出するために、過去の特徴と実際の特徴の間の距離メトリクス（KLダイバージェンスなど）を追跡しました。
If the number of metrics tracked is so large, even with only a handful of columns, the probability that at least one column violates constraints is high!
追跡されるメトリクスの数が非常に多い場合、たとえほんの一握りの列であっても、少なくとも1つの列が制約に違反する確率が高くなります。

Taking a step back, the purpose of assessing data quality before serving predictions is to validate early.
一歩下がって、予測を提供する前にデータの品質を評価する目的は、早期に検証することです。
Correctly monitoring data quality demonstrates the conflict between validating early and versioning—if data validation methods flag a broken data point, which in turn rejects the corresponding prediction made by the main ML model, some backup plan or fallback model version (Section 4.5) is necessary.
もしデータ検証方法が壊れたデータポイントにフラグを立て、それがメインのMLモデルによって作られた対応する予測を拒否する場合、何らかのバックアッププランまたはフォールバックモデルバージョン（セクション4.5）が必要です。
Consequently, an excessive number of false-positive alerts leads to two pain points: (1) unnecessarily maintaining many model versions or simple heuristics, which can be hard to keep track of, and (2) a lower overall accuracy or ML metric, as baseline models might not serve high-quality predictions (P14, P19).
(1)不必要に多くのモデルバージョンや単純なヒューリスティックを維持すること、これは追跡するのが難しいかもしれません。

#### 5.1.2.1. Dealing with Alert Fatigue. 5.1.2.1. アラート疲労への対処。

A surplus of false-positive alerts led to fatigue and silencing of alerts, which could miss actual performance drops.
誤認識の多いアラートは疲労を招き、アラートを黙殺するため、実際のパフォーマンス低下を見逃してしまう可能性がありました。
P8 said “people [were] getting bombed with these alerts.”
P8は、「人々はこれらのアラートを浴びせかけられた」と述べています。
P14 mentioned a current initiative at their company to reduce the alert fatigue:
P14は、アラート疲労を軽減するために、現在自社で行っている取り組みについて言及しました。

Recently we’ve noticed that some of these alerts have been rather noisy and not necessarily reflective of events that we care about triaging and fixing.
最近、これらのアラートの中には、トリアージや修正を必要とするイベントを必ずしも反映していない、ノイズの多いものがあることに気づきました。
So we’ve recently taken a close look at those alerts and are trying to figure out, how can we more precisely specify that query such that it’s only highlighting the problematic events?
そこで最近、これらのアラートをよく観察し、問題のあるイベントのみを強調するようなクエリーをより正確に指定するにはどうしたらよいかを考えています。

P18 shared a similar sentiment, that there was “nothing critical in most of the alerts.”
P18 は、「ほとんどのアラートには重要なものはない」と同じような感想を述べています。
The only time there was something critical was “way back when [they] had to actually wake up in the middle of the night to solve it...the only time [in years].”
唯一重大なものがあったのは、「昔、夜中に起きて解決しなければならなかった時...その時だけ（ここ数年）」だったそうです。
When we asked what they did about the noncritical alerts and how they acted on the alerts, P18 said:
非重要なアラートについてどうしたか、アラートに対してどう行動したかを尋ねたところ、P18はこう答えました。

You typically ignore most alerts...I guess on record I’d say 90% of them aren’t immediate.
通常、ほとんどのアラートは無視されます......記録上では、90%は即時性がないと言えるでしょう。
You just have to acknowledge them [internally], like just be aware that there is something happening.
ただ、何かが起きていることを認識する必要があります。

The alert fatigue typically materialized when engineers were on-call, or responsible for ML pipelines during a 7 or 14-day shift.
アラートの疲労は、エンジニアがオンコールになったときや、7日または14日のシフト中にMLパイプラインを担当したときに生じるのが一般的です。
P19 recounted how on-call rotations were dreaded amongst their team, particularly for new team members, due to the high rate of false-positive alerts:
P19は、特に新入社員にとって、オンコールローテーションは誤検出率が高いため、チーム内で恐れられていたことを語っています。

The pain point is dealing with that alert fatigue and the domain expertise necessary to know what to act on during on-call.
苦労するのは、そのアラート疲れと、オンコールで何をすべきなのか、その領域の専門知識への対応です。
New members freak out in the first [oncall], so [for every rotation,] we have two members.
新メンバーは最初のオンコールでパニックになってしまうので、（ローテーションごとに）2人のメンバーを配置しています。
One member is a shadow, and they ask a lot of questions.
1人はシャドーで、たくさん質問してくれます。

P19 also discussed an initiative at their company to reduce the alert fatigue, ironically with another model:
P19では、皮肉にも別のモデルで、アラート疲れを軽減するための自社での取り組みも紹介された。

The [internal tool] looks at different metrics for what alerts were [acted on] during the on-call...[the internal tool] tries to reduce the noise level, alert.
内部ツールは、オンコール中にどのようなアラートが処理されたかについて、さまざまな指標を調べます...内部ツールは、アラートというノイズレベルを下げようとします。
It says, hey, this alert has been populated this like 1,000 times and ignored 45% of time.
このアラートは1,000回ほど入力されましたが、45%は無視されました」と表示されます。
[The on-call member] will acknowledge whether we need to [fix] the issue
[オンコールメンバーは、その問題を修正する必要があるかどうかを確認します。

#### 5.1.2.2. Creating Meaningful Data Alerts is Challenging. 5.1.2.2. 意味のあるデータアラートの作成は難しい

If schema checks and rudimentary column bounds didn’t flag all the errors, and distance metrics between historical and live feature values flagged too many false positive errors, how could engineers find a “Goldilocks” alert setting?
スキーマチェックや初歩的なカラム境界ではすべてのエラーにフラグが立たず、履歴と実際のフィーチャー値の間の距離メトリックでは誤検出が多すぎるとしたら、エンジニアはどのようにして「ゴルディロックス」アラート設定を見つけることができるでしょうか。
5 We organized the data-related issues faced by engineers into a hierarchy, from most frequently occurring to least frequently occurring:
5 エンジニアが直面するデータ関連の問題を、発生頻度の高いものから低いものへと階層的に整理しました。

- Feedback delays: Many participants said that ground-truth labels for live predictions often arrived after a delay, which could vary unpredictably (e.g., human-in-the-loop or networking delays) and thus caused problems for knowing realtime performance or retraining regularly (P2, P7, P8, P15, P17, P18). P7 felt strongly about the negative impact of feedback delays on their ML pipelines: フィードバックの遅れ。 多くの参加者は、ライブ予測のための基底真理ラベルはしばしば遅延後に到着し、それは予測不可能に変化する可能性があり（例えば、ヒューマンインザループやネットワーク遅延）、したがって、リアルタイム性能を知ることや定期的に再トレーニングを行うための問題を引き起こすと言いました（P2、P7、P8、P15、P17、P18）。 P7は、フィードバックの遅延がMLパイプラインに与える悪影響について強く感じていました。

- I have no idea how well [models] actually perform on live data. We do log the the [feature and output] data, but feedback is always delayed by at least 2 weeks. Sometimes we might not have feedback...so when we realize maybe something went wrong, it could [have been] 2 weeks ago, and yeah, it’s just straight up—we don’t even care...nobody is solving the label lag problem. It doesn’t make sense to me that a monitoring tool is not addressing this, because [it’s] the number one problem. 実際のデータで[モデル]がどの程度のパフォーマンスを発揮するのか、私にはわかりません。 機能・出力]データのログは取っていますが、フィードバックは常に最低でも2週間は遅れています。 フィードバックがないこともあります......だから、何か問題が起きたと気づいたときには、それは2週間も前のことかもしれません。 モニタリングツールがこれに対処していないのは納得がいきません。

- P8 discussed how they spent 2-3 years developing a humanin-the-loop pipeline to manually label live data as frequently as possible: “you want to come up with the rate at which data is changing, and then assign people to manage this rate roughly”. On the other hand, P17 and P19 both talked about how, when they worked on recommender systems, they did not have to experience feedback delay issues. P17 said: “With recommendations, it’s pretty clear whether or not we got it right because we get pretty immediate feedback. We suggest something, and someone’s like go away or they click it.” P8は、ライブデータにできるだけ頻繁に手動でラベルを付けるために、2-3年かけてヒューマンインザループパイプラインを開発したことを説明しました。 「データが変化する速度を考え、その速度を大まかに管理するために人を配置したい」。 一方、P17とP19は、レコメンダーシステムに携わったとき、フィードバック遅延の問題を経験する必要がなかったことを話しています。 P17はこう言っています。 「レコメンダーでは、すぐにフィードバックが来るので、正しいかどうかがはっきりします。 私たちが何かを提案すると、誰かが去っていくか、それをクリックするかです。

- Unnatural data drift: Often, in production pipelines, data was missing, incomplete, or corrupted, causing model performance to sharply degrade (P3, P6, P7, P10, P16, P17). Several participants cited Covid as an example, but there are other (better) everyday instances of unnatural data drift. P6 described a bug where users had inconsistent definitions of the same word, complicating the deployment of a service to a new user. P7 mentioned a bug where data from users in a certain geographic region arrived more sporadically than usual. P10 discussed a bug where the format of raw data was occasionally corrupted: “Tables didn’t always have headers in the same place, even though they were the same tables.” 不自然なデータドリフト。 実運用パイプラインでは、しばしばデータが欠落、不完全、または破損し、モデルの性能が急激に低下することがありました（P3、P6、P7、P10、P16、P17）。 参加者の何人かはCovidを例として挙げましたが、不自然なデータドリフトの事例は他にも（より良い）日常的なものがあります。 P6 は、ユーザーが同じ単語の定義に一貫性がなく、新しいユーザーへのサービスの展開を複雑にしてしまうバグについて述べています。 P7は、特定の地域のユーザーからのデータが通常よりも散発的に到着するバグについて述べています。 P10は、生データのフォーマットが時々破損する不具合について述べています。 "同じテーブルなのに、ヘッダが同じ場所にあるとは限らない"。

- Natural data drift: Surprisingly, participants didn’t seem too worried about slower, expected natural data drift over time—they noted that frequent model retrains solved this problem (P6, P7, P8, P12, P15, P16, P17). As an anecdote, we asked P17 to give an example of a natural data drift problem their company faced, and they could not think of a good example. P14 also said they don’t have natural data drift problems: 自然なデータドリフト。 意外なことに、参加者は、時間の経過とともに予想されるゆっくりとした自然なデータドリフトをあまり心配していないようでした。 P17に、自社が直面したナチュラルドリフトの問題の例を挙げてもらったところ、良い例が思いつかなかったという逸話があります。 P14 も自然データドリフトの問題はないと言っている。

- The model gets retrained every day, so we don’t have the scenario of like: Oh, our models got stale and we need to retrain it because it’s starting to make mistakes because data has drifted...fortunately we’ve never had to deal with [such a] scenario. Sometimes there are bad [training] jobs, but we can always effectively roll back to a different [model]. モデルは毎日再トレーニングされるので、「モデルが古くなったから再トレーニングしよう」というようなシナリオはありません。 幸いなことに、このようなシナリオに直面したことは一度もありません。 しかし、いつでも効果的に別のモデルにロールバックすることができます。

- However, a few engineers mentioned that natural data shift could cause some hand-curated features and data quality checks to corrupt (P3, P6, P8). P6 discussed a histogram used to make a feature (i.e., converting a real-valued feature to a categorical feature) for an ML model—as data changed over time, the bucket boundaries became useless, resulting in buggy predictions. P8 described how, in their NLP models, the vocabulary of frequently-occurring words changed over time, forcing them to update their preprocessor functions regularly. Our takeaway is that any function that summarizes data—be it cleaning tools, preprocessors, features, or models— needs to be refit regularly. しかし、数名のエンジニアは、自然なデータシフトにより、手作業で作成した特徴量やデータ品質チェックが破損する可能性があると述べています（P3, P6, P8）。 P6 は、ML モデルの特徴量の作成（実数値特徴量のカテゴリ化）に使用したヒストグラムについて、データの時間的変化によりバケット境界が使えなくなり、結果として予測にバグが生じたと述べています。 P8は、NLPモデルにおいて、頻出する単語の語彙が時間とともに変化するため、プリプロセッサの関数を定期的に更新することを余儀なくされていることを説明しました。 クリーニングツール、プリプロセッサー、機能、モデルなど、データを要約する機能は定期的に更新する必要がある、というのが我々の結論です。

#### 5.1.2.3. Takeaway. 5.1.2.3. テイクアウェイ

Unfortunately, none of the participants reported having solved the Goldilocks ML alert problem at their companies.
残念ながら、参加者の中で、自社のゴルディロックス型MLアラートの問題を解決できたと報告した人はいなかった。
What metrics can be reliably monitored in real-time, and what criteria should trigger alerts to maximize precision and recall when identifying model performance drops?
どのような指標がリアルタイムで信頼できるのか、どのような基準でアラートを発し、モデルの性能低下を特定する際に精度と再現性を最大化するのか。
How can these metrics and alerting criteria—functions of naturally-drifting data—automatically tune themselves over time?
これらの指標とアラート基準は、自然に漂うデータの機能であり、時間とともに自動的に調整されるのでしょうか？
We envision this to be an opportunity for new data management tools.
私たちは、これが新しいデータ管理ツールの機会となることを想定しています。

### 5.1.3. Taming the Long Tail of ML Pipeline Bugs. 5.1.3. MLパイプラインのバグのロングテール化。

In the interviews, we gathered the sentiment that ML debugging is different from debugging during standard software engineering, where one can write test cases to cover the space of potential bugs.
MLのデバッグは、一般的なソフトウェアエンジニアリングのデバッグと異なり、テストケースを書いてバグの可能性を網羅することができる、というのがインタビューの感想です。
But for ML, if one can’t categorize bugs effectively because every bug feels unique, how will they prevent future similar failures?
しかし、MLでは、バグの一つ一つがユニークであるため、効果的にバグを分類できないとしたら、今後どのようにして類似の障害を防ぐことができるでしょうか？
Moreover, it’s important to fix pipeline bugs as soon as possible to minimize downtime, and a long tail of possible ML pipeline bugs forces practitioners to have high debugging velocity.
さらに、ダウンタイムを最小にするためにパイプラインのバグをできるだけ早く修正することが重要で、MLパイプラインのバグの可能性がロングテールであるため、実務者は高いデバッグ速度を持たざるを得ないのです。
“I just sort of poked around until, at some point, I figured [it] out,” P6 said, describing their ad-hoc approach to debugging.
P6は、「私は、ある時点で（バグが）分かるようになるまで、ただ、あちこち調べました」と、デバッグに対する彼らのアドホックなアプローチについて述べています。
Other participants similarly mentioned that they debug without a systematic framework, which could take them a long time (P5, P8, P10, P18).
他の参加者も同様に、体系的な枠組みを持たずにデバッグを行うため、長い時間がかかると述べています（P5、P8、P10、P18）。

While some types of bugs were discussed by multiple participants, such as accidentally flipping labels in classification models (P1, P3, P6, P11) and forgetting to set random seeds (P1, P12, P13), the vast majority of bugs described to us in the interviews were seemingly bespoke and not shared among participants.
分類モデルのラベルを誤って反転させてしまう（P1、P3、P6、P11）、ランダムシードを設定し忘れる（P1、P12、P13）など、複数の参加者が議論した種類のバグもありましたが、インタビューで語られた大部分のバグは、一見オーダーメイドで、参加者間で共有されていないように見えました。
For example, P8 forgot to drop special characters (e.g., apostrophes) for their language models.
例えば，P8は言語モデルの特殊文字（アポストロフィーなど）を削除するのを忘れていました．
P6 found that the imputation value for missing features was once corrupted.
P6は、欠落した特徴量のインピュテーション値が一度破損していることを発見しました。
P18 mentioned that a feature of unstructured data type (e.g., JSON) had half of the keys’ values missing for a “long time.”
P18は、非構造化データ型（例えば、JSON）の特徴が、"長い間 "キーの値の半分が欠落していたことに言及した。

**Unpredictable Bugs; Predictable Symptoms**.
**予測できないバグ、予測できる症状**。
Interestingly, these one-off bugs from the long tail showed similar symptoms of failure.
興味深いことに、これらのロングテールからの単発のバグは、同じような失敗の症状を示しました。
For instance, a symptom of unnatural data drift issues (defined in Section 5.1.2) was a large discrepancy between offline validation accuracy and production accuracy immediately after deployment (P1, P6, P14, P18).
例えば，不自然なデータドリフトの問題(セクション 5.1.2 で定義)の症状として，オフライン検証の精度と配備直後の本番の精度の間に大きな不一致がありました(P1, P6, P14, P18)．
The similarity in symptoms highlighted the similarity in methods for isolating bugs; they were almost always some variant of slicing and dicing data for different groups of customers or data points (P2, P6, P11, P14, P17, P19).
症状の類似性から、バグの切り分け方法も類似しており、ほとんどの場合、顧客グループやデータ ポイントごとにデータをスライスして切り分けるという方法をとっていました（P2、P6、P11、P14、P17、P19）。
P14 discussed tracking bugs for different slices of data and only drilling down into their queue of bugs when they observed “systematic mistakes for a large number of customers.”
P14は、異なるスライスデータのバグを追跡し、「多数の顧客に対する体系的な誤り」を観察した場合にのみ、バグのキューにドリルダウンすることについて述べています。
P2 did something similar, although they hesitated to call it debugging:
P2は、デバッグと呼ぶのはためらわれましたが、同様のことを行っていました。

You can sort of like, look for instances of a particular [underperforming slice] and [debug]—although I’d argue that [it isn’t] debugging as much as it is sampling the world for more data...maybe it’s not a bug, and [it’s] just [that] the model has not seen enough examples of some slice.
ある特定の[パフォーマンスが低いスライス]の例を探して、[デバッグ]することができます。しかし、私は、より多くのデータを求めて世界をサンプリングするのと同じくらいデバッグしていないと主張します...おそらくそれはバグではなく、モデルがあるスライスの例を十分に見ていないだけです。

Paranoia Caused by ML Debugging Trauma.
MLデバッグのトラウマが引き起こすパラノイア。
After several iterations of chasing bespoke ML-related bugs in production, ML engineers that we interviewed developed a sense of paranoia while evaluating models offline, possibly as a coping mechanism (P1, P2, P6, P15, P17, P19).
私たちがインタビューしたMLエンジニアは，本番環境で特注のML関連バグを何度も追いかけた結果，オフラインでモデルを評価する際に，対処療法的にパラノイアの感覚を持つようになりました（P1，P2，P6，P15，P17，P19)．
P1 recounted a bug that was “impossible to discover” after a deployment to production:
P1 は，本番環境へのデプロイ後に「発見不可能」なバグが発生したことを語っている．

ML [bugs] don’t get caught by tests or production systems and just silently cause errors [that manifest as] slight reductions in performance.
ML の[バグ]はテストや生産システムには引っかからず、ただ黙ってエラーを 引き起こし、それがわずかな性能低下として現れるだけです。
This is why [you] need to be paranoid when you’re writing ML code, and then be paranoid when you’re coding.
このため、ML のコードを書いているときは疑い深くなり、コーディングしているときも疑い深くなる必要があるのです。
I remember one example of a beefy PR with a lot of new additions to data augmentation...but the ground truth data was flipped.
私は、データ拡張のために多くの新しい追加をしたビーフなPRの一例を覚えています...しかし、グランドトゥルースデータが反転していました。
If it hadn’t been caught in code review, it [would’ve been] almost impossible to discover.
コードレビューで発見されなかったら、発見するのはほとんど不可能だったでしょう。
I can think of no mechanism by which we would have found this besides someone just curiously reading the code.
誰かが興味本位でコードを読む以外に、これを発見するメカニズムが思いつきません。
[In production], it would have only [slightly] hurt accuracy.
[実稼働環境では、精度が少し落ちる程度でしょう。

It’s possible that many of the bespoke bugs could be ignored if they didn’t actually affect model performance.
モデルのパフォーマンスに影響を与えないのであれば、特注バグの多くは無視できる可能性があります。
Tying this concept to the data quality issue, maybe all engineers needed to know was when model performance was suffering.
この概念をデータ品質の問題と結びつけると、エンジニアが知るべきことは、モデルのパフォーマンスがいつ低下しているかということだけかもしれません。
But they needed to know precisely when models were underperforming, an unsolved question as discussed in Section 5.1.2.
しかし、エンジニアが知る必要があったのは、モデルのパフォーマンスが低下したときであり、これは5.1.2節で説明したように未解決の問題です。
When we asked P1, “how do you know when the model is not working as well as you expect?”—they gave the following answer:
P1に「モデルが期待通りに動作していないとき、どうやって知るのですか」と尋ねると、彼らは次のような答えを返してきました。

Um, yeah, it’s really hard.
ええと、そうですね、本当に難しいです。
Basically there’s no surefire strategy.
基本的に、確実な戦略はありません。
The closest that I’ve seen is for people to integrate a very high degree of observability into every part of their pipeline.
私が見た中で最も近いのは、パイプラインのあらゆる部分に非常に高度な観測性を統合することです。
It starts with having really good raw data, observability, and visualization tools.
そのためには、優れた生データ、観測能力、可視化ツールを用意することから始めます。
The ability to query.
クエリ機能。
I’ve noticed, you know, so much of this [ad-hoc bug exploration] is just—if you make the friction [to debug] lower, people will do it more.
アドホックなバグ探索の多くは、摩擦を少なくすれば、より多くの人が行うようになります。
So as an organization, you need to make the friction very low for investigating what the data actually looks like, [such as] looking at specific examples.
ですから、組織として、データが実際にどのようなものかを調査するための摩擦を非常に少なくする必要があります（具体例を見るなど）。

**Takeaway**.
**Takeaway**.
Our takeaway is that there is a chicken-and-egg problem in making it easier to tackle the long tail of ML bugs.
私たちが得た教訓は、MLバグのロングテールへの取り組みを容易にするためには、鶏と卵の問題があることです。
To group the tail into higher-order categories—i.e., to know what bugs to focus on and what to throw out—we need to know when models are precisely underperforming; then we can map performance drops to bugs.
ロングテールを高次のカテゴリーに分類するために、つまり、どのバグに注目し、何を捨てればよいかを知るために、我々は、いつモデルが正確に低パフォーマンスになるかを知る必要があり、そうすれば、パフォーマンスの低下をバグに対応付けることができます。
However, to know when models are precisely underperforming, given feedback delays and other data quality assessment challenges as described in Section 5.1.2, we need to be able to identify all the bugs in a pipeline and reason how much each one could plausibly impact performance.
しかし、セクション5.1.2で説明したように、フィードバックの遅れやその他のデータ品質評価の課題があるため、モデルがいつ正確にパフォーマンスを低下させるかを知るためには、パイプライン内のすべてのバグを特定し、それぞれがパフォーマンスにどの程度影響を与えるかを合理的に判断できるようにする必要があるのです。
Breaking this cycle could be a valuable contribution to the production ML community and help alleviate challenges that stem from the long tail of ML bugs.
このサイクルを断ち切ることは、MLコミュニティへの貴重な貢献であり、MLバグのロングテールに起因する課題を軽減するのに役立つと思われる。

### 5.1.4. Multi-Staged Deployments Seemingly Take Forever. 5.1.4. 多段階デプロイメントに時間がかかるようです。

Multiple participants complained that end-to-end experimentation—the conception of an idea to improve ML performance to validating the idea—took too long (P7, P14, P16, P17, P18, P19).
複数の参加者が、エンドツーエンドの実験（MLの性能を向上させるアイデアの考案からアイデアの検証まで）に時間がかかりすぎるという不満を述べている（P7, P14, P16, P17, P18, P19）。
This reveals the synergies between velocity and validating early: if ideas can be invalidated in earlier stages of deployment, then overall velocity is increased.
これは、ベロシティと早期検証の相乗効果を明らかにするものである。
But sometimes a stage of deployment would take a long time to observe meaningful results—for example, P19 mentioned that at their company, the timeline for trying a new feature idea took over three months:
たとえば、P19 は、自分の会社では、新しい機能のアイデアを試すのに 3 か月以上かかると述べています。

I don’t have the exact numbers; around 40 or 50% will make it to initial launch.
正確な数字は分かりませんが、約40〜50％が最初の打ち上げまでこぎつけます。
And then, either because it doesn’t pass the legal or privacy or some other complexity, we drop about 50% of [the launched experiments].
そして、法的な問題やプライバシーの問題、あるいはその他の複雑な問題をクリアできないために、50％ほどを打ち切ります。
We have to drop a lot of ideas.
多くのアイデアを捨てなければならないのです。

The uncertainty of whether projects will be successful stemmed from the unpredictable, real-world nature of the experiments (P18, P19).
プロジェクトが成功するかどうかの不確実性は、実験の予測不可能な現実的な性質から生じています（P18, P19）。
P19 said that some features don’t make sense after a few months, given the nature of how user behaviors change, which would cause an initially good idea to never fully and finally deploy to production:
P19は、ユーザーの行動がどのように変化するかという本質を考えると、数ヶ月後には意味がない機能もあると述べ、当初は良いアイデアでも、最終的に本番環境に導入されることはないだろうとしています。

You have to look at so many different metrics, and even for very experienced folks doing this process like dozen times, sometimes it’s hard to figure out especially when the user’s behavior changes very steadily.
非常に多くの指標を見る必要があり、このプロセスを何十回も行っている経験豊富な人でも、特にユーザーの行動が着実に変化している場合は、把握するのが難しいことがあるのです。
There’s no sudden change [in evaluation metrics] because of one launch; it just usage patterns that change.
ある製品を発売したからといって、評価指標が突然変わることはありません。

P18 offered an anecdote where their company’s key product metrics changed in the middle of one of their experiments, causing them to kill a experiment that appeared to be promising (the original metric was improving):
P18は、彼らの会社の主要な製品指標がある実験の途中で変化し、有望と思われた実験（元の指標は改善していた）を中止させたという逸話を紹介した。

It was causing a huge gain on the product metrics; it was definitely a green signal.
製品の指標は大きく向上し、間違いなく青信号でした。
But as for the product, metrics keep on rotating based on the company’s priorities, you know.
しかし、製品に関しては、会社の優先順位によって、指標は常に変化しています。
Is it the revenue at this point?
今のところ、売上なのか？
Is it the total number of, let’s say, installs?
インストール数なのか、クリック数なのか。
Or clicks at this particular point of time?
それとも、この時点のクリック数ですか？
They keep on changing with company’s roadmap...
会社のロードマップに合わせて、常に変化していくのです。

Takeaway.
要点
While most participants were unable to share exact information about the length of the staged deployment process and specific anecdotes about experiments they needed to cancel for privacy reasons, we found it interesting how different organizations had different deployment evaluation practices yet similar pain around failed project ideas due to the highly iterative, experimental nature of ML.
ほとんどの参加者は、段階的なデプロイメントプロセスの長さや、プライバシー上の理由から中止しなければならなかった実験に関する具体的な逸話について正確な情報を共有することができませんでしたが、私たちは、組織によってデプロイメントの評価方法が異なる一方で、MLの高度な反復性と実験性のために、プロジェクトのアイデアの失敗に関する苦痛が似ていることに興味深いことに気づきました。
We believe there is an opportunity for tooling to streamline ML deployments in this multi-stage pattern, to minimize wasted work and help practitioners predict the end-to-end gains for their ideas.
私たちは、このような多段階のパターンでのMLデプロイメントを合理化するツールが、無駄な作業を最小限に抑え、実務家が自分のアイデアのエンドツーエンドの利益を予測するのを助ける機会があると信じています。

## 5.2. Observed MLOps Anti-Patterns 5.2. 観察されたMLOpsのアンチパターン

Here we report a list of MLOps anti-patterns observed in our interviews, or common potentially-problematic behaviors in the ecosystem around ML experiments and deployments.
ここでは、MLOpsのアンチパターン、つまりML実験やデプロイメントにまつわるエコシステムで問題となりうる一般的な振る舞いをインタビューから報告します。

### 5.2.1. Industry-Classroom Mismatch. 5.2.1. 産業と教室のミスマッチ

P1, P5, P7, P11, and P16 each discussed some ML-related bugs they encountered early in their career, right after leaving school, that they knew how to avoid only after on-the-job experience.
P1、P5、P7、P11、P16はそれぞれ、学校を卒業してすぐ、キャリアの初期に遭遇したML関連のバグについて、実地で経験を積んでから回避する方法がわかったと述べています。
“I learned a lot of data science in school, but none of it was quite like all these things you’re [asking],” P7 told us at the end of their interview.
P7はインタビューの最後に、「私は学校でデータサイエンスをたくさん学びましたが、あなたが（質問している）ようなことは全くありませんでした」と話しています。
P5 said they did a lot of “learning by doing.”
P5は、多くのことを "Learning by doing "で学んだと述べています。
P11 provided further insight:
P11 は、さらなる洞察を示してくれました。

It was [hard to be], like, thrown into the wild, and have to learn all of this on the job.
野生の世界に放り込まれたようなもので、仕事中にすべてを学ばなければならないのは大変なことでした。
Coming out of [university in the US with a strong CS program], these are not things that anyone has ever taught right, at least in school...my mindset has always been a little bit more, I guess, practically oriented, even since the academic days, and that’s not to say we had great mental models—or frameworks or playbooks—for doing this.
私の考え方は、アカデミックな時代からずっと、もう少し実践的な方向に向いていました。

Our interviews with participants didn’t focus on what specific skills they could have learned in the classroom that would have prepared them better for their jobs.
参加者へのインタビューでは、教室でどんな具体的なスキルを学べば、よりよい準備ができたかについては、焦点を当てませんでした。
We leave this to future study and collaborations between academia and industry.
この点については、今後の研究や産学連携に委ねたいと思います。

### 5.2.2. Keeping GPUs Warm. 5.2.2. GPU を暖かく保つ。

P5 first mentioned the phrase “keeping GPUs warm”—i.e., running as many experiments as possible given computational resources, or making sure all GPUs were utilized at any given point in time:
P5が最初に述べたのは、「GPUを温存する」、つまり、計算機資源がある限りできるだけ多くの実験を行う、あるいは任意の時点ですべてのGPUを利用できるようにする、ということです。

One thing that I’ve noticed is, especially when you have as many resources as [large companies] do, that there’s a compulsive need to leverage all the resources that you have.
特に、大企業のように多くのリソースを持っている場合、持っているリソースをすべて活用しなければならないという強迫観念があることに気づきました。
And just, you know, get all the experiments out there.
そして、とにかく、あらゆる実験を行うことです。
Come up with a bunch of ideas; run a bunch of stuff.
たくさんのアイデアを出して、たくさんのことをやってみる。
I actually think that’s bad.
実は、これは良くないことだと思います。
You can be overly concerned with keeping your GPUs warm, [so much] so that you don’t actually think deeply about what the highest value experiment is.
GPUを温めることに気を取られすぎて、最も価値の高い実験が何なのか、深く考えなくなる可能性があります。
I think you can end up saving a lot more time—and obviously GPU cycles, but mostly end-to-end completion time—if you spend more efforts choosing the right experiment to run instead of [spreading yourself] thin.
GPUサイクルはもちろんですが、エンドツーエンドの完成までの時間を短縮するためには、実験対象を絞り込むことに力を注げば、より多くの時間を節約できると思います。
All these different experiments have their own frontier to explore, and all these frontiers have different options.
さまざまな実験には、それぞれ探求すべきフロンティアがあり、そのフロンティアにはさまざまなオプションがあります。
I basically will only do the most important thing from each project’s frontier at a given time, and I found that the net throughput for myself has been much higher.
私は基本的に、各プロジェクトのフロンティアから、その時点で最も重要なものだけを実行するようにしています。

In executing experiment ideas, we noticed a tradeoff between a guided search and random search.
実験アイデアを実行する際、ガイド付き探索とランダム探索の間にトレードオフがあることに気付いた。
Random searches were more suited to parallelization—e.g., hyperparameter searches or ideas that didn’t depend on each other.
ランダム検索は、ハイパーパラメータ検索や互いに依存しないアイデアなど、より並列化に向いていた。
Although computing infrastructure could support many different experiments in parallel, the cognitive load of managing such experiments was too cumbersome for participants (P5, P10, P18, P19).
コンピュータのインフラは多くの異なる実験を並列にサポートできるが、そのような実験の管理は参加者にとって面倒であった（P5、P10、P18、P19）。
In other words, having high velocity means drowning in a sea of versions of experiments.
言い換えれば、高速性を追求することは、多くのバージョンの実験の海に溺れることを意味する。
Rather, participants noted more success when pipelining learnings from one experiment into the next, like a guided search to find the best idea (P5, P10, P18).
むしろ、参加者は、最適なアイデアを見つけるためのガイド付きサーチのように、1つの実験から次の実験に学習をパイプライン化する方が成功すると述べている（P5, P10, P18）。
P18 described their ideological shift from random search to guided search:
P18は、ランダム検索からガイド付き検索への思想的転換を述べている。

Previously, I tried to do a lot of parallelization.
以前は、多くの並列化を試みていました。
I used to take, like, 5 ideas and try to run experimentation in parallel, and that definitely not only took my time, but I also focused less.
そのため、時間がかかるだけでなく、集中力も低下していました。
If I focus on one idea, a week at a time, then it boosts my productivity a lot more.
1つのアイデアに1週間ずつ集中することで、生産性が格段に向上するんです。

By following a guided search, engineers are, essentially, significantly pruning a tree of experiment ideas without executing them.
ガイド付きサーチを行うことで、エンジニアは本質的に、実験のアイデアを実行することなく、ツリーを大幅に刈り込んでいるのです。
Contrary to what they were taught in academia, P1 observed that some hyperparameter searches could be pruned early because hyperparameters had such little impact on the end-to-end pipeline:
ハイパーパラメータはエンドツーエンドのパイプラインにほとんど影響を与えないため、P1は、学界で教えられたのとは逆に、いくつかのハイパーパラメータ検索は早期に刈り込まれることを観察しました。

I remember one example where the ML team spent all this time making better models, and it was not helping [overall performance].
ある例では、MLチームがより良いモデルを作るために多くの時間を費やしましたが、[全体的なパフォーマンス]には役立たなかったのです。
Then everyone was so frustrated when one person on the controls team just tweaked one parameter [for the non-ML part of the pipeline], and [the end-to-end pipeline] worked so much better.
そのとき、コントロールチームの一人が（パイプラインの非ML部分の）パラメータを1つ調整しただけで、（エンドツーエンドのパイプラインが）とてもよく機能するようになったので、みんなとてもイライラしていたんです。
Like we’ve invested all this infrastructure for hyperparameter tuning a experiment, and I’m like what is this.
ハイパーパラメータのチューニングのために、これだけのインフラを投資して実験しているのに、これは何なんだ、と。
Why did this happen?
なぜ、こんなことになったのか？

Our takeaway is that while it may seem like there are unlimited computational resources, developer time and energy is the limiting reagent for ML experiments.
私たちが得たものは、計算資源は無限にあるように見えるかもしれませんが、開発者の時間とエネルギーがML実験の制限試薬であるということです。
At the end of the day, experiments are human-validated and deployed.
一日の終わりに、実験は人間が検証し、デプロイされます。
Mature ML engineers know their personal tradeoff between parallelizing disjoint experiment ideas and pipelining ideas that build on top of each other, ultimately yielding successful deployments.
熟練したMLエンジニアは、バラバラの実験アイデアを並列化することと、アイデアをパイプライン化して互いに積み重ねることの間のトレードオフを知っており、最終的にデプロイメントを成功させることができるのです。

### 5.2.3. Retrofitting an Explanation. 5.2.3. 説明のレトロフィット。

Right from the first interview, participants discussed uncovering good results from experiments, productionizing changes, and then trying to reason why these changes worked so well (P1, P2, P7, P12).
最初のインタビューから、参加者は、実験から良い結果を発見し、変更を加え、なぜその変更がうまくいったのか理由を考えようとすることを話していた（P1、P2、P7、P12）。
P1 said:
P1が言った。

A lot of ML is is like: people will claim to have like principled stances on why they did something and why it works.
MLの多くは、なぜそれをやったのか、なぜそれがうまくいくのかということについて、原則的なスタンスを持っていると主張するようなものです。
I think you can have intuitions that are useful and reasonable for why things should be good, but the most defining characteristic of [my most productive colleague] is that he has the highest pace of experimentation out of anyone.
でも、「私の最も生産的な同僚」の最大の特徴は、誰よりも実験のペースが速いということです。
He’s always running experiments, always trying everything.
彼はいつも実験をしていて、あらゆることを試しています。
I think this is relatively common—people just try everything and then backfit some nice-sounding explanation for why it works.
これは比較的よくあることだと思います。人は何でも試してみて、それがなぜうまくいくのか、聞こえのいい説明を後付けするものです。

We wondered, why was it even necessary to have an explanation for why something worked?
私たちは、なぜ何かがうまくいったという説明が必要なのだろうかと考えました。
Why not simply accept that, unlike in software, we may not have elegant, principled reasons for successful ML experiments?
ソフトウェアと違って、MLの実験が成功するためのエレガントで原理的な理由がないことを、単純に受け入れてはどうでしょう？
P2 hypothesized that such retrofitted explanations could guide future experiment ideas over a longer horizon.
P2は、そのような後付けの説明は、より長い視野で将来の実験のアイデアを導くことができると仮定した。
Alternatively, P7 mentioned that their customers sometimes demanded explanations for certain predictions:
また、P7は、顧客がある予測に対して説明を求めることがあると述べている。

Do I know why?
なぜかわかるか？
No idea.
わからない。
I have to convince people that, okay, we try our best.
私たちはベストを尽くしているのだと、みんなに納得してもらわなければなりません。
We try to [compute] correlations.
私たちは相関関係を計算しようとします。
We try to [compute] similarities.
類似性を計算しようとする。
Why is it different?
なぜ違うのでしょうか？
I have to make conjectures.
私は推測をしなければなりません。

We realized that although they could be false, retrofitted explanations can help with collaboration and business goals.
私たちは、間違った説明であっても、後付けされた説明はコラボレーションやビジネスゴールに役立つことがあることに気づきました。
If they satisfy customers and help organize teams around a roadmap of experiment ideas, maybe they are not so bad.
もし、それが顧客を満足させ、実験のアイデアのロードマップを中心にチームを組織するのに役立つのであれば、それほど悪いことではないのかもしれません。

### 5.2.4. Undocumented Tribal Knowledge. 5.2.4. 文書化されていない部族の知識。

P6, P10, P13, P14, P16, P17, and P19 each discussed pain points related to undocumented knowledge about ML experiments and pipelines amongst collaborators with more experience related to specific pipelines.
P6、P10、P13、P14、P16、P17、P19はそれぞれ、特定のパイプラインに関する経験が豊富な共同研究者の間で、ML実験やパイプラインに関する知識が文書化されていないことに関する苦痛について話しています。
Across interviews, it seemed like high velocity created many versions, which made it hard to maintain up-to-date documentation.
インタビューを通じて、高速で多くのバージョンが作成され、最新のドキュメントを維持することが困難であるように思えた。
P10 mentioned that there were parts of a pipeline that no one touched because it was already running in production, and the principal developer who knew most about it had left the company.
P10は、あるパイプラインがすでに本番稼動しており、そのパイプラインに最も詳しい主要開発者が退社したため、誰も触らない部分があったと述べている。
P16 said that “most of the, like, actual models were trained before [their] time.”
P16 は、「実際のモデルのほとんどは、彼らの時代より前にトレーニングされた」と述べています。
P14 described a “pipeline jungle” that was difficult to maintain:
P14 は、メンテナンスが困難な「パイプラインジャングル」を描写しました。

You end up with this pipeline jungle where everything’s super entangled, and it’s really hard to make changes, because just to make one single change, you have to hold so much context in your brain.
パイプラインのジャングルのように、すべてが超もつれ合っていて、変更を加えるのが本当に難しいのです。
You’re trying to think about like, okay this one change is gonna affect this system which affects this [other] system, [which creates]...the pipeline got to the point where it was very difficult to make even simple changes.
たった一つの変更が、このシステムに影響を与え、それがまた別のシステムに影響を与え、それがまた別のシステムを作り出す......といったことを考えようとすると、パイプラインは単純な変更でさえも非常に困難な状態になってしまいます。

While writing down institutional knowledge can be straightforward to do once, P6 discussed that in the ML setting, they learn faster than they can document; moreover, people don’t want to read so many different versions of documentation:
しかし、P6によると、MLの現場では、知識を文書化するよりも、学習する方が早く、また、多くの異なるバージョンの文書を読みたくないということでした。

There are people in the team, myself included, that have been on it for several years now, and so there’s some institutional knowledge embodied on the team that sometimes gets written down.
私を含め、このチームには数年来のメンバーがおり、チームとしての知識が蓄積されています。
But you know, even when it does get written down, maybe you will read them, but then, they kind of disappear to the ether.
でも、書き留められたとしても、読むことはできるかもしれないけれど、そのうちどこかに消えていってしまうんです。

Finally, P17 realized that poorly documented pipelines forced them to treat pipelines as black boxes:
最後に、P17は、パイプラインのドキュメントが不十分なため、パイプラインをブラックボックスとして扱わざるを得ないことに気づきました。
“Some of our models are pretty old and not well documented, so I don’t have great expectations for what they should be doing.”
「我々のモデルのいくつかはかなり古く、文書化もされていないため、パイプラインが何をすべきなのか、あまり期待できないのです。
Without intuition for how pipelines should perform, practitioner productivity can be stunted.
パイプラインがどのように機能すべきかという直感がなければ、実務担当者の生産性は阻害される可能性があります。

Takeaway.
テイクアウェイ
The MLOps anti-patterns described in this section reveal that ML engineering, as a field, is changing faster than educational resources can keep up.
本節で紹介したMLOpsのアンチパターンは、MLエンジニアリングが、分野として、教育資源が追いつくよりも速く変化していることを明らかにしています。
We see this as opportunities for new resources, such as classroom material (e.g., textbooks, courses) to prescribe the right engineering practices and rigor for the highly experimental discipline that is production ML, and automated documentation assistance for ML pipelines in organizations.
これは、プロダクションMLという非常に実験的な分野に対して、正しい工学的実践と厳密さを規定するための教室教材（例：教科書、コース）、組織におけるMLパイプラインの自動文書化支援といった新しいリソースの機会だと考えています。

## 5.3. Characterizing the “MLOps Stack” for Tool Builders 5.3. ツールビルダー向け「MLOpsスタック」の特徴づけ

MLOps tool builders may be interested in an organization of the dozens of tools, libraries, and services MLEs use to run ML and data processing pipelines.
MLOps ツールビルダーは、MLE が ML やデータ処理パイプラインを実行するために使用する数十のツール、ライブラリ、およびサービスの整理に関心があるかもしれません。
Although multiple MLEs reported having to “glue” open-source solutions together and having to build “homegrown” infrastructure as part of their work (P1, P2, P5, P6, P10, P12), an analysis of the various deployments reveals that tools can be grouped into a stack of four layers, depicted in Figure 2 and discussed further in Appendix D.
複数のMLEが、オープンソースのソリューションを「接着」したり、「自家製」インフラを構築する必要があると報告しているが（P1、P2、P5、P6、P10、P12）、さまざまな導入事例を分析した結果、ツールは図2に描かれている4層のスタックにグループ化できることが判明した（付録Dで詳しく説明）。
We discuss the four layers in turn:
この4つの層について順番に説明する。

- (1) Run Layer: A run is a record of an execution of an ML or data pipeline (and its components). Run-level data is often managed by data catalogs, model registries, and training dashboards. Example Tools: Weights & Biases, MLFlow, Hive metastores, AWS Glue (1) ラン層。 ランとは、MLやデータパイプライン（およびそのコンポーネント）の実行記録である。 ランレベルのデータは、データカタログ、モデルレジストリ、トレーニングダッシュボードで管理されることが多い。 ツールの例 Weights & Biases、MLFlow、Hiveメタストア、AWS Glue

- (2) Pipeline Layer: Finer-grained than a run, a pipeline further specifies the dependencies between artifacts and details of the corresponding computations. Pipelines can run ad-hoc or on a schedule. Pipelines change less frequently than runs, but more frequently than components. Example Tools: Papermill, DBT, Airflow, TensorFlow Extended, Sagemaker (2)パイプライン層。 パイプラインは、ランよりも粒度が細かく、成果物間の依存関係や対応する計算の詳細をさらに詳細に指定します。 パイプラインは、アドホックに実行することも、スケジュールに従って実行することもできます。 パイプラインの変更頻度はランよりも低いが、コンポーネントよりも高い。 ツールの例 Papermill、DBT、Airflow、TensorFlow Extended、Sagemakerなど。

- (3) Component Layer: A component is an individual node of computation in a pipeline, often a script inside a managed environment. Some MLEs reported having an organizationwide “library of common components” for pipelines to use, such as feature generation and model training (P2, P6). Example Tools: Python, Spark, PyTorch, TensorFlow (3) コンポーネント層。 コンポーネントとは、パイプラインにおける計算の個々のノードであり、多くの場合、管理環境内のスクリプトである。 MLE の中には、特徴量生成やモデル学習など、パイプラインが使用する「共通コンポーネントのライブラリ」を組織全体で保有していると報告した企業もある（P2、P6）。 ツールの例 Python、Spark、PyTorch、TensorFlowなど。

- (4) Infrastructure Layer: MLEs described a wide range of solutions, but most used cloud storage (e.g., S3), and GPU-backed cloud computing (AWS and GCP). Infrastructure changed far less frequently than other layers in the stack, but each change was more laborious and prone to wide-ranging consequences. Example Tools: Docker, AWS, GCP (4) インフラ層。 MLE はさまざまなソリューションについて説明しましたが、ほとんどの場合、クラウド ストレージ（S3 など）、GPU を使用したクラウドコンピューティング（AWS および GCP）を使用していました。 インフラストラクチャーは、スタックの他のレイヤーに比べて変更頻度がはるかに少ないですが、変更のたびに手間がかかり、広範囲に影響を及ぼしやすいものでした。 ツールの例 Docker、AWS、GCP

We found that MLEs used layers of abstraction (e.g., “config-based development”) as a way to manage complexity: most changes (especially high-velocity ones) were minor and limited to the Run Layer, such as selecting hyperparameters.
私たちは、MLEが複雑さを管理する方法として、抽象化のレイヤー（例えば「設定ベースの開発」）を使用していることを発見しました。ほとんどの変更（特に高速のもの）は、ハイパーパラメータの選択など、小規模で実行レイヤーに限られたものでした。
As the stack gets deeper, changes become less frequent:
スタックが深くなるにつれて、変更の頻度も少なくなります。
MLEs ran training jobs daily but modified Dockerfiles occasionally.
MLEは毎日トレーニングジョブを実行しますが、Dockerfileは時々修正します。
In the past, as MLOps tool builders, we (the authors) have incorrectly assumed uniform user access patterns across all layers of the MLOps stack.
過去に、MLOpsツールビルダーとして、私たち（著者）は、MLOpsスタックのすべてのレイヤーで、ユーザーのアクセスパターンが均一であると誤って想定していました。
Tool builders may want to pay attention to the layer(s) they are addressing and make sure they are not designing tools for the wrong layer(s).
ツール作成者は、自分たちが取り組んでいるレイヤーに注意を払い、間違ったレイヤー用のツールを設計していないことを確認する必要があるかもしれません。

Additionally, we noticed a high-level pattern in how interviewees discussed the tools they used: engineers seemed to prefer tools that significantly improved their experience with respect to the Three Vs (Section 4.2).
さらに、インタビュイーが使用するツールについて、あるハイレベルなパターンがあることに気づきました。
For example, experiment tracking tools increased engineers’ speed of iterating on feature or modeling ideas (P14, P15)—a velocity virtue.
例えば、実験追跡ツールは、エンジニアが機能またはモデリングのアイデアを反復する速度を向上させる（P14, P15）、これはベロシティの美徳である。
In another example, feature stores (i.e., tables of derived columns for ML models) helped engineers debug models because they could access the relevant historical versions of features used in training such models (P3, P6, P14, P17)—a versioning virtue.
別の例では、特徴ストア（ML モデルの派生カラムのテーブル）は、モデルのトレーニングに使用された特徴の履歴にアクセスできるため、エンジニアによるモデルのデバッグに役立ちます（P3、P6、P14、P17） - バージョン管理の徳目です。
MLOps tool builders may want to prioritize “10x” better experiences across velocity, validating early, or versioning for their products.
MLOps ツール開発者は、製品のベロシティ、早期検証、またはバージョニングにおいて、「10 倍」優れたエクスペリエンスを優先させたいと考えているかもしれません。

# 6. Conclusion 6. 結論

In this paper, we presented results from a semi-structured interview study of ML engineers spanning different organizations and applications to understand their workflow, best practices, and challenges.
この論文では、異なる組織やアプリケーションにまたがるMLエンジニアのワークフロー、ベストプラクティス、および課題を理解するための半構造化インタビュー調査の結果を発表しました。
We found that successful MLOps practices center around having high velocity, validating as early as possible, and maintaining multiple versions of models for minimal production downtime.
その結果、MLOpsの成功の鍵は、高い速度、可能な限り早い段階での検証、ダウンタイムを最小限に抑えるための複数バージョンのモデルの維持にあることがわかりました。
We reported on the experimental nature of production ML, aspects of effective model evaluation, and tips to sustain model performance over time.
我々は、プロダクションMLの実験的性質、効果的なモデル評価の側面、そして長期間にわたってモデルのパフォーマンスを維持するためのヒントについて報告しました。
Finally, we discussed MLOps pain points and anti-patterns discovered in our interviews to inspire new MLOps tooling and research ideas.
最後に、新しいMLOpsツールや研究のアイデアを得るために、インタビューで発見されたMLOpsのペインポイントやアンチパターンについて議論しました。
