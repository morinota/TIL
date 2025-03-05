
Sign up
サインアップ

Sign in
サインイン

Sign up
サインアップ

Sign in
サインイン



# T-LEAF: Taxonomy Learning and EvaluAtion Framework T-LEAF: タクソノミー学習と評価フレームワーク
Cen(Mia) Zhao
Cen(Mia) Zhao

Follow
フォローする
The Airbnb Tech Blog
Airbnbテックブログ

--
--

Listen
聞く
Share
共有する
How we applied qualitative learning, human labeling and machine learning to iteratively develop Airbnb’s Community Support Taxonomy.
私たちが質的学習、人間のラベリング、機械学習をどのように適用して、Airbnbのコミュニティサポートタクソノミーを反復的に開発したか。

By:Mia Zhao,Peggy Shao,Maggie Hanson,Peng Wang,Bo Zeng
著者: Mia Zhao, Peggy Shao, Maggie Hanson, Peng Wang, Bo Zeng



# Background 背景

Taxonomies are knowledge organization systems used to classify and organize information. 
タクソノミーは、情報を分類し整理するために使用される知識組織システムです。

Taxonomies use words to describe things — as opposed to numbers or symbols — and hierarchies to group things into categories. 
タクソノミーは、物事を説明するために言葉を使用し（数字や記号ではなく）、階層を用いて物事をカテゴリにグループ化します。

The structure of a taxonomy expresses how those things relate to each other. 
タクソノミーの構造は、それらの物事がどのように相互に関連しているかを表現します。

For instance, a Superhost is a type of Host and a Host is a type of Airbnb User. 
例えば、SuperhostはHostの一種であり、HostはAirbnb Userの一種です。

Taxonomies provide vital terminology control and enable downstream systems to navigate information and analyze consistent, structured data. 
タクソノミーは重要な用語管理を提供し、下流のシステムが情報をナビゲートし、一貫した構造化データを分析できるようにします。

Airbnb uses taxonomies in front-end products to help guests and hosts discover exciting stays or experiences, as well as inspirational content and customer support offerings. 
Airbnbは、フロントエンド製品でタクソノミーを使用して、ゲストやホストが魅力的な宿泊や体験を発見し、インスピレーションを与えるコンテンツやカスタマーサポートの提供を行います。

Airbnb also uses taxonomies in backstage tooling to structure data, organize internal information, and support machine learning applications. 
Airbnbは、バックエンドツールでもタクソノミーを使用してデータを構造化し、内部情報を整理し、機械学習アプリケーションをサポートします。

Classifying the types of issues Airbnb community members face is vital for several reasons: 
Airbnbコミュニティメンバーが直面する問題の種類を分類することは、いくつかの理由から重要です。

- Hosts and guests need to be able to describe issues to Airbnb in order to receive relevant help suggestions or get connected with the best support. 
- ホストとゲストは、関連するヘルプの提案を受けたり、最適なサポートに接続されたりするために、Airbnbに問題を説明できる必要があります。

- Support Ambassadors (Airbnb’s Community Support specialists) need quick and easy access to workflows that help them resolve issues for guests and Hosts. 
- サポートアンバサダー（Airbnbのコミュニティサポート専門家）は、ゲストやホストの問題を解決するためのワークフローに迅速かつ簡単にアクセスできる必要があります。

- Airbnb business units need to understand where and why guests and Hosts encounter problems so that we can improve our product and make the Airbnb experience better. 
- Airbnbのビジネスユニットは、ゲストやホストが問題に直面する場所と理由を理解する必要があり、製品を改善しAirbnbの体験を向上させることができます。

The Contact Reasons taxonomy is a new, consolidated issue taxonomy that supports all of these use cases. 
Contact Reasonsタクソノミーは、これらすべてのユースケースをサポートする新しい統合された問題タクソノミーです。

Before Contact Reasons, Community Support had siloed taxonomies for guests and Hosts, Support Ambassadors, and machine learning models that each used different words and structures to classify the same issues and relied on manual mapping efforts to keep in sync.
Contact Reasonsの前、コミュニティサポートは、ゲストとホスト、サポートアンバサダー、機械学習モデルのために分離されたタクソノミーを持っており、それぞれが同じ問題を分類するために異なる言葉と構造を使用し、手動でのマッピング作業に依存して同期を保っていました。

