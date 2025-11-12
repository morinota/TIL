refs: https://www.unofficialgoogledatascience.com/2016/10/practical-advice-for-analysis-of-large.html


### Search This Blog このブログを検索



# The Unofficial Google Data Science Blog 非公式Googleデータサイエンスブログ

- Home ホーム
- More… もっと…
- About this blog このブログについて
- Home ホーム
- About this blog このブログについて
- Home ホーム
- About this blog このブログについて



### Practical advice for analysis of large, complex data sets 大規模で複雑なデータセットの分析に関する実用的なアドバイス

- Get link リンクを取得
- Facebook
- X
- Pinterest
- Email
- Other Apps その他のアプリ
Get link リンクを取得
Get link リンクを取得
Facebook
Facebook
X
X
Pinterest
Pinterest
Email
Email
Other Apps その他のアプリ
October 31, 2016 2016年10月31日
- Technical: Ideas and techniques for how to manipulate and examine your data. 
- 技術的: データを操作し、検査するためのアイデアと技術。
- Process: Recommendations on how you approach your data, what questions to ask, and what things to check. 
- プロセス: データにどのようにアプローチするか、どのような質問をするか、何を確認するかに関する推奨事項。
- Social: How to work with others and communicate about your data and insights. 
- 社会的: 他者と協力し、データや洞察についてコミュニケーションを取る方法。



## Technical 技術的内容  
### Look at your distributions 分布を確認する



### Consider the outliers 外れ値を考慮する



### Report noise/confidence ノイズ/信頼度の報告



### Look at examples 例を見てみましょう



### Slice your data データのスライス




### Consider practical significance 実用的意義を考慮する



### Check for consistency over time 時間における一貫性の確認



## Process プロセス  
### Separate Validation, Description, and Evaluation 分離した検証、説明、および評価

1. Validation or Initial Data Analysis: Do I believe data is self-consistent, that the data was collected correctly, and that data represents what I think it does? 
   検証または初期データ分析：データが自己一貫性を持ち、正しく収集され、私が考えている通りのことを表していると信じているか？ 
   This often goes under the name of “sanity checking”. 
   これはしばしば「サニティチェック」と呼ばれます。 
   For example, if manual testing of a feature was done, can I look at the logs of that manual testing? 
   例えば、機能の手動テストが行われた場合、その手動テストのログを見ることができるか？ 
   For a feature launched on mobile devices, do my logs claim the feature exists on desktops? 
   モバイルデバイスで開始された機能について、私のログはその機能がデスクトップに存在すると主張しているか？

2. Description: What’s the objective interpretation of this data? 
   説明：このデータの客観的な解釈は何か？ 
   For example, “Users do fewer queries with 7 words in them?”, 
   例えば、「ユーザーは7語を含むクエリを少なく行うのか？」、 
   “The time page load to click (given there was a click) is larger by 1%”, 
   「クリックがあった場合、ページの読み込みからクリックまでの時間は1%長くなる」、 
   and “A smaller percentage of users go to the next page of results.” 
   そして「次の結果ページに進むユーザーの割合が小さくなる。」

3. Evaluation: Given the description, does the data tell us that something good is happening for the user, for Google, for the world? 
   評価：説明を考慮した場合、データはユーザー、Google、世界にとって何か良いことが起こっていることを示しているか？ 
   For example, “Users find results faster” or “The quality of the clicks is higher.” 
   例えば、「ユーザーは結果をより早く見つける」または「クリックの質が高い」。



### Confirm expt/data collection setup 実験/データ収集設定の確認

- If it’s a features of a product, try it out yourself. 
- それが製品の機能であれば、自分で試してみてください。
- If you can’t, at least look through screenshots/descriptions of behavior.
- もしできない場合は、少なくともスクリーンショットや動作の説明を確認してください。

- Look for anything unusual about the time range the experiment ran over (holidays, big launches, etc.)
- 実験が行われた期間について、何か異常な点（祝日、大きな製品の発売など）がないか探してください。



### Check vital signs バイタルサインの確認



