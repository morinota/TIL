---
marp: false
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
header: 企業と博士人材の交流会(2022年度) Masato Morita
# footer: 2022, 8, 24 Masato Morita
style: |
  section.title * , h1{
      text-align: center;
  }
---

# 自己PRプレゼンテーション

![bg left:50% 100%](building_gis_data.png)

###### 名古屋大学大学院

###### 環境学研究科 都市環境学専攻

###### 博士後期課程1年

#### 森田 大登 (Morita Masato)

---

# Today's Outline

## - Moritaの自己紹介

## - Moritaの修士研究について(2020~2022)

## - Moritaの博士研究について(2022~)

## - Moritaが最近ハマっている事：推薦システム

## - まとめ：結局、Moritaは何がしたいのか??

---

### 自己紹介

![bg left:40% 100% ](全身写真.jpg)

- 氏名:森田 大登 (Morita Masato)
- 趣味:筋トレ
- 好きな事：数学とプログラミング
- 嬉しいと感じる時：
  - スクリプトを設計・実装して、それが想定通りに動いた時
  - 処理を自動化・効率化できた時
  - 技術をより深く理解できた時

---

### 修士&博士研究の背景

###### 「フロー型社会から**ストック型社会**へ」

###### 社会に投入された物質資源を**長期的に利用**する事で、一次資源の新規投入を抑制する

###### - ストックが社会に存在する期間=`滞留年数`

###### - 社会に放置された未利用のストック=`退蔵ストック`

### 本研究のMotivation

##### ストックの**滞留年数を延伸**しつつ**退蔵ストック発生を抑制**するような、**持続可能な都市構造**の提案を試みる

![bg left:39% 102% ](research_background.png)

---

#### 修士研究で行った事① 退蔵ストック発生に寄与する要因は??

###### - 手法：「退蔵ストック発生」は確率的事象であり、その確率は`建物の属性`や周囲の`地理的・社会的要因`によって異なると仮定.`教師有り機械学習(GLM)`による**退蔵確率モデル**の構築・汎化性能の検証・感度解析.

###### - 結果・得られた示唆：

###### 1. 退蔵確率は`「築年数」の増加に伴い上昇`していく.

###### 2. 建物の「`道路へのアクセス状況の悪さ`」が最も退蔵確率の増加に寄与する

![bg right:40% 100% ](result_master_thesis_1.png)

---
#### 修士研究で行った事② 滞留年数の違いに寄与する要因は??

![bg left:40% 100% ](result_master_thesis_2.png)

###### - 手法：「建物の解体」は確率的事象であり、その確率は`建物の属性`や周囲の`地理的・社会的要因`によって異なると仮定.`教師有り機械学習(CART)`による**解体確率モデル**の構築・汎化性能の検証・感度解析.

###### - 結果・得られた示唆：

###### 1. 解体確率は「築年数」の増加に伴い上昇していくが、`築40年を超えた後`は「築年数」は解体確率の増減に寄与しない.

###### 2. 築40年を超えた後の解体確率の傾向は、特に`周囲の人口情報に依存`して異なる.

---

#### 修士研究で行った事③ 退蔵ストック発生&滞留年数の将来シミュレーション

###### - 手法：`退蔵確率モデル`×`解体確率モデル`×乱数生成を用いたシミュレーション手法を構築.福岡県北九州市の全建物に適用.

###### - 結果・得られた示唆：

###### 1. 平均の滞留年数は**人口減少&高齢化に伴い延伸傾向**：34.2年(in2015)→60.1年(in2050)

###### 2. 退蔵ストックは、**都市外縁部&住宅密度の高い斜面市街地**に分布.2050年に掛けて**総量は増加&分布も拡大**

![bg right:40% 80% ](result_master_thesis_3.png)

---

### 修士研究で新たに感じた課題

#### 課題1: ストックの長期的利用の為に、行政は**どう介入**し**どのような都市構造**を目指すべきか?

###### `- 「滞留年数は延伸傾向?どうやら人口減少&高齢化の影響かも?」なのは分かったが、ではストック型社会へ向けて都市はどうあるべきか、**意思決定に関わる有益な示唆**が得られなかった...`

#### 課題2: 既存の退蔵ストックは放置しておいても良いのか?

###### `- 「〇〇な条件下にある建物が退蔵ストック化しやすい」のは分かったが、都市物質代謝の観点からは、既存の退蔵ストックは放置しても良いのでは?`

