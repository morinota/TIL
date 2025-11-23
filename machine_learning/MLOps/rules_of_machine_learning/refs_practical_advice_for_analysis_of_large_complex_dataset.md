refs: https://www.unofficialgoogledatascience.com/2016/10/practical-advice-for-analysis-of-large.html

### Practical advice for analysis of large, complex data sets 大規模で複雑なデータセットの分析に関する実用的なアドバイス

October 31, 2016 2016年10月31日

For a number of years, I led the data science team for Google Search logs.
We were often asked to make sense of confusing results, measure new phenomena from logged behavior, validate analyses done by others, and interpret metrics of user behavior. 
Some people seemed to be naturally good at doing this kind of high quality data analysis. 
These engineers and analysts were often described as “careful” and “methodical”. But what do those adjectives actually mean? What actions earn you these labels?
何年にもわたり、私はGoogle検索ログのデータサイエンスチームを率いてきました。私たちはしばしば、混乱した結果を理解し、ログに記録された行動から新しい現象を測定し、他の人が行った分析を検証し、ユーザー行動の指標を解釈するよう求められました。この種の高品質なデータ分析を自然にうまく行う人もいるようです。これらのエンジニアやアナリストはしばしば「注意深い」および「体系的」と表現されました。しかし、これらの形容詞は実際には何を意味するのでしょうか？どのような行動がこれらのラベルを獲得するのでしょうか？

To answer those questions, I put together a document shared Google-wide which I optimistically and simply titled “Good Data Analysis.” To my surprise, this document has been read more than anything else I’ve done at Google over the last eleven years. Even four years after the last major update, I find that there are multiple Googlers with the document open any time I check.
それらの質問に答えるために、私はGoogle全体で共有される文書をまとめ、「良いデータ分析」と楽観的かつ単純に題しました。驚いたことに、この文書は過去11年間にわたって私がGoogleで行った他のどのことよりも多く読まれています。最後の大幅な更新から4年経った今でも、私が確認するたびに複数のGoogle社員がその文書を開いていることがわかります。

Why has this document resonated with so many people over time? I think the main reason is that it’s full of specific actions to take, not just abstract ideals. I’ve seen many engineers and analysts pick up these habits and do high quality work with them. I'd like to share the contents of that document in this blog post.
なぜこの文書は時間の経過とともに多くの人々の共感を呼んだのでしょうか？主な理由は、抽象的な理想だけでなく、具体的な行動が満載されているからだと思います。私は多くのエンジニアやアナリストがこれらの習慣を身につけ、それらを使って高品質な仕事をしているのを見てきました。その文書の内容をこのブログ投稿で共有したいと思います。(ありがたいじゃん!:thinking:)

The advice is organized into three general areas:
このアドバイスは、次の3つの一般的な分野に整理されています。

- Technical: Ideas and techniques for how to manipulate and examine your data. 
  - 技術的: データを操作し、検査するためのアイデアと技術。
- Process: Recommendations on how you approach your data, what questions to ask, and what things to check. 
  - プロセス: データにどのようにアプローチするか、どのような質問をするか、何を確認するかに関する推奨事項。
- Social: How to work with others and communicate about your data and insights. 
- 社会的: 他者と協力し、データや洞察についてコミュニケーションを取る方法.

<!-- ここまで読んだ! -->

## Technical 技術的内容  
### Look at your distributions 分布を確認する

While we typically use summary metrics (means, median, standard deviation, etc.) to communicate about distributions, you should usually be looking at a much richer representation of the distribution. Something like histograms, CDFs, Q-Q plots, etc. will allow you to see if there are important interesting features of the data such as multi-modal behavior or a significant class of outliers that you need to decide how to summarize.
平均、中央値、標準偏差などの要約指標を使用して分布について伝えることが一般的ですが、通常は分布のはるかに豊かな表現を確認する必要があります。ヒストグラム、累積分布関数（CDF）、Q-Qプロットなどのようなものは、多峰性の挙動や要約方法を決定する必要がある重要な外れ値のクラスなど、データの重要な特徴を確認することができます。

### Consider the outliers 外れ値を考慮する

You should look at the outliers in your data. They can be canaries in the coal mine for more fundamental problems with your analysis. It’s fine to exclude them from your data or to lump them together into an “Unusual” category, but you should make sure you know why data ended up in that category. For example, looking at the queries with the lowest click-through rate (CTR) may reveal clicks on elements in the user interface that you are failing to count. Looking at queries with the highest CTR may reveal clicks you should not be counting. On the other hand, some outliers you will never be able to explain so you need to be careful in how much time you devote this.
データの外れ値を確認する必要があります。これらは、分析に関するより根本的な問題のカナリアである可能性があります。データから除外したり、「異常」カテゴリにまとめたりすることは問題ありませんが、そのカテゴリにデータが入った理由を理解していることを確認する必要があります。例えば、クリック率（CTR）が最も低いクエリを調べると、カウントできていないユーザーインターフェイスの要素へのクリックが明らかになる場合があります。CTRが最も高いクエリを調べると、カウントすべきでないクリックが明らかになる場合があります。一方で、説明できない外れ値もあるため、これにどれだけの時間を割くかには注意が必要です。

