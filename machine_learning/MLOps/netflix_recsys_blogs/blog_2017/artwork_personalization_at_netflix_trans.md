## refs 審判

- <https://netflixtechblog.com/artwork-personalization-c589f074ad76> <https://netflixtechblog.com/artwork-personalization-c589f074ad76>

# Artwork Personalization at Netflix Netflixにおけるアートワークのパーソナライズ

For many years, the main goal of the Netflix personalized recommendation system has been to get the right titles in front each of our members at the right time.
長年にわたり、Netflixのパーソナライズド・レコメンデーション・システムの主な目標は、適切なタイトルを適切なタイミングで各会員の前に提供することでした。
With a catalog spanning thousands of titles and a diverse member base spanning over a hundred million accounts, recommending the titles that are just right for each member is crucial.
何千ものタイトルを網羅するカタログと、1億を超えるアカウントに及ぶ多様な会員基盤により、各会員に最適なタイトルを推薦することは極めて重要である。
But the job of recommendation does not end there.
しかし、推薦の仕事はそれだけで終わらない。
Why should you care about any particular title we recommend? What can we say about a new and unfamiliar title that will pique your interest? How do we convince you that a title is worth watching? Answering these questions is critical in helping our members discover great content, especially for unfamiliar titles.
なぜ私たちが推薦する特定のタイトルに関心を持たなければならないのか？新しくて馴染みのないタイトルについて何を語れば興味をそそるのか？どうすれば、そのタイトルが見る価値があると納得してもらえるのか？これらの質問に答えることは、会員が優れたコンテンツ、特に馴染みのないタイトルを発見する上で非常に重要です。
One avenue to address this challenge is to consider the artwork or imagery we use to portray the titles.
この課題を解決するひとつの方法は、タイトルを描写するために使用するアートワークやイメージを検討することだ。
If the artwork representing a title captures something compelling to you, then it acts as a gateway into that title and gives you some visual “evidence” for why the title might be good for you.
あるタイトルを表すアートワークが、あなたにとって魅力的な何かを捉えているならば、それはそのタイトルへの入り口として機能し、なぜそのタイトルがあなたにとって良いかもしれないという視覚的な "証拠 "を与えてくれる。
The artwork may highlight an actor that you recognize, capture an exciting moment like a car chase, or contain a dramatic scene that conveys the essence of a movie or TV show.
あなたが知っている俳優にスポットを当てたり、カーチェイスのようなエキサイティングな瞬間を捉えたり、映画やテレビ番組のエッセンスを伝えるドラマチックなシーンを盛り込んだり。
If we present that perfect image on your homepage (and as they say: an image is worth a thousand words), then maybe, just maybe, you will give it a try.
その完璧なイメージをホームページに提示すれば（そして、彼らは言う： 百聞は一見にしかず）、もしかしたら、もしかしたら、試していただけるかもしれません。
This is yet another way Netflix differs from traditional media offerings: we don’t have one product but over a 100 million different products with one for each of our members with personalized recommendations and personalized visuals.
これが、Netflixが従来のメディアと異なるもう一つの点である： Netflixの商品は1つではなく、1億種類以上あり、会員一人ひとりにパーソナライズされたお薦め商品とパーソナライズされたビジュアルが用意されています。

In previous work, we discussed an effort to find the single perfect artwork for each title across all our members.
前作では、各タイトルの完璧なアートワークを、全メンバーの中から1つだけ探し出す取り組みについて説明した。
Through multi-armed bandit algorithms, we hunted for the best artwork for a title, say Stranger Things, that would earn the most plays from the largest fraction of our members.
マルチアームド・バンディット・アルゴリズムによって、例えば『ストレンジャー・シングス』のようなタイトルのために、メンバーの最大数パーセントから最も再生回数の多い最高のアートワークを探し出した。
However, given the enormous diversity in taste and preferences, wouldn’t it be better if we could find the best artwork for each of our members to highlight the aspects of a title that are specifically relevant to them?
しかし、趣味や嗜好は千差万別であることを考えると、それぞれの会員にとって最適な作品を見つけ、その人に特に関係のあるタイトルの側面を際立たせることができれば、それに越したことはないのではないだろうか。

