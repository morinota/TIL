refs: <https://www.arxiv.org/pdf/2511.18013>

Save, Revisit, Retain: A Scalable Framework for Enhancing User Retention in Large-Scale Recommender Systems
保存、再訪、retention：大規模レコメンダーシステムにおけるユーザーretentionを強化するためのスケーラブルなフレームワーク

### 0.1. Weijie Jiang, Armando Ordorica, Jaewon Yang, Olafur Gudmundsson, Yucheng Tu[*], Huizhong Duan Pinterest Inc

weijiejiang,aordorica,jaewonyang,ogudmundsson,ytu,<hduan@pinterest.com>  

## 1. **Abstract**  

**要約**  

User retention is a critical objective for online platforms like Pinterest, as it strengthens user loyalty and drives growth through repeated engagement.  
**ユーザーretentionは、Pinterestのようなオンラインプラットフォームにとって重要な目標**であり、ユーザーの忠誠心を強化し、繰り返しのエンゲージメントを通じて成長を促進します。
A key indicator of retention is revisitation, i.e., when users return to view previously saved content, a behavior often sparked by personalized recommendations and user satisfaction.  
**retentionの重要な指標は再訪**であり、ユーザーが以前に保存したコンテンツを再度表示することです。この行動は、パーソナライズされた推薦やユーザーの満足度によって引き起こされることが多いです。  
However, modeling and optimizing revisitation poses significant challenges.  
しかし、再訪のモデル化と最適化には重要な課題があります。
One core difficulty is accurate attribution: it is often unclear which specific user actions or content exposures trigger a revisit, since many confounding factors (e.g., content quality, user interface, notifications, or even changing user intent) can influence return behavior.  
一つの主要な難しさは正確な帰属です。**どの特定のユーザーアクションやコンテンツの露出が再訪を引き起こすのかはしばしば不明であり、多くの混乱要因（例：コンテンツの質、ユーザーインターフェース、通知、あるいはユーザーの意図の変化など）が帰還行動に影響を与える可能性があります。**  
Additionally, the scale and timing of revisitations introduce further complexity; users may revisit content days or even weeks after their initial interaction, requiring the system to maintain and associate extensive historical records across millions of users and sessions.  
さらに、**再訪のスケールとタイミング**はさらなる複雑さをもたらします。ユーザーは初回のインタラクションから数日または数週間後にコンテンツを再訪することがあり、システムは数百万のユーザーとセッションにわたって広範な履歴記録を維持し、関連付ける必要があります。  
These complexities render existing methods insufficient for robustly capturing and optimizing long-term revisitation.  
これらの複雑さにより、既存の方法では長期的な再訪を堅牢に捉え、最適化することが不十分になります。  

<!-- ここまで読んだ! -->

To address these gaps, we introduce a novel, lightweight, and interpretable framework for modeling revisitation behavior and optimizing long-term user retention in Pinterest’s search-based recommendation context.  
これらのギャップに対処するために、私たちはPinterestの検索ベースの推薦コンテキストにおける再訪行動をモデル化し、長期的なユーザーretentionを最適化するための新しい軽量で解釈可能なフレームワークを導入します。  
By defining a surrogate attribution process that links saves to subsequent revisitations, we reduce noise in the causal relationship between user actions and return visits.  
保存とその後の再訪を結びつける代理帰属プロセスを定義することにより、**ユーザーアクションと帰還訪問の因果関係におけるノイズを減少**させます。  
Our scalable event aggregation pipeline enables large-scale analysis of user revisitation patterns and enhances the ranking system’s ability to surface items with high retention value.  
私たちのスケーラブルなイベント集約パイプラインは、ユーザーの再訪パターンの大規模分析を可能にし、ランキングシステムが高いretention価値を持つアイテムを表面化する能力を向上させます。  
Deployed on Pinterest’s Related Pins surface to serve 500+ million users, the framework led to a significant lift of 0.1% in active users without additional computational costs.  
Pinterestの関連ピンの表面に展開され、5億人以上のユーザーにサービスを提供するこのフレームワークは、**追加の計算コストなしでアクティブユーザーを0.1%増加させる重要な効果**をもたらしました。  
Our data analysis reveals novel insights, such as the impact of content topics on revisitation rates; for example, users are more likely to revisit aesthetically pleasing topics.  
私たちのデータ分析は、**コンテンツのトピックが再訪率に与える影響**などの新しい洞察を明らかにします。例えば、ユーザーは美的に魅力的なトピックを再訪する可能性が高いです。  

<!-- ここまで読んだ! -->

## 2. Introduction   はじめに  

User retention is an important business objective for online platforms such as Pinterest, as it fosters stronger relationships with users, builds loyalty, and ultimately drives both growth and revenue.  
**ユーザーretentionは、Pinterestのようなオンラインプラットフォームにとって重要なビジネス目標**であり、**ユーザーとの関係を強化し、忠誠心を築き、最終的には成長と収益を促進**します。  
A key behavior indicating strong user retention is revisitation (Zhang et al. 2021), which occurs when a user returns to view specific content that they previously accessed and saved.  
**強いユーザーretentionを示す重要な行動は再訪（Zhang et al. 2021）**であり、これはユーザーが以前にアクセスして保存した特定のコンテンツを再度表示する際に発生します。
(ここでの再訪(revisit)は、Pinterestへの再訪というよりは、Pinterest内の特定のコンテンツへの再訪を意味してる...??　少なくともPinterestではそっちをretentionのより有効なproxyとして捉えている! :thinking:)
This behavior often signals user satisfaction, typically driven by personalized content and recommendations.  
この行動はしばしばユーザーの満足度を示し、通常はパーソナライズされたコンテンツや推薦によって促進されます。  
Therefore, identifying and leveraging previously saved content that encourages users to return can serve as a valuable signal for fostering long-term user retention.  
したがって、ユーザーが再訪することを促す以前に**保存されたコンテンツを特定し活用することは、長期的なユーザーretentionを促進するための貴重な信号**となります。  

Modeling and optimizing revisitation behavior presents several challenges.  
再訪行動のモデル化と最適化にはいくつかの課題があります。  
The first is attribution: it is difficult to determine what exactly triggers a user to revisit.  
**最初の課題は帰属です。ユーザーが再訪する正確なトリガーを特定することは困難**です。  
Many confounding factors can influence revisitation, such as content quality, user experience, and platform notifications or reminders (Adar, Teevan, and Dumais 2008; Zhang et al. 2021).  
再訪には、コンテンツの質、ユーザー体験、プラットフォームの通知やリマインダー（Adar, Teevan, and Dumais 2008; Zhang et al. 2021）など、多くの混乱要因が影響を与える可能性があります。  
For instance, if a user returns with a completely different intent than in their previous session, it would be inappropriate to attribute that revisit to their earlier activities.  
**例えば、ユーザーが前回のセッションとはまったく異なる意図で戻ってきた場合、その再訪を以前の活動に帰属させるのは不適切**です。  

The second challenge concerns scale.  
第二の課題はスケールに関するものです。  
Since revisitations can occur within a day, a week, or even a month (Adar, Teevan, and Dumais 2009), tracking them effectively requires maintaining extensive records of user activity over indefinite periods.  
再訪は1日、1週間、あるいは1ヶ月の間に発生する可能性があるため（Adar, Teevan, and Dumais 2009）、それらを効果的に追跡するには、無期限にわたるユーザー活動の広範な記録を維持する必要があります。  (まあ1ヶ月くらいだったらDWHにretentionできるかなとは思う...!:thinking:)
This creates significant data processing and scaling challenges (Jin et al. 2017).  
これにより、重要なデータ処理とスケーリングの課題が生じます（Jin et al. 2017）。  
To date, there has been little concrete research on whether it is reasonable to disregard revisitations after a certain period (e.g., after X days).  
これまでのところ、特定の期間（例：X日後）を過ぎた再訪を無視することが合理的かどうかについての具体的な研究はほとんどありません。  

<!-- ここまで読んだ! -->

Because of these challenges, many existing methods prioritize immediate engagement metrics (e.g., clicks, saves) over longer-term retention (Gugnani and Misra 2020; Wang et al. 2020; Dang et al. 2025; Gong et al. 2025; Jia et al. 2025).  
**これらの課題のため、多くの既存の方法は長期的なretentionよりも即時のエンゲージメントメトリクス（例：クリック、保存）を優先しています**（Gugnani and Misra 2020; Wang et al. 2020; Dang et al. 2025; Gong et al. 2025; Jia et al. 2025）。
In some cases, effective modeling also increases the time users spend (Guo et al. 2022).  
場合によっては、効果的なモデル化がユーザーの滞在時間を増加させることもあります（Guo et al. 2022）。
Reinforcement learning (RL) offers a framework for optimizing long-term rewards.  
強化学習（RL）は、長期的な報酬を最適化するためのフレームワークを提供します。  
Although RL methods have improved intra-session engagement (Afsar, Crump, and Far 2022; Cai et al. 2023; Liu et al. 2024), applying RL to optimize longer-term outcomes such as revisitation (events that may occur days after exposure) remains highly challenging.  
RL手法はセッション内のエンゲージメントを改善していますが（Afsar, Crump, and Far 2022; Cai et al. 2023; Liu et al. 2024）、**再訪のような長期的な結果を最適化するためにRLを適用することは非常に困難です（露出の数日後に発生するイベント）**。
Existing RL approaches often lack the scalability and robustness to handle multi-day sequences that may encompass thousands of recommended items.  
既存のRLアプローチは、数千の推奨アイテムを含む可能性のある複数日のシーケンスを処理するためのスケーラビリティと堅牢性に欠けることがよくあります。  
To the best of our knowledge, there are currently no RL-based approaches that, at Pinterest’s scale, explicitly target long-term revisitation while jointly addressing attribution and scalability.  
私たちの知る限り、Pinterestのスケールで、帰属とスケーラビリティを同時に考慮しながら長期的な再訪を明示的にターゲットにするRLベースのアプローチは現在存在しません。  

