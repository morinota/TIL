refs: https://arxiv.org/html/2502.08845v2


University of Siegen シーゲン大学
Faculty IV: Department of Electrical Engineering and Computer Science 学部 IV：電気工学およびコンピュータサイエンス学科
Master Thesis 修士論文
Title: Optimal Dataset Size for Recommender Systems: Evaluating Algorithms’ Performance via Downsampling
タイトル：レコメンダーシステムの最適データセットサイズ：ダウンサンプリングによるアルゴリズムのパフォーマンス評価
Supervisors: Prof. Dr. Jöran Beel, Tobias Vente
指導教員：Jöran Beel教授、Tobias Vente
Name: Ardalan Arabzadeh
氏名：アルダラン・アラバザデ
Email: ardalan.arabzadeh@student.uni-siegen.de
メール：ardalan.arabzadeh@student.uni-siegen.de
Program of Study: Master of Mechatronics
学位プログラム：メカトロニクス修士課程
Date of Submission: 31.01.2025
提出日：2025年1月31日

This thesis investigates the potential of dataset downsampling as a strategy to optimize energy efficiency in recommender systems while maintaining competitive performance. 
この論文は、レコメンダーシステムにおけるエネルギー効率を最適化する戦略としてのデータセットのダウンサンプリングの可能性を調査し、競争力のあるパフォーマンスを維持します。
With the increasing size of datasets posing computational and environmental challenges, this study explores the trade-offs between energy efficiency and recommendation quality in the context of Green Recommender Systems, which aim to minimize environmental impact. 
データセットのサイズが増加することで計算上および環境上の課題が生じる中、この研究は、環境への影響を最小限に抑えることを目的としたグリーンレコメンダーシステムの文脈において、エネルギー効率と推薦品質のトレードオフを探ります。
By applying two downsampling approaches to seven datasets, 12 algorithms, and two levels of core pruning, the research highlights that significant reductions in runtime and carbon emissions can be achieved. 
7つのデータセット、12のアルゴリズム、および2つのコアプルーニングレベルに2つのダウンサンプリングアプローチを適用することで、研究は実行時間と炭素排出の大幅な削減が達成できることを強調します。
For instance, using a downsampling portion of 30% in a typical case can reduce runtime by approximately 52% compared to the full dataset, resulting in a reduction in carbon emissions of up to 51.02KgCO2e during the training of a single algorithm on an individual dataset. 
例えば、典型的なケースで30%のダウンサンプリング部分を使用すると、フルデータセットと比較して実行時間を約52%削減でき、個々のデータセットで単一のアルゴリズムをトレーニングする際に最大51.02KgCO2eの炭素排出削減が得られます。

The analysis reveals that algorithm performance under different downsampling portions is influenced by factors such as dataset characteristics, algorithm complexity, and the specific downsampling configuration (scenario dependent). 
分析は、異なるダウンサンプリング部分におけるアルゴリズムのパフォーマンスが、データセットの特性、アルゴリズムの複雑さ、および特定のダウンサンプリング構成（シナリオ依存）などの要因に影響されることを明らかにします。
In particular, some algorithms, which generally showed lower absolute nDCG@10 scores compared to those that performed better, exhibited lower sensitivity to the amount of training data provided, demonstrating greater potential to achieve optimal efficiency in lower downsampling portions. 
特に、一般的により良いパフォーマンスを示したアルゴリズムと比較して、絶対的なnDCG@10スコアが低いアルゴリズムの中には、提供されるトレーニングデータの量に対する感度が低く、低いダウンサンプリング部分で最適な効率を達成する可能性が高いことを示しました。
For instance, on average, these algorithms retained ∼similar-to∼81% of their full-size performance when using only 50% of the training set. 
例えば、平均して、これらのアルゴリズムはトレーニングセットの50%のみを使用した場合、フルサイズのパフォーマンスの約81%を維持しました。
In certain configurations of the downsampling method, where the focus was on progressively involving more users while keeping the test set fixed in size, they even demonstrated higher nDCG@10 scores than when using the original full-size dataset. 
ダウンサンプリング手法の特定の構成では、テストセットのサイズを固定しながら徐々により多くのユーザーを関与させることに焦点を当てた場合、元のフルサイズデータセットを使用したときよりも高いnDCG@10スコアを示しました。
These findings underscore the feasibility of balancing sustainability and effectiveness, providing practical insights for designing energy-efficient recommender systems and advancing sustainable AI practices. 
これらの発見は、持続可能性と効果のバランスを取ることの実現可能性を強調し、エネルギー効率の良いレコメンダーシステムの設計や持続可能なAIプラクティスの推進に向けた実践的な洞察を提供します。

Keywords: Green Recommender Systems, Energy Efficiency, Dataset Downsampling, Runtime Reduction, Carbon Emissions, Sustainability, Algorithm Performance.
キーワード：グリーンレコメンダーシステム、エネルギー効率、データセットダウンサンプリング、実行時間削減、炭素排出、持続可能性、アルゴリズムパフォーマンス。



## Acknowledgements 謝辞

This thesis was conducted as part of the requirements for the Master of Mechatronics program at the University of Siegen, within the Department of Electrical Engineering and Computer Science. 
この論文は、ジーゲン大学のメカトロニクス修士課程の要件の一部として、電気工学およびコンピュータサイエンス学科で実施されました。

It was completed without any external funding, relying solely on academic and institutional resources. 
外部の資金提供なしで、学術的および制度的なリソースのみに依存して完成しました。

Parts of the work presented in this thesis have been previously published[10], reflecting an important step in disseminating the findings to the broader academic community. 
この論文で提示された作業の一部は以前に発表されており[10]、発見を広範な学術コミュニティに普及させる重要なステップを反映しています。

Additionally, the code used for conducting the experiments is publicly available on GitHub[9], ensuring transparency and reproducibility of the research. 
さらに、実験を行うために使用されたコードはGitHub[9]で公開されており、研究の透明性と再現性を確保しています。

The writing and development of this thesis benefited from the use of ChatGPT for grammar and wording improvements[12], contributing to the clarity and precision of the text. 
この論文の執筆と開発は、文法や表現の改善のためにChatGPTを使用したことで恩恵を受け、テキストの明確さと精度に寄与しました。

Computational resources for the experiments were partially provided by the Omni Cluster at the University of Siegen, for which I am grateful. 
実験のための計算リソースは、ジーゲン大学のオムニクラスターによって部分的に提供され、感謝しています。

I would like to express my sincere gratitude to my supervisors, Professor Dr. Jöran Beel and Ph.D. student Tobias Vente, for their guidance, insightful feedback, and encouragement throughout this research. 
私の指導教官であるJöran Beel教授と博士課程の学生Tobias Venteに、研究全体を通じての指導、洞察に満ちたフィードバック、そして励ましに心から感謝の意を表したいと思います。

Their insights and expertise have been instrumental in shaping this work. 
彼らの洞察と専門知識は、この研究を形作る上で重要な役割を果たしました。



## 1.Introduction 1. はじめに  
### 1.1Background 背景
Recommender systems have become a cornerstone of modern digital platforms, playing a crucial role in e-Commerce, media streaming, and social networks[4,32,46]. 
レコメンダーシステムは、現代のデジタルプラットフォームの基盤となり、eコマース、メディアストリーミング、ソーシャルネットワークにおいて重要な役割を果たしています[4,32,46]。 
These systems are designed to provide personalized recommendations, improve user experiences, and drive the rapid growth of digital services[26,37]. 
これらのシステムは、パーソナライズされた推薦を提供し、ユーザー体験を向上させ、デジタルサービスの急速な成長を促進するように設計されています[26,37]。 
Techniques like collaborative filtering, content-based filtering, and hybrid methods are commonly employed to make accurate and meaningful recommendations[45,56,54,30,17]. 
協調フィルタリング、コンテンツベースのフィルタリング、ハイブリッド手法などの技術が、正確で意味のある推薦を行うために一般的に使用されています[45,56,54,30,17]。 
Recommender systems are commonly evaluated using metrics such as Root Mean Square Error (RMSE), Mean Absolute Error (MAE), Precision, Recall, and normalized Discounted Cumulative Gain (nDCG)[23,48]. 
レコメンダーシステムは、平均二乗誤差（RMSE）、平均絶対誤差（MAE）、適合率、再現率、正規化割引累積ゲイン（nDCG）などの指標を使用して一般的に評価されます[23,48]。 
Among these, nDCG is frequently used for ranking-based evaluations, particularly nDCG@10, which measures the relevance of the top 10 recommendations, with higher scores indicating better performance in prioritizing relevant items[59]. 
これらの中で、nDCGはランキングベースの評価に頻繁に使用され、特にnDCG@10は、上位10件の推薦の関連性を測定し、高いスコアが関連アイテムの優先順位付けにおけるより良いパフォーマンスを示します[59]。 

RMSE  
RMSE  

MAE  
MAE  

nDCG  
nDCG  

nDCG  
nDCG  

nDCG@10  
nDCG@10  

Datasets play a pivotal role in the development and evaluation of recommender systems, as they define the foundation upon which algorithms operate. 
データセットは、レコメンダーシステムの開発と評価において重要な役割を果たし、アルゴリズムが動作する基盤を定義します。 
Publicly available datasets, such as MovieLens and Amazon Reviews, provide diverse scenarios for testing recommender systems in controlled environments[3,11]. 
MovieLensやAmazon Reviewsなどの公開データセットは、制御された環境でレコメンダーシステムをテストするための多様なシナリオを提供します[3,11]。 
These datasets often vary in size, sparsity, and user-item interaction density, making them suitable for studying algorithm scalability, robustness, and performance under different conditions. 
これらのデータセットは、サイズ、スパース性、ユーザーとアイテムの相互作用の密度が異なることが多く、アルゴリズムのスケーラビリティ、堅牢性、および異なる条件下でのパフォーマンスを研究するのに適しています。 
For example, different versions of the MovieLens datasets (100K, 1M, 10M, 20M) are widely recognized for their high data density, well-balanced structure, and consistent rating distribution, making them a common choice for recommender systems research and experiments[28]. 
たとえば、MovieLensデータセットの異なるバージョン（100K、1M、10M、20M）は、高いデータ密度、バランスの取れた構造、一貫した評価分布で広く認識されており、レコメンダーシステムの研究や実験に一般的に選ばれています[28]。 

MovieLens  
MovieLens  

Amazon  
Amazon  

MovieLens  
MovieLens  

100K  
100K  

1M  
1M  

10M  
10M  

20M  
20M  

Datasets are essential not only for evaluating the performance of recommender systems but also for tackling challenges related to scalability and algorithmic efficiency[33,49,43]. 
データセットは、レコメンダーシステムのパフォーマンスを評価するだけでなく、スケーラビリティやアルゴリズムの効率性に関連する課題に取り組むためにも不可欠です[33,49,43]。 
The size of these datasets can vary significantly, ranging from small-scale collections with thousands of interactions to large-scale datasets containing millions or even billions of entries. 
これらのデータセットのサイズは大きく異なり、数千の相互作用を持つ小規模なコレクションから、数百万または数十億のエントリを含む大規模なデータセットまでさまざまです。 
In the training phase, the runtime and resource demands become especially critical when developing algorithms that must operate efficiently in real-world applications, where large datasets and limited computational resources are often encountered[61]. 
トレーニングフェーズでは、大規模なデータセットと限られた計算リソースがしばしば遭遇する現実のアプリケーションで効率的に動作する必要があるアルゴリズムを開発する際に、実行時間とリソースの要求が特に重要になります[61]。 

As the reliance on large datasets and computational resources continues to grow in the development of recommender systems, it is important to consider their broader environmental and societal impacts. 
レコメンダーシステムの開発における大規模データセットと計算リソースへの依存が増す中、これらの技術のより広範な環境的および社会的影響を考慮することが重要です。 
AI systems, including recommender algorithms, often require substantial computational resources, which can lead to increased energy consumption and contribute to greenhouse gas emissions[53]. 
AIシステム、特にレコメンダーアルゴリズムは、しばしば多くの計算リソースを必要とし、これがエネルギー消費の増加を引き起こし、温室効果ガスの排出に寄与する可能性があります[53]。 
As climate change becomes an urgent global challenge, it is essential to recognize and address the environmental footprint of these technologies[58]. 
気候変動が緊急のグローバルな課題となる中、これらの技術の環境への影響を認識し、対処することが不可欠です[58]。 
Developing methods to measure, monitor, and minimize their carbon emissions is crucial to ensure that advancements in AI contribute to sustainable progress rather than exacerbating ecological concerns[16]. 
これらの技術の炭素排出量を測定、監視、最小化する方法を開発することは、AIの進歩が持続可能な進展に寄与し、エコロジーの懸念を悪化させないようにするために重要です[16]. 



### 1.2 研究問題

The increasing reliance on recommender systems has introduced significant computational challenges, particularly in terms of scalability and efficiency. 
推薦システムへの依存が高まる中で、特にスケーラビリティと効率性の観点から、重要な計算上の課題が生じています。

As the volume of available data increases exponentially, processing and analyzing these datasets in real time demands vast computational resources and more advanced algorithms[2,21]. 
利用可能なデータの量が指数関数的に増加するにつれて、これらのデータセットをリアルタイムで処理・分析するには、膨大な計算リソースとより高度なアルゴリズムが必要です[2,21]。

In general, it is observed that the performance of deep learning and AI-based algorithms, including recommender systems, improves with larger training datasets. 
一般的に、推薦システムを含む深層学習およびAIベースのアルゴリズムの性能は、より大きなトレーニングデータセットによって向上することが観察されています。

These expansive datasets allow models to capture more intricate patterns, leading to greater accuracy and enhanced performance[52,40]. 
これらの広範なデータセットは、モデルがより複雑なパターンを捉えることを可能にし、より高い精度と向上した性能をもたらします[52,40]。

However, handling massive datasets comes at a cost: substantial computational resources are required, resulting in prolonged training times, higher operational costs, and increased energy consumption[2,61,21]. 
しかし、大規模なデータセットを扱うことにはコストが伴います。膨大な計算リソースが必要であり、その結果、トレーニング時間が長くなり、運用コストが高くなり、エネルギー消費が増加します[2,61,21]。

Furthermore, the environmental impact of processing these large datasets is substantial, with significant carbon emissions associated with computational demands[58,50,51]. 
さらに、これらの大規模データセットを処理することによる環境への影響は大きく、計算要求に関連する重要な炭素排出があります[58,50,51]。

For instance, the total CO2e emissions generated by conducting all the full-paper experiments presented at ACM RecSys 2023 were equivalent to the emissions produced by 384 flights between New York (USA) and Melbourne (Australia)[35]. 
例えば、ACM RecSys 2023で発表されたすべてのフルペーパー実験によって生成された総CO2e排出量は、ニューヨーク（アメリカ）とメルボルン（オーストラリア）間の384回のフライトによって生じる排出量に相当しました[35]。

The disparity in energy consumption between datasets of different sizes further illustrates this issue. 
異なるサイズのデータセット間のエネルギー消費の不均衡は、この問題をさらに明らかにします。

For example, experiments using the DGCF algorithm revealed that the energy consumed when processing the Yelp-2018 dataset was up to 1,444 times greater than that required for the Hetrec-LastFM dataset, despite the former being only approximately 63 times larger in size[58]. 
例えば、DGCFアルゴリズムを使用した実験では、Yelp-2018データセットを処理する際に消費されるエネルギーが、Hetrec-LastFMデータセットに必要なエネルギーの最大1,444倍であることが明らかになりましたが、前者はサイズが約63倍大きいだけです[58]。

This highlights an important insight: If experiments are conducted on smaller datasets, a significant amount of energy could be saved. 
これは重要な洞察を浮き彫りにします：もし実験が小さなデータセットで行われれば、かなりの量のエネルギーを節約できる可能性があります。

For example, datasets like MovieLens 10M are commonly used for training recommender systems[28], but it is unclear whether utilizing the full 10 million instances is always necessary, especially when employing simple baseline algorithms. 
例えば、MovieLens 10Mのようなデータセットは推薦システムのトレーニングに一般的に使用されます[28]が、特に単純なベースラインアルゴリズムを使用する場合、常に全ての1,000万インスタンスを利用する必要があるかどうかは不明です。

This raises the possibility that smaller subsets of data could achieve comparable performance for certain models while significantly reducing runtime and energy consumption. 
これにより、特定のモデルに対して小さなデータのサブセットが同等の性能を達成しながら、実行時間とエネルギー消費を大幅に削減できる可能性が生じます。

Addressing this aspect is critical to achieving more sustainable and efficient recommender systems. 
この側面に対処することは、より持続可能で効率的な推薦システムを実現するために重要です。

With growing concerns about environmental sustainability, the focus on the environmental impact of computational systems, including recommender systems, has intensified. 
環境の持続可能性に対する懸念が高まる中、推薦システムを含む計算システムの環境への影響に対する関心が高まっています。

Addressing this challenge is the concept of Green Recommender Systems, which aim to mitigate the environmental costs of these systems[58,51,10]. 
この課題に対処するための概念が、これらのシステムの環境コストを軽減することを目指すグリーン推薦システムです[58,51,10]。

As defined by Beel et al.[14]: “Green Recommender Systems” are recommender systems designed to minimize their environmental impact throughout their life cycle, from research and design to implementation and operation. 
Beelらによって定義されたように[14]：「グリーン推薦システム」とは、研究と設計から実装と運用に至るまで、そのライフサイクル全体を通じて環境への影響を最小限に抑えるように設計された推薦システムです。

Green Recommender Systems typically aim to match the performance of traditional systems but may also accept trade-offs in accuracy or other metrics to prioritize sustainability. 
グリーン推薦システムは、通常、従来のシステムの性能に匹敵することを目指しますが、持続可能性を優先するために精度や他の指標においてトレードオフを受け入れることもあります。

Minimizing environmental impact typically but not necessarily means minimizing energy consumption and CO2 emissions.[14] 
環境への影響を最小限に抑えることは、通常、エネルギー消費とCO2排出を最小限に抑えることを意味しますが、必ずしもそうではありません。[14]



### 1.3 Research Question 研究課題

As mentioned earlier, the increasing size and complexity of the datasets used in the recommender systems pose significant computational and environmental challenges. 
前述のように、推薦システムで使用されるデータセットのサイズと複雑さの増加は、重要な計算および環境上の課題を引き起こします。

One potential solution to mitigate these challenges is downsampling the dataset. 
これらの課題を軽減するための一つの潜在的な解決策は、データセットのダウンサンプリングです。

Could reducing it, perhaps to just 10% of its original size, be sufficient to maintain performance while potentially saving up to 90% of the energy required for computation? 
元のサイズのわずか10%に削減することが、パフォーマンスを維持しつつ、計算に必要なエネルギーを最大90%節約するのに十分である可能性はあるのでしょうか？

This raises a broader question: Is it possible to achieve an acceptable trade-off between energy efficiency and performance in recommender algorithms by reducing dataset size? 
これは、データセットのサイズを削減することによって、推薦アルゴリズムにおけるエネルギー効率とパフォーマンスの間で受け入れ可能なトレードオフを達成することが可能かという、より広い問題を提起します。

This study is situated within the broader context of "Green Recommender Systems", which emphasizes minimizing environmental impact while maintaining effective functionality. 
この研究は、「グリーン推薦システム」というより広い文脈の中に位置づけられ、効果的な機能を維持しながら環境への影響を最小限に抑えることを強調しています。

Is it possible to achieve an acceptable trade-off between energy efficiency and performance in recommender algorithms by reducing dataset size? 
データセットのサイズを削減することによって、推薦アルゴリズムにおけるエネルギー効率とパフォーマンスの間で受け入れ可能なトレードオフを達成することが可能でしょうか？



### 1.4 Research Goal 研究目標

The goal of this research is to investigate the potential of dataset downsampling as a means of achieving energy-efficient recommender systems without significantly compromising performance. 
この研究の目的は、データセットのダウンサンプリングの可能性を調査し、パフォーマンスを大きく損なうことなくエネルギー効率の良いレコメンダーシステムを実現することです。

By exploring the relationship between dataset size and performance, this work aims to develop guidelines to minimize the environmental impact of recommender systems, making them more sustainable, possibly without or with minimum sacrificing of accuracy of the recommendation.[10].
データセットのサイズとパフォーマンスの関係を探ることで、この研究はレコメンダーシステムの環境への影響を最小限に抑えるためのガイドラインを開発し、持続可能性を高め、推薦の精度をほとんど犠牲にすることなく、または最小限に抑えることを目指します。

To achieve this goal, our research objectives are as follows:
この目標を達成するために、私たちの研究目的は以下の通りです。

- • Assess impact on recommendation quality: This objective aims to evaluate how and to what extent different downsampling approaches affect critical performance metrics, such as nDCG@10. 
- • 推薦の質への影響を評価する：この目的は、異なるダウンサンプリングアプローチがnDCG@10などの重要なパフォーマンス指標にどのように、またどの程度影響を与えるかを評価することを目指しています。

By evaluating these approaches, we seek to analyze their influence on recommendation quality across varying levels of downsampling and identify thresholds beyond which performance degrades significantly.
これらのアプローチを評価することで、異なるダウンサンプリングのレベルにおける推薦の質への影響を分析し、パフォーマンスが著しく低下する閾値を特定することを目指します。

- • Quantify computational savings: This objective involves measuring the reductions in runtime and the associated CO2e emissions achieved through downsampling of the data set across various algorithms of the recommender system. 
- • 計算コストの削減を定量化する：この目的は、レコメンダーシステムのさまざまなアルゴリズムにおけるデータセットのダウンサンプリングによって達成される実行時間の削減と関連するCO2e排出量を測定することを含みます。

By analyzing these reductions, we aim to estimate the computational and energy savings provided by the proposed downsampling approaches, offering insights into their efficiency and environmental benefits.
これらの削減を分析することで、提案されたダウンサンプリングアプローチによって提供される計算およびエネルギーの節約を推定し、その効率性と環境的利益に関する洞察を提供することを目指します。

- • Develop practical guidelines: Based on our findings, we will propose evidence-based recommendations on the minimal dataset size necessary for effective training and evaluation of recommender systems, with a focus on balancing performance and energy efficiency.
- • 実用的なガイドラインを開発する：私たちの発見に基づいて、レコメンダーシステムの効果的なトレーニングと評価に必要な最小データセットサイズに関するエビデンスに基づく推奨事項を提案し、パフォーマンスとエネルギー効率のバランスを重視します。

In this research, we hypothesize that by downsampling datasets used in recommender systems, we can reduce computational time, energy consumption, and CO2e emissions, while achieving nearly the same recommendation quality as when using full datasets[10].
この研究では、レコメンダーシステムで使用されるデータセットをダウンサンプリングすることで、計算時間、エネルギー消費、CO2e排出量を削減し、フルデータセットを使用した場合とほぼ同じ推薦の質を達成できると仮定します。



### 1.5 Contribution 貢献

This thesis advances the field of Green Recommender Systems by investigating the interplay between dataset size, algorithmic performance, and environmental sustainability. 
この論文は、データセットのサイズ、アルゴリズムの性能、および環境の持続可能性の相互作用を調査することによって、グリーン推薦システムの分野を前進させます。

The study demonstrates that downsampling datasets can yield substantial energy and carbon savings, while the extent of performance compromise depends on the algorithm, dataset, and downsampling method used. 
この研究は、データセットのダウンサンプリングが大幅なエネルギーと炭素の節約をもたらすことを示しており、性能の妥協の程度は使用されるアルゴリズム、データセット、およびダウンサンプリング方法に依存します。

As a reference case, downsampling the training set to 50% reduces runtime by∼similar-to\sim∼27% to∼similar-to\sim∼39% compared to training on the full-size dataset, depending on the downsampling method used. 
参考ケースとして、トレーニングセットを50%にダウンサンプリングすると、使用されるダウンサンプリング方法に応じて、フルサイズのデータセットでのトレーニングと比較して、実行時間が約27%から39%削減されます。

These runtime reductions correspond to significant environmental benefits, translating to carbon emission savings of approximately 26.49KgCO2e to 38.26KgCO2e for training a single algorithm on a single dataset. 
これらの実行時間の削減は、重要な環境上の利点に対応し、単一のデータセットで単一のアルゴリズムをトレーニングする際の炭素排出量の節約は約26.49KgCO2eから38.26KgCO2eに相当します。