### Standard first, custom second 標準が先、カスタムが後




### Measure twice, or more 二度、あるいはそれ以上測る



### Check for reproducibility 再現性の確認



### Check for consistency with past measurements 過去の測定との整合性の確認



### Make hypotheses and look for evidence 仮説を立て、証拠を探す




### Exploratory analysis benefits from end to end iteration
### 探索的分析はエンドツーエンドの反復から利益を得る



## Social 社会

### Data analysis starts with questions, not data or a technique
データ分析はデータや技術ではなく、質問から始まる。



### Acknowledge and count your filtering フィルタリングの認識とカウント

- Acknowledge and clearly specify what filtering you are doing
- あなたが行っているフィルタリングを認識し、明確に指定してください。

- Count how much is being filtered at each of your steps
- 各ステップでどれだけフィルタリングされているかをカウントしてください。



### Ratios should have clear numerator and denominators 比率は明確な分子と分母を持つべきである

- “# clicks on site’ / ‘# results for that site” 
- ‘# search result pages with clicks to that site’ / ‘# search result pages with that site shown’



### Educate your consumers 消費者を教育する



### Be both skeptic and champion 懐疑的でありながら擁護者であれ



### Share with peers first, external consumers second
### まずは仲間と共有し、次に外部の消費者と共有する



### Expect and accept ignorance and mistakes 無知と間違いを期待し、受け入れる




## Closing thoughts 結論

- Get link
- Facebook
- X
- Pinterest
- Email
- Other Apps
リンクを取得
リンクを取得
Facebook
Facebook
X
X
Pinterest
Pinterest
Email
Email
Other Apps
Other Apps



### Comments コメント

1. MattNovember 4, 2016 at 7:11PMgreat advice.  
1. Matt 2016年11月4日 19:11 素晴らしいアドバイスです。

2. ElleryNovember 6, 2016 at 5:38AMThank you for this great actionable items. Just to be curious, is that possible to share that document, or it is the actual document here? By the way, the share icon does not work. Please take a look. I am using Google Chrome~~ :D  
2. Ellery 2016年11月6日 5:38 この素晴らしい実行可能な項目をありがとうございます。ちょっと気になったのですが、その文書を共有することは可能ですか、それともここにあるのが実際の文書ですか？ちなみに、共有アイコンが機能していません。確認してください。私はGoogle Chromeを使用しています~~ :D

3. Amir NajmiNovember 6, 2016 at 10:33AMGlad you liked it. This post contains the content of that internal document without reference to Google-internal technology and systems.  
3. Amir Najmi 2016年11月6日 10:33 あなたが気に入ってくれて嬉しいです。この投稿には、Google内部の技術やシステムに言及せずに、その内部文書の内容が含まれています。

4. prasadNovember 9, 2016 at 12:26PMSuch a good advice. I would definitely share it accross  
4. prasad 2016年11月9日 12:26 こんなに良いアドバイスはありません。私は間違いなくそれを広めます。

5. DeepakApril 25, 2017 at 10:34PMAmazing Article. Thanks a ton.. very well put.  
5. Deepak 2017年4月25日 22:34 素晴らしい記事です。ありがとうございます.. とてもよくまとめられています。

6. UnknownNovember 10, 2017 at 7:08PMSpot on and excellent  
6. Unknown 2017年11月10日 19:08 的を射ていて素晴らしいです。



#### Post a Comment コメントを投稿する



### Archive アーカイブ
- March 20251
- April 20241
- July 20231
- December 20211
- April 20211
- November 20201
- July 20201
- December 20191
- August 20191
- April 20191
1
1
1
1
1
1
1
1
1
1
- July 20181
- March 20181
- January 20181
- October 20171
- July 20171
- April 20171
- March 20171
- January 20171
- October 20161
- September 20161
- August 20161
- July 20161
- June 20161
- May 20161
- March 20161
- February 20161
- January 20161
- December 20151
- November 20152
- October 20152
- September 20152
- August 20152
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
2
2
2
2
Show more
Show less
