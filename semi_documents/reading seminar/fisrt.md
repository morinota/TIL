# Overview

## title

Quantifying urban mass gain and loss by a GIS-based material stocks and flows analysis
GISを用いた物質ストック・フロー解析による都市の質量増減の定量化

## Abstract

- Rapid urbanization generates substantial demand, use, and demolition waste of construction materials.
  - 急速な都市化により、建設資材の需要、使用、解体廃棄物が大量に発生している。
- However, the existing top-down or bottom-up frameworks combining material flow analysis (MFA) and geographic information system (GIS) tend to underestimate both input and output of construction material flows due to insufficient descriptions of key processes in building construction and demolition.
  - しかし、MFAとGISを組み合わせた既存のフレームワークは、建築物の建設と解体における主要プロセスの記述が不十分である為、**建設資材フローのInputとOutputを過小評価する傾向**にある。
- To address this limitation, this study identifies four important and complementary processes construction, demolition, replacement, and maintenance, and integrates them into an improved framework to capture all material flows.
  - その制限を解決する為に、本研究では、建設、解体、交換、維持管理という4つの重要且つ補完的なプロセスを特定し、それらを統合して、**全てのMFを把握する為の**改良されたフレームワークを構築した。
- We take Xiamen, a rapidly urbanizing city, as a case study to verify this framework.
  - ケーススタディとして、急速に都市化が進むXiamenに対してフレームワークを適用し検証した。
- The results show that ∼40% of material inputs and ∼65% of outputs are underestimated by previous frameworks because they fail to capture material inputs in building maintenance and outputs in construction.
  - その結果、従来の手法では、建物の維持管理におけるマテリアルのInputの約40%、アウトプットの約65%が過小評価されている事が分かった。
- ## These findings indicate a better estimation of such key flows in the modeling framework helps to accurately characterize building material metabolism.
- Based on systematic counting of material stocks and flows, the improved framework can help design effective policies for urban resource management by explicitly recognizing the spatiotemporal patterns and processes of material metabolism.

# Introduction

## 都市質量の変化の重要性

- 都市は、自然環境と人口環境の間で物質、水、エネルギｰの交換を継続的に発生させており、都市の物質的なInputがOutputを上回るとアンバランスが生じ、都市の質量増加に寄与する。
- 都市質量の変化は、エネルギー消費や温室効果ガス排出に大きな影響を与える事が示されている。

## 都市の物質収支の空間分布に関する研究

- These frameworks usually start at building material stock quantification and then estimate material flows based on the difference of material stocks by process-based assumptions, which belong to the “bottom-up and stock-driven approach” (Augiseau & Barles, 2017).
-

## 弱点

- First, material use in new construction activity was considered as an input flow in previous studies (Han et al., 2018; Heeren & Hellweg, 2019; Reyna & Chester, 2014; Tanikawa & Hashimoto, 2009) but waste generation in this process was usually omitted.
  - ストックの新規建設活動における物質の使用は、Inputのみカウントされ、廃棄物の発生は省略されていた。
- Second, the maintenance of in-use buildings would generate both material input and output instead of the net flow before and after the refurbishment (Heeren & Hellweg, 2019).
  - 使用中の建物の維持管理は、材料のInputとOutputの両方を発生させる。
- Third, buildings’ demolition usually followed a lognormal (Miatto et al., 2017) or a logistic growth (Tanikawa & Hashimoto, 2009) with regard to building’s age and the demolition rate can be used to estimate material output for a community (Han et al., 2018), a city (Hu, Voet, et al., 2010), or even a country (Bergsdal et al., 2007; Huang et al., 2017; Müller, 2006; Yang & Kohler, 2008).
  - 建物の解体は、建物の築年数に関して寿命分布に従う事が多く、都市、地域、国スケールでは用いられる。
  - However, this assumption cannot be adapted to material output quantification at the individual building level because the demolition of an individual building not only is correlated to building’s age but also depends on urban planning, building’s status, cost-benefit in economy, and residents’ willingness.
    - しかし、個々の建物の解体は、建物の築年数に相関するだけでなく、都市計画、建物のステータス、経済におけるコストベネフィット、住民の意思に依存する為、この仮定は個々の建物レベルでのマテリアルアウトプットの定量化には適応できない。 (Kohler & Hassler, 2002; Pomponi & Moncaster, 2017; Wuyts et al., 2019,)
  - These various drivers can determine building demolition through complex socioeconomic interactions and therefore lead to nonlinear relationships and feedbacks (Caduff et al., 2014; Kohler & Hassler, 2002).
    - これらの様々なドライバーは、複雑な社会経済的相互作用を通じて建物の取り壊しを決定する為、非線形な関係やフィードバックにつながる (Caduff et al., 2014; Kohler & Hassler, 2002).