On average, across all algorithms and datasets examined, in the specific case of 50% downsampling, performance measured by nDCG@10 can decrease by only∼similar-to\sim∼36% compared to the full dataset size or, in some cases, increase by as much as∼similar-to\sim∼10%, depending on the configurations of the downsampling method and the primary focus it seeks to address. 
調査したすべてのアルゴリズムとデータセットを通じて平均すると、50%のダウンサンプリングの特定のケースでは、nDCG@10で測定された性能はフルデータセットサイズと比較して約36%しか減少せず、場合によってはダウンサンプリング方法の構成と主な焦点に応じて最大10%増加することもあります。

These findings emphasize the potential of optimizing dataset sizes to achieve environmentally sustainable recommender systems while maintaining competitive levels of performance. 
これらの発見は、競争力のある性能レベルを維持しながら、環境的に持続可能な推薦システムを実現するためにデータセットのサイズを最適化する可能性を強調しています。

By quantifying the trade-offs between computational efficiency and algorithmic effectiveness, this work provides actionable insights into designing energy-efficient systems without significant performance degradation, offering a practical path toward sustainability in AI and Recommender systems practices. 
計算効率とアルゴリズムの有効性のトレードオフを定量化することによって、この研究は、重要な性能低下なしにエネルギー効率の良いシステムを設計するための実用的な洞察を提供し、AIおよび推薦システムの実践における持続可能性への実用的な道を提供します。



## 2.Related Work 関連研究

Several studies in the field of recommender systems have explored the relationship between data set size and algorithm performance efficiency, a key focus of this research. 
推薦システムの分野におけるいくつかの研究は、データセットのサイズとアルゴリズムの性能効率との関係を探求しており、これは本研究の重要な焦点です。

Among these, the study by Spillo et al., published shortly before the results of this thesis were reported, investigates the potential of data reduction strategies to improve sustainability in recommender systems[51]. 
これらの中でも、Spilloらによる研究は、本論文の結果が報告される直前に発表され、推薦システムにおける持続可能性を向上させるためのデータ削減戦略の可能性を調査しています[51]。

Their analysis, based on two datasets and nine state-of-the-art algorithms, demonstrated that data reduction can significantly lower the carbon footprint of recommender systems, generally following a linear trend. 
彼らの分析は、2つのデータセットと9つの最先端アルゴリズムに基づいており、データ削減が推薦システムのカーボンフットプリントを大幅に低下させることができることを示し、一般的に線形の傾向に従うことがわかりました。

While data reduction led to an expected decrease in accuracy, they also identified that the trade-off between accuracy and emissions is highly scenario-dependent, requiring careful consideration of application-specific needs. 
データ削減は予想通り精度の低下をもたらしましたが、彼らはまた、精度と排出量のトレードオフがシナリオ依存性が高いことを特定し、アプリケーション固有のニーズを慎重に考慮する必要があることを示しました。

While their findings are insightful, the study’s focus on a single library and a limited dataset variety restricts its generalizability. 
彼らの発見は洞察に富んでいますが、単一のライブラリと限られたデータセットの多様性に焦点を当てているため、一般化可能性が制限されています。

This thesis addresses these gaps by exploring a wider range of datasets, applying different levels of core pruning as preprocessing steps, analyzing two distinct downsampling approaches, and incorporating diverse algorithms, including deep learning models and more traditional algorithms such as UserKNN and ItemKNN, which are commonly used in research. 
本論文は、より広範なデータセットを探求し、前処理ステップとして異なるレベルのコアプルーニングを適用し、2つの異なるダウンサンプリングアプローチを分析し、深層学習モデルや研究で一般的に使用されるUserKNNやItemKNNなどの多様なアルゴリズムを組み込むことで、これらのギャップに対処します。

Furthermore, these analyses leverage three widely used libraries, RecBole, LensKit, and RecPack, to provide a more comprehensive evaluation of the impact of data reduction on performance and energy efficiency. 
さらに、これらの分析は、RecBole、LensKit、RecPackという3つの広く使用されているライブラリを活用し、データ削減が性能とエネルギー効率に与える影響のより包括的な評価を提供します。

In addition to addressing these limitations, other studies have explored related trade-offs between algorithm performance and data constraints. 
これらの制限に対処するだけでなく、他の研究もアルゴリズムの性能とデータ制約との関連するトレードオフを探求しています。

Notably, Bentzer and Thulin explored the trade-off between accuracy and computational efficiency in collaborative filtering algorithms under constrained data scenarios[15]. 
特に、BentzerとThulinは、制約のあるデータシナリオにおける協調フィルタリングアルゴリズムの精度と計算効率のトレードオフを探求しました[15]。

Their findings revealed that the IBCF (Item-Based Collaborating Filtering) algorithm demonstrates superior accuracy in smaller datasets, whereas the SVD (Singular Value Decomposition) algorithm outperforms IBCF in terms of speed and scalability when applied to larger datasets. 
彼らの発見は、IBCF（アイテムベースの協調フィルタリング）アルゴリズムが小規模データセットで優れた精度を示す一方で、SVD（特異値分解）アルゴリズムが大規模データセットに適用された場合に速度とスケーラビリティの面でIBCFを上回ることを明らかにしました。

However, their study is limited to comparing only these two algorithms and does not provide a broader analysis of how other algorithms respond to similar constraints. 
しかし、彼らの研究はこれら2つのアルゴリズムの比較に限られており、他のアルゴリズムが同様の制約にどのように応答するかについてのより広範な分析を提供していません。

To address this limitation, this thesis evaluates a broader range of algorithms, focusing on optimizing both energy efficiency and performance under varying data sizes. 
この制限に対処するために、本論文はより広範なアルゴリズムを評価し、異なるデータサイズの下でエネルギー効率と性能の両方を最適化することに焦点を当てています。

Similarly, Jain and Jindal reviewed the role of sampling and filtering techniques in enhancing the computational efficiency of recommender systems[31]. 
同様に、JainとJindalは、推薦システムの計算効率を向上させるためのサンプリングおよびフィルタリング技術の役割をレビューしました[31]。

Their study provides a theoretical overview of various sampling methods discussed in different papers and, based on their evaluation, suggests specific sampling and filtering methods that are more effective for various applications and domains within recommender systems, including movies, product recommendations, and disease diagnosis systems. 
彼らの研究は、異なる論文で議論されたさまざまなサンプリング方法の理論的概要を提供し、評価に基づいて、映画、製品推薦、病気診断システムなど、推薦システム内のさまざまなアプリケーションおよびドメインに対してより効果的な特定のサンプリングおよびフィルタリング方法を提案しています。

These methods aim to capture essential attributes of dataset by selecting a subset of data, thereby increasing the efficiency and optimizing the learning process. 
これらの方法は、データのサブセットを選択することによってデータセットの重要な属性を捉えることを目的としており、その結果、効率を高め、学習プロセスを最適化します。

While their theoretical insights suggest improvements in speed and accuracy, their lack of empirical evaluation leaves a gap in understanding the practical implications of these methods. 
彼らの理論的な洞察は速度と精度の改善を示唆していますが、実証的な評価が欠如しているため、これらの方法の実際の影響を理解する上でのギャップが残ります。

This thesis complements their theoretical work by offering empirical analyses that bridge the gap between theory and application, focusing on the practical implications of dataset reduction. 
本論文は、理論と応用のギャップを埋める実証分析を提供することで、彼らの理論的な研究を補完し、データセット削減の実際の影響に焦点を当てています。

Despite extensive research on data reduction techniques in domains such as automated machine learning, artificial intelligence, and computer vision[6,19,18,29,44,55], their application in recommender systems remains comparatively under-explored. 
自動機械学習、人工知能、コンピュータビジョンなどの分野におけるデータ削減技術に関する広範な研究にもかかわらず、推薦システムにおけるその適用は比較的未探求のままです。

For instance, Zogaj et al. demonstrated that dataset downsampling in genetic programming-based AutoML systems can lead to improved computational efficiency and, in many cases, enhanced pipeline performance, especially for larger datasets. 
例えば、Zogajらは、遺伝的プログラミングに基づくAutoMLシステムにおけるデータセットのダウンサンプリングが計算効率の向上や、多くの場合、特に大規模データセットにおいてパイプライン性能の向上につながることを示しました。

Their work highlights that optimal downsampling ratios enable exploration of more candidate pipelines, sometimes resulting in models that perform better compared to using the full dataset[62]. 
彼らの研究は、最適なダウンサンプリング比率がより多くの候補パイプラインの探索を可能にし、時にはフルデータセットを使用するよりも優れた性能を発揮するモデルを生み出すことを強調しています[62]。

While these findings reveal the potential benefits of dataset reduction, they are not directly applicable to traditional recommender systems, where similar effects remain underexplored, particularly in the context of automated recommender systems (AutoRecSys[7,27,57]), where vast configuration spaces need to be explored. 
これらの発見はデータセット削減の潜在的な利点を明らかにしていますが、従来の推薦システムには直接適用できず、特に自動推薦システム（AutoRecSys[7,27,57]）の文脈では、広大な構成空間を探索する必要があるため、同様の効果は未探求のままです。

Building on these foundational insights, this thesis adapts and applies data reduction principles specifically to recommender systems, addressing domain-specific challenges and opportunities. 
これらの基礎的な洞察に基づき、本論文はデータ削減の原則を推薦システムに特化して適応し、ドメイン固有の課題と機会に対処します。



## 3.Methodology 方法論  
### 3.1Datasets and Preprocessing データセットと前処理

To conduct our experiments, we utilized seven datasets: MovieLens 100K, MovieLens 1M, MovieLens 10M[28], Amazon 2018 Toys-and-Games, Amazon 2018 CDs-and-Vinyl, Amazon 2018 Electronics[41], and Gowalla[22].  
実験を行うために、私たちは7つのデータセットを利用しました：MovieLens 100K、MovieLens 1M、MovieLens 10M[28]、Amazon 2018 Toys-and-Games、Amazon 2018 CDs-and-Vinyl、Amazon 2018 Electronics[41]、およびGowalla[22]。  
The key statistics for each data set before preprocessing are presented in Table 3.1.  
前処理前の各データセットの主要な統計は、表3.1に示されています。  

MovieLens 100K  
MovieLens 1M  
MovieLens 10M  
Amazon 2018 Toys-and-Games  
Amazon 2018 CDs-and-Vinyl  
Amazon 2018 Electronics  
Gowalla  

3.1  
The preprocessing steps applied to the datasets include:  
データセットに適用された前処理ステップは以下の通りです：  

- • Removal of duplicate rows (i.e., identical user-item-rating combinations).  
- • 重複行の削除（すなわち、同一のユーザ-アイテム-評価の組み合わせ）。  
- • Averaging of duplicate ratings for the same user-item pair with different rating values.  
- • 異なる評価値を持つ同一のユーザ-アイテムペアの重複評価の平均化。  
- • Application of 10-core and 30-core pruning to retain only users and items with at least 10 and 30 interactions, respectively[36,42].  
- • それぞれ少なくとも10回および30回の相互作用を持つユーザとアイテムのみを保持するための10コアおよび30コアのプルーニングの適用[36,42]。  

The statistics of the resulting dataset after preprocessing are summarized in Table 3.2.  
前処理後の結果データセットの統計は、表3.2に要約されています。  
It is important to note that applying 10-core pruning preserves all seven datasets for analysis.  
10コアのプルーニングを適用することで、すべての7つのデータセットが分析のために保持されることは重要です。  
However, under 30-core pruning, only four datasets—MovieLens 100K, MovieLens 1M, MovieLens 10M, and Gowalla—contain sufficient interactions to remain viable for further evaluation.  
しかし、30コアのプルーニングの下では、MovieLens 100K、MovieLens 1M、MovieLens 10M、およびGowallaの4つのデータセットのみが、さらなる評価に適した十分な相互作用を含んでいます。  
The other three datasets were excluded under this criterion due to insufficient data density.  
他の3つのデータセットは、データ密度が不十分であるため、この基準の下で除外されました。  
Consequently, the results and analyses in this thesis primarily utilize the 10-core pruning case with all seven datasets for consistency and comprehensiveness.  
したがって、本論文の結果と分析は、一貫性と包括性のために、主にすべての7つのデータセットを使用した10コアのプルーニングケースを利用しています。  
However, for the specific comparison of 10-core and 30-core pruning presented in Section 4.1 (Supplementary Analysis: 10-Core vs. 30-Core Pruning), only the four datasets supporting both pruning levels are used to ensure a fair and consistent evaluation.  
ただし、セクション4.1（補足分析：10コア対30コアプルーニング）で示される10コアと30コアのプルーニングの具体的な比較については、両方のプルーニングレベルをサポートする4つのデータセットのみが使用され、公平で一貫した評価を確保します。  

3.2  
MovieLens 100K  
MovieLens 1M  
MovieLens 10M  
Gowalla  

4.1  
Additionally, two key features of the datasets, sparsity and entropy, are reported.  
さらに、データセットの2つの重要な特徴、スパース性とエントロピーが報告されています。  
Sparsity quantifies the proportion of missing interactions within the dataset; higher sparsity values indicate fewer observed interactions relative to all possible user-item pairs (i.e., sparsity is the complement of density).  
スパース性は、データセット内の欠落した相互作用の割合を定量化します。高いスパース性の値は、すべての可能なユーザ-アイテムペアに対して観測された相互作用が少ないことを示します（すなわち、スパース性は密度の補数です）。  
Entropy measures the diversity or uniformity of the rating distribution; higher entropy values suggest a more balanced distribution of ratings across the scale.  
エントロピーは、評価分布の多様性または均一性を測定します。高いエントロピーの値は、スケール全体にわたる評価のよりバランスの取れた分布を示唆します。  

Table 3.1:  
表3.1:  

| Dataset                     | Feedback Type | Users | Items | Interactions | Avg Int/User | Avg Int/Item | Sparsity (%) | Entropy |
|-----------------------------|---------------|-------|-------|--------------|--------------|--------------|--------------|---------|
| MovieLens 100K             | Explicit      | 943   | 1,682 | 100,000      | 106          | 599          | 3.7          | 1.46    |
| MovieLens 1M               | Explicit      | 6,040 | 3,706 | 1,000,209    | 165          | 269          | 95.5         | 1.45    |
| MovieLens 10M              | Explicit      | 69,878| 10,677| 10,000,054   | 143          | 936          | 98.6         | 1.33    |
| Gowalla                    | Implicit      | 107,092| 1,280,969| 6,442,892  | 605          | 99.9         | -           | -       |
| Amazon Toys and Games      | Explicit      | 208,180| 78,772| 1,828,971    | 823          | 99.9         | 0.93        | -       |
| Amazon CDs and Vinyl       | Explicit      | 112,395| 73,713| 1,443,755    | 121          | 999          | 99.9        | 1.00    |
| Amazon Electronics          | Explicit      | 728,719| 160,052| 6,739,590    | 942          | 99.9         | 1.10        | -       |

Dataset  
データセット  

| Feedback Type               | Users | Items | Interactions | Avg Int/User | Avg Int/Item | Sparsity (%) | Entropy |
|-----------------------------|-------|-------|--------------|--------------|--------------|--------------|---------|
| Preprocessed with 10-Core pruning | | | | | | | |
| MovieLens 100K             | 943   | 1,152 | 97,953       | 103          | 859          | 0.9          | 1.46    |
| MovieLens 1M               | 6,040 | 3,260 | 998,539      | 165          | 306          | 94.9         | 1.45    |
| MovieLens 10M              | 69,878| 9,708 | 9,995,471    | 143          | 1,029        | 98.5         | 1.33    |
| Gowalla                    | 29,858| 40,988| 1,027,464    | 342          | 599          | 0.9          | -       |
| Amazon Toys and Games      | 11,609| 8,443 | 202,721      | 172          | 499          | 0.7          | 0.97    |
| Amazon CDs and Vinyl       | 21,450| 18,398| 527,503      | 242          | 899          | 0.8          | 1.07    |
| Amazon Electronics          | 135,867| 49,160| 2,260,696    | 164          | 599          | 0.9          | 1.05    |

Preprocessed with 30-Core pruning  
30コアのプルーニングで前処理されたデータ  

| Dataset                     | Users | Items | Interactions | Avg Int/User | Avg Int/Item | Sparsity (%) | Entropy |
|-----------------------------|-------|-------|--------------|--------------|--------------|--------------|---------|
| MovieLens 100K             | 720   | 795   | 86,295       | 119          | 108          | 84.9         | 1.44    |
| MovieLens 1M               | 5,278 | 2,830 | 971,992      | 184          | 343          | 93.4         | 1.45    |
| MovieLens 10M              | 57,496| 8,282 | 9,671,552    | 168          | 116          | 97.9         | 1.33    |
| Gowalla                    | 1,011 | 899   | 61,429       | 606          | 893          | 3.2          | -       |



### 3.2 アルゴリズムと評価

To conduct our experiments, we selected 12 algorithms from three widely used recommender system libraries: LensKit[24], RecPack[39], and RecBole[60]. 
実験を行うために、私たちは3つの広く使用されているレコメンダーシステムライブラリ（LensKit[24]、RecPack[39]、RecBole[60]）から12のアルゴリズムを選択しました。 

Table 3.3 lists the algorithms alongside their corresponding libraries. 
表3.3には、アルゴリズムとそれに対応するライブラリが一覧表示されています。 

The Random algorithm in our experiments serves as a baseline for comparison, providing a reference point to validate the performance of other algorithms. 
私たちの実験におけるRandomアルゴリズムは、他のアルゴリズムの性能を検証するための基準点を提供する比較のためのベースラインとして機能します。 

However, it is excluded from the detailed results and statistics discussed in the following sections. 
しかし、これは次のセクションで議論される詳細な結果と統計からは除外されています。 

Additionally, two algorithms, ItemKNN and Popularity, are implemented using two distinct libraries, LensKit and RecPack. 
さらに、ItemKNNとPopularityの2つのアルゴリズムは、LensKitとRecPackの2つの異なるライブラリを使用して実装されています。 

This duplication allows us to verify the accuracy of results, as the outputs of these implementations should ideally produce comparable performance. 
この重複により、これらの実装の出力が理想的には比較可能な性能を生み出すべきであるため、結果の正確性を検証することができます。 

It also provides an opportunity to explore subtle performance differences between the same algorithms deployed from different libraries. 
また、異なるライブラリから展開された同じアルゴリズム間の微妙な性能差を探る機会も提供します。 

Moreover, the Bias algorithm is excluded from experiments on the Gowalla dataset due to the implicit feedback nature of the data set, as this algorithm requires explicit ratings to operate effectively. 
さらに、Biasアルゴリズムは、明示的な評価が必要なため、データセットの暗黙的フィードバックの性質により、Gowallaデータセットでの実験から除外されています。 

3.3
Random
ItemKNN
Popularity
Bias
Gowalla

To evaluate performance, we employ the normalized Discounted Cumulative Gain at rank 10 (nDCG@10), which measures the quality of top 10 ranking predictions[59]. 
パフォーマンスを評価するために、私たちは、上位10のランキング予測の質を測定する正規化割引累積利得（nDCG@10）を使用します[59]。 

We ensure consistent calculation logic across all libraries to facilitate a fair comparison of algorithm results[47]. 
すべてのライブラリで一貫した計算ロジックを確保し、アルゴリズム結果の公正な比較を促進します[47]。 

While achieving the highest possible performance for each algorithm is not the primary focus of this thesis, we performed limited grid search hyperparameter tuning to optimize key parameters[5,8]. 
各アルゴリズムの最高のパフォーマンスを達成することはこの論文の主な焦点ではありませんが、重要なパラメータを最適化するために限られたグリッドサーチハイパーパラメータチューニングを実施しました[5,8]。 

Furthermore, to enhance the reliability of results, all experiments were repeated five times using different random seed values (21, 42, 63, 84, and 105), and the final results represent the average performance across these repetitions. 
さらに、結果の信頼性を高めるために、すべての実験は異なるランダムシード値（21、42、63、84、105）を使用して5回繰り返され、最終結果はこれらの繰り返しにわたる平均パフォーマンスを示します。 

Table 3.3:
Algorithms User KNN Item KNN Popular Random Bias Funk SVD Biased MF Neu MF Popularity Item KNN SVD NMF Library LensKit LensKit LensKit LensKit LensKit LensKit LensKit RecBole RecPack RecPack RecPack RecPack

Algorithms
User KNN
Item KNN
Popular
Random
Bias
Funk SVD
Biased MF
Neu MF
Popularity
Item KNN
SVD
NMF

Library
LensKit
LensKit
LensKit
LensKit
LensKit
LensKit
LensKit
RecBole
RecPack
RecPack
RecPack
RecPack



### 3.3 データ分割とダウンサンプリング戦略

In all experiments conducted in this thesis, the dataset is split into three subsets: 80% of the total interactions are allocated to the training set, 10% to the validation set, and 10% to the test set. 
この論文で行ったすべての実験では、データセットは3つのサブセットに分割されます：全体のインタラクションの80%がトレーニングセットに、10%がバリデーションセットに、10%がテストセットに割り当てられます。

The validation set is utilized for hyperparameter tuning, while the test set is used for performance evaluation. 
バリデーションセットはハイパーパラメータの調整に使用され、テストセットは性能評価に使用されます。

The training set is further downsampled into various portions, ranging from 10% to 100% (e.g., 10%, 20%, 30%, and so on, up to 100%). 
トレーニングセットはさらに、10%から100%のさまざまな部分にダウンサンプリングされます（例：10%、20%、30%、など、100%まで）。

Importantly, the sizes of the validation and test sets remain constant across all downsampling levels. 
重要なことに、バリデーションセットとテストセットのサイズは、すべてのダウンサンプリングレベルで一定のままです。

For clarity, the downsampling percentages (e.g., 10%, 20%, etc.) refer to the proportion of the original training set that is retained after downsampling. 
明確にするために、ダウンサンプリングのパーセンテージ（例：10%、20%など）は、ダウンサンプリング後に保持される元のトレーニングセットの割合を指します。

For instance, 10% downsampling corresponds to 10% of the 80% interactions initially allocated to the training set, whereas 100% downsampling corresponds to using the entire training set. 
例えば、10%のダウンサンプリングは、最初にトレーニングセットに割り当てられた80%のインタラクションの10%に相当し、100%のダウンサンプリングはトレーニングセット全体を使用することに相当します。

In this thesis, we consistently refer to downsampling in terms of the training set. 
この論文では、ダウンサンプリングをトレーニングセットの観点から一貫して言及します。

While the exact phrase “n% of the training set” may not always be explicitly stated in later chapters for simplicity, it should be understood in this context. 
「n%のトレーニングセット」という正確なフレーズは、後の章で簡潔さのために常に明示的に述べられるわけではありませんが、この文脈で理解されるべきです。

We employed two distinct downsampling strategies in our experiments[38], referred to as User-Based and User-Subset. 
私たちは、実験で2つの異なるダウンサンプリング戦略を採用しました[38]。これらはUser-BasedとUser-Subsetと呼ばれます。

User-Based
User-Subset
User-Based Downsampling:
In this approach, interactions for each user are randomly divided into the three subsets: training set, validation set, and test set, based on the specified proportions. 
User-Basedダウンサンプリング：このアプローチでは、各ユーザーのインタラクションが指定された割合に基づいて、トレーニングセット、バリデーションセット、テストセットの3つのサブセットにランダムに分割されます。

For example, 10% of each user’s interactions are assigned to the test set, 10% to the validation set, and the remaining interactions to the training set. 
例えば、各ユーザーのインタラクションの10%がテストセットに、10%がバリデーションセットに、残りのインタラクションがトレーニングセットに割り当てられます。

User-Based Downsampling
When downsampling, a specific fraction of each user’s training interactions is randomly selected to create the downsampled training set. 
User-Basedダウンサンプリング：ダウンサンプリングを行う際、各ユーザーのトレーニングインタラクションの特定の割合がランダムに選択され、ダウンサンプリングされたトレーニングセットが作成されます。

For example, in a 50% downsampling scenario, half of the remaining interactions of each user (excluding those assigned to the validation and test sets) are included in the downsampled training set. 
例えば、50%のダウンサンプリングシナリオでは、各ユーザーの残りのインタラクションの半分（バリデーションセットとテストセットに割り当てられたものを除く）がダウンサンプリングされたトレーニングセットに含まれます。

This approach ensures that all users involved in the original dataset (after preprocessing) remain represented in every subset of training, validation, and test set across all downsampling levels, which is a key factor distinguishing this downsampling strategy from the second approach. 
このアプローチは、元のデータセット（前処理後）に関与するすべてのユーザーが、すべてのダウンサンプリングレベルでトレーニング、バリデーション、テストセットの各サブセットに表現されることを保証します。これは、このダウンサンプリング戦略を2番目のアプローチと区別する重要な要素です。

