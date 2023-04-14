# Twitter's Recommendation Algorithm

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://blog.twitter.com/engineering/en_us/topics/open-source/2023/twitter-recommendation-algorithm
url(github-repositoy): https://github.com/twitter/the-algorithm
(勉強会発表者: morinota)

---

## どんなもの?

- twitter で稼働している 推薦システムに関する、techブログ 及び githubリポジトリが公開された.
- twitterでは様々なパーソナライズ推薦のサービスが稼働しているとのこと. ex. ユーザフォローの推薦, トピックス(キーワードフォロー的な概念?)の推薦, トレンドやイベントの推薦, etc.
- 今回主に公開されたサービスとしては"**For Youフィード**"(おすすめフィード?)に表示される **ツイートアイテムをユーザ毎にパーソナライズする機能**なのかな.

## 先行研究と比べて何がすごい？

論文ではないためパスします!

## 技術や手法の肝は？

推薦システムにおける推論処理は、以下の三段階に分かれているとのこと.

- Candidate Sources
- Ranking
- heuristics and filters

### 段階1: Candidate Sources

この段階では、まず推薦アイテムの候補を取得する.
各リクエストに対して、以下のソースを通じて、数億ツイートのプールから推薦候補1500ツイートを抽出することを試みる.
推薦アイテムのCandidate Source(出どころ?)は大きく二種類に分けられる: In-network source と Out-of-network source.
現在、For Youフィードのタイムラインは、平均して50％のIn-Networkツイートと50％のOut-of-Networkツイートで構成されている.

In-Network sourceからのcandidate生成では、ユーザ自身がフォローしているユーザのツイートから、最も関連性の高い最新のツイートを取得する事を目的としている.
light-ranker(ロジスティック回帰モデル)を使って、フォローした人のツイートを関連性に基づいてランク付けする.