As inspiration, let us explore scenarios where personalization of artwork would be meaningful.
インスピレーションとして、アートワークのパーソナライズが意味を持つシナリオを探ってみよう。
Consider the following examples where different members have different viewing histories.
メンバーによって視聴履歴が異なる以下の例を考えてみよう。
On the left are three titles a member watched in the past.
左はメンバーが過去に観た3タイトル。
To the right of the arrow is the artwork that a member would get for a particular movie that we recommend for them.
矢印の右側は、私たちが推薦する特定の映画について、会員が手にするアートワークである。

Let us consider trying to personalize the image we use to depict the movie Good Will Hunting.
私たちが映画『グッド・ウィル・ハンティング』を描写するために使っているイメージを、個人的なものにしようと考えてみよう。
Here we might personalize this decision based on how much a member prefers different genres and themes.
ここでは、会員がどの程度異なるジャンルやテーマを好むかによって、この決定をパーソナライズすることもできるだろう。
Someone who has watched many romantic movies may be interested in Good Will Hunting if we show the artwork containing Matt Damon and Minnie Driver, whereas, a member who has watched many comedies might be drawn to the movie if we use the artwork containing Robin Williams, a well-known comedian.
マット・デイモンとミニー・ドライバーが描かれた作品を見せれば、恋愛映画をたくさん見てきた人が『グッド・ウィル・ハンティング』に興味を持つかもしれないし、コメディアンとして有名なロビン・ウィリアムズが描かれた作品を使えば、コメディ映画をたくさん見てきた会員が『グッド・ウィル・ハンティング』に惹かれるかもしれない。

In another scenario, let’s imagine how the different preferences for cast members might influence the personalization of the artwork for the movie Pulp Fiction.
別のシナリオとして、出演者の好みの違いが、映画『パルプ・フィクション』のアートワークのパーソナライゼーションにどのような影響を与えるかを想像してみよう。
A member who watches many movies featuring Uma Thurman would likely respond positively to the artwork for Pulp Fiction that contains Uma.
ユマ・サーマンが出演する映画をよく見る会員なら、ユマが登場する『パルプ・フィクション』のアートワークに好意的な反応を示すだろう。
Meanwhile, a fan of John Travolta may be more interested in watching Pulp Fiction if the artwork features John.
一方、ジョン・トラボルタのファンは、ジョンが登場するアートワークであれば、『パルプ・フィクション』を観たいと思うかもしれない。

Of course, not all the scenarios for personalizing artwork are this clear and obvious.
もちろん、アートワークをパーソナライズするすべてのシナリオが、これほど明確で明白であるとは限らない。
So we don’t enumerate such hand-derived rules but instead rely on the data to tell us what signals to use.
だから、私たちはそのような手作業で導き出したルールを列挙するのではなく、どのようなシグナルを使うべきかを教えてくれるデータに頼っている。
Overall, by personalizing artwork we help each title put its best foot forward for every member and thus improve our member experience.
全体として、アートワークをパーソナライズすることで、各タイトルがすべての会員に最高のサービスを提供し、会員体験を向上させることができます。

## Challenges チャレンジ

