# Link

- https://www.sciencedirect.com/science/article/pii/S0921344916302439

## title

Material stock's overburden: Automatic spatial detection and estimation of domestic extraction and hidden material flows
物質ストックの重荷 国内採掘と隠れたマテリアルフローの自動空間検出と推定

## Abstract

- Anthropogenic material stocks are expanding at ever-increasing rates across the world, and their environmental and economic impacts draw more and more attention from academia, policy makers, and economic and environmental bodies. 人為的な物質ストックは世界各地で拡大し、その環境的・経済的影響が学界、政策立案者、経済・環境団体からますます注目されている。
- As the knowledge base regarding anthropogenic material stocks expands, it is important to not only comprehend the societal side of material stock growth but also its counterpart to the material balance—the natural environment from which the materials used for stocks come from. 人為的な物質ストックに関する知識ベースが拡大するにつれ、物質ストック増加の社会的側面を理解するだけでなく、物質バランスの対極にある、ストックに使用される物質が由来する自然環境も理解することが重要となっている。
- However, due to difficulties of data procurement, and muted interest in materials which are considered low-value high volume, the environmental burdens related to construction minerals have received less attention so far despite the huge amounts involved. しかし、建設用鉱物の環境負荷は、データ調達の難しさや低価多量とされる材料への関心の低さなどから、その量が多いにもかかわらず、これまであまり注目されてこなかった。
- In this study, we employ geographic information systems (GIS) with digital elevation model (DEM) datasets, to form an automated method of detection and measurement of the anthropogenic disturbance of soil and earth at excavation and mining sites, 本研究では、地理情報システム（GIS）と数値標高モデル（DEM）データセットを用いて、掘削・採掘現場における土砂の人為的撹乱を自動検出・測定する方法を構築した。
- , which accounts not only for the material extracted for usage in the anthroposphere, but also its related unused extraction. この地理的に明確な方法により、人為的攪乱の位置と量を直接特定することができる。
- Using Japan as a case study, the results suggest that the ratio of unused extraction to used extraction may exceed 1:1 for construction minerals in Japan. 日本を事例として、日本の建設用鉱物について、未使用採掘量と使用採掘量の比率が1：1を超える可能性を示唆する結果を得た。
- We also find that the environmental effects of anthropogenic activity are bigger than natural soil disturbance by several orders of magnitude, highlighting the need to reduce raw material extraction and increase the efficient use of the existing material stock.また、人為的な活動の環境影響は、自然の土壌攪乱よりも数桁大きいことがわかり、原料の採取を減らし、既存の原料ストックの有効利用を増やす必要性が強調された。

# Introduction

- 人間社会で年間消費される材料のうち、多くの場合 50%以上が人為 的な材料ストックとなる.
  - 金属、木材、プラ スチックなどのほか、骨材、砂、アスファルト、セメントなど、主に建 設用の鉱物である

## Hidden flowの存在

- マテリアルフローとストック会計の基礎となる物質収支の原則は、 人為的に使用中の物質ストックが増加すると、それと同量に自然ストッ クが減少することを述べている。
- However, for every unit of material that enters the economy, there is a certain amount of material which was mined, quarried, excavated, moved, or otherwise disturbed during the pro-curement of the wanted material but has no economic function and remains in nature, albeit in an altered state. しかし、経済に投入される材料 1 単位 に対して、**必要な材料を調達するために採掘、採石、掘削、移動**、その他の妨害を受けたが、経済的機能を持たず、**変化した状態とはいえ自然界に残っている材料**が一定量存在する。
- This material, termed **overburden**, **hidden material flow (HMF)** (Adriaanse et al., 1997), or **unused extraction** (Eurostat, 2001) has long been recognized to be of the same order of magnitude as the used extraction (Matthews et al., 2000).この物質は、残土、隠れた物質 フロー（HMF）（ Adriaanse et al.、1997）、 ま た は 未 使 用 抽 出 物 （Eurostat、2001）と呼ばれ、使用済み抽出物と同じ大きさであると 長い間認識されてきた（Matthews et al.、2000）。
  - これは、景観の変 化、土地被覆や水系の変化、生物多様性や動物の生息地に対する影響な ど、材料の採取に関連した生態学的ストレスの指標として機能する
  - 特 に建設業の場合、資源採取、住宅開発のための切り土・盛り土、ビルや 社会インフラの建設などが大規模な地形変化を生み出している（田村, 2012）。
- This rapid anthropogenic disturbance causes destruction of the natural environment, and it is accelerated by technical innovations in industrial fields and ongoing demands for construction materials and mineral resources.このような急激な人為的攪乱は、自然環境の破壊を引き起こし、 産業分野の技術革新や建設資材・鉱物資源の継続的な需要によって加速 されている。