The consolidation of disjointed issue taxonomies into Contact Reasons was the first project of its kind at Airbnb. 
分離された問題タクソノミーをContact Reasonsに統合することは、Airbnbにおけるその種の最初のプロジェクトでした。

The development of such a new taxonomy requires iterative learning: create/revise the taxonomy by taxonomists; roll out to train ML model, product and services; evaluate the quality of the taxonomy and identify areas for improvement. 
このような新しいタクソノミーの開発には反復学習が必要です：タクソノミストによるタクソノミーの作成/改訂、MLモデル、製品、サービスのトレーニングへの展開、タクソノミーの品質評価と改善点の特定です。

Before this work, there was no systematic process in place to evaluate taxonomy development or performance and the iteration was mostly subjective and qualitative. 
この作業の前には、タクソノミーの開発やパフォーマンスを評価するための体系的なプロセスは存在せず、反復は主に主観的かつ定性的でした。

To accelerate the iterative development with more quantitative and objective evaluation of the quality of the taxonomy, we created T-LEAF, a Taxonomy Learning and Evaluation Framework, to quantitatively evaluate taxonomy from three perspectives: coverage, usefulness, and agreement. 
タクソノミーの品質をより定量的かつ客観的に評価することで反復開発を加速するために、私たちはT-LEAF（Taxonomy Learning and Evaluation Framework）を作成し、カバレッジ、有用性、合意の3つの視点からタクソノミーを定量的に評価します。



# Challenges in Evaluating the New Taxonomy 新しい分類法の評価における課題

In the Airbnb Community Support domain, new taxonomies or taxonomy nodes often need to be created before we have either real-world data or clear downstream workflow applications. 
Airbnbコミュニティサポートの分野では、実世界のデータや明確な下流のワークフローアプリケーションがない状態で、新しい分類法や分類ノードを作成する必要があることがよくあります。

Without a consistent quantitative evaluation framework to generate input metrics, it’s difficult to gauge the quality of a new taxonomy (or a taxonomy version) when directly applying it to downstream applications.
入力メトリクスを生成するための一貫した定量的評価フレームワークがないと、新しい分類法（または分類法のバージョン）を下流のアプリケーションに直接適用した際の品質を評価することが難しくなります。



# Lack of quantitative evaluation framework 定量評価フレームワークの欠如

Taxonomies are typically developed by qualitative-centric approaches¹. 
分類体系は通常、質的中心のアプローチによって開発されます¹。

When we started prototyping the new taxonomy, we evaluated feedback from existing users, and recruited guests and Hosts for several rounds of user research to generate insights. 
新しい分類体系のプロトタイピングを始めたとき、既存のユーザからのフィードバックを評価し、洞察を得るためにゲストとホストを数回のユーザーリサーチに募集しました。

While qualitative evaluation like domain expert review is helpful in identifying high-level challenges and opportunities, it is insufficient for providing evaluation at scale, due to small sample sizes and potential sample bias from users participating in the research. 
ドメイン専門家レビューのような質的評価は、高レベルの課題や機会を特定するのに役立ちますが、サンプルサイズが小さく、研究に参加するユーザからの潜在的なサンプルバイアスのため、スケールでの評価を提供するには不十分です。



# Lengthy and iterative product cycle for taxonomy launches
分類法の開発と立ち上げは、実質的で信頼できる定量的フィードバックを得るために数四半期を要する長期的かつ反復的なプロセスです。典型的なプロセスには以下が含まれます：
- 製品要件またはデータ駆動分析に基づく分類法の発見と開発
- 必要なデザインとコンテンツの更新を含むバックエンド環境とフロントエンド表面を統合するための生産変更
- MLモデルの（再）ラベル付けトレーニングデータ、再トレーニング、およびデプロイメント
- ユーザーフィードバックに関するログ記録とデータ分析
T-LEAF以前は、分類法の開発プロセスは新しい分類法の効果を測定するために出力メトリックのみに依存していました。これは、1) 大きな変更には実験とテストに長い時間がかかること、2) 新しいノードの追加や更新のような小さな変更はテストされないことを意味します。これらの2つの痛点は、T-LEAFフレームワークによって一貫した定期的なスコアリングで対処できます。
T-LEAFは、分類法の開発における定量的評価を増やし、上記の2つの痛点に対処して分類法の開発の反復を加速するために開発されました。



# Taxonomy Learning and EvaluAtion Framework (T-LEAF) タクソノミー学習と評価フレームワーク (T-LEAF)



# Quality of a Taxonomy タクソノミーの質