At Netflix, we embrace personalization and algorithmically adapt many aspects of our member experience, including the rows we select for the homepage, the titles we select for those rows, the galleries we display, the messages we send, and so forth.
ネットフリックスでは、パーソナライゼーションを採用し、ホームページで選択する行、その行で選択するタイトル、表示するギャラリー、送信するメッセージなど、会員体験の多くの側面をアルゴリズムで適応させている。
Each new aspect that we personalize has unique challenges; personalizing the artwork we display is no exception and presents different personalization challenges.
私たちがパーソナライズする新しい側面には、それぞれユニークな課題があります。私たちが展示するアート作品のパーソナライズも例外ではなく、パーソナライズにはさまざまな課題があります。
One challenge of image personalization is that we can only select a single piece of artwork to represent each title in each place we present it.
イメージ・パーソナライゼーションの課題のひとつは、それぞれのタイトルを表現するために、それぞれの場所で1つの作品しか選べないということだ。
In contrast, typical recommendation settings let us present multiple selections to a member where we can subsequently learn about their preferences from the item a member selects.
対照的に、一般的なレコメンデーション設定では、会員に複数の選択項目を提示し、会員が選択した項目から会員の嗜好を知ることができる。
This means that image selection is a chicken-and-egg problem operating in a closed loop: if a member plays a title it can only come from the image that we decided to present to that member.
つまり、画像の選択は、閉じたループの中で動作する鶏と卵の問題である： もしメンバーがタイトルをプレーすれば、それは我々がそのメンバーに提示すると決めたイメージからしか生まれない。
What we seek to understand is when presenting a specific piece of artwork for a title influenced a member to play (or not to play) a title and when a member would have played a title (or not) regardless of which image we presented.
私たちが理解しようとしているのは、あるタイトルの特定のアートワークを提示したことが、そのタイトルをプレーする（あるいはプレーしない）会員にどのような影響を与えたか、また、私たちがどのようなイメージを提示しても、会員がそのタイトルをプレーした（あるいはプレーしなかった）か、ということである。
Therefore artwork personalization sits on top of the traditional recommendation problem and the algorithms need to work in conjunction with each other.
したがって、アートワーク・パーソナライゼーションは従来の推薦問題の上に位置し、アルゴリズムは互いに連動する必要がある。
Of course, to properly learn how to personalize artwork we need to collect a lot of data to find signals that indicate when one piece of artwork is significantly better for a member.
もちろん、アートワークをパーソナライズする方法を適切に学ぶためには、多くのデータを収集し、あるアートワークがメンバーにとって著しく優れていることを示すシグナルを見つける必要がある。

Another challenge is to understand the impact of changing artwork that we show a member for a title between sessions.
もうひとつの課題は、セッションの合間にメンバーに見せるタイトルのアートワークを変えることの影響を理解することだ。
Does changing artwork reduce recognizability of the title and make it difficult to visually locate the title again, for example if the member thought was interested before but had not yet watched it? Or, does changing the artwork itself lead the member to reconsider it due to an improved selection? Clearly, if we find better artwork to present to a member we should probably use it; but continuous changes can also confuse people.
アートワークを変更することで、タイトルの認知度が下がり、例えば、以前は興味があったがまだ観ていなかった会員が、再びタイトルを視覚的に探すことが困難になるのか。それとも、アートワークそのものを変えることで、品揃えが良くなり、会員が再考するきっかけになるのでしょうか？明らかに、会員に提示するより良いアートワークを見つけたら、それを使うべきだろう。しかし、継続的な変更もまた、人々を混乱させる可能性がある。
Changing images also introduces an attribution problem as it becomes unclear which image led a member to be interested in a title.
また、画像を変更すると、会員がどの画像を見てそのタイトルに興味を持ったのかが不明確になるため、帰属の問題も生じる。

Next, there is the challenge of understanding how artwork performs in relation to other artwork we select in the same page or session.
次に、同じページやセッションで選んだ他のアートワークとの関連で、アートワークがどのように機能するかを理解するという課題がある。
Maybe a bold close-up of the main character works for a title on a page because it stands out compared to the other artwork.
主役の大胆なアップは、他の作品に比べて目立つので、ページのタイトルに効果的なのかもしれない。
But if every title had a similar image then the page as a whole may not seem as compelling.
しかし、すべてのタイトルが同じような画像であった場合、ページ全体として説得力がなくなるかもしれない。
Looking at each piece of artwork in isolation may not be enough and we need to think about how to select a diverse set of images across titles on a page and across a session.
それぞれの作品を単独で見るだけでは十分ではないかもしれないし、ページ上のタイトルやセッション全体にわたって、多様な画像をどのように選択するかを考える必要がある。
Beyond the artwork for other titles, the effectiveness of the artwork for a title may depend on what other types of evidence and assets (e.g.synopses, trailers, etc.) we also display for that title.
他のタイトルのアートワーク以上に、あるタイトルのアートワークの有効性は、そのタイトルについてどのような他のタイプの証拠やアセット（例：シノプス、予告編など）も表示するかによって左右される場合があります。
Thus, we may need a diverse selection where each can highlight complementary aspects of a title that may be compelling to a member.
したがって、会員にとって魅力的なタイトルの補完的な側面をそれぞれが強調できるような、多様なセレクションが必要かもしれない。