## 使用される材料と使用されない材料の両方のフローを考慮すべきだが、後者が軽視されている事実とその理由

- 使用される材料と使用されない材料の両方のフローを考慮するため に、総材料所要量（TMR）という指標が制定された（Bringezu et al.2004; Eurostat, 2001）。
- しかしながら、上記に引用したように、近 年の材料ストック分野の進歩は、材料ストックバランスの社会経済的な 角度に焦点が当てられているため、**自然環境の側面はやや軽視されてきた**。
  - これは、建設鉱物がどこにでもあり、金属や貴金属などの材料に比べて見かけ上の使用量・未使用量の比率が小さいこともあるが、**データ 調達の難しさが大きな理由**であろう。
  - 社会で消費される材料は経済的な 理由から一般的に計上され、使用中の在庫はボトムアップ、トップダウ ンなどの手法で特定、カウントすることができるが（Müller et al., 2014; Tanikawa et al., 2015）、未使用の材料についてはデータがあま り存在しない。
  - 多くの場合、**係数**（Bringezu and Schuetz, 2001）や **特定の事例から算出された残土と有用物の比率**（Douglas and Lawson, 2000 など）といった間接的な算定方法が用いられるが、これらは空間的にも時間的にも非常に大きなばらつきがあり、場所によって鉱物や化 学的土壌組成は異なり、鉱区や採石場は時間の経過と共に枯渇しその比 率は高くなり、そうした間接法の不確実性を増している。

## そこで本研究は...

- 建設資 材の採取は、掘削・採掘跡に明確な物理的変化を残す。
  - このような 地形変化を分析することで、社会的な材料ストックに対する継続的 な需要によって引き起こされる人為的撹乱を直接測定することがで きる。
- 本研究では、土壌の自然攪乱とは異なる、掘削現場や露天掘 りの鉱山に特有の地形変化を識別することによって、人為的攪乱を 検出する自動化手法を導入する。
  - この新しい手法を日本全国に適用 し、日本における人為的攪乱を直接測定する。
  - 日本では、国内での 鉱物の採取はほとんど掘削や採石による建設用鉱物に限られている ため、この方法は良いケーススタディとなる。
    - <=地表変動法では検出 できないような活発な地下鉱山や井戸は、ほとんど存在しないから。
- These anthropogenic disturbances (AD) include both the used extracted material (domestic extraction, DE in MFA parlance) and the unused extraction (HMF).これらの人為的撹乱（AD）には、使用済みの抽出物（国内抽 出、MFA 用語では DE）と未使用の抽出物（HMF）の両方が含まれ る。
  - Thus the anthropogenic disturbances detected and mapped with our method can be easily related to the official DE (used extraction) statistics,
    - したがって、我々の方法で検出されマップ化された人為的攪乱 は、公式の DE（使用済み抽出物）統計と容易に関連付けることがで き、
  - and **the difference between the two** can be assumed to account for Japan’s hidden material flow. 両者の差は日本の隠れた物質フローを説明するものと仮定する ことができる。

# Data and methods

## Research approach

- 地表の撹乱や影響は、地形図、航空写真、現地調査などを用いて研 究するのが一般的であり、最近ではリモートセンシング技術や地理 情報システム（GIS）の発達により、3 次元モデルの利用が進んでい る（Ross et al.、2016）。
- GIS、特にデジタル標高モデル（DEM） と呼ばれる標高図は、標高や他の地形属性の経時変化を比較するこ とで、地形変化の直接測定を容易にする。
- **DEM は、衛星データ、航空写真、等高線図など、いくつかのデータソースから作成され**ます。
  - 航空写真や等高線は古い地形を再現するのに適しています が、衛星データに比べるとカバーできる範囲が限定される。
  - 衛星デ ータから作成された DEM データセットは、カバー範囲はほぼ地 球全域に及ぶ。しかし、航空写真から作成された DEM と比較す ると解像度や標高精度は劣る。

### Table1 DEM を用いた地形変化に関する最近の研究事例

- 基本的に人為的攪乱は、採掘や掘削が行われた場所の**標高変化を 2 つ の期間で比較する**ことによって算出され、**実質的にその場所で移動した 土の量を測定する**ものである。
  - しかし、この方法では、自然の土壌攪乱も検出される。
-

### 図1 アルゴリズム 本研究では...

- 本研究では、一連の GIS ツールを用いて、人 為的攪乱を自動的に検出するアルゴリズムを紹介
  - まず、 これらのユニークな地形変化を特定し
  - 次に既知のサイトでアル ゴリズムを校正し、
  - 最後に日本全体の地形を走査させて、全国規 模の人為的攪乱の検出、地図化、量的計測を行う。