### Report noise/confidence ノイズ/信頼度の報告

First and foremost, we must be aware that randomness exists and will fool us. If you aren’t careful, you will find patterns in the noise. Every estimator that you produce should have a notion of your confidence in this estimate attached to it. Sometimes this will be more formal and precise (through techniques such as confidence intervals or credible intervals for estimators, and p-values or Bayes factors for conclusions) and other times you will be more loose. For example if a colleague asks you how many queries about frogs we get on Mondays, you might do a quick analysis looking and a couple of Mondays and report “usually something between 10 and 12 million” (not real numbers).
まず第一に、ランダム性が存在し、私たちを騙すことを認識しなければなりません。注意しないと、ノイズの中にパターンを見つけてしまいます。生成するすべての推定値には、この推定に対する信頼度の概念を添付する必要があります。場合によっては、より正式で正確なもの（推定値の信頼区間や信用区間、結論のp値やベイズ因子などの技術を通じて）であり、他の場合はより緩やかになります。例えば、同僚が月曜日にカエルに関するクエリがどれくらいあるか尋ねた場合、数回の月曜日を調べて「通常は1000万から1200万の間くらい」と報告するかもしれません（実際の数字ではありません）。


### Look at examples 例を見てみましょう

Anytime you are producing new analysis code, you need to look at examples of the underlying data and how your code is interpreting those examples. It’s nearly impossible to produce working analysis code of any complexity without this. Your analysis is removing lots of features from the underlying data to produce useful summaries. By looking at the full complexity of individual examples, you can gain confidence that your summarization is reasonable.
新しい分析コードを生成するたびに、基礎となるデータの例とコードがそれらの例をどのように解釈しているかを確認する必要があります。これなしで複雑な分析コードを動作させることはほぼ不可能です。分析は、基礎となるデータから多くの特徴を削除して有用な要約を生成しています。個々の例の完全な複雑さを確認することで、要約が合理的であるという自信を得ることができます。

You should be doing stratified sampling to look at a good sample across the distribution of values so you are not too focussed on the most common cases.
層化サンプリングを行い、値の分布全体にわたる良いサンプルを確認して、最も一般的なケースに過度に焦点を当てないようにする必要があります。

For example, if you are computing Time to Click, make sure you look at examples throughout your distribution, especially the extremes. If you don’t have the right tools/visualization to look at your data, you need to work on those first.
例えば、クリックまでの時間を計算している場合、分布全体、特に極端な例を確認してください。データを確認するための適切なツールや視覚化がない場合は、まずそれらに取り組む必要があります。

### Slice your data データのスライス

Slicing means to separate your data into subgroups and look at the values of your metrics in those subgroups separately. In analysis of web traffic, we commonly slice along dimensions like mobile vs. desktop, browser, locale, etc. If the underlying phenomenon is likely to work differently across subgroups, you must slice the data to see if it is. Even if you do not expect a slice to matter, looking at a few slices for internal consistency gives you greater confidence that you are measuring the right thing. In some cases, a particular slice may have bad data, a broken experience, or in some way be fundamentally different.
**Slicingは、データをサブグループに分離し、これらのサブグループでメトリックの値を別々に確認すること**を意味します。Webトラフィックの分析では、モバイル対デスクトップ、ブラウザ、ロケールなどの次元に沿ってスライスすることが一般的です。基礎となる現象がサブグループごとに異なる可能性がある場合は、そのようであるかどうかを確認するためにデータをスライスする必要があります。**スライスが重要でないと予想される場合でも、内部の一貫性のためにいくつかのスライスを確認することで、正しいものを測定しているという自信が高まります。**場合によっては、特定のスライスに不良データ、壊れたエクスペリエンス、または何らかの方法で根本的に異なるものが存在する可能性があります。

Anytime you are slicing your data to compare two groups (like experiment/control, but even time A vs. time B comparisons), you need to be aware of mix shifts. A mix shift is when the amount of data in a slice is different across the groups you are comparing. Simpson’s paradox and other confusions can result. Generally, if the relative amount of data in a slice is the same across your two groups, you can safely make a comparison.
データをスライスして2つのグループ（実験/制御のようなもの、あるいは時間A対時間Bの比較でさえ）を比較する場合、ミックスシフトに注意する必要があります。ミックスシフトとは、比較しているグループ間でスライス内のデータ量が異なる場合のことです。シンプソンのパラドックスやその他の混乱が生じる可能性があります。一般に、スライス内のデータの相対量が2つのグループ間で同じであれば、安全に比較を行うことができます。