To achieve effective personalization, we also need a good pool of artwork for each title.
効果的なパーソナライゼーションを実現するには、各タイトルに適したアートワークのプールも必要だ。
This means that we need several assets where each is engaging, informative and representative of a title to avoid “clickbait”.
つまり、"クリックベイト "を避けるために、それぞれが魅力的で、有益で、タイトルを代表するような複数のアセットが必要なのだ。
The set of images for a title also needs to be diverse enough to cover a wide potential audience interested in different aspects of the content.
また、タイトルの画像は、コンテンツのさまざまな側面に興味を持つ潜在的な視聴者を幅広くカバーできるよう、十分に多様である必要がある。
After all, how engaging and informative a piece of artwork is truly depends on the individual seeing it.
結局のところ、作品がどれだけ魅力的で有益なものであるかは、それを見る個人次第なのだ。
Therefore, we need to have artwork that highlights not only different themes in a title but also different aesthetics.
したがって、タイトルの異なるテーマだけでなく、異なる美学を際立たせるアートワークが必要なのだ。
Our teams of artists and designers strive to create images that are diverse across many dimensions.
私たちのアーティストとデザイナーのチームは、さまざまな次元で多様なイメージを創造するよう努めています。
They also take into consideration the personalization algorithms which will select the images during their creative process for generating artwork.
また、アートワークを生成するためのクリエイティブなプロセスにおいて、画像を選択するパーソナライゼーション・アルゴリズムも考慮に入れている。

Finally, there are engineering challenges to personalize artwork at scale.
最後に、アートワークを大規模にパーソナライズするには、工学的な課題がある。
One challenge is that our member experience is very visual and thus contains a lot of imagery.
ひとつの課題は、私たちの会員体験は非常に視覚的で、そのため多くの画像が含まれていることです。
So using personalized selection for each asset means handling a peak of over 20 million requests per second with low latency.
つまり、各アセットにパーソナライズされたセレクションを使用するということは、ピーク時には毎秒2000万を超えるリクエストを低レイテンシーで処理することを意味する。
Such a system must be robust: failing to properly render the artwork in our UI brings a significantly degrades the experience.
このようなシステムは堅牢でなければならない： UIのアートワークを適切にレンダリングできないと、体験は著しく低下する。
Our personalization algorithm also needs to respond quickly when a title launches, which means rapidly learning to personalize in a cold-start situation.
私たちのパーソナライゼーション・アルゴリズムは、タイトルが発売されたときに素早く反応する必要もある。
Then, after launch, the algorithm must continuously adapt as the effectiveness of artwork may change over time as both the title evolves through its life cycle and member tastes evolve.
そして発売後も、タイトルのライフサイクルの進化や会員の嗜好の変化に伴い、アートワークの効果が時間とともに変化する可能性があるため、アルゴリズムは継続的に適応していかなければならない。

## Contextual bandits approach ♪コンテクスチュアル・バンディッツ・アプローチ