In this study, we propose a novel lightweight and interpretable framework for modeling user revisitation behavior and optimizing for long-term user retention in the recommendation context of search.  
本研究では、検索の推薦コンテキストにおける**ユーザー再訪行動をモデル化**し、長期的なユーザーretentionを最適化するための新しい軽量で解釈可能なフレームワークを提案します。
Research shows that well-chosen user behaviors can serve as effective surrogate rewards for predicting and optimizing long-term engagement in recommender systems (Wang et al. 2022).  
研究によれば、**適切に選択されたユーザー行動は、レコメンダーシステムにおける長期的なエンゲージメントを予測し最適化するための効果的な代理報酬として機能する**ことが示されています（Wang et al. 2022）。  
Therefore, to address the first challenge of attribution, we establish a surrogate for the causal effect of saving an item on subsequent revisitation events to reduce ambiguity and noise in revisitation signals.  
したがって、帰属の最初の課題に対処するために、アイテムを保存することがその後の再訪イベントに与える**因果効果の代理を確立**し、再訪信号のあいまいさとノイズを減少させます。
Figure 1 illustrated two types of revisitation attribution process.  
図1は、2種類の再訪帰属プロセスを示しています。  

- Same day revisitation: A user searched for “recipe” on _day 0 and saved a particular recipe item to their profile.  
同日再訪：ユーザーは_0日目に「レシピ」を検索し、特定のレシピアイテムを自分のプロフィールに保存しました。  
Later that day, they revisited the saved recipe item in their profile.  
その日の後半に、彼らはプロフィール内の保存したレシピアイテムを再訪しました。  
In this case, we attribute revisitation to the saved recipe item.
**この場合、再訪は保存したレシピアイテムに帰属**させます。  
We do not attribute other items the user viewed on other days to the saved recipe item.  
他の日にユーザーが表示した他のアイテムを保存したレシピアイテムに帰属させることはありません。  

- Cross-day revisitation: The user saved a shoe item via search on day 1 and viewed some other items in subsequent days.  
複数日再訪：ユーザーは1日目に検索を通じて靴のアイテムを保存し、その後の日に他のアイテムをいくつか表示しました。  
We do not attribute revisitation to the shoe item until the user revisited it in own profile on day 6.  
ユーザーが6日目に自分のプロフィールで靴のアイテムを再訪するまで、その再訪を靴のアイテムに帰属させません。

<!-- ここまで読んだ! -->

To leverage the constructed revisitation attributions and address the second challenge of scale, we first conduct a comprehensive analysis of user revisitation patterns and then translate the findings into a scalable data pipeline.  
構築した再訪帰属を活用し、スケールの第二の課題に対処するために、**まずユーザーの再訪パターンの包括的な分析を行い、その後、発見をスケーラブルなデータパイプラインに変換**します。  
The pipeline aggregates event data over a seven-day window across sessions and presentation surfaces by linking search-surface save events to profile-surface revisit events.  
このパイプラインは、検索サーフェスの保存イベントをプロフィールサーフェスの再訪イベントにリンクさせることによって、セッションとプレゼンテーションサーフェス全体で7日間のウィンドウにわたってイベントデータを集約します。  
This aggregation allows us to capture the most important revisitation signals for saved items, which serve as an auxiliary prediction task for the ranking model.  
この集約により、保存されたアイテムの最も重要な再訪信号を捉えることができ、これはランキングモデルの補助的な予測タスクとして機能します。  

In this way, the recommender system prioritizes items with high predicted probabilities of saving and revisit in the top positions, thereby driving downstream return visits and promoting long-term retention.  
このようにして、レコメンダーシステムは保存と再訪の高い予測確率を持つアイテムを上位に優先し、下流の再訪を促進し、長期的なretentionを促進します。  

This framework was shown to be effective in significantly increasing active users by 0.1% through both extensive offline experiments and a large-scale online A/B test with 24 million users on Pinterest’s Related Pins surface (Liu et al. 2017) over two months.  
このフレームワークは、広範なオフライン実験とPinterestの関連ピンの表面で2400万人のユーザーを対象とした大規模なオンラインA/Bテストを通じて、アクティブユーザーを0.1%増加させるのに効果的であることが示されました（Liu et al. 2017）。  

In summary, our contributions include:  
要約すると、私たちの貢献には以下が含まれます：  

- Large-scale analysis: We provide the first large-scale analysis of user revisitation patterns on online platform with hundreds of millions of users.  
- 大規模分析：私たちは、数億人のユーザーを持つオンラインプラットフォームにおけるユーザー再訪パターンの初の大規模分析を提供します。  

- Methodology & metrics improvements: We propose a novel, lightweight, and scalable framework for modeling user revisitation behavior without additional cost, which is demonstrated to improve long-term user retention via a large-scale online experiment of 24 millions of users.  
- 方法論とメトリクスの改善：追加のコストなしでユーザー再訪行動をモデル化するための新しい軽量でスケーラブルなフレームワークを提案し、2400万人のユーザーを対象とした大規模なオンライン実験を通じて長期的なユーザーretentionを改善することが示されています。  

- Interpretability & insights: The proposed framework offers greater interpretability than the SOTA methods, and it is able to show the reasoning behind the metrics improvement and the long-term and short-term revisitation patterns on topics.  
- 解釈可能性と洞察：提案されたフレームワークは、SOTA手法よりも高い解釈可能性を提供し、メトリクスの改善の背後にある理由やトピックに関する長期的および短期的な再訪パターンを示すことができます。  

- Deployment: The proposed method has been deployed on Pinterest’s Related Pins surface (Liu et al. 2017), efficiently serving 500+ millions of users without incurring additional computational costs.  
- 展開：提案された方法はPinterestの関連ピンの表面に展開され（Liu et al. 2017）、追加の計算コストをかけずに5億人以上のユーザーに効率的にサービスを提供しています。  

### 2.1. Related Work  

### 2.2. 関連研究  

User retention is critical objective for online platforms as sustained engagement typically drives more growth and revenue than short-term interactions.  
ユーザーretentionはオンラインプラットフォームにとって重要な目標であり、持続的なエンゲージメントは通常、短期的なインタラクションよりも多くの成長と収益を促進します。  

However, typical recommender systems in online platforms mainly focused on immediate engagement metrics such as click-through rates but struggled to capture the temporal dynamics essential for user retention.  
しかし、オンラインプラットフォームの典型的なレコメンダーシステムは、クリック率などの即時のエンゲージメントメトリクスに主に焦点を当てており、ユーザーretentionに不可欠な時間的ダイナミクスを捉えるのに苦労しています。  

The first challenge is that there are lots of noise in the collected data of user behaviors when modeling retention and it is difficult to find the factors that contribute to user retention (Sun et al. 2025).  
最初の課題は、retentionをモデル化する際にユーザー行動の収集データに多くのノイズが含まれており、ユーザーretentionに寄与する要因を見つけるのが難しいことです（Sun et al. 2025）。  

Ding et al. (2023) designed a contrastive multi-instance learning framework to explore the rationale and improve the interpretability of user retention, and they argue that recommender systems should rank different items for a user according to the user-item retention scores.  
Ding et al.（2023）は、ユーザーretentionの理由を探求し、その解釈可能性を向上させるための対照的なマルチインスタンス学習フレームワークを設計し、レコメンダーシステムはユーザーアイテムretentionスコアに基づいてユーザーのために異なるアイテムをランク付けすべきだと主張しています。  

The second challenge is the supervised information of user retention has been expected to be much sparser than immediate explicit feedback, such as click and save.  
第二の課題は、ユーザーretentionの監視情報がクリックや保存などの即時の明示的フィードバックよりもはるかに希薄であると予想されていることです。  

Generative Flow Networks (Liu et al. 2024) have been proposed to model retention by treating it as a probabilistic flow over user sessions, which aims to address the challenges of sparse and delayed retention signals.  
生成フローネットワーク（Liu et al. 2024）は、ユーザーセッションにおける確率的フローとしてretentionをモデル化することを提案しており、希薄で遅延したretention信号の課題に対処することを目指しています。  

DT4Rec (Zhao et al. 2023) leveraged the Decision Transformer to optimize long-term user retention by modeling sequences of interactions.  
DT4Rec（Zhao et al. 2023）は、インタラクションのシーケンスをモデル化することによって長期的なユーザーretentionを最適化するためにDecision Transformerを活用しました。  

. DT4Rec (Zhao et al. 2023) leveraged the Decision Transformer to optimize long-term user retention by modeling sequences of interactions.
DT4Rec（Zhao et al. 2023）は、インタラクションのシーケンスをモデル化することで、長期的なユーザーretentionを最適化するためにDecision Transformerを活用しました。

This approach incorporates an autodiscretized reward prompt that preserves partial order relationships between rewards, enhancing retention modeling over time.
このアプローチは、報酬間の部分的な順序関係をretentionする自動離散化報酬プロンプトを組み込んでおり、時間の経過とともにretentionモデルを強化します。

Other workstream such as customer purchase behavior analysis in industries like fashion have empirically validated that diverse product recommendations not only increase purchase rates but also positively influence long-term retention (Kwon, Han, and Han 2020).
ファッションのような業界における顧客購入行動分析などの他の作業ストリームは、多様な製品推薦が購入率を増加させるだけでなく、長期的なretentionにもポジティブな影響を与えることを実証的に検証しています（Kwon, Han, and Han 2020）。

Fashion is one of the most popular topic on Pinterest.
ファッションはPinterestで最も人気のあるトピックの一つです。

However, our past experiments when intentionally improving recommendation diversity hurt engagement metrics like click and save by more than 1% and we observed the tradeoff tension between relevance and diversity.
しかし、推薦の多様性を意図的に改善しようとした過去の実験では、クリックや保存といったエンゲージメント指標が1%以上悪化し、関連性と多様性の間のトレードオフの緊張を観察しました。

Wang et al. (2022) demonstrated that well-chosen user behaviors can serve as effective surrogate rewards for predicting and optimizing long-term engagement in recommender systems.
Wang et al.（2022）は、適切に選ばれたユーザー行動が推薦システムにおける長期的なエンゲージメントを予測し最適化するための効果的な代理報酬として機能することを示しました。