User-Subset Downsampling:
In the second downsampling strategy, we downsample the dataset by selecting a random subset of users for each downsampling step (i.e., at higher downsampling levels, a larger portion of users is included). 
User-Subsetダウンサンプリング：2番目のダウンサンプリング戦略では、各ダウンサンプリングステップでランダムなユーザーのサブセットを選択することによってデータセットをダウンサンプリングします（つまり、より高いダウンサンプリングレベルでは、より多くのユーザーが含まれます）。

The interactions of these selected users are split such that 10% of the total interactions in the original dataset (after preprocessing) are allocated to the validation set, 10% to the test set, and the remaining interactions of the selected users are assigned to the training set. 
これらの選択されたユーザーのインタラクションは、元のデータセット（前処理後）の総インタラクションの10%がバリデーションセットに、10%がテストセットに、残りのインタラクションが選択されたユーザーのトレーニングセットに割り当てられるように分割されます。

User-Subset Downsampling
To ensure the validation and test sets maintain a fixed number of interactions across all downsampling levels, the proportion of each user’s interactions allocated to these sets decreases as more users are included at higher downsampling portions. 
User-Subsetダウンサンプリング：バリデーションセットとテストセットがすべてのダウンサンプリングレベルで一定のインタラクション数を維持するために、これらのセットに割り当てられる各ユーザーのインタラクションの割合は、より多くのユーザーが高いダウンサンプリング部分に含まれるにつれて減少します。

Consequently, the size of the training set grows progressively, as desired, with increasing downsampling levels according to the expected portions (10%, 20%, …, 100%). 
その結果、トレーニングセットのサイズは、期待される割合（10%、20%、…、100%）に従って、ダウンサンプリングレベルが増加するにつれて徐々に増加します。

Unlike the User-Based approach, not all users from the original dataset are included in every downsampling step. 
User-Basedアプローチとは異なり、元のデータセットのすべてのユーザーがすべてのダウンサンプリングステップに含まれるわけではありません。

Instead, only a selected subset of users is included at each level. 
代わりに、各レベルで選択されたユーザーのサブセットのみが含まれます。

As a result, an increasing proportion of users contribute to the validation and test sets as the downsampling portion grows. 
その結果、ダウンサンプリング部分が増えるにつれて、バリデーションセットとテストセットに寄与するユーザーの割合が増加します。

Despite this, the retention of a fixed size for the validation and test sets in terms of the number of interactions across all downsampling portions, as well as ensuring the consistency of having the same users across the training, validation, and test sets within each downsampling step, is preserved. 
それにもかかわらず、すべてのダウンサンプリング部分にわたってインタラクションの数に関してバリデーションセットとテストセットの固定サイズを保持し、各ダウンサンプリングステップ内でトレーニング、バリデーション、テストセットに同じユーザーが存在することを保証することが維持されます。

Unlike the previous, more commonly used method, this setup enables an analysis of how reducing the dataset size by limiting the number of users impacts runtime, CO2e emissions, and the obtained nDCG@10 score compared to the full size of the dataset. 
以前の、より一般的に使用される方法とは異なり、この設定は、ユーザーの数を制限することによってデータセットのサイズを削減することが、ランタイム、CO2e排出量、およびデータセットのフルサイズと比較して得られたnDCG@10スコアにどのように影響するかを分析することを可能にします。

Additionally, it simulates real-world applications where an increasing number of users is continuously involved in the dataset in online systems. 
さらに、これは、オンラインシステムでデータセットに継続的に関与するユーザーの数が増加する実世界のアプリケーションをシミュレートします。

CO2e
2
nDCG@10
The codes and configurations for all experiments conducted in this study are openly accessible on GitHub[9]. 
この研究で行ったすべての実験のコードと設定は、GitHub[9]で公開されています。



## 4.Results 結果

This chapter provides a comprehensive analysis of the performance and efficiency of various recommender algorithms across multiple datasets, evaluated using two distinct downsampling approaches: User-Based and User-Subset downsampling. 
この章では、さまざまな推薦アルゴリズムの性能と効率に関する包括的な分析を提供し、2つの異なるダウンサンプリングアプローチ、すなわちUser-BasedとUser-Subsetダウンサンプリングを使用して評価します。

The main focus of this chapter is twofold: firstly, analyzing the performance of algorithms in terms of their achieved nDCG@10 scores at different downsampling portions, and secondly, examining the corresponding performance-efficiency trade-offs. 
この章の主な焦点は二つあり、第一に、異なるダウンサンプリング部分における達成されたnDCG@10スコアの観点からアルゴリズムの性能を分析し、第二に、対応する性能と効率のトレードオフを検討します。

In this context, two key terms are used repeatedly throughout the upcoming chapters: Normalized nDCG@10 score and Relative Performance. 
この文脈では、今後の章で繰り返し使用される2つの重要な用語があります：Normalized nDCG@10スコアとRelative Performanceです。

The Normalized nDCG@10 score, sometimes referred to as Normalized Performance, represents the absolute nDCG@10 scores obtained by algorithms, scaled to a range of 0 to 1 to allow fair comparisons between datasets when averaging results. 
Normalized nDCG@10スコア（時にはNormalized Performanceとも呼ばれる）は、アルゴリズムによって得られた絶対nDCG@10スコアを表し、結果を平均化する際にデータセット間で公平な比較を可能にするために0から1の範囲にスケーリングされます。

On the other hand, Relative Performance evaluates the efficiency of downsampling by expressing the performance of each algorithm in a given downsampling portion as a percentage of its performance (measured by the obtained nDCG@10 score) in the full size of the dataset (100%), which serves as the baseline. 
一方、Relative Performanceは、特定のダウンサンプリング部分における各アルゴリズムの性能を、データセットの全体サイズ（100%）における性能（得られたnDCG@10スコアで測定）に対するパーセンテージとして表現することによって、ダウンサンプリングの効率を評価します。

When the term ‘more efficient’ is used, it refers to achieving a score closer to the score obtained on the full size of the dataset. 
「より効率的」という用語が使用される場合、それはデータセットの全体サイズで得られたスコアに近いスコアを達成することを指します。

These definitions are provided to avoid ambiguity, as the terms will be used consistently throughout the following sections and chapters. 
これらの定義は、用語が今後のセクションや章で一貫して使用されるため、曖昧さを避けるために提供されています。

These investigations consider overall trends, as well as algorithm-specific and dataset-specific behaviors, discussed in subsequent sections. 
これらの調査は、全体的な傾向だけでなく、次のセクションで議論されるアルゴリズム特有およびデータセット特有の挙動を考慮します。

The chapter begins with an overview of overall performance trends, highlighting the general behaviors and performance averages of algorithms across all datasets. 
この章は、全体的な性能傾向の概要から始まり、すべてのデータセットにおけるアルゴリズムの一般的な挙動と性能の平均を強調します。

As part of this analysis, a supplementary section delves into the effects of 10-core and 30-core pruning, offering additional insights into the impact of different core pruning levels on algorithm performance. 
この分析の一環として、補足セクションでは10コアおよび30コアのプルーニングの影響を掘り下げ、異なるコアプルーニングレベルがアルゴリズムの性能に与える影響についての追加の洞察を提供します。

Subsequently, a deeper analysis is conducted, focusing on algorithm-specific and dataset-specific behaviors to provide a more granular understanding of performance variations. 
その後、アルゴリズム特有およびデータセット特有の挙動に焦点を当てたより深い分析が行われ、性能の変動に関するより詳細な理解を提供します。

This analysis highlights the influence of algorithmic and dataset characteristics on the observed trends and uncovers patterns of similar behavior across algorithms and datasets. 
この分析は、観察された傾向に対するアルゴリズムおよびデータセットの特性の影響を強調し、アルゴリズムとデータセット間での類似の挙動のパターンを明らかにします。

Finally, the chapter explores runtime efficiency and the associated reductions in carbon emissions and energy consumption achieved through downsampling. 
最後に、この章ではランタイム効率と、ダウンサンプリングによって達成された炭素排出量とエネルギー消費の削減について探ります。

This section provides valuable insights into the sustainability implications of the examined downsampling approaches, further emphasizing the trade-offs between performance and efficiency. 
このセクションは、検討されたダウンサンプリングアプローチの持続可能性の影響に関する貴重な洞察を提供し、性能と効率の間のトレードオフをさらに強調します。

Unless explicitly stated in the supplementary section on core pruning, all results presented in this chapter are based on the 10-core pruned versions of the datasets. 
コアプルーニングに関する補足セクションで明示的に述べられていない限り、この章で提示されるすべての結果は、データセットの10コアプルーニングバージョンに基づいています。



### 4.1 全体的なパフォーマンストレンド

To understand the behavior of recommender algorithms under different downsampling scenarios, we first analyze their normalized nDCG@10 performance averaged across all datasets. 
異なるダウンサンプリングシナリオにおけるレコメンダーアルゴリズムの挙動を理解するために、まずすべてのデータセットにわたる平均化された正規化nDCG@10パフォーマンスを分析します。

Figure 4.1 illustrates the normalized and averaged performance trends for the User-Based and User-Subset approaches. 
図4.1は、User-BasedアプローチとUser-Subsetアプローチの正規化された平均パフォーマンストレンドを示しています。

The normalized scores of each algorithm are averaged across datasets to capture how performance evolves as the training set size increases, up to the full dataset size (100%). 
各アルゴリズムの正規化スコアはデータセット全体で平均化され、トレーニングセットのサイズが増加するにつれてパフォーマンスがどのように進化するかを捉えます。これは、完全なデータセットサイズ（100%）までの範囲です。

In Figure 4.1 (User-Based), we observe that the normalized nDCG@10 scores for all examined cases steadily increase as the downsampling portion grows. 
図4.1（User-Based）では、調査したすべてのケースにおける正規化nDCG@10スコアが、ダウンサンプリングの割合が増加するにつれて着実に増加することが観察されます。

For example, at 30%, 50%, and 70% of the training set, the average normalized score for the SVD algorithm rises from 0.27 to 0.43 and 0.58, respectively, demonstrating a clear upward trend. 
例えば、トレーニングセットの30%、50%、70%において、SVDアルゴリズムの平均正規化スコアはそれぞれ0.27から0.43、0.58に上昇し、明確な上昇傾向を示しています。

In contrast, results obtained using User-Subset approach reveals a more varied pattern across different groups of algorithms. 
対照的に、User-Subsetアプローチを使用して得られた結果は、異なるアルゴリズムグループ間でより多様なパターンを示しています。

For instance, while the SVD algorithm shows a slight upward trend, with average normalized nDCG@10 scores of 0.73, 0.77, and 0.78 at the same training set portions (30%, 50%, and 70%), and appears to reach a saturation point around the 50%, the Popular (LensKit) algorithm exhibits a declining trend, achieving normalized scores of 0.28, 0.24, and 0.22, respectively. 
例えば、SVDアルゴリズムは同じトレーニングセットの割合（30%、50%、70%）で平均正規化nDCG@10スコアがそれぞれ0.73、0.77、0.78とわずかな上昇傾向を示し、50%付近で飽和点に達するように見える一方で、Popular (LensKit)アルゴリズムは下降傾向を示し、それぞれ0.28、0.24、0.22の正規化スコアを達成します。

This divergence highlights differences in algorithm behavior under both downsampling approaches, which will be explored in greater detail in the following sections. 
この乖離は、両方のダウンサンプリングアプローチにおけるアルゴリズムの挙動の違いを強調しており、次のセクションでより詳細に探求されます。

While figures 4.1 focus on normalized algorithm performance, the next step evaluates relative performance efficiency compared to full-size training data. 
図4.1が正規化されたアルゴリズムのパフォーマンスに焦点を当てているのに対し、次のステップではフルサイズのトレーニングデータと比較した相対的なパフォーマンス効率を評価します。

Figure 4.2 presents the averaged relative performance of all algorithms across datasets at each downsampling portion, expressed as a percentage of full dataset performance. 
図4.2は、各ダウンサンプリング部分におけるすべてのアルゴリズムの平均相対パフォーマンスをデータセット全体で示し、フルデータセットパフォーマンスのパーセンテージとして表現しています。

This analysis offers insights into the efficiency trade-offs between the User-Based and User-Subset approaches. 
この分析は、User-BasedアプローチとUser-Subsetアプローチ間の効率的なトレードオフに関する洞察を提供します。

Specifically, relative performance percentages highlight each downsampling method’s ability (not directly comparable between methods) to retain effectiveness as training data is reduced. 
具体的には、相対パフォーマンスのパーセンテージは、トレーニングデータが減少するにつれて各ダウンサンプリング手法の効果を保持する能力（手法間で直接比較できない）を強調します。

At 10% of the training set, the User-Based approach achieves an average of ∼39% of its full dataset performance, while the User-Subset approach records ∼112%. 
トレーニングセットの10%において、User-Basedアプローチはそのフルデータセットパフォーマンスの平均約39%を達成し、一方でUser-Subsetアプローチは約112%を記録します。

For the User-Subset approach, values at this portion range from ∼54% to ∼193% depending on algorithm and dataset, highlighting variations influenced by specific configurations. 
User-Subsetアプローチにおいて、この部分の値はアルゴリズムとデータセットに応じて約54%から約193%の範囲で変動し、特定の構成によって影響を受ける変動を強調しています。

This suggests that certain algorithms can retain performance very effectively under the User-Subset method, especially with minimal training data, as discussed in greater detail later. 
これは、特定のアルゴリズムがUser-Subsetメソッドの下で非常に効果的にパフォーマンスを保持できることを示唆しており、特に最小限のトレーニングデータである場合において、後でより詳細に議論されます。

Similarly, at 50% of the training set, the User-Based approach achieves ∼64% of its full dataset performance, while the User-Subset approach achieves ∼110%. 
同様に、トレーニングセットの50%において、User-Basedアプローチはそのフルデータセットパフォーマンスの約64%を達成し、一方でUser-Subsetアプローチは約110%を達成します。

These findings indicate that the behavior of algorithms varies with the strategy and focus used to reduce training data, with the User-Subset approach exhibiting strong retention and, in some cases, performance in terms of nDCG@10 scores exceeding full-dataset levels at lower portions, while the User-Based approach shows an expected steady improvement as the amount of training data increases. 
これらの発見は、アルゴリズムの挙動がトレーニングデータを減少させるために使用される戦略と焦点によって異なることを示しており、User-Subsetアプローチは強い保持を示し、場合によってはnDCG@10スコアのパフォーマンスが低い部分でフルデータセットレベルを超える一方で、User-Basedアプローチはトレーニングデータの量が増加するにつれて予想される安定した改善を示します。

The underlying potential reasons for this different behavior between the two approaches will be discussed in the Discussion and Interpretation chapter. 
この2つのアプローチ間の異なる挙動の根本的な理由は、Discussion and Interpretation章で議論されます。



#### Supplementary Analysis: 10-Core vs. 30-Core Pruning 補足分析：10コアと30コアのプルーニング

This supplementary analysis explores the impact of core pruning levels on algorithm performance under both the User-Based and User-Subset downsampling approaches. 
この補足分析では、ユーザーベースおよびユーザサブセットのダウンサンプリングアプローチにおけるコアプルーニングレベルがアルゴリズムのパフォーマンスに与える影響を探ります。

Specifically, we analyze two aspects: (1) the averaged and normalized nDCG@10 scores across all algorithms and datasets and (2) the averaged relative performance (as a percentage of the nDCG@10 score obtained at full size) to assess the efficiency of each pruning level. 
具体的には、(1) すべてのアルゴリズムとデータセットにわたる平均化された正規化nDCG@10スコアと、(2) 各プルーニングレベルの効率を評価するために、フルサイズで得られたnDCG@10スコアのパーセンテージとしての平均相対パフォーマンスを分析します。

It is important to note that this comparison is based on the four datasets (MovieLens 100K, MovieLens 1M, MovieLens 10M, and Gowalla) that support both 10-core and 30-core pruning, ensuring consistency in evaluation. 
この比較は、10コアと30コアのプルーニングの両方をサポートする4つのデータセット（MovieLens 100K、MovieLens 1M、MovieLens 10M、Gowalla）に基づいていることに注意することが重要であり、評価の一貫性を確保しています。

Figure 4.3 presents the averaged and normalized nDCG@10 scores across all datasets and algorithms at each downsampling portion for the 10-core and 30-core pruning levels under the User-Based and User-Subset approaches. 
図4.3は、ユーザーベースおよびユーザサブセットアプローチにおける10コアおよび30コアのプルーニングレベルの各ダウンサンプリング部分における、すべてのデータセットとアルゴリズムにわたる平均化された正規化nDCG@10スコアを示しています。

In the User-Based approach (Figure 4.3), the results reveal that the 30-core pruning consistently outperforms 10-core pruning in all portions of the training set. 
ユーザーベースアプローチ（図4.3）では、結果は30コアのプルーニングがトレーニングセットのすべての部分で10コアのプルーニングを一貫して上回ることを示しています。

For instance, at 30% of the training set, the averaged and normalized nDCG@10 score for 10-core pruning is approximately 0.2424, while the 30-core pruning achieves a slightly higher score of 0.2490, reflecting a relative improvement of about 2.7%. 
例えば、トレーニングセットの30%で、10コアのプルーニングの平均化された正規化nDCG@10スコアは約0.2424であり、30コアのプルーニングはわずかに高い0.2490のスコアを達成し、約2.7%の相対的改善を反映しています。

At 70%, the scores rise to 0.3876 and 0.3938 for the 10-core and 30-core pruning levels, respectively, demonstrating an improvement of ∼1.6% in this case. 
70%では、10コアと30コアのプルーニングレベルのスコアはそれぞれ0.3876と0.3938に上昇し、この場合の改善は∼1.6%を示しています。

A similar trend is observed in the User-Subset approach. 
ユーザサブセットアプローチでも同様の傾向が見られます。

At 30% of the training set, the averaged and normalized nDCG@10 score for 10-core pruning is around 0.5297, compared to 0.5750 for the 30-core pruning, showing a relative improvement of 8.5%. 
トレーニングセットの30%で、10コアのプルーニングの平均化された正規化nDCG@10スコアは約0.5297であり、30コアのプルーニングは0.5750で、8.5%の相対的改善を示しています。

At 70%, the normalized scores increase to 0.4752 and 0.4868 for the 10-core and 30-core pruning levels, respectively, further supporting the advantage of 30-core pruning in this approach. 
70%では、正規化スコアはそれぞれ10コアと30コアのプルーニングレベルで0.4752と0.4868に増加し、このアプローチにおける30コアのプルーニングの利点をさらに支持しています。

It is important to note that the general downward trend observed for the User-Subset approach in Figure 4.3 reflects average performance across all algorithms and datasets, with the primary purpose of broadly evaluating the effect of core pruning. 
図4.3におけるユーザサブセットアプローチの一般的な下降傾向は、すべてのアルゴリズムとデータセットにわたる平均的なパフォーマンスを反映しており、コアプルーニングの効果を広く評価することを主な目的としています。

As shown in Figure 4.1 and discussed in following sections, relative performance varies significantly with algorithm complexity and dataset characteristics, highlighting unique trends in specific algorithm-dataset combinations. 
図4.1に示され、次のセクションで議論されるように、相対的なパフォーマンスはアルゴリズムの複雑さやデータセットの特性によって大きく異なり、特定のアルゴリズム-データセットの組み合わせにおける独自の傾向を浮き彫りにしています。

These results suggest that denser interaction networks in 30-core datasets provide richer training data, leading to consistently higher performance (nDCG@10 scores) under both downsampling methods. 
これらの結果は、30コアデータセットにおけるより密な相互作用ネットワークがより豊富なトレーニングデータを提供し、両方のダウンサンプリング手法において一貫して高いパフォーマンス（nDCG@10スコア）をもたらすことを示唆しています。

This observation aligns with findings by Beel et al. [13], which will be further discussed in the Discussion and Interpretation chapter. 
この観察は、Beelらの発見[13]と一致しており、議論と解釈の章でさらに議論される予定です。

Building on this analysis, Figure 4.4 delves deeper into the efficiency of each pruning level, comparing the averaged relative performance (as a percentage of full-size performance) under both the User-Based and User-Subset approaches. 
この分析を基に、図4.4は各プルーニングレベルの効率をさらに深く掘り下げ、ユーザーベースおよびユーザサブセットアプローチの下での平均相対パフォーマンス（フルサイズパフォーマンスのパーセンテージとして）を比較します。

In the User-Based method (Figure 4.4), the 10-core pruning is slightly more efficient than the 30-core pruning (i.e., the obtained nDCG@10 scores at downsampled portions are closer to the score obtained at 100% of the dataset). 
ユーザーベース手法（図4.4）では、10コアのプルーニングが30コアのプルーニングよりもわずかに効率的です（すなわち、ダウンサンプリングされた部分で得られたnDCG@10スコアがデータセットの100%で得られたスコアに近い）。

For example, at 30% of the training set, the averaged relative performance for 10-core pruning is around 52%, compared to ∼50% for the 30-core pruning. 
例えば、トレーニングセットの30%で、10コアのプルーニングの平均相対パフォーマンスは約52%であり、30コアのプルーニングは∼50%です。

This trend persists across all downsampling portions, indicating that, despite achieving slightly lower normalized nDCG@10 scores, on average, algorithms sacrifice slightly less performance relative to their full training set size under 10-core pruning compared to 30-core pruning, demonstrating slightly greater efficiency for our data reduction purposes. 
この傾向はすべてのダウンサンプリング部分にわたって持続し、わずかに低い正規化nDCG@10スコアを達成しているにもかかわらず、平均してアルゴリズムは30コアのプルーニングと比較して10コアのプルーニングの下でフルトレーニングセットサイズに対してわずかに少ないパフォーマンスを犠牲にしていることを示しており、データ削減の目的に対してわずかに大きな効率を示しています。

Conversely, the User-Subset plot in Figure 4.4 shows a different trend, where 30-core pruning demonstrates superior efficiency. 
一方、図4.4のユーザサブセットプロットは異なる傾向を示しており、30コアのプルーニングが優れた効率を示しています。

For instance, at 30% of the training set, the averaged relative performance of algorithms for 10-core pruning is approximately 129%, while 30-core pruning achieves ∼135%, both surpassing the full dataset performance (as discussed earlier). 
例えば、トレーニングセットの30%で、10コアのプルーニングのアルゴリズムの平均相対パフォーマンスは約129%であり、30コアのプルーニングは∼135%を達成し、両者ともフルデータセットのパフォーマンスを上回っています（前述の通り）。

This shift in efficiency trend can be attributed to the fact that, as shown in Figure 4.3 (User-Subset plot), the normalized nDCG@10 scores for algorithms under 30-core pruning improve more significantly at lower downsampling portions compared to higher portions, as evidenced by a notable gap between the 10-core and 30-core pruning versions at these lower portions. 
この効率傾向の変化は、図4.3（ユーザサブセットプロット）に示されているように、30コアのプルーニングの下でのアルゴリズムの正規化nDCG@10スコアが、より高い部分と比較して低いダウンサンプリング部分でより顕著に改善されることに起因しています。これは、これらの低い部分での10コアと30コアのプルーニングバージョンの間に顕著なギャップがあることからも明らかです。

This leads to a greater relative performance gain compared to their 100% training size performance, ultimately surpassing the 10-core pruned version in terms of efficiency. 
これにより、100%のトレーニングサイズパフォーマンスと比較してより大きな相対パフォーマンスの向上が得られ、最終的には効率の面で10コアプルーニングバージョンを上回ります。

Thus, in the User-Subset approach, 30-core pruning not only enhances normalized nDCG@10 scores but also achieves better efficiency in retaining relative effectiveness than 10-core pruning. 
したがって、ユーザサブセットアプローチにおいて、30コアのプルーニングは正規化nDCG@10スコアを向上させるだけでなく、10コアのプルーニングよりも相対的な効果を保持する上でより良い効率を達成します。



### 4.2 アルゴリズム特有の分析