### Consider practical significance 実用的意義を考慮する

With a large volume of data, it can be tempting to focus solely on statistical significance or to hone in on the details of every bit of data. But you need to ask yourself, “Even if it is true that value X is 0.1% more than value Y, does it matter?” This can be especially important if you are unable to understand/categorize part of your data. If you are unable to make sense of some user agents strings in our logs, whether it’s 0.1% of 10% makes a big difference in how much you should investigate those cases.
大量のデータがある場合、統計的有意性のみに焦点を当てたり、すべてのデータの詳細にこだわったりすることは魅力的です。**しかし、「値Xが値Yより0.1%多いというのが本当であっても、それは重要か？」と自問する必要があります**。データの一部を理解/分類できない場合、これは特に重要です。ログ内の一部のユーザーエージェント文字列を理解できない場合、それが10%の0.1%であるかどうかは、そのケースをどれだけ調査すべきかに大きな違いをもたらします。

On the flip side, you sometimes have a small volume of data. Many changes will not look statistically significant but that is different than claiming it is “neutral”. You must ask yourself “How likely is it that there is still a practically significant change”? 
データ量が少ない場合もあります。多くの変更は統計的に有意に見えませんが、それは「中立的」であると主張することとは異なります。「実用的に重要な変化がまだ存在する可能性はどれくらいか？」と自問する必要があります。

### Check for consistency over time 時間における一貫性の確認

One particular slicing you should almost always employ is to slice by units of time (we often use days, but other units may be useful also). This is because many disturbances to underlying data happen as our systems evolve over time. Typically the initial version of a feature or the initial data collection will be checked carefully, but it is not uncommon for something to break along the way.
**ほぼ常に使用すべき特定のスライスは、時間単位でのスライス**です（通常は日を使用しますが、他の単位も有用な場合があります）。これは、基礎となるデータへの多くの妨害が時間の経過とともにシステムが進化するにつれて発生するためです。通常、機能の初期バージョンや初期のデータ収集は注意深く確認されますが、途中で何かが壊れることは珍しくありません。

Just because a particular day or set of days is an outlier does not mean you should discard it. Use the data as a hook to find a causal reason for that day being different before you discard it.
特定の日または一連の日が外れ値であるからといって、それを破棄すべきだというわけではありません。その日が異なる理由を見つけるためのフックとしてデータを使用し、破棄する前に原因を特定してください。

The other benefit of looking at day over day data is it gives you a sense of the variation in the data that would eventually lead to confidence intervals or claims of statistical significance. This should not generally replace rigorous confidence interval calculation, but often with large changes you can see they will be statistically significant just from the day-over-day graphs.
日々のデータを確認するもう一つの利点は、最終的に信頼区間や統計的有意性の主張につながるデータの変動を把握できることです。これは一般に厳密な信頼区間の計算に取って代わるものではありませんが、**大きな変化がある場合、日々のグラフからそれらが統計的に有意であることがわかることがよくあります。**

<!-- ここまで読んだ! -->

## Process プロセス  

### Separate Validation, Description, and Evaluation 分離した検証、説明、および評価

I think about about exploratory data analysis as having 3 interrelated stages:
**探索的データ分析を3つの相互に関連する段階**として考えています：

1. **Validation or Initial Data Analysis**: Do I believe data is self-consistent, that the data was collected correctly, and that data represents what I think it does? 
   検証または初期データ分析：データが自己一貫性を持ち、正しく収集され、私が考えている通りのことを表していると信じているか？ 
   This often goes under the name of “sanity checking”. 
   これはしばしば「サニティ(健全性)チェック」と呼ばれます。 
   For example, if manual testing of a feature was done, can I look at the logs of that manual testing? 
   例えば、機能の手動テストが行われた場合、その手動テストのログを見ることができるか？ 
   For a feature launched on mobile devices, do my logs claim the feature exists on desktops? 
   モバイルデバイスで開始された機能について、私のログはその機能がデスクトップに存在すると主張しているか？

2. **Description**: What’s the objective interpretation of this data? 
   説明：このデータの客観的な解釈は何か？ 
   For example, “Users do fewer queries with 7 words in them?”, 
   例えば、「ユーザーは7語を含むクエリを少なく行うのか？」、 
   “The time page load to click (given there was a click) is larger by 1%”, 
   「クリックがあった場合、ページの読み込みからクリックまでの時間は1%長くなる」、 
   and “A smaller percentage of users go to the next page of results.” 
   そして「次の結果ページに進むユーザーの割合が小さくなる。」