Much of the Netflix recommendation engine is powered by machine learning algorithms.
ネットフリックスのレコメンデーションエンジンの多くは、機械学習アルゴリズムによって動いている。
Traditionally, we collect a batch of data on how our members use the service.
従来から、会員がどのようにサービスを利用しているかについてのデータを一括して収集している。
Then we run a new machine learning algorithm on this batch of data.
次に、このデータのバッチに対して新しい機械学習アルゴリズムを実行する。
Next we test this new algorithm against the current production system through an A/B test.
次に、A/Bテストを通じて、この新しいアルゴリズムを現在の本番システムと比較テストする。
An A/B test helps us see if the new algorithm is better than our current production system by trying it out on a random subset of members.
A/Bテストは、ランダムなメンバーのサブセットで試すことで、新しいアルゴリズムが現在の本番システムよりも優れているかどうかを確認するのに役立ちます。
Members in group A get the current production experience while members in group B get the new algorithm.
グループAのメンバーは現在の生産経験を得、グループBのメンバーは新しいアルゴリズムを得る。
If members in group B have higher engagement with Netflix, then we roll-out the new algorithm to the entire member population.
グループBのメンバーのネットフリックスへのエンゲージメントが高ければ、新しいアルゴリズムをメンバー全体に展開する。
Unfortunately, this batch approach incurs regret: many members over a long period of time did not benefit from the better experience.
残念ながら、この一括アプローチは後悔を生む： 長期間にわたって多くの会員が、より良い経験の恩恵を受けられなかったのだ。
This is illustrated in the figure below.
これは下の図に示されている。

To reduce this regret, we move away from batch machine learning and consider online machine learning.
この後悔を減らすために、私たちはバッチ機械学習から脱却し、オンライン機械学習を考える。
For artwork personalization, the specific online learning framework we use is contextual bandits.
アートワークのパーソナライゼーションのために、我々が使用している特定のオンライン学習フレームワークは、コンテクスチュアル・バンディットである。
Rather than waiting to collect a full batch of data, waiting to learn a model, and then waiting for an A/B test to conclude, contextual bandits rapidly figure out the optimal personalized artwork selection for a title for each member and context.
データの完全なバッチを収集し、モデルを学習し、A/Bテストが終了するのを待つのではなく、コンテクスチュアル・バンディットは、各メンバーとコンテクスチュアに最適なタイトルのパーソナライズされたアートワークの選択を迅速に見つけ出す。
Briefly, contextual bandits are a class of online learning algorithms that trade off the cost of gathering training data required for learning an unbiased model on an ongoing basis with the benefits of applying the learned model to each member context.
簡単に説明すると、コンテキスト・バンディットはオンライン学習アルゴリズムの一種であり、不偏モデルを継続的に学習するために必要な学習データを収集するコストと、学習したモデルを各メンバーのコンテキストに適用する利点をトレードオフするものである。
In our previous unpersonalized image selection work, we used non-contextual bandits where we found the winning image regardless of the context.
私たちの以前の非個人化画像選択研究では、文脈に関係なく勝利画像を見つける非文脈バンディットを使用しました。
For personalization, the member is the context as we expect different members to respond differently to the images.
パーソナライゼーションでは、メンバーによって画像に対する反応が異なることが予想されるため、メンバーがコンテキストとなる。

A key property of contextual bandits is that they are designed to minimize regret.
コンテクスチュアル・バンディットの重要な特性は、後悔を最小化するように設計されていることである。
At a high level, the training data for a contextual bandit is obtained through the injection of controlled randomization in the learned model’s predictions.
高度なレベルでは、文脈バンディットの訓練データは、学習されたモデルの予測に制御されたランダム化を注入することによって得られる。
The randomization schemes can vary in complexity from simple epsilon-greedy formulations with uniform randomness to closed loop schemes that adaptively vary the degree of randomization as a function of model uncertainty.
ランダム化スキームは、一様なランダム性を持つ単純なε-greedy定式化から、モデルの不確実性の関数としてランダム化の程度を適応的に変化させる閉ループスキームまで、複雑さは様々である。
We broadly refer to this process as data exploration.
私たちはこのプロセスを広くデータ探索と呼んでいる。
The number of candidate artworks that are available for a title along with the size of the overall population for which the system will be deployed informs the choice of the data exploration strategy.
あるタイトルで利用可能な候補作品の数は、システムが展開される全体的な母集団の規模とともに、データ探索戦略の選択に反映される。
With such exploration, we need to log information about the randomization for each artwork selection.
このような探査では、作品選択ごとにランダム化に関する情報を記録する必要がある。
This logging allows us to correct for skewed selection propensities and thereby perform offline model evaluation in an unbiased fashion, as described later.
このロギングによって、後述するように、偏った選択傾向を補正し、不偏的な方法でオフラインのモデル評価を行うことができる。