T-LEAF framework measures the quality of a taxonomy in three aspects: 1) coverage, 2) usefulness and 3) agreement.
T-LEAFフレームワークは、タクソノミーの質を3つの側面で測定します：1) カバレッジ、2) 有用性、3) 一致。



# Coverage カバレッジ

Coverage indicates how well a taxonomy can classify the scope of real-world objects. 
カバレッジは、分類体系が実世界のオブジェクトの範囲をどれだけうまく分類できるかを示します。

In Contact Reasons, coverage score evaluates how well the taxonomy captures the reasons guests and Hosts contact Airbnb’s Community Support team. 
「Contact Reasons」では、カバレッジスコアが、ゲストとホストがAirbnbのコミュニティサポートチームに連絡する理由を分類体系がどれだけうまく捉えているかを評価します。

When ‘coverage’ is low, a lot of user issues (data objects) will not be covered by the taxonomy and become ‘Other’ or ‘Unknown’. 
「カバレッジ」が低いと、多くのユーザーの問題（データオブジェクト）が分類体系にカバーされず、「その他」または「不明」となります。

Coverage Score = 1 - percentage of data classified as “other” or “undefined.” 
カバレッジスコア = 1 - 「その他」または「未定義」と分類されたデータの割合。



# Usefulness 有用性

Usefulness shows how evenly objects distribute across the structure of the taxonomy into meaningful categories. 
有用性は、オブジェクトが意味のあるカテゴリに分類されるタクソノミーの構造全体にどれだけ均等に分布しているかを示します。

If a taxonomy is too coarse, i.e., has too few nodes or categories, the limited number of options may not adequately distinguish between the objects that are being described. 
タクソノミーがあまりにも粗い場合、つまりノードやカテゴリの数が少なすぎると、限られた選択肢では記述されているオブジェクトを十分に区別できない可能性があります。

On the other hand, if a taxonomy is too granular, it may fail to explain similarities between objects. 
一方、タクソノミーがあまりにも細かすぎると、オブジェクト間の類似点を説明できなくなる可能性があります。

In T-LEAF, for a benchmark dataset with n examples (e.g., distinct user issues), we hypothesize that a taxonomy with sqrt(n) number of nodes² gives a good balance between ‘too coarse’ and ‘too granular’. 
T-LEAFでは、n個の例（例えば、異なるユーザーの問題）を持つベンチマークデータセットに対して、ノード数が$\sqrt{n}$のタクソノミーが「粗すぎる」と「細かすぎる」の間で良いバランスを提供すると仮定します。

For any input x, we compute a split score from (0,1] to evaluate the ‘usefulness’: 
任意の入力$x$に対して、‘有用性’を評価するために(0,1]の範囲でスプリットスコアを計算します。

We want to evaluate the data deviation by assuming the normal distribution. 
私たちは、正規分布を仮定してデータの偏差を評価したいと考えています。

For example, with 100 distinct user issues, if we split into 1 (‘too coarse’) or 100 categories (‘too granular’), the usefulness score would be close to 0; 
例えば、100の異なるユーザーの問題がある場合、1（‘粗すぎる’）または100カテゴリ（‘細かすぎる’）に分割すると、有用性スコアは0に近くなります。

if we split into 10 categories, the usefulness score would be 1. 
10カテゴリに分割すると、有用性スコアは1になります。



# Agreement 合意

Agreement captures the inter-rater reliability given the taxonomy. 
合意は、分類に基づく評価者間の信頼性を捉えます。
We propose two ways to evaluate agreement. 
私たちは、合意を評価するための2つの方法を提案します。



## Human Label Inter-rater Agreement 人間のラベルの評価者間合意

Multiple human annotators annotate the same data according to the taxonomy definition and we calculate the inter-rater reliabilities using Cohen’s Keppa in the range of [-1, 1]:
複数の人間のアノテーターが、分類法の定義に従って同じデータに注釈を付け、私たちはCohenのKappaを使用して評価者間の信頼性を[-1, 1]の範囲で計算します。



## ML Model Training Accuracy MLモデルのトレーニング精度