Out-of-network sourceからのcandidate生成では、ユーザのネットワーク(i.e.フォロー関係)の外側にある、ユーザと関連度の高いツイートを取得する事を目的としている. 最終的には、In-Network source同様にlight-ranker(ロジスティック回帰モデル)を使ってランク付けし、上位ツイートを推薦アイテム候補として段階2に送る.
Out-of-network sourceにおいて主に使用される特徴量は、ユーザ-ユーザネットワーク(ユーザフォローのネットワーク)から抽出された コミュニティ表現ベクトル. これは[SimClusters](https://www.kdd.org/kdd2020/accepted-papers/view/simclusters-community-based-representations-for-heterogeneous-recommendatio)にもとづいて生成される.
(次週はこのSimClustesの手法をまとめる予定! このSimClustesによるユーザやアイテムのコミュニティ表現ベクトルは、**twitterのあらゆる推薦・パーソナライズ機能で共通利用されているembedding**らしい. **SNS特有のネットワークに基づく手法だが、使い勝手がかなり良さそうで興味深い**..!!)

### 段階2: Ranking

段階1で得られた推薦アイテム候補(1ユーザ当たり1500件ほど)に対して、Heavy Rankerを用いてランキングする.
Heavy Rankerは、 Candidate Sourcesの段階を柄したツイートをランク付けする為に使用されるMLシステム.
この段階では、どの candidate source から出たものであるかは関係なく、**すべての candidates が平等に扱われる**.
Heavy Rankerで採用されているMLモデルは、 [MaskNet(深層学習に基づくFactotization Machine系列のモデル)](https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md).

このモデルは、ツイート(アイテム)と推薦されるユーザに関する特徴量を受け取り、user engagement(ユーザ体験の良し悪し、みたいな意味合い?)を表現する10個のラベル確信度(binaryラベルに所属する確率というか確信度というか $0 ~ 1$の値)を出力する.

- `scored_tweets_model_weight_fav：` ユーザがそのツイートをお気に入りにする確率.
- `scored_tweets_model_weight_retweet`: ユーザがツイートをリツイートする確率.
- `scored_tweets_model_weight_reply`: ユーザがそのツイートに対して返信する確率.
- `scored_tweets_model_weight_good_profile_click` ： ユーザがツイート作成者のプロフィールを開き、ツイートに「いいね！」または「返信」する確率.
- `scored_tweets_model_weight_video_playback50`: ユーザが動画の半分以上を視聴する確率(動画ツイートの場合).
- `scored_tweets_model_weight_reply_engaged_by_author` :ユーザがツイートに対して返信し、この返信がツイート作成者によってエンゲージされる確率.
- `scored_tweets_model_weight_good_click` ： ユーザがこのツイートの会話をクリックし、ツイートに返信したり「いいね！」したりする確率.
- `scored_tweets_model_weight_good_click_v2` ： ユーザがこのツイートの会話をクリックし、少なくとも2分間そこにとどまる確率.
- `scored_tweets_model_weight_negative_feedback_v2` : ユーザが否定的な反応（ツイートや作者に対して「表示回数を減らす」ことを要求したり、ツイート作者をブロックしたりミュートしたりする）をする確率.
- `scored_tweets_model_weight_report`: ユーザがツイートを報告するをクリックする確率.

10個のMLモデル出力値は、重み付け和として一つの推薦スコアとして統合される. 各出力値の重み付け設定は以下.

- `scored_tweets_model_weight_fav：` 0.5
- `scored_tweets_model_weight_retweet`: 1.0
- `scored_tweets_model_weight_reply`: 13.5
- `scored_tweets_model_weight_good_profile_click` ：12.0
- `scored_tweets_model_weight_video_playback50`: 0.005
- `scored_tweets_model_weight_reply_engaged_by_author` :75.0
- `scored_tweets_model_weight_good_click` ： 11.0
- `scored_tweets_model_weight_good_click_v2` ： 10.0
- `scored_tweets_model_weight_negative_feedback_v2` : -74.0
- `scored_tweets_model_weight_report`: -369.0

推薦スコアの統合式は以下.

$$
score = \sum_{i} \text{weight of engagement}_i \times \text{probabiliyt of engageement}_i
$$

各エンゲージメントの平均確率はそれぞれ異なるため、当初は、重み付けされたエンゲージメントの確率が平均してスコアにほぼ等しく貢献するように設定されていた. その後、運用上のmetricsを最適化するために、定期的に重みを調整しているらしい.

以下のサービスから特徴量を生成して、Heavy Rankerに入力する.

- GraphJet: ユーザとツイート間の二部構成グラフをリアルタイムに保持するグラフ処理エンジン.[論文link](http://www.vldb.org/pvldb/vol9/p1281-sharma.pdf)
- SimClusters: コミュニティ検出とそのコミュニティへのスパース埋め込み. [論文link](https://www.kdd.org/kdd2020/accepted-papers/view/simclusters-community-based-representations-for-heterogeneous-recommendatio)
- TwHIN: ユーザとツイートのための密な知識グラフの埋め込み
- RealGraph: Twitterユーザが他のユーザと交流する可能性を予測するモデル。
- TweepCred: Twitterユーザの評判を計算するためのPage-Rankアルゴリズム。
- Trust & Safety: NSFWや虐待的なコンテンツを検出するためのモデル。

### 段階3: Heuristics and Filters

段階2でランク付した後、Heuristics とFiltersによる後処理的なプロセスを適用して、"for you"フィードを作る.

例えば、以下のようなfilterを適用する:

- Visibility Filtering:
- Author Diversity:
- Content Balance: In-NetworkツイートとOut-of-Networkツイートを**公平なバランスで配信していることを確認する.**
- Feedback-based Fatigue: **視聴者がそのツイートに対してネガティブなフィードバックをした場合、特定のツイートのスコアを下げる.**
  - (これは、推薦結果を表示した後、ユーザ側から明示的なnegativeフィードバックを受け取って、推薦結果を修正する取り組みなのかな. active learning的な)
- Social Proof: 品質保護として、そのツイートと**二次的なつながりがないネットワーク外のツイートを除外する**. (i.e. あるユーザがフォローしている誰かがそのツイートに関与しているか、そのツイートの作者をフォローしているかを確認する.)

最終的には、"for you"フィード推薦システムの推薦ツイートリストとツイート以外のコンテンツ(ex. 広告, ユーザフォローの推薦, etc.)を混ぜ合わせ、UIに表示する.

## どうやって有効だと検証した?

論文ではないためパスします!

## 感想

推薦システムの流れ自体は王道というか、「推薦候補の用意-> ランク付 -> 後処理をして表示」ではあるが、グラフネットワークを活用した推薦候補や特徴量作成の方法や、実行速度とか分散処理とか色々工夫がありそうだなという印象.
あと個人的には、ranking用のモデルで単にCTR的な指標のみを考慮するのではなく、ユーザがツイートを視聴する時間等を考慮して学習させている点は、「単にクリックさせてしまえばいい」というのではなくユーザ体験が良くなるような推薦を志している感があって良いと思った.
(ただ実際、長期的なユーザ体験の向上に資するような推薦システムでないと、プロダクトを使い続けてもらえず利益が損なわれてしまうと思うので、当たり前といえば当たり前ではあるのかな...)

また自分は現在、Newsアプリの組織に関わらせてもらっているのだが、これまではニュース推薦の分野を主にServeyしていたので、ユーザフォローのネットワークの活用等のSNS分野の技術もServeyしたいと思った.
個人的には、ユーザ-ユーザのフォロー関係グラフから各ユーザが所属するcommunityを発見する**SimClusters**という手法は気になった!(Candidate Sourcesで使われているやつ)

## 次に読むべき論文は？

- [Source Candidateでも使用している SimClustersの論文](https://www.kdd.org/kdd2020/accepted-papers/view/simclusters-community-based-representations-for-heterogeneous-recommendatio)
- [Rankingで使用している FM系列のCTR予測モデルの論文](https://arxiv.org/abs/2102.07619)

## お気持ち実装