## Digital elevation models

- 本研究で使用する基本的な GIS データセットは、**デジタル標高モデル（DEM）**である。
  - DEM はラスターデータセット：一定の空間解像度 を持つセルのデジタル化されたグリッドで、各セルは気温、土地利用、 標高などの特定のタイプの情報を表す値を持つ（Esri, 2015a）。
  - DEM の場合、ラスターは地形の標高を表すグリッドマップであり、グリッド の各セルの値はそのセル内の地形の海抜からの標高を表しています。
- DEM には 2 種類
  - Digital Terrain Model (DTM)
    - 地表を覆っ ている物体（樹木や建物など）を取り除いた、地表の標高
  - Digital Surface Model (DSM).
    - 地表にあるすべての物体が含まれる。
- 本研究で使用したソースは、国土地理院（GSI, 2015a,b）が公開し ている 2 つの DTM データセットである（表 2）(1998年と2005年)
  - これらは二つとも、日本の全領域をカバーする 1:25000 contour maps**等高線地図**から作成された。

## Slope and aspect

- In addition to the elevation data necessary for the calculation of the volume of AD, two more geomorphological attributes of a cell are required for the identification of AD as opposed to natural causes: the slope and its aspect.AD の体積計算に必要な標高データに加え、**自然的な原因とは異なる AD を特定するため**には、さらに 2 つのセルの地形的な属性、すなわち**勾配**とその**アスペクト**が必要となる。(Table2)
  - スロープは、セル の標高から隣接する隣地の標高までの最も急な傾斜角度で、0◦ （平坦）から 90◦（急勾配）までと定義されています（Esri, 2015c）。
  - アスペクトは、0◦（北）から 359.9◦まで時計回りで 測定された傾斜のコンパス方向である（Esri, 2015d）
- 標高 だけでなく、勾配やアスペクトを用いることで、山の上の平地、 丘の上の一定方向への傾斜、山の平均的な勾配など、地形の特徴 をより明確に観察することが可能になる（Shahabi and Hashim, 2015; Quan and Lee, 2012）。
  - DEM データソースには、各セル の地形の標高だけが含まれています。
  - 2つのデータセットのセルの 勾配とアスペクトは、ArcGIS ソフトウェアの空間分析ツールボッ クスで利用可能なツールを使用して計算されました。

## Automated detection and estimation model

- 人為的攪乱を自動的に特定するために、ArcGIS の Weighted Overlay Tool を使用する。
  - これは、**サイト選定や適性モデルなどの 地理的多基準問題を解決できる計算ツール**である（Esri, 2015e; Malczewski, 2000）。
  - 地形学の分野では、この Weighted Overlay Tool は地すべり感受性のマッピングに使用されており、その結果は ハザード軽減の目的や地域計画に有用な情報を示しているが（清水 ら、2008）、人為的攪乱の検出にはまだ使用されていなかった。
- 2 つの調査期間中の標高、傾斜、アスペクトの 3 つの属性の変化 は、重み付けオーバーレイツールの入力基準として使用された。
  - 3 つ の属性はそれぞれ異なるスケールと測定単位を持つため、この ArcGIS ツールで要求されるように、**最小値 0 から最大値 9 まで列挙 された相対スケールに再スケーリング**する必要があった（Esri, 2015e）。
    - 標高変化は 10 段階（0-9）で再スケーリングされ、2 つの 期間の間で標高の損失が大きいほど高い値が与えられ、標高に変化がない、または正の変化は 0 が割り当てられた。
    - 同じ 10 段階の再ス ケーリングプロセスが斜面の変化にも適用され、この場合、人為的 撹乱がより平坦な地形を生み出すことが以前に発見されているため （吉田ら、レビュー中）、セルがより平らになり急でなければなるほ ど高い値が割り当てられることになる。
- 既知の 4 つの採掘場をケーススタディとしてモデルのキャリブレー ションを行った結果、**AD の検出には標高の変化が勾配やアスペクトの変化よりも重要**であることが認識された。
  - 自動検出に使用される最終的なデータグリッドは、各セルについて、3 つの属性の割合の重み付け値を合計した 1 つの数値となる。

## Post-detection processing and calculation of AD

- **採掘と掘削作業は、個々の 50m セルよりも大きなスケールで行われる**ため、人為的攪乱は一つのセル内だけでなく、**複数のセルに またがって観測される**。
  - ArcGIS のマジョリティ・フィルター・ツールを用いて、エラーと思われる**単一セルや小さなセル・クラスターを除去**している。
  - マジョリティフィルタは、グリッド内のゾーンの エッジを一般化するために、その連続する近隣のマジョリティ値に 基づいてセルを置き換える（Esri, 2015f）。