The algorithm-specific analysis of performance and efficiency delves into the distinct behaviors of individual algorithms, highlighting patterns that emerge when grouping algorithms with similar tendencies.  
アルゴリズム特有の性能と効率の分析は、個々のアルゴリズムの異なる挙動を掘り下げ、類似の傾向を持つアルゴリズムをグループ化する際に現れるパターンを強調します。  
This analysis is based on heat map visualizations that display the normalized average nDCG@10 scores for each algorithm across different downsampling portions.  
この分析は、異なるダウンサンプリング部分にわたる各アルゴリズムの正規化された平均 nDCG@10 スコアを表示するヒートマップの視覚化に基づいています。  
These heat maps, constructed for both the User-Based and User-Subset approaches, reveal two distinct groups of algorithms, as illustrated in Figure 4.5.  
ユーザベースアプローチとユーザサブセットアプローチの両方に対して構築されたこれらのヒートマップは、図4.5に示されるように、2つの異なるアルゴリズムグループを明らかにします。  

Group 1 algorithms, comprising UserKNN, ItemKNN (LensKit), ItemKNN (RecPack), SVD, NMF, and NeuMF, distinguish themselves with significantly higher nDCG@10 scores, especially at higher downsampling portions in both approaches.  
グループ1のアルゴリズムは、UserKNN、ItemKNN (LensKit)、ItemKNN (RecPack)、SVD、NMF、およびNeuMFで構成され、特に両方のアプローチで高いダウンサンプリング部分において、著しく高い nDCG@10 スコアを示します。  
They exhibit a consistent increase in normalized nDCG@10 scores as the downsampling portion increases.  
彼らは、ダウンサンプリング部分が増加するにつれて、正規化された nDCG@10 スコアが一貫して増加することを示しています。  
This upward trend is particularly pronounced in the User-Based approach.  
この上昇傾向は、ユーザベースアプローチで特に顕著です。  
In the User-Subset approach, the trend remains, albeit with a slightly reduced gradient of improvement.  
ユーザサブセットアプローチでは、傾向は残りますが、改善の勾配はわずかに減少します。  
This behavior is visually reflected in the heat map, with a gradient transitioning from light yellow (lower scores) to dark red (higher scores) as the downsampling portion increases.  
この挙動はヒートマップに視覚的に反映されており、ダウンサンプリング部分が増加するにつれて、明るい黄色（低いスコア）から暗い赤（高いスコア）への勾配が移行します。  

Group 2 algorithms, including FunkSVD, Bias, Popular (LensKit), Popularity (RecPack), and BiasedMF, display a steadier performance pattern.  
グループ2のアルゴリズムは、FunkSVD、Bias、Popular (LensKit)、Popularity (RecPack)、およびBiasedMFを含み、より安定した性能パターンを示します。  
In the User-Based approach, their normalized scores show only a slight upward trend, shifting from light yellow to a slightly darker yellow as the downsampling portions increase.  
ユーザベースアプローチでは、彼らの正規化スコアはわずかな上昇傾向を示し、ダウンサンプリング部分が増加するにつれて明るい黄色からやや暗い黄色に移行します。  
However, in the User-Subset approach, their performance slightly declines, transitioning from darker yellow at smaller portions to lighter yellow at larger portions.  
しかし、ユーザサブセットアプローチでは、彼らの性能はわずかに低下し、小さな部分では暗い黄色から大きな部分では明るい黄色に移行します。  
These results suggest that Group 2 algorithms, typically simpler models, not only achieve lower performance in terms of nDCG@10 scores compared to Group 1 but also respond differently to variations in downsampling approaches.  
これらの結果は、グループ2のアルゴリズムが通常はより単純なモデルであり、グループ1と比較して nDCG@10 スコアの点で低い性能を達成するだけでなく、ダウンサンプリングアプローチの変動に対して異なる反応を示すことを示唆しています。  

The patterns observed in these heat maps align closely with those in the overall trends section, where normalized performance was represented by linear graphs.  
これらのヒートマップで観察されたパターンは、正規化された性能が線形グラフで表されている全体的な傾向のセクションと密接に一致しています。  
The similarity in behavior within each group underscores the feasibility of analyzing efficiency and performance trends by treating algorithms with similar characteristics as representative groups.  
各グループ内の挙動の類似性は、類似の特性を持つアルゴリズムを代表的なグループとして扱うことによって、効率と性能の傾向を分析することの実現可能性を強調しています。  
This approach simplifies the analysis without sacrificing depth, allowing a focus on broader patterns rather than individual algorithm nuances.  
このアプローチは、深さを犠牲にすることなく分析を簡素化し、個々のアルゴリズムのニュアンスではなく、より広範なパターンに焦点を当てることを可能にします。  

To further explore efficiency, the analysis evaluates the average relative performance of each algorithm compared to its performance at the full dataset size across all datasets, grouping algorithms into Group 1 and Group 2.  
効率をさらに探求するために、分析は、すべてのデータセットにわたるフルデータセットサイズでの性能と比較して、各アルゴリズムの平均相対性能を評価し、アルゴリズムをグループ1とグループ2に分類します。  
Figure 4.6 visualizes this through line graphs with confidence bands for both downsampling approaches.  
図4.6は、両方のダウンサンプリングアプローチに対して信頼区間を持つ線グラフを通じてこれを視覚化します。  
Preliminary observations suggest that in the User-Based approach, both groups show an upward trend as the training set size increases.  
初期の観察結果は、ユーザベースアプローチにおいて、両グループがトレーニングセットサイズが増加するにつれて上昇傾向を示すことを示唆しています。  
For instance, Group 1 algorithms begin at approximately 15% of their full-size performance when using 10% of the training set and steadily climb to ∼76% at 80%.  
例えば、グループ1のアルゴリズムは、トレーニングセットの10%を使用する際に、フルサイズ性能の約15%から始まり、80%で∼76%に安定して上昇します。  
Group 2 algorithms, while starting from a higher baseline of ∼68%, exhibit more gradual improvements, reaching around 91% at 80% training set size.  
グループ2のアルゴリズムは、∼68%という高いベースラインから始まりますが、より緩やかな改善を示し、80%のトレーニングセットサイズで約91%に達します。  
This indicates that, under the User-Based approach, increasing the training data volume for a fixed set of users across all portions allows algorithms in both groups to approach their full dataset baseline performance.  
これは、ユーザベースアプローチの下で、すべての部分にわたって固定されたユーザセットのためにトレーニングデータのボリュームを増加させることで、両グループのアルゴリズムがフルデータセットのベースライン性能に近づくことを可能にすることを示しています。  

However, in the User-Subset approach, a divergence arises: while Group 1 algorithms maintain a similar upward trend, Group 2 algorithms behave differently, performing better at lower downsampled portions compared to larger ones.  
しかし、ユーザサブセットアプローチでは、分岐が生じます：グループ1のアルゴリズムが同様の上昇傾向を維持する一方で、グループ2のアルゴリズムは異なる挙動を示し、大きな部分と比較して小さなダウンサンプリング部分でより良い性能を発揮します。  
For example, Group 2 algorithms achieve around 164% relative performance at 10% training set size but drop to approximately 105% at 80%.  
例えば、グループ2のアルゴリズムは、トレーニングセットサイズの10%で約164%の相対性能を達成しますが、80%では約105%に低下します。  
The relative efficiency of algorithms is evident in the placement of lines in these charts.  
アルゴリズムの相対効率は、これらのチャートにおける線の配置に明らかです。  
A higher position at a specific downsampling portion signifies that less performance is sacrificed compared to the full dataset size score as the dataset is reduced.  
特定のダウンサンプリング部分での高い位置は、データセットが減少するにつれてフルデータセットサイズスコアと比較して、性能があまり犠牲にされていないことを示します。  
In this context, Group 2 algorithms (generally simpler, more basic models) demonstrate higher efficiency at downsampled portions in both approaches, retaining more of their performance when trained on smaller subsets.  
この文脈において、グループ2のアルゴリズム（一般的により単純で基本的なモデル）は、両方のアプローチでダウンサンプリング部分においてより高い効率を示し、小さなサブセットでトレーニングされたときにより多くの性能を保持します。  
Although this group of algorithms achieves lower absolute nDCG@10 scores than Group 1, they exhibit greater potential for energy efficiency performance trade-offs, achieving ∼81% of their full-size performance with only 50% of the training set in the User-Based approach and ∼123% in the User-Subset approach.  
このアルゴリズムグループはグループ1よりも低い絶対 nDCG@10 スコアを達成しますが、エネルギー効率の性能トレードオフの可能性が高く、ユーザベースアプローチではトレーニングセットの50%でフルサイズ性能の∼81%を達成し、ユーザサブセットアプローチでは∼123%を達成します。  



### 4.3 Dataset-Specific Analysis データセット特有の分析

In this section, we shift the focus from algorithms to datasets to examine how the characteristics of the dataset influence the performance and efficiency of recommender system algorithms under varying levels of downsampling. 
このセクションでは、アルゴリズムからデータセットに焦点を移し、データセットの特性が異なるダウンサンプリングレベルにおけるレコメンダーシステムアルゴリズムの性能と効率にどのように影響するかを検討します。

This analysis has two main objectives: identifying common patterns among dataset groups and understanding their roles in shaping algorithm performance and efficiency. 
この分析には2つの主な目的があります：データセットグループ間の共通パターンを特定することと、アルゴリズムの性能と効率を形成する上でのそれらの役割を理解することです。

To achieve this, we generated two heat maps, one for the User-Based and another for the User-Subset downsampling methods (Figure 4.7). 
これを達成するために、ユーザーベースのダウンサンプリング手法用とユーザサブセットのダウンサンプリング手法用の2つのヒートマップを生成しました（図4.7）。

Like in the previous section, these heat maps show normalized and averaged nDCG@10 scores for all algorithms across different downsampling portions, but this time, with rows representing individual datasets instead. 
前のセクションと同様に、これらのヒートマップは異なるダウンサンプリング部分にわたるすべてのアルゴリズムの正規化された平均nDCG@10スコアを示していますが、今回は行が個々のデータセットを表しています。

The heat maps reveal that the datasets can be logically grouped as follows: 
ヒートマップは、データセットが以下のように論理的にグループ化できることを示しています：

MovieLens Group: Comprising MovieLens 100K, MovieLens 1M, and MovieLens 10M datasets. 
MovieLensグループ：MovieLens 100K、MovieLens 1M、およびMovieLens 10Mデータセットを含む。

Amazon Group: Including Amazon Toys and Games, Amazon CDs and Vinyl, and Amazon Electronics datasets. 
Amazonグループ：Amazon Toys and Games、Amazon CDs and Vinyl、およびAmazon Electronicsデータセットを含む。

Gowalla Group: Represented solely by the Gowalla dataset, as the single implicit feedback type dataset. 
Gowallaグループ：単一の暗黙的フィードバックタイプのデータセットとしてGowallaデータセットのみで構成されています。

This grouping is justified not only by the shared origins of the datasets within the same dataset collection, such as the Amazon or MovieLens collections, but also by the distinct behavioral patterns these groups exhibit in the heat maps. 
このグループ化は、AmazonやMovieLensコレクションなど、同じデータセットコレクション内のデータセットの共有された起源だけでなく、これらのグループがヒートマップで示す明確な行動パターンによっても正当化されます。

In the User-Based heat map, the MovieLens group consistently shows stronger normalized nDCG@10 scores, particularly at higher downsampling portions, represented by darker red colors. 
ユーザーベースのヒートマップでは、MovieLensグループが常により強い正規化nDCG@10スコアを示し、特に高いダウンサンプリング部分では、より濃い赤色で表されています。

In contrast, the Amazon group demonstrates lower performance, while Gowalla occupies an intermediate position between the two. 
対照的に、Amazonグループは低い性能を示し、Gowallaはその2つの間の中間的な位置を占めています。

This pattern becomes even more pronounced in the User-Subset heat map. 
このパターンは、ユーザサブセットのヒートマップではさらに顕著になります。

Here, the MovieLens datasets exhibit a reverse trend: their normalized nDCG@10 scores decrease as the downsampling portions increase, transitioning from dark red (high scores) to light red (lower scores). 
ここでは、MovieLensデータセットが逆の傾向を示します：その正規化nDCG@10スコアは、ダウンサンプリング部分が増加するにつれて減少し、濃い赤（高スコア）から薄い赤（低スコア）に移行します。

Meanwhile, Amazon datasets and Gowalla show upward trends, with Gowalla outperforming Amazon in normalized scores at higher portions. 
一方、AmazonデータセットとGowallaは上昇傾向を示し、Gowallaは高い部分での正規化スコアでAmazonを上回ります。

To delve deeper into overall relative performance, we calculated the relative efficiency of algorithms, defined as the percentage of their performance at each downsampling portion relative to their full-size performance. 
全体的な相対性能を深く掘り下げるために、各ダウンサンプリング部分におけるアルゴリズムの性能をフルサイズの性能に対する割合として定義した相対効率を計算しました。

For each dataset group, these relative values were averaged across all algorithms to represent the overall efficiency of the group. 
各データセットグループについて、これらの相対値はすべてのアルゴリズムにわたって平均化され、グループの全体的な効率を表します。

Figure 4.8 illustrates these results with confidence bands, where applicable. 
図4.8は、該当する場合に信頼区間を伴ったこれらの結果を示しています。

The Gowalla dataset, being the sole member of its group, lacks confidence bands due to the absence of variability within the group. 
Gowallaデータセットはそのグループの唯一のメンバーであるため、グループ内の変動がないため信頼区間がありません。

In the User-Based plot of Figure 4.8, the MovieLens group demonstrates slightly higher efficiency (averaged relative performance) than the Amazon and Gowalla groups up to around 40% downsampling. 
図4.8のユーザーベースのプロットでは、MovieLensグループがAmazonおよびGowallaグループよりも約40%のダウンサンプリングまでわずかに高い効率（平均相対性能）を示しています。

For instance, at 20% downsampling, the MovieLens group retains an average relative performance of ∼similar-to∼∼47%, compared to ∼similar-to∼∼44% for Amazon and ∼similar-to∼∼43% for Gowalla. 
例えば、20%のダウンサンプリングでは、MovieLensグループは平均相対性能が∼similar-to∼∼47%を維持し、Amazonは∼similar-to∼∼44%、Gowallaは∼similar-to∼∼43%です。

However, beyond this point, the Amazon and Gowalla groups become more efficient, losing less performance relative to their full-size scores. 
しかし、このポイントを超えると、AmazonおよびGowallaグループはより効率的になり、フルサイズのスコアに対して性能を失うことが少なくなります。

At 70% downsampling, Amazon and Gowalla retain ∼similar-to∼∼78% and ∼similar-to∼∼79% of their full-size performance, respectively, while MovieLens drops to ∼similar-to∼∼72%. 
70%のダウンサンプリングでは、AmazonとGowallaはそれぞれ∼similar-to∼∼78%と∼similar-to∼∼79%のフルサイズ性能を維持し、一方でMovieLensは∼similar-to∼∼72%に低下します。

Overall, from an efficiency perspective in downsampled dataset sizes which is a primary focus of this research, the differences between the examined groups of datasets in this downsampling approach are not substantial. 
全体として、この研究の主な焦点であるダウンサンプリングされたデータセットサイズにおける効率の観点から、このダウンサンプリングアプローチにおける調査されたデータセットグループ間の違いはそれほど大きくありません。

The User-Subset approach presents a different trend. 
ユーザサブセットアプローチは異なる傾向を示します。

The MovieLens group maintains the highest efficiency (average relative performance) but shows a downward trend, indicating a relative drop in performance as downsampling portions increase. 
MovieLensグループは最高の効率（平均相対性能）を維持していますが、ダウンサンプリング部分が増加するにつれて相対的な性能の低下を示す下降傾向があります。

At 20% downsampling, the MovieLens group retains ∼similar-to∼∼146% of its full-size performance, while Gowalla and Amazon retain ∼similar-to∼∼99% and ∼similar-to∼∼87%, respectively. 
20%のダウンサンプリングでは、MovieLensグループはフルサイズ性能の∼similar-to∼∼146%を維持し、GowallaとAmazonはそれぞれ∼similar-to∼∼99%と∼similar-to∼∼87%を維持します。

At 70% downsampling, the relative performance of Gowalla is closely aligned with that of Amazon, with algorithms achieving ∼similar-to∼∼102% and ∼similar-to∼∼99% of their full-size scores, respectively. 
70%のダウンサンプリングでは、Gowallaの相対性能はAmazonのそれと密接に一致し、アルゴリズムはそれぞれフルサイズスコアの∼similar-to∼∼102%と∼similar-to∼∼99%を達成します。

It is important to emphasize that the plots in Figure 4.8 reflect the average relative performance across all algorithms. 
図4.8のプロットは、すべてのアルゴリズムにわたる平均相対性能を反映していることを強調することが重要です。

For example, the upward trend observed for the Amazon group in the User-Subset plot does not imply that all algorithms follow this trend. 
例えば、ユーザサブセットプロットでAmazonグループに見られる上昇傾向は、すべてのアルゴリズムがこの傾向に従うことを意味するわけではありません。

As noted in Figure 4.6 of the Algorithm-Specific Analysis section, different algorithm groups can exhibit contradictory relative behaviors. 
アルゴリズム特有の分析セクションの図4.6で指摘されているように、異なるアルゴリズムグループは矛盾する相対的な挙動を示すことがあります。

To identify the most efficient configurations with minimal performance sacrifice during downsampling, it is essential to integrate insights from both Figure 4.6 (Algorithm-Specific Analysis) and Figure 4.8 (Dataset-Specific Analysis). 
ダウンサンプリング中に最小限の性能犠牲で最も効率的な構成を特定するためには、図4.6（アルゴリズム特有の分析）と図4.8（データセット特有の分析）の両方からの洞察を統合することが不可欠です。

This combined perspective will help to pinpoint the best combinations of algorithms and dataset groups, thereby enabling the development of energy-efficient and effective recommender systems. 
この統合された視点は、アルゴリズムとデータセットグループの最良の組み合わせを特定するのに役立ち、エネルギー効率の高い効果的なレコメンダーシステムの開発を可能にします。



### 4.4 実行効率と炭素排出削減

To further evaluate the efficiency of the two downsampling approaches used in this investigation, we analyzed their impact on runtime reduction during algorithm training and the corresponding reduction in CO2e emissions.  
この調査で使用された2つのダウンサンプリングアプローチの効率をさらに評価するために、アルゴリズムのトレーニング中の実行時間の短縮とそれに伴うCO2e排出量の削減への影響を分析しました。

We calculated the average runtime across all algorithms and all seven 10-core pruned datasets for each downsampling portion.  
各ダウンサンプリング部分について、すべてのアルゴリズムと7つの10コアプルーニングデータセット全体の平均実行時間を計算しました。

Figure 4.9 presents the average runtime percentages for both User-Based downsampling and User-Subset downsampling approaches, relative to the required runtime for the full dataset.  
図4.9は、フルデータセットに必要な実行時間に対するUser-BasedダウンサンプリングとUser-Subsetダウンサンプリングアプローチの平均実行時間の割合を示しています。

As illustrated, downsampling the training data using User-Based approach to 30%, 50%, and 70% reduces the runtime for training and evaluation phases to ∼64%, ∼73%, and ∼82% of the runtime required for the full dataset, respectively.  
示されているように、User-Basedアプローチを使用してトレーニングデータを30%、50%、および70%にダウンサンプリングすると、トレーニングおよび評価フェーズの実行時間は、それぞれフルデータセットに必要な実行時間の約64%、73%、および82%に短縮されます。

The energy required for a single execution of a recommender algorithm on a dataset is estimated to be around 0.51 kWh [58].  
データセット上でのレコメンダーアルゴリズムの単一実行に必要なエネルギーは、約0.51 kWhと推定されています[58]。

Considering that each algorithm typically undergoes 10 hyperparameter tuning configurations, and applying the global average of 481 g CO2e per kWh as a conversion factor [25], we further incorporated a scaling factor of 40 to account for additional tasks such as prototyping, debugging, reruns, and other preliminary activities [58].  
各アルゴリズムが通常10のハイパーパラメータチューニング構成を経ることを考慮し、481 g CO2e/kWhのグローバル平均を変換係数として適用し[25]、プロトタイピング、デバッグ、再実行、その他の予備活動などの追加タスクを考慮するためにスケーリング係数40をさらに組み込みました[58]。

Using these values, the potential carbon equivalent emissions savings from downsampling the training set to 30%, 50%, and 70% compared to the full dataset for training of a single algorithm on an individual dataset are calculated as follows:  
これらの値を使用して、個々のデータセット上での単一アルゴリズムのトレーニングに対して、トレーニングセットをフルデータセットと比較して30%、50%、および70%にダウンサンプリングすることによる潜在的な炭素排出削減量を以下のように計算しました：

30% downsampling:  
30%ダウンサンプリング：

$$
(4.1)
$$

50% downsampling:  
50%ダウンサンプリング：

$$
(4.2)
$$

70% downsampling:  
70%ダウンサンプリング：

$$
(4.3)
$$

Similarly, the same analysis was conducted for the User-Subset downsampling approach.  
同様に、User-Subsetダウンサンプリングアプローチについても同じ分析が行われました。

As shown, downsampling the training data to 30%, 50%, and 70% reduces the runtime for training and evaluation phases to ∼48%, ∼61%, and ∼76% of the runtime required for the full dataset, respectively.  
示されているように、トレーニングデータを30%、50%、および70%にダウンサンプリングすると、トレーニングおよび評価フェーズの実行時間は、それぞれフルデータセットに必要な実行時間の約48%、61%、および76%に短縮されます。

Using the same calculation methodology, the estimated potential carbon equivalent emissions savings for the User-Subset approach are as follows:  
同じ計算方法を使用して、User-Subsetアプローチの推定される潜在的な炭素排出削減量は以下の通りです：

30% downsampling:  
30%ダウンサンプリング：

$$
(4.4)
$$

50% downsampling:  
50%ダウンサンプリング：

$$
(4.5)
$$

70% downsampling:  
70%ダウンサンプリング：

$$
(4.6)
$$

These calculations provide an approximate assessment of the CO2e emission reductions achieved by training a single algorithm on a single dataset, derived exclusively from the runtime reductions observed associated with downsampling.  
これらの計算は、ダウンサンプリングに関連して観察された実行時間の短縮から得られた、単一のデータセット上で単一のアルゴリズムをトレーニングすることによって達成されたCO2e排出削減の概算評価を提供します。

They assumed that the same hardware was utilized for both the full and the downsampled data sets and assumed a near-linear correlation between runtime, energy consumption, and carbon emissions.  
フルデータセットとダウンサンプリングされたデータセットの両方に同じハードウェアが使用され、実行時間、エネルギー消費、および炭素排出量の間にほぼ線形の相関関係があると仮定しました。

This assumption aligns with the principles outlined by the MLCO2e Impact calculator tool [34].  
この仮定は、MLCO2e Impact計算ツール[34]によって概説された原則と一致しています。

Figure 4.9:  
図4.9：

Our analysis reveals that the User-Subset downsampling method consistently outperforms the User-Based approach in reducing the runtime during the training phase across all portions.  
私たちの分析は、User-Subsetダウンサンプリング法がすべての部分においてトレーニングフェーズ中の実行時間を短縮する点で、User-Basedアプローチを一貫して上回ることを明らかにしています。

In every point-to-point comparison of downsampling levels, the User-Subset method achieves a more significant runtime reduction.  
ダウンサンプリングレベルのすべてのポイント間比較において、User-Subsetメソッドはより大きな実行時間の短縮を達成します。

On average, across all downsampling portions from 10% to 90%, the User-Subset approach demonstrates an additional ∼16% reduction in runtime compared to the User-Based method.  
平均して、10%から90%までのすべてのダウンサンプリング部分において、User-SubsetアプローチはUser-Basedメソッドと比較して約16%の追加的な実行時間の短縮を示します。

This enhanced efficiency translates directly into equivalent improvements in energy savings and corresponding reductions in CO2e emissions.  
この向上した効率は、エネルギーの節約とそれに伴うCO2e排出量の削減に直接的な改善をもたらします。



## 5.Discussion and Interpretation 議論と解釈

Our analysis provides valuable insights into the trade-offs between dataset size reduction and algorithmic performance in the context of energy-efficient recommender systems.  
私たちの分析は、エネルギー効率の良いレコメンダーシステムの文脈におけるデータセットサイズの削減とアルゴリズムのパフォーマンスのトレードオフに関する貴重な洞察を提供します。  
One of the most striking observations is the variability in algorithm performance across different downsampling methods and datasets.  
最も顕著な観察の一つは、異なるダウンサンプリング手法とデータセット間でのアルゴリズムのパフォーマンスの変動性です。  

