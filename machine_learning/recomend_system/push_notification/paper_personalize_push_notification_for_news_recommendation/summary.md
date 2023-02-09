本記事において、 :thinking: ←このマークがついている記述は私の感想です...!

# Personalized Push Notifications for News Recommendation

published date: 13 September 2019,

authors: Babak Loni, Anne Schuth, Lucas van de Haas, Jeroen Jansze, Vasco Visser, Marlies van der Wees

url: https://proceedings.mlr.press/v109/loni19a.html

(勉強会発表者: morinota)

:smiley:

---

## どんなもの?

- プッシュ通知は、モバイルデバイス上で最新かつ重要なニュースをユーザーに通知するための迅速かつ効果的な方法.
- 本論文では、ベルギーのニュースメディア企業「DPG Media」のプッシュ通知システムを対象に、Personalized Push Notificationを作成する為の分散システムを提案.
- また本論文内で、Personalized Push Notificationが満たすべき基準や、未解決の問題についても主張している.
- なお、Personalizeのモデル自体に関しては、以下の**二種類のスコア**を特徴量とした分類モデル(=多分outputは過去のプッシュ通知のタップしたか否かとか?)を採用しているっぽい...!
  - content similarity:
    - アイテムのcontentを表すベクトル & ユーザが読んだアイテムたちのcontentを集約したものを表すベクトル のcosine similarity.
  - location overlap:
    - アイテムに紐づくlocationと、ユーザに紐づくlocationの重なりの度合い.
  - **新規ニュースアイテムが作成される度に**、ユーザ\*アイテムペアに対して上記の2種類の特徴量を生成し、分類モデル(=教師あり学習? or シンプルにスコアに対する閾値分類?)に通してpositiveと判定された場合に、プッシュ通知の候補に入れる、みたいな事をしているっぽい...!
  - (論文ではプッシュ通知システム全体に関して説明しているので、モデル単体の説明はラフな感じ...!)
  - (個人的には ２つ目のスコア=location overlapが新鮮で興味深かった...!)

## 先行研究と比べて何がすごい?

- 論文によると、"プッシュ通知でパーソナライズされたニュース推薦を提供することを提案する研究は存在しない"とのこと. その点でOriginalityは高そう.

## どうやって有効だと検証した?

- 検証結果は記載されていない.

## 技術や手法の肝は？

Personalized Push Notificationが満たすべき性質として、以下の7つを主張.

1. Personalized:
   - プッシュ通知はユーザの興味や嗜好を考慮すべき.
2. Explainable:
   - プッシュ通知が送られた理由は説明可能であるべき.
3. Include important news:
   - パーソナライズの程度に関わらず、プッシュ通知は速報や重要な情報をユーザに伝えるべき.
4. Diversity and opposing opinions
   - パーソナライズがユーザにfilter bubbleをもたらさないようにする為に、多様性を持たせるべき & ユーザが良く読む意見ばかりに依らないようにすべき?(=客観性?)
5. (Hyper-)local news
   - (Hyper-)local newsとは、ごく少数のユーザにしか関係しないがそのユーザにとって非常に関連性の高いニュースの一つ. **ユーザは近くで何が起こっているかを気にしている**.
   - この性質は、パーソナライズされていないプッシュ通知システムでは考慮が困難.
6. Anonymous users:
   - アカウントを持たない匿名ユーザにも、対応できる必要がある.
   - (↑に関してはプロダクトやサービスに依るよなー...)
7. Address the cold-start problem:
   - ニュース推薦の本質的な課題として、cold-start問題がある.
   - 新しく公開された記事に対するInteractionが無いor非常に限られている為、ニュース記事のcontentを効果的に利用する必要がある.
   - (Push通知は基本的に新しいアイテムを推薦する. -> collaborative filteringベースの手法のみでは対応困難 -> content-base的な要素を含める必要がありそう...!)

プッシュ通知のパーソナライズのモデルに関して:
**新規ニュースアイテムが作成される度に**、ユーザ\*アイテムペアに対して特徴量を生成し、分類モデル(=教師あり学習? or シンプルにスコアに対する閾値分類?)に通してpositiveと判定された場合に、プッシュ通知の候補に入れる、みたいな事をしているっぽい...!

本論文では特徴量の例として、以下の2つを挙げている.

- content similarity:
- location overlap:

content similarityに関しては、アイテムのcontentを表すベクトル & ユーザが読んだアイテムたちのcontentを集約したものを表すベクトル のcosine類似度を採用している. アイテムベクトルは、Word2Vecを用いたwordベクトルのBag-of-Words表現. ユーザベクトルは、ユーザがreactionしたアイテムベクトルの集約.

location overlapに関しては、アイテムに紐づくlocationとユーザに紐づくlocationの重なりの度合い.

具体的なスコアの定義式は以下.

$$
l_{overlap} = w \frac{|l_{user} \cap l_{item}|}{|l_{user}|}
+ (1 - w) \frac{|gl_{user} \cap gl_{item}|}{|gl_{user}|}
$$

ここで、

- $l_{item}$: 記事アイテムから抽出したlocationの集合(=固有表現抽出的なアプローチで"location"に関するtokenを抽出してるっぽい...?)
- $gl_{item}$: アプリで記事を読んでいる時のユーザーの物理的位置(位置情報??)の集合.
- $l_{user}$: ユーザーが過去に読んだ記事のlocations($l_{item}$)の集合
- $w$: 上記の比率の計算スコアへの寄与を制御する重みパラメータ.

(このlocationの情報を活用するのは、前述されているPersonalized Push Notificationが満たすべき性質"(Hyper-)local news"を実現しようとしているようで面白い...! 通常のニュースリストの推薦と比べて、緊急性の高いプッシュ通知においてより重要な性質なのかも)
(あとlocationに関するcontextを考慮する推薦は、元々グルメアプリとかホテル予約サイトとかでは重要だろうかと思ってたけど、ニュース推薦においても重要な性質かもと感じた)

## 議論はある？

本論文のアプローチで未解決の課題として、以下の5つを主張している.

1. Daily limits: 単位時間当たり(ex. 1日, 1時間, etc.)のユーザあたりのプッシュ通知数の制限. 今後、実験する予定. パーソナライズも検討.
2. Diversity: **重複防止** と **トピックの多様化** の両方が含まれる. 推薦のDiversityに関する既存研究の多くは、top Nの推薦リストの多様化に焦点を当てている. Push通知において、どう多様化すべきか. 現在は、ほぼ重複したプッシュを送るのを避ける為に、以前にプッシュした記事との類似性を考慮している. 将来的には、ユーザ毎にプッシュ通知するトピックを多様化させたい.
3. Explainability: プッシュ通知のすぐ下に、推薦した理由の説明を表示させたい. プロダクトのアルゴリズムがこの特定の記事をこのユーザーにプッシュする原因となった、最も一般的な理由を提供することを検討.
4. Explicit Feedback: 推薦理由を説明した後は、その理由に対するfeedback機能をユーザーに提供することを検討. ユーザは特定の記事ではなく、"記事を推薦した理由"に対してfeedbackを提供する仕様. このexplicitなfeebbackをユーザのprofileの更新に活用したい.
5. Timing: Push通知の適切なタイミング.

## 次に読むべき論文は？

本論文のRelated Workにて、情報推薦分野において特に"ニュース推薦"を対象とした論文がいくつか紹介されていたので、読んでみようと思う...!
(これまではあまり、特定のDomainに焦点を当てた論文を触っていなかったなぁ...)

- ニュース推薦 Domainのサーベイ論文...?[News recommender systems – survey and roads ahead. Information Processing and Management](https://dl.acm.org/doi/pdf/10.1145/1772690.1772780?casa_token=_NkfT8SH_V4AAAAA:mkjn91maD3dGMMF6GbfFSbmOqqa9tfqBDohAO26vAytPbVt0BQidOPWX0tL4EsUkRD00tJ-4CrMWAQ)
- ニュース推薦におけるscalableなアーキテクチャを提案してるらしい [An analysis of recommender algorithms for online news](http://doi.acm.org/10.1145/2888422.2888443)
- 同じくscalableなニュース推薦システムの提案 [Scalable news recommendation using multi-dimensional similarity and jaccard-kmeans clustering.](http://dx.doi.org/10.1016/j.jss.2014.04.046)
- ニュース記事とユーザの地理的な近接性に関して? [Towards a journalist-based news recommendation system: The wesomender approach](https://doi.org/10.1016/j.eswa.2013.06.032)