Through deep analyses on the revisitation behaviors of users on Pinterest, we observed that user revisitation behaviors are less sparse than some other user behaviors such as long click and share.
Pinterest上のユーザーの再訪行動に関する詳細な分析を通じて、ユーザーの再訪行動は、長クリックやシェアなどの他のユーザー行動よりもまばらではないことを観察しました。

Therefore, we establish our surrogate as the causal relationship between a saved item and its associated revisitation events.
したがって、私たちは保存されたアイテムとそれに関連する再訪イベントとの因果関係を代理として確立します。

-----
Figure 2: Illustration of Save, Revistation Impression and Revisitation Grid-click on Pinterest
図2: Pinterestにおける保存、再訪印象、再訪グリッドクリックの図解

and its associated revisitation events.
およびそれに関連する再訪イベント。

Although Zhang et al. (2021) designed a separate model for modeling the probability of click revisit and used it together with the ranking model that predicts click rate for predicting retention, deploying an additional model is very costly and increases serving latency.
Zhang et al.（2021）は、クリック再訪の確率をモデル化するための別のモデルを設計し、クリック率を予測するランキングモデルと共に使用しましたが、追加のモデルを展開することは非常にコストがかかり、サービスのレイテンシを増加させます。

In this work, we propose a revisitation modeling framework that jointly models users’ save and revisitation actions within the existing multi-task recommender, adding no cost or latency relative to the current system.
本研究では、既存のマルチタスク推薦システム内でユーザーの保存および再訪アクションを共同でモデル化する再訪モデルフレームワークを提案し、現在のシステムに対してコストやレイテンシを追加しません。

### 2.3. Revisitation Behavior Analysis

### 2.4. 再訪行動分析

Users engage in a variety of behaviors on online platforms, such as browsing, clicking on grids, liking, saving, sharing, and commenting.
ユーザーは、オンラインプラットフォーム上で、ブラウジング、グリッドのクリック、いいね、保存、共有、コメントなど、さまざまな行動に従事します。

They can also return to the platform for many reasons, from upper-funnel activities like aesthetically-pleasing content to completing lower-funnel projects like DIY and Crafts, or performing outbound clicks on previously saved outfits.
彼らはまた、美的に魅力的なコンテンツのような上流の活動から、DIYやクラフトのような下流のプロジェクトを完了するため、または以前に保存したアウトフィットに対して外部クリックを行うために、さまざまな理由でプラットフォームに戻ることができます。

Among these behaviors, revisitation stands out as a special type of return behavior, where a user goes back to content they had previously saved, an action that arguably indicates user satisfaction.
これらの行動の中で、再訪は特別なタイプの戻り行動として際立っており、ユーザーが以前に保存したコンテンツに戻る行動は、ユーザーの満足度を示すものと考えられます。

In this work, we leverage the common “save” action on online platforms to build an attribution between saved content and subsequent revisitation behaviors.
本研究では、オンラインプラットフォーム上の一般的な「保存」アクションを活用して、保存されたコンテンツとその後の再訪行動との間の帰属を構築します。

Specifically, when a user saves an item, it is added to their personal profile (such as a collection or board).
具体的には、ユーザーがアイテムを保存すると、それは彼らの個人プロフィール（コレクションやボードなど）に追加されます。

Users can then revisit their saved items in two primary ways:
ユーザーは次の2つの主要な方法で保存したアイテムを再訪できます。

- Impression-Based Revisitation: Scroll or navigate through the saved content without deeper interaction on their personal profile (such as collection or board).
- 印象ベースの再訪: 個人プロフィール（コレクションやボードなど）での深いインタラクションなしに、保存されたコンテンツをスクロールまたはナビゲートします。

- Grid-click-based Revisitation: Tap on the saved content to access more information on their personal profile (such as collection or board).
- グリッドクリックベースの再訪: 保存されたコンテンツをタップして、個人プロフィール（コレクションやボードなど）での詳細情報にアクセスします。

Figure 2 shows an example of a user who saved a Pin of a ramen recipe on Pinterest, had a revisitation impression on the Pin on their own board several days later, and then a revisitation grid-click to zoom in the Pin for more details.
図2は、Pinterestでラーメンレシピのピンを保存したユーザーの例を示しており、数日後に自分のボードでそのピンに再訪印象を持ち、その後、詳細を確認するためにピンを拡大するための再訪グリッドクリックを行ったことを示しています。

We conducted extensive analyses on these two revisitation behaviors and observed the following patterns:
私たちはこれらの2つの再訪行動に関して広範な分析を行い、以下のパターンを観察しました。

1. More users tend to have revisitation impressions rather than revisitation grid-clicks, and the percentage of users revisiting decays (Figure 3a).
1. より多くのユーザーが再訪印象を持つ傾向があり、再訪グリッドクリックよりも、再訪するユーザーの割合は減少します（図3a）。

Suppose a user saved a Pin on day 0, 14.6% of the users tend to have a revisitation impression on the saved Pin on day 0 immediately and 19.5% of the users on day 1, following a significant decay till 8.7% on day 9.
ユーザーが0日目にピンを保存したと仮定すると、14.6%のユーザーが0日目に保存されたピンに再訪印象を持ち、19.5%のユーザーが1日目に持ち、9日目には8.7%まで大幅に減少します。

The percentage of users have a revisitation grid-click starts at 6.6% at day 0 and peaked at day 1 of 7.7%, and decays to only 1.6% day 9.
再訪グリッドクリックを持つユーザーの割合は、0日目に6.6%から始まり、1日目に7.7%でピークに達し、9日目にはわずか1.6%に減少します。

1. The volume of revisitation grid-clicks decays dramatically in the first three days (Figure 3b).
2. 再訪グリッドクリックのボリュームは最初の3日間で劇的に減少します（図3b）。

Only 4.7% of the saved Pins get a revisitation grid-click on day 0 and the percentage dropped by half on day 1 followed by another half on day 3.
保存されたピンのうち、0日目に再訪グリッドクリックを受けるのはわずか4.7%で、1日目にはその割合が半分に減少し、3日目にはさらに半分に減少します。

The percentage dropped more steadily until it reaches 0.5% by day 5 and 0.3% by day 9.
その割合はより安定して減少し、5日目には0.5%、9日目には0.3%に達します。

1. The sooner they revisit, the higher the expected number of days active in the next 1-month period.
2. 早く再訪するほど、次の1か月間にアクティブであると予想される日数が増えます。

Figure 4 shows that: (1) users who revisited by day t tend to have more days active in the following 1-month period compared to users who did not revisit by day t (distribution less left skewed);
図4は次のことを示しています：（1）日tまでに再訪したユーザーは、日tまでに再訪しなかったユーザーと比較して、次の1か月間にアクティブである日数が多い傾向があります（分布が左に偏っていない）。

(2) users who revisited sooner tend to have more days active in the following 1-month period.
（2）早く再訪したユーザーは、次の1か月間にアクティブである日数が多い傾向があります。

It is worth mentioning that the fact that they revisit soon does not imply that they will be more active.
早く再訪することが、彼らがよりアクティブになることを意味するわけではないことは注目に値します。

Instead, it could also be true that users who are more active tend to come back sooner.
むしろ、よりアクティブなユーザーが早く戻ってくる傾向があることも真実かもしれません。

1. Revisitation grid-click drives deeper engagement than just revisitation impression.
2. 再訪グリッドクリックは、単なる再訪印象よりも深いエンゲージメントを促進します。

We have one group of users with only revisitation impressions and another group of users with revisitation grid-click.
私たちは、再訪印象のみを持つユーザーのグループと、再訪グリッドクリックを持つユーザーのグループを持っています。

We computed the difference in their active days between the two groups in the 1-month period after the initial revisitation by Day 0 to Day 6 and estimate their incremental change within the 1-month period.
私たちは、初回の再訪から0日目から6日目までの1か月間における2つのグループのアクティブ日数の差を計算し、1か月間の中での増分変化を推定しました。

Figure 5 shows that Grid-click-based revisitation has a higher correlation with the change in the 1-month activity than pure Impression-based revisitation.
図5は、グリッドクリックベースの再訪が純粋な印象ベースの再訪よりも1か月間のアクティビティの変化との相関が高いことを示しています。

Unsurprisingly, this suggests that more “intentional” revisitation (i.e. via a grid click over just an impression) yields superior retention outcomes.
驚くことではありませんが、より「意図的な」再訪（すなわち、単なる印象よりもグリッドクリックを介して行われる再訪）が優れたretention結果をもたらすことを示唆しています。

### 2.5. Revisitation Modeling in Multi-task Learning Recommender System

### 2.6. マルチタスク学習推薦システムにおける再訪モデル化

We proposed revisitation modeling on the Related Pins surface on Pinterest (Liu et al. 2017) (Figure 6), a search-like surface which serves around 50% of the traffic on the entire platform.
私たちは、Pinterestの関連ピンサーフェス（Liu et al. 2017）（図6）における再訪モデル化を提案しました。これは、全プラットフォームの約50%のトラフィックを提供する検索のようなサーフェスです。

Users enter the Related Pins surface when they grid-click a Pin on any other upper-stream surface (such as Homefeed or Search).
ユーザーは、他の上流サーフェス（ホームフィードや検索など）でピンをグリッドクリックすると、関連ピンサーフェスに入ります。

There are two main parts of the Related Pins surface:
関連ピンサーフェスには2つの主要な部分があります。

(1) A closer view of the Pin (query Pin) they just grid-clicked on from an upper-stream surface where they can read the title and descriptions of the Pin, and save the Pin to their own profile so they can revisit it any time later (Figure 6 left).
（1）ユーザーが上流サーフェスからグリッドクリックしたピン（クエリピン）の詳細ビューで、ピンのタイトルや説明を読み、ピンを自分のプロフィールに保存して後でいつでも再訪できるようにします（図6左）。

(2) When user scrolls down, they will see a grid view of recommended Pins under title “More like this” which are related to the query Pin above (Figure 6 right).
（2）ユーザーがスクロールダウンすると、上記のクエリピンに関連する「このようなもの」のタイトルの下に推奨ピンのグリッドビューが表示されます（図6右）。