Regarding the User-Based downsampling method, we observe that algorithms generally exhibit an upward trend in performance with increasing downsampling portions.  
User-Basedダウンサンプリング手法に関して、アルゴリズムは一般的にダウンサンプリングの割合が増加するにつれてパフォーマンスが上昇する傾向を示します。  
This indicates that providing the models with larger training sets, while keeping the number of users fixed and consistent across all portions, consistently results in improved algorithm performance.  
これは、ユーザーの数を固定し、すべての部分で一貫性を保ちながら、モデルにより大きなトレーニングセットを提供することが、常にアルゴリズムのパフォーマンスを向上させることを示しています。  
As shown in Figure 4.6, the sensitivity to training data reduction varies significantly across algorithms.  
図4.6に示すように、トレーニングデータの削減に対する感度はアルゴリズム間で大きく異なります。  
Some algorithms experience a substantial drop in their performance, as measured by the obtained nDCG@10 scores, when compared to their full-size dataset performance.  
いくつかのアルゴリズムは、得られたnDCG@10スコアで測定した場合、フルサイズのデータセットパフォーマンスと比較してパフォーマンスが大幅に低下します。  
In contrast, other algorithms, typically more basic models that inherently have simpler patterns for recommendation, exhibit less sensitivity to training data reduction.  
対照的に、通常はより基本的なモデルで、推薦のためのパターンが本質的に単純な他のアルゴリズムは、トレーニングデータの削減に対してあまり敏感ではありません。  
These basic algorithms often achieve scores closer to their full-size performance at lower training data volumes.  
これらの基本的なアルゴリズムは、トレーニングデータのボリュームが少ない場合でも、フルサイズのパフォーマンスに近いスコアを達成することがよくあります。  
As a result, they can be identified as more efficient options for scenarios where absolute performance is not the primary priority, and computational or resource efficiency is emphasized.  
その結果、彼らは絶対的なパフォーマンスが主な優先事項でないシナリオにおいて、計算またはリソース効率が強調される場合に、より効率的な選択肢として特定できます。  

Furthermore, regarding the effect of dataset characteristics in the User-Based approach, as illustrated in Figure 4.8, sparser datasets, such as those of the Amazon collection, demonstrate greater efficiency in retaining algorithmic performance at higher levels of downsampling (portions above 40%).  
さらに、User-Basedアプローチにおけるデータセットの特性の影響については、図4.8に示すように、Amazonコレクションのようなスパースデータセットは、より高いダウンサンプリングレベル（40％以上の部分）でアルゴリズムのパフォーマンスを保持する効率が高いことを示しています。  
However, the observed differences between the datasets are not substantial, suggesting that the impact of dataset sparsity in this approach is relatively minimal compared to other factors.  
しかし、データセット間で観察された違いはそれほど大きくなく、このアプローチにおけるデータセットのスパース性の影響は他の要因と比較して比較的最小限であることを示唆しています。  

Overall, the consistent upward trend observed across all algorithms and datasets in this more commonly used downsampling method aligns with the broadly accepted principle in AI and machine learning that "more data leads to better performance."  
全体として、この一般的に使用されるダウンサンプリング手法において、すべてのアルゴリズムとデータセットで観察される一貫した上昇傾向は、「より多くのデータがより良いパフォーマンスにつながる」というAIおよび機械学習における広く受け入れられた原則と一致します。  
This trend underscores the importance of larger training data volumes for achieving optimal results in most recommendation system applications.  
この傾向は、ほとんどのレコメンデーションシステムアプリケーションで最適な結果を達成するために、より大きなトレーニングデータボリュームの重要性を強調しています。  

However, an interesting phenomenon arises with the User-Subset downsampling approach, where certain algorithms outperform their full dataset performance under specific conditions.  
しかし、特定の条件下で特定のアルゴリズムがフルデータセットのパフォーマンスを上回るUser-Subsetダウンサンプリングアプローチにおいて、興味深い現象が発生します。  
This contradictory behavior raises important questions about the underlying factors driving these differences and warrants further investigation.  
この矛盾した挙動は、これらの違いを引き起こす根本的な要因に関する重要な疑問を提起し、さらなる調査を必要とします。  

A detailed analysis of algorithm performance on individual datasets reveals distinct trends for the User-Subset approach.  
個々のデータセットにおけるアルゴリズムのパフォーマンスの詳細な分析は、User-Subsetアプローチに対する明確な傾向を明らかにします。  
Algorithms classified as poorer performing based on nDCG@10 scores (referred to as Group 2 in earlier sections) exhibit a consistent downward trend as the downsampling portion increases, irrespective of the dataset group.  
nDCG@10スコアに基づいてパフォーマンスが低いと分類されたアルゴリズム（前のセクションでGroup 2と呼ばれる）は、データセットグループに関係なく、ダウンサンプリングの割合が増加するにつれて一貫した下降傾向を示します。  
In contrast, algorithms with higher performance (Group 1) demonstrate varied behaviors.  
対照的に、パフォーマンスが高いアルゴリズム（Group 1）は、さまざまな挙動を示します。  
On Amazon and Gowalla datasets, these algorithms generally show an upward trend with increasing downsampling portions, while on MovieLens datasets, they follow a downward trend similar to Group 2 algorithms.  
AmazonおよびGowallaデータセットでは、これらのアルゴリズムは一般的にダウンサンプリングの割合が増加するにつれて上昇傾向を示しますが、MovieLensデータセットでは、Group 2アルゴリズムと同様の下降傾向を示します。  

We hypothesize that these varying trends across datasets and algorithms stem from the design of the User-Subset downsampling method, intrinsic dataset characteristics, and the nature of the algorithms themselves.  
私たちは、データセットとアルゴリズム間のこれらの異なる傾向が、User-Subsetダウンサンプリング手法の設計、内在するデータセットの特性、およびアルゴリズム自体の性質に起因していると仮定します。  
In the User-Subset approach, increasing the downsampling portion involves incorporating a larger number of users while maintaining fixed proportions of interactions (10% of the full dataset) in the validation and test sets.  
User-Subsetアプローチでは、ダウンサンプリングの割合を増加させることは、検証およびテストセットにおいて固定された割合のインタラクション（フルデータセットの10％）を維持しながら、より多くのユーザーを組み込むことを含みます。  
This setup requires progressively adjusting the train-to-test ratio for each user’s interactions as more users are added to the downsampling portion.  
この設定では、ダウンサンプリング部分により多くのユーザーが追加されるにつれて、各ユーザーのインタラクションのトレイン・テスト比率を徐々に調整する必要があります。  
To ensure that the total number of interactions in the validation and test sets remains constant across all downsampling portions, the proportion of each user’s interactions allocated to these sets is reduced as more users are included, while the training portion is increased.  
検証およびテストセットのインタラクションの総数がすべてのダウンサンプリング部分で一定に保たれるように、これらのセットに割り当てられる各ユーザーのインタラクションの割合は、より多くのユーザーが含まれるにつれて減少し、トレーニング部分は増加します。  
This design guarantees that the validation and test sets stay consistent in size, while the training set expands incrementally as more users are included.  
この設計により、検証およびテストセットのサイズが一貫して保たれ、トレーニングセットはより多くのユーザーが含まれるにつれて徐々に拡大します。  

It is important to note that this approach introduces a fundamental difference compared to the User-Based method: the composition of the validation and test sets changes with each downsampling portion as new groups of users are included.  
このアプローチは、User-Based手法と比較して根本的な違いをもたらすことに注意することが重要です：新しいユーザーグループが含まれるにつれて、検証およびテストセットの構成が各ダウンサンプリング部分で変化します。  
While the amount of data reserved for validation and test sets remains statistically constant, the dynamic composition of users introduces some variability in the test and validation sets.  
検証およびテストセットに予約されたデータの量は統計的に一定のままですが、ユーザーの動的な構成はテストおよび検証セットにいくつかの変動をもたらします。  
This variability could reflect real-world scenarios where user subsets and interactions are not static.  
この変動は、ユーザーのサブセットとインタラクションが静的でない現実のシナリオを反映している可能性があります。  
While it may contribute to variations and unexpected observed performance trends for certain algorithms, this dynamic setup also offers valuable insights into the robustness of algorithm behavior across different user populations.  
これは、特定のアルゴリズムに対する変動や予期しないパフォーマンストレンドに寄与する可能性がありますが、この動的な設定は異なるユーーポピュレーションにおけるアルゴリズムの挙動の堅牢性に関する貴重な洞察も提供します。  
In addition, it introduces factors that influence performance, which will be discussed in further detail.  
さらに、パフォーマンスに影響を与える要因を導入し、これについてはさらに詳しく議論します。  

Despite these practical limitations, the User-Subset method is evaluated in this thesis as a case study to investigate how reducing the dataset size by decreasing the number of users impacts runtime, carbon footprint reduction, and the efficiency-performance trade-off, compared to reducing interactions while keeping the number of users fixed.  
これらの実際的な制限にもかかわらず、User-Subset手法は、この論文でケーススタディとして評価され、ユーザー数を減少させることによってデータセットサイズを削減することが、ユーザー数を固定したままインタラクションを減少させることと比較して、ランタイム、カーボンフットプリントの削減、および効率とパフォーマンスのトレードオフにどのように影響するかを調査します。  
In this setup, two critical factors are likely to influence performance: the change in the number of users included in the data subsets and the change in the train/test ratio of each user’s interactions within each subset.  
この設定では、パフォーマンスに影響を与える可能性のある2つの重要な要因があります：データサブセットに含まれるユーザーの数の変化と、各サブセット内の各ユーザーのインタラクションのトレイン/テスト比率の変化です。  

To examine these factors, we conducted experiments with the UserKNN algorithm, a representative of Group 1 algorithms, which shows contrasting trends on Amazon (upward) and MovieLens (downward) datasets.  
これらの要因を調査するために、UserKNNアルゴリズムを使用した実験を行いました。これはGroup 1アルゴリズムの代表であり、Amazon（上昇）とMovieLens（下降）データセットで対照的な傾向を示します。  
Two representative datasets, MovieLens 100K and Amazon Toys and Games, were selected for further analysis.  
さらなる分析のために、2つの代表的なデータセット、MovieLens 100KとAmazon Toys and Gamesが選ばれました。  
For each dataset, we performed two sets of experiments:  
各データセットについて、2つの実験セットを実施しました：  
- Fixing the number of users while varying the train/test ratio of each user’s interactions across downsampling portions.  
- ユーザーの数を固定し、ダウンサンプリング部分全体で各ユーザーのインタラクションのトレイン/テスト比率を変化させる。  
- Fixing the train/test ratio of each user’s interactions while varying the number of users across downsampling portions.  
- 各ユーザーのインタラクションのトレイン/テスト比率を固定し、ダウンサンプリング部分全体でユーザーの数を変化させる。  

The results indicate that when the number of users is increased while keeping the train/test ratio of each user constant, the performance of UserKNN remains relatively stable, with only minor variations.  
結果は、各ユーザーのトレイン/テスト比率を一定に保ちながらユーザーの数を増加させると、UserKNNのパフォーマンスは比較的安定しており、わずかな変動しかないことを示しています。  
This suggests that merely increasing the number of users without improving the quality of their interactions (e.g., denser interactions) has a limited impact on algorithm performance in terms of the obtained absolute score.  
これは、インタラクションの質（例えば、より密なインタラクション）を改善せずに単にユーザーの数を増やすことが、得られた絶対スコアの観点からアルゴリズムのパフォーマンスに限られた影響を与えることを示唆しています。  
As an example, when the same algorithms are applied to the full-size MovieLens 10M dataset, they do not necessarily achieve significantly higher nDCG@10 scores compared to the full-size MovieLens 100K dataset, despite the former having nearly 100 times more users.  
例えば、同じアルゴリズムをフルサイズのMovieLens 10Mデータセットに適用した場合、前者がほぼ100倍のユーザーを持っているにもかかわらず、フルサイズのMovieLens 100Kデータセットと比較して、必ずしも大幅に高いnDCG@10スコアを達成するわけではありません。  
Both datasets share similar user interaction densities, leading to comparable performance and trends under the same train/test set ratios.  
両方のデータセットは類似したユーザーインタラクション密度を持ち、同じトレイン/テストセット比率の下で比較可能なパフォーマンスと傾向をもたらします。  

However, when analyzing the impact of varying each user’s train/test ratio while keeping the number of users involved fixed (Figure 5.1), we observe trends consistent with our earlier observations: a downward trend for MovieLens datasets and an upward trend for Amazon datasets.  
しかし、ユーザーの数を固定したまま各ユーザーのトレイン/テスト比率を変化させる影響を分析すると（図5.1）、私たちの以前の観察と一致する傾向が見られます：MovieLensデータセットでは下降傾向、Amazonデータセットでは上昇傾向です。  
This confirms that the variation in each user’s train/test ratio is the primary factor driving the contrasting behavior of the same group of algorithms across different datasets.  
これは、各ユーザーのトレイン/テスト比率の変動が、異なるデータセット間で同じグループのアルゴリズムの対照的な挙動を引き起こす主な要因であることを確認します。  
This variation plays a critical role in explaining the unexpected performance patterns observed for some algorithms under the User-Subset approach (where obtained nDCG@10 score exceeds that of the full dataset at lower portions of the data).  
この変動は、User-Subsetアプローチの下で観察された一部のアルゴリズムの予期しないパフォーマンスパターンを説明する上で重要な役割を果たします（得られたnDCG@10スコアがデータの低い部分でフルデータセットのスコアを上回る場合）。  
Ultimately, this factor accounts for the differences in algorithm behavior between the two downsampling approaches, emphasizing the influence of how data partitioning strategies impact performance.  
最終的に、この要因は2つのダウンサンプリングアプローチ間のアルゴリズムの挙動の違いを説明し、データのパーティショニング戦略がパフォーマンスに与える影響を強調します。  
These findings align with prior research by Rocío et al., which emphasizes the significant influence of train/test splits on both absolute nDCG@10 scores and the relative performance of algorithms.  
これらの発見は、Rocíoらの以前の研究と一致しており、絶対nDCG@10スコアとアルゴリズムの相対的なパフォーマンスの両方に対するトレイン/テスト分割の重要な影響を強調しています。  

Furthermore, the observed trends, whether upward or downward, appear to depend on both the dataset characteristics and the complexity of the algorithm.  
さらに、観察された傾向は、上昇または下降にかかわらず、データセットの特性とアルゴリズムの複雑さの両方に依存しているようです。  
Our assumption is that simpler algorithms (e.g., Popular, Bias) or those with limited pattern discovery capabilities tend to struggle as the test set ratio decreases.  
私たちの仮定は、より単純なアルゴリズム（例：Popular、Bias）やパターン発見能力が限られているアルゴリズムは、テストセット比率が減少するにつれて苦労する傾向があるということです。  
With fewer interactions available for prediction, their chances of correct predictions diminish.  
予測に利用できるインタラクションが少なくなると、正しい予測の可能性が減少します。  
These algorithms rely on straightforward patterns, such as popularity trends or biases, which do not improve significantly with a larger training set.  
これらのアルゴリズムは、人気のトレンドやバイアスなどの単純なパターンに依存しており、より大きなトレーニングセットでは大幅に改善されません。  
Consequently, the expanded training set fails to offset the challenges posed by a smaller test set, leading to a consistent downward trend across both dense (MovieLens) and sparse (Amazon) datasets.  
その結果、拡張されたトレーニングセットは小さなテストセットがもたらす課題を相殺できず、密な（MovieLens）およびスパースな（Amazon）データセットの両方で一貫した下降傾向をもたらします。  

In contrast, algorithms which are better equipped to capture complex patterns in user-item interactions (e.g., UserKNN, ItemKNN, NeuMF), exhibit dataset-dependent behaviors.  
対照的に、ユーザー-アイテムインタラクションの複雑なパターンを捉える能力が高いアルゴリズム（例：UserKNN、ItemKNN、NeuMF）は、データセット依存の挙動を示します。  
In dense datasets like MovieLens, where users have numerous interactions, these algorithms can learn sufficiently strong patterns even with smaller portions of training data.  
ユーザーが多数のインタラクションを持つ密なデータセット（例：MovieLens）では、これらのアルゴリズムは小さなトレーニングデータの部分でも十分に強いパターンを学習できます。  
However, reducing the test set ratio for each user’s interactions diminishes the opportunity to validate the learned patterns accurately.  
しかし、各ユーザーのインタラクションのテストセット比率を減少させると、学習したパターンを正確に検証する機会が減少します。  
This reduction in the test set ratio appears to have a greater negative impact on performance than the incremental benefit gained from increasing the training set ratio, resulting in the observed downward trend.  
テストセット比率の減少は、トレーニングセット比率を増加させることから得られる漸進的な利益よりもパフォーマンスに対してより大きな悪影響を与えるようで、観察された下降傾向をもたらします。  

Conversely, in sparse datasets like Amazon and Gowalla, where users generally have fewer interactions, increasing the training set ratio provides advanced algorithms with a larger pool of interactions to uncover meaningful patterns.  
逆に、ユーザーが一般的に少ないインタラクションを持つスパースデータセット（例：Amazon、Gowalla）では、トレーニングセット比率を増加させることで、高度なアルゴリズムに意味のあるパターンを発見するためのより大きなインタラクションのプールを提供します。  
The expanded training data offers a more comprehensive representation of user preferences, which outweighs the drawbacks of a smaller test set ratio, resulting in an upward performance trend.  
拡張されたトレーニングデータは、ユーザーの好みのより包括的な表現を提供し、小さなテストセット比率の欠点を上回り、上昇するパフォーマンストレンドをもたらします。  
Sparse datasets, by nature, require more training data to support effective pattern discovery, making the increased training portion especially beneficial.  
スパースデータセットは本質的に、効果的なパターン発見をサポートするためにより多くのトレーニングデータを必要とし、トレーニング部分の増加が特に有益です。  

These observations suggest that dataset characteristics play a significant role in shaping the contrasting behaviors of algorithms under different downsampling scenarios.  
これらの観察は、データセットの特性が異なるダウンサンプリングシナリオにおけるアルゴリズムの対照的な挙動を形成する上で重要な役割を果たすことを示唆しています。  
This aligns with findings by Adomavicius and Zhang, who highlighted the critical impact of data density and rating distribution on recommendation accuracy.  
これは、データ密度と評価分布が推薦精度に与える重要な影響を強調したAdomaviciusとZhangの発見と一致します。  
While these explanations offer a plausible basis for the observed trends, the precise mechanisms remain unclear.  
これらの説明は観察された傾向のためのもっともらしい基盤を提供しますが、正確なメカニズムは不明のままです。  
Further research is required to better understand the interplay between dataset properties and algorithm performance.  
データセットの特性とアルゴリズムのパフォーマンスの相互作用をよりよく理解するためには、さらなる研究が必要です。  

Based on the results and the details discussed regarding the downsampling strategies in this thesis, it is essential to emphasize that the two approaches, User-Based and User-Subset, are not directly comparable in terms of efficiency in maintaining algorithm performance.  
この論文で議論されたダウンサンプリング戦略に関する結果と詳細に基づいて、User-BasedとUser-Subsetの2つのアプローチは、アルゴリズムのパフォーマンスを維持する効率の観点から直接比較できないことを強調することが重要です。  
Their distinct configurations, focus areas, and the differing test sets they employ make a direct comparison impractical.  
それぞれの異なる構成、焦点領域、および使用するテストセットの違いにより、直接比較は実用的ではありません。  
Instead, the key aspect where they can be meaningfully compared is their impact on runtime and carbon footprint reduction.  
代わりに、彼らが意味のある比較ができる重要な側面は、ランタイムとカーボンフットプリントの削減に対する影響です。  
One of the primary motivations for introducing the User-Subset approach as an alternative to the widely used User-Based method was to analyze how reducing the dataset by decreasing the number of involved users affects runtime and carbon-equivalent reductions.  
User-Based手法の代替としてUser-Subsetアプローチを導入する主な動機の一つは、関与するユーザーの数を減少させることによってデータセットを削減することが、ランタイムとカーボン同等の削減にどのように影響するかを分析することでした。  
In this aspect, the User-Subset approach demonstrates ∼similar-to∼∼14.5% greater runtime efficiency on average across all algorithms, datasets, and downsampling portions compared to the User-Based method.  
この点において、User-Subsetアプローチは、すべてのアルゴリズム、データセット、およびダウンサンプリング部分にわたって、User-Based手法と比較して平均して∼similar-to∼∼14.5%のランタイム効率の向上を示します。  

The User-Based approach remains a widely adopted and straightforward method for downsampling and dataset splitting.  
User-Basedアプローチは、ダウンサンプリングとデータセット分割のための広く採用されている簡単な方法のままです。  
Its simplicity and intuitive setup make it the default choice in most research contexts.  
そのシンプルさと直感的な設定は、ほとんどの研究コンテキストでデフォルトの選択肢となります。  
In contrast, the User-Subset approach, as introduced in this thesis, is not commonly used in similar studies.  
対照的に、この論文で紹介されたUser-Subsetアプローチは、同様の研究では一般的に使用されていません。  
Its primary purpose here was to explore the effects of dataset reduction on runtime and carbon efficiency while maintaining the split setup defined in this thesis: allocating 10% of total interactions for validation, 10% for test, and varying portions for training set.  
ここでの主な目的は、検証のために全インタラクションの10％、テストのために10％を割り当て、トレーニングセットのために変動する部分を維持しながら、データセット削減がランタイムとカーボン効率に与える影響を探ることでした。  

Although the User-Subset approach provides valuable insights, it introduces additional complexity.  
User-Subsetアプローチは貴重な洞察を提供しますが、追加の複雑さをもたらします。  
Specifically, it requires adjusting the train/test ratio for each user’s interactions and dynamically includes different users in the validation and test sets across downsampling portions.  
具体的には、各ユーザーのインタラクションのトレイン/テスト比率を調整し、ダウンサンプリング部分全体で検証およびテストセットに異なるユーザーを動的に含める必要があります。  
Although this setup is statistically consistent with the split methodology, the variability in user interaction patterns may influence the observed algorithm performance.  
この設定は統計的に分割方法論と一貫していますが、ユーザーインタラクションパターンの変動が観察されたアルゴリズムのパフォーマンスに影響を与える可能性があります。  
These factors highlight that the User-Subset method is not without trade-offs.  
これらの要因は、User-Subset手法がトレードオフなしではないことを強調します。  

Therefore, the User-Subset approach should be regarded as a case-study method designed to explore specific trade-offs and opportunities for analysis, particularly concerning runtime and carbon efficiency, rather than as a universally superior alternative to the User-Based approach.  
したがって、User-Subsetアプローチは、特にランタイムとカーボン効率に関する特定のトレードオフと分析の機会を探るために設計されたケーススタディ手法と見なされるべきであり、User-Basedアプローチに対する普遍的に優れた代替手段としてではありません。  

Regarding the effect of pruning, the presented statistics indicate that the 30-core pruned versions of datasets generally lead to improved absolute algorithm performance.  
プルーニングの効果に関して、提示された統計は、データセットの30コアプルーニングバージョンが一般的に絶対的なアルゴリズムパフォーマンスの改善につながることを示しています。  
For the three MovieLens datasets (100K, 1M, 10M), the 30-core pruned versions, which eliminate 17% of users compared to the 10-core versions, show an average improvement of ∼similar-to∼∼5.1% and ∼similar-to∼∼8.9% in nDCG@10 scores across all algorithms and portions for the User-Based and User-Subset approaches, respectively.  
3つのMovieLensデータセット（100K、1M、10M）について、30コアプルーニングバージョンは、10コアバージョンと比較して17％のユーザーを排除し、User-BasedおよびUser-Subsetアプローチのすべてのアルゴリズムと部分でnDCG@10スコアがそれぞれ∼similar-to∼∼5.1％および∼similar-to∼∼8.9％改善されることを示しています。  
Similarly, for the Gowalla dataset, the 30-core pruning retains only users with 30 or more interactions, resulting in remarkable average score improvements of ∼similar-to∼∼205% and ∼similar-to∼∼234% in the User-Based and User-Subset approaches, respectively, despite eliminating 96% of users compared to the 10-core version.  
同様に、Gowallaデータセットでは、30コアプルーニングが30回以上のインタラクションを持つユーザーのみを保持し、10コアバージョンと比較して96％のユーザーを排除したにもかかわらず、User-BasedおよびUser-Subsetアプローチでそれぞれ∼similar-to∼∼205％および∼similar-to∼∼234％の平均スコア改善をもたらします。  