## そこで本研究は...

To fill these gaps, we

- (1) proposed an improved framework to characterize material metabolism and avoid the underestimation of material flow, especially at the individual building level,
  - 個々の建物レベルでの物質フローの過小評価を避ける為の改良されたフレームワークを提案
- (2) took Xiamen, a rapidly urbanizing city in China, as a case study to verify this framework, and
  - Xiamenをケーススタディとしてフレームワークを検証し、
- (3) examined both the benefits and challenges of combining spatial analysis with material flow analysis (MFA).
  - 空間分析と物質フロー解析を組み合わせる利点と課題の両方を検証した。

# methodology

## An improved framework for estimating building material metabolism

### Material Stocks

$$
MS_m^t = \sum{Q_{i, s, n}^t \times MI_{s, m, n}^t}
$$

where

- MS is total stock of material m at year t,
- Q is the total floor area (footprint \* level) of building i with structure s ad year of build n,
- and MI represents the intensity of material m with structures s and year of build n.

### Material Flows

$$
MS_m^{t+1} - MS_m^{t}  = NetFlow = MIF_{m}^{t+1} - MOF_{m}^{t+1} \\

MIF_{m}^{t+1} = MIF_{i, m, s1}^{t+1} + MIF_{i, m, s3}^{t+1} + MIF_{i, m, s4}^{t+1} \\

MOF_{m}^{t+1} = MOF_{i, m, s1}^{t+1} + MOF_{j, m, s2}^{t+1} + MOF_{j, m, s3}^{t+1} + MIF_{i, m, s4}^{t+1} \\
$$

where

- MIF_m^{t+1} is the total input of material m from year t to t+1,
- MOF_m^{t+1} is the total output of material m from year t to t+1,
- s1, s2, s3, and, s4 represent the four complementary construction activities, respectively.

#### Construction

$$
NetFlow_{m,s1}^{t+1} = \sum_{i}{MIF_{i,m,s1}^{t+1}} - \sum_{i}{MOF_{i,m,s1}^{t+1}}
$$

ここで、MIF*{s1}は新しい建物iを建設される為に投入される材料。これらの投入材料は次の年代t+1でMSに変換される。
一方、新規建設では建設廃棄物も発生する為、MOF*{s1}となる。(例えば中国では約50kg/m^2)

#### Demolition

Demolitionは都市内の緑地や空き地を増やす為に、使用中の建物を取り壊す事であり、アウトプットフローのみを発生させるもの。

$$
NetFlow_{m,s2}^{t+1} = - \sum_{j}{MOF_{j,m,s2}^{t+1}}
$$

ここで、MOF\_{j,m,s2}^{t+1}の値は、解体された建物jのMSに等しい。

#### Replacement

解体とは異なり、Replacementとは、都市再開発などで古い建物が取り壊された跡地に、新しい建物を建設すること。使用中の建物の解体と新規建設が同時に行われる事。
これがマテリアルフローの過小評価を減らす為に重要。

$$
NetFlow_{m,s3}^{t+1} = \sum_{i}{MIF_{i,m,s3}^{t+1}} - \sum_{j}{MOF_{j,m,s3}^{t+1}} - \sum_{i}{MOF_{i,m,s3}^{t+1}}
$$

where

- MIF\_{s3} is material input for constructing new building i
- and MOF\_{s3} includes both material output from demolished building j and construction waste generated by the new construction i.

#### Maintenance

建物全体ではなく特定の部品が耐用年数を迎えたときに、その部品を交換する事。
そのため、材料のInputとOutputの両方が発生する。

$$
MOF_{m, s4}^{t+1} = \sum_{i}{Q_{i,m}\times (D_i^{t+1} - D_i^{t}) \times MI_{i,m}^n} \\