3. **Evaluation**: Given the description, does the data tell us that something good is happening for the user, for Google, for the world? 
   評価：説明を考慮した場合、データはユーザー、Google、世界にとって何か良いことが起こっていることを示しているか？ 
   For example, “Users find results faster” or “The quality of the clicks is higher.” 
   例えば、「ユーザーは結果をより早く見つける」または「クリックの質が高い」。

By separating these phases, you can more easily reach agreement with others. Description should be things that everyone can agree on from the data. Evaluation is likely to have much more debate because you imbuing meaning and value to the data. If you do not separate Description and Evaluation, you are much more likely to only see the interpretation of the data that you are hoping to see. Further, Evaluation tends to be much harder because establishing the normative value of a metric, typically through rigorous comparisons with other features and metrics, takes significant investment.
**これらの段階を分離することで、他の人とより簡単に合意に達することができます**。説明は、データから誰もが同意できるものであるべきです。評価は、データに意味と価値を与えるため、はるかに多くの議論がある可能性があります。**説明と評価を分離しない場合、見たいと望んでいるデータの解釈しか見られない可能性が高くなります。**さらに、評価は通常、他の機能やメトリックとの厳密な比較を通じてメトリックの規範的価値を確立するため、多大な投資が必要になるため、はるかに困難になる傾向があります。

These stages do not progress linearly. As you explore the data, you may jump back and forth between the stages, but at any time you should be clear what stage you are in.
これらの段階は線形に進行しません。データを探索する際に、段階間を行き来することがありますが、**いつでも自分がどの段階にいるかを明確にする必要があります**。

<!-- ここまで読んだ! -->

### Confirm expt/data collection setup 実験/データ収集設定の確認

Before looking at any data, make sure you understand the experiment and data collection setup. Communicating precisely between the experimentalist and the analyst is a big challenge. If you can look at experiment protocols or configurations directly, you should do it. Otherwise, write down your own understanding of the setup and make sure the people responsible for generating the data agree that it’s correct.
データを見る前に、実験とデータ収集の設定を理解していることを確認してください。**実験者とアナリストの間で正確にコミュニケーションを取ることは大きな課題**です。実験プロトコルや構成を直接確認できる場合は、そうするべきです。そうでない場合は、設定に関する自分の理解を書き留め、データの生成に責任を持つ人々がそれが正しいことに同意していることを確認してください。

You may spot unusual or bad configurations or population restrictions (such as valid data only for a particular browser). Anything notable here may help you build and verify theories later. Some things to consider:
あなたは、異常または不良の構成や人口制限（特定のブラウザにのみ有効なデータなど）を見つけるかもしれません。ここで注目すべきことは、後で理論を構築し検証するのに役立つかもしれません。考慮すべきいくつかのこと：

- If it’s a features of a product, try it out yourself. 
  それが製品の機能であれば、自分で試してみてください。
  If you can’t, at least look through screenshots/descriptions of behavior.
  もしできない場合は、少なくともスクリーンショットや動作の説明を確認してください。

- Look for anything unusual about the time range the experiment ran over (holidays, big launches, etc.)
  実験が行われた期間について、何か異常な点（祝日、大きな製品の発売など）がないか探してください。

<!-- ここまで読んだ! -->   

### Check vital signs バイタルサインの確認

Before actually answering the question you are interested in (e.g. “Did users use my awesome new feature?”) you need to check for a lot of other things that may not be related to what you are interested in but may be useful in later analysis or indicate problems in the data. Did the number of users change? Did the right number of affected queries show up in all my subgroups? Did error rates changes? Just as your doctor always checks your height, weight, and blood pressure when you go in, check your data vital signs to potential catch big problems.
This is one important part of the “Validation” stage. 
実際に興味のある質問（例：「ユーザーは私の素晴らしい新機能を使用しましたか？」）に答える前に、興味のあることとは関係ないかもしれませんが、後の分析で役立つ可能性がある、またはデータの問題を示す多くの他のことを確認する必要があります。ユーザー数は変化しましたか？影響を受けたクエリの適切な数がすべてのサブグループに表示されましたか？エラー率は変化しましたか？**医者があなたの身長、体重、血圧を常にチェックするように、データのバイタルサインをチェックして大きな問題を潜在的にキャッチしてください。**

### Standard first, custom second 標準が先、カスタムが後