Exploration in contextual bandits typically has a cost (or regret) due to the fact that our artwork selection in a member session may not use the predicted best image for that session.
コンテクスチュアル・バンディットの探索には、通常、コスト（または後悔）が伴う。これは、メンバー・セッションでの作品選択が、そのセッションで予測された最良の画像を使用しない可能性があるためである。
What impact does this randomization have on the member experience (and consequently on our metrics)? With over a hundred millions members, the regret incurred by exploration is typically very small and is amortized across our large member base with each member implicitly helping provide feedback on artwork for a small portion of the catalog.
このランダム化は、メンバーの経験（ひいては私たちの指標）にどのような影響を与えるのでしょうか？1億人以上の会員がいるため、探索によって発生する後悔は一般的に非常に小さく、各会員が暗黙のうちにカタログのごく一部のアートワークに対するフィードバックを提供することで、大規模な会員ベース全体で償却されます。
This makes the cost of exploration per member negligible, which is an important consideration when choosing contextual bandits to drive a key aspect of our member experience.
これは、会員体験の重要な側面を促進するためにコンテクスチュアル・バンディットを選択する際の重要な考慮事項である。
Randomization and exploration with contextual bandits would be less suitable if the cost of exploration were high.
ランダム化とコンテクスト・バンディットによる探索は、探索のコストが高ければ適さない。

Under our online exploration scheme, we obtain a training dataset that records, for each (member, title, image) tuple, whether that selection resulted in a play of the title or not.
私たちのオンライン探索スキームでは、各（メンバー、タイトル、画像）タプルについて、その選択がタイトルの再生につながったかどうかを記録するトレーニングデータセットを得る。
Furthermore, we can control the exploration such that artwork selections do not change too often.
さらに、作品のセレクトがあまり頻繁に変わらないように、探索をコントロールすることもできる。
This gives a cleaner attribution of the member’s engagement to specific artwork.
これにより、メンバーの特定の作品への関与をより明確に示すことができる。
We also carefully determine the label for each observation by looking at the quality of engagement to avoid learning a model that recommends “clickbait” images: ones that entice a member to start playing but ultimately result in low-quality engagement.
また、「クリックベイト」画像を推奨するモデルの学習を避けるために、エンゲージメントの質を見て各観察のラベルを慎重に決定します： メンバーを誘惑してプレーを開始させるが、最終的には質の低いエンゲージメントになるような「クリックベイト」画像を推奨するモデルを学習しないようにするためである。

### Model training モデルトレーニング

In this online learning setting, we train our contextual bandit model to select the best artwork for each member based on their context.
このオンライン学習環境では、コンテキスト・バンディット・モデルを訓練して、各メンバーのコンテキストに基づいて最適な作品を選択する。
We typically have up to a few dozen candidate artwork images per title.
通常、1タイトルにつき数十点のアートワーク候補画像を用意しています。
To learn the selection model, we can consider a simplification of the problem by ranking images for a member independently across titles.
選択モデルを学習するために、あるメンバーの画像をタイトル間で独立にランク付けすることで、問題を単純化することを考えることができる。
Even with this simplification we can still learn member image preferences across titles because, for every image candidate, we have some members who were presented with it and engaged with the title and some members who were presented with it and did not engage.
このように単純化しても、すべての画像候補について、それを提示され、タイトルに関与した会員と、それを提示され、関与しなかった会員がいるため、タイトルをまたいだ会員の画像嗜好を学習することができる。
These preferences can be modeled to predict for each (member, title, image) tuple, the probability that the member will enjoy a quality engagement.
これらの嗜好をモデル化することで、各（メンバー、タイトル、画像）タプルについて、そのメンバーが質の高いエンゲージメントを享受する確率を予測することができる。
These can be supervised learning models or contextual bandit counterparts with Thompson Sampling, LinUCB, or Bayesian methods that intelligently balance making the best prediction with data exploration.
これらは、教師あり学習モデル、もしくはcontextual bandit対応のアプローチ(Thompson Sampling、LinUCB、ベイズ法)である。contextual bandit対応のアプローチは、最良の予測とデータ探索を賢くバランスさせる。