This behavior aligns with findings by Beel et al., who demonstrated that pruning datasets to exclude users with fewer interactions often leads to artificially inflated performance metrics because data points where algorithms typically underperform are removed.  
この挙動は、インタラクションが少ないユーザーを除外するためにデータセットをプルーニングすることが、アルゴリズムが通常パフォーマンスが低下するデータポイントを除去するため、しばしばパフォーマンスメトリックを人工的に膨らませることを示したBeelらの発見と一致します。  
For example, their study highlighted that in pruned versions of the MovieLens datasets, users with fewer than 20 ratings, representing 42% of the user base but contributing only 5% of the ratings, are excluded.  
例えば、彼らの研究は、MovieLensデータセットのプルーニングバージョンでは、20件未満の評価を持つユーザーが除外され、これはユーザーベースの42％を占めるが、評価の5％しか貢献していないことを強調しました。  
Algorithms tend to perform worse for these low-interaction users, with RMSE scores approximately 23% higher compared to users with more interactions.  
アルゴリズムは、これらの低インタラクションユーザーに対してパフォーマンスが低下する傾向があり、RMSEスコアはより多くのインタラクションを持つユーザーと比較して約23％高くなります。  
These results suggest that excluding sparse users simplifies the modeling task and skews performance metrics favorably, a pattern also observed in the 30-core pruned datasets analyzed in this thesis.  
これらの結果は、スパースユーザーを除外することがモデリングタスクを簡素化し、パフォーマンスメトリックを有利に歪めることを示唆しており、この論文で分析された30コアプルーニングデータセットでも同様のパターンが観察されました。  

When evaluating the ranking of algorithms, our experiments reveal only minor shifts in ranking between the 10-core and 30-core pruning versions in most cases, with differences in scores being minimal.  
アルゴリズムのランキングを評価する際、私たちの実験は、ほとんどの場合、10コアと30コアのプルーニングバージョン間でのランキングのわずかな変動しか示さず、スコアの違いは最小限です。  
However, in the heavily pruned Gowalla dataset, algorithm rankings change more noticeably, indicating that the degree of pruning can influence the relative order of algorithms.  
しかし、厳しくプルーニングされたGowallaデータセットでは、アルゴリズムのランキングがより顕著に変化し、プルーニングの程度がアルゴリズムの相対的な順序に影響を与える可能性があることを示しています。  
This observation supports the hypothesis that substantial pruning can alter how algorithms perform relative to one another.  
この観察は、相当なプルーニングがアルゴリズムの相対的なパフォーマンスを変える可能性があるという仮説を支持します。  

Interestingly, the relative performance of algorithms, compared to their full-size scores, exhibits different trends depending on the downsampling approach.  
興味深いことに、アルゴリズムの相対的なパフォーマンスは、フルサイズのスコアと比較して、ダウンサンプリングアプローチによって異なる傾向を示します。  
In the User-Based approach, algorithms trained on the 30-core pruned datasets show slightly lower averaged relative performance compared to the 10-core pruned datasets, with an average drop of around 2%.  
User-Basedアプローチでは、30コアプルーニングデータセットで訓練されたアルゴリズムは、10コアプルーニングデータセットと比較してわずかに低い平均相対パフォーマンスを示し、平均で約2％の低下があります。  
Conversely, in the User-Subset approach, the 30-core pruned datasets show an average ∼similar-to∼∼4% higher relative performance than their 10-core counterparts, highlighting an advantage in terms of energy efficiency-performance trade-offs.  
対照的に、User-Subsetアプローチでは、30コアプルーニングデータセットが10コアのデータセットよりも平均して∼similar-to∼∼4％高い相対パフォーマンスを示し、エネルギー効率とパフォーマンスのトレードオフにおける利点を強調します。  

While the primary focus of this project is not on the effects of pruning, the observed results underscore the importance of this factor and suggest that more focused and in-depth investigations into the implications of different pruning levels could provide valuable insights.  
このプロジェクトの主な焦点はプルーニングの効果ではありませんが、観察された結果はこの要因の重要性を強調し、異なるプルーニングレベルの影響に関するより焦点を絞った詳細な調査が貴重な洞察を提供できることを示唆しています。  

These findings and discussions naturally lead to addressing the central research question of this thesis:  
これらの発見と議論は、この論文の中心的な研究質問に自然に導きます：  
RQ: Is it possible to achieve an acceptable trade-off between energy efficiency and performance in recommender algorithms by reducing dataset size?  
RQ: データセットサイズを削減することによって、レコメンダーアルゴリズムにおいてエネルギー効率とパフォーマンスの間で受け入れ可能なトレードオフを達成することは可能か？  

The findings of this study indicate that data reduction through downsampling can indeed contribute to energy efficiency by significantly reducing runtime and carbon emissions.  
この研究の結果は、ダウンサンプリングによるデータ削減が、ランタイムとカーボン排出量を大幅に削減することによってエネルギー効率に寄与することができることを示しています。  
As shown in Figure 4.9, this energy savings is closely correlated with the extent of data reduction, demonstrating the potential for improved efficiency in computationally intensive tasks.  
図4.9に示すように、このエネルギーの節約はデータ削減の程度と密接に相関しており、計算集約的なタスクにおける効率の向上の可能性を示しています。  

However, the impact of data reduction on algorithm performance is highly scenario-dependent and varies with the downsampling approach.  
しかし、データ削減がアルゴリズムのパフォーマンスに与える影響は、シナリオに依存し、ダウンサンプリングアプローチによって異なります。  
For example, in the User-Based downsampling method, data reduction typically results in a predictable decline in performance, as illustrated in Figure 4.1.  
例えば、User-Basedダウンサンプリング手法では、データ削減が通常、図4.1に示すようにパフォーマンスの予測可能な低下をもたらします。  
However, the extent of this performance drop varies across different groups of algorithms; some algorithms exhibit lower sensitivity to training data reduction, making them more suitable choices when energy efficiency is the primary focus.  
しかし、このパフォーマンスの低下の程度は異なるアルゴリズムグループ間で異なり、一部のアルゴリズムはトレーニングデータの削減に対して低い感度を示し、エネルギー効率が主な焦点である場合により適した選択肢となります。  
In contrast, the User-Subset approach introduced in this thesis demonstrates that, with a flexible and distinct design setup, it is possible to achieve metric scores that are comparable to or, in some cases, better than those achieved with the full dataset (strictly in terms of the absolute scores obtained), all while significantly reducing runtime and carbon footprint.  
対照的に、この論文で紹介されたUser-Subsetアプローチは、柔軟で独自の設計設定を用いることで、フルデータセットで達成されたものと同等、または場合によってはそれを上回るメトリックスコアを達成することが可能であることを示しています（得られた絶対スコアの観点から厳密に）、すべてのランタイムとカーボンフットプリントを大幅に削減しながら。  

Ultimately, achieving a favorable trade-off between energy efficiency and performance depends on several factors: the complexity and nature of the algorithms, the characteristics of the datasets, and the specifics of the downsampling setup.  
最終的に、エネルギー効率とパフォーマンスの間で好ましいトレードオフを達成することは、アルゴリズムの複雑さと性質、データセットの特性、およびダウンサンプリング設定の詳細など、いくつかの要因に依存します。  
By carefully selecting and aligning these factors in scenarios where absolute peak performance is not the primary objective, and where flexibility in algorithm and dataset choice exists, researchers and practitioners can significantly improve energy efficiency with minimal and carefully optimized compromise to performance effectiveness.  
絶対的なピークパフォーマンスが主な目的でないシナリオで、アルゴリズムとデータセットの選択に柔軟性がある場合に、これらの要因を慎重に選択し調整することによって、研究者や実務者はパフォーマンスの効果を最小限に抑えつつ、エネルギー効率を大幅に改善することができます。  



## 6. 結論

This thesis investigates the potential of dataset downsampling as a strategy to achieve energy-efficient recommender systems while maintaining acceptable performance levels. 
本論文では、エネルギー効率の良いレコメンダーシステムを実現しつつ、許容可能なパフォーマンスレベルを維持するための戦略として、データセットのダウンサンプリングの可能性を調査します。

By evaluating the effects of downsampling across diverse algorithms, datasets, and configurations, this research provides a comprehensive assessment of the trade-offs between energy efficiency and recommendation quality. 
さまざまなアルゴリズム、データセット、および構成にわたるダウンサンプリングの効果を評価することにより、本研究はエネルギー効率と推薦品質のトレードオフに関する包括的な評価を提供します。

The results demonstrate that downsampling can effectively reduce the energy demands of recommender systems, leading to significant savings in runtime and carbon emissions. 
結果は、ダウンサンプリングがレコメンダーシステムのエネルギー需要を効果的に削減できることを示しており、実行時間と炭素排出量の大幅な節約につながります。

When considering 30% up to 70% downsampling portions, runtime reductions ranged from approximately 52% up to 18% (Figure 4.9), depending on the method and exact portion of downsampling, while carbon emissions were lowered by an estimated 17.66 up to 51.02 KgCO2e for training of a single algorithm on a single dataset. 
30%から70%のダウンサンプリング部分を考慮した場合、実行時間の削減は、方法とダウンサンプリングの正確な部分に応じて、約52%から18%までの範囲でした（図4.9）。一方、炭素排出量は、単一のアルゴリズムを単一のデータセットでトレーニングする際に、推定で17.66から51.02 KgCO2e削減されました。

These findings highlight the value of data reduction in mitigating the environmental impact of AI-driven systems, particularly in large-scale applications. 
これらの発見は、特に大規模なアプリケーションにおいて、AI駆動システムの環境への影響を軽減するためのデータ削減の価値を強調しています。

In terms of performance, the study shows that recommender systems can retain a substantial portion of their effectiveness even with reduced training datasets. 
パフォーマンスに関して、この研究は、レコメンダーシステムがトレーニングデータセットを削減しても、その効果の大部分を保持できることを示しています。

Relative performance ranged from approximately 39% to as high as approximately 115% of the full dataset scores averaged across algorithms and datasets (Figure 4.2), depending on the downsampling approach and portion used. 
相対的なパフォーマンスは、ダウンサンプリングのアプローチと使用された部分に応じて、アルゴリズムとデータセット全体のスコアの平均に対して約39%から約115%までの範囲でした（図4.2）。

This suggests that, in some cases, depending on the dataset reduction configuration and objectives, it is possible to achieve comparable or even better metric scores with smaller datasets, offering a practical pathway to optimize energy efficiency without incurring severe performance penalties. 
これは、データセットの削減構成と目的に応じて、より小さなデータセットで同等またはそれ以上のメトリックスコアを達成することが可能であることを示唆しており、エネルギー効率を最適化しながら深刻なパフォーマンスペナルティを回避する実用的な道を提供します。

The research also reveals that the effectiveness of downsampling strategies in achieving an optimal trade-off between energy efficiency and performance is influenced by the interaction of the characteristics of the data set and the algorithmic complexity (Figures 4.6 and 4.8). 
この研究は、エネルギー効率とパフォーマンスの最適なトレードオフを達成するためのダウンサンプリング戦略の効果が、データセットの特性とアルゴリズムの複雑さの相互作用によって影響を受けることも明らかにしています（図4.6および4.8）。

Sparse datasets, which inherently provide fewer interactions, typically result in lower absolute nDCG@10 scores compared to denser datasets. 
本質的に相互作用が少ないスパースデータセットは、通常、より密なデータセットと比較して、絶対的なnDCG@10スコアが低くなります。

However, they could exhibit higher efficiency in data reduction under specific configurations of downsampling approaches and targeted data reductions. 
しかし、特定のダウンサンプリングアプローチとターゲットデータ削減の構成の下では、データ削減においてより高い効率を示す可能性があります。

Similarly, simpler algorithms, while generally achieving lower overall performance compared to advanced algorithms capable of capturing intricate user-item patterns, generally demonstrated greater potential for achieving performance efficiency at reduced dataset portions due to their reduced sensitivity to training data size. 
同様に、一般的に複雑なユーザーアイテムパターンを捉えることができる高度なアルゴリズムと比較して、全体的なパフォーマンスが低いシンプルなアルゴリズムは、トレーニングデータサイズに対する感度が低いため、削減されたデータセット部分でパフォーマンス効率を達成する可能性が高いことを示しました。

Finally, based on the findings of this thesis, we address our research question and conclude that downsampling can be a viable and effective strategy for balancing energy efficiency and performance in recommender systems, although its effectiveness remains highly context-dependent. 
最後に、本論文の発見に基づいて、私たちは研究課題に取り組み、ダウンサンプリングがレコメンダーシステムにおけるエネルギー効率とパフォーマンスのバランスを取るための実行可能で効果的な戦略であると結論付けますが、その効果は非常に文脈依存であることに留意します。

Achieving a successful trade-off depends on factors such as the configuration of the downsampling approach, the characteristics of the datasets, and the complexity of the algorithms. 
成功したトレードオフを達成するには、ダウンサンプリングアプローチの構成、データセットの特性、およびアルゴリズムの複雑さなどの要因に依存します。

Although absolute peak performance may occasionally require the full dataset, this study demonstrates that, for many practical applications, careful downsampling can achieve a favorable balance. 
絶対的なピークパフォーマンスは時折フルデータセットを必要とするかもしれませんが、本研究は、多くの実用的なアプリケーションにおいて、慎重なダウンサンプリングが好ましいバランスを達成できることを示しています。

This approach not only reduces computational resource requirements but also contributes to the development of sustainable AI systems. 
このアプローチは、計算リソースの要件を削減するだけでなく、持続可能なAIシステムの開発にも寄与します。

In conclusion, this research supports the integration of downsampling techniques into the design and operation of recommender systems as a means of optimizing both performance and energy efficiency. 
結論として、この研究は、パフォーマンスとエネルギー効率の両方を最適化する手段として、レコメンダーシステムの設計と運用にダウンサンプリング技術を統合することを支持します。

By achieving meaningful reductions in resource usage with minimal impact on recommendation quality, downsampling offers a scalable and environmentally conscious solution to advance the field of recommender systems. 
リソース使用の有意な削減を達成し、推薦品質への影響を最小限に抑えることで、ダウンサンプリングはレコメンダーシステムの分野を進展させるためのスケーラブルで環境に配慮した解決策を提供します。



## 7.Summary 要約

This thesis addresses the computational and environmental challenges posed by the growing size of datasets used in recommender systems. 
この論文は、推薦システムで使用されるデータセットのサイズの増加によって引き起こされる計算上および環境上の課題に対処します。 

While larger datasets often enhance performance, they do so at the cost of increased energy consumption and carbon emissions. 
より大きなデータセットはしばしばパフォーマンスを向上させますが、それはエネルギー消費と炭素排出の増加というコストを伴います。 

The central research question investigates whether reducing dataset size can balance energy efficiency and algorithmic performance without significant or with only minimal compromises. 
中心となる研究課題は、データセットのサイズを削減することで、エネルギー効率とアルゴリズムのパフォーマンスのバランスを、重大な妥協なしに、または最小限の妥協で実現できるかどうかを調査します。 

To explore this, the study utilized seven datasets, applying two distinct downsampling strategies, User-Based and User-Subset, along with two pruning levels (10-core and 30-core). 
この探求のために、研究は7つのデータセットを利用し、2つの異なるダウンサンプリング戦略（User-BasedとUser-Subset）と2つのプルーニングレベル（10-coreと30-core）を適用しました。 

A diverse set of 12 algorithms, ranging from basic to advanced, were evaluated using nDCG@10 as the performance metric. 
基本的なものから高度なものまでの多様な12のアルゴリズムが、パフォーマンス指標としてnDCG@10を使用して評価されました。 

These configurations enabled a detailed analysis of the trade-offs between dataset size, algorithm performance, and energy efficiency, with a focus on identifying sustainable practices for recommender systems. 
これらの構成により、データセットのサイズ、アルゴリズムのパフォーマンス、およびエネルギー効率の間のトレードオフを詳細に分析でき、推薦システムの持続可能な実践を特定することに焦点を当てました。 

Key findings of the research include: 
研究の主要な発見は以下の通りです：

Overall Performance Trends: The performance of the algorithms, measured by normalized nDCG@10, consistently improved with larger training datasets in the User-Based approach. 
全体的なパフォーマンストレンド：アルゴリズムのパフォーマンスは、正規化されたnDCG@10で測定され、User-Basedアプローチにおいてより大きなトレーニングデータセットで一貫して改善されました。 

However, some algorithms displayed less sensitivity to increases in training data, suggesting they may perform relatively well even with smaller datasets. 
しかし、一部のアルゴリズムはトレーニングデータの増加に対してあまり敏感ではなく、より小さなデータセットでも比較的良好に機能する可能性があることを示唆しています。 

In contrast, the User-Subset approach showed varied behavior. 
対照的に、User-Subsetアプローチはさまざまな挙動を示しました。 

Some algorithms, particularly simpler or more basic ones, exhibited a downward trend in performance as the downsampling portion increased, yet still achieved metric scores exceeding those obtained with the full dataset at lower downsampling portions. 
特に単純なアルゴリズムは、ダウンサンプリングの割合が増加するにつれてパフォーマンスが低下する傾向を示しましたが、依然として低いダウンサンプリング割合でフルデータセットよりも高いメトリックスコアを達成しました。 

For instance, as a representative case study at 50% downsampling, the User-Based method achieved approximately 64% of its full dataset nDCG@10 score, while the User-Subset approach, utilizing a different data reduction configuration, achieved approximately 110%. 
例えば、50%のダウンサンプリングでの代表的なケーススタディとして、User-BasedメソッドはフルデータセットのnDCG@10スコアの約64%を達成しましたが、異なるデータ削減構成を利用したUser-Subsetアプローチは約110%を達成しました。 

Effect of Pruning: The analysis of pruning levels showed that 30-core pruning improved absolute performance, with gains of ∼similar-to∼5.1% to ∼similar-to∼8.9% in dense datasets (MovieLens) and up to ∼similar-to∼234% in sparse datasets (Gowalla). 
プルーニングの効果：プルーニングレベルの分析は、30-coreプルーニングが絶対的なパフォーマンスを改善し、密なデータセット（MovieLens）で∼similar-to∼5.1%から∼similar-to∼8.9%の向上を示し、疎なデータセット（Gowalla）では最大∼similar-to∼234%の向上を示しました。 

However, relative performance trends varied: 10-core pruning yielded higher efficiency under the User-Based method, while 30-core pruning excelled in the User-Subset approach. 
しかし、相対的なパフォーマンストレンドは異なりました：10-coreプルーニングはUser-Basedメソッドの下でより高い効率をもたらし、30-coreプルーニングはUser-Subsetアプローチで優れた結果を示しました。 

These results highlight the trade-offs between denser interaction networks and relative performance efficiency. 
これらの結果は、より密な相互作用ネットワークと相対的なパフォーマンス効率の間のトレードオフを強調しています。 

Algorithmic Behavior: Algorithms were categorized into two groups based on their performance trends. 
アルゴリズミックな挙動：アルゴリズムはそのパフォーマンストレンドに基づいて2つのグループに分類されました。 

Group 1 algorithms, including ItemKNN (both versions), UserKNN, NeuMF, SVD, and NMF, consistently benefited from larger training sets under both downsampling approaches, particularly under User-Based method, achieving higher nDCG@10 scores compared to the other group. 
グループ1のアルゴリズム（ItemKNN（両方のバージョン）、UserKNN、NeuMF、SVD、NMFを含む）は、両方のダウンサンプリングアプローチ、特にUser-Basedメソッドの下で、より大きなトレーニングセットから一貫して利益を得ており、他のグループと比較して高いnDCG@10スコアを達成しました。 

In contrast, Group 2 algorithms namely Popular, BiasedMF, FunkSVD, Popularity, and Bias exhibited higher relative performance under both approaches, as their nDCG@10 scores at reduced training set sizes were closer to their full-size dataset scores. 
対照的に、グループ2のアルゴリズム（Popular、BiasedMF、FunkSVD、Popularity、Bias）は、両方のアプローチでより高い相対的パフォーマンスを示しました。なぜなら、トレーニングセットサイズが減少した際のnDCG@10スコアがフルサイズのデータセットスコアに近かったからです。 

These trends underscore the varying sensitivities of algorithms to dataset size and downsampling strategies. 
これらのトレンドは、アルゴリズムがデータセットのサイズやダウンサンプリング戦略に対して異なる感受性を持つことを強調しています。 

Dataset Characteristics: Performance trends varied across the dataset groups of MovieLens, Amazon, and Gowalla. 
データセットの特性：パフォーマンストレンドは、MovieLens、Amazon、Gowallaのデータセットグループ間で異なりました。 

On average, MovieLens datasets achieved higher nDCG@10 scores and showed better relative performance (efficiency) in the User-Subset method. 
平均して、MovieLensデータセットはより高いnDCG@10スコアを達成し、User-Subsetメソッドでより良い相対的パフォーマンス（効率）を示しました。 

Conversely, Amazon and Gowalla datasets demonstrated better relative performance at higher downsampling portions (above 40%) under the User-Based approach. 
逆に、AmazonおよびGowallaデータセットは、User-Basedアプローチの下でより高いダウンサンプリング割合（40%以上）でより良い相対的パフォーマンスを示しました。 

These findings highlight the impact of characteristics of the dataset on algorithmic behavior. 
これらの発見は、データセットの特性がアルゴリズムの挙動に与える影響を強調しています。 

Environmental Benefits: Downsampling significantly reduced runtime and carbon emissions. 
環境上の利点：ダウンサンプリングは、実行時間と炭素排出を大幅に削減しました。 

For instance, at 30% downsampling, depending on the chosen downsampling approach, runtime reductions ranged from ∼similar-to∼36% to ∼similar-to∼52% compared to full-size datasets, with corresponding carbon savings of ∼similar-to∼35.32 to ∼similar-to∼51.02 KgCO2e per algorithm per dataset. 
例えば、30%のダウンサンプリングでは、選択したダウンサンプリングアプローチに応じて、実行時間の削減はフルサイズのデータセットと比較して∼similar-to∼36%から∼similar-to∼52%の範囲であり、対応する炭素削減はアルゴリズムごとにデータセットあたり∼similar-to∼35.32から∼similar-to∼51.02 KgCO2eでした。 

Notably, the User-Subset approach consistently outperformed the User-Based method in reducing runtime and energy consumption. 
特に、User-Subsetアプローチは、実行時間とエネルギー消費の削減において常にUser-Basedメソッドを上回りました。 

Impact of Downsampling Strategies: The User-Based approach, characterized by its commonly used configuration where only the interactions of the same consistent users are downsampled, provided predictable results, aligning with the traditional expectation that larger training set yield better outcomes. 
ダウンサンプリング戦略の影響：User-Basedアプローチは、同じ一貫したユーザーの相互作用のみがダウンサンプリングされる一般的に使用される構成によって特徴付けられ、予測可能な結果を提供し、より大きなトレーニングセットがより良い結果をもたらすという従来の期待に沿っています。 

In contrast, the User-Subset method revealed unexpected trends, with certain algorithms benefiting from reduced dataset sizes in terms of achieved absolute scores compared to the full dataset score. 
対照的に、User-Subsetメソッドは予期しないトレンドを明らかにし、特定のアルゴリズムがフルデータセットスコアと比較して達成された絶対スコアの点でデータセットサイズの削減から利益を得ることを示しました。 

These trends can be attributed to differences in configurations, such as variations in each user’s train/test ratios and user selection mechanisms. 
これらのトレンドは、各ユーザーのトレーニング/テスト比率やユーザー選択メカニズムの違いなど、構成の違いに起因する可能性があります。 

Overall, this thesis demonstrates the feasibility of optimizing dataset sizes to achieve sustainable AI practices. 
全体として、この論文は持続可能なAIプラクティスを達成するためにデータセットサイズを最適化することの実現可能性を示しています。 

However, the ability to achieve a favorable trade-off between energy efficiency and performance depends on multiple factors, including algorithm complexity, dataset characteristics, and downsampling configurations. 
しかし、エネルギー効率とパフォーマンスの間で好ましいトレードオフを達成する能力は、アルゴリズムの複雑さ、データセットの特性、およびダウンサンプリング構成など、複数の要因に依存します。 

The findings suggest that smaller datasets are capable of reducing runtime and carbon footprint without necessarily sacrificing performance significantly in many cases. 
この発見は、より小さなデータセットが多くのケースでパフォーマンスを大幅に犠牲にすることなく、実行時間と炭素フットプリントを削減できることを示唆しています。 