Having multiple human raters annotate one data set can be expensive. 
複数の人間の評価者が1つのデータセットに注釈を付けることは高価になる可能性があります。 
In reality, most data is annotated by just one human. 
実際には、ほとんどのデータは1人の人間によって注釈が付けられています。 
In Airbnb’s Community Support, each customer issue/ticket is processed by one agent and agents label the ticket’s issue type based on the taxonomy. 
Airbnbのコミュニティサポートでは、各顧客の問題/チケットは1人のエージェントによって処理され、エージェントはタクソノミーに基づいてチケットの問題タイプにラベルを付けます。 
We train a ML model based on this single-rater labeled training data and then apply the model over the training data to measure the training accuracy. 
私たちは、この単一評価者によってラベル付けされたトレーニングデータに基づいてMLモデルをトレーニングし、その後、トレーニングデータにモデルを適用してトレーニング精度を測定します。 
If the taxonomy is well defined (i.e., with high ‘agreement’), then similar issues (data points) should have similar labels even though these labels come from different agents. 
タクソノミーが明確に定義されている場合（すなわち、高い「合意」を持つ場合）、類似の問題（データポイント）は、これらのラベルが異なるエージェントから来ているにもかかわらず、類似のラベルを持つべきです。 
ML models trained over highly agreed(consistent) training dataset should have high training accuracy. 
高い合意（整合性）のあるトレーニングデータセットでトレーニングされたMLモデルは、高いトレーニング精度を持つべきです。 
We have done experiments comparing the multi-label inter-rater agreement approach and ML training accuracy over single-rated training data. 
私たちは、マルチラベルの評価者間合意アプローチと単一評価データにおけるMLトレーニング精度を比較する実験を行いました。 
Results are shown in Table 1. 
結果は表1に示されています。 
We observed that for both methods: 1) accuracies were similar for the top two levels of the taxonomy (L1 and L2 issues are defined in the next section) and; 2) there were similar areas of confusion in both approaches. 
私たちは、両方の方法において次のことを観察しました：1）精度はタクソノミーの上位2レベル（L1およびL2の問題は次のセクションで定義されます）で類似しており、2）両方のアプローチで混乱の類似した領域がありました。 
If taxonomy nodes are clear enough for humans to perform tagging, the consistency rate increases and the model can better capture human intent. 
タクソノミーノードが人間がタグ付けを行うのに十分に明確であれば、一貫性の割合が増加し、モデルは人間の意図をよりよく捉えることができます。 
The opposite is also true; model training accuracy is negatively impacted if end users are confused by options or unable to choose proper categories. 
逆もまた真であり、エンドユーザーが選択肢に混乱したり、適切なカテゴリを選択できない場合、モデルのトレーニング精度は悪影響を受けます。 
It took 1 analyst and 9 annotators about a month to create the multi-rater dataset. 
マルチレーターデータセットを作成するのに、1人のアナリストと9人の注釈者が約1ヶ月かかりました。 
In contrast, it took one ML engineer a day to train a ML model over the single-rated data and calculate the training accuracy. 
対照的に、1人のMLエンジニアが単一評価データに対してMLモデルをトレーニングし、トレーニング精度を計算するのに1日かかりました。 
As shown in Table 1, ML Training accuracy provides a similar evaluation of taxonomy’s ‘agreement’ quality. 
表1に示されているように、MLトレーニング精度はタクソノミーの「合意」品質の類似した評価を提供します。



