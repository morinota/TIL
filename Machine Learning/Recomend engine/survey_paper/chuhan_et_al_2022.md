<!--
title:   [ニュースの個別化推薦]"Personalized News Recommendation: Methods and Challenges"(chuhan et al. 2022)を読んでみた
tags:    Python
-->

## title

"Personalized News Recommendation: Methods and Challenges"(chuhan et al. 2022)

# 1. Introduction

# 2. Framework Of Personalized News Recommendation

## 2.1. News Modeling

## 2.2. User Modeling

## 2.3. Personalized Ranking

## 2.4. Model Training

## 2.5. Evaluation

## 2.6. Dataset And Benchmark

## 2.7. Responsible News Recommendation

- 個人向けニュース推薦に関するほとんどの研究は，推薦結果の精度を向上させることに焦点を当てている。
- 近年，**機械知能システムの責任に関する研究**は，AI技術がよりよく人間に奉仕し，**社会的に負の影響や非倫理的な結果につながる可能性**がある危険で有害な行動さえ避けるために高い注目を集めている
- 個人向けニュース推薦システムの責任を改善するには多くの面がある
- 例えば、多くのニュース推薦手法は私的なユーザデータに基づいて学習されるため、推薦モデルの学習やオンラインサービスにおいてユーザのプライバシーを保護することが重要である
- Federated Learning [137] はプライバシーを考慮した機械学習パラダイムであり、プライバシー保護型のニュース推薦システムの構築を支援することが可能である。
- ニュース推薦の精度を最適化することに加え、ニュース推薦結果の多様性を促進することも重要であり、これにより、情報の多様性に関するユーザのニーズを満たし、イルターバブル問題を緩和することができる[65,164,166,212]
- また，偏ったユーザデータから学習した推薦モデルは不要なバイアスを継承し，アルゴリズムの偏見や不公平な推薦結果を招く可能性があるため，公平性は責任あるニュース推薦の重要な側面である
- ニュース推薦手法の不公平問題を軽減するために，公平性を考慮した機械学習技術[221]は，異なるユーザグループに高品質のニュース推薦サービスを提供する包括的で公平なアルゴリズムの構築を支援することが可能である．
- しかし，既存のサーベイ論文では，責任あるニュース推薦に関する体系的なレビューが不足している.

以上の概要を踏まえ、以下の章では、それぞれの核心的問題について、より深い議論を展開する。

# 3. News Modeling

## 3.1. Feature-Based News Modeling

## 3.2. Deep Learning-Based News Modeling

## 3.3. Discussions On News Modeling

# 4. User Modeling

## 4.1. Feature-Based User Modeling

## 4.2. Deep Learning-Based User Modeling

## 4.3. Discussion On User Modeling

# 5. Personalized Ranking

## 5.1. Relevance-Based Personalized Ranking

## 5.2. Reinforcement Learning-Based Personalized Ranking

## 5.3. Discussions On Personalized Ranking

# 6. Model Training

## 6.1. Training Methods

## 6.2. Training Environment

## 6.3. Discussions On Model Training

# 7. Evaluation Metrics

# 8. Dataset, Competition And Benchmark

# 9. Responsible Personalized News Recommendation

## 9.1. Privacy Protection

## 9.2. Debiasing

## 9.3. Fairness 公平性

## 9.4. Diversity 多様性

## 9.5. Content Moderation 内容の適正化

# 10. Future Direction And Conclusion

## 10.1. Deep News Understanding

## 10.2. Universal User Modeling

## 10.3. Efective And Eficient Personalized Ranking

## 10.4. Hyperbolic Representation Learning For News Recommendation

## 10.5. Unified Model Training

## 10.6. News Recommendation In Social Context

## 10.7. Privacy-Preserving News Recommendation

## 10.8. Secure And Robust News Recommendation

## 10.9. Diversity-Aware News Recommendation 多様性を考慮したニュース推薦

## 10.10. Bias-Free News Recommendation バイアスを除去したニュース推薦

## 10.11. Fairness-Aware News Recommendation

## 10.12. Content Moderation In News Recommendation ニュース推薦におけるコンテンツの適正化

## 10.13. Societal Impact Of News Recommendation ニュース推薦の社会的な影響

# 11. Conclusion