### Potential signals 潜在的なシグナル

In contextual bandits, the context is usually represented as an feature vector provided as input to the model.
コンテキスト・バンディットでは、コンテキストは通常、モデルへの入力として提供される特徴ベクトルとして表現される。
There are many signals we can use as features for this problem.
この問題の特徴として使える信号はたくさんある。
In particular, we can consider many attributes of the member: the titles they’ve played, the genre of the titles, interactions of the member with the specific title, their country, their language preferences, the device that the member is using, the time of day and the day of week.
特に、会員の多くの属性を考慮することができる： プレイしたタイトル、タイトルのジャンル、会員と特定のタイトルとのインタラクション、会員の国、言語の好み、会員が使用しているデバイス、時間帯、曜日などです。
Since our algorithm selects images in conjunction with our personalized recommendation engine, we can also use signals regarding what our various recommendation algorithms think of the title, irrespective of what image is used to represent it.
私たちのアルゴリズムは、パーソナライズされた推薦エンジンと連動して画像を選択するため、どのような画像がタイトルに使用されているかに関係なく、私たちの様々な推薦アルゴリズムがタイトルをどのように考えているかに関するシグナルを使用することもできます。

An important consideration is that some images are naturally better than others in the candidate pool.
重要な考慮点は、候補の中には当然、他よりも優れた画像があるということだ。
We observe the overall take rates for all the images in our data exploration, which is simply the number of quality plays divided by the number of impressions.
これは、単純にクオリティ・プレイの数をインプレッション数で割ったものである。
Our previous work on unpersonalized artwork selection used overall differences in take rates to determine the single best image to select for a whole population.
パーソナライズされていない作品選択に関する私たちの以前の研究では、全体的な撮影率の違いを利用して、集団全体で選択すべき単一の最良の画像を決定した。
In our new contextual personalized model, the overall take rates are still important and personalization still recovers selections that agree on average with the unpersonalized model’s ranking.
私たちの新しい文脈パーソナライズド・モデルでは、全体的なテイクレートは依然として重要であり、パーソナライズは依然として、パーソナライズされていないモデルのランキングと平均的に一致する選択を回復する。

### Image Selection 画像選択

The optimal assignment of image artwork to a member is a selection problem to find the best candidate image from a title’s pool of available images.
画像アートワークのメンバーへの最適な割り当ては、タイトルの利用可能な画像プールから最良の候補画像を見つける選択問題です。
Once the model is trained as above, we use it to rank the images for each context.
上記のようにモデルが学習されたら、それを使って各コンテキストの画像をランク付けする。
The model predicts the probability of play for a given image in a given a member context.
このモデルは、ある会員のコンテクストにおいて、ある画像がプレーされる確率を予測する。
We sort a candidate set of images by these probabilities and pick the one with the highest probability.
これらの確率によって画像の候補セットをソートし、最も確率の高いものを選ぶ。
That is the image we present to that particular member.
それが、私たちが特定のメンバーに示すイメージなのだ。

## Performance evaluation パフォーマンス評価

### Offline オフライン

To evaluate our contextual bandit algorithms prior to deploying them online on real members, we can use an offline technique known as replay [1].
コンテキスト・バンディット・アルゴリズムを実際のメンバーにオンライン展開する前に評価するために、リプレイ[1]として知られるオフライン技術を使用することができる。
This method allows us to answer counterfactual questions based on the logged exploration data (Figure 1).
この方法により、記録された探査データに基づいて、反事実的な質問に答えることができる（図1）。
In other words, we can compare offline what would have happened in historical sessions under different scenarios if we had used different algorithms in an unbiased way.
言い換えれば、公平な方法で異なるアルゴリズムを使用した場合、異なるシナリオの下で、過去のセッションで何が起こったかをオフラインで比較することができる。