# Developing the Contact Reason Taxonomy using T-LEAF
連絡理由の分類法は、レベル1（L1）の広いカテゴリからレベル2（L2）の狭いカテゴリ、そしてレベル3（L3）の特定の問題に至るまで、約200のノードで構成されています。例えば：
- あなたの予約に関する問題 (L1)
- 清潔さと健康に関する懸念 (L2)
- リスティング内の煙やその他の臭い (L3)
While the old taxonomy had unpredictable levels of granularity, depending on the section, Contact Reasons has a consistent, three-level structure that better supports our continuous evaluation framework.
古い分類法は、セクションによって予測不可能な粒度のレベルを持っていましたが、連絡理由は一貫した三層構造を持ち、私たちの継続的評価フレームワークをより良くサポートします。
We utilized T-LEAF in the transition from the old taxonomy to the new taxonomy (Contact Reasons) to enable a faster feedback loop and provide a quantified quality control before launching the new taxonomy into production environments (Figure 3).
私たちは、古い分類法から新しい分類法（連絡理由）への移行にT-LEAFを利用し、より迅速なフィードバックループを可能にし、新しい分類法を本番環境に投入する前に定量的な品質管理を提供しました（図3）。
First, we sent a real-world dataset to Airbnb Community Support Labs (CS Labs) — a group of skilled and tenured Support Ambassadors — for human annotation.
まず、私たちは実世界のデータセットをAirbnb Community Support Labs（CS Labs）に送信しました。これは、熟練したサポート大使のグループです。
Then, we used T-LEAF scores as an input to the taxonomy development process.
次に、私たちはT-LEAFスコアを分類法開発プロセスへの入力として使用しました。
Using that input, the Core Machine Learning (CoreML) Engineering team and the Taxonomy team collaborated to significantly improve T-LEAF scores before running experiments in production.
その入力を使用して、Core Machine Learning（CoreML）エンジニアリングチームと分類法チームは、本番環境での実験を行う前にT-LEAFスコアを大幅に改善するために協力しました。
To evaluate the Contact Reasons taxonomy in one of these production environments, we reviewed its performance in Airbnb bot³.
これらの本番環境の1つで連絡理由の分類法を評価するために、私たちはAirbnb bot³でのパフォーマンスをレビューしました。
Airbnb bot is one of Community Support’s core products that helps guests and Hosts self-solve issues and connect to Support Ambassadors when necessary.
Airbnb botは、ゲストとホストが問題を自己解決し、必要に応じてサポート大使に接続するのを助ける、コミュニティサポートのコア製品の1つです。
We found that the improvements to the Contact Reason taxonomy as measured by T-LEAF’s metrics of coverage, usefulness, and agreement also translated to actual improvements in issue coverage, self-solve effectiveness, and issue prediction accuracy.
私たちは、T-LEAFのカバレッジ、有用性、合意の指標で測定された連絡理由の分類法の改善が、問題のカバレッジ、自己解決の効果、および問題予測の精度の実際の改善にもつながることを発見しました。



# A higher T-LEAF coverage score leads to greater issue coverage in production
T-LEAFカバレッジスコアが高いほど、製品における問題のカバレッジが向上する

After launching the Contact Reasons taxonomy, we examined 4-months of production data and found that 1.45% of issues were labeled “It’s something else,” which is 5.8% less than the old taxonomy. 
Contact Reasonsタクソノミーを導入した後、4か月間の生産データを調査したところ、問題の1.45%が「それ以外」とラベル付けされており、これは旧タクソノミーより5.8%少ないことがわかりました。 
This is consistent with T-LEAF coverage score improvement (5.3% more coverage than the previous version).
これは、T-LEAFカバレッジスコアの改善（前のバージョンより5.3%のカバレッジ向上）と一致しています。



# A higher usefulness score leads to more issues being resolved through self-service
より高い有用性スコアは、自己サービスを通じてより多くの問題が解決されることにつながります。

For example, in the new taxonomy, there are two new nodes called “Cancellations and refunds > Canceling a reservation you booked > Helping a Host with a cancellation” and “Cancellations and refunds > Canceling a reservation you’re hosting > Helping a guest with a cancellation.” 
例えば、新しい分類法には、「キャンセルと返金 > 予約した予約のキャンセル > ホストのキャンセルを手伝う」と「キャンセルと返金 > あなたがホストしている予約のキャンセル > ゲストのキャンセルを手伝う」という2つの新しいノードがあります。

The old taxonomy only have nodes for “Reservations > Cancellations > Host-initiated” and “Reservations > Cancellations >Guest-initiated”, which did not have granularity to determine when the guest or Host seeking support is not the one requesting the cancellation. 
古い分類法には「予約 > キャンセル > ホスト主導」と「予約 > キャンセル > ゲスト主導」のノードしかなく、サポートを求めるゲストまたはホストがキャンセルを要求していない場合を特定するための詳細さがありませんでした。

With the new nodes, we developed a machine learning model that drives traffic to tailored cancellation workflows⁴. 
新しいノードを使用して、特定のキャンセルワークフローにトラフィックを誘導する機械学習モデルを開発しました⁴。

This ensures that guests receive the appropriate refund and Host cancellation penalties are applied only when relevant, all without needing to contact Airbnb Support Ambassadors. 
これにより、ゲストは適切な返金を受け取り、ホストのキャンセルペナルティは関連する場合にのみ適用され、すべてAirbnbサポートアンバサダーに連絡する必要がなくなります。



# A higher T-LEAF agreement score results in more accurate issue prediction
T-LEAF合意スコアが高いほど、問題予測がより正確になります。