##### これらの課題を踏まえて、博士研究ではより深く"ストック型社会へ向けた持続可能な都市構造"の検討を試みる...!

---

#### 博士研究での試み①地理情報×コンピュータビジョン技術を用いた退蔵ストック検出

![bg contain vertical right:38%](flag_shape_vec_genarating_process.jpg)
![bg contain right](flag_shape_vec_classified.jpg)

###### 退蔵ストックのデータ収集方法は基本的に人力→コストが大きい→整備状況△or ✗

###### `→人間の視覚的な情報による判断を代替・自動化できれば、データ整備状況を改善できるのでは!`

###### 例:`道路アクセス状況の悪さ`の定量化手法の改善

###### `建物の位置情報→俯瞰図を取得→画像データとしてMLモデルに入力`

###### `→視覚的には認識しやすいが数値化しづらい「周囲の建物 & 道路との位置関係」= を定量化・自動分類`

---

#### 博士研究での試み②空間統計による空間的相互作用を考慮した分析

![bg contain vertical left:37%](spatial_autocorrelation.png)
![bg contain left](spatial_spillover_impact.png)

###### - 修士研究では"ある建物"と"その隣の建物"の確率的事象は"独立"と仮定していた.

###### ＝＞実世界では互いに影響を与えうる...!

`ex1) 近隣に退蔵ストックが存在すると、その周囲の建物の滞留年数は...?`
`ex2) 近隣に大規模商業施設が存在すると、その周囲の建物の退蔵確率は...?`
`ex3) 退蔵ストックの発生は"波及"や"伝染"するのでは...?`

###### **建物間の空間的相互作用**を定量評価し、"持続可能な都市構造"の検討を試みる...!

---

#### 最近ハマっている事：推薦システム

###### きっかけ：Kaggleの個別化推薦コンペ(2022年3月～)

###### - 好きな推薦アルゴリズム: Matrix Factorization(特にimplicit feedbackに対するALS), ConvMF

###### - ハマった理由①データ活用の総合格闘技?

###### - ハマった理由②深層学習がBestではない?

###### - 取り組み①「〇〇の論文読んで実装してみた」記事をQiitaに投稿中

###### - 取り組み②7月から某ニュースアプリの推薦アルゴリズム改善に参加(楽しい&感謝…!)