Replay allows us to see how members would have engaged with our titles if we had hypothetically presented images that were selected through a new algorithm rather than the algorithm used in production.
リプレイを使えば、もし仮に、本番で使われたアルゴリズムではなく、新しいアルゴリズムで選ばれた画像を提示したとしたら、会員がどのようにタイトルに関与したかを見ることができる。
For images, we are interested in several metrics, particularly the take fraction, as described above.
画像については、前述のように、いくつかのメトリクス、特にテイク・フラクションに関心がある。
Figure 2 shows how contextual bandit approach helps increase the average take fraction across the catalog compared to random selection or non-contextual bandits.
図2は、コンテキスト・バンディット・アプローチが、ランダム・セレクションや非コンテクスト・バンディットと比較して、カタログ全体の平均獲得率を高めるのに役立っていることを示している。

### Online オンライン

After experimenting with many different models offline and finding ones that had a substantial increase in replay, we ultimately ran an A/B test to compare the most promising personalized contextual bandits against unpersonalized bandits.
オフラインでさまざまなモデルを実験し、再生回数が大幅に増加するモデルを見つけた後、最終的にA/Bテストを実施し、最も有望なパーソナライズされたコンテクスト盗賊団と、パーソナライズされていない盗賊団を比較した。
As we suspected, the personalization worked and generated a significant lift in our core metrics.
思惑通り、パーソナライゼーションは功を奏し、主要な指標は大幅に向上した。
We also saw a reasonable correlation between what we measured offline in replay and what we saw online with the models.
また、リプレーでオフラインで計測したものと、モデルを使ってオンラインで見たものとの間には、それなりの相関関係があった。
The online results also produced some interesting insights.
オンラインの結果からも興味深い洞察が得られた。
For example, the improvement of personalization was larger in cases where the member had no prior interaction with the title.
例えば、パーソナライゼーションの向上は、会員がタイトルと過去に接したことがないケースの方が大きかった。
This makes sense because we would expect that the artwork would be more important to someone when a title is less familiar.
これは理にかなっている。というのも、あまり馴染みのないタイトルの場合、アートワークがより重要視されると予想されるからだ。

## Conclusion 結論

With this approach, we’ve taken our first steps in personalizing the selection of artwork for our recommendations and across our service.
このアプローチにより、私たちは推薦作品やサービス全体の作品選択をパーソナライズする第一歩を踏み出しました。
This has resulted in a meaningful improvement in how our members discover new content… so we’ve rolled it out to everyone! This project is the first instance of personalizing not just what we recommend but also how we recommend to our members.
その結果、会員が新しいコンテンツを発見する方法が有意義に改善されました！このプロジェクトは、私たちが何を推薦するかだけでなく、どのように会員に推薦するかをパーソナライズする最初の例です。
But there are many opportunities to expand and improve this initial approach.
しかし、この最初のアプローチを拡大し、改善する機会はたくさんある。
These opportunities include developing algorithms to handle cold-start by personalizing new images and new titles as quickly as possible, for example by using techniques from computer vision.
このような機会には、新しい画像や新しいタイトルをできるだけ早くパーソナライズすることで、コールドスタートに対応するアルゴリズムを開発することも含まれる。
Another opportunity is extending this personalization approach across other types of artwork we use and other evidence that describe our titles such as synopses, metadata, and trailers.
もうひとつの機会は、このパーソナライゼーション・アプローチを、私たちが使用する他のタイプのアートワークや、あらすじ、メタデータ、予告編など、タイトルを説明する他の証拠に拡張することだ。
There is also an even broader problem: helping artists and designers figure out what new imagery we should add to the set to make a title even more compelling and personalizable.
さらに広い問題もある： アーティストやデザイナーが、タイトルをより魅力的で個性的なものにするために、どのような新しいイメージをセットに加えるべきかを考える手助けをすることだ。

If these types of challenges interest you, please let us know! We are always looking for great people to join our team, and, for these types of projects, we are especially excited by candidates with machine learning and/or computer vision expertise.
このような課題にご興味がありましたら、ぜひお知らせください！この種のプロジェクトでは、機械学習やコンピュータ・ビジョンの専門知識を持つ候補者を特に歓迎します。