This is a variant of checking for what shouldn’t change. Especially when looking at new features and new data, it’s tempting to jump right into the metrics that are novel or special for this new feature. But you should always look at standard metrics first, even if you expect them to change. For example, when adding a brand new UI feature to the search page, you should make sure you understand the impact on standard metrics like clicks on results before diving into the special metrics about this new UI feature. You do this because standard metrics are much better validated and more likely to be correct. If your new, custom metrics don’t make sense with your standard metrics, your new, custom metrics are likely wrong.
これは、**変化すべきでないものを確認する**バリアントです。特に新しい機能や新しいデータを見るとき、この新しい機能にとって新規または特別なメトリックにすぐに飛び込むのは魅力的です。しかし、たとえそれらが変化すると予想される場合でも、**常に標準のメトリックを最初に確認する必要があります**。例えば、検索ページにまったく新しいUI機能を追加する場合、この新しいUI機能に関する特別なメトリックに飛び込む前に、結果のクリックなどの標準的なメトリックへの影響を理解していることを確認する必要があります。これを行う理由は、標準的なメトリックの方がはるかに検証されており、正しい可能性が高いためです。新しいカスタムメトリックが標準メトリックと一致しない場合、新しいカスタムメトリックは間違っている可能性が高いです。

<!-- ここまで読んだ! -->

### Measure twice, or more 二度、あるいはそれ以上測る

Especially if you are trying to capture a new phenomenon, try to measure the same underlying thing in multiple ways. Then, check to see if these multiple measurements are consistent. By using multiple measurements, you can identify bugs in measurement or logging code, unexpected features of the underlying data, or filtering steps that are important. It’s even better if you can use different data sources for the measurements.
**特に新しい現象を捉えようとしている場合は、同じ基礎となるものを複数の方法で測定してみてください。そして、これらの複数の測定が一貫しているかどうかを確認してください**。複数の測定を使用することで、測定やログ記録コードのバグ、基礎となるデータの予期しない特徴、または重要なフィルタリングステップを特定できます。測定に異なるデータソースを使用できる場合はさらに良いです。

### Check for reproducibility 再現性の確認

Both slicing and consistency over time are particular examples of checking for reproducibility. If a phenomenon is important and meaningful, you should see it across different user populations and time. But reproducibility means more than this as well. If you are building models of the data, you want those models to be stable across small perturbations in the underlying data. Using different time ranges or random sub-samples of your data will tell you how reliable/reproducible this model is. If it is not reproducible, you are probably not capturing something fundamental about the underlying process that produced this data.
**スライシングと時間にわたる一貫性の両方は、再現性を確認する特定の例**です。現象が重要で意味のあるものであれば、異なるユーザポピュレーションと時間にわたってそれを見ることができます。しかし、再現性はこれ以上の意味も持ちます。データのモデルを構築している場合、基礎となるデータの小さな摂動にわたってそのモデルが安定していることを望んでいます。データの異なる時間範囲やランダムなサブサンプルを使用すると、このモデルがどれほど信頼性/再現性があるかがわかります。再現性がない場合、おそらくこのデータを生成した基礎となるプロセスについて根本的な何かを捉えていない可能性があります。

<!-- ここまで読んだ! -->

### Check for consistency with past measurements 過去の測定との整合性の確認

Often you will be calculating a metric that is similar to things that have been counted in the past. You should compare your metrics to metrics reported in the past, even if these measurements are on different user populations. For example, if you are looking at measuring search volume on a special population and you measure a much larger number than the commonly accepted number, then you need to investigate. Your number may be right on this population, but now you have to do more work to validate this. Are you measuring the same thing? Is there a rational reason to believe these populations are different? You do not need to get exact agreement, but you should be in the same ballpark. If you are not, assume that you are wrong until you can fully convince yourself. Most surprising data will turn out to be a error, not a fabulous new insight.
New metrics should be applied to old data/features first
しばしば、過去にカウントされたものと類似したメトリックを計算することがあります。これらの測定が異なるユーザポピュレーションであっても、過去に報告されたメトリックと比較する必要があります。例えば、特定のポピュレーションでの検索ボリュームを測定しており、一般に受け入れられている数よりもはるかに大きな数を測定した場合、調査する必要があります。そのポピュレーションではあなたの数値が正しいかもしれませんが、これを検証するためにさらに多くの作業を行う必要があります。同じことを測定していますか？これらのポピュレーションが異なると信じる合理的な理由はありますか？**正確な一致を得る必要はありませんが、同じ範囲内にいるべきです。そうでない場合は、自分自身を完全に納得させるまで、自分が間違っていると仮定してください。ほとんどの驚くべきデータは、素晴らしい新しい洞察ではなく、エラーであることが判明**します。

If you gather completely new data and try to learn something new, you won’t know if you got it right. When you gather a new kind of data, you should first apply this data to a known feature or data. For example, if you have a new metric for user satisfaction, you should make sure it tells you your best features help satisfaction. Doing this provides validation for when you then go to learn something new.
もし完全に新しいデータを収集して新しいことを学ぼうとする場合、正しく取得したかどうかわかりません。**新しい種類のデータを収集する場合、最初にこのデータを既知の機能またはデータに適用する必要があります**。例えば、ユーザー満足度の新しいメトリックがある場合、最高の機能が満足度を向上させることを確認する必要があります。これを行うことで、新しいことを学ぶときの検証が提供されます。

