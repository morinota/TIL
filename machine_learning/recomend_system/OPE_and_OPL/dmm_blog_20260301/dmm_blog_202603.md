## refs:

- [「指標ハック」から「事業貢献」へ： DMM TV が実践する、レコメンド最適化のプロセス](https://zenn.dev/dmmdata/articles/strategic-search-rec-3)

## 読んだメモ:

- はじめに。
  - DMM TV の事例。
  - 最も重要な動線の一つが、Topページ上部に位置する u2i 棚 (「あなたにおすすめの作品」棚)
    - ほぼ全ユーザが目にする棚。
  - u2i 棚には、従来からTwo-towerモデルをベースとした推薦エンジンを採用 (ブログ内ではalpha engineと呼称)。
    - ユーザの行動履歴から生成したuser embeddingと、作品のメタデータから生成したitem embeddingの近傍探索によって、パーソナライズ推薦を提示するもの。
    - ブログ内の概念図が素敵な図だった...! :pray:
      - アイテムタワーは、item id, category id, text などを入力。
      - ユーザタワーは、ユーザがinteractしたアイテムのembedding (=たぶんアイテムタワーの出力)のsequenceを入力...!! :thinking:

![alt text](image.png)

- 課題: 
  - ある時、従来のAlpha Engineと全く異なるBeta Engineを導入。
  - A/Bテストの結果「u2i棚経由の視聴時間」は大幅に増加したものの、「サービス全体の創始長時間」を見ると微増にとどまった。
    - テストの結果分析を経て、Beta Engineは「**検索や他の棚でどのみち視聴されるはずだった作品をu2i棚に提示することで数字を奪っている**」傾向があることがわかった。
    - 特定の棚の数値がよく見えてるだけで、サービス全体としての視聴純増への寄与は小さい。
  - 特定の棚の数値がよく見えるだけの指標ハックを脱却し、レコメンドによってのみ発生し得る視聴を新規獲得できるようにしたい...!!

- 取り組んだ内容:
  - ボトルネックの特定:
    - hoge
  - オフライン評価の実装:
    - 評価手法:
      - hoge
    - 報酬設計:
      - hoge
  - ボトルネックを狙い撃ちするモデル改善:
    - multi-task学習
      - 「視聴の有無」のbinaryラベルの他に「末端閲覧の有無」と「視聴時間」のラベルも追加して、multi-task学習を実施。
      - 具体的なhowとしては、**末端閲覧履歴と視聴履歴を用いてSampling Weight で重み付け**する形で学習するようにした。
        - たぶん、予測タスクは「視聴の有無」のbinaryタスクのままで、末端閲覧と視聴時間のラベルは、学習時のサンプル重みを決めるために用いている感じ...!!:thinking:
        - たぶん以下みたいな感じ...!!:thinking:
          - y = watch (0 or 1)
          - weight = view + 4*watch + log(duration+1)
          - loss = \sum_{i} (weight_i * BCE(y_i, \hat{y}_i))
        - 注意: **重み付けした報酬関数をそのまま予測するタスクにはしてなくて、あくまでsampling weightに適用してそう...!! なんで?? そっちの方がいいの??**:thinking:
          - 強化学習っぽくいうとimportance weightingに近い。weighted supervised learning。
          - 推薦ドメインではよくあるっぽい??
            - こういう式がよく出る? : `weight = click+ 3 * watch+ log(duration)+ 5 * completion`



## +アルファ調査: クリックベイトを避けたいとして、そのまま合成した報酬関数の回帰タスクにするんじゃなくて、回帰タスクはbinary metricのままでsampling weightを使うアプローチの方がいい理由はなんだろう...!!:thinking:

- refs:
  - 1. Tencent(WeChat)の2022年の論文: [Reweighting Clicks with Dwell Time in Recommendation](https://arxiv.org/abs/2209.09000)
    - ユーザ満足度を学習させるために、click をそのまま使うとノイズが多いのでdwell time で training sample を reweight してる手法。
  - 2. Youtubeの2016年のTwo-tower論文: [Deep Neural Networks for YouTube Recommendations](https://arxiv.org/abs/1609.08675)
    - ランキングモデルを、視聴時間を最大化するように学習させるための具体的なhowとして、clickのBCE lossでロジスティック回帰学習なんだけど、その際に各training sampleをその視聴時間に応じて重み付けしてる。(負例は単位重み、正例は視聴時間に応じた重み)
  - 3. KDD2024年のHuaweiの論文: [Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time](https://arxiv.org/abs/2406.07932)
    - 視聴時間の回帰タスクとして扱わない理由について、duration biasの問題を挙げて説明してる論文。