![bg contain vertical left:38%](https://qiita-user-contents.imgix.net/https%3A%2F%2Fcdn.qiita.com%2Fassets%2Fpublic%2Farticle-ogp-background-9f5428127621718a910c8b63951390ad.png?ixlib=rb-4.0.0&w=1200&mark64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ3PTkxNiZ0eHQ9JUU1JTg4JTlEJUU1JUFEJUE2JUU4JTgwJTg1JUUzJTgxJThDQ29sbGFib3JhdGl2ZSUyMEZpbHRlcmluZyUyMGZvciUyMEltcGxpY2l0JTIwRmVlZGJhY2slMjBEYXRhc2V0cyVFMyU4MiU5MiVFOCVBQSVBRCVFMyU4MiU5MyVFMyU4MSVBNyVFMyU4MiVCOSVFMyU4MiVBRiVFMyU4MyVBOSVFMyU4MyU4MyVFMyU4MyU4MSVFNSVBRSU5RiVFOCVBMyU4NSVFMyU4MSU5NyVFMyU4MSVBNiVFMyU4MSVCRiVFMyU4MiU4QiZ0eHQtY29sb3I9JTIzMjEyMTIxJnR4dC1mb250PUhpcmFnaW5vJTIwU2FucyUyMFc2JnR4dC1zaXplPTU2JnR4dC1jbGlwPWVsbGlwc2lzJnR4dC1hbGlnbj1sZWZ0JTJDdG9wJnM9YWFkNzQ4MjZiNzliMzA3YjdmNGY3MzM3ODNiN2VhNGE&mark-x=142&mark-y=112&blend64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ3PTYxNiZ0eHQ9JTQwbW9yaW5vdGEmdHh0LWNvbG9yPSUyMzIxMjEyMSZ0eHQtZm9udD1IaXJhZ2lubyUyMFNhbnMlMjBXNiZ0eHQtc2l6ZT0zNiZ0eHQtYWxpZ249bGVmdCUyQ3RvcCZzPTNjMDA2ODNmNDMwOWJjOTNmYzM1ODVmYmQxOGQyMGE5&blend-x=142&blend-y=491&blend-mode=normal&s=0d87ee120b5374706294ee30381c3e2b)
![bg contain left](https://qiita-user-contents.imgix.net/https%3A%2F%2Fcdn.qiita.com%2Fassets%2Fpublic%2Farticle-ogp-background-9f5428127621718a910c8b63951390ad.png?ixlib=rb-4.0.0&w=1200&mark64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ3PTkxNiZ0eHQ9JUU4JUE5JTk1JUU0JUJFJUExJUU4JUExJThDJUU1JTg4JTk3JUUzJTgxJUE4JUUzJTgyJUEyJUUzJTgyJUE0JUUzJTgzJTg2JUUzJTgzJUEwJUUzJTgxJUFFJUU4JUFBJUFDJUU2JTk4JThFJUU2JTk2JTg3JUU2JTlCJUI4JUUzJTgyJTkyJUU2JUI0JUJCJUU3JTk0JUE4JUUzJTgxJTk3JUUzJTgxJTlGJUU2JThFJUE4JUU4JTk2JUE2JUUzJTgyJUI3JUUzJTgyJUI5JUUzJTgzJTg2JUUzJTgzJUEwJUUzJTgwJThDQ29udk1GJUUzJTgwJThEJUUzJTgyJTkyJUU0JUJEJTk1JUUzJTgxJUE4JUUzJTgxJThCJUU1JUFFJTlGJUU4JUEzJTg1JUUzJTgxJTk3JUUzJTgxJUE2JUUzJTgxJTg0JUUzJTgxJThEJUUzJTgxJTlGJUUzJTgxJTg0JTIxJUUyJTkxJUEyTkxQJUUzJTgxJUFCJUUzJTgxJThBJUUzJTgxJTkxJUUzJTgyJThCQ05OJUUzJTgzJTkxJUUzJTgzJUJDJUUzJTgzJTg4JUUzJTgxJUFFJUUyJTgwJUE2JnR4dC1jb2xvcj0lMjMyMTIxMjEmdHh0LWZvbnQ9SGlyYWdpbm8lMjBTYW5zJTIwVzYmdHh0LXNpemU9NTYmdHh0LWNsaXA9ZWxsaXBzaXMmdHh0LWFsaWduPWxlZnQlMkN0b3Amcz05YTdhNWM1MDU2MmY0YzgzMWY1MWJjMTk1NGZmMzhkZQ&mark-x=142&mark-y=112&blend64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ3PTYxNiZ0eHQ9JTQwbW9yaW5vdGEmdHh0LWNvbG9yPSUyMzIxMjEyMSZ0eHQtZm9udD1IaXJhZ2lubyUyMFNhbnMlMjBXNiZ0eHQtc2l6ZT0zNiZ0eHQtYWxpZ249bGVmdCUyQ3RvcCZzPTNjMDA2ODNmNDMwOWJjOTNmYzM1ODVmYmQxOGQyMGE5&blend-x=142&blend-y=491&blend-mode=normal&s=cdb143a6a17b8fb844ae8bc4d517eecc)
![bg contain left](https://qiita-user-contents.imgix.net/https%3A%2F%2Fcdn.qiita.com%2Fassets%2Fpublic%2Farticle-ogp-background-9f5428127621718a910c8b63951390ad.png?ixlib=rb-4.0.0&w=1200&mark64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ3PTkxNiZ0eHQ9JUUzJTgwJThDJUU1JThEJTkzJUU3JTkwJTgzJUU3JUFCJUI2JUU2JThBJTgwJUU1JTlCJUEzJUU0JUJEJTkzJUU2JTg4JUE2JUUzJTgxJUFCJUUzJTgxJThBJUUzJTgxJTkxJUUzJTgyJThCJTIyJUUzJTgzJTgwJUUzJTgzJTk2JUUzJTgzJUFCJUUzJTgyJUI5JUUzJTgxJUFFJUU1JThCJTlEJUU2JTk1JTk3JTIyJUUzJTgxJThDJTIyJUU1JTlCJUEzJUU0JUJEJTkzJUU2JTg4JUE2JUUzJTgxJUFFJUU1JThCJTlEJUU2JTk1JTk3JTIyJUUzJTgxJUFCJUU0JUI4JThFJUUzJTgxJTg4JUUzJTgyJThCJUU1JTlCJUEwJUU2JTlFJTlDJUU1JThBJUI5JUU2JTlFJTlDJUUzJTgyJTkyJUU1JUFFJTlBJUU5JTg3JThGJUU1JThDJTk2JUUzJTgxJTk3JUUzJTgxJTlGJUUzJTgxJTg0JUUzJTgwJThEJUUzJTgyJUI5JUUzJTgzJTg2JUUzJTgzJTgzJUUzJTgzJTk3JUUyJTkxJUExJUU1JTlCJTlFJUU1JUI4JUIwJUUzJTgzJUEyJUUzJTgzJTg3JUUzJTgzJUFCJUUzJTgxJUE4JUUyJTgwJUE2JnR4dC1jb2xvcj0lMjMyMTIxMjEmdHh0LWZvbnQ9SGlyYWdpbm8lMjBTYW5zJTIwVzYmdHh0LXNpemU9NTYmdHh0LWNsaXA9ZWxsaXBzaXMmdHh0LWFsaWduPWxlZnQlMkN0b3Amcz1kMzE1OGYyMTJjZGExY2I5MDIwY2VkNzc3ZWU4MDExNQ&mark-x=142&mark-y=112&blend64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ3PTYxNiZ0eHQ9JTQwbW9yaW5vdGEmdHh0LWNvbG9yPSUyMzIxMjEyMSZ0eHQtZm9udD1IaXJhZ2lubyUyMFNhbnMlMjBXNiZ0eHQtc2l6ZT0zNiZ0eHQtYWxpZ249bGVmdCUyQ3RvcCZzPTNjMDA2ODNmNDMwOWJjOTNmYzM1ODVmYmQxOGQyMGE5&blend-x=142&blend-y=491&blend-mode=normal&s=14790bb66ee994e26c9ee8c95a1fb9ba)
![bg contain left](https://qiita-user-contents.imgix.net/https%3A%2F%2Fcdn.qiita.com%2Fassets%2Fpublic%2Farticle-ogp-background-9f5428127621718a910c8b63951390ad.png?ixlib=rb-4.0.0&w=1200&mark64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ3PTkxNiZ0eHQ9aW1wbGljaXQtZmVlZGJhY2slMjBNRiVFMyU4MSVBQiVFMyU4MSU4QSVFMyU4MSU5MSVFMyU4MiU4QkFMUyVFMyU4MSVBRSVFOSVBQiU5OCVFOSU4MCU5RiVFNSU4QyU5NiVFMyU4MSVBQiVFOSU5NiVBMiVFMyU4MSU5NyVFMyU4MSVBNiUyMC0lMjAlRTMlODAlOENGYXN0JTIwTWF0cml4JTIwRmFjdHJpemF0aW9uJTIwZm9yJTIwT25saW5lJTIwUmVjb21tZW5kYXRpb24lMjB3aXRoJTIwSW0lRTIlODAlQTYmdHh0LWNvbG9yPSUyMzIxMjEyMSZ0eHQtZm9udD1IaXJhZ2lubyUyMFNhbnMlMjBXNiZ0eHQtc2l6ZT01NiZ0eHQtY2xpcD1lbGxpcHNpcyZ0eHQtYWxpZ249bGVmdCUyQ3RvcCZzPTgzOTRmNDM5NWRkZDRiMzM3YmRmMDg1YTM4MWIzNjAz&mark-x=142&mark-y=112&blend64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ3PTYxNiZ0eHQ9JTQwbW9yaW5vdGEmdHh0LWNvbG9yPSUyMzIxMjEyMSZ0eHQtZm9udD1IaXJhZ2lubyUyMFNhbnMlMjBXNiZ0eHQtc2l6ZT0zNiZ0eHQtYWxpZ249bGVmdCUyQ3RvcCZzPTNjMDA2ODNmNDMwOWJjOTNmYzM1ODVmYmQxOGQyMGE5&blend-x=142&blend-y=491&blend-mode=normal&s=efccd7d7d9c9027b451e11eef38504db)

---

### 最後に：結局、森田は何がしたいのか??

###### 都市物質代謝? 画像認識? 空間統計? 推薦システム?

```
「自分が学んだ技術を使いたい!」 >= 「課題を解決したい!」
```

#### ＝＞「**自分が興味を持って学んだ技術** を使って課題を解決したい...!」

###### (そんな課題を選びたい...!)

###### (興味の対象：**数学とプログラミング**)

![bg left:40% 100% ](全身写真.jpg)

---

<!-- _class: title -->

# ご清聴ありがとうございました!:smile:

###### 何となくコメントしたい事、ほんの少し疑問に思った事、ぼんやり気になった事などがありましたら、ぜひ残りの時間でカジュアルにお話できれば嬉しいです...！

######