<!-- ここまで読んだ! -->

### Make hypotheses and look for evidence 仮説を立て、証拠を探す

Typically, exploratory data analysis for a complex problem is iterative. You will discover anomalies, trends, or other features of the data. Naturally, you will make hypotheses to explain this data. It’s essential that you don’t just make a hypothesis and proclaim it to be true. Look for evidence (inside or outside the data) to confirm/deny this theory. For example, If you believe an anomaly is due to the launch of some other feature or a holiday in Katmandu, make sure that the population the feature launched to is the only one affected by the anomaly. Alternatively, make sure that the magnitude of the change is consistent with the expectations of the launch.
通常、複雑な問題の探索的データ分析は反復的です。データの異常、傾向、またはその他の特徴を発見します。自然に、このデータを説明するための仮説を立てます。**仮説を立ててそれが真実であると宣言するだけではなく、証拠（データ内外）を探してこの理論を確認/否定することが不可欠**です。例えば、ある異常が他の機能の開始やカトマンズの休日によるものであると信じている場合、その機能が開始されたポピュレーションだけが異常の影響を受けていることを確認してください。あるいは、変化の大きさが開始の期待と一致していることを確認してください。


Good data analysis will have a story to tell. To make sure it’s the right story, you need to tell the story to yourself, predict what else you should see in the data if that hypothesis is true, then look for evidence that it’s wrong. One way of doing this is to ask yourself, “What experiments would I run that would validate/invalidate the story I am telling?” Even if you don’t/can’t do these experiments, it may give you ideas on how to validate with the data that you do have.
優れたデータ分析には語るべきストーリーがあります。正しいストーリーであることを確認するために、自分自身にストーリーを伝え、その仮説が真実である場合にデータで他に何を見るべきかを予測し、それが間違っているという証拠を探す必要があります。**これを行う一つの方法は、「自分が伝えているストーリーを検証/無効化するためにどのような実験を行うか？」と自問すること**です。これらの実験を行わない/できない場合でも、持っているデータで検証する方法についてのアイデアを得ることができます。

The good news is that these hypotheses and possible experiments may lead to new lines of inquiry that transcend trying to learn about any particular feature or data. You then enter the realm of understanding not just this data, but deriving new metrics and techniques for all kinds of future analyses.
良いニュースは、これらの仮説と可能な実験が、特定の機能やデータについて学ぼうとすることを超越した新しい調査の道につながる可能性があることです。そうすると、単にこのデータを理解するだけでなく、あらゆる種類の将来の分析のための新しいメトリックと技術を導き出す領域に入ります。

<!-- ここまで読んだ! -->

### Exploratory analysis benefits from end to end iteration
### 探索的分析はエンドツーエンドの反復から利益を得る

When doing exploratory analysis, you should strive to get as many iterations of the whole analysis as possible. Typically you will have multiple steps of signal gathering, processing, modelling, etc. If you spend too long to get the very first stage of your initial signals perfect you are missing out on opportunities to get more iterations in the same amount of time. Further, when you finally look at your data at the end, you may make discoveries that change your direction. Therefore, your initial focus should not be on perfection but on getting something reasonable all the way through. Leave notes for yourself and acknowledge things like filtering steps and data records that you can’t parse/understand, but trying to get rid of all of them is a waste of time at the beginning of exploratory analysis.
探索的分析を行う際には、可能な限り多くの反復を全体の分析で取得するよう努めるべきです。通常、信号収集、処理、モデリングなどの複数のステップがあります。最初の信号の非常に最初の段階を完璧にするためにあまりにも長く費やすと、同じ時間内により多くの反復を得る機会を逃しています。さらに、最終的にデータを確認すると、方向性を変える発見をすることがあります。したがって、**最初の焦点は完璧さではなく、合理的なものを最後まで取得することにあるべき**です。自分自身へのメモを残し、フィルタリングステップや解析/理解できないデータレコードなどのことを認識してください。ただし、それらすべてを取り除こうとすることは、探索的分析の初めには時間の無駄です。

<!-- ここまで読んだ! -->

## Social 社会

### Data analysis starts with questions, not data or a technique　データ分析はデータや技術ではなく、質問から始まる。