Users can engage with the recommended Pins, a.k.a. candidate Pins with the following main actions:
ユーザーは、推奨ピン、すなわち候補ピンに対して次の主要なアクションで関与できます。

-----
(a) Percentage of Users Revisiting Per Day (b) Percentage of Grid-click based Revisitation Volume Per Day
(a) ユーザーの再訪割合（毎日） (b) グリッドクリックベースの再訪ボリュームの割合（毎日）

Figure 3: Revisitation analysis (users & volume) - Day 0 is when a Pin was saved
図3: 再訪分析（ユーザーとボリューム） - 0日目はピンが保存された日です

Figure 5: Correlation Between Revisit Type by Day X and ∆ in 28-day Engagement with 95% Confidence Intervals  
図5: 日Xによる再訪タイプと28日間のエンゲージメントの変化との相関（95%信頼区間）

Figure 4: 28-day activity distribution by revisit status (revisit by day 0-6)
図4: 再訪状況による28日間のアクティビティ分布（0-6日目の再訪）

- Impression: Scroll or navigate through a Pin without deeper engagement.
- 印象: より深いエンゲージメントなしにピンをスクロールまたはナビゲートします。

- Grid-click: A single tap on the Pin that makes it appear larger.
- グリッドクリック: ピンを大きく表示するための単一のタップです。

When a grid-click happens, user will enter another Related Pin feed where the query Pin becomes the previously tapped Pin and new recommendations will be generated for that Pin.
グリッドクリックが発生すると、ユーザーは別の関連ピンフィードに入り、クエリピンが以前にタップしたピンになり、そのピンに対して新しい推奨が生成されます。

- Save (a.k.a. Repin): Click on the “Save” button to save the Pin to user’s own profile so they can revisit it any time later.
- 保存（別名: リピン）: 「保存」ボタンをクリックして、ピンをユーザーのプロフィールに保存し、後でいつでも再訪できるようにします。

- Click: Click on the “Visit” button to view more information about the Pin from a third-party website (if there is the Visit button for that Pin).
- クリック: 「訪問」ボタンをクリックして、第三者のウェブサイトからピンに関する詳細情報を表示します（そのピンに訪問ボタンがある場合）。

- Long click: User stay on the third-party website for longer than 35s.
- 長クリック: ユーザーが第三者のウェブサイトに35秒以上滞在します。

#### 2.6.1. Multi-task Learning Recommender System

#### 2.6.2. マルチタスク学習推薦システム

The goal of a multi-task recommender system is to jointly optimize for multiple related tasks by leveraging shared representations and correlations among those tasks (Zhang and Yang 2021).
マルチタスク推薦システムの目標は、共有表現とタスク間の相関を活用して、複数の関連タスクを共同で最適化することです（Zhang and Yang 2021）。

Figure 7 (left) shows the main architecture of the multi-task learning ranking model for recommendation on Related Pins.
図7（左）は、関連ピンに対する推薦のためのマルチタスク学習ランキングモデルの主要なアーキテクチャを示しています。

The input layer includes query Pin features, candidate Pin features, user features, and a transformer-based user sequence module that encodes user historical actions.
入力層には、クエリピンの特徴、候補ピンの特徴、ユーザーの特徴、およびユーザーの過去の行動をエンコードするトランスフォーマーベースのユーザーシーケンスモジュールが含まれています。

The summarization layer includes some feature crossing manipulation between query Pin features and candidate Pin features and dimension reductions, where the output embedding is fed to a DCNv2 module (Wang et al. 2021) to learn deeper feature interactions.
要約層には、クエリピンの特徴と候補ピンの特徴の間のいくつかの特徴交差操作と次元削減が含まれ、出力埋め込みはDCNv2モジュール（Wang et al. 2021）に供給され、より深い特徴の相互作用を学習します。

A final MLP layer aggregates the output embeddings of DCNv2 into a single embedding and feed it to an MMoE module (Ma et al. 2018) for multi-task learning.
最終的なMLP層は、DCNv2の出力埋め込みを単一の埋め込みに集約し、それをMMoEモジュール（Ma et al. 2018）に供給してマルチタスク学習を行います。

Each action is binary so the loss function is the sum of binary cross entropy loss (Equation (1)),
各アクションはバイナリであるため、損失関数はバイナリ交差エントロピー損失の合計です（式（1））、

$$
\text{loss}_1 = \sum_{i \in L} w_i \cdot \left[ c_i \log p(c_i | q, \theta) + (1 - c_i) \log p(1 - c_i | q, \theta) \right]
$$

where $L = \{ \text{grid-click}, \text{repin}, \text{click}, \text{long-click} \}$, $q$ refers to query Pin, $c$ refers to candidate Pin, $\theta$ denotes model parameters, $c_i$ is binary label, where 1 indicating action $i$ is positive and 0 means negative, and $w_i$ refers to the loss weight for task $i$.
ここで、$L = \{ \text{grid-click}, \text{repin}, \text{click}, \text{long-click} \}$、$q$はクエリピンを指し、$c$は候補ピンを指し、$\theta$はモデルパラメータを示し、$c_i$はバイナリラベルで、1はアクション$i$がポジティブであることを示し、0はネガティブであることを意味し、$w_i$はタスク$i$の損失重みを指します。

The recommender system requires an aggregated score based on the prediction of each task to rank all the candidate Pins.
推薦システムは、すべての候補ピンをランク付けするために、各タスクの予測に基づいた集約スコアを必要とします。

For each task, a utility weight $u_i$ representing the importance of the action based on business need is tuned and assigned to $p(c_i | q)$ and all the tasks are aggregated to calculate the final score for ranking the candidate Pins (Equation (2)).
各タスクに対して、ビジネスニーズに基づくアクションの重要性を表すユーティリティ重み$u_i$が調整され、$p(c_i | q)$に割り当てられ、すべてのタスクが集約されて候補ピンのランク付けのための最終スコアを計算します（式（2））。

$$
\text{score} = \sum_{i \in L} u_i \cdot p(c_i | q, \theta)
$$

#### 2.6.3. Revisitation Label Design

#### 2.6.4. 再訪ラベル設計

_Goal. We seek a revisitation signal that balances label density (coverage) and intent (precision) as the best proxy for retention._
_目標. 私たちは、retentionの最良の代理としてラベル密度（カバレッジ）と意図（精度）をバランスさせる再訪信号を求めています。_

_Interaction type. Impression-based revisits provide high coverage but include incidental scroll noise; grid-click revisits are rarer but indicate deliberate return intent._
_インタラクションタイプ. 印象ベースの再訪は高いカバレッジを提供しますが、偶発的なスクロールノイズが含まれます。グリッドクリック再訪はまれですが、意図的な戻り意図を示します。_

. Impression-based revisits provide high coverage but include incidental scroll noise; grid-click revisits are rarer but indicate deliberate return intent.
印象に基づく再訪は高いカバレッジを提供しますが、偶発的なスクロールノイズが含まれます。一方、グリッドクリックによる再訪は稀ですが、意図的な戻りの意図を示します。

Section “Revisitation Behavior Analysis” shows grid-click revisits correlate more strongly with downstream activity than impressions.  
「再訪行動分析」セクションでは、グリッドクリックによる再訪が印象よりも下流の活動とより強く相関していることが示されています。

_Temporal window. In section “Revisitation Behavior Analysis”, we observed that revisits concentrate shortly after saves (sharp decay within the first week).  
_時間的ウィンドウ。「再訪行動分析」セクションでは、再訪が保存後すぐに集中することを観察しました（最初の1週間で急激に減少します）。

In addition, the sooner revisitation happens, the more likely it is for users to be more active within the following 1-month period.  
さらに、再訪が早ければ早いほど、ユーザーがその後の1か月間により活発になる可能性が高くなります。

Therefore, we utilized the revisitation behaviors that happened 0-6 days after repin as revisitation labels as they are more recent and take up most of the revisitation actions.  
したがって、私たちは、リピン後0-6日以内に発生した再訪行動を再訪ラベルとして利用しました。これらはより最近のものであり、再訪行動の大部分を占めています。

We surmised that driving more revisitation behaviors on the saved Pin in the following week could lead to an increase in active days by users and potentially improve user retention.  
保存されたピンに対する再訪行動を次の週に増やすことが、ユーザーのアクティブな日数の増加につながり、ユーザーのretentionを改善する可能性があると推測しました。

In addition, based on our finding that revisitation grid-clicks take less than half of the volume of revisitation impressions but they tend to drive deeper engagement than revisitation impressions,  
さらに、再訪のグリッドクリックが再訪の印象のボリュームの半分未満であることがわかりましたが、再訪の印象よりも深いエンゲージメントを促進する傾向があることに基づいて、

we utilized revisitation grid-clicks that happened 0-6 days after repin while only use same-day revisitation impressions as repin.  
リピン後0-6日以内に発生した再訪のグリッドクリックを利用し、同日の再訪印象のみをリピンとして使用しました。

The final revisitation labels include:  
最終的な再訪ラベルには以下が含まれます：

- Same-day Revisitation Impression (1dRevImpre): User saved a Pin and has a revisitation impression of the saved Pin on the same day.  
- 同日再訪印象 (1dRevImpre): ユーザーがピンを保存し、同日に保存されたピンの再訪印象を持っています。

The volume of same-day revisitation impressions consists of 25.8% of the repin volume in a day.  
同日再訪印象のボリュームは、1日のリピンボリュームの25.8%を占めています。

- Same-day Revisitation Grid-click (1dRevGrid): User saved a Pin and has a revisitation grid-click of the saved Pin on the same day.  
- 同日再訪グリッドクリック (1dRevGrid): ユーザーがピンを保存し、同日に保存されたピンの再訪グリッドクリックを持っています。

The volume of same-day revisitation grid-clicks takes up 4.7% of the repin volume in a day.  
同日再訪グリッドクリックのボリュームは、1日のリピンボリュームの4.7%を占めています。

- 7-day Revisitation Grid-click (7dRevGrid): User saved a Pin and has a revisitation grid-click of the saved Pin in the following 0-6 days.  
- 7日再訪グリッドクリック (7dRevGrid): ユーザーがピンを保存し、次の0-6日以内に保存されたピンの再訪グリッドクリックを持っています。

