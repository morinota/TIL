# Recommendations as Treatments: Debiasing Learning and Evaluation

published date: hogehoge September 2022,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://arxiv.org/abs/1602.05352
(勉強会発表者: morinota)

---

## どんなもの?

- 推薦システムを評価・訓練するためのデータの多くは、ユーザ自身の選択行動や推薦システム自体の動作によって、選択バイアスがかかっている.
- 本論文は、実験・観測データに対する因果推論の観点と推薦システムを結びつける事で、推薦システムにおける選択バイアスを扱うアプローチを提案する.
  - 第一に、causal inference(因果推論)の問題で扱われる、**propensity-weighting(傾向性重み付け)技術**を使って、推薦システムの品質を推定する方法を示す.
  - 第二に、propensity-weightingで作成した推定量を用いて、選択バイアス下の推薦システムを学習する為の**Empirical Risk Minimization (ERM) フレームワーク**を提案する.
  - 第三に、ERMフレームワークを用いて、選択バイアスを考慮しつつ、**概念的にシンプルで拡張性の高い行列分解法**を導出する.

## 先行研究と比べて何がすごい？

## 技術や手法の肝は？

## どうやって有効だと検証した?

## 議論はある？

## 次に読むべき論文は？

## お気持ち実装