There’s always a reason that you are doing some analysis. If you take the time to formulate your needs as questions or hypotheses, it will go a long way towards making sure that you are gathering the data you should be gathering and that you are thinking about the possible gaps in the data. Of course, the questions you ask can and should evolve as you look at the data. But analysis without a question will end up aimless.
分析を行う理由は常にあります。ニーズを質問や仮説として定式化する時間を取ると、収集すべきデータを収集していること、データの可能なギャップについて考えていることを確認するのに大いに役立ちます。もちろん、あなたが尋ねる質問はデータを見ながら進化することができ、そうすべきです。**しかし、質問なしの分析は目的がなく終わってしまいます。**

Further, you have to avoid the trap of finding some favorite technique and then only finding the parts of problems that this technique works on. Again, making sure you are clear what the questions are will help you avoid this.
さらに、この技術が機能する問題の一部のみを見つけるというお気に入りの技術を見つける罠を避ける必要があります。**再度、質問が何であるかを明確にする**ことで、これを回避するのに役立ちます。

<!-- ここまで読んだ! -->

### Acknowledge and count your filtering フィルタリングの認識とカウント

Almost every large data analysis starts by filtering the data in various stages. Maybe you want to consider only US users, or web searches, or searches with a result click. Whatever the case, you must
ほとんどの大規模なデータ分析は、さまざまな段階でデータをフィルタリングすることから始まります。おそらく、米国のユーザー、ウェブ検索、または結果のクリックがある検索のみを考慮したいでしょう。いずれにせよ、あなたは次のことを行う必要があります：

- Acknowledge and clearly specify what filtering you are doing
  - あなたが行っているフィルタリングを認識し、明確に指定してください。
- Count how much is being filtered at each of your steps
  - 各ステップでどれだけフィルタリングされているかをカウントしてください。

Often the best way to do the latter is to actually compute all your metrics even for the population you are excluding. Then you can look at that data to answer questions like “What fraction of queries did my filtering remove?”
後者を行う最良の方法は、実際に除外しているポピュレーションのすべてのメトリックを計算することです。そうすれば、そのデータを見て、「フィルタリングによってクエリの何分の1が削除されたか？」などの質問に答えることができます。

Further, looking at examples of what is filtered is also essential for filtering steps that are novel for your analysis. It’s easy to accidentally include some “good” data when you make a simple rule of data to exclude.
さらに、フィルタリングされる例を見ることも、分析にとって新しいフィルタリングステップにとって不可欠です。除外するデータの単純なルールを作成するときに、誤って「良い」データを含めることは簡単です。

### Ratios should have clear numerator and denominators 比率は明確な分子と分母を持つべきである

Many interesting metrics are ratios of underlying measures. Unfortunately, there is often ambiguity of what your ratio is. For example, if I say click-through rate of a site on search results, is it:
**多くの興味深いメトリックは、基礎となる測定値の比率**です。残念ながら、あなたの比率が何であるかにはしばしば曖昧さがあります。例えば、検索結果におけるサイトのクリック率と言った場合、それは次のどれですか：

- “# clicks on site’ / ‘# results for that site” 
  - 「そのサイトのクリック数」/「そのサイトの結果数」
- ‘# search result pages with clicks to that site’ / ‘# search result pages with that site shown’
  - 「そのサイトへのクリックがある検索結果ページ数」/「そのサイトが表示されている検索結果ページ数」

When you communicate results, you must be clear about this. Otherwise your audience (and you!) will have trouble comparing to past results and interpreting a metric correctly.
**結果を伝えるときは、これについて明確にする必要があります**。そうしないと、あなたの聴衆（そしてあなた自身！）は過去の結果と比較したり、メトリックを正しく解釈したりするのに苦労します。

<!-- ここまで読んだ! -->

### Educate your consumers 消費者を教育する

You will often be presenting your analysis and results to people who are not data experts. Part of your job is to educate them on how to interpret and draw conclusions from your data. This runs the gamut from making sure they understand confidence intervals to why certain measurements are unreliable in your domain to what typical effect sizes are for “good” and “bad” changes to understanding population bias effects.
あなたはしばしば、データの専門家ではない人々にあなたの分析と結果を提示することになります。**あなたの仕事の一部は、彼らにあなたのデータからどのように解釈し、結論を導き出すかを教育すること**です。これは、信頼区間を理解していることから、あなたのドメインで特定の測定が信頼できない理由、「良い」および「悪い」変化の典型的な効果サイズ、人口バイアス効果の理解まで、幅広く及びます。

This is especially important when your data has a high risk of being misinterpreted or selectively cited. You are responsible for providing the context and a full picture of the data and not just the number a consumer asked for.
これは、あなたのデータが誤解されるリスクが高い場合や選択的に引用される場合に特に重要です。**あなたは、消費者が求めた数値だけでなく、データのコンテキストと全体像を提供する責任があります**。

<!-- ここまで読んだ! -->

### Be both skeptic and champion 懐疑的でありながら擁護者であれ