The volume of 7-day revisitation grid-click consists of 9% of the repin volume in a day in total as we see a quick decay of revisitation grid-click after repin on day 0 in Figure 3b.  
7日再訪グリッドクリックのボリュームは、1日のリピンボリュームの9%を占めており、図3bでリピン後0日目に再訪グリッドクリックが急速に減少するのが見られます。

We merge the three types of labels as the final revisitation label, and add a revisitation head in the multi-tasks learning ranking model for predicting the probability of a candidate Pin being saved and revisited in the future using the constructed revisitation label.  
私たちは、3種類のラベルを最終的な再訪ラベルとして統合し、構築した再訪ラベルを使用して、候補ピンが将来保存され再訪される確率を予測するために、マルチタスク学習ランキングモデルに再訪ヘッドを追加しました。

Therefore, the loss function with the additional revisitation head is shown in Equation (3), where RP indicates Repin and RV stands for Revisit.  
したがって、追加の再訪ヘッドを持つ損失関数は式(3)に示されており、RPはリピンを、RVは再訪を示します。

$$
loss2 = loss1 + w_{RP \& RV} [c_{RP \& RV} \log p(c_{RP \& RV} | q, \theta) + (1 - c_{RP \& RV}) \log p(1 - c_{RP \& RV} | q, \theta)]
$$

The final ranking score is shown in Equation (4), and we tune the utility weight $u_{RP \& RV}$ for the new task.  
最終的なランキングスコアは式(4)に示されており、新しいタスクのためにユーティリティ重み$u_{RP \& RV}$を調整します。

$$
score = u_i \cdot p(c_i | q, \theta) + u_{RP \& RV} \cdot p(c_{RP \& RV} | q, \theta)
$$

#### 2.6.5. Revisitation Features Design  

#### 2.6.6. 再訪特徴の設計

The current recommender system on the Related Pins surface takes various Pin features as input, including content features, such as text embeddings and visual embeddings (Zhai et al. 2019), and graph based embeddings, such as graphsage embeddings (Hamilton, Ying, and Leskovec 2017), pinnersage embeddings (Pancha et al. 2022), omnis_age embeddings (Badrinath et al. 2025), and engagement features like Navboost (Kislyuk et al. 2015).  
現在の関連ピンの表面上のレコメンダーシステムは、テキスト埋め込みや視覚埋め込み（Zhai et al. 2019）などのコンテンツ特徴、グラフベースの埋め込み（Hamilton, Ying, and Leskovec 2017）、pinnersage埋め込み（Pancha et al. 2022）、omnis_age埋め込み（Badrinath et al. 2025）、およびNavboost（Kislyuk et al. 2015）などのエンゲージメント特徴を含むさまざまなピン特徴を入力として受け取ります。

One of the most important engagement features that have been adopted on all the surfaces is called Pin perf, counting the historical number of actions on a specific Pin.  
すべての表面で採用されている最も重要なエンゲージメント特徴の1つは、特定のピンに対する過去のアクションの数をカウントするPin perfと呼ばれています。

For each positive action (including grid-click, save, click, and long click), the Pin perf feature counts the how many times a Pin has been engaged with that action on Pinterest in the past 90 days.  
各ポジティブアクション（グリッドクリック、保存、クリック、長押しを含む）について、Pin perf特徴は、過去90日間にPinterestでそのアクションでピンがどれだけエンゲージされたかをカウントします。

In this work, we designed a set of revisitation Pin perf features to evaluate the popularity of the saved Pins receiving revisitations in the past 7 days, 30 days, and 90 days.  
この作業では、過去7日間、30日間、90日間に再訪を受けた保存されたピンの人気を評価するための再訪Pin perf特徴のセットを設計しました。

Corresponding to the three types of revisitation labels, we designed three types of revisitation Pin perf features, which we refer as Related Pins-triggered revisitation Pin perf features since we only count +1 if the revisited Pin is saved on the Related Pins surface by the same user.  
3種類の再訪ラベルに対応して、3種類の再訪Pin perf特徴を設計しました。これは、再訪されたピンが同じユーザーによって関連ピンの表面に保存された場合にのみ+1をカウントするため、関連ピンによってトリガーされた再訪Pin perf特徴と呼びます。

This design is for enhancing the model learning correlations between a Pin’s revisitation popularity in history (features) and its current revisitation performance (labels).  
この設計は、ピンの再訪人気の歴史（特徴）とその現在の再訪パフォーマンス（ラベル）との相関をモデルが学習するのを強化するためのものです。

We aggregated the features on the 7-day (update very day), 30-day (update every 3 days), and 90-day (update every week) basis for the sake of higher feature coverage.  
より高い特徴カバレッジのために、7日（毎日更新）、30日（3日ごとに更新）、90日（毎週更新）ベースで特徴を集約しました。

- Same-day Revisit Impression Pin Perf: 60% coverage  
- 同日再訪印象Pin Perf: 60%カバレッジ

- Same-day Revisit Grid-click Pin Perf: 49% coverage  
- 同日再訪グリッドクリックPin Perf: 49%カバレッジ

- 7-day Revisit Grid-click Pin Perf: 51% coverage  
- 7日再訪グリッドクリックPin Perf: 51%カバレッジ

In addition, to capture the general popularity of a Pin being revisited, we designed a set of overall revisitation Pin perf features where we do not require the repin happened on the Related Pin surface and do not define the time gap between repin and revisitation.  
さらに、再訪されるピンの一般的な人気を捉えるために、関連ピンの表面でリピンが発生する必要がなく、リピンと再訪の間の時間ギャップを定義しない全体的な再訪Pin perf特徴のセットを設計しました。

- Overall Revisit Impression Pin Perf: 80% coverage  
- 全体再訪印象Pin Perf: 80%カバレッジ

- Overall Revisit Grid-click Pin Perf: 70% coverage  
- 全体再訪グリッドクリックPin Perf: 70%カバレッジ

For each Pin perf feature, we include a count of “number of actions” and a count of “unique users” to reflect volume and popularity, respectively.  
各Pin perf特徴について、「アクションの数」と「ユニークユーザーの数」を含めて、ボリュームと人気をそれぞれ反映させます。

Volume alone could be noise to the system since the Pin revisitation count could be heavily driven by a single enthusiastic user.  
ボリュームだけでは、システムにノイズをもたらす可能性があります。なぜなら、ピンの再訪カウントは、単一の熱心なユーザーによって大きく影響を受ける可能性があるからです。

#### 2.6.7. Cross-surface Revisitation Data Pipeline  

#### 2.6.8. クロスサーフェス再訪データパイプライン

Figure 7 (right) illustrates the end-to-end user journey on Pinterest.  
図7（右）は、Pinterestにおけるエンドツーエンドのユーザーの旅を示しています。

When user lands on Related Pins surface from other surface (such as Homefeed and Search) and grid-clicks a Pin they like, they can save (repin) the Pin to their own profile.  
ユーザーが他の表面（ホームフィードや検索など）から関連ピンの表面に到達し、気に入ったピンをグリッドクリックすると、そのピンを自分のプロフィールに保存（リピン）できます。

Later on, they can go back to their own profile and browse the Pin (revisitation impression); they can also tap on the saved Pin to have a bigger and deeper view of the Pin (revisitation grid-click) where they will re-land on Related Pins with the saved Pin as query Pin and browse the recommended Pins that are to it.  
その後、彼らは自分のプロフィールに戻り、ピンを閲覧（再訪印象）できます。また、保存されたピンをタップして、ピンのより大きく深いビューを得ることもできます（再訪グリッドクリック）。その際、保存されたピンをクエリピンとして関連ピンに再度到達し、それに関連する推奨ピンを閲覧します。

Users’ actions on all the candidate Pins in the grid view on the Related Pins surface (staging 2 and 3 with blue color) are logged to a daily generated dataset for training the ranking model for recommendations on the Related Pins surface.  
関連ピンの表面のグリッドビューにあるすべての候補ピンに対するユーザーのアクション（青色のステージング2および3）は、関連ピンの表面での推奨のためのランキングモデルをトレーニングするために、日次生成データセットに記録されます。

However, users’ revisitation actions on their own profiles were not included in the training data.  
ただし、ユーザーのプロフィールでの再訪アクションはトレーニングデータに含まれていませんでした。

In order to further track users’ revisitation behaviors on their saved Pins, we did a cross-surface join of the existing training data of user actions on the Related Pins surface and data of user actions on their own profile on user ID and Pin ID to  
保存されたピンに対するユーザーの再訪行動をさらに追跡するために、関連ピンの表面でのユーザーアクションの既存のトレーニングデータと、ユーザーIDおよびピンIDに基づくユーザーのプロフィールでのアクションデータをクロスサーフェスで結合しました。

map users’ revisitation actions in their own profile to their saved Pins on related Pins surface.  
ユーザーのプロフィールでの再訪アクションを関連ピンの表面にある保存されたピンにマッピングします。

Figure 8 illustrates the revisitation data generation and the final training data generation pipeline.  
図8は、再訪データ生成と最終的なトレーニングデータ生成パイプラインを示しています。

1. Log the revisitation Pin perf features, join them with the other features, and convert raw features log entries into TabularML.  
1. 再訪Pin perf特徴をログに記録し、他の特徴と結合し、生の特徴ログエントリをTabularMLに変換します。

1. Extracts all the user actions on the Related Pins surface from Feedview Log into labels.  
1. Feedviewログから関連ピンの表面でのすべてのユーザーアクションをラベルに抽出します。

1. Cross-surface and cross-session (day) join of users’ save actions on the Related Pins surface and users’ revisitation impressions and revisitation grid-clicks actions on their own profile (join key: User ID and Pin ID, condition: timesave < timerevisit < timesave+7(days)).  
1. 関連ピンの表面でのユーザーの保存アクションと、ユーザーのプロフィールでの再訪印象および再訪グリッドクリックアクションのクロスサーフェスおよびクロスセッション（日）結合（結合キー：ユーザーIDおよびピンID、条件：timesave < timerevisit < timesave+7（日））。