MIF_{m, s4}^{t+1} = \sum_{i}{Q_{i,m}\times (D_i^{t+1} - D_i^{t}) \times MI_{i,m}^{t+1}} \\

D_{i}^t = \frac{1}{(t-n)SD_i \sqrt{2\pi}}
\cdot e \left( - \frac{[\ln(t-n) - Mean_{i}]^2}{2SD_{i}^2}  \right)
$$

where

- MS^n is the material stock in the building i ad the year of build n
- and D_i^t is the demolition rate of building i at the year t.
  - Its value is related to the average lifespan (mean) and standart deviation (SD) of building i.
  - Mean\_{i} is given by surveys.
  - (e.g., 30-year for brickconcrete structure and 50-year for reinforced-concrete structure)
  - or the year when the ratio of remaining-to-demolished parts is 50:50 (Han et al., 2018; Komatsu, 1992)

_なんか正規分布の式っぽい？？ ==> x = (t-n)とした対数正規分布Log-normal distributionか！笑_

- 対数正規分布のパラメータは\muと\sigma^2。
- PDFは以下。
  ![](https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Lognormal_distribution_PDF.png/488px-Lognormal_distribution_PDF.png)
- CDF(Cumlative distribution function)は以下。
  ![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Lognormal_distribution_CDF.png/488px-Lognormal_distribution_CDF.png)

## Study area and data compilation

- 面積、人口、人口密度
- Google Earth => ArcGISでベクトルポリゴン化
- 属性情報に関しては、かなり地道に頑張ってそう...

# result

## Temporal changes of material stocks and flows MSとMFの時間的変化

1つの都市の結果だけ乗せると、傾向しかわからない。他の都市ものせて比較すべき？？
- **Material stocks** kept increasing in both spatial extent and density on Xiamen Island (Figure 3). In the 1980s, only the downtown area, located in the southwest corner of the island, had materials stocks (Figure 3).
-**Material inputs** showed a reversed U-shaped tendency during 1980–2018.More specifically, material inputs increased from the 1980s, peaked in
2003 (∼8 Mt/year), and then declined (Figure 2).
  - *投入量の各complementary construction activitiesのContributionのBreakdownを把握できるのは、色々得られる示唆が増えそうでいいなぁ...*
- Material outputs generally kept growing since the 1980s and hit ∼0.8 Mt until 2018 (Figure 2).
  - Before 2005, solid waste generated from new construction activities dominated material outputs (Figure 2).
    - 2005年以前は、新規建設活動から発生する固形廃棄物がOutputの大半を占めていた。
  - After that, the maintenance and replacement activities had generated more and more wastes and finally contributed to ∼85% and ∼10% in 2018, respectively (Figure 2).
    - その語、維持管理および交換活動から発生する廃棄物が増加し、2018年にはそれぞれ約85%、約10%を占めるに至った。
    - *Demolishionはゼロ??*
  - The substantial contributions of waste generation (material output) from construction and maintenance activities indicated that it is necessary to identify such activities for material flow quantification (see more in Section 4.1).
    - 建設と維持管理活動によるOutputの寄与が大きい事から、MFの定量化の為には、こうした活動を特定する必要がある事が示された。


## Spatial patterns of material stocks and flows MSとMFの空間的パターン
- 空間的なホットスポット。

# Discussion

## Advances and uncertainties of the improved MFA-GIS framework on material flow quantificationマテリアルフローの定量化に関する改良型フレームワークの進展と不確実性

## Policy implications for urban management 都市経営における政策的な意義
- The spatial features of material stock and potential CDW (output flow) generation simulated based on the updated framework are key information to design recycling facilities planning and optimize the waste management system.
  - シミュレーションされた物質ストックと潜在的なCDW発生の空間的特徴は、リサイクル施設計画を設計し、廃棄物管理システムを最適化する為の重要な情報である。
  - ホットスポットは、地域のリサイクル施設や物流センターを計画する上で重要な地域となる可能性がある。

- そのため、材料投入の時空間的なホットスポットは、空間と時間にわたる体現された環境負荷を理解する為の鍵となる。
- 輸送システムの最適化。

# Conclusions

# Reference
