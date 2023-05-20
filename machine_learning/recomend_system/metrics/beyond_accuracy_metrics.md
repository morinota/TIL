# Diversity metrics group:

推薦リストのアイテム間の非類似性を表すmetrics.

- “intra-list” diversity:推薦リスト内の多様性
- temporal diversity: ユーザの異なる訪問時に表示された、推薦アイテムの数に依存する(by Lathia et al[10])
- "personalization": ユーザペア間の推薦結果の多様性(by Zhou et al[30])

# Novelty metrics group:

推薦アイテムがユーザにとって新しいものであるかを示すmetrics(ex. ユーザーがすでに好きなカテゴリのアイテムを推薦することは、Noveltyが低い推薦と言える)

- “surprisal”: (by reference[30])

# Coverage metrics group:

- coverage: これまでに推薦されたことのあるアイテムの割合を示すmetrics.
  - $coverage = \frac{|I_s|}{|I|}$
- prediction coverage: 推薦結果を作成可能なユーザ数(?)
  - $coverage = \frac{|I_p|}{|I|}$
- Gini Index: ジニ係数
- Shannon’s Entropy [17]

# Serendipity metrics group:

推薦アイテムがユーザにとって予想外であると同時にlikeである性質を示す.

概念的には、Adamopoulosらの式が良く用いられる.

$$
serendipity = \frac{|UNEXP \cap USEFUL|}{|N|}
$$

UNEXPは、ユーザにとって意外性のあるコンテンツ集合.以下の式で定義される.

$$
UNEXP = RS \setminus PM
$$

ここで、$RS$は対象の推薦システムが提示した推薦リスト、$PM$はprimitiveな(accuracy-basedな?)推薦アルゴリズムが生成した推薦リスト.
primitiveな予測モデルは高いレータビリティを示し低い意外性を生み出す、という仮定に基づいている.

- Serendipity by Ge [7]:
  - $SRDP = \frac{\sum_{i=1}^{N}u(RS_{i})}{N}$
    - ここで、$RS_{i}$は $UNEXP$のアイテムであると定義する.
    - $u()$ は、ユーザにとって有用(like)なアイテムなら1, 有用でない(dislike)なアイテムなら0を返すfunction.
  - 参考:
    - [元論文](https://www.researchgate.net/publication/221140976_Beyond_accuracy_Evaluating_recommender_systems_by_coverage_and_serendipity)
    - [日本語のレビュー論文?](https://www.jstage.jst.go.jp/article/fss/30/0/30_718/_pdf)
- Serendipity by Murakami [14]