1. Join the revisitation labels with the repin labels and on User ID and Pin ID and add a new column for the revisitation label indicating which saved Pin has been revisited in the final label constructor.  
1. 再訪ラベルをリピンラベルとユーザーIDおよびピンIDで結合し、最終ラベル構築者でどの保存されたピンが再訪されたかを示す再訪ラベルの新しい列を追加します。

1. Join feature TabularML and the final labels (with revisitation label added) on API request id and candidate Pin id.  
1. 特徴TabularMLと最終ラベル（再訪ラベル追加）をAPIリクエストIDおよび候補ピンIDで結合します。

Step (1) (2) and (3) can be conducted in parallel, followed by step (4) and step (5) sequentially.  
ステップ（1）（2）および（3）は並行して実行でき、その後ステップ（4）および（5）を順次実行します。

This solution of mapping user revisitation labels to training data is scalable to any other surface on Pinterest and other platforms where users can save content and revisit the saved content.  
ユーザーの再訪ラベルをトレーニングデータにマッピングするこのソリューションは、Pinterestの他の表面や、ユーザーがコンテンツを保存し、保存されたコンテンツを再訪できる他のプラットフォームにもスケーラブルです。

### 2.7. Offline Experiment  

### 2.8. オフライン実験

We trained the multi-task learning ranking model on the Related Pins surface on Pinterest illustrated in Figure 7 with the designed revisitation labels and revisitation Pin perf features.  
私たちは、図7に示されたPinterestの関連ピンの表面で、設計された再訪ラベルと再訪Pin perf特徴を使用してマルチタスク学習ランキングモデルをトレーニングしました。

We used 27 days of data for training, the last day of training data for calibration and the following 3 days of data for evaluation.  
トレーニングには27日間のデータを使用し、トレーニングデータの最終日をキャリブレーションに、次の3日間のデータを評価に使用しました。

The size of the entire training data is around 6.6 billion and the size of the evaluation data is around 700 million.  
全体のトレーニングデータのサイズは約66億で、評価データのサイズは約7億です。

We train the model for 1 epoch.  
モデルを1エポックでトレーニングしました。

We also tuned the utility weight $u_{RP \& RV}$ for the added revisitation task in Equation (4) and experiment results showed that the model achieved the best gain without tradeoff when $u_{RP \& RV} = 1.27 \cdot u_{Repin}$.  
また、式(4)の追加された再訪タスクのためにユーティリティ重み$u_{RP \& RV}$を調整し、実験結果は、モデルが$u_{RP \& RV} = 1.27 \cdot u_{Repin}$のときにトレードオフなしで最良の利益を達成したことを示しました。

Table 1 first shows the offline evaluation results.  
表1は、最初にオフライン評価結果を示しています。

For ranking metrics per task (head), we observed revisitation head  
タスク（ヘッド）ごとのランキングメトリックについて、再訪ヘッドを観察しました。

Table 1: Offline Evaluation Results  
表1: オフライン評価結果

| Metric                | Repin      | Revisit    |
|-----------------------|------------|------------|
| NDCG@3 Lift (%)       | **0.1279** | **40.15**  |
| MAP@3 Lift (%)        | **0.06453**| **43.44**  |
| Recip Rank@3 Lift (%) | -0.02666   | **27.62**  |
| Recall@3 Lift (%)     | **0.2705** | **35.4**   |
| Pairwise Accuracy Lift (%) | **0.10** | **21.62**  |
| Hits@3 Lift (%)       | **0.59**   | **0.65**   |

Note: Bold numbers indicate metrics gain.  
注: 太字の数字はメトリックの増加を示します。

achieved 20%-40% lift and repin head also achieved 0.05%-0.03% lift compared to the current ranking model without revisitation modeling.  
再訪ヘッドは20%-40%のリフトを達成し、リピンヘッドも再訪モデリングなしの現在のランキングモデルと比較して0.05%-0.03%のリフトを達成しました。

Because all the revisited Pins were saved Pins (repins), the model was able to prioritize ranking the Pins that may receive more revisitations in the top positions.  
すべての再訪されたピンが保存されたピン（リピン）であったため、モデルは再訪が多くなる可能性のあるピンを上位にランク付けすることができました。

In addition, we used Hits@3 to evaluate the overall ranking performance based on the final ranking score defined in Equation (4).  
さらに、式(4)で定義された最終ランキングスコアに基づいて、全体的なランキングパフォーマンスを評価するためにHits@3を使用しました。

For example, we incremented Hits@3 (Re_pin) if the user saved any of the top 3 recommendations.  
たとえば、ユーザーが上位3つの推奨のいずれかを保存した場合、Hits@3（Re_pin）を増加させました。

We tuned the utility weight for the revisitation head in Equation (4) based on Hits@3 metrics.  
Hits@3メトリックに基づいて、式(4)の再訪ヘッドのユーティリティ重みを調整しました。

By modeling revisitation in the ranking model, the model improved the Hits@3 metrics on repin by 0.59% and revisitation by 0.65% significantly without trade-offs on other heads.  
ランキングモデルで再訪をモデル化することにより、モデルはリピンのHits@3メトリックを0.59%、再訪を0.65%大幅に改善し、他のヘッドに対するトレードオフなしで実現しました。