Compared to issue prediction models built on the old taxonomy, the model built on the new taxonomy has improved accuracy by 9%. 
古い分類に基づいて構築された問題予測モデルと比較して、新しい分類に基づいて構築されたモデルは、9%の精度向上を示しました。

This means that the category the ML model predicts for an issue is more likely to match the category selected by the Support Ambassador.
これは、MLモデルが問題に対して予測するカテゴリが、サポートアンバサダーによって選択されたカテゴリと一致する可能性が高いことを意味します。



# Conclusion 結論

A quantitative framework to evaluate taxonomy supports faster iterations and reduces the risk of launching major taxonomy transformations, which has positive impacts for all of our audiences: guests, Hosts, Support Ambassadors, and Airbnb businesses. 
分類法を評価するための定量的フレームワークは、より迅速な反復をサポートし、大規模な分類法の変革を開始するリスクを軽減します。これは、私たちのすべてのオーディエンス（ゲスト、ホスト、サポートアンバサダー、Airbnbビジネス）にとってポジティブな影響をもたらします。

The T-LEAF framework that scores the quality of taxonomy in the aspects of coverage, usefulness, agreement, has now been applied to a production taxonomy in Community Support and results show that using this methodology for quantitative taxonomy evaluation can lead to better model performance and larger issue coverage. 
カバレッジ、有用性、合意の観点から分類法の質をスコアリングするT-LEAFフレームワークは、現在、コミュニティサポートのプロダクション分類法に適用されており、この定量的分類法評価の方法論を使用することで、モデルのパフォーマンスが向上し、より多くの問題をカバーできることが示されています。

Developing, piloting, and establishing T-LEAF as part of our continuous improvement framework for taxonomy evolution has been a collaborative effort across teams. 
T-LEAFを分類法の進化のための継続的改善フレームワークの一部として開発、試行、確立することは、チーム間の協力的な努力でした。

The CoreML team partnered closely with Taxonomy, Product, and CS Labs to create this new model for iterative development of issue categorization and prediction. 
CoreMLチームは、問題の分類と予測の反復的な開発のための新しいモデルを作成するために、分類法、製品、CSラボと密接に連携しました。

Having piloted this new way of working on Contact Reasons, we’re confident we’ll see more positive results as we continue to apply the T-LEAF methodology to future taxonomy initiatives. 
コンタクト理由に関するこの新しい作業方法を試行したことで、今後の分類法の取り組みにT-LEAFの方法論を適用し続けることで、より良い結果が得られると確信しています。

[1]: Szopinski, D., Schoormann, T., & Kundisch, D. (2019). Because Your Taxonomy is Worth IT: towards a Framework for Taxonomy Evaluation.ECIS.https://aisel.aisnet.org/ecis2019_rp/104/  
[1]: Szopinski, D., Schoormann, T., & Kundisch, D. (2019). あなたの分類法はそれだけの価値がある: 分類法評価のためのフレームワークに向けて。ECIS. https://aisel.aisnet.org/ecis2019_rp/104/

[2]: Carlis, J., & Bruso, K. (2012). RSQRT: AN HEURISTIC FOR ESTIMATING THE NUMBER OF CLUSTERS TO REPORT. Electronic commerce research and applications, 11(2), 152–158.https://doi.org/10.1016/j.elerap.2011.12.006  
[2]: Carlis, J., & Bruso, K. (2012). RSQRT: 報告するクラスタ数を推定するためのヒューリスティック。電子商取引研究と応用、11(2)、152–158。https://doi.org/10.1016/j.elerap.2011.12.006

[3]: Intelligent Automation Platform: Empowering Conversational AI and Beyond at Airbnb.https://medium.com/airbnb-engineering/intelligent-automation-platform-empowering-conversational-ai-and-beyond-at-airbnb-869c44833ff2  
[3]: インテリジェントオートメーションプラットフォーム: Airbnbにおける会話型AIとその先を支える。https://medium.com/airbnb-engineering/intelligent-automation-platform-empowering-conversational-ai-and-beyond-at-airbnb-869c44833ff2

[4]: Task-Oriented Conversational AI in Airbnb Customer Support.https://medium.com/airbnb-engineering/task-oriented-conversational-ai-in-airbnb-customer-support-5ebf49169eaa  
[4]: Airbnbカスタマーサポートにおけるタスク指向の会話型AI。https://medium.com/airbnb-engineering/task-oriented-conversational-ai-in-airbnb-customer-support-5ebf49169eaa