As recommender systems are increasingly used in large-scale applications, adopting such optimization strategies can have a meaningful impact on reducing the environmental footprint of AI technologies. 
推薦システムが大規模なアプリケーションでますます使用される中、こうした最適化戦略を採用することは、AI技術の環境フットプリントを削減する上で意味のある影響を与える可能性があります。 

This research contributes to the emerging field of Green Recommender Systems by offering practical guidelines to balance performance and sustainability. 
この研究は、パフォーマンスと持続可能性のバランスを取るための実用的なガイドラインを提供することによって、グリーン推薦システムの新興分野に貢献しています。



## 8.Future Work and Limitations 8. 今後の研究と限界

This research provides a comprehensive analysis of the trade-offs between energy efficiency and recommendation quality through dataset downsampling. 
本研究は、データセットのダウンサンプリングを通じて、エネルギー効率と推薦品質のトレードオフに関する包括的な分析を提供します。しかし、いくつかの限界と今後の探求の領域が残っており、これによりこの研究の適用性と影響を高めることができます。

1. Scope of Algorithms 1. アルゴリズムの範囲
While this thesis evaluates a diverse range of 12 algorithms across multiple libraries (LensKit, RecPack, and RecBole), the selection is not exhaustive. 
この論文では、複数のライブラリ（LensKit、RecPack、RecBole）にわたる12のアルゴリズムの多様な範囲を評価していますが、選択は網羅的ではありません。Most of the algorithms examined are traditional recommender systems, with NeuMF being the only deep learning model analyzed. 
調査されたアルゴリズムのほとんどは従来のレコメンダーシステムであり、NeuMFが分析された唯一の深層学習モデルです。この限られた選択は、現代の最先端モデルがダウンサンプリングにどのように反応するかに関する洞察を制限します。Future research should include more state-of-the-art deep learning algorithms, particularly those based on graph neural networks and transformer-based architectures. 
今後の研究では、特にグラフニューラルネットワークやトランスフォーマーベースのアーキテクチャに基づく、より多くの最先端の深層学習アルゴリズムを含めるべきです。Examining these advanced models would provide a deeper understanding of the impact of downsampling strategies on algorithm performance and efficiency, offering a more comprehensive evaluation of contemporary recommender systems. 
これらの高度なモデルを調査することで、アルゴリズムのパフォーマンスと効率に対するダウンサンプリング戦略の影響をより深く理解し、現代のレコメンダーシステムの包括的な評価を提供することができます。

2. Dataset Characteristics and Core Pruning 2. データセットの特性とコアプルーニング
The datasets analyzed in this study span multiple domains and levels of sparsity. 
本研究で分析されたデータセットは、複数のドメインとスパース性のレベルにわたっています。しかし、特にAmazonコレクションからの非常にスパースなデータセットは、プルーニング後の相互作用が不十分であるため、特定のプルーニング条件（例：30コアプルーニング）の下で除外されました。 
これにより、特に極端なスパース性やユニークな相互作用パターンを持つデータセットに関連するプルーニング効果に関する発見の一般化が制限されます。Future research should incorporate a broader spectrum of datasets, including highly sparse datasets from both explicit and implicit feedback types, that remain viable under different core pruning levels, to validate findings across diverse contexts. 
今後の研究では、異なるコアプルーニングレベルの下で有効な、明示的および暗黙的フィードバックタイプの両方からの非常にスパースなデータセットを含む、より広範なデータセットのスペクトルを取り入れるべきです。Additionally, while core pruning was a secondary focus in this thesis, its notable effects on algorithm rankings and performance trends suggest that dedicated investigations into varying pruning levels could yield valuable preprocessing guidelines for recommender systems. 
さらに、コアプルーニングはこの論文の二次的な焦点でしたが、アルゴリズムのランキングやパフォーマンストレンドに対する顕著な影響は、さまざまなプルーニングレベルに関する専用の調査がレコメンダーシステムのための貴重な前処理ガイドラインを生み出す可能性があることを示唆しています。

3. Downsampling Configuration and Train/Test Ratio Dynamics 3. ダウンサンプリング構成とトレイン/テスト比率のダイナミクス
The User-Subset approach introduced in this study demonstrated effectiveness but also introduced complexity due to its dynamic train/test ratio and selective user inclusion. 
本研究で導入されたユーザーサブセットアプローチは効果的であることを示しましたが、動的なトレイン/テスト比率と選択的なユーザーの包含により複雑さももたらしました。Moreover, the approach involves varying groups of users in the validation and test sets across different downsampling portions, which, while statistically consistent in maintaining fixed sizes for these sets, may influence observed performance. 
さらに、このアプローチは、異なるダウンサンプリング部分にわたって検証およびテストセット内のユーザーの異なるグループを含むため、これらのセットのサイズを固定する上で統計的に一貫しているものの、観察されたパフォーマンスに影響を与える可能性があります。この複雑さは、より単純な方法との直接的な比較を困難にし、シンプルさと標準化が好まれるシナリオでの適用性を制限する可能性があります。Future work could focus on developing more straightforward and commonly used downsampling approaches or innovative techniques that address these limitations, maintaining efficiency while offering simpler and more practical configurations. 
今後の研究では、これらの制限に対処しつつ効率を維持し、よりシンプルで実用的な構成を提供する、より単純で一般的に使用されるダウンサンプリングアプローチや革新的な技術の開発に焦点を当てることができるでしょう。Furthermore, in this study, the experiments were conducted using a fixed Train/Validation/Test split ratio of 80%-10%-10%. 
さらに、本研究では、固定されたトレイン/バリデーション/テストの分割比率80%-10%-10%を使用して実験が行われました。Exploring alternative split configurations (e.g., 60%-20%-20%), could provide further insights into the efficiency and effectiveness of different train/test ratios in downsampling scenarios. 
代替の分割構成（例：60%-20%-20%）を探ることで、ダウンサンプリングシナリオにおける異なるトレイン/テスト比率の効率と効果に関するさらなる洞察を提供できるでしょう。Moreover, further exploration is needed to understand the dynamic interaction between train/test ratios and algorithm performance across datasets. 
さらに、トレイン/テスト比率とデータセット全体のアルゴリズムパフォーマンスとの動的な相互作用を理解するためのさらなる探求が必要です。For instance, advanced algorithms exhibited improved performance on sparse datasets (e.g., Amazon, Gowalla) with increasing training portions, while the same group of algorithms showed decreased performance in dense datasets (e.g., MovieLens). 
例えば、高度なアルゴリズムは、トレーニング部分が増加するにつれてスパースなデータセット（例：Amazon、Gowalla）でパフォーマンスが向上しましたが、同じアルゴリズムのグループは密なデータセット（例：MovieLens）でパフォーマンスが低下しました。Investigating these contrasting behaviors would help optimize downsampling configurations to maximize efficiency and effectiveness for various algorithm-dataset combinations. 
これらの対照的な挙動を調査することで、さまざまなアルゴリズム-データセットの組み合わせに対して効率と効果を最大化するためのダウンサンプリング構成を最適化するのに役立ちます。

4. Environmental Impact Assumptions and Broader Metrics 4. 環境影響の仮定と広範な指標
This study approximates carbon emissions and energy savings based on assumptions such as linear correlations between runtime, energy consumption, and CO2e emissions. 
本研究は、ランタイム、エネルギー消費、およびCO2e排出量との間の線形相関などの仮定に基づいて、炭素排出量とエネルギー節約を近似しています。Although useful for obtaining an initial understanding, these estimates may vary significantly depending on real-world factors such as hardware, software configurations, and energy sources. 
初期の理解を得るためには有用ですが、これらの推定値は、ハードウェア、ソフトウェア構成、エネルギー源などの実世界の要因によって大きく異なる可能性があります。Future research should consider additional sustainability metrics, such as the impact of downsampling on hardware and computational resource demands (e.g., RAM and GPU usage). 
今後の研究では、ダウンサンプリングがハードウェアや計算リソースの要求（例：RAMやGPU使用量）に与える影響など、追加の持続可能性指標を考慮すべきです。Expanding sustainability metrics beyond carbon emissions and runtime would provide a more comprehensive view of the environmental implications of downsampling strategies. 
炭素排出量やランタイムを超えた持続可能性指標を拡張することで、ダウンサンプリング戦略の環境への影響に関するより包括的な視点を提供することができます。

5. Limited Evaluation Metrics 5. 限られた評価指標
Performance evaluation in this research is based solely on the nDCG@10 metric, which measures the quality of ranking of the top 10 recommendations. 
本研究のパフォーマンス評価は、トップ10の推薦のランキングの質を測定するnDCG@10指標のみに基づいています。While nDCG@10 is relevant for ranking-focused tasks, it does not encompass other important aspects of recommender systems, such as precision, recall, diversity, and novelty. 
nDCG@10はランキングに焦点を当てたタスクには関連していますが、精度、再現率、多様性、新規性など、レコメンダーシステムの他の重要な側面を含んでいません。Future studies should incorporate a broader range of evaluation metrics to provide a more holistic assessment of performance. 
今後の研究では、パフォーマンスのより包括的な評価を提供するために、より広範な評価指標を取り入れるべきです。This would allow researchers to better understand the trade-offs introduced by downsampling, particularly its broader impact on the quality and utility of recommendations. 
これにより、研究者はダウンサンプリングによってもたらされるトレードオフ、特に推薦の質と有用性に対するより広範な影響をよりよく理解できるようになります。

The findings of this research contribute significantly to the emerging field of Green Recommender Systems, highlighting the potential of downsampling as a strategy to balance sustainability and effectiveness. 
本研究の結果は、グリーンレコメンダーシステムの新興分野に大きく貢献しており、持続可能性と効果をバランスさせる戦略としてのダウンサンプリングの可能性を強調しています。しかし、これらの限界に対処し、提案された今後の方向性を追求することで、効率的でスケーラブルかつ環境に配慮したレコメンダーシステムの開発をさらに進めることができます。



## Bibliography 参考文献

- [1]↑G.Adomavicius and J.Zhang.Impact of data characteristics on recommender systems performance.ACM Transactions on Management Information Systems (ACM Trans. Manag. Inform. Syst.), 3(1):1–17, April 2012.URL:http://doi.acm.org/10.1145/2151163.2151166,doi:10.1145/2151163.2151166.
- [1]↑G.AdomaviciusとJ.Zhang.データ特性がレコメンダーシステムの性能に与える影響.ACMマネジメント情報システムトランザクション (ACM Trans. Manag. Inform. Syst.), 3(1):1–17, 2012年4月.URL:http://doi.acm.org/10.1145/2151163.2151166,doi:10.1145/2151163.2151166.

- [2]↑O.Y. Al-Jarrah, P.D. Yoob, S.Muhaidat, G.K. Karagiannidis, and K.Taha.Efficient machine learning for big data: A review.Big Data Research, 2(3):87–99, 2015.doi:10.1016/j.bdr.2015.04.002.
- [2]↑O.Y. Al-Jarrah, P.D. Yoob, S.Muhaidat, G.K. Karagiannidis, とK.Taha.ビッグデータのための効率的な機械学習: レビュー.Big Data Research, 2(3):87–99, 2015.doi:10.1016/j.bdr.2015.04.002.

- [3]↑M.T. Alam, S.Ubaid, S.Shakil, S.S. Sohail, M.Nadeem, S.Hussain, and J.Siddiqui.Comparative analysis of machine learning based filtering techniques using movielens dataset.Procedia Computer Science, 194:210–217, 2021.Department of Computer Science and Engineering, Jamia Hamdard, New Delhi, India; School of Computer Science, University of Petroleum and Energy Studies; Department of Computer Science, Aligarh Muslim University, Aligarh, India.
- [3]↑M.T. Alam, S.Ubaid, S.Shakil, S.S. Sohail, M.Nadeem, S.Hussain, とJ.Siddiqui.Movielensデータセットを使用した機械学習に基づくフィルタリング技術の比較分析.Procedia Computer Science, 194:210–217, 2021.インド、ニューデリーのジャミアハムダルド大学コンピュータサイエンス工学科; 石油とエネルギー研究大学のコンピュータサイエンス学部; アリガルムスリム大学のコンピュータサイエンス学部.

- [4]↑Y.H. Alfaifi.Recommender systems applications: Data sources, features, and challenges.Information, 15(10):660, 2024.doi:10.3390/info15100660.
- [4]↑Y.H. Alfaifi.レコメンダーシステムの応用: データソース、特徴、および課題.Information, 15(10):660, 2024.doi:10.3390/info15100660.

- [5]↑H.Alibrahim and S.A. Ludwig.Hyperparameter optimization: Comparing genetic algorithm against grid search and bayesian optimization.In2021 IEEE Congress on Evolutionary Computation (CEC), pages 1551–1559. IEEE, 2021.
- [5]↑H.Alibrahim と S.A. Ludwig.ハイパーパラメータ最適化: 遺伝的アルゴリズムとグリッドサーチおよびベイズ最適化の比較.2021 IEEE進化計算会議 (CEC)において、ページ1551–1559. IEEE, 2021.

- [6]↑Y.I. Alzoubi and A.Mishra.Green artificial intelligence initiatives: Potentials and challenges.Journal of Cleaner Production, 468:143090, 2024.URL:https://www.sciencedirect.com/science/article/pii/S0959652624025393,doi:10.1016/j.jclepro.2024.143090.
- [6]↑Y.I. Alzoubi と A.Mishra.グリーン人工知能イニシアティブ: 潜在能力と課題.Journal of Cleaner Production, 468:143090, 2024.URL:https://www.sciencedirect.com/science/article/pii/S0959652624025393,doi:10.1016/j.jclepro.2024.143090.

- [7]↑R.Anand and J.Beel.Auto-surprise: An automated recommender-system (autorecsys) library with tree of parzens estimator (tpe) optimization.In14th ACM Conference on Recommender Systems (RecSys), pages 1–4, 2020.URL:https://arxiv.org/abs/2008.13532.
- [7]↑R.Anand と J.Beel.Auto-surprise: パルゼン推定器 (tpe) 最適化を用いた自動レコメンダーシステム (autorecsys) ライブラリ.第14回ACMレコメンダーシステム会議 (RecSys)において、ページ1–4, 2020.URL:https://arxiv.org/abs/2008.13532.

- [8]↑D.A. Anggoro and S.S. Mukti.Performance comparison of grid search and random search methods for hyperparameter tuning in extreme gradient boosting algorithm to predict chronic kidney failure.International Journal of Intelligent Engineering & Systems, 14(6), 2021.
- [8]↑D.A. Anggoro と S.S. Mukti.慢性腎不全を予測するための極端な勾配ブースティングアルゴリズムにおけるハイパーパラメータ調整のためのグリッドサーチとランダムサーチ手法の性能比較.国際知能工学およびシステムジャーナル, 14(6), 2021.

- [9]↑A.Arabzadeh.Master thesis github repository, 2025.URL:https://github.com/Ardalan224/Master-Thesis/.
- [9]↑A.Arabzadeh.修士論文のGitHubリポジトリ, 2025.URL:https://github.com/Ardalan224/Master-Thesis/.

- [10]↑A.Arabzadeh, T.Vente, and J.Beel.Green recommender systems: Optimizing dataset size for energy-efficient algorithm performance.InInternational Workshop on Recommender Systems for Sustainability and Social Good (RecSoGood) at the 18th ACM Conference on Recommender Systems (ACM RecSys), 2024.
- [10]↑A.Arabzadeh, T.Vente, と J.Beel.グリーンレコメンダーシステム: エネルギー効率の良いアルゴリズム性能のためのデータセットサイズの最適化.第18回ACMレコメンダーシステム会議 (ACM RecSys)における持続可能性と社会的善のためのレコメンダーシステムに関する国際ワークショップ (RecSoGood), 2024.

- [11]↑D.Basaran, E.Ntoutsi, and A.Zimek.Redundancies in data and their effect on the evaluation of recommendation systems: A case study on the amazon reviews datasets.InProceedings of the 2017 SIAM International Conference on Data Mining (SDM), pages 390–398. SIAM, 2017.
- [11]↑D.Basaran, E.Ntoutsi, と A.Zimek.データの冗長性とそれがレコメンダーシステムの評価に与える影響: アマゾンレビューのデータセットに関するケーススタディ.2017年SIAM国際データマイニング会議 (SDM)の議事録において、ページ390–398. SIAM, 2017.

- [12]↑J.Beel.Our use of ai-tools for writing research papers, 2024.In: Intelligent Systems Group, Blog.URL:https://isg.beel.org/blog/2024/08/19/our-use-of-ai-tools-for-writing-research-papers/.
- [12]↑J.Beel.研究論文執筆のためのAIツールの使用について, 2024年.In: インテリジェントシステムグループ, ブログ.URL:https://isg.beel.org/blog/2024/08/19/our-use-of-ai-tools-for-writing-research-papers/.

- [13]↑J.Beel and V.Brunel.Data pruning in recommender systems research: Best-practice or malpractice?InACM RecSys 2019 Late-breaking Results, Copenhagen, Denmark, September 2019.16th–20th September 2019.
- [13]↑J.Beel と V.Brunel.レコメンダーシステム研究におけるデータプルーニング: ベストプラクティスか、悪行か?ACM RecSys 2019の遅延結果において、コペンハーゲン, デンマーク, 2019年9月. 2019年9月16日–20日.

- [14]↑J.Beel, A.Said, T.Vente, and L.Wegmeth.Green recommender systems – a call for attention.Recommender-Systems.com Blog, 2024.URL:https://isg.beel.org/pubs/2024_Green_Recommender_Systems-A_Call_for_Attention.pdf,doi:10.31219/osf.io/5ru2g.
- [14]↑J.Beel, A.Said, T.Vente, と L.Wegmeth.グリーンレコメンダーシステム – 注目を呼びかける.Recommender-Systems.com ブログ, 2024.URL:https://isg.beel.org/pubs/2024_Green_Recommender_Systems-A_Call_for_Attention.pdf,doi:10.31219/osf.io/5ru2g.

- [15]↑C.Bentzer and H.Thulin.Recommender systems using limited dataset sizes, June 8 2023.Degree Project in Computer Science and Engineering, First cycle, 15 credits, KTH Royal Institute of Technology.
- [15]↑C.Bentzer と H.Thulin.限られたデータセットサイズを使用したレコメンダーシステム, 2023年6月8日.コンピュータサイエンスと工学の学位プロジェクト, 第1サイクル, 15クレジット, KTH王立工科大学.

- [16]↑S.A. Budennyy, V.D. Lazarev, N.N. Zakharenko, A.N. Korovin, O.A. Plosskaya, D.V. Dimitrov, V.S. Akhripkin, I.V. Pavlov, I.V. Oseledets, I.S. Barsola, etal.Eco2ai: carbon emissions tracking of machine learning models as the first step towards sustainable ai.Doklady Mathematics, 106(Suppl 1):S118–S128, 2022.
- [16]↑S.A. Budennyy, V.D. Lazarev, N.N. Zakharenko, A.N. Korovin, O.A. Plosskaya, D.V. Dimitrov, V.S. Akhripkin, I.V. Pavlov, I.V. Oseledets, I.S. Barsola, など.Eco2ai: 持続可能なAIに向けた第一歩としての機械学習モデルの炭素排出量追跡.Doklady Mathematics, 106(Suppl 1):S118–S128, 2022.

- [17]↑R.Burke.Hybrid recommender systems: Survey and experiments.User Modeling and User-Adapted Interaction, 12:331–370, 2002.doi:10.1023/A:1021240730564.
- [17]↑R.Burke.ハイブリッドレコメンダーシステム: 調査と実験.ユーザーモデリングとユーザー適応インタラクション, 12:331–370, 2002.doi:10.1023/A:1021240730564.

- [18]↑D.Castellanos-Nieves and L.García-Forte.Improving automated machine-learning systems through green ai.Applied Sciences, 13(20), 2023.URL:https://www.mdpi.com/2076-3417/13/20/11583,doi:10.3390/app132011583.
- [18]↑D.Castellanos-Nieves と L.García-Forte.グリーンAIを通じて自動化された機械学習システムを改善する.Applied Sciences, 13(20), 2023.URL:https://www.mdpi.com/2076-3417/13/20/11583,doi:10.3390/app132011583.

- [19]↑D.Castellanos-Nieves and L.García-Forte.Strategies of automated machine learning for energy sustainability in green artificial intelligence.Applied Sciences (2076-3417), 14(14), 2024.
- [19]↑D.Castellanos-Nieves と L.García-Forte.グリーン人工知能におけるエネルギー持続可能性のための自動化された機械学習の戦略.Applied Sciences (2076-3417), 14(14), 2024.

- [20]↑R.Cañamares, P.Castells, and A.Moffat.Offline evaluation options for recommender systems.Information Retrieval Journal, 23:387–410, 2020.doi:10.1007/s10791-020-09371-3.
- [20]↑R.Cañamares, P.Castells, と A.Moffat.レコメンダーシステムのオフライン評価オプション.情報検索ジャーナル, 23:387–410, 2020.doi:10.1007/s10791-020-09371-3.

- [21]↑C.Chen, P.Zhang, H.Zhang, J.Dai, Y.Yi, H.Zhang, and Y.Zhang.Deep learning on computational-resource-limited platforms: A survey.Advances in Artificial Intelligence, 2020.First published: 01 March 2020.doi:10.1155/2020/8454327.
- [21]↑C.Chen, P.Zhang, H.Zhang, J.Dai, Y.Yi, H.Zhang, と Y.Zhang.計算リソースが制限されたプラットフォームにおける深層学習: 調査.人工知能の進歩, 2020.初版: 2020年3月1日.doi:10.1155/2020/8454327.

- [22]↑E.Cho, S.A. Myers, and J.Leskovec.Friendship and mobility: User movement in location-based social networks.InProceedings of the 17th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD ’11), pages 1082–1090, San Diego, California, USA, 2011. Association for Computing Machinery.doi:10.1145/2020408.2020579.
- [22]↑E.Cho, S.A. Myers, と J.Leskovec.友情と移動: ロケーションベースのソーシャルネットワークにおけるユーザーの動き.第17回ACM SIGKDD国際会議の議事録 (KDD ’11)において、ページ1082–1090, サンディエゴ, カリフォルニア, アメリカ, 2011年. コンピュータ機械協会.doi:10.1145/2020408.2020579.

- [23]↑P.Cremonesi, Y.Koren, and R.Turrin.Performance of recommender algorithms on top-n recommendation tasks.InRecSys ’10: Proceedings of the Fourth ACM Conference on Recommender Systems, pages 39–46, New York, NY, USA, 2010. ACM.doi:10.1145/1864708.1864721.
- [23]↑P.Cremonesi, Y.Koren, と R.Turrin.トップn推薦タスクにおけるレコメンダーアルゴリズムの性能.RecSys ’10: 第4回ACMレコメンダーシステム会議の議事録において、ページ39–46, ニューヨーク, NY, アメリカ, 2010年. ACM.doi:10.1145/1864708.1864721.

- [24]↑M.D. Ekstrand.Lenskit for python: Next-generation software for recommender systems experiments.InProceedings of the 29th ACM International Conference on Information & Knowledge Management, pages 2999–3006, Virtual Event, Ireland, 2020.doi:10.1145/3340531.3412778.
- [24]↑M.D. Ekstrand.Python用Lenskit: レコメンダーシステム実験のための次世代ソフトウェア.第29回ACM国際情報および知識管理会議の議事録において、ページ2999–3006, バーチャルイベント, アイルランド, 2020年.doi:10.1145/3340531.3412778.

- [25]↑Ember and Energy Institute.Carbon intensity of electricity generation – ember and energy institute, 2024.Yearly Electricity Data by Ember; Statistical Review of World Energy by Energy Institute. Dataset processed by Our World in Data.URL:https://ourworldindata.org/grapher/carbon-intensity-electricity.
- [25]↑Ember とエネルギー研究所.電力生成の炭素強度 – ember とエネルギー研究所, 2024年.Emberによる年間電力データ; エネルギー研究所による世界エネルギーの統計レビュー.データセットはOur World in Dataによって処理されました.URL:https://ourworldindata.org/grapher/carbon-intensity-electricity.

- [26]↑A.A. Gowda, H.-K. Su, and W.-K. Kuo.Personalized e-commerce: Enhancing customer experience through machine learning-driven personalization.In2024 IEEE International Conference on Information Technology, Electronics and Intelligent Communication Systems (ICITEICS), pages 1–5, 2024.doi:10.1109/ICITEICS61368.2024.10624901.
- [26]↑A.A. Gowda, H.-K. Su, と W.-K. Kuo.パーソナライズされたeコマース: 機械学習駆動のパーソナライズを通じて顧客体験を向上させる.2024 IEEE国際情報技術、電子工学、インテリジェントコミュニケーションシステム会議 (ICITEICS)において、ページ1–5, 2024年.doi:10.1109/ICITEICS61368.2024.10624901.