As you work with data, you must be both the champion of the insights you are gaining as well as a skeptic. You will hopefully find some interesting phenomena in the data you look at. When you have an interesting phenomenon you should ask both “What other data could I gather to show how awesome this is?” and “What could I find that would invalidate this?”. Especially in cases where you are doing analysis for someone who really wants a particular answer (e.g. “My feature is awesome”) you are going to have to play the skeptic to avoid making errors.
データを扱う際には、得られる洞察の擁護者であると同時に懐疑的でなければなりません。あなたが見るデータでいくつかの興味深い現象を見つけることを願っています。**興味深い現象がある場合、「この素晴らしさを示すためにどのような他のデータを収集できるか？」と「これを無効にする可能性のあるものは何か？」の両方を尋ねるべき**です。特に、特定の答え（例：「私の機能は素晴らしい」）を本当に望んでいる人のために分析を行っている場合、エラーを避けるために懐疑的な役割を果たす必要があります。

<!-- ここまで読んだ! -->

### Share with peers first, external consumers second　まずは仲間と共有し、次に外部の消費者と共有する

A skilled peer reviewer can provide qualitatively different feedback and sanity-checking than the consumers of your data can, especially since consumers generally have an outcome they want to get. Ideally, you will have a peer that knows something about the data you are looking at, but even a peer with just experience looking at data in general is extremely valuable. The previous points suggested some ways to get yourself to do the right kinds of sanity checking and validation. But sharing with a peer is one of the best ways to force yourself to do all these things. Peers are useful at multiple points through the analysis. Early on you can find out about gotchas your peer knows about, suggestions for things to measure, and past research in this area. Near the end, peers are very good at pointing out oddities, inconsistencies, or other confusions.
熟練したピアレビュアーは、あなたのデータの消費者が提供できるものとは質的に異なるフィードバックとサニティチェックを提供できます。特に、消費者は一般的に得たい結果を持っているためです。理想的には、あなたが見ているデータについて何かを知っている仲間がいるでしょうが、一般的にデータを見る経験だけを持つ仲間でさえ非常に価値があります。前のポイントでは、適切な種類のサニティチェックと検証を行うためのいくつかの方法を提案しました。**しかし、仲間と共有することは、これらすべてのことを強制的に行うための最良の方法の一つです。**仲間は分析全体を通じて複数のポイントで役立ちます。初期段階では、仲間が知っているゴッチャ、測定するための提案、およびこの分野での過去の研究について知ることができます。終わり近くでは、仲間は奇妙な点、不整合、またはその他の混乱を指摘するのに非常に優れています。

<!-- ここまで読んだ! -->


### Expect and accept ignorance and mistakes 無知と間違いを期待し、受け入れる

There are many limits to what we can learn from data. Nate Silver makes a strong case in The Signal and the Noise that only by admitting the limits of our certainty can we make advances in better prediction. Admitting ignorance is a strength but it is not usually immediately rewarded. It feels bad at the time, but will ultimately earn you respect with colleagues and leaders who are data-wise. It feels even worse when you make a mistake and discover it later (or even too late!), but proactively owning up to your mistakes will translate into credibility. Credibility is the key social value for any data scientist.
データから学べることには多くの限界があります。Nate Silverは『The Signal and the Noise』で、確実性の限界を認めることによってのみ、より良い予測で進歩を遂げることができるという強力な主張をしています。**無知を認めることは強みですが、通常はすぐに報われるわけではありません。その時点では気分が悪く感じますが、最終的にはデータに精通した同僚やリーダーから尊敬を得るでしょう**。後で（または遅すぎて！）間違いを犯して発見したときはさらに悪く感じますが、**自分の間違いを積極的に認めることで信頼性につながります。信頼性は、あらゆるデータサイエンティストにとっての重要な社会的価値です**。

<!-- ここまで読んだ! -->

## Closing thoughts 結論

No short list of advice can be complete even when we break through the barrier of the Top 10 List format (for those of you who weren’t counting, there are 24 here). As you apply these ideas to real problems, you’ll find the habits and techniques that are most important in your domain, the tools that help you do those analyses quickly and correctly, and the advice you wish were on this list. Make sure you share what you’ve learned so we can all be better data scientists.
このアドバイスの短いリストは、トップ10リスト形式の壁を突破しても完全ではありません（数えていなかった人のために、ここには24個あります）。これらのアイデアを実際の問題に適用すると、あなたのドメインで最も重要な習慣と技術、それらの分析を迅速かつ正確に行うのに役立つツール、そしてこのリストに載っていてほしいアドバイスが見つかります。**あなたが学んだことを共有して、私たち全員がより良いデータサイエンティストになれるようにしてください**。

<!-- ここまで読んだ! -->