Interested in working at Airbnb? Check out these open roles: 
Airbnbで働くことに興味がありますか？これらのオープンポジションをチェックしてください：

Senior Staff Data Architect, Community Support Platform  
シニアスタッフデータアーキテクト、コミュニティサポートプラットフォーム

Sr. Product Manager, Community Experience Products  
シニアプロダクトマネージャー、コミュニティエクスペリエンス製品

Product Manager, Claims Experience  
プロダクトマネージャー、クレームエクスペリエンス



# Acknowledgments 謝辞

Thanks to CS Labs for labeling support on existing and new taxonomies! 
既存および新しい分類法に対するラベリングサポートを提供してくれたCS Labsに感謝します！

Thanks to Pratik Shah, Rachel Lang, Dexter Dilla, Shuo Zhang, Zhiheng Xu, Alex Zhou, Wayne Zhang, Zhenyu Zhao, Jerry Hong, Gavin Li, Kristen Jaber, Aliza Hochsztein, Naixin Zhang, Gina Groom, Robin Foyle, Parag Hardas, Zhiying Gu, Kevin Jungmeisteris, Jonathan Li-On Wing, Danielle Martin, Bill Selman, Hwanghah Jeong, Stanley Wong, Lindsey Oben, Chris Enzaldo, Jijo George, Ravish Gadhwal, and Ben Ma for supporting our successful CS taxonomy launch and workflow related applications! 
Pratik Shah、Rachel Lang、Dexter Dilla、Shuo Zhang、Zhiheng Xu、Alex Zhou、Wayne Zhang、Zhenyu Zhao、Jerry Hong、Gavin Li、Kristen Jaber、Aliza Hochsztein、Naixin Zhang、Gina Groom、Robin Foyle、Parag Hardas、Zhiying Gu、Kevin Jungmeisteris、Jonathan Li-On Wing、Danielle Martin、Bill Selman、Hwanghah Jeong、Stanley Wong、Lindsey Oben、Chris Enzaldo、Jijo George、Ravish Gadhwal、Ben Maに感謝します。彼らは私たちの成功したCS分類法の立ち上げとワークフロー関連のアプリケーションを支援してくれました！

Thank Joy Zhang, Andy Yasutake, Jerry Hong, Lianghao Li, Susan Stevens, Evelyn Shen, Axelle Vivien, Lauren Mackevich, Cynthia Garda, for reviewing, editing and making great suggestions to the blog post! 
Joy Zhang、Andy Yasutake、Jerry Hong、Lianghao Li、Susan Stevens、Evelyn Shen、Axelle Vivien、Lauren Mackevich、Cynthia Gardaに感謝します。彼らはブログ投稿のレビュー、編集、素晴らしい提案をしてくれました！

Last but not least, we appreciate Joy Zhang, Andy Yasutake, Raj Rajagopal, Tina Su and Cynthia Garda for leadership support! 
最後に、Joy Zhang、Andy Yasutake、Raj Rajagopal、Tina Su、Cynthia Gardaのリーダーシップサポートに感謝します！



## Sign up to discover human stories that deepen your understanding of the world. 
世界の理解を深める人間の物語を発見するためにサインアップしてください。



## Free 無料

Distraction-free reading. No ads.  
気を散らさない読書。広告なし。

Organize your knowledge with lists and highlights.  
リストやハイライトを使って知識を整理しましょう。

Tell your story. Find your audience.  
自分の物語を語り、聴衆を見つけましょう。



## Membership メンバーシップ

Read member-only stories
メンバー限定のストーリーを読む

Support writers you read most
最もよく読む作家をサポートする

Earn money for your writing
あなたの執筆に対してお金を稼ぐ

Listen to audio narrations
オーディオナレーションを聞く

Read offline with the Medium app
Mediumアプリを使ってオフラインで読む



## Published in The Airbnb Tech Blog

Creative engineers and data scientists building a world where you can belong anywhere.
クリエイティブなエンジニアとデータサイエンティストが、どこにでも属することができる世界を構築しています。  
http://airbnb.io



## Written by Cen(Mia) Zhao 著者: Cen(Mia) Zhao



## No responses yet まだ応答はありません

What are your thoughts? あなたの考えは何ですか？
Also publish to my profile 私のプロフィールにも公開します
Help 助けて
Status ステータス
About この件について
Careers キャリア
Press プレス
Blog ブログ
Privacy プライバシー
Terms 利用規約
Text to speech テキスト読み上げ
Teams チーム