- [27]↑S.Gupta and J.Beel.Auto-caserec: Automatically selecting and optimizing recommendation-systems algorithms.OSF Preprints DOI:10.31219/osf.io/4znmd,, 2020.doi:10.31219/osf.io/4znmd.
- [27]↑S.Gupta と J.Beel.Auto-caserec: レコメンダーシステムアルゴリズムの自動選択と最適化.OSF Preprints DOI:10.31219/osf.io/4znmd,, 2020.doi:10.31219/osf.io/4znmd.

- [28]↑F.M. Harper and J.A. Konstan.The movielens datasets: History and context.ACM Transactions on Interactive Intelligent Systems (TiiS), 5(4):1–19, 2015.doi:10.1145/2827872.
- [28]↑F.M. Harper と J.A. Konstan.Movielensデータセット: 歴史と文脈.ACMインタラクティブインテリジェントシステムトランザクション (TiiS), 5(4):1–19, 2015.doi:10.1145/2827872.

- [29]↑L.Hennig, T.Tornede, and M.Lindauer.Towards leveraging automl for sustainable deep learning: A multi-objective hpo approach on deep shift neural networks.InarXiv, 2024.URL:https://arxiv.org/abs/2404.01965,arXiv:2404.01965.
- [29]↑L.Hennig, T.Tornede, と M.Lindauer.持続可能な深層学習のためのautomlの活用に向けて: 深層シフトニューラルネットワークにおける多目的HPOアプローチ.arXiv, 2024.URL:https://arxiv.org/abs/2404.01965,arXiv:2404.01965.

- [30]↑J.L. Herlocker, J.A. Konstan, and J.Riedl.Explaining collaborative filtering recommendations.InCSCW ’00: Proceedings of the 2000 ACM Conference on Computer Supported Cooperative Work, pages 241–250, New York, NY, USA, 2000. ACM.doi:10.1145/358916.358995.
- [30]↑J.L. Herlocker, J.A. Konstan, と J.Riedl.協調フィルタリング推薦の説明.CSCW ’00: 2000年ACMコンピュータ支援協調作業会議の議事録において、ページ241–250, ニューヨーク, NY, アメリカ, 2000年. ACM.doi:10.1145/358916.358995.

- [31]↑K.Jain and R.Jindal.Sampling and noise filtering methods for recommender systems: A literature review.Engineering Applications of Artificial Intelligence, 122:106129, 2023.
- [31]↑K.Jain と R.Jindal.レコメンダーシステムのためのサンプリングとノイズフィルタリング手法: 文献レビュー.人工知能の工学応用, 122:106129, 2023.

- [32]↑S.KJ, S.N. BV, C.C.S. Balne, V.K. Sunkara, S.Bhaduri, V.Jain, and A.Chadha.Advancements in modern recommender systems: Industrial applications in social media, e-commerce, entertainment, and beyond, 2024.hal-04711099.URL:https://hal.archives-ouvertes.fr/hal-04711099.
- [32]↑S.KJ, S.N. BV, C.C.S. Balne, V.K. Sunkara, S.Bhaduri, V.Jain, と A.Chadha.現代のレコメンダーシステムの進展: ソーシャルメディア、eコマース、エンターテインメントなどにおける産業応用, 2024.hal-04711099.URL:https://hal.archives-ouvertes.fr/hal-04711099.

- [33]↑U.Kużelewska.Effect of dataset size on efficiency of collaborative filtering recommender systems with multi-clustering as a neighbourhood identification strategy.In V.V. Krzhizhanovskaya etal., editors,Computational Science – ICCS 2020, volume 12139 ofLecture Notes in Computer Science. Springer, Cham, 2020.doi:10.1007/978-3-030-50420-5\_25.
- [33]↑U.Kużelewska.データセットサイズが多クラスタリングを近隣識別戦略として用いた協調フィルタリングレコメンダーシステムの効率に与える影響.V.V. Krzhizhanovskaya ら編, 計算科学 – ICCS 2020, コンピュータサイエンスの講義ノート第12139巻. Springer, Cham, 2020.doi:10.1007/978-3-030-50420-5\_25.

- [34]↑A.Lacoste, A.Luccioni, V.Schmidt, and T.Dandres.Quantifying the carbon emissions of machine learning.arXiv preprint, 2019.arXiv:1910.09700 [cs.CY].URL:https://mlco2.github.io/impact/.
- [34]↑A.Lacoste, A.Luccioni, V.Schmidt, と T.Dandres.機械学習の炭素排出量を定量化する.arXiv プレプリント, 2019.arXiv:1910.09700 [cs.CY].URL:https://mlco2.github.io/impact/.

- [35]↑L.Lannelongue, J.Grealey, and M.Inouye.Green algorithms: Quantifying the carbon footprint of computation.Advanced Science, 8(12):2100707, 2021.arXiv:https://onlinelibrary.wiley.com/doi/pdf/10.1002/advs.202100707,doi:10.1002/advs.202100707.
- [35]↑L.Lannelongue, J.Grealey, と M.Inouye.グリーンアルゴリズム: 計算の炭素フットプリントを定量化する.アドバンスドサイエンス, 8(12):2100707, 2021.arXiv:https://onlinelibrary.wiley.com/doi/pdf/10.1002/advs.202100707,doi:10.1002/advs.202100707.

- [36]↑F.Lin, X.Zhu, Z.Zhao, D.Huang, Y.Yu, X.Li, Z.Zheng, T.Xu, and E.Chen.Knowledge graph pruning for recommendation.arXiv preprint arXiv:2405.11531, 2024.
- [36]↑F.Lin, X.Zhu, Z.Zhao, D.Huang, Y.Yu, X.Li, Z.Zheng, T.Xu, と E.Chen.レコメンデーションのための知識グラフプルーニング.arXiv プレプリント arXiv:2405.11531, 2024.

- [37]↑E.Maslowska, E.C. Malthouse, and L.D. Hollebeek.The role of recommender systems in fostering consumers’ long-term platform engagement.Journal of Service Management, 2022.Article publication date: 9 May 2022, Issue publication date: 8 July 2022.
- [37]↑E.Maslowska, E.C. Malthouse, と L.D. Hollebeek.消費者の長期的なプラットフォームエンゲージメントを促進するレコメンダーシステムの役割.サービスマネジメントジャーナル, 2022年.記事の公開日: 2022年5月9日, 発行日: 2022年7月8日.

- [38]↑Z.Meng, R.McCreadie, C.Macdonald, and I.Ounis.Exploring data splitting strategies for the evaluation of recommendation models.InProceedings of RecSys ’20: The 14th ACM Recommender Systems Conference (RecSys ’20), page8, New York, NY, USA, 2020. ACM.doi:10.1145/1122445.1122456.
- [38]↑Z.Meng, R.McCreadie, C.Macdonald, と I.Ounis.レコメンデーションモデルの評価のためのデータ分割戦略の探求.RecSys ’20: 第14回ACMレコメンダーシステム会議の議事録において、ページ8, ニューヨーク, NY, アメリカ, 2020年. ACM.doi:10.1145/1122445.1122456.

- [39]↑L.Michiels, R.Verachtert, and B.Goethals.Recpack: An(other) experimentation toolkit for top-n recommendation using implicit feedback data.InProceedings of the 16th ACM Conference on Recommender Systems, RecSys ’22, page 648–651, New York, NY, USA, 2022. Association for Computing Machinery.doi:10.1145/3523227.3551472.
- [39]↑L.Michiels, R.Verachtert, と B.Goethals.Recpack: 暗黙のフィードバックデータを使用したトップn推薦のための(別の)実験ツールキット.第16回ACMレコメンダーシステム会議の議事録において、RecSys ’22, ページ648–651, ニューヨーク, NY, アメリカ, 2022年. コンピュータ機械協会.doi:10.1145/3523227.3551472.

- [40]↑W.Ng, B.Minasny, W.D.S. Mendes, and J.A.M. Demattê.The influence of training sample size on the accuracy of deep learning models for the prediction of soil properties with near-infrared spectroscopy data.SOIL, 6:565–578, 2020.doi:10.5194/soil-6-565-2020.
- [40]↑W.Ng, B.Minasny, W.D.S. Mendes, と J.A.M. Demattê.近赤外分光データを用いた土壌特性の予測における深層学習モデルの精度に対するトレーニングサンプルサイズの影響.SOIL, 6:565–578, 2020.doi:10.5194/soil-6-565-2020.

- [41]↑J.Ni, J.Li, and J.McAuley.Justifying recommendations using distantly-labeled reviews and fine-grained aspects.InProceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages 188–197, Hong Kong, China, 2019. Association for Computational Linguistics.doi:10.18653/v1/D19-1018.
- [41]↑J.Ni, J.Li, と J.McAuley.遠くにラベル付けされたレビューと細かい側面を使用して推薦を正当化する.2019年自然言語処理に関する経験的手法会議および第9回国際共同自然言語処理会議 (EMNLP-IJCNLP)の議事録において、ページ188–197, 香港, 中国, 2019年. 計算言語学協会.doi:10.18653/v1/D19-1018.

- [42]↑Y.Qu, L.Qu, T.Chen, X.Zhao, Q.V.H. Nguyen, and H.Yin.Scalable dynamic embedding size search for streaming recommendation.InProceedings of the 33rd ACM International Conference on Information and Knowledge Management, pages 1941–1950, 2024.
- [42]↑Y.Qu, L.Qu, T.Chen, X.Zhao, Q.V.H. Nguyen, と H.Yin.ストリーミング推薦のためのスケーラブルな動的埋め込みサイズ検索.第33回ACM国際情報および知識管理会議の議事録において、ページ1941–1950, 2024年.

- [43]↑C.Roy and S.S. Rautaray.Challenges and issues of recommender system for big data applications.In S.S. Rautaray, P.Pemmaraju, and H.Mohanty, editors,Trends of Data Science and Applications, volume 954 ofStudies in Computational Intelligence. Springer, Singapore, 2021.doi:10.1007/978-981-33-6815-6_16.
- [43]↑C.Roy と S.S. Rautaray.ビッグデータアプリケーションのためのレコメンダーシステムの課題と問題.S.S. Rautaray, P.Pemmaraju, と H.Mohanty 編, データサイエンスとアプリケーションのトレンド, 計算知能の研究第954巻. Springer, シンガポール, 2021.doi:10.1007/978-981-33-6815-6_16.

- [44]↑S.O.S. Santos, A.Skiarski, D.García-Núñez, V.Lazzarini, R.DeAndradeMoral, E.Galvan, A.L.C. Ottoni, and E.Nepomuceno.Green machine learning: Analysing the energy efficiency of machine learning models.In2024 35th Irish Signals and Systems Conference (ISSC), pages 1–6, 2024.doi:10.1109/ISSC61953.2024.10603302.
- [44]↑S.O.S. Santos, A.Skiarski, D.García-Núñez, V.Lazzarini, R.DeAndradeMoral, E.Galvan, A.L.C. Ottoni, と E.Nepomuceno.グリーン機械学習: 機械学習モデルのエネルギー効率を分析する.2024年第35回アイルランド信号とシステム会議 (ISSC)において、ページ1–6, 2024年.doi:10.1109/ISSC61953.2024.10603302.

- [45]↑J.B. Schafer, D.Frankowski, J.Herlocker, and S.Sen.Collaborative filtering recommender systems.Computer Science, 2007.
- [45]↑J.B. Schafer, D.Frankowski, J.Herlocker, と S.Sen.協調フィルタリングレコメンダーシステム.コンピュータサイエンス, 2007年.

- [46]↑J.B. Schafer, J.A. Konstan, and J.Riedl.E-commerce recommendation applications.GroupLens Research Project, Department of Computer Science and Engineering, University of Minnesota, 2001.
- [46]↑J.B. Schafer, J.A. Konstan, と J.Riedl.電子商取引推薦アプリケーション.GroupLens研究プロジェクト, ミネソタ大学コンピュータサイエンスと工学科, 2001年.

- [47]↑M.Schmidt, J.Nitschke, and T.Prinz.Evaluating the performance-deviation of itemknn in recbole and lenskit.arXiv preprint arXiv:2407.13531, 2024.
- [47]↑M.Schmidt, J.Nitschke, と T.Prinz.RecboleとLenskitにおけるitemknnの性能偏差の評価.arXiv プレプリント arXiv:2407.13531, 2024.

- [48]↑T.Silveira, M.Zhang, X.Lin, W.Ma, H.-F. Lam, and W.Guo.How good your recommender system is? a survey on evaluations in recommendation.International Journal of Machine Learning and Cybernetics, 10:813–831, 2019.doi:10.1007/s13042-017-0762-9.
- [48]↑T.Silveira, M.Zhang, X.Lin, W.Ma, H.-F. Lam, と W.Guo.あなたのレコメンダーシステムはどれほど良いですか? 推薦における評価に関する調査.国際機械学習とサイバネティクスジャーナル, 10:813–831, 2019.doi:10.1007/s13042-017-0762-9.

- [49]↑M.Singh.Scalability and sparsity issues in recommender datasets: a survey.Knowledge and Information Systems, 62:1–43, 2020.doi:10.1007/s10115-018-1254-2.
- [49]↑M.Singh.レコメンダーデータセットにおけるスケーラビリティとスパース性の問題: 調査.知識と情報システム, 62:1–43, 2020.doi:10.1007/s10115-018-1254-2.

- [50]↑G.Spillo, A.DeFilippo, M.Milano, C.Musto, and G.Semeraro.Towards sustainability-aware recommender systems: Analyzing the trade-off between algorithms performance and carbon footprint.InProceedings of the ACM Conference, page7, Singapore, Singapore, 2023.doi:10.1145/3604915.3608840.
- [50]↑G.Spillo, A.DeFilippo, M.Milano, C.Musto, と G.Semeraro.持続可能性を意識したレコメンダーシステムに向けて: アルゴリズムの性能と炭素フットプリントのトレードオフを分析する.ACM会議の議事録において、ページ7, シンガポール, シンガポール, 2023年.doi:10.1145/3604915.3608840.

- [51]↑G.Spillo, A.DeFilippo, C.Musto, M.Milano, and G.Semeraro.Towards green recommender systems: Investigating the impact of data reduction on carbon footprint and algorithm performances.In18th ACM Conference on Recommender Systems, 2024.
- [51]↑G.Spillo, A.DeFilippo, C.Musto, M.Milano, と G.Semeraro.グリーンレコメンダーシステムに向けて: データ削減が炭素フットプリントとアルゴリズムの性能に与える影響を調査する.第18回ACMレコメンダーシステム会議, 2024年.

- [52]↑C.Sun, A.Shrivastava, S.Singh, and A.Gupta.Revisiting unreasonable effectiveness of data in deep learning era.InProceedings of the IEEE International Conference on Computer Vision (ICCV), pages 843–852, 2017.
- [52]↑C.Sun, A.Shrivastava, S.Singh, と A.Gupta.深層学習時代におけるデータの不合理な効果を再考する.IEEE国際コンピュータビジョン会議 (ICCV)の議事録において、ページ843–852, 2017年.

- [53]↑N.Sundberg.Tackling ai’s climate change problem.MIT Sloan Management Review, 65(2):38–41, 2024.
- [53]↑N.Sundberg.AIの気候変動問題に取り組む.MITスローンマネジメントレビュー, 65(2):38–41, 2024.

- [54]↑P.B. Thorat, R.M. Goudar, and S.Barve.Survey on collaborative filtering, content-based filtering and hybrid recommendation system.International Journal of Computer Applications, 110(4), January 2015.Poonam B. Thorat, R. M. Goudar, Sunita Barve, Computer Engineering, MIT Academy of Engineering, Pune, India.
- [54]↑P.B. Thorat, R.M. Goudar, と S.Barve.協調フィルタリング、コンテンツベースフィルタリング、ハイブリッド推薦システムに関する調査.国際コンピュータアプリケーションジャーナル, 110(4), 2015年1月.Poonam B. Thorat, R. M. Goudar, Sunita Barve, コンピュータ工学, MIT工学アカデミー, プネ, インド.

- [55]↑T.Tornede, A.Tornede, J.Hanselle, F.Mohr, M.Wever, and E.Hüllermeier.Towards green automated machine learning: Status quo and future directions.arXiv / Journal of Artificial Intelligence Research, 77:427–457, 2021 / 2023.
- [55]↑T.Tornede, A.Tornede, J.Hanselle, F.Mohr, M.Wever, と E.Hüllermeier.グリーン自動化機械学習に向けて: 現状と今後の方向性.arXiv / 人工知能研究ジャーナル, 77:427–457, 2021 / 2023.

- [56]↑R.VanMeteren and M.VanSomeren.Using content-based filtering for recommendation.InProceedings of the machine learning in the new information age: MLnet/ECML2000 workshop, volume30, pages 47–56. Barcelona, 2000.
- [56]↑R.VanMeteren と M.VanSomeren.推薦のためのコンテンツベースフィルタリングの使用.新しい情報時代における機械学習: MLnet/ECML2000ワークショップの議事録において、ボリューム30, ページ47–56. バルセロナ, 2000年.

- [57]↑T.Vente, M.Ekstrand, and J.Beel.Introducing lenskit-auto, an experimental automated recommender system (autorecsys) toolkit.InProceedings of the 17th ACM Conference on Recommender Systems, pages 1212–1216, 2023.URL:https://dl.acm.org/doi/10.1145/3604915.3610656.
- [57]↑T.Vente, M.Ekstrand, と J.Beel.lenskit-autoの導入: 実験的な自動レコメンダーシステム (autorecsys) ツールキット.第17回ACMレコメンダーシステム会議の議事録において、ページ1212–1216, 2023年.URL:https://dl.acm.org/doi/10.1145/3604915.3610656.

- [58]↑T.Vente, L.Wegmeth, A.Said, and J.Beel.From clicks to carbon: The environmental toll of recommender systems.InProceedings of the 18th ACM Conference on Recommender Systems, RecSys ’24, page 580–590, New York, NY, USA, 2024. Association for Computing Machinery.URL:https://arxiv.org/abs/2408.08203,doi:10.1145/3640457.3688074.
- [58]↑T.Vente, L.Wegmeth, A.Said, と J.Beel.クリックから炭素へ: レコメンダーシステムの環境コスト.第18回ACMレコメンダーシステム会議の議事録において、RecSys ’24, ページ580–590, ニューヨーク, NY, アメリカ, 2024年. コンピュータ機械協会.URL:https://arxiv.org/abs/2408.08203,doi:10.1145/3640457.3688074.

- [59]↑Y.Wang, L.Wang, Y.Li, D.He, and T.-Y. Liu.A theoretical analysis of ndcg type ranking measures.In Shai Shalev-Shwartz and Ingo Steinwart, editors,Proceedings of the 26th Annual Conference on Learning Theory, volume30 ofProceedings of Machine Learning Research, pages 25–54, Princeton, NJ, USA, 12–14 Jun 2013. PMLR.URL:https://proceedings.mlr.press/v30/Wang13.html.
- [59]↑Y.Wang, L.Wang, Y.Li, D.He, と T.-Y. Liu.ndcgタイプのランキング測定の理論的分析.Shai Shalev-Shwartz と Ingo Steinwart 編, 学習理論に関する第26回年次会議の議事録において、ボリューム30の機械学習研究の議事録, ページ25–54, プリンストン, NJ, アメリカ, 2013年6月12日–14日. PMLR.URL:https://proceedings.mlr.press/v30/Wang13.html.

- [60]↑L.Xu, Z.Tian, G.Zhang, J.Zhang, L.Wang, B.Zheng, Y.Li, J.Tang, Z.Zhang, Y.Hou, etal.Towards a more user-friendly and easy-to-use benchmark library for recommender systems.InProceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval, pages 2837–2847, 2023.
- [60]↑L.Xu, Z.Tian, G.Zhang, J.Zhang, L.Wang, B.Zheng, Y.Li, J.Tang, Z.Zhang, Y.Hou, など.レコメンダーシステムのためのよりユーザーフレンドリーで使いやすいベンチマークライブラリに向けて.第46回国際ACM SIGIR会議の議事録において、情報検索の研究と開発に関するページ2837–2847, 2023年.

- [61]↑X.Yang, Y.Wang, C.Chen, Q.Tan, C.Yu, J.Xu, and X.Zhu.Computation resource allocation solution in recommender systems.arXiv, 2103.02259, March 2021.URL:https://arxiv.org/abs/2103.02259,arXiv:2103.02259.
- [61]↑X.Yang, Y.Wang, C.Chen, Q.Tan, C.Yu, J.Xu, と X.Zhu.レコメンダーシステムにおける計算リソース割り当てソリューション.arXiv, 2103.02259, 2021年3月.URL:https://arxiv.org/abs/2103.02259,arXiv:2103.02259.

- [62]↑F.Zogaj, J.P. Cambronero, M.C. Rinard, and J.Cito.Doing more with less: Characterizing dataset downsampling for automl.Proceedings of the VLDB Endowment (PVLDB), 14(11):2059–2072, 2021.doi:10.14778/3476249.3476262.
- [62]↑F.Zogaj, J.P. Cambronero, M.C. Rinard, と J.Cito.より少ないものでより多くを行う: automlのためのデータセットダウンサンプリングの特性. VLDBエンダウメントの議事録 (PVLDB), 14(11):2059–2072, 2021.doi:10.14778/3476249.3476262.



## Declaration of Authorship 著作権の宣言

I hereby confirm that this thesis and the work presented in it is entirely my own. 
私はここに、この論文およびその中で提示された作業が全て私自身のものであることを確認します。

Where I have consulted the work of others, this is always clearly stated. 
他者の作業を参照した場合は、常に明確に記載しています。

All statements taken literally from other writings or referred to by analogy are marked, and the source is always given. 
他の文献から文字通り引用したすべての文や、類推によって言及された文はマークされており、出典は常に示されています。

This paper has not yet been submitted to another examination office, either in the same or similar form. 
この論文は、同じまたは類似の形で他の審査機関に提出されていません。

Place and Date:Siegen, 31.01.2025
場所と日付：ジーゲン、2025年1月31日

Place and Date:
場所と日付：

Name:Ardalan Arabzadeh
名前：アルダラン・アラブザデ

Name:
名前：



##### Report Github Issue GitHubの問題報告

LATE
LATE

A
A

E
E

xml
xml



## Instructions for reporting errors エラー報告の手順

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. 
私たちは論文のHTMLバージョンを改善し続けており、あなたのフィードバックはアクセシビリティとモバイルサポートの向上に役立ちます。 
To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:
HTMLのエラーを報告して、変換とレンダリングの改善に役立てるために、以下のいずれかの方法を選択してください：
- Click the "Report Issue" button.
- "Report Issue"ボタンをクリックしてください。
- Open a report feedback form via keyboard, use "Ctrl + ?".
- キーボードを使って報告フィードバックフォームを開くには、「Ctrl + ?」を使用してください。
- Make a text selection and click the "Report Issue for Selection" button near your cursor.
- テキストを選択し、カーソルの近くにある「Report Issue for Selection」ボタンをクリックしてください。
- You can use Alt+Y to toggle on and Alt+Shift+Y to toggle off accessible reporting links at each section.
- 各セクションでアクセシブルな報告リンクをオンにするにはAlt+Yを、オフにするにはAlt+Shift+Yを使用できます。

Our team has already identified the following issues. 
私たちのチームはすでに以下の問題を特定しています。 
We appreciate your time reviewing and reporting rendering errors we may not have found yet. 
私たちは、まだ見つけていない可能性のあるレンダリングエラーをレビューし報告するためにあなたが費やした時間に感謝します。 
Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. 
あなたの努力は、すべての読者のためにHTMLバージョンを改善するのに役立ちます。なぜなら、障害は研究へのアクセスの障壁であってはならないからです。 
Thank you for your continued support in championing open access for all.
すべての人にオープンアクセスを推進するための継続的なサポートに感謝します。

Have a free development cycle? 
開発サイクルに余裕がありますか？ 
Help support accessibility at arXiv! 
arXivでのアクセシビリティをサポートしてください！ 
Our collaborators at LaTeXML maintain a list of packages that need conversion, and welcome developer contributions.
LaTeXMLの協力者は、変換が必要なパッケージのリストを維持しており、開発者の貢献を歓迎しています。