```md
By modeling revisitation in the ranking model, the model improved the Hits@3 metrics on repin by 0.59% and revisitation by 0.65% significantly without trade-offs on other heads. 
ランキングモデルにおける再訪問をモデル化することにより、モデルはrepinにおけるHits@3メトリクスを0.59%、再訪問を0.65%改善し、他のヘッドに対するトレードオフなしに達成しました。

Empirical evidence at Pinterest showed that Hits@3 usually lines up the most with the online A/B experiment among all of the metrics. 
Pinterestでの実証的証拠は、Hits@3がすべてのメトリクスの中でオンラインA/B実験と最も一致することを示しました。

### Online A/B Experiment
We conducted a large-scale online A/B experiment from April 29, 2025 to June 26, 2025 on Pinterest Related Pins surface (Liu et al. 2017). 
私たちは、2025年4月29日から2025年6月26日までPinterestの関連ピンサーフェスで大規模なオンラインA/B実験を実施しました（Liu et al. 2017）。

The number of users in each group was around 12 million. 
各グループのユーザー数は約1200万人でした。

The experiment ran for 2 months from which we reported the accumulated results. 
実験は2ヶ月間行われ、その結果を報告しました。

#### Revisitation Online Metrics
Table 2 first shows the three types of revisitation metrics corresponding to the proposed revisitation labels, i.e., 1dRevImpre, 1dRevGrid, and 7dRevGrid. 
表2は、提案された再訪問ラベルに対応する3種類の再訪問メトリクス、すなわち1dRevImpre、1dRevGrid、および7dRevGridを最初に示しています。

Compared to the control group, the treatment group achieved 0.95% - 1.42% lift on the revisitation grid-clicks metrics. 
対照群と比較して、処置群は再訪問グリッドクリックメトリクスで0.95%から1.42%の向上を達成しました。

The revisitation grid-clicks metrics gains are higher than the repin gain, which indicating revisitation grid-click rate gain overall after removing the impact of repin gain on revisitation metrics. 
再訪問グリッドクリックメトリクスの向上はrepinの向上よりも高く、これは再訪問メトリクスに対するrepinの影響を除去した後の再訪問グリッドクリック率の向上を示しています。

Notably, the treatment group achieved higher revisitation ratio in terms of both volume and propensity, indicating that the revisitation modeling in the treatment group was driving larger proportion of revisitations from the saved Pins. 
特に、処置群はボリュームと傾向の両方においてより高い再訪問比率を達成し、処置群の再訪問モデルが保存されたピンからの再訪問の大きな割合を推進していることを示しています。

Compared to the same-day revisitation grid-click metrics, the treatment group achieved higher lift on the 7-day revisitation grid-clicks metrics, which demonstrated strong accumulative effect of revisitation modeling in driving users’ longer term revisitation behaviors on the platform. 
同日再訪問グリッドクリックメトリクスと比較して、処置群は7日間の再訪問グリッドクリックメトリクスでより高い向上を達成し、これはプラットフォーム上でのユーザーの長期的な再訪問行動を推進する再訪問モデルの強い累積効果を示しました。

We also observed that the gain on the same-day revisitation impression is lower than the grid-click based revisitation metrics. 
また、同日再訪問インプレッションの向上は、グリッドクリックベースの再訪問メトリクスよりも低いことを観察しました。

This aligns with our previous finding that revisitation grid-clicks drives deeper engagement than just Impression-based revisitation. 
これは、再訪問グリッドクリックが単なるインプレッションベースの再訪問よりも深いエンゲージメントを促進するという以前の発見と一致しています。

#### Engagement Metrics and User Retention Metrics
Table 2 also shows the engagement metrics lift on the Related Pins surface between the control group and the treatment group with revisitation modeling. 
表2は、再訪問モデルを用いた対照群と処置群の間の関連ピンサーフェスでのエンゲージメントメトリクスの向上も示しています。

Aligned with the offline metrics, the treatment group achieved better metrics of 0.94% volume gain and 0.64% propensity gain on repin. 
オフラインメトリクスと一致して、処置群はrepinにおいて0.94%のボリューム向上と0.64%の傾向向上を達成しました。

Table 2 showed that the treatment group with revisitation modeling is driving +0.41% user sessions that are longer than 5 minutes and +0.35% Web or API requests overall on Pinterest. 
表2は、再訪問モデルを用いた処置群がPinterest全体で5分以上のユーザーセッションを+0.41%、WebまたはAPIリクエストを+0.35%推進していることを示しました。

We also observed from Table 2 that the users in the treatment group spent longer time on the Related Pins surface (+0.53%) as well as their own profile (+0.68%) where revisitations happen, and overall in App (+0.39%) than users in the control group. 
また、表2から、処置群のユーザーは関連ピンサーフェスでより長い時間（+0.53%）を過ごし、再訪問が発生する自身のプロフィールでも（+0.68%）過ごし、全体的にアプリ内で（+0.39%）対照群のユーザーよりも長い時間を過ごしていることを観察しました。

Given that our model only directly affected the recommendations on the Related Pins surface, the gains on site-wide retention metrics were considered as significantly notable. 
私たちのモデルが関連ピンサーフェスの推薦にのみ直接影響を与えたことを考慮すると、サイト全体のリテンションメトリクスの向上は非常に注目すべきものでした。

All these metrics gains contributed to 0.1% volume gain and 0.08% propensity gain on active users. 
これらすべてのメトリクスの向上は、アクティブユーザーに対して0.1%のボリューム向上と0.08%の傾向向上に寄与しました。

#### Visualization
Based on the online A/B experiment results, we further conducted multiple revisitation visualizations on the 16 main topics of Pins on Pinterest. 
オンラインA/B実験の結果に基づいて、私たちはPinterestの16の主要なピントピックに関する複数の再訪問可視化をさらに実施しました。

**Interpretability**
By incorporating revisitation modeling into the multi-task recommendation system (Equation (3)), the model is prioritizing recommending Pins that achieved more saves and revisitations. 
再訪問モデルをマルチタスク推薦システム（式（3））に組み込むことにより、モデルはより多くの保存と再訪問を達成したピンを推薦することを優先しています。

Pins that received more revisitations historically will tend to receive more repins by the proposed revisitation modeling framework. 
歴史的により多くの再訪問を受けたピンは、提案された再訪問モデルフレームワークによってより多くのrepinを受ける傾向があります。

We calculated the average probability of repin and revisitation $P$ (cRP &RV |q, θ) on each topic for the control group, and the repin volume lift (%) per user of treatment group over control group. 
私たちは、対照群の各トピックに対するrepinと再訪問の平均確率$P$ (cRP &RV |q, θ)を計算し、処置群のユーザーあたりのrepinボリューム向上（%）を対照群に対して計算しました。

Figure 9 shows that the topics that have the highest $P$ (cRP &RV |q, θ) (such as Beauty, Architecture, and Entertainment) generated higher repin volume lift than other topics in the treatment group, while the topics that have the lowest $P$ (cRP &RV |q, θ) (e.g., Finance, Health, and Quotes) incurred more negative repin lift. 
図9は、最高の$P$ (cRP &RV |q, θ)（美容、建築、エンターテインメントなど）を持つトピックが処置群の他のトピックよりも高いrepinボリューム向上を生み出した一方で、最低の$P$ (cRP &RV |q, θ)（例：金融、健康、引用）を持つトピックはより多くのネガティブなrepin向上を引き起こしたことを示しています。

**Repin Rate v.s. Revisitation Rate**
Figure 10 uses a heatmap to illustrate the average repin rate, average overall revisitation rate, and revisitation grid-click rates for each topic. 
図10は、各トピックの平均repin率、平均全体再訪問率、および再訪問グリッドクリック率を示すためにヒートマップを使用しています。

We observed that topics such as DIY and Crafts, Parenting, and Health which requires more real-life practices received higher repin rates but lower revisitation rates. 
DIYやクラフト、育児、健康など、より実生活の実践を必要とするトピックは、より高いrepin率を受けましたが、再訪問率は低くなりました。

On the other hands, Beauty, Architecture, Travel, Event Planning, Art, Electronics received lower repin rates but high revisitation rates. 
一方で、美容、建築、旅行、イベント計画、アート、エレクトロニクスは、低いrepin率を受けましたが、高い再訪問率を得ました。

**Long-term v.s. Short-term Revisitation**
In Figure 3b, we observed that the volume of revisitation grid-clicks decays dramatically in the first three days. 
図3bでは、再訪問グリッドクリックのボリュームが最初の3日間で劇的に減少することを観察しました。

8% of the saved Pins received a revisitation grid-click after 0-2 days while the ratio dropped to only 1.9% in the next four days (day 3 to day 6). 
保存されたピンの8%が0-2日後に再訪問グリッドクリックを受けましたが、次の4日間（3日目から6日目）ではその比率がわずか1.9%に減少しました。

In Table 3, we calculated revisit3−6day, the ratio of 3-6 day revisitation grid-click volume to the 0-6 day revisitation grid-click volume for each topic, where a higher ratio indicates that the topic tends to be revisited 3-6 days after saving (longer term revisitation interests). 
表3では、3-6日間の再訪問グリッドクリックボリュームと0-6日間の再訪問グリッドクリックボリュームの比率revisit3−6dayを計算しました。比率が高いほど、そのトピックは保存後3-6日で再訪問される傾向があることを示します（長期的な再訪問の関心）。

The longer term revisitation interests are Event Planning, Health, Home Decor, and DIY and Crafts, which are innately related to long-term user interests. 
長期的な再訪問の関心は、イベント計画、健康、ホームデコレーション、DIYおよびクラフトであり、これらは本質的に長期的なユーザーの関心に関連しています。

The topics which users have the most short-term revisitation interest are Finance, Electronics, Vehicles, Architecture, and Art. 
ユーザーが最も短期的な再訪問の関心を持つトピックは、金融、エレクトロニクス、車両、建築、アートです。

Table 3: Long-term v.s. Short-term Revisitation by Topic
| Topic ratio | Topic ratio |
|---|---|
| Event Planning | 0.1881 |
| Health | 0.1836 |
| Home Decor | 0.1780 |
| DIY and Crafts | 0.1733 |
| Quotes | 0.1725 |
| Beauty | 0.1666 |
| Parenting | 0.1659 |
| Travel | 0.1654 |
| Entertainment | 0.1639 |
| Animals | 0.1633 |
| Education | 0.1602 |
| Art | 0.1572 |
| Architecture | 0.1495 |
| Vehicles | 0.1334 |
| Electronics | 0.1079 |
| Finance | 0.1056 |

### Conclusion
This work introduces a revisitation modeling framework in a multi-task learning recommender system, using Pinterest as a test bed. 
本研究は、Pinterestをテストベッドとして使用したマルチタスク学習推薦システムにおける再訪問モデルフレームワークを紹介します。

By analyzing user save (repin) actions and their cross-session, cross-date revisitation behaviors, we establish causal links between saved Pins and user retention. 
ユーザーの保存（repin）アクションとそのクロスセッション、クロスデートの再訪問行動を分析することにより、保存されたピンとユーザーリテンションの因果関係を確立します。

Our approach encompasses comprehensive behavior analysis, label and feature design for revisitation, and demonstrates scalability to other online platforms. 
私たちのアプローチは、包括的な行動分析、再訪問のためのラベルと特徴の設計を含み、他のオンラインプラットフォームへのスケーラビリティを示します。

Differing from traditional recommender systems that rely on in-session actions, our model leverages cross-session, cross-date, and cross-surface revisitation data, aiming to enhance long-term user retention and core engagement metrics, as validated through both offline and large-scale online experiments. 
従来のセッション内アクションに依存する推薦システムとは異なり、私たちのモデルはクロスセッション、クロスデート、クロスサーフェスの再訪問データを活用し、オフラインおよび大規模オンライン実験を通じて検証された長期的なユーザーリテンションとコアエンゲージメントメトリクスの向上を目指しています。

While our results show the framework effectively drives engagement, revisitation, and retention metrics, we identified a bottleneck: highly active users contribute disproportionately by repinning more than less active users, leading to limited revisitation label data from the latter group. 
私たちの結果は、このフレームワークがエンゲージメント、再訪問、リテンションメトリクスを効果的に推進することを示していますが、ボトルネックを特定しました：非常にアクティブなユーザーは、あまりアクティブでないユーザーよりも多くのrepinを行うことで不均衡に貢献し、後者のグループからの再訪問ラベルデータが限られることにつながります。

To address this, future work could broaden revisitation actions beyond explicit repin events to include implicit signals, such as users interacting with Pins on similar topics across consecutive sessions. 
これに対処するために、今後の研究では、明示的なrepinイベントを超えて再訪問アクションを広げ、連続するセッションで同様のトピックのピンとユーザーが相互作用するなどの暗黙の信号を含めることができるでしょう。

Overall, our work offers a novel, scalable framework for estimating and optimizing user revisitation and long-term retention. 
全体として、私たちの研究は、ユーザーの再訪問と長期的なリテンションを推定し最適化するための新しいスケーラブルなフレームワークを提供します。

### Acknowledgments
We would like to acknowledge our cross-team colleagues Jing Zhang and Yinuo Liu for their invaluable contributions to the productionization of the revisitation labels and revisitation features, respectively. 
私たちは、再訪問ラベルと再訪問機能の製品化に対する貴重な貢献をしてくれたクロスチームの同僚であるJing ZhangとYinuo Liuに感謝します。

We are grateful to Haoran Guo and Liyao Lu for their excellent guidance in shipping this work to production. 
私たちは、この作業を製品化するための優れた指導をしてくれたHaoran GuoとLiyao Luに感謝しています。

We also thank Shivin Thukral, Tianyu Feng, Wendy Shao, Jinfeng Rao, Lu Liu, Jinyu Xie, Matt Chun, Michael Chau, Karim Wahba, and Rajat Raina for their generous support throughout this work. 
また、この作業を通じての寛大なサポートをしてくれたShivin Thukral、Tianyu Feng、Wendy Shao、Jinfeng Rao、Lu Liu、Jinyu Xie、Matt Chun、Michael Chau、Karim Wahba、Rajat Rainaにも感謝します。

| Event Planning | 0.1881 | Health | 0.1836 | Home Decor | 0.1780 | DIY and Crafts | 0.1733 | Quotes | 0.1725 | Beauty | 0.1666 | Parenting | 0.1659 | Travel | 0.1654 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Entertainment | 0.1639 | Animals | 0.1633 | Education | 0.1602 | Art | 0.1572 | Architecture | 0.1495 | Vehicles | 0.1334 | Electronics | 0.1079 | Finance | 0.1056 |
```

. 2025. Augmenting Sequential Recommendation with Balanced Relevance and Diversity. In _Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, 11563–11571._
2025年。バランスの取れた関連性と多様性を持つ逐次推薦の拡張。_AAAI人工知能会議の議事録、第39巻、11563–11571_に掲載。