- これに続き、Cluster Outlier Analysis Tool を適用して、AD が特定されたセルをクラスタに統一(=**セルをグルーピング！**)した。各クラスタは、人為的攪乱の単一のサイトとして扱われる（Esri, 2015g）。
- この後、**地すべり GIS データを重ね合わせ、誤って検出された地 すべり領域を除外**し、人為的擾乱のみを抽出するようにした。

最後に、残りの地形変化地点は人為的攪乱地点と判断でき、その総量はセルごとの標高変化から以下の式で算出した。

$$
AD(gravel, stone) = \sum{(V_{t2, i}- V_{t1, i})}
$$

where $AD(gravel, stone)$ denotes **the total volume of the anthropogenic disturbance**, $V_{t2.i}$ is the volume in the period 1998–2005 at site i, and $V_{t1,i}$ is the volume in 1987 at site i.

# Results

## Calibration of detection and estimation accuracy
- 大阪の関西国際空港の建設では、人工島を埋め立てるために大量の土砂が採取された。掘削場所は、同地域の阪南、加太、洲本、津名である（大林、2011；大阪府、1996；依上、2011）。図3は、関西国際空港と掘削地点の位置関係を示している。これらの地点は、企業や自治体の記録から掘削に関する情報（位置、掘削量、活動期間）が得られること（表4）、また、杉本ら（2015）、吉田ら（審査中）によりDEMデータによる先行研究が行われており、これらの先行研究の結果と比較できることから、本研究で採用した検出手法の精度確認とキャリブレーションに選ばれたものである。この4地点は、自動検出アルゴリズムが地点を認識し、正確に検出することを確認するために、既知の位置と面積を用いた校正に使用されました。4遺跡のうち、Hannan遺跡の発掘調査だけが、2つのDEMデータセットの年の間に完全に収まっていた。他の遺跡は1987年に発掘が開始されたが、後者のデータセットの最終年以降に終了している。そのため、阪南の全発掘量の公式統計と我々の計算方法を比較し、その正確性を確認することができた。なお、阪南事業所の掘削物はすべて輸送され、埋立処分されたため、公式には事業所等にHMFは残っていない（大林、2011；大阪府、1996；依上、2011）。阪南鉱区では、公式記録では5500万m3であるのに対し、本研究で算出した総採取量は5590万m3に達している（大林、2011）。このことから、DEMによる推定では、統計的に記録されている量と比較して、約1.6%の推定となることがわかります。杉本ら（2015）によれば、DEMに基づく推定では、元のDEMの精度にもよるが、8％～17％程度の過大推定となる可能性があるとのことである。阪南の事例に加えて、三崎地区にも着目し、杉本ら（2015）の研究再現性を確認した。地元自治体の記録によると、三崎の総物的発掘量は7000万m3である。採掘前はデジタルマップ50mグリッド、採掘後はALOS30mグリッドを使用し、総物質採取量は7430万m3に達することが分かった。この結果は、政府の記録が正確であると仮定すると、DEMによる推定はわずか6%の過大評価であることを示唆している。杉本ら（2015）の結果（8％～17％）と比較すると、我々の推定結果はより低い過大評価を生み出しており（6％）、高い研究再現性が三崎の研究で示された。したがって、我々の結果と公表されている統計値との間に乖離はあるものの、それは最小限のものであり、我々の手順に対する信頼性をもたらすものである（図4）。

www.DeepL.com/Translator（無料版）で翻訳しました。

## Anthropogenic disturbance in Japan

# Discussion
- How much of the 7 billion m3 of earth and soil disturbed by anthropogenic activities is actually used by the Japanese economy? 
  - The attributions of the 7 billion m3 is presented in Fig. 8.

## Accounting for AD

## Environmental and geographic implications of AD

# Conclusions
- 社会の物質ストックは、環境から膨大な量の原料を必要とします。 
  - ストックの蓄積が人間圏に及ぼす影響が注目されている一方で、必要な 素材を採取する際の上流環境負荷に関する研究はこれまで、金属などの 経済的に価値の高い素材に限られており、地理的に明示的な分析はさら に珍しいと言えます。
  - GIS や DEM データを用いた地理的解析により、 人為的攪乱の検出や HMF を含む総量の推定が可能になり、自然環境の 破壊や時には取り返しのつかない影響の空間情報も明らかになりました。
- 本研究では、国内で消費される建設鉱物にほぼ限定して、日本にお ける掘削や採掘などの大規模な人為的攪乱に着目した。
  - 約 70 億 m3 が計上された。
  - **そのうち 26 億～38 億 m3 が未使用の抽出**であり、これは決して は経済圏に入るため価値がないとされていますが、その膨大な量は 環境に深刻な悪影響を与えています。

