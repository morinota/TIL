## refs

- https://tech-blog.monotaro.com/entry/2022/06/30/090000

## 何それ

- stationary bandit setting(定常バンディット設定)
  - 各アームの報酬分布が時間で変わらないような状況(stationary, 定常状態)を仮定したバンディット設定。
- non-stationary bandit setting(非定常バンディット設定)
  - **各アームの報酬分布が時間とともに変化し得る**ような状況(non-stationary, 非定常状態)を仮定したバンディット設定。

## non-stationary bandit settingに対応するための手法の1つ: A Linear Bandit for Seasonal Environments

- Benedetto et al. (From Amazon)から発表されたICML 2020 Workshopの論文。
- 概要:
  - contextual banditではstationaryな報酬分布を仮定するが、時間的に変化するnon-stationaryな報酬分布は想定していない。しかし、現実はnon-stationaryなものがほとんど。
  - 本論文はnon-stationaryな報酬分布だけでなく、seasonallyな報酬分布も考慮。
  - 本論文の手法では、Base BanditとShadow Bandit という２つのcontextual banditを用いて、報酬分布の変化に適応する。
  - シミュレーターによる実験において、non-stationaryの先行研究と比べて本論文の手法の性能が良かった。
- 背景とモチベーション:
  - 典型的な確率的banditやcontextual banditはstationary bandit settingsを想定してる。
    - i.e. 「観測される報酬はある確率分布に従っており、それは時間とともに変化しない」という問題設定。
  - しかし実環境では、報酬分布が時間とともに変化し得る(non-stationary bandit settings)ことが多い。
    - ex)
      - 日毎のプロモーションで、カートインするかどうかのベルヌーイ分布が変化する。
      - 一時的なイベントによってユーザの嗜好が変化する。
  - また、**報酬分布が季節性(seasonally)を持つこと**もある。
    - ex)
      - 定期的に発生するセールイベント(ブラックフライデー、サイバーマンデー、クリスマスセールなど)によって、特定商品の売上が増加する。
    - この場合、分布は時間経過で変化し、なおかつ周期的に再度同じ分布が到来する。
    - このようなseasonallyな報酬分布の変化の場合は、変化が観測されるたびに再度学習するのではなく、適切に分布の変化を検知し、過去の学習結果を活用することが望ましい(その方が効率的)。
- 提案手法: a
  - hoge
- 実験:
  - hoge

## naiveに非定常バンディット設定に対応する方法

- refs:
  - https://www.jstage.jst.go.jp/article/tjsai/36/3/36_36-3_D-K84/_pdf/-char/ja
- 受動的な手法: 
  - ざっくり何それ?
    - 報酬分布が変化したアームやタイミングを探すことなく、単に**過去の結果よりも直近の結果を重視**することで報酬分布の時間変化に追従する手法。
  - **SW(Sliding Window)-UCB, SW-TS 戦略**
    - **「直近の履歴(スライディングウィンドウ)」だけ使って腕選択する**非定常バンディット用のアルゴリズム。
  - D-UCB戦略
    - 直近のラウンドを重視した重み付き平均を行う。
- 能動的な手法:
  - ざっくり何それ?
    - 変化点検知アルゴリズムを用いて、報酬分布が変化したアームやタイミングを把握し、変化に追従する手法。
  