Ding, R.; Xie, R.; Hao, X.; Yang, X.; Ge, K.; Zhang, X.; Zhou, J.; and Lin, L. 2023. Interpretable user retention modeling in recommendation.
Ding, R.; Xie, R.; Hao, X.; Yang, X.; Ge, K.; Zhang, X.; Zhou, J.; Lin, L. 2023年。推薦における解釈可能なユーザretentionモデル。_第17回ACM推薦システム会議の議事録、702–708_に掲載。

Gong, S.; Liu, Y.; Dang, Y.; Guo, G.; Zhao, J.; and Wang, X. 2025. Multiple Purchase Chains with Negative Transfer Elimination for Multi-Behavior Recommendation.
Gong, S.; Liu, Y.; Dang, Y.; Guo, G.; Zhao, J.; Wang, X. 2025年。多行動推薦のための負の転送排除を伴う複数購入チェーン。_AAAI人工知能会議の議事録、第39巻、11717–11725_に掲載。

Gugnani, A.; and Misra, H. 2020. Implicit skills extraction using document embedding and its use in job recommendation.
Gugnani, A.; Misra, H. 2020年。文書埋め込みを用いた暗黙的スキル抽出とその職業推薦への利用。_AAAI人工知能会議の議事録、第34巻、13286–13293_に掲載。

Guo, X.; Wang, S.; Zhao, H.; Diao, S.; Chen, J.; Ding, Z.; He, Z.; Lu, J.; Xiao, Y.; Long, B.; et al. 2022. Intelligent online selling point extraction for e-commerce recommendation.
Guo, X.; Wang, S.; Zhao, H.; Diao, S.; Chen, J.; Ding, Z.; He, Z.; Lu, J.; Xiao, Y.; Long, B.; et al. 2022年。eコマース推薦のためのインテリジェントなオンライン販売ポイント抽出。_AAAI人工知能会議の議事録、第36巻、12360–12368_に掲載。

Hamilton, W.; Ying, Z.; and Leskovec, J. 2017. Inductive representation learning on large graphs.
Hamilton, W.; Ying, Z.; Leskovec, J. 2017年。大規模グラフにおける帰納的表現学習。_神経情報処理システムの進展、30_に掲載。

Jia, J.; Wang, Y.; Li, Y.; Chen, H.; Bai, X.; Liu, Z.; Liang, J.; Chen, Q.; Li, H.; Jiang, P.; et al. 2025. LEARN: Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application.
Jia, J.; Wang, Y.; Li, Y.; Chen, H.; Bai, X.; Liu, Z.; Liang, J.; Chen, Q.; Li, H.; Jiang, P.; et al. 2025年。LEARN: 大規模言語モデルから実用的な産業応用のための推薦への知識適応。_AAAI人工知能会議の議事録、第39巻、11861–11869_に掲載。

Jin, L.; Feng, L.; Liu, G.; and Wang, C. 2017. Personal web revisitation by context and content keywords with relevance feedback.
Jin, L.; Feng, L.; Liu, G.; Wang, C. 2017年。関連フィードバックを用いた文脈とコンテンツキーワードによる個人ウェブ再訪。_IEEE知識とデータ工学トランザクション、29(7): 1508–1521_に掲載。

Kislyuk, D.; Liu, Y.; Liu, D.; Tzeng, E.; and Jing, Y. 2015. Human curation and convnets: Powering item-to-item recommendations on pinterest.
Kislyuk, D.; Liu, Y.; Liu, D.; Tzeng, E.; Jing, Y. 2015年。人間のキュレーションと畳み込みネットワーク: Pinterestにおけるアイテム間推薦の推進。_arXivプレプリント arXiv:1511.04003_。

Kwon, H.; Han, J.; and Han, K. 2020. ART (Attractive Recommendation Tailor) How the Diversity of Product Recommendations Affects Customer Purchase Preference in Fashion Industry?
Kwon, H.; Han, J.; Han, K. 2020年。ART（魅力的な推薦テイラー）製品推薦の多様性がファッション業界における顧客の購入嗜好にどのように影響するか？_第29回ACM国際情報および知識管理会議の議事録、2573–2580_に掲載。

Liu, D. C.; Rogers, S.; Shiau, R.; Kislyuk, D.; Ma, K. C.; Zhong, Z.; Liu, J.; and Jing, Y. 2017. Related pins at pinterest: The evolution of a real-world recommender system.
Liu, D. C.; Rogers, S.; Shiau, R.; Kislyuk, D.; Ma, K. C.; Zhong, Z.; Liu, J.; Jing, Y. 2017年。Pinterestにおける関連ピン: 実世界の推薦システムの進化。_第26回国際WWWコンパニオン会議の議事録、583–592_に掲載。

Liu, Z.; Liu, S.; Yang, B.; Xue, Z.; Cai, Q.; Zhao, X.; Zhang, Z.; Hu, L.; Li, H.; and Jiang, P. 2024. Modeling User Retention through Generative Flow Networks.
Liu, Z.; Liu, S.; Yang, B.; Xue, Z.; Cai, Q.; Zhao, X.; Zhang, Z.; Hu, L.; Li, H.; Jiang, P. 2024年。生成フローネットワークを通じたユーザretentionのモデル化。_第30回ACM SIGKDD知識発見およびデータマイニング会議の議事録、5497–5508_に掲載。

Ma, J.; Zhao, Z.; Yi, X.; Chen, J.; Hong, L.; and Chi, E. H. 2018. Modeling task relationships in multi-task learning with multi-gate mixture-of-experts.
Ma, J.; Zhao, Z.; Yi, X.; Chen, J.; Hong, L.; Chi, E. H. 2018年。マルチゲート混合専門家を用いたマルチタスク学習におけるタスク関係のモデル化。_第24回ACM SIGKDD国際会議の議事録、1930–1939_に掲載。

Pancha, N.; Zhai, A.; Leskovec, J.; and Rosenberg, C. 2022. Pinnerformer: Sequence modeling for user representation at pinterest.
Pancha, N.; Zhai, A.; Leskovec, J.; Rosenberg, C. 2022年。Pinnerformer: Pinterestにおけるユーザ表現のためのシーケンスモデリング。_第28回ACM SIGKDD知識発見およびデータマイニング会議の議事録、3702–3712_に掲載。

Sun, R.; Kong, R.; Milton, A.; Kluver, D.; Paterson, I.; and Konstan, J. A. 2025. Why They Come And Go: A Case Study of Productive Flyby Users and Their Rating Integrity Challenge in Movie Recommenders.
Sun, R.; Kong, R.; Milton, A.; Kluver, D.; Paterson, I.; Konstan, J. A. 2025年。なぜ彼らは来ては去るのか: 映画推薦における生産的なフライバイユーザとその評価の整合性の課題に関するケーススタディ。_2025年ACM SIGIR人間情報インタラクションおよび検索会議の議事録、1–11_に掲載。

Wang, C.; Kim, L.; Bang, G.; Singh, H.; Kociuba, R.; Pomerville, S.; and Liu, X. 2020. Discovery news: a generic framework for financial news recommendation.
Wang, C.; Kim, L.; Bang, G.; Singh, H.; Kociuba, R.; Pomerville, S.; Liu, X. 2020年。Discovery news: 財務ニュース推薦のための汎用フレームワーク。_AAAI人工知能会議の議事録、第34巻、13390–13395_に掲載。

Wang, R.; Shivanna, R.; Cheng, D.; Jain, S.; Lin, D.; Hong, L.; and Chi, E. 2021. Dcn v2: Improved deep & cross network and practical lessons for web-scale learning to rank systems.
Wang, R.; Shivanna, R.; Cheng, D.; Jain, S.; Lin, D.; Hong, L.; Chi, E. 2021年。DCN v2: 改良された深層およびクロスネットワークとウェブ規模の学習ランキングシステムに関する実践的な教訓。_ウェブ会議2021の議事録、1785–1797_に掲載。

Wang, Y.; Sharma, M.; Xu, C.; Badam, S.; Sun, Q.; Richardson, L.; Chung, L.; Chi, E. H.; and Chen, M. 2022. Surrogate for long-term user experience in recommender systems.
Wang, Y.; Sharma, M.; Xu, C.; Badam, S.; Sun, Q.; Richardson, L.; Chung, L.; Chi, E. H.; Chen, M. 2022年。推薦システムにおける長期ユーザ体験の代理。_第28回ACM SIGKDD知識発見およびデータマイニング会議の議事録、4100–4109_に掲載。

Zhai, A.; Wu, H.-Y.; Tzeng, E.; Park, D. H.; and Rosenberg, C. 2019. Learning a unified embedding for visual search at pinterest.
Zhai, A.; Wu, H.-Y.; Tzeng, E.; Park, D. H.; Rosenberg, C. 2019年。Pinterestにおける視覚検索のための統一埋め込みの学習。_第25回ACM SIGKDD国際会議の議事録、2412–2420_に掲載。

Zhang, Y.; Wang, D.; Li, Q.; Shen, Y.; Liu, Z.; Zeng, X.; Zhang, Z.; Gu, J.; and Wong, D. F. 2021. User Retention: A Causal Approach with Triple Task Modeling.
Zhang, Y.; Wang, D.; Li, Q.; Shen, Y.; Liu, Z.; Zeng, X.; Zhang, Z.; Gu, J.; Wong, D. F. 2021年。ユーザretention: トリプルタスクモデリングによる因果アプローチ。_IJCAI、3399–3405_に掲載。

Zhang, Y.; and Yang, Q. 2021. A survey on multi-task learning.
Zhang, Y.; Yang, Q. 2021年。マルチタスク学習に関する調査。_IEEE知識とデータ工学トランザクション、34(12): 5586–5609_に掲載。

Zhao, K.; Zou, L.; Zhao, X.; Wang, M.; and Yin, D. 2023. User retention-oriented recommendation with decision transformer.
Zhao, K.; Zou, L.; Zhao, X.; Wang, M.; Yin, D. 2023年。ユーザretention指向の推薦における決定トランスフォーマー。_ACMウェブ会議2023の議事録、1141–1149_に掲載。
