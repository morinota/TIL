refs: https://arxiv.org/html/2406.07932v2


Back to arXiv
Back to arXiv
This is experimental HTML to improve accessibility. 
これはアクセシビリティを改善するための実験的なHTMLです。
We invite you to report rendering errors. 
レンダリングエラーを報告することをお勧めします。
Use Alt+Y to toggle on accessible reporting links and Alt+Shift+Y to toggle off. 
Alt+Yを使用してアクセシブルな報告リンクを切り替え、Alt+Shift+Yを使用してオフにします。
Learn more about this project and help improve conversions. 
このプロジェクトについて詳しく学び、コンバージョンの改善を手伝ってください。
Use Alt+Y to toggle on accessible reporting links and Alt+Shift+Y to toggle off. 
Alt+Yを使用してアクセシブルな報告リンクを切り替え、Alt+Shift+Yを使用してオフにします。



## Table of Contents 目次
1. Abstract 要約
2. 1Introduction はじめに
3. 2Related work 関連研究
4. 3Counterfactual watch time 反実仮想視聴時間
   3.1Definition of counterfactual watch time 反実仮想視聴時間の定義
   3.2The existence of counterfactual watch time 反実仮想視聴時間の存在
      3.2.1Evidence 1: repeated playing 証拠1: 繰り返し再生
      3.2.2Evidence 2: bimodal distribution 証拠2: 二峰性分布
      3.2.3Explanation from counterfactual watch time 反実仮想視聴時間からの説明
   3.3An economic view of user watching ユーザ視聴の経済的視点
   3.4Limitation of existing methods 既存手法の限界
5. 4Our approach 私たちのアプローチ
   4.1Cost-based transform function コストベースの変換関数
   4.2Counterfactual likelihood function 反実仮想尤度関数
      4.2.1Formulation of the counterfactual likelihood function 反実仮想尤度関数の定式化
      4.2.2Parameterize and optimize the likelihood function 尤度関数のパラメータ化と最適化
   4.3Online inference オンライン推論
6. 5Experiments and Results 実験と結果
   5.1Experimental setting 実験設定
      5.1.1Datasets データセット
      5.1.2Evaluation 評価
      5.1.3Baselines ベースライン
   5.2Overall performance 全体的な性能
   5.3Effectiveness on duration debiasing 時間バイアスの除去に対する効果
   5.4Comparison with more baselines より多くのベースラインとの比較
   5.5Ablation study アブレーションスタディ
   5.6Online A/B Testing オンラインA/Bテスト
7. 6Conclusion 結論
8. AProof of theorem 1 定理1の証明
9. BDetailed Experimental Setting 詳細な実験設定
10. CThe Unbiasedness of Interest Labels 興味ラベルの無偏性
11. DMore Experimental results さらなる実験結果
    D.1Parameter sensitivity パラメータ感度
    D.2Better fit to the true watch time distribution 真の視聴時間分布への適合性
12. References 参考文献
```

```md
# Counteracting Duration Bias in Video Recommendation via Counterfactual Watch Time
動画推薦における時間バイアスの対抗：反実仮想視聴時間を用いて
Haiyuan Zhao
School of Information
Renmin University of China
Beijing
China
haiyuanzhao@ruc.edu.cn

Guohao Cai
Huawei Noah’s Ark Lab
Shenzhen
China
caiguohao1@huawei.com

Jieming Zhu
Huawei Noah’s Ark Lab
Shenzhen
China
jiemingzhu@ieee.org

Zhenhua Dong
Huawei Noah’s Ark Lab
Shenzhen
China
dongzhenhua@huawei.com

Jun Xu
Gaoling School of Artificial Intelligence
Renmin University of China
Beijing
China
junxu@ruc.edu.cn

and

Ji-Rong Wen
Gaoling School of Artificial Intelligence
Renmin University of China
Beijing
China
jrwen@ruc.edu.cn

In video recommendation, an ongoing effort is to satisfy users’ personalized information needs by leveraging their logged watch time. 
動画推薦において、ユーザのログされた視聴時間を活用して、ユーザの個別の情報ニーズを満たすための継続的な努力が行われています。

However, watch time prediction suffers from duration bias, hindering its ability to reflect users’ interests accurately. 
しかし、視聴時間の予測は時間バイアスの影響を受け、ユーザの興味を正確に反映する能力を妨げています。

Existing label-correction approaches attempt to uncover user interests through grouping and normalizing observed watch time according to video duration. 
既存のラベル修正アプローチは、動画の長さに応じて観察された視聴時間をグループ化し、正規化することでユーザの興味を明らかにしようとしています。

Although effective to some extent, we found that these approaches regard completely played records (i.e., a user watches the entire video) as equally high interest, which deviates from what we observed on real datasets: 
ある程度効果的ではありますが、これらのアプローチは完全に再生された記録（すなわち、ユーザが動画全体を視聴すること）を同等に高い興味と見なすことが分かりましたが、これは実際のデータセットで観察されたものとは異なります。

users have varied explicit feedback proportion when completely playing videos. 
ユーザは動画を完全に再生する際に、明示的なフィードバックの割合が異なります。

In this paper, we introduce the counterfactual watch time (CWT), the potential watch time a user would spend on the video if its duration is sufficiently long. 
本論文では、反実仮想視聴時間（CWT）を導入します。これは、動画の長さが十分に長い場合にユーザがその動画に費やす可能性のある視聴時間です。

Analysis shows that the duration bias is caused by the truncation of CWT due to the video duration limitation, which usually occurs on those completely played records. 
分析の結果、時間バイアスは動画の長さの制限によるCWTの切り捨てによって引き起こされることが示され、これは通常、完全に再生された記録に発生します。

Besides, a Counterfactual Watch Model (CWM) is proposed, revealing that CWT equals the time users get the maximum benefit from video recommender systems. 
さらに、反実仮想視聴モデル（CWM）が提案され、CWTはユーザが動画推薦システムから最大の利益を得る時間に等しいことが明らかになります。

Moreover, a cost-based transform function is defined to transform the CWT into the estimation of user interest, and the model can be learned by optimizing a counterfactual likelihood function defined over observed user watch times. 
さらに、CWTをユーザの興味の推定に変換するためのコストベースの変換関数が定義され、モデルは観察されたユーザの視聴時間に基づいて定義された反実仮想尤度関数を最適化することで学習できます。

Extensive experiments on three real video recommendation datasets and online A/B testing demonstrated that CWM effectively enhanced video recommendation accuracy and counteracted the duration bias. 
3つの実際の動画推薦データセットとオンラインA/Bテストにおける広範な実験により、CWMが動画推薦の精度を効果的に向上させ、時間バイアスに対抗したことが示されました。



## 1.Introduction 1. はじめに

The rising of video content platforms have attracted billions of users and become more frequent in the daily use of users nowadays(Covington etal.,2016a; Davidson etal.,2010; Liu etal.,2019,2021). 
動画コンテンツプラットフォームの台頭は、数十億のユーザーを惹きつけ、現在ではユーザーの日常的な利用がより頻繁になっています（Covington etal.,2016a; Davidson etal.,2010; Liu etal.,2019,2021）。 
To satisfy users’ information needs and enhance their engagement, developing accurate and personalized video recommender systems is critical. 
ユーザーの情報ニーズを満たし、エンゲージメントを高めるためには、正確でパーソナライズされた動画レコメンダーシステムの開発が重要です。 
It is essential to incorporate various feedback signals that reflect users’ interests to achieve this goal. 
この目標を達成するためには、ユーザーの興味を反映するさまざまなフィードバック信号を組み込むことが不可欠です。 
In the video scenario, watch time has been commonly employed as an indicator of user interest and can be leveraged to enhance the accuracy of video recommender systems(Covington etal.,2016a; Cai etal.,2023). 
動画のシナリオでは、視聴時間がユーザーの興味の指標として一般的に使用されており、動画レコメンダーシステムの精度を向上させるために活用できます（Covington etal.,2016a; Cai etal.,2023）。 

Like other implicit feedback signals (e.g., user click) in recommender systems, directly inferring the user interest labels from the watch time is also hurt by the bias problem. 
レコメンダーシステムにおける他の暗黙的フィードバック信号（例：ユーザークリック）と同様に、視聴時間からユーザーの興味ラベルを直接推測することもバイアス問題に悩まされています。 
One crucial bias is duration bias; that is, users’ watch time is not only related to their interest but also affected by the duration (length) of the video(Zhan etal.,2022; Zheng etal.,2022). 
重要なバイアスの一つは、持続時間バイアスです。つまり、ユーザーの視聴時間は彼らの興味に関連するだけでなく、動画の持続時間（長さ）にも影響されます（Zhan etal.,2022; Zheng etal.,2022）。 
It has been observed that users naturally tend to watch for more time on longer videos, making watch time no longer a faithful reflection of the user’s interest. 
ユーザーは長い動画をより多くの時間視聴する傾向があることが観察されており、視聴時間はもはやユーザーの興味を忠実に反映するものではなくなっています。 

Existing approaches like Play Completion Rate (PCR), Watch Time Gain (WTG)(Zhan etal.,2022)and Quantile-based method (D2Q)(Zheng etal.,2022)regard duration bias as a problem of inconsistent watch time scales caused by the video duration. 
Play Completion Rate (PCR)、Watch Time Gain (WTG)（Zhan etal.,2022）、およびQuantile-based method (D2Q)（Zheng etal.,2022）などの既存のアプローチは、持続時間バイアスを動画の持続時間によって引き起こされる不一致な視聴時間スケールの問題と見なしています。 
The longer the video duration, the larger the watch time scale, resulting in a longer average watch time. 
動画の持続時間が長くなるほど、視聴時間スケールは大きくなり、平均視聴時間が長くなります。 
Therefore, these methods group and normalize the watch time according to the video duration, which keeps the watch time corresponding to different video duration consistent in scale. 
したがって、これらの方法は動画の持続時間に応じて視聴時間をグループ化し、正規化することで、異なる動画の持続時間に対応する視聴時間をスケールで一貫性を保ちます。 
For example, PCR directly divides the watch time according to the corresponding video duration and then normalizes the watch time into intervals of 0 to 1. 
例えば、PCRは視聴時間を対応する動画の持続時間に応じて直接分割し、その後視聴時間を0から1の範囲に正規化します。 
These normalized values are treated as estimated labels of user interest in downstream tasks. 
これらの正規化された値は、下流タスクにおけるユーザーの興味の推定ラベルとして扱われます。 
Since these methods mitigating bias via correcting labels, they can be categorised as label-correction methods. 
これらの方法はラベルを修正することでバイアスを軽減するため、ラベル修正方法として分類できます。 

In practice, both video ranking based on user interest and accurately predicting watch time are crucial tasks. 
実際には、ユーザーの興味に基づく動画ランキングと視聴時間の正確な予測の両方が重要なタスクです。 
The advantage of the label-correction method is that it can not only provide an unbiased estimate of the user interest score but also predict watch time through the inverse transformation of the normalization function. 
ラベル修正方法の利点は、ユーザーの興味スコアの偏りのない推定を提供できるだけでなく、正規化関数の逆変換を通じて視聴時間を予測できることです。 
In contrast, other existing methods, such as the feature-based methods: DCR(He etal.,2023)and CVRDD(Tang etal.,2023a), primarily focus on the unbiased estimation of user interest scores. 
対照的に、DCR（He etal.,2023）やCVRDD（Tang etal.,2023a）などの他の既存の方法は、主にユーザーの興味スコアの偏りのない推定に焦点を当てています。 
While these methods have proven effective, they struggle to simultaneously estimate both watch time and user interest scores as effectively as label-correction methods. 
これらの方法は効果的であることが証明されていますが、視聴時間とユーザーの興味スコアの両方をラベル修正方法と同じように効果的に同時に推定することに苦労しています。 

Although existing label-correction methods have shown effectiveness in some extent, we argue that there are still limitations. 
既存のラベル修正方法はある程度の効果を示していますが、まだ限界があると主張します。 
In existing methods, after the normalization, the completely played records (i.e., the user watched the whole video) are usually treated as the highest user interest, regardless of the video duration. 
既存の方法では、正規化後、完全に再生された記録（すなわち、ユーザーが動画全体を視聴した場合）は、動画の持続時間に関係なく通常は最高のユーザー興味として扱われます。 
Typically, records with explicit feedback can reflect user engagement and interest to some extent. 
通常、明示的なフィードバックを持つ記録は、ある程度ユーザーのエンゲージメントと興味を反映できます。 
However, from the explicit user feedback signals provided in KuaiRand dataset111https://kuairand.com/and WeChat dataset222https://algo.weixin.qq.com/, we observed that user explicit feedback in these completely played records does not align well with current methods. 
しかし、KuaiRandデータセット111https://kuairand.com/およびWeChatデータセット222https://algo.weixin.qq.com/で提供される明示的なユーザーフィードバック信号から、これらの完全に再生された記録におけるユーザーの明示的なフィードバックは、現在の方法とよく一致しないことが観察されました。 
Specifically, Fig.1shows the proportion of explicit positive feedback(i.e., like and forward) received by those completely played records, grouped by the video duration. 
具体的には、図1は、動画の持続時間に基づいてグループ化された完全に再生された記録が受け取った明示的なポジティブフィードバック（すなわち、いいねやシェア）の割合を示しています。 

In existing methods(Zhan etal.,2022; Zheng etal.,2022), since the user has fully watched the video, these completely played records should be considered as indicating equally high interest. 
既存の方法（Zhan etal.,2022; Zheng etal.,2022）では、ユーザーが動画を完全に視聴したため、これらの完全に再生された記録は同じく高い興味を示すものと見なされるべきです。 
However, Fig.1clearly shows that, on both two datasets, longer completely played videos have a higher proportion of positive feedback, even though the short videos are also completely played. 
しかし、図1は明確に示しており、両方のデータセットにおいて、長い完全に再生された動画は、短い動画も完全に再生されているにもかかわらず、より高い割合のポジティブフィードバックを受けています。 

The results in Fig.1suggest that even if users have watched the entire video, these completely played records may reflect varying levels of interest. 
図1の結果は、ユーザーが動画全体を視聴した場合でも、これらの完全に再生された記録が異なるレベルの興味を反映する可能性があることを示唆しています。 
Moreover, the shorter the video duration, the lower the user interest level that a completely played record can represent, as it corresponds to a lower explicit feedback proportion. 
さらに、動画の持続時間が短いほど、完全に再生された記録が表すことができるユーザーの興味レベルは低くなり、これはより低い明示的フィードバックの割合に対応します。 
This inspires us to derive a novel interpretation of the duration bias:There exists a potential watch time that faithfully reflects user interest, which is truncated by the video’s duration, thereby resulting in a duration bias. 
これにより、持続時間バイアスの新しい解釈を導き出すことができます：ユーザーの興味を忠実に反映する潜在的な視聴時間が存在し、これは動画の持続時間によって切り捨てられるため、持続時間バイアスが生じます。 
As illustrated in Figure2, let’s consider two users, A and B, engaged in watching the same video with a 30s duration. 
図2に示すように、同じ30秒の動画を視聴している2人のユーザー、AとBを考えてみましょう。 
Both users have completely played the video, and their watch times are recorded as 30s in the log data. 
両方のユーザーは動画を完全に再生しており、彼らの視聴時間はログデータに30秒として記録されています。 
However, after watching the same video, User B exhibits a higher level of interest than User A, thus appearing to be left wanting more. 
しかし、同じ動画を視聴した後、ユーザーBはユーザーAよりも高い興味レベルを示し、より多くを求めているように見えます。 
We then consider a counterfactual question:How long will the user watch if the video duration is sufficiently long? 
次に、反事実的な質問を考えます：動画の持続時間が十分に長い場合、ユーザーはどれくらいの時間視聴するでしょうか？ 
It becomes clear that User A is less likely, or even unlikely, to extend her observed watch time. 
ユーザーAは観察された視聴時間を延長する可能性が低い、あるいは全くないことが明らかになります。 
The logged 30s watch time for user A can sufficiently reflect her interest. 
ユーザーAのログされた30秒の視聴時間は、彼女の興味を十分に反映しています。 
Conversely, User B prefers exceeding her observed watch time. 
逆に、ユーザーBは観察された視聴時間を超えることを好みます。 
Since her information needs are not fully satisfied after watching this video, the logged 30s watch time cannot represent B’s interest. 
この動画を視聴した後、彼女の情報ニーズが完全に満たされていないため、ログされた30秒の視聴時間はBの興味を表すことができません。 

To this end, we argue that there exists a counterfactual watch time (CWT) corresponding to user interest, which is partially observed due to the truncation by video duration. 
この目的のために、ユーザーの興味に対応する反事実的視聴時間（CWT）が存在し、これは動画の持続時間によって切り捨てられるため部分的に観察されると主張します。 
For incompletely played records, the CWT equals its observed watch time, thus reflecting user interest. 
不完全に再生された記録の場合、CWTはその観察された視聴時間に等しく、したがってユーザーの興味を反映します。 
For completely played records, the CWT could be longer than the observed watch time due to the truncation by video duration. 
完全に再生された記録の場合、CWTは動画の持続時間による切り捨てのため、観察された視聴時間よりも長くなる可能性があります。 
The user’s true interest level could be higher than that directly inferred from the observed watch time. 
ユーザーの真の興味レベルは、観察された視聴時間から直接推測されるものよりも高い可能性があります。 

The CWT can explain the results in Fig.1 well: various CWT are truncated by video duration in an entirely played video. 
CWTは図1の結果をうまく説明できます：さまざまなCWTは、完全に再生された動画の動画の持続時間によって切り捨てられます。 
Therefore, the same observed watch time may correspond to various CWT and thus cannot distinguish user interest level. 
したがって、同じ観察された視聴時間はさまざまなCWTに対応する可能性があり、したがってユーザーの興味レベルを区別することはできません。 
Furthermore, the completion of shorter videos occurs more easily than longer ones, exacerbating the truncation of CWT. 
さらに、短い動画の完了は長い動画よりも容易に発生し、CWTの切り捨てを悪化させます。 
This results in a more pronounced duration bias, impacting the accuracy of interest measurement based on watch time. 
これにより、より顕著な持続時間バイアスが生じ、視聴時間に基づく興味測定の精度に影響を与えます。 

To model the CWT and estimate user interests, we propose a Counterfactual Watch Model (CWM) that adopts an economic perspective to model users’ CWT. 
CWTをモデル化し、ユーザーの興味を推定するために、ユーザーのCWTをモデル化するために経済的視点を採用したCounterfactual Watch Model（CWM）を提案します。 
Specifically, CWM treats user watching as a process of accumulating watching rewards, where the marginal rewards are indicative of user interest, and the invested watch time corresponds to the user watching cost. 
具体的には、CWMはユーザーの視聴を視聴報酬を蓄積するプロセスとして扱い、限界報酬はユーザーの興味を示し、投資された視聴時間はユーザーの視聴コストに対応します。 
At the time point where a user’s marginal cost equals the marginal rewards, the user attains the maximum cumulative benefit, making her actively stop watching. 
ユーザーの限界コストが限界報酬に等しくなる時点で、ユーザーは最大の累積利益を得て、視聴を積極的に停止します。 
This time point corresponds to the aforementioned CWT. 
この時点は、前述のCWTに対応します。 
Then, a cost-based transform function is derived to transform the CWT to the estimated user interest. 
次に、CWTを推定されたユーザーの興味に変換するためのコストベースの変換関数が導出されます。 
The duration-debiased recommendation model can be learned by optimizing a counterfactual likelihood function defined over observed user watch times. 
持続時間バイアスを除去した推薦モデルは、観察されたユーザーの視聴時間に基づいて定義された反事実的尤度関数を最適化することで学習できます。 
In summary, CWM attempts to model users’ consumption behavior, specifically in video scenarios. 
要約すると、CWMはユーザーの消費行動をモデル化しようとし、特に動画シナリオにおいてです。 
Similar to the commonly used click model(Chuklin etal.,2016), our CWM is beneficial for both relevance ranking and watch time prediction via effectively modeling user behaviors. 
一般的に使用されるクリックモデル（Chuklin etal.,2016）と同様に、私たちのCWMはユーザーの行動を効果的にモデル化することで、関連性ランキングと視聴時間予測の両方に有益です。 

The major contributions of this work are: 
この研究の主な貢献は次のとおりです：

1. (1)We provide a novel concept called counterfactual watch time (CWT) for interpreting the essence of duration bias; 
(1)持続時間バイアスの本質を解釈するための反事実的視聴時間（CWT）という新しい概念を提供します； 
2. (2)We propose a method named CWM for modeling CWT. 
(2)CWTをモデル化するためのCWMという方法を提案します。 
We further develop a cost-based transform function and counterfactual likelihood function for learning a duration-debiased recommendation model; 
さらに、持続時間バイアスを除去した推薦モデルを学習するためのコストベースの変換関数と反事実的尤度関数を開発します； 
3. (3)We conduct experiments on three real video recommendation datasets and online A/B testing. 
(3)3つの実際の動画推薦データセットとオンラインA/Bテストで実験を行います。 
The result improvements demonstrate the effectiveness of our CWM. 
結果の改善は、私たちのCWMの効果を示しています。 



## 2.Related work 関連研究

Video Recommendation. In the evolution from traditional video recommendation to TV show, various methods have been developed to enhance the user experience and accuracy of recommendations.
動画推薦。従来の動画推薦からテレビ番組への進化において、ユーザー体験と推薦の精度を向上させるためにさまざまな手法が開発されてきました。

Park etal.(2017)introduced a system that incorporates time factors and user preferences using 4-dimensional tensor factorization to improve recommendation accuracy.
Parkら（2017）は、4次元テンソル分解を使用して時間要因とユーザーの好みを組み込んだシステムを導入し、推薦の精度を向上させました。

Cho etal.(2019)presented a recommendation method that accounts for user feedback within specific watchable intervals to enhance user satisfaction with TV show recommendations.
Choら（2019）は、特定の視聴可能な間隔内でのユーザーのフィードバックを考慮した推薦手法を提案し、テレビ番組の推薦に対するユーザーの満足度を向上させました。

Qin etal.(2023)proposed a model that identifies and adapts to the behavior of multiple users interacting with a TV system, thereby improving the personalization of recommendations.
Qinら（2023）は、テレビシステムと相互作用する複数のユーザーの行動を特定し適応するモデルを提案し、推薦のパーソナライズを向上させました。

Most research works have transferred from traditional video to micro-video scenarios in the mobile internet era.
ほとんどの研究は、モバイルインターネット時代に従来の動画からマイクロ動画のシナリオに移行しています。

Covington etal.(2016b)introduced the funnel architecture of YouTube recommender system.
Covingtonら（2016b）は、YouTube推薦システムのファネルアーキテクチャを導入しました。

They predicted the expected watch time from training samples with weighted logistic regression, which utilizes observed watch time as the weight of positive samples’ loss.
彼らは、観察された視聴時間を正のサンプルの損失の重みとして利用する加重ロジスティック回帰を用いて、トレーニングサンプルから期待される視聴時間を予測しました。

Multi-task methods(Ma etal.,2018; Tang etal.,2020; Chang etal.,2023; Zhao etal.,2019)have been proposed to improve metrics such as watch time prediction, relevance of user-item pair, and number of video views together.
マルチタスク手法（Maら、2018; Tangら、2020; Changら、2023; Zhaoら、2019）が、視聴時間予測、ユーザー-アイテムペアの関連性、動画視聴回数などの指標を同時に改善するために提案されています。

Ma etal.(2018)extend the mixture-of-experts(Jacobs etal.,1991)architecture to multi-gate expert knowledge integration.
Maら（2018）は、専門家の混合（Jacobsら、1991）アーキテクチャをマルチゲート専門家知識統合に拡張しました。

Tang etal.(2020)proposed a shared learning structure to address the seesaw phenomenon.
Tangら（2020）は、シーソー現象に対処するための共有学習構造を提案しました。

Chang etal.(2023)proposed a plug-and-play parameter and embedding personalized network for a multi-domain and multi-task recommendation.
Changら（2023）は、マルチドメインおよびマルチタスク推薦のためのプラグアンドプレイパラメータと埋め込みパーソナライズネットワークを提案しました。

Counterfactual Information Retrieval. Most information retrieval systems consider users’ implicit feedback as a supervision signal to infer their true interests.
反事実情報検索。ほとんどの情報検索システムは、ユーザーの暗黙のフィードバックを監視信号として考慮し、彼らの真の興味を推測します。

However, implicit feedback is influenced not only by users’ interests but also by external factors.
しかし、暗黙のフィードバックはユーザーの興味だけでなく、外部要因にも影響されます。

Consequently, user interest signals are often concealed within implicit feedback and remain unobserved.
その結果、ユーザーの興味信号はしばしば暗黙のフィードバックの中に隠され、観察されないままとなります。

Researchers have drawn inspiration from causal inference techniques(Wu etal.,2022)and developed counterfactual information retrieval technology to address the biases inherent in implicit feedback.
研究者たちは因果推論技術（Wuら、2022）からインスピレーションを得て、暗黙のフィードバックに内在するバイアスに対処するための反事実情報検索技術を開発しました。

Previous work in counterfactual IR primarily focuses on mitigating position bias(Joachims etal.,2017; Ai etal.,2018; Yuan etal.,2020; Chen etal.,2021), popularity bias(Zhang etal.,2021; Zheng etal.,2021; Wei etal.,2021), and selection bias(Schnabel etal.,2016; Wang etal.,2016; Saito etal.,2020).
反事実情報検索に関する以前の研究は、主に位置バイアス（Joachimsら、2017; Aiら、2018; Yuanら、2020; Chenら、2021）、人気バイアス（Zhangら、2021; Zhengら、2021; Weiら、2021）、および選択バイアス（Schnabelら、2016; Wangら、2016; Saitoら、2020）の軽減に焦点を当てています。

However, duration bias becomes a crucial concern when it comes to video recommendation, which has been discussed in existing studies(Zhan etal.,2022; Zheng etal.,2022; Quan etal.,2023; Tang etal.,2023a; He etal.,2023).
しかし、動画推薦に関しては、持続時間バイアスが重要な懸念事項となり、既存の研究（Zhanら、2022; Zhengら、2022; Quanら、2023; Tangら、2023a; Heら、2023）で議論されています。

In contrast to our approach, current methods for correcting duration bias cannot effectively explain and eliminate duration bias.
私たちのアプローチとは対照的に、持続時間バイアスを修正するための現在の手法は、持続時間バイアスを効果的に説明し排除することができません。

Click model in Information Retrieval. Modeling user behaviors plays a vital role in enhancing the performance of information retrieval systems.
情報検索におけるクリックモデル。ユーザーの行動をモデル化することは、情報検索システムの性能を向上させる上で重要な役割を果たします。

The ability to accurately model user behaviors allows a retrieval system better to fulfill users’ information needs(Chuklin etal.,2016).
ユーザーの行動を正確にモデル化する能力は、検索システムがユーザーの情報ニーズをより良く満たすことを可能にします（Chuklinら、2016）。

To this end, many models have been proposed to explain or predict user click behavior in various contexts: cascade model (CM)(Craswell etal.,2008), user browsing model (UBM)(Dupret and Piwowarski,2008)and dynamic Bayesian network (DBN) model(Chapelle and Zhang,2009)model users’ click behavior in desktop searching with different assumption; mobile click model (MCM)(Mao etal.,2018)and F-shape Click Model (FSCM)(Fu etal.,2023)further extend the understanding of users’ click behaviors on mobile devices.
この目的のために、さまざまな文脈でユーザーのクリック行動を説明または予測するための多くのモデルが提案されています：カスケードモデル（CM）（Craswellら、2008）、ユーザーブラウジングモデル（UBM）（DupretとPiwowarski、2008）、および動的ベイジアンネットワーク（DBN）モデル（ChapelleとZhang、2009）は、異なる仮定のもとでデスクトップ検索におけるユーザーのクリック行動をモデル化します。モバイルクリックモデル（MCM）（Maoら、2018）およびF字型クリックモデル（FSCM）（Fuら、2023）は、モバイルデバイス上でのユーザーのクリック行動の理解をさらに拡張します。

Moreover,Borisov etal.(2016)andChen etal.(2020)develop the click model into neural networks, which enable automatic dependency detection.
さらに、Borisovら（2016）およびChenら（2020）は、クリックモデルをニューラルネットワークに発展させ、自動依存関係検出を可能にしました。

Unlike the above click models, the UWM proposed in this paper focuses on modeling and explaining users’ watching behavior since it is a better quantitative indicator of user preferences in video feeds.
上記のクリックモデルとは異なり、本論文で提案するUWMは、ユーザーの視聴行動をモデル化し説明することに焦点を当てています。これは、動画フィードにおけるユーザーの好みのより良い定量的指標だからです。



## 3. Counterfactual watch time

## 3. 反事実的視聴時間

In this section, we will first define the video recommendation problem and the counterfactual watch time(CWT); then we will provide supporting evidences for our proposed CWT. 
このセクションでは、まず動画推薦問題と反事実的視聴時間（CWT）を定義し、次に提案するCWTの支持証拠を提供します。

We also present an economic view of the user watch behavior based on the watch cost and reward. 
また、視聴コストと報酬に基づいたユーザーの視聴行動の経済的視点も提示します。

Finally, we point out the current methods’ limitation from the CWT viewpoint. 
最後に、CWTの観点から現在の手法の限界を指摘します。

### 3.1. Definition of counterfactual watch time

### 3.1. 反事実的視聴時間の定義

The task of user interest and watch time prediction can be formalized as follows: 
ユーザーの興味と視聴時間の予測タスクは次のように形式化できます。

Suppose $\mathcal{U}$ and $\mathcal{V}$ are the sets of users and videos, respectively. 
ユーザーの集合を$\mathcal{U}$、動画の集合を$\mathcal{V}$とします。

We can record user $u \in \mathcal{U}$’s watching behavior on video $v \in \mathcal{V}$ as $\mathcal{D}_{u,v} = \{\mathbf{x}_{u,v}, w_{u,v}, d_{v}\}$, 
ユーザー $u \in \mathcal{U}$ の動画 $v \in \mathcal{V}$ に対する視聴行動を $\mathcal{D}_{u,v} = \{\mathbf{x}_{u,v}, w_{u,v}, d_{v}\}$ として記録できます。

where $\mathbf{x}_{u,v} \in \mathbb{R}^{k}$ represents the feature vector of the sample pair and $k$ is the feature dimension. 
ここで、$\mathbf{x}_{u,v} \in \mathbb{R}^{k}$ はサンプルペアの特徴ベクトルを表し、$k$ は特徴次元です。

$w_{u,v} \in \mathbb{R}^{+}$ denotes user $u$’s observed watch time on video $v$ (e.g., in seconds), 
$w_{u,v} \in \mathbb{R}^{+}$ はユーザー $u$ の動画 $v$ に対する観測された視聴時間（例：秒単位）を示します。

while $d_{v} \in \mathbb{R}^{+}$ is the duration of video $v$. 
一方、$d_{v} \in \mathbb{R}^{+}$ は動画 $v$ の長さです。

Next, we will introduce a novel concept called counterfactual watch time (CWT), which is denoted as $w^{c}_{u,v}$. 
次に、反事実的視聴時間（CWT）と呼ばれる新しい概念を導入します。これは $w^{c}_{u,v}$ と表されます。

As we have discussed before, the CWT can be defined as: 
前述のように、CWTは次のように定義できます。

For user $u$ and video $v$, the CWT $w^{c}_{u,v} \in \mathbb{R}$ is defined as the time users want to watch based on the user’s interest $r_{u,v}$ if the video duration is sufficiently long. 
ユーザー $u$ と動画 $v$ に対して、CWT $w^{c}_{u,v} \in \mathbb{R}$ は、動画の長さが十分に長い場合に、ユーザーの興味 $r_{u,v}$ に基づいてユーザーが視聴したい時間として定義されます。

There is no correlation between $w^{c}_{u,v}$ and video duration $d_{v}$. 
$w^{c}_{u,v}$ と動画の長さ $d_{v}$ との間には相関関係はありません。

The CWT $w^{c}_{u,v}$ corresponds to user interests. 
CWT $w^{c}_{u,v}$ はユーザーの興味に対応します。

However, CWT $w^{c}_{u,v}$ does not always equal the observed watch time $w_{u,v}$ since it can be truncated by video duration $d_{v}$ in practice. 
しかし、CWT $w^{c}_{u,v}$ は、実際には動画の長さ $d_{v}$ によって切り捨てられる可能性があるため、観測された視聴時間 $w_{u,v}$ と常に等しいわけではありません。

CWT may also be truncated at 0, making it difficult to discern how much a user dislikes the video. 
CWT は 0 で切り捨てられることもあり、ユーザーが動画をどれだけ嫌っているかを判断するのが難しくなります。

However, this study is more concerned with the videos users like than those they dislike. 
しかし、この研究は、ユーザーが嫌う動画よりも、ユーザーが好む動画により関心を持っています。

Their relationship is formulated as follows: 
それらの関係は次のように定式化されます。

$$
w_{u,v} = \min(w^{c}_{u,v}, d_{v})
$$

Eq.(1) indicates that observed watch time $w_{u,v}$ can be regarded as the truncated variable of CWT $w^{c}_{u,v}$. 
式(1)は、観測された視聴時間 $w_{u,v}$ が CWT $w^{c}_{u,v}$ の切り捨て変数と見なすことができることを示しています。

### 3.2. The existence of counterfactual watch time

### 3.2. 反事実的視聴時間の存在

Though the CWT is not directly observable from the data, we can still find hints about the existence of CWT in real-world video recommendation datasets. 
CWT はデータから直接観測できませんが、実世界の動画推薦データセットにおける CWT の存在に関する手がかりを見つけることができます。

Next, we will use CWT to explain two phenomena presented in real datasets: (i) users’ repeated playing and (ii) the bimodal distribution of watch time. 
次に、CWT を使用して、実データセットに示される 2 つの現象を説明します：(i) ユーザーの繰り返し再生と (ii) 視聴時間の二峰性分布です。

#### 3.2.1. Evidence 1: repeated playing

#### 3.2.1. 証拠 1: 繰り返し再生

In real datasets, we found that users may engage in repeated playing (for example, by rewinding the video progress bar), leading to actual watch time that exceeds the video duration. 
実データセットでは、ユーザーが繰り返し再生（例えば、動画の進行バーを巻き戻すこと）を行うことがあり、これにより実際の視聴時間が動画の長さを超えることがあることがわかりました。

This phenomenon is often due to users’ high interest level in the current video. 
この現象は、ユーザーが現在の動画に対して高い興味を持っていることが多いです。

However, the video’s duration is insufficient to meet their needs, which is similar to our definition of CWT. 
しかし、動画の長さは彼らのニーズを満たすには不十分であり、これは私たちのCWTの定義に似ています。

Since the definition of CWT necessitates a sufficiently long video duration (Definition 1), in this study, we do not equate repeat playing with CWT. 
CWT の定義は十分に長い動画の長さを必要とするため（定義 1）、この研究では繰り返し再生を CWT と同一視しません。

In Fig.3, we investigate the repeated playing in both the KuaiRand and WeChat datasets. 
図3では、KuaiRand と WeChat の両データセットにおける繰り返し再生を調査します。

Specifically, we focus on two metrics: (1) repeated play proportion, which represents the proportion of repeat played records within the current video duration, and (2) average repeat play ratio, which reflects the average extent of repeat playing within the current video duration, defined as $(w_{u,v}-d_{v})/d_{v}$. 
具体的には、2 つの指標に焦点を当てます：(1) 繰り返し再生比率は、現在の動画の長さ内での繰り返し再生された記録の割合を示し、(2) 平均繰り返し再生比率は、現在の動画の長さ内での繰り返し再生の平均的な程度を反映し、$(w_{u,v}-d_{v})/d_{v}$ と定義されます。

The results depicted in Fig.3 indicate that both the proportion of users’ repeat playing and the degree of repeat playing are higher for shorter videos and decrease as video duration increases. 
図3に示される結果は、ユーザーの繰り返し再生の割合と繰り返し再生の程度の両方が短い動画で高く、動画の長さが増すにつれて減少することを示しています。

#### 3.2.2. Evidence 2: bimodal distribution

#### 3.2.2. 証拠 2: 二峰性分布

Another supporting evidence is the bimodal distribution of users’ watch time. 
もう一つの支持証拠は、ユーザーの視聴時間の二峰性分布です。

For the overall distribution of all the video playing records, existing studies argue that logarithmic watch time obeys the Gaussian distribution. 
すべての動画再生記録の全体的な分布について、既存の研究は対数視聴時間がガウス分布に従うと主張しています。

However, when we focus on a given video duration (e.g., 30s), the distribution of observed watch time turns out to be bimodal, as shown in Fig.4. 
しかし、特定の動画の長さ（例：30秒）に焦点を当てると、観測された視聴時間の分布は二峰性であることがわかります（図4参照）。

The bimodal distribution reveals that most users skip over the recommended video or completely watch it, while only a few users stop watching in the middle of the video playing. 
この二峰性分布は、ほとんどのユーザーが推奨された動画をスキップするか、完全に視聴する一方で、わずか数人のユーザーが動画の再生中に視聴を中止することを明らかにしています。

This abnormal distribution change is less interpreted by existing studies but can be well explained by the CWT. 
この異常な分布の変化は既存の研究ではあまり解釈されていませんが、CWT によってうまく説明できます。

#### 3.2.3. Explanation from counterfactual watch time

#### 3.2.3. 反事実的視聴時間からの説明

Without loss of generality, we assume that CWT $w^{c}_{u,v}$ obeys a Gaussian distribution. 
一般性を失うことなく、CWT $w^{c}_{u,v}$ がガウス分布に従うと仮定します。

However, as we have mentioned in Eq.(1), all sampled $w^{c}_{u,v}$ will be truncated by duration $d_{v}$. 
しかし、式(1)で述べたように、すべてのサンプル $w^{c}_{u,v}$ は長さ $d_{v}$ によって切り捨てられます。

Meanwhile, $w^{c}_{u,v}$ will also be truncated to 0 since all recorded watch times have to be non-negative. 
同時に、すべての記録された視聴時間は非負でなければならないため、$w^{c}_{u,v}$ も 0 に切り捨てられます。

The truncated samples are assigned to $d_{v}$ or 0, respectively. 
切り捨てられたサンプルは、それぞれ $d_{v}$ または 0 に割り当てられます。

As illustrated in Fig.5(a), with the video duration increases, CWT experiences less truncation on the right side, thereby reducing the tendency for users to engage in repeat playing. 
図5(a)に示すように、動画の長さが増すにつれて、CWT は右側での切り捨てが少なくなり、ユーザーが繰り返し再生を行う傾向が減少します。

Meanwhile, in Fig.5(b), when the original Gaussian distribution is truncated, it presents a bimodal distribution, as we observed in the real-world dataset. 
同時に、図5(b)では、元のガウス分布が切り捨てられると、実世界のデータセットで観察されたように二峰性分布を示します。

Hence, CWT can successfully interpret the above phenomenon, which in turn supports its existence. 
したがって、CWT は上記の現象をうまく解釈でき、これがその存在を支持します。

### 3.3. An economic view of user watching

### 3.3. ユーザー視聴の経済的視点

To address the relationship between CWT and user interest, we model the user’s watch behavior from an economic perspective. 
CWT とユーザーの興味との関係を考えるために、ユーザーの視聴行動を経済的視点からモデル化します。

The foundation of CWT within this framework is based on the concepts of utility maximization and rational choice. 
この枠組みの中での CWT の基盤は、効用最大化と合理的選択の概念に基づいています。



. The foundation of CWT within this framework is based on the concepts of utility maximization (Aleskerov et al., 2007) and rational choice (Vriend, 1996). 
CWTのこの枠組みの基盤は、効用最大化（Aleskerov et al., 2007）と合理的選択（Vriend, 1996）の概念に基づいています。

This means users decide how much time to allocate to watching videos based on the perceived utility (satisfaction) derived from the content and their resource constraints. 
これは、ユーザーがコンテンツから得られる認知された効用（満足度）とリソースの制約に基づいて、動画視聴にどれだけの時間を割り当てるかを決定することを意味します。

In accordance with these economic principles, individuals allocate resources—in this case, time—to maximize their utility. 
これらの経済原則に従って、個人はリソース（この場合は時間）を割り当てて効用を最大化します。

Utility can be seen as the reward minus the cost. 
効用は、報酬からコストを引いたものと見なすことができます。

For users, the reward for watching a video is the information or pleasure derived from the video content, which is determined by their interest to the video. 
ユーザーにとって、動画視聴の報酬は、動画コンテンツから得られる情報や楽しみであり、これは動画への興味によって決まります。

However, users cannot earn unlimited rewards, as they face resource constraints, such as limited time. 
しかし、ユーザーは限られた時間などのリソースの制約に直面しているため、無限の報酬を得ることはできません。

To illustrate the constraint, we introduce the concept of watching cost, which refers to the overall effort and resources required to watch a video, including not just the value of time for the user but also the user’s mental energy and attention. 
この制約を示すために、視聴コストの概念を導入します。視聴コストとは、ユーザーの時間の価値だけでなく、ユーザーの精神的エネルギーや注意も含めて、動画を視聴するために必要な全体的な努力とリソースを指します。

This watching cost highlights that watching a video requires users to allocate their finite resources, which could have been spent on other activities. 
この視聴コストは、動画を視聴するためにはユーザーが他の活動に使うことができた有限のリソースを割り当てる必要があることを強調しています。

In summary, we assume that the user’s watching behavior follows the underlying assumptions: 
要約すると、私たちはユーザーの視聴行動が以下の基本的な仮定に従うと仮定します：

- • Diminishing marginal reward: When the user watches a video, the enjoyment or satisfaction derived per second decreases gradually, which is supported by the habituation phenomenon in the psychology field (Thompson and Spencer, 1966) and existing practice (Xie et al., 2023). 
- • 限界的報酬の減少：ユーザーが動画を視聴すると、1秒あたりの楽しみや満足度は徐々に減少します。これは心理学の分野における習慣化現象（Thompson and Spencer, 1966）や既存の実践（Xie et al., 2023）によって支持されています。

The initial marginal watch reward corresponds to user interest. 
初期の限界視聴報酬はユーザーの興味に対応します。

- • Constant marginal cost: Since the watching cost is mainly influenced by context factors, we can mildly assume that context factors are not significantly altered during the period user watching video. 
- • 限界コストの一定性：視聴コストは主に文脈要因に影響されるため、ユーザーが動画を視聴している期間中に文脈要因が大きく変化しないと仮定することができます。

Therefore, we consider the marginal watch cost as a constant. 
したがって、私たちは限界視聴コストを一定と見なします。

- • Rational users: Users typically act rationally by maximizing their cumulative utility. 
- • 合理的なユーザー：ユーザーは通常、累積効用を最大化するように合理的に行動します。

Users will stop watching the video when the marginal watch cost equals the reward. 
ユーザーは、限界視聴コストが報酬と等しくなると動画の視聴を停止します。

Based on the three assumptions above, we draw the marginal watch cost/reward curves in Fig. 6(a) and the cumulative watch cost/reward curves in Fig. 6(b). 
上記の3つの仮定に基づいて、図6(a)に限界視聴コスト/報酬曲線を、図6(b)に累積視聴コスト/報酬曲線を描きます。

The marginal curves are obtained as derivatives of the cumulative curves. 
限界曲線は累積曲線の導関数として得られます。

The figure shows that the marginal watch reward decreases monotonically while the marginal watch cost curve is constant. 
この図は、限界視聴報酬が単調に減少する一方で、限界視聴コスト曲線は一定であることを示しています。

When these two curves meet, a user’s marginal watch reward equals the marginal watch cost. 
これらの2つの曲線が交わると、ユーザーの限界視聴報酬は限界視聴コストに等しくなります。

At this point, the cumulative utility (i.e., cumulative reward minus cumulative cost) is maximized, as illustrated in Figure 6(b). 
この時点で、累積効用（すなわち、累積報酬から累積コストを引いたもの）が最大化されます。これは図6(b)に示されています。

Formally, we refer to this time point as our proposed CWT. 
正式には、この時点を私たちの提案するCWTと呼びます。

Our economic view can interpret the phenomenon in Fig. 1 and Fig. 2: users' interest level in a video is reflected by the time when they receive their maximum cumulative utility. 
私たちの経済的視点は、図1および図2の現象を解釈できます：ユーザーの動画に対する興味レベルは、彼らが最大の累積効用を得る時点によって反映されます。

When the video duration is too short to achieve each user’s maximum cumulative utility point, users with either high or low interest will completely play it. 
動画の長さが各ユーザーの最大累積効用点を達成するには短すぎる場合、高い興味を持つユーザーも低い興味を持つユーザーもそれを完全に再生します。

### 3.4. Limitation of existing methods
### 3.4. 既存の方法の限界

Finally, we point out the limitation of current methods from the viewpoint of CWT. 
最後に、私たちはCWTの観点から現在の方法の限界を指摘します。

We will prove that users’ true interest cannot be inferred with only a transform function over the observed watch time, as shown in the following theorem: 
私たちは、次の定理に示すように、観察された視聴時間に対する変換関数だけではユーザーの真の興味を推測できないことを証明します：

For ∀𝒲⊆ℝ+, g∈𝒢 formulae-sequence for-all 𝒲 superscript ℝ g 𝒢 ∀ ~{}~{} \mathcal{W} \subseteq \mathbb{R}^{+}, g \in \mathcal{G} ∀ caligraphic_W ⊆ blackboard_R start_POSTSUPERSCRIPT + end_POSTSUPERSCRIPT , italic_g ∈ caligraphic_G, given g:ℛ→𝒲:𝑔→ℛ𝒲 g:\mathcal{R} \to \mathcal{W} italic_g : caligraphic_R → caligraphic_W, we have ∄ g−1:𝒲→ℛ: not-exists superscript 𝑔1→𝒲ℛ \n exists ~{}~{} g^{-1}:\mathcal{W} \to \mathcal{R} ∄ italic_g start_POSTSUPERSCRIPT - 1 end_POSTSUPERSCRIPT : caligraphic_W → caligraphic_R, where 𝒲 𝒲 \mathcal{W} caligraphic_W is the set of all observed watch time values, 𝒢 𝒢 \mathcal{G} caligraphic_G is the function space, ℛ ℛ \mathcal{R} caligraphic_R is the set of all interest probability values. 
∀ ~{}~{} \mathcal{W} \subseteq \mathbb{R}^{+}, g \in \mathcal{G} ∀ caligraphic_W ⊆ blackboard_R start_POSTSUPERSCRIPT + end_POSTSUPERSCRIPT , italic_g ∈ caligraphic_G に対して、g:ℛ→𝒲:𝑔→ℛ𝒲 g:\mathcal{R} \to \mathcal{W} italic_g : caligraphic_R → caligraphic_W が与えられたとき、∄ g^{-1}:\mathcal{W} \to \mathcal{R} ∄ italic_g start_POSTSUPERSCRIPT - 1 end_POSTSUPERSCRIPT : caligraphic_W → caligraphic_R となります。ここで、𝒲 𝒲 \mathcal{W} caligraphic_W はすべての観察された視聴時間の値の集合、𝒢 𝒢 \mathcal{G} caligraphic_G は関数空間、ℛ ℛ \mathcal{R} caligraphic_R はすべての興味確率値の集合です。

The proof of this theorem is presented in our Appendix A. 
この定理の証明は、私たちの付録Aに示されています。

This theorem indicates that existing methods fail to uncover user interest in those completely played records, especially when the video duration is short. 
この定理は、既存の方法が完全に再生された記録におけるユーザーの興味を明らかにできないこと、特に動画の長さが短い場合に失敗することを示しています。

The failure of current methods motivates us to develop a CWT-based approach to address this problem and better understand user interest. 
現在の方法の失敗は、私たちがこの問題に対処し、ユーザーの興味をよりよく理解するためにCWTベースのアプローチを開発する動機となります。



## 4. 私たちのアプローチ

For better modeling the CWT and estimating user interest, we propose Counterfactual Watch Model (CWM). 
CWTをより良くモデル化し、ユーザの興味を推定するために、Counterfactual Watch Model (CWM)を提案します。

Fig7 illustrates the flow of CWM in the inference stage and training stage. 
図7は、推論段階と訓練段階におけるCWMの流れを示しています。

At the inference stage, a recommendation model $f_{\theta}(\cdot)$, parameterized with $\theta$, estimates the user interest $\hat{r}_{u,v}$ based on the feature vector $\mathbf{x}_{u,v}$. 
推論段階では、パラメータ $\theta$ でパラメータ化された推薦モデル $f_{\theta}(\cdot)$ が、特徴ベクトル $\mathbf{x}_{u,v}$ に基づいてユーザの興味 $\hat{r}_{u,v}$ を推定します。

Then a transform function $g(\cdot)$, conditioned on user watch cost $c$, converts the interest estimation into the CWT prediction $\hat{w}^{c}_{u,v}$. 
次に、ユーザの視聴コスト $c$ に条件付けられた変換関数 $g(\cdot)$ が、興味の推定をCWT予測 $\hat{w}^{c}_{u,v}$ に変換します。

The actual watch time prediction $\hat{w}_{u,v}$ is obtained by truncating it through the video duration $d_{v}$. 
実際の視聴時間予測 $\hat{w}_{u,v}$ は、ビデオの長さ $d_{v}$ によって切り捨てられます。

At the training stage, to estimate the parameters $\theta$, we employ a set of user activity log $\mathcal{D} \subseteq \{\mathcal{D}_{u,v}=\{\mathbf{x}_{u,v},w_{u,v},d_{v}\}:u\in\mathcal{U},v\in\mathcal{V}\}$. 
訓練段階では、パラメータ $\theta$ を推定するために、ユーザ活動ログのセット $\mathcal{D} \subseteq \{\mathcal{D}_{u,v}=\{\mathbf{x}_{u,v},w_{u,v},d_{v}\}:u\in\mathcal{U},v\in\mathcal{V}\}$ を使用します。

For each $\mathcal{D}_{u,v} \in \mathcal{D}$, the observed watch time $w_{u,v}$ is transformed into the supervision signal of user interest by the inverse of the transform function, i.e., $r^{\prime}_{u,v}=g^{-1}(w_{u,v};c)$. 
各 $\mathcal{D}_{u,v} \in \mathcal{D}$ に対して、観測された視聴時間 $w_{u,v}$ は、変換関数の逆を用いてユーザの興味の監視信号に変換されます。すなわち、$r^{\prime}_{u,v}=g^{-1}(w_{u,v};c)$ です。

Although we use observed watch time $w_{u,v}$ as the input of the inverse transform function here, we will approximate it to CWT in optimization. 
ここでは観測された視聴時間 $w_{u,v}$ を逆変換関数の入力として使用しますが、最適化ではこれをCWTに近似します。

Then the predicted user interest $\hat{r}_{u,v}=f_{\theta}(\mathbf{x}_{u,v})$ is calculated with current model parameters. 
次に、予測されたユーザの興味 $\hat{r}_{u,v}=f_{\theta}(\mathbf{x}_{u,v})$ は、現在のモデルパラメータを用いて計算されます。

For all $\mathcal{D}_{u,v} \in \mathcal{D}$, comparing $r^{\prime}_{u,v}$ and $\hat{r}_{u,v}$ jointly with duration $d_{v}$ derives the likelihood function $\mathcal{L}_{c}(\cdot)$. 
すべての $\mathcal{D}_{u,v} \in \mathcal{D}$ に対して、$r^{\prime}_{u,v}$ と $\hat{r}_{u,v}$ をビデオの長さ $d_{v}$ と共に比較することで、尤度関数 $\mathcal{L}_{c}(\cdot)$ が導出されます。

Thus, the learning of the recommendation model can be performed by optimizing $\mathcal{L}_{c}(\cdot)$. 
したがって、推薦モデルの学習は $\mathcal{L}_{c}(\cdot)$ を最適化することで行うことができます。

Next, we will elaborate on the design of CWM’s key components: (1) the transform function $g(\cdot)$ and (2) the likelihood function $\mathcal{L}_{c}(\cdot)$. 
次に、CWMの主要なコンポーネントの設計について詳しく説明します：(1) 変換関数 $g(\cdot)$ と (2) 尤度関数 $\mathcal{L}_{c}(\cdot)$ です。

### 4.1. コストベースの変換関数

As defined in Section 3.1, the CWT $w^{c}_{u,v}$ reveals user interest level $r_{u,v}$. 
セクション3.1で定義されているように、CWT $w^{c}_{u,v}$ はユーザの興味レベル $r_{u,v}$ を明らかにします。

To estimate $r_{u,v}$ from $w^{c}_{u,v}$, we first define the transform function between $w^{c}_{u,v}$ and $r_{u,v}$. 
$w^{c}_{u,v}$ から $r_{u,v}$ を推定するために、まず $w^{c}_{u,v}$ と $r_{u,v}$ の間の変換関数を定義します。

Based on the economic view of the user’s watching process in Section 3.3, we first formulate the cumulative watch reward and cumulative watch cost function as: 
セクション3.3でのユーザの視聴プロセスの経済的観点に基づいて、まず累積視聴報酬と累積視聴コスト関数を次のように定式化します：

$$
F_{\mathrm{reward}}(r_{u,v}) \quad \text{and} \quad F_{\mathrm{cost}}(c)
$$

where the $\omega(r_{u,v})$ is the initial marginal reward that corresponds to user interest level $r_{u,v}$, and $c$ is the user watch cost per second. 
ここで、$\omega(r_{u,v})$ はユーザの興味レベル $r_{u,v}$ に対応する初期限界報酬であり、$c$ はユーザの視聴コスト（秒あたり）です。

It is evident that the derivative function of $F_{\mathrm{reward}}$ is monotonically decreasing while that of $F_{\mathrm{cost}}$ is constant, which satisfies the assumptions in Section 3.3. 
$F_{\mathrm{reward}}$ の導関数が単調減少であり、$F_{\mathrm{cost}}$ の導関数が一定であることは明らかであり、これはセクション3.3の仮定を満たします。

When their derivative values are equal, we can derive a time point (i.e., CWT) for the maximum cumulative benefit: 
その導関数の値が等しいとき、最大累積利益のための時間点（すなわちCWT）を導出できます：

$$
\frac{dF_{\mathrm{reward}}}{dt} = \frac{dF_{\mathrm{cost}}}{dt}
$$

Now we will formulate the initial marginal reward function $\omega(r_{u,v})$. 
ここで、初期限界報酬関数 $\omega(r_{u,v})$ を定式化します。

Since $r_{u,v} \in (0,1)$, the $\omega(r_{u,v})$ is expected to fulfill the following conditions: 
$r_{u,v} \in (0,1)$ であるため、$\omega(r_{u,v})$ は以下の条件を満たすことが期待されます：

(i) monotonically increasing. 
(i) 単調増加。

(ii) when $r_{u,v} \rightarrow 0$, the initial marginal reward $\omega(r_{u,v})$ should also tend to 0. 
(ii) $r_{u,v} \rightarrow 0$ のとき、初期限界報酬 $\omega(r_{u,v})$ も0に近づくべきです。

(iii) when $r_{u,v} \rightarrow 1$, the initial marginal reward $\omega(r_{u,v})$ should tend to positive infinity. 
(iii) $r_{u,v} \rightarrow 1$ のとき、初期限界報酬 $\omega(r_{u,v})$ は正の無限大に近づくべきです。

To this end, we formulate that $\omega(r_{u,v})=1/(-\log r_{u,v})$, so the CWT can be further written as: 
このため、$\omega(r_{u,v})=1/(-\log r_{u,v})$ と定式化し、CWTは次のように書き換えることができます：

$$
CWT = g^{-1}(r_{u,v}; c)
$$

Eq.(2) indicates how user interest $r_{u,v}$ and users’ watch cost $c$ affect their CWT. 
式(2)は、ユーザの興味 $r_{u,v}$ とユーザの視聴コスト $c$ がどのようにCWTに影響を与えるかを示しています。

Since we aim to uncover user interest from the CWT for training recommendation model, we can rewrite Eq.(2) to its inverse function: 
推薦モデルの訓練のためにCWTからユーザの興味を明らかにすることを目指しているため、式(2)をその逆関数に書き換えることができます：

$$
r_{u,v} = g(CWT; c)
$$

Both Eq.(2) and Eq.(3) are the cost-based transform functions since we introduce an extra cost parameter $c$ (as a hyper-parameter) for controlling the conversion sensitivity from CWT to user interest or vice versa. 
式(2)と式(3)は、CWTからユーザの興味への変換感度を制御するために追加のコストパラメータ $c$（ハイパーパラメータとして）を導入しているため、コストベースの変換関数です。

Then we can leverage them to estimate user interest and predict the user’s actual watch time. 
これらを利用してユーザの興味を推定し、ユーザの実際の視聴時間を予測することができます。

### 4.2. 反事実的尤度関数

Although we have proposed the cost-based transform function to describe the relationship between CWT and user interest, we still face the problem that CWT is truncated when the record is completely played. 
CWTとユーザの興味の関係を説明するためにコストベースの変換関数を提案しましたが、記録が完全に再生されるとCWTが切り捨てられるという問題に直面しています。

We need to approximate the CWT by the observed watch time to optimize our recommendation model. 
推薦モデルを最適化するために、観測された視聴時間によってCWTを近似する必要があります。

#### 4.2.1. 反事実的尤度関数の定式化

Inspired by the solution of survival analysis (Li et al., 2016), we regard the observed watch time distribution as the truncated distribution of CWT. 
生存分析の解決策（Li et al., 2016）に触発されて、観測された視聴時間分布をCWTの切り捨てられた分布と見なします。

The overall likelihood function of the truncated CWT can be written as: 
切り捨てられたCWTの全体的な尤度関数は次のように書くことができます：

$$
\mathcal{L}(W^{c})
$$

where $W^{c}$ denotes the random variable of CWT. 
ここで、$W^{c}$ はCWTの確率変数を示します。

Based on Eq.(1), we can replace all $w^{c}_{u,v}$ by $w_{u,v}$ in the second line. 
式(1)に基づいて、2行目のすべての $w^{c}_{u,v}$ を $w_{u,v}$ に置き換えることができます。

Eq(4) contains two parts: when $w_{u,v} < d_{v}$, the likelihood function equals the joint probability that the counterfactual duration variable is equal to $w_{u,v}$ and CWT variable is not truncated. 
式(4)は2つの部分を含んでいます：$w_{u,v} < d_{v}$ のとき、尤度関数は反事実的持続時間変数が $w_{u,v}$ に等しく、CWT変数が切り捨てられないという同時確率に等しくなります。



. When $w^{c}_{u,v} \geq d_{v}$, the likelihood function equals the probability that the CWT variable is truncated. 
$w^{c}_{u,v} \geq d_{v}$ のとき、尤度関数はCWT変数が切り捨てられる確率に等しくなります。

As discussed in Theorem 2, we cannot find a transform function for indicating user interest from observed watch time. 
定理2で述べたように、観察された視聴時間からユーザの興味を示す変換関数を見つけることはできません。

What we know is only $w^{c}_{u,v} \geq d_{v}$, so we incorporate this prior in likelihood function, allowing the models to determine the extent to which $w^{c}_{u,v}$ should exceed $d_{v}$. 
私たちが知っているのは $w^{c}_{u,v} \geq d_{v}$ のみであるため、この事前情報を尤度関数に組み込み、モデルが $w^{c}_{u,v}$ が $d_{v}$ をどの程度超えるべきかを決定できるようにします。

Maximizing Eq.(4) can reduce the duration bias caused by the truncation of CWT. 
式(4)を最大化することで、CWTの切り捨てによって引き起こされる期間バイアスを減少させることができます。

To estimate the user interest, we then equally transform Eq.(4) into the likelihood function of user interest $r_{u,v}$ via the transform function in Eq.(3): 
ユーザの興味を推定するために、次に式(4)を式(3)の変換関数を介してユーザの興味の尤度関数 $r_{u,v}$ に変換します：

$$
(5)
$$

where $R$ denotes the random variable of user interest probability. 
ここで、$R$ はユーザの興味確率の確率変数を示します。

Next, we will parameterize this likelihood function. 
次に、この尤度関数をパラメータ化します。

#### 4.2.2. Parameterize and optimize the likelihood function
#### 4.2.2. 尤度関数のパラメータ化と最適化

According to the result in (Li et al., 2016), Eq.(5) can be parameterized with a theoretical guarantee if the random variable $R$ obeys Gaussian distribution. 
(Li et al., 2016)の結果によれば、式(5)は確率変数 $R$ がガウス分布に従う場合、理論的保証のもとでパラメータ化できます。

For converting $R$ into a Gaussian-distributed random variable, we employ an inverse function of the standard Gaussian-distributed cumulative distribution function: 
$R$ をガウス分布の確率変数に変換するために、標準ガウス分布の累積分布関数の逆関数を使用します：

$$
(6)
$$

where $\phi(\cdot)$ and $\Phi(\cdot)$ are the probability density function and cumulative distribution function of standard Gaussian distribution, respectively. 
ここで、$\phi(\cdot)$ と $\Phi(\cdot)$ はそれぞれ標準ガウス分布の確率密度関数と累積分布関数です。

$\sigma$ is the standard deviation of the interest, which is treated as a hyper-parameter in our method. 
$\sigma$ は興味の標準偏差であり、私たちの手法ではハイパーパラメータとして扱われます。

And $f_{\theta}(\mathbf{x}_{u,v})$ is the recommendation model for predicting user interest, its parameter is denoted as $\theta$. 
そして、$f_{\theta}(\mathbf{x}_{u,v})$ はユーザの興味を予測するための推薦モデルであり、そのパラメータは $\theta$ として示されます。

Then the log-likelihood function is utilized in our training: 
次に、対数尤度関数が私たちのトレーニングに利用されます：

$$
(7)
$$

Remark. Eq.(7) is derived from maximum likelihood estimation (MLE): The optimal parameters are those that best describe the currently observed data. 
注記。式(7)は最大尤度推定（MLE）から導出されます：最適なパラメータは、現在観察されているデータを最もよく説明するものです。

For the CWT, we observe that when the video is not fully watched, the CWT equals to the actual watch time, this is the MSE part of Eq.(7). 
CWTについて、私たちはビデオが完全に視聴されていないとき、CWTが実際の視聴時間に等しいことを観察します。これは式(7)のMSE部分です。

However, for the video is fully watched, the observation we only know is CWT may larger than the actual watch time, this led to the amplification part of Eq.(7). 
しかし、ビデオが完全に視聴された場合、私たちが知っている観察はCWTが実際の視聴時間よりも大きい可能性があるため、これは式(7)の増幅部分につながります。

This approach to modelling truncated data is also common in endogenous problems and survival analysis. 
切り捨てデータをモデル化するこのアプローチは、内生的問題や生存分析でも一般的です。

Although simply amplifies predictions for fully watched videos cannot precisely model interest, it can still enhance our interest predictions in a large margin, which is verified in our experimental results. 
完全に視聴されたビデオの予測を単純に増幅することは興味を正確にモデル化できませんが、それでも私たちの興味の予測を大きく向上させることができ、これは私たちの実験結果で確認されています。

The detailed derivation from Eq.(5) to Eq.(7) can be found in our appendix. 
式(5)から式(7)までの詳細な導出は、私たちの付録にあります。

Finally, a duration-debiased recommendation model can be obtained through maximizing Eq.(7): 
最後に、式(7)を最大化することで、期間バイアスを除去した推薦モデルを得ることができます。

### 4.3. Online inference
### 4.3. オンライン推論

In the inference stage, given a user-video pair $(u,v)$, the predicted interest and watch time can be calculated by the unbiased recommendation model $f_{\theta^{*}}$ parameterized by the learned parameter $\theta^{*}$: 
推論段階では、ユーザ-ビデオペア $(u,v)$ が与えられたとき、予測された興味と視聴時間は学習されたパラメータ $\theta^{*}$ によってパラメータ化されたバイアスのない推薦モデル $f_{\theta^{*}}$ によって計算できます：

where $clip(x,a,b)$ function means clipping the value of $x$ into $[a,b]$. 
ここで、$clip(x,a,b)$ 関数は $x$ の値を $[a,b]$ にクリッピングすることを意味します。



## 5. Experiments and Results 実験と結果

We conducted experiments to verify the effectiveness of CWM on two large-scale publicly available benchmarks and a dataset collected from an industrial video product.  
私たちは、CWMの有効性を検証するために、2つの大規模な公開ベンチマークと、産業用ビデオ製品から収集したデータセットで実験を行いました。  
More implementation details can be found in Appendix B.  
実装の詳細については、付録Bに記載されています。  
More experimental results can be found in Appendix D.  
さらなる実験結果は、付録Dに記載されています。  
The source code and dataset are available at https://github.com/hyz20/CWM.git.  
ソースコードとデータセットは、https://github.com/hyz20/CWM.git で入手可能です。  

| Dataset  | #Users | #Videos | #Interactions | Mean Complete Ratio (%) |
|----------|--------|---------|---------------|--------------------------|
| KuaiRand | 26,988 | 6,598   | 1,266,560     | 17.5%                    |
| WeChat   | 20,000 | 96,418  | 7,310,108     | 45.5%                    |
| Product  | 2,000,000 | 1,011,007 | 36,366,437 | 32.8%                    |

| Dataset  | Backbone | FM | DCN | AutoInt | Method | VR | PC | RW | LR | D2Q | WTGD | 2Co | CWM |
|----------|----------|----|-----|---------|--------|----|----|----|----|-----|------|-----|-----|
| KuaiRand | MAE      | ↓↓ | ↓↓ | ↓↓     | ↓↓     | 22.100 | 20.974 | 24.279 | 18.271 | 23.044 | 22.262 | 17.738 | 21.698 |
|          | AUC      | 0.683 | 0.697 | 0.668 | 0.646 | 0.666 | 0.662 | 0.714 | 0.692 | 0.696 | 0.680 | 0.649 | 0.695 |
| WeChat   | MAE      | ↓↓ | ↓↓ | ↓↓     | ↓↓     | 9.404 | 8.920 | 9.653 | 8.778 | 9.637 | 10.200 | 8.001 | 9.317 |
|          | AUC      | 0.711 | 0.639 | 0.651 | 0.645 | 0.602 | 0.629 | 0.573 | 0.703 | 0.712 | 0.641 | 0.699 | 0.696 |
| Product  | MAE      | ↓↓ | ↓↓ | ↓↓     | ↓↓     | 9.411 | 7.395 | 8.913 | 7.383 | 7.420 | 7.511 | 6.785 | 9.384 |
|          | AUC      | 0.669 | 0.605 | 0.593 | 0.623 | 0.624 | 0.640 | 0.629 | 0.660 | 0.678 | 0.608 | 0.593 | 0.625 |

#### 5.1.1. Datasets データセット

The experiments were conducted on two public real-world datasets: WeChat and KuaiRand.  
実験は、2つの公共の実世界データセット、WeChatとKuaiRandで行われました。  
They are respectively collected from two large micro-video platforms, Wechat Channels and Kuaishou.  
それぞれ、Wechat ChannelsとKuaishouという2つの大規模なマイクロビデオプラットフォームから収集されました。  
We also conduct our evaluation in a large-scale product dataset from our video platform, which has tens of billions of daily active users.  
私たちはまた、数十億のデイリーアクティブユーザーを持つビデオプラットフォームからの大規模な製品データセットで評価を行います。  
We list their statistic information in Table 1.  
それらの統計情報を表1に示します。  
Note that we present each dataset’s completely played record percentage in the last column of Table 1.  
各データセットの完全に再生されたレコードの割合を表1の最後の列に示しています。  
Since the duration bias usually occurs on those completely played records, their percentages in all records represent the severity of the duration bias of each dataset.  
再生時間バイアスは通常、完全に再生されたレコードに発生するため、すべてのレコードにおけるその割合は、各データセットの再生時間バイアスの深刻度を示します。  
According to the statistics, WeChat has the most serious bias, while KuaiRand has the least bias.  
統計によると、WeChatは最も深刻なバイアスを持ち、KuaiRandは最も少ないバイアスを持っています。  

#### 5.1.2. Evaluation 評価

In this paper, we not only adopt our CWM for ranking videos by user interest (i.e., relevance ranking) but also for predicting users’ watch time.  
本論文では、ユーザーの興味に基づいてビデオをランク付けするためにCWMを採用するだけでなく（すなわち、関連性ランキング）、ユーザーの視聴時間を予測するためにも使用します。  
Both tasks are of great importance in real video recommendation scenarios.  
両方のタスクは、実際のビデオ推薦シナリオにおいて非常に重要です。  
As for the task of watch time prediction, we utilize users’ actual watch time $w_{u,v}$ as the ground truth, MAE (Mean Absolute Error) and XAUC (Zhan et al., 2022) were used as the evaluation measures.  
視聴時間予測のタスクについては、ユーザーの実際の視聴時間 $w_{u,v}$ を真実値として利用し、MAE（平均絶対誤差）とXAUC（Zhan et al., 2022）を評価指標として使用しました。  
Note that XAUC evaluates if the predictions of two samples are in the same order as their actual watch time.  
XAUCは、2つのサンプルの予測が実際の視聴時間と同じ順序であるかどうかを評価します。  
Such pairs are uniformly sampled, and the percentile of samples that are correctly ordered by predictions is XAUC.  
そのようなペアは均等にサンプリングされ、予測によって正しく順序付けられたサンプルのパーセンタイルがXAUCです。  
A larger XAUC suggests better watch time prediction performance.  
XAUCが大きいほど、視聴時間予測のパフォーマンスが良いことを示します。  

As for evaluating the task of relevance ranking according to user interest, considering that the user interest labels are unobserved in real-world datasets, we defined user interests based on CWT.  
ユーザーの興味に基づく関連性ランキングのタスクを評価するために、ユーザーの興味ラベルが実世界のデータセットでは観測されないことを考慮し、CWTに基づいてユーザーの興味を定義しました。  
Given a $(u,v)$ pair, the user interest label is defined as:  
$(u,v)$ペアに対して、ユーザーの興味ラベルは次のように定義されます：  

$$(8)$$

The $w_{0.7}$ indicates the 70% percentile of observed watch time, which is considered as the threshold for CWT.  
$w_{0.7}$は観測された視聴時間の70%パーセンタイルを示し、CWTの閾値と見なされます。  
When a user watches beyond this time, we consider the user to be interested.  
ユーザーがこの時間を超えて視聴した場合、ユーザーは興味を持っていると見なします。  
The similar user interest definition is also adopted in (Gao et al., 2022b; Zhao et al., 2023).  
同様のユーザー興味の定義は（Gao et al., 2022b; Zhao et al., 2023）でも採用されています。  
We will discuss the unbiasedness of $r_{u,v}$ in Appendix C.  
$ r_{u,v} $ のバイアスのない性質については、付録Cで議論します。  
The $r_{u,v}$ is used as the ground truth for evaluating the relevance ranking task, AUC and nDCG@k are utilized as the evaluation metrics.  
$r_{u,v}$は関連性ランキングタスクの評価のための真実値として使用され、AUCとnDCG@kが評価指標として利用されます。  

#### 5.1.3. Baselines ベースライン

In the experiments, we compared the proposed method with the following baselines:  
実験では、提案手法を以下のベースラインと比較しました：  
Three duration debiased baselines: PCR, WTG (Zheng et al., 2022), D2Q (Zhan et al., 2022), D2Co (Zhao et al., 2023);  
3つの再生時間バイアス除去ベースライン：PCR、WTG（Zheng et al., 2022）、D2Q（Zhan et al., 2022）、D2Co（Zhao et al., 2023）；  
Two watch time-weighted baselines: WLR (Covington et al., 2016a) and NDT (Xie et al., 2023);  
2つの視聴時間加重ベースライン：WLR（Covington et al., 2016a）とNDT（Xie et al., 2023）；  
And a naive baseline: VR (value regression) which directly fit the observed watch time.  
そして、観測された視聴時間に直接適合するナイーブベースライン：VR（値回帰）。  
For relevance ranking task, we also provide the result of Oracle, which is trained directly with the label defined in Eq. (8) and denote the upper bound performance of relevance ranking.  
関連性ランキングタスクについては、式（8）で定義されたラベルで直接訓練されたOracleの結果も提供し、関連性ランキングの上限性能を示します。  
Most of these methods are designed initially for relevance ranking or watch time prediction via a transform function.  
これらの手法のほとんどは、変換関数を介して関連性ランキングまたは視聴時間予測のために最初に設計されています。  
For the relevance ranking task, we directly rank the candidate videos via the predicted scores output by the recommendation models trained by these methods.  
関連性ランキングタスクでは、これらの手法で訓練された推薦モデルによって出力された予測スコアを介して候補ビデオを直接ランク付けします。  
For the watch time prediction task, we first transform the prediction of recommendation models into the interval of watch time via the inverse transform function of each method.  
視聴時間予測タスクでは、まず各手法の逆変換関数を介して推薦モデルの予測を視聴時間の範囲に変換します。  
Then we clip the estimated watch time into $0$ to $d_{v}$ as what we did in CWM.  
次に、CWMで行ったように、推定された視聴時間を$0$から$d_{v}$にクリップします。  
Two exceptions are WLR and NDT, which are implemented by a two-tower model and have no inverse transform function available.  
2つの例外はWLRとNDTで、これらは2タワーモデルで実装されており、逆変換関数は利用できません。  
Therefore, WLR is only used in watch time prediction, and NDT is used only in relevance ranking.  
したがって、WLRは視聴時間予測にのみ使用され、NDTは関連性ランキングにのみ使用されます。  

To investigate the generalization of our method and the baselines, we integrate them with different backbone models.  
私たちの手法とベースラインの一般化を調査するために、異なるバックボーンモデルと統合します。  
Specifically, we use recommendation models of FM (Rendle, 2012), DCN (Wang et al., 2017) and AutoInt (Song et al., 2019) as the backbone models.  
具体的には、FM（Rendle, 2012）、DCN（Wang et al., 2017）、およびAutoInt（Song et al., 2019）の推薦モデルをバックボーンモデルとして使用します。  
These three backbone models respectively represent three types of feature interactions: inner product, outer product, and attention mechanisms.  
これらの3つのバックボーンモデルは、それぞれ3種類の特徴相互作用を表します：内積、外積、および注意メカニズム。  

### 5.2. Overall performance 全体のパフォーマンス

We compared our CWM with other baselines in the three datasets’ watch time prediction task and relevance ranking task, as shown in Table 2 and Table 3, respectively.  
私たちは、表2および表3に示すように、3つのデータセットの視聴時間予測タスクと関連性ランキングタスクにおいて、CWMを他のベースラインと比較しました。  
It can be seen that our CWM obtains the best performance on almost all three datasets, all backbones and both tasks significantly.  
私たちのCWMは、ほぼすべての3つのデータセット、すべてのバックボーン、および両方のタスクで最良のパフォーマンスを得ていることがわかります。  
We also note that on WeChat, those methods equipped with duration debiasing (e.g., WTG and D2Q) perform even worse than the naive VR method.  
また、WeChatでは、再生時間バイアス除去機能を備えた手法（例：WTGやD2Q）が、ナイーブなVR手法よりもさらに悪いパフォーマンスを示すことにも注意が必要です。  
The reason is that the WeChat dataset has much more completely played records (45.5%) than that of KuaiRand (17.5%), showing that increasing completely played records make current debiasing methods get ineffective.  
その理由は、WeChatデータセットがKuaiRand（17.5%）よりもはるかに多くの完全に再生されたレコード（45.5%）を持っているため、完全に再生されたレコードを増やすことで現在のバイアス除去手法が効果を失うことを示しています。  
In contrast, CWM improved more on WeChat than on other datasets.  
対照的に、CWMは他のデータセットよりもWeChatでの改善が大きくなりました。  
The results also verified the motivation of this paper: Current methods regard all completely played records as the same high interest, violating real interest distribution in real data.  
結果はまた、本論文の動機を検証しました：現在の手法は、すべての完全に再生されたレコードを同じ高い興味として扱い、実データにおける実際の興味分布に違反しています。  
Therefore, when the dataset contains many completely played records (i.e., records with truncated CWT), the performance of these methods gets worse.  
したがって、データセットに多くの完全に再生されたレコード（すなわち、切り捨てられたCWTを持つレコード）が含まれる場合、これらの手法のパフォーマンスは悪化します。  
Instead, CWM can model users’ truncated CWT to estimate user interest better and predict users’ actual watch time.  
その代わりに、CWMはユーザーの切り捨てられたCWTをモデル化して、ユーザーの興味をより良く推定し、ユーザーの実際の視聴時間を予測できます。  

### 5.3. Effectiveness on duration debiasing 再生時間バイアス除去の効果

To investigate why our CWM is more effective on duration debiasing than other baselines, we divided the KuaiRand dataset into ten equal parts with different duration ranges.  
私たちのCWMが他のベースラインよりも再生時間バイアス除去においてより効果的である理由を調査するために、KuaiRandデータセットを異なる再生時間範囲で10等分しました。  
Then we evaluate each model on the subset of KuaiRand.  
次に、KuaiRandのサブセットで各モデルを評価します。  
The result is presented in Fig. 8.  
結果は図8に示されています。  
Note that the evaluation metric has different value scales among different subsets, so we report the relative improvement of each method to VR to show the extent to which these methods address duration bias.  
評価指標は異なるサブセット間で異なる値のスケールを持つため、これらの手法が再生時間バイアスにどの程度対処しているかを示すために、各手法のVRに対する相対的な改善を報告します。  
The relative improvement is $\Delta Imp = \frac{v_{m} - v_{0}}{v_{0}}$ where $v_{0}$ is the metric value of VR and $v_{m}$ is the metric value of each method.  
相対的な改善は $\Delta Imp = \frac{v_{m} - v_{0}}{v_{0}}$ であり、ここで $v_{0}$ はVRの指標値、$v_{m}$ は各手法の指標値です。  
Fig 8(a) illustrates the performance of each method on the watch time prediction task, measured by $\Delta Imp$ on XAUC.  
図8(a)は、視聴時間予測タスクにおける各手法のパフォーマンスを、XAUCに対する $\Delta Imp$ で測定したものを示しています。  


```md
. Fig8(b) illustrates the performance of each method on the relevance ranking task, measured byΔImpΔ𝐼𝑚𝑝\Delta Improman_Δ italic_I italic_m italic_pon AUC. 
図8(b)は、AUCで測定された関連性ランキングタスクにおける各手法の性能を示しています。

In both tasks, most baselines perform better than VR in short videos (i.e., duration¡30s), indicating their effectiveness on duration debiasing to some extent. 
両方のタスクにおいて、ほとんどのベースラインは短い動画（すなわち、再生時間が30秒未満）でVRよりも良い性能を示しており、ある程度の再生時間のバイアス除去に効果的であることを示しています。

However, since they simply regard completely played records as equally high interest, CWM performed better than them. 
しかし、彼らは単に完全に再生された記録を同じく高い興味と見なすため、CWMはそれらよりも良い性能を発揮しました。

We can find that these baselines perform worse in longer videos on both tasks. 
これらのベースラインは、両方のタスクにおいて長い動画では性能が悪化することがわかります。

This is also because they regard short, completely played video recordings as high interest, leading to underestimating user interest and watch time prediction for longer videos. 
これは、彼らが短い完全再生された動画記録を高い興味と見なすため、長い動画に対するユーザーの興味と視聴時間の予測を過小評価することにつながります。

In contrast, CWM can model the CWT and assign fairer interest estimates to videos of different durations. 
対照的に、CWMはCWTをモデル化し、異なる再生時間の動画に対してより公平な興味の推定を割り当てることができます。

### 5.4.Comparison with more baselines
### 5.4. より多くのベースラインとの比較

We have compared our CWM with other label-correction methods before, but the superiority of CWM compared with other state-of-the-art methods remains unclear. 
私たちは以前に他のラベル修正手法とCWMを比較しましたが、CWMが他の最先端手法と比較して優れているかどうかは不明のままです。

Therefore, we further implemented CVRDD(Tang etal.,2023a), DCR(He etal.,2023), and VLDRec(Quan etal.,2023). 
したがって、私たちはさらにCVRDD（Tang et al., 2023a）、DCR（He et al., 2023）、およびVLDRec（Quan et al., 2023）を実装しました。

CVRDD treats video duration as a mediation factor, DCR considers video duration as a confounder, and VLDRec employs PCR as the label with pairwise learning, all primarily feature-based or data-based approaches. 
CVRDDは動画の再生時間を媒介因子として扱い、DCRは動画の再生時間を交絡因子と見なし、VLDRecはペアワイズ学習を用いてPCRをラベルとして使用します。これらはすべて主に特徴ベースまたはデータベースのアプローチです。

In contrast, our label-correction method, CWM, consistently outperforms these baselines in terms of AUC and nDCG@3 metrics, as shown in Table4. 
対照的に、私たちのラベル修正手法であるCWMは、AUCおよびnDCG@3メトリックの観点から、これらのベースラインを一貫して上回っています（表4に示されています）。

The superiority of CWM is consistent across all datasets and backbone models. 
CWMの優位性は、すべてのデータセットおよびバックボーンモデルにおいて一貫しています。

In conclusion, our CWM method demonstrates superior performance in mitigating duration bias by modeling counterfactual watch time (CWT), highlighting its effectiveness in delivering more accurate and unbiased recommendations in short video recommendation systems. 
結論として、私たちのCWM手法は、反事実的視聴時間（CWT）をモデル化することによって再生時間のバイアスを軽減する優れた性能を示し、短い動画推薦システムにおいてより正確で偏りのない推薦を提供する効果を強調しています。

### 5.5.Ablation study
### 5.5. アブレーションスタディ

We also investigate how CWM’s two components benefit the CWM, i.e., the cost-based transform function and the counterfactual likelihood functions. 
私たちはまた、CWMの2つのコンポーネントがCWMにどのように利益をもたらすかを調査します。すなわち、コストベースの変換関数と反事実的尤度関数です。

The cost-based transform function estimates user interest from the CWT, and the counterfactual likelihood function optimizes the model unbiasedly using the observed watch time. 
コストベースの変換関数はCWTからユーザーの興味を推定し、反事実的尤度関数は観察された視聴時間を使用してモデルを偏りなく最適化します。

Specifically, we produce two variants for CWM. 
具体的には、CWMの2つのバリアントを作成します。

The first is denoted as CWM-C, which removes the cost-based transform function and directly applies the original watch time to the counterfactual likelihood function. 
最初のものはCWM-Cと呼ばれ、コストベースの変換関数を削除し、元の視聴時間を反事実的尤度関数に直接適用します。

The second one is denoted as CWM-L, which replaces the counterfactual likelihood function with a mean squared error loss function. 
2つ目はCWM-Lと呼ばれ、反事実的尤度関数を平均二乗誤差損失関数に置き換えます。

Fig.9 demonstrates the performance comparison between CWM and its variants on two datasets and two tasks. 
図9は、2つのデータセットと2つのタスクにおけるCWMとそのバリアントの性能比較を示しています。

On KuaiRand, CWM-L obtains similar performances to CWM, while CWM-C has a significant performance drop to CWM. 
KuaiRandでは、CWM-LはCWMと同様の性能を得る一方で、CWM-CはCWMに対して大幅な性能低下を示します。

We argue that when CWT is less truncated (e.g., KuaiRand has only 17.5% completely played records), how it is converted into an interest estimation can primarily affect performance. 
CWTがあまり切り捨てられない場合（例えば、KuaiRandでは完全に再生された記録が17.5%しかない）、それがどのように興味の推定に変換されるかが性能に主に影響を与えると主張します。

On WeChat, CWM-C obtains a similar performance to CWM, while CWM-L has a significant performance drop to CWM. 
WeChatでは、CWM-CはCWMと同様の性能を得る一方で、CWM-LはCWMに対して大幅な性能低下を示します。

We argue that when CWT is heavily truncated (e.g., WeChat has 45.5% completely played records), how the observed watch time is used to approximate the learning of CWT becomes the performance bottleneck. 
CWTが大幅に切り捨てられる場合（例えば、WeChatでは完全に再生された記録が45.5%）、観察された視聴時間がCWTの学習を近似するためにどのように使用されるかが性能のボトルネックになると主張します。

### 5.6.Online A/B Testing
### 5.6. オンラインA/Bテスト

To verify the effectiveness of CWM in real-world recommendation scenarios, we conducted online experiments in our commercial system, a popular platform with tens of millions of active users every day. 
CWMの実世界の推薦シナリオにおける効果を検証するために、私たちは商業システムでオンライン実験を実施しました。これは、毎日数千万のアクティブユーザーを持つ人気のプラットフォームです。

The baseline is a highly-optimized multi-task model deployed for the product. 
ベースラインは、製品のために展開された高度に最適化されたマルチタスクモデルです。

Both the baseline and CWM were trained incrementally on the same anonymous logging data, and each one serves 5% traffic, randomly selected from the same user group. 
ベースラインとCWMの両方は、同じ匿名ログデータで段階的にトレーニングされ、各々は同じユーザーグループからランダムに選ばれた5%のトラフィックを提供します。

As for short video recommendations, improving customers’ mean watch time (MWT) is the main target. 
短い動画の推薦に関しては、顧客の平均視聴時間（MWT）を改善することが主な目標です。

Other metrics, such as average valid viewing volume (VV) and click-through rate (CTR), are also adopted. 
平均有効視聴量（VV）やクリック率（CTR）などの他のメトリックも採用されています。

According to the online A/B testing results shown in Table5, we can see that CWM does help users to entertain themselves and spend more time watching the short videos. 
表5に示されているオンラインA/Bテストの結果によれば、CWMはユーザーが楽しむのを助け、短い動画をより多く視聴する時間を増やすことがわかります。

```



## 6.Conclusion 結論

In this study, we aim to counteract the duration bias in video recommendation. 
本研究では、ビデオ推薦における期間バイアスに対抗することを目的としています。

We propose counterfactual watch time (CWT) for interpreting the duration bias in video recommendation and point out that the duration bias is caused by the truncation of the user’s CWT by video duration. 
ビデオ推薦における期間バイアスを解釈するために反事実的視聴時間（CWT）を提案し、期間バイアスはユーザのCWTがビデオの期間によって切り捨てられることによって引き起こされることを指摘します。

A Counterfactual Watch Model (CWM) is then developed, revealing that the CWT equals the time users get the maximum benefit from video recommender systems. 
次に、反事実的視聴モデル（CWM）が開発され、CWTはユーザがビデオ推薦システムから最大の利益を得る時間に等しいことが明らかになります。

A cost-based correction function is defined to transform the CWT into the user interest, and the unbiased recommendation model can be learned by optimizing a counterfactual likelihood function defined over observed user watch times. 
CWTをユーザの興味に変換するためのコストベースの補正関数が定義され、観察されたユーザの視聴時間に基づいて定義された反事実的尤度関数を最適化することによって、バイアスのない推薦モデルを学習することができます。

Experimental results on three offline real datasets and online A/B testing indicate the superiority of the proposed CWM. 
3つのオフライン実データセットとオンラインA/Bテストにおける実験結果は、提案されたCWMの優位性を示しています。



## References 参考文献
- (1)↑
- Ai etal.(2018)↑Qingyao Ai, Keping Bi, Cheng Luo, Jiafeng Guo, and W.Bruce Croft. 2018.Unbiased Learning to Rank with Unbiased Propensity Estimation. InThe 41st International ACM SIGIR Conference on Research Development in Information Retrieval(Ann Arbor, MI, USA)(SIGIR ’18). ACM, New York, NY, USA, 385–394.https://doi.org/10.1145/3209978.3209986
- Ai etal.(2018)↑Qingyao Ai, Keping Bi, Cheng Luo, Jiafeng Guo、およびW.Bruce Croft. 2018.バイアスのない傾向推定を用いたバイアスのないランキング学習. 第41回国際ACM SIGIR情報検索研究開発会議（アナーバー、ミシガン州、アメリカ）（SIGIR '18）。ACM、ニューヨーク、NY、アメリカ、385–394. https://doi.org/10.1145/3209978.3209986
- Aleskerov etal.(2007)↑Fuad Aleskerov, Denis Bouyssou, and Bernard Monjardet. 2007.Utility maximization, choice and preference. Vol.16.Springer Science & Business Media.
- Aleskerov etal.(2007)↑Fuad Aleskerov, Denis Bouyssou、およびBernard Monjardet. 2007.効用最大化、選択と嗜好. 第16巻. Springer Science & Business Media.
- Amemiya (1984)↑Takeshi Amemiya. 1984.Tobit models: A survey.Journal of econometrics24, 1-2 (1984), 3–61.
- Amemiya (1984)↑雨宮武. 1984.トビットモデル：調査. 経済学ジャーナル 24, 1-2 (1984), 3–61.
- Borisov etal.(2016)↑Alexey Borisov, Ilya Markov, Maarten de Rijke, and Pavel Serdyukov. 2016.A Neural Click Model for Web Search. InProceedings of the 25th International Conference on World Wide Web(Montréal, Québec, Canada)(WWW ’16). International World Wide Web Conferences Steering Committee, Republic and Canton of Geneva, CHE, 531–541.https://doi.org/10.1145/2872427.2883033
- Borisov etal.(2016)↑アレクセイ・ボリソフ、イリヤ・マルコフ、マールテン・デ・ライケ、およびパベル・セルデュコフ. 2016.ウェブ検索のためのニューラルクリックモデル. 第25回国際ワールドワイドウェブ会議（モントリオール、ケベック、カナダ）（WWW '16）。国際ワールドワイドウェブ会議運営委員会、ジュネーブ州、スイス、531–541. https://doi.org/10.1145/2872427.2883033
- Cai etal.(2023)↑Qingpeng Cai, Zhenghai Xue, Chi Zhang, Wanqi Xue, Shuchang Liu, Ruohan Zhan, Xueliang Wang, Tianyou Zuo, Wentao Xie, Dong Zheng, Peng Jiang, and Kun Gai. 2023.Two-Stage Constrained Actor-Critic for Short Video Recommendation. InProceedings of the ACM Web Conference 2023, WWW 2023, Austin, TX, USA, 30 April 2023 - 4 May 2023. ACM, 865–875.
- Cai etal.(2023)↑Qingpeng Cai, Zhenghai Xue, Chi Zhang, Wanqi Xue, Shuchang Liu, Ruohan Zhan, Xueliang Wang, Tianyou Zuo, Wentao Xie, Dong Zheng, Peng Jiang、およびKun Gai. 2023.短編動画推薦のための二段階制約付きアクター-クリティック. ACM Web Conference 2023の議事録、WWW 2023、オースティン、TX、アメリカ、2023年4月30日 - 5月4日。ACM、865–875.
- Chang etal.(2023)↑Jianxin Chang, Chenbin Zhang, Yiqun Hui, Dewei Leng, Yanan Niu, Yang Song, and Kun Gai. 2023.PEPNet: Parameter and Embedding Personalized Network for Infusing with Personalized Prior Information.CoRRabs/2302.01115 (2023).
- Chang etal.(2023)↑Jianxin Chang, Chenbin Zhang, Yiqun Hui, Dewei Leng, Yanan Niu, Yang Song、およびKun Gai. 2023.PEPNet: パラメータと埋め込みの個別化ネットワークによる個別化事前情報の注入. CoRR abs/2302.01115 (2023).
- Chapelle and Zhang (2009)↑Olivier Chapelle and Ya Zhang. 2009.A Dynamic Bayesian Network Click Model for Web Search Ranking. InProceedings of the 18th International Conference on World Wide Web(Madrid, Spain)(WWW ’09). Association for Computing Machinery, New York, NY, USA, 1–10.https://doi.org/10.1145/1526709.1526711
- Chapelle and Zhang (2009)↑オリビエ・シャペルとヤ・ザン. 2009.ウェブ検索ランキングのための動的ベイジアンネットワーククリックモデル. 第18回国際ワールドワイドウェブ会議の議事録（マドリード、スペイン）（WWW '09）。計算機科学協会、ニューヨーク、NY、アメリカ、1–10. https://doi.org/10.1145/1526709.1526711
- Chen etal.(2020)↑Jia Chen, Jiaxin Mao, Yiqun Liu, Min Zhang, and Shaoping Ma. 2020.A Context-Aware Click Model for Web Search. InProceedings of the 13th International Conference on Web Search and Data Mining(Houston, TX, USA)(WSDM ’20). Association for Computing Machinery, New York, NY, USA, 88–96.https://doi.org/10.1145/3336191.3371819
- Chen etal.(2020)↑Jia Chen, Jiaxin Mao, Yiqun Liu, Min Zhang、およびShaoping Ma. 2020.ウェブ検索のためのコンテキスト認識クリックモデル. 第13回国際ウェブ検索およびデータマイニング会議の議事録（ヒューストン、TX、アメリカ）（WSDM '20）。計算機科学協会、ニューヨーク、NY、アメリカ、88–96. https://doi.org/10.1145/3336191.3371819
- Chen etal.(2021)↑Mouxiang Chen, Chenghao Liu, Jianling Sun, and StevenC.H. Hoi. 2021.Adapting Interactional Observation Embedding for Counterfactual Learning to Rank. InProceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval(Virtual Event, Canada)(SIGIR ’21). Association for Computing Machinery, New York, NY, USA, 285–294.https://doi.org/10.1145/3404835.3462901
- Chen etal.(2021)↑Mouxiang Chen, Chenghao Liu, Jianling Sun、およびSteven C.H. Hoi. 2021.反事実的ランキング学習のための相互作用観察埋め込みの適応. 第44回国際ACM SIGIR情報検索研究開発会議の議事録（バーチャルイベント、カナダ）（SIGIR '21）。計算機科学協会、ニューヨーク、NY、アメリカ、285–294. https://doi.org/10.1145/3404835.3462901
- Cho etal.(2019)↑Kyung-Jae Cho, Yeon-Chang Lee, Kyungsik Han, Jaeho Choi, and Sang-Wook Kim. 2019.No, that’s not my feedback: TV show recommendation using watchable interval. In2019 IEEE 35th International Conference on Data Engineering (ICDE). IEEE, 316–327.
- Cho etal.(2019)↑キョンジェ・チョ、ヨンチャン・リー、キョンシク・ハン、ジェホ・チョイ、およびサンウク・キム. 2019.いいえ、それは私のフィードバックではありません：視聴可能なインターバルを使用したテレビ番組推薦. 2019年IEEE第35回データ工学国際会議（ICDE）。IEEE、316–327.
- Chuklin etal.(2016)↑Aleksandr Chuklin, Ilya Markov, and Maarten de Rijke. 2016.Click Models for Web Search and Their Applications to IR: WSDM 2016 Tutorial. InProceedings of the Ninth ACM International Conference on Web Search and Data Mining(San Francisco, California, USA)(WSDM ’16). Association for Computing Machinery, New York, NY, USA, 689–690.https://doi.org/10.1145/2835776.2855113
- Chuklin etal.(2016)↑アレクサンドル・チュクリン、イリヤ・マルコフ、およびマールテン・デ・ライケ. 2016.ウェブ検索のためのクリックモデルとその情報検索への応用：WSDM 2016チュートリアル. 第9回ACM国際ウェブ検索およびデータマイニング会議の議事録（サンフランシスコ、カリフォルニア州、アメリカ）（WSDM '16）。計算機科学協会、ニューヨーク、NY、アメリカ、689–690. https://doi.org/10.1145/2835776.2855113
- Covington etal.(2016a)↑Paul Covington, Jay Adams, and Emre Sargin. 2016a.Deep Neural Networks for YouTube Recommendations. InProceedings of the 10th ACM Conference on Recommender Systems(Boston, Massachusetts, USA)(RecSys ’16). Association for Computing Machinery, New York, NY, USA, 191–198.https://doi.org/10.1145/2959100.2959190
- Covington etal.(2016a)↑ポール・コビントン、ジェイ・アダムス、およびエムレ・サルギン. 2016a. YouTube推薦のための深層ニューラルネットワーク. 第10回ACM推薦システム会議の議事録（ボストン、マサチューセッツ州、アメリカ）（RecSys '16）。計算機科学協会、ニューヨーク、NY、アメリカ、191–198. https://doi.org/10.1145/2959100.2959190
- Covington etal.(2016b)↑Paul Covington, Jay Adams, and Emre Sargin. 2016b.Deep Neural Networks for YouTube Recommendations. InProceedings of the 10th ACM Conference on Recommender Systems, Boston, MA, USA, September 15-19, 2016. ACM, 191–198.
- Covington etal.(2016b)↑ポール・コビントン、ジェイ・アダムス、およびエムレ・サルギン. 2016b. YouTube推薦のための深層ニューラルネットワーク. 第10回ACM推薦システム会議の議事録、ボストン、MA、アメリカ、2016年9月15-19日。ACM、191–198.
- Craswell etal.(2008)↑Nick Craswell, Onno Zoeter, Michael Taylor, and Bill Ramsey. 2008.An Experimental Comparison of Click Position-Bias Models. InProceedings of the 2008 International Conference on Web Search and Data Mining(Palo Alto, California, USA)(WSDM ’08). Association for Computing Machinery, New York, NY, USA, 87–94.https://doi.org/10.1145/1341531.1341545
- Craswell etal.(2008)↑ニック・クラスウェル、オノ・ゾエター、マイケル・テイラー、およびビル・ラムジー. 2008.クリック位置バイアスモデルの実験的比較. 2008年国際ウェブ検索およびデータマイニング会議の議事録（パロアルト、カリフォルニア州、アメリカ）（WSDM '08）。計算機科学協会、ニューヨーク、NY、アメリカ、87–94. https://doi.org/10.1145/1341531.1341545
- Davidson etal.(2010)↑James Davidson, Benjamin Liebald, Junning Liu, Palash Nandy, Taylor VanVleet, Ullas Gargi, Sujoy Gupta, Yu He, Mike Lambert, Blake Livingston, and Dasarathi Sampath. 2010.The YouTube Video Recommendation System. InProceedings of the Fourth ACM Conference on Recommender Systems(Barcelona, Spain)(RecSys ’10). Association for Computing Machinery, New York, NY, USA, 293–296.https://doi.org/10.1145/1864708.1864770
- Davidson etal.(2010)↑ジェームズ・デイビッドソン、ベンジャミン・リーバルド、ジュンニング・リウ、パラシュ・ナンディ、テイラー・ヴァンブリート、ウラス・ガルギ、スジョイ・グプタ、ユー・ハ、マイク・ランバート、ブレイク・リビングストン、およびダサラティ・サンパス. 2010. YouTube動画推薦システム. 第4回ACM推薦システム会議の議事録（バルセロナ、スペイン）（RecSys '10）。計算機科学協会、ニューヨーク、NY、アメリカ、293–296. https://doi.org/10.1145/1864708.1864770
- Dupret and Piwowarski (2008)↑GeorgesE. Dupret and Benjamin Piwowarski. 2008.A User Browsing Model to Predict Search Engine Click Data from Past Observations.. InProceedings of the 31st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval(Singapore, Singapore)(SIGIR ’08). Association for Computing Machinery, New York, NY, USA, 331–338.https://doi.org/10.1145/1390334.1390392
- Dupret and Piwowarski (2008)↑ジョルジュ・E・デュプレとベンジャミン・ピウォワルスキー. 2008.過去の観察から検索エンジンのクリックデータを予測するユーザーブラウジングモデル. 第31回国際ACM SIGIR情報検索研究開発会議の議事録（シンガポール、シンガポール）（SIGIR '08）。計算機科学協会、ニューヨーク、NY、アメリカ、331–338. https://doi.org/10.1145/1390334.1390392
- Fu etal.(2023)↑Lingyue Fu, Jianghao Lin, Weiwen Liu, Ruiming Tang, Weinan Zhang, Rui Zhang, and Yong Yu. 2023.An F-Shape Click Model for Information Retrieval on Multi-Block Mobile Pages. InProceedings of the Sixteenth ACM International Conference on Web Search and Data Mining(Singapore, Singapore)(WSDM ’23). Association for Computing Machinery, New York, NY, USA, 1057–1065.https://doi.org/10.1145/3539597.3570365
- Fu etal.(2023)↑リンユエ・フー、ジャンハオ・リン、ウェイウェン・リウ、ルイミン・タン、ウェイナン・ジャン、ルイ・ジャン、およびヨン・ユー. 2023.マルチブロックモバイルページにおける情報検索のためのF字型クリックモデル. 第16回ACM国際ウェブ検索およびデータマイニング会議の議事録（シンガポール、シンガポール）（WSDM '23）。計算機科学協会、ニューヨーク、NY、アメリカ、1057–1065. https://doi.org/10.1145/3539597.3570365
- Gao etal.(2022b)↑Chongming Gao, Shijun Li, Yuan Zhang, Jiawei Chen, Biao Li, Wenqiang Lei, Peng Jiang, and Xiangnan He. 2022b.KuaiRand: An Unbiased Sequential Recommendation Dataset with Randomly Exposed Videos. InProceedings of the 31st ACM International Conference on Information and Knowledge Management(Atlanta, GA, USA)(CIKM ’22). 5pages.https://doi.org/10.1145/3511808.3557624
- Gao etal.(2022b)↑チョンミン・ガオ、シジュン・リ、ユアン・ジャン、ジアウェイ・チェン、ビャオ・リ、ウェンチアン・レイ、ペン・ジャン、およびシャンナン・ハ. 2022b.KuaiRand: ランダムに露出された動画を持つバイアスのない逐次推薦データセット. 第31回ACM国際情報および知識管理会議の議事録（アトランタ、GA、アメリカ）（CIKM '22）。5ページ。 https://doi.org/10.1145/3511808.3557624
- Gao etal.(2022a)↑Yunjun Gao, Yuntao Du, Yujia Hu, Lu Chen, Xinjun Zhu, Ziquan Fang, and Baihua Zheng. 2022a.Self-Guided Learning to Denoise for Robust Recommendation. InProceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval(Madrid, Spain)(SIGIR ’22). Association for Computing Machinery, New York, NY, USA, 1412–1422.https://doi.org/10.1145/3477495.3532059
- Gao etal.(2022a)↑ユンジュン・ガオ、ユンタオ・ドゥ、ユージア・フー、ルー・チェン、シンジュン・ジュ、ズイチュアン・ファン、およびバイファ・ジェン. 2022a.堅牢な推薦のための自己指導型学習によるノイズ除去. 第45回国際ACM SIGIR情報検索研究開発会議の議事録（マドリード、スペイン）（SIGIR '22）。計算機科学協会、ニューヨーク、NY、アメリカ、1412–1422. https://doi.org/10.1145/3477495.3532059
- He etal.(2023)↑Xiangnan He, Yang Zhang, Fuli Feng, Chonggang Song, Lingling Yi, Guohui Ling, and Yongdong Zhang. 2023.Addressing Confounding Feature Issue for Causal Recommendation.ACM Trans. Inf. Syst.41, 3, Article 53 (feb 2023), 23pages.https://doi.org/10.1145/3559757
- He etal.(2023)↑シャンナン・ハ、ヤン・ジャン、フーリ・フェン、チョンガン・ソン、リンリン・イー、グオフイ・リン、およびヨンドン・ジャン. 2023.因果推薦のための混乱特徴問題への対処. ACM Trans. Inf. Syst. 41, 3, 記事53 (2023年2月)、23ページ。 https://doi.org/10.1145/3559757
- Jacobs etal.(1991)↑RobertA. Jacobs, MichaelI. Jordan, StevenJ. Nowlan, and GeoffreyE. Hinton. 1991.Adaptive Mixtures of Local Experts.Neural Comput.3, 1 (1991), 79–87.
- Jacobs etal.(1991)↑ロバートA. ジェイコブス、マイケルI. ジョーダン、スティーブンJ. ノーラン、およびジェフリーE. ヒントン. 1991.適応型ローカルエキスパートの混合. Neural Comput. 3, 1 (1991), 79–87.
- Joachims etal.(2017)↑Thorsten Joachims, Adith Swaminathan, and Tobias Schnabel. 2017.Unbiased Learning-to-Rank with Biased Feedback. InProceedings of the Tenth ACM International Conference on Web Search and Data Mining(Cambridge, United Kingdom)(WSDM ’17). ACM, New York, NY, USA, 781–789.https://doi.org/10.1145/3018661.3018699
- Joachims etal.(2017)↑トルステン・ジョアヒムス、アディス・スワミナサン、およびトビアス・シュナーベル. 2017.バイアスのあるフィードバックを用いたバイアスのないランキング学習. 第10回ACM国際ウェブ検索およびデータマイニング会議の議事録（ケンブリッジ、イギリス）（WSDM '17）。ACM、ニューヨーク、NY、アメリカ、781–789. https://doi.org/10.1145/3018661.3018699
- Li etal.(2016)↑Yan Li, KevinS. Xu, and ChandanK. Reddy. 2016.Regularized Parametric Regression for High-dimensional Survival Analysis. InProceedings of the 2016 SIAM International Conference on Data Mining, Miami, Florida, USA, May 5-7, 2016, SanjayChawla Venkatasubramanian and WagnerMeira Jr. (Eds.). SIAM, 765–773.https://doi.org/10.1137/1.9781611974348.86
- Li etal.(2016)↑ヤン・リー、ケビンS. シュ、チャンダンK. レディ. 2016.高次元生存分析のための正則化パラメトリック回帰. 2016年SIAM国際データマイニング会議の議事録、マイアミ、フロリダ州、アメリカ、2016年5月5-7日、サンジェイ・チャウラ・ヴェンカタスブラマニアンおよびワグナー・メイラ・ジュニア（編）。SIAM、765–773. https://doi.org/10.1137/1.9781611974348.86
- Liu etal.(2019)↑Shang Liu, Zhenzhong Chen, Hongyi Liu, and Xinghai Hu. 2019.User-Video Co-Attention Network for Personalized Micro-Video Recommendation. InThe World Wide Web Conference(San Francisco, CA, USA)(WWW ’19). Association for Computing Machinery, New York, NY, USA, 3020–3026.https://doi.org/10.1145/3308558.3313513
- Liu etal.(2019)↑シャング・リウ、ゼンジョン・チェン、ホンイー・リウ、およびシンハイ・フー. 2019.個別化されたマイクロビデオ推薦のためのユーザー-ビデオ共同注意ネットワーク. ワールドワイドウェブ会議（サンフランシスコ、CA、アメリカ）（WWW '19）。計算機科学協会、ニューヨーク、NY、アメリカ、3020–3026. https://doi.org/10.1145/3308558.3313513
- Liu etal.(2021)↑Yiyu Liu, Qian Liu, Yu Tian, Changping Wang, Yanan Niu, Yang Song, and Chenliang Li. 2021.Concept-Aware Denoising Graph Neural Network for Micro-Video Recommendation. InProceedings of the 30th ACM International Conference on Information Knowledge Management(Virtual Event, Queensland, Australia)(CIKM ’21). Association for Computing Machinery, New York, NY, USA, 1099–1108.https://doi.org/10.1145/3459637.3482417
- Liu etal.(2021)↑イーユー・リウ、チャン・リウ、ユ・ティアン、チャンピン・ワン、ヤナン・ニウ、ヤン・ソン、およびチェンリャン・リ. 2021.マイクロビデオ推薦のための概念認識ノイズ除去グラフニューラルネットワーク. 第30回ACM国際情報および知識管理会議の議事録（バーチャルイベント、クイーンズランド、オーストラリア）（CIKM '21）。計算機科学協会、ニューヨーク、NY、アメリカ、1099–1108. https://doi.org/10.1145/3459637.3482417
- Ma etal.(2018)↑Jiaqi Ma, Zhe Zhao, Xinyang Yi, Jilin Chen, Lichan Hong, and EdH. Chi. 2018.Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts. InProceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, KDD 2018, London, UK, August 19-23, 2018. ACM, 1930–1939.
- Ma etal.(2018)↑ジャキ・マ、ゼ・ジャオ、シンヤン・イー、ジリン・チェン、リチャン・ホン、およびエドH. チー. 2018.マルチゲートエキスパートの混合を用いたマルチタスク学習におけるタスク関係のモデリング. 第24回ACM SIGKDD国際知識発見およびデータマイニング会議の議事録、KDD 2018、ロンドン、イギリス、2018年8月19-23日。ACM、1930–1939.
- Mao etal.(2018)↑Jiaxin Mao, Cheng Luo, Min Zhang, and Shaoping Ma. 2018.Constructing Click Models for Mobile Search. InThe 41st International ACM SIGIR Conference on Research & Development in Information Retrieval(Ann Arbor, MI, USA)(SIGIR ’18). Association for Computing Machinery, New York, NY, USA, 775–784.https://doi.org/10.1145/3209978.3210060
- Mao etal.(2018)↑ジャイシン・マオ、チェン・ルオ、ミン・ジャン、およびシャオピング・マ. 2018.モバイル検索のためのクリックモデルの構築. 第41回国際ACM SIGIR情報検索研究開発会議（アナーバー、ミシガン州、アメリカ）（SIGIR '18）。計算機科学協会、ニューヨーク、NY、アメリカ、775–784. https://doi.org/10.1145/3209978.3210060
- Park etal.(2017)↑Yoojin Park, Jinoh Oh, and Hwanjo Yu. 2017.RecTime: Real-time recommender system for online broadcasting.Information Sciences409 (2017), 1–16.
- Park etal.(2017)↑ユジン・パク、ジノ・オ、ハンジョ・ユ. 2017.RecTime: オンライン放送のためのリアルタイム推薦システム. 情報科学 409 (2017), 1–16.
- Qin etal.(2023)↑Jiarui Qin, Jiachen Zhu, Yankai Liu, Junchao Gao, Jianjie Ying, Chaoxiong Liu, Ding Wang, Junlan Feng, Chao Deng, Xiaozheng Wang, etal.2023.Learning to distinguish multi-user coupling behaviors for tv recommendation. InProceedings of the Sixteenth ACM International Conference on Web Search and Data Mining. 204–212.
- Qin etal.(2023)↑ジアルイ・チン、ジアチェン・ジュ、ヤンカイ・リウ、ジュンチャオ・ガオ、ジアンジェ・イン、チャオシオン・リウ、ディン・ワン、ジュンラン・フェン、チャオ・デン、シャオジェン・ワン、他. 2023.テレビ推薦のためのマルチユーザー結合行動を区別する学習. 第16回ACM国際ウェブ検索およびデータマイニング会議の議事録。204–212.
- Quan etal.(2023)↑Yuhan Quan, Jingtao Ding, Chen Gao, Nian Li, Lingling Yi, Depeng Jin, and Yong Li. 2023.Alleviating Video-length Effect for Micro-video Recommendation.ACM Trans. Inf. Syst.42, 2, Article 44 (nov 2023), 24pages.https://doi.org/10.1145/3617826
- Quan etal.(2023)↑ユーハン・クアン、ジンタオ・ディン、チェン・ガオ、ニアン・リー、リンリン・イー、デペン・ジン、およびヨン・リー. 2023.マイクロビデオ推薦のための動画長効果の緩和. ACM Trans. Inf. Syst. 42, 2, 記事44 (2023年11月)、24ページ。 https://doi.org/10.1145/3617826
- Rendle (2012)↑Steffen Rendle. 2012.Factorization Machines with LibFM.ACM Trans. Intell. Syst
- Rendle (2012)↑ステッフェン・レンデル. 2012. LibFMを用いた因子分解マシン. ACM Trans. Intell. Syst



. Inf. Syst.42, 2, Article 44 (nov 2023), 24pages.https://doi.org/10.1145/3617826
. Inf. Syst.42, 2, Article 44 (2023年11月), 24ページ。https://doi.org/10.1145/3617826

- Rendle (2012)↑Steffen Rendle. 2012.Factorization Machines with LibFM.ACM Trans. Intell. Syst. Technol.3, 3, Article 57 (may 2012), 22pages.https://doi.org/10.1145/2168752.2168771
- Rendle (2012)↑Steffen Rendle. 2012. LibFMを用いた因子分解マシン。ACMトランザクションズ インテリジェントシステム技術 3, 3, Article 57 (2012年5月), 22ページ。https://doi.org/10.1145/2168752.2168771

- Saito etal.(2020)↑Yuta Saito, Suguru Yaginuma, Yuta Nishino, Hayato Sakata, and Kazuhide Nakata. 2020.Unbiased Recommender Learning from Missing-Not-At-Random Implicit Feedback. InProceedings of the 13th International Conference on Web Search and Data Mining(Houston, TX, USA)(WSDM ’20). Association for Computing Machinery, New York, NY, USA, 501–509.https://doi.org/10.1145/3336191.3371783
- Saito et al. (2020)↑斉藤優太、八木沼優、西野優、坂田隼人、中田和秀。2020年。欠落した非ランダムな暗黙のフィードバックからのバイアスのないレコメンダー学習。第13回国際ウェブ検索およびデータマイニング会議の論文集（アメリカ・テキサス州ヒューストン）（WSDM '20）。ACM、ニューヨーク、NY、USA、501–509。https://doi.org/10.1145/3336191.3371783

- Schnabel etal.(2016)↑Tobias Schnabel, Adith Swaminathan, Ashudeep Singh, Navin Chandak, and Thorsten Joachims. 2016.Recommendations as treatments: Debiasing learning and evaluation. Ininternational conference on machine learning. PMLR, 1670–1679.
- Schnabel et al. (2016)↑トビアス・シュナベル、アディス・スワミナサン、アシュディープ・シン、ナビン・チャンダク、トルステン・ジョアヒムス。2016年。推薦を治療として：学習と評価のバイアス除去。国際機械学習会議において。PMLR、1670–1679。

- Song etal.(2019)↑Weiping Song, Chence Shi, Zhiping Xiao, Zhijian Duan, Yewen Xu, Ming Zhang, and Jian Tang. 2019.AutoInt: Automatic Feature Interaction Learning via Self-Attentive Neural Networks. InProceedings of the 28th ACM International Conference on Information and Knowledge Management(Beijing, China)(CIKM ’19). Association for Computing Machinery, New York, NY, USA, 1161–1170.https://doi.org/10.1145/3357384.3357925
- Song et al. (2019)↑ソン・ウェイピング、シー・チェン、シャオ・ジーピン、ドゥアン・ジージアン、シュー・イェウェン、チャン・ミン、タン・ジアン。2019年。AutoInt：自己注意型ニューラルネットワークによる自動特徴相互作用学習。第28回ACM国際情報および知識管理会議の論文集（中国・北京）（CIKM '19）。ACM、ニューヨーク、NY、USA、1161–1170。https://doi.org/10.1145/3357384.3357925

- Tang etal.(2020)↑Hongyan Tang, Junning Liu, Ming Zhao, and Xudong Gong. 2020.Progressive Layered Extraction (PLE): A Novel Multi-Task Learning (MTL) Model for Personalized Recommendations. InRecSys 2020: Fourteenth ACM Conference on Recommender Systems, Virtual Event, Brazil, September 22-26, 2020. ACM, 269–278.
- Tang et al. (2020)↑唐紅燕、劉俊寧、趙明、龔旭東。2020年。Progressive Layered Extraction (PLE)：パーソナライズド推薦のための新しいマルチタスク学習（MTL）モデル。RecSys 2020：第14回ACM推薦システム会議、バーチャルイベント、ブラジル、2020年9月22-26日。ACM、269–278。

- Tang etal.(2023a)↑Shisong Tang, Qing Li, Dingmin Wang, Ci Gao, Wentao Xiao, Dan Zhao, Yong Jiang, Qian Ma, and Aoyang Zhang. 2023a.Counterfactual Video Recommendation for Duration Debiasing. InProceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining(¡conf-loc¿, ¡city¿Long Beach¡/city¿, ¡state¿CA¡/state¿, ¡country¿USA¡/country¿, ¡/conf-loc¿)(KDD ’23). Association for Computing Machinery, New York, NY, USA, 4894–4903.https://doi.org/10.1145/3580305.3599797
- Tang et al. (2023a)↑唐士松、李青、王丁敏、曹慈、肖文韬、趙丹、江勇、馬倩、張奧揚。2023a。持続時間のバイアス除去のための反事実的ビデオ推薦。第29回ACM SIGKDD知識発見とデータマイニング会議の論文集（ロングビーチ、CA、USA）（KDD '23）。ACM、ニューヨーク、NY、USA、4894–4903。https://doi.org/10.1145/3580305.3599797

- Tang etal.(2023b)↑Shisong Tang, Qing Li, Dingmin Wang, Ci Gao, Wentao Xiao, Dan Zhao, Yong Jiang, Qian Ma, and Aoyang Zhang. 2023b.Counterfactual Video Recommendation for Duration Debiasing. InProceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining(Long Beach, CA, USA)(KDD ’23). Association for Computing Machinery, New York, NY, USA, 4894–4903.https://doi.org/10.1145/3580305.3599797
- Tang et al. (2023b)↑唐士松、李青、王丁敏、曹慈、肖文韬、趙丹、江勇、馬倩、張奧揚。2023b。持続時間のバイアス除去のための反事実的ビデオ推薦。第29回ACM SIGKDD知識発見とデータマイニング会議の論文集（ロングビーチ、CA、USA）（KDD '23）。ACM、ニューヨーク、NY、USA、4894–4903。https://doi.org/10.1145/3580305.3599797

- Thompson and Spencer (1966)↑RichardF Thompson and WilliamA Spencer. 1966.Habituation: a model phenomenon for the study of neuronal substrates of behavior.Psychological review73, 1 (1966), 16.
- Thompson and Spencer (1966)↑リチャード・F・トンプソン、ウィリアム・A・スペンサー。1966年。習慣化：行動の神経基盤の研究のためのモデル現象。心理学レビュー 73, 1 (1966), 16。

- Vriend (1996)↑NicolaasJ Vriend. 1996.Rational behavior and economic theory.Journal of Economic Behavior & Organization29, 2 (1996), 263–285.
- Vriend (1996)↑ニコラス・J・ブリント。1996年。合理的行動と経済理論。経済行動と組織のジャーナル 29, 2 (1996), 263–285。

- Wang etal.(2019)↑Ping Wang, Yan Li, and ChandanK Reddy. 2019.Machine learning for survival analysis: A survey.ACM Computing Surveys (CSUR)51, 6 (2019), 1–36.
- Wang et al. (2019)↑王平、李燕、チャンダン・K・レディ。2019年。生存分析のための機械学習：調査。ACMコンピューティングサーベイ（CSUR）51, 6 (2019), 1–36。

- Wang etal.(2017)↑Ruoxi Wang, Bin Fu, Gang Fu, and Mingliang Wang. 2017.Deep & Cross Network for Ad Click Predictions. InProceedings of the ADKDD’17(Halifax, NS, Canada)(ADKDD’17). Association for Computing Machinery, New York, NY, USA, Article 12, 7pages.https://doi.org/10.1145/3124749.3124754
- Wang et al. (2017)↑王若西、傅斌、傅剛、王明亮。2017年。広告クリック予測のためのDeep & Cross Network。ADKDD'17の論文集（カナダ・ハリファックス）（ADKDD'17）。ACM、ニューヨーク、NY、USA、Article 12、7ページ。https://doi.org/10.1145/3124749.3124754

- Wang etal.(2021)↑Wenjie Wang, Fuli Feng, Xiangnan He, Liqiang Nie, and Tat-Seng Chua. 2021.Denoising Implicit Feedback for Recommendation. InProceedings of the 14th ACM International Conference on Web Search and Data Mining(Virtual Event, Israel)(WSDM ’21). Association for Computing Machinery, New York, NY, USA, 373–381.https://doi.org/10.1145/3437963.3441800
- Wang et al. (2021)↑王文杰、馮富麗、何向南、聶立強、蔡達生。2021年。推薦のための暗黙のフィードバックのノイズ除去。第14回ACM国際ウェブ検索およびデータマイニング会議の論文集（バーチャルイベント、イスラエル）（WSDM '21）。ACM、ニューヨーク、NY、USA、373–381。https://doi.org/10.1145/3437963.3441800

- Wang etal.(2016)↑Xuanhui Wang, Michael Bendersky, Donald Metzler, and Marc Najork. 2016.Learning to Rank with Selection Bias in Personal Search. InProceedings of the 39th International ACM SIGIR Conference on Research and Development in Information Retrieval(Pisa, Italy)(SIGIR ’16). ACM, New York, NY, USA, 115–124.
- Wang et al. (2016)↑王選輝、マイケル・ベンダースキー、ドナルド・メッツラー、マーク・ナイヨーク。2016年。個人検索における選択バイアスを伴うランキング学習。第39回国際ACM SIGIR情報検索に関する会議の論文集（イタリア・ピサ）（SIGIR '16）。ACM、ニューヨーク、NY、USA、115–124。

- Wang etal.(2022)↑Yu Wang, Xin Xin, Zaiqiao Meng, JoemonM Jose, Fuli Feng, and Xiangnan He. 2022.Learning Robust Recommenders through Cross-Model Agreement. InProceedings of the ACM Web Conference 2022(Virtual Event, Lyon, France)(WWW ’22). Association for Computing Machinery, New York, NY, USA, 2015–2025.https://doi.org/10.1145/3485447.3512202
- Wang et al. (2022)↑王宇、辛辛、孟在喬、ジョエモン・M・ホセ、馮富麗、何向南。2022年。クロスモデル合意を通じてロバストなレコメンダーを学習する。ACMウェブ会議2022の論文集（バーチャルイベント、フランス・リヨン）（WWW '22）。ACM、ニューヨーク、NY、USA、2015–2025。https://doi.org/10.1145/3485447.3512202

- Wei etal.(2021)↑Tianxin Wei, Fuli Feng, Jiawei Chen, Ziwei Wu, Jinfeng Yi, and Xiangnan He. 2021.Model-Agnostic Counterfactual Reasoning for Eliminating Popularity Bias in Recommender System. InProceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery Data Mining(Virtual Event, Singapore)(KDD ’21). Association for Computing Machinery, New York, NY, USA, 1791–1800.https://doi.org/10.1145/3447548.3467289
- Wei et al. (2021)↑韋天鑫、馮富麗、陳家偉、吳子偉、易金峰、何向南。2021年。推薦システムにおける人気バイアスを排除するためのモデル非依存の反事実的推論。第27回ACM SIGKDD知識発見データマイニング会議の論文集（バーチャルイベント、シンガポール）（KDD '21）。ACM、ニューヨーク、NY、USA、1791–1800。https://doi.org/10.1145/3447548.3467289

- Wu etal.(2022)↑Peng Wu, Haoxuan Li, Yuhao Deng, Wenjie Hu, Quanyu Dai, Zhenhua Dong, Jie Sun, Rui Zhang, and Xiao-Hua Zhou. 2022.On the Opportunity of Causal Learning in Recommendation Systems: Foundation, Estimation, Prediction and Challenges. InProceedings of the Thirty-First International Joint Conference on Artificial Intelligence, IJCAI-22. 5646–5653.Survey Track.
- Wu et al. (2022)↑呉鵬、李浩軒、邓宇豪、胡文杰、戴全宇、董振華、孫杰、張瑞、周小華。2022年。推薦システムにおける因果学習の機会について：基礎、推定、予測と課題。第31回国際共同人工知能会議の論文集、IJCAI-22。5646–5653。調査トラック。

- Xie etal.(2023)↑Ruobing Xie, Lin Ma, Shaoliang Zhang, Feng Xia, and Leyu Lin. 2023.Reweighting Clicks with Dwell Time in Recommendation. InCompanion Proceedings of the ACM Web Conference 2023(Austin, TX, USA)(WWW ’23 Companion). Association for Computing Machinery, New York, NY, USA, 341–345.https://doi.org/10.1145/3543873.3584624
- Xie et al. (2023)↑謝若冰、馬琳、張少良、夏峰、林樂宇。2023年。推薦における滞在時間を用いたクリックの再重み付け。ACMウェブ会議2023の補足論文集（アメリカ・テキサス州オースティン）（WWW '23 Companion）。ACM、ニューヨーク、NY、USA、341–345。https://doi.org/10.1145/3543873.3584624

- Yuan etal.(2020)↑Bowen Yuan, Yaxu Liu, Jui-Yang Hsia, Zhenhua Dong, and Chih-Jen Lin. 2020.Unbiased Ad Click Prediction for Position-Aware Advertising Systems. InFourteenth ACM Conference on Recommender Systems(Virtual Event, Brazil)(RecSys ’20). ACM, New York, NY, USA, 368–377.https://doi.org/10.1145/3383313.3412241
- Yuan et al. (2020)↑袁博文、劉雅旭、謝瑞揚、董振華、林志仁。2020年。位置を考慮した広告システムのためのバイアスのない広告クリック予測。第14回ACM推薦システム会議の論文集（バーチャルイベント、ブラジル）（RecSys '20）。ACM、ニューヨーク、NY、USA、368–377。https://doi.org/10.1145/3383313.3412241

- Zhan etal.(2022)↑Ruohan Zhan, Changhua Pei, Qiang Su, Jianfeng Wen, Xueliang Wang, Guanyu Mu, Dong Zheng, Peng Jiang, and Kun Gai. 2022.Deconfounding Duration Bias in Watch-Time Prediction for Video Recommendation. InProceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining(Washington DC, USA)(KDD ’22). Association for Computing Machinery, New York, NY, USA, 4472–4481.https://doi.org/10.1145/3534678.3539092
- Zhan et al. (2022)↑詹若涵、裴常華、蘇強、文建峰、王雪亮、穆冠宇、鄭東、姜鵬、蓋昆。2022年。ビデオ推薦のための視聴時間予測における持続時間バイアスの除去。第28回ACM SIGKDD知識発見とデータマイニング会議の論文集（アメリカ・ワシントンDC）（KDD '22）。ACM、ニューヨーク、NY、USA、4472–4481。https://doi.org/10.1145/3534678.3539092

- Zhang etal.(2021)↑Yang Zhang, Fuli Feng, Xiangnan He, Tianxin Wei, Chonggang Song, Guohui Ling, and Yongdong Zhang. 2021.Causal Intervention for Leveraging Popularity Bias in Recommendation. InProceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval(Virtual Event, Canada)(SIGIR ’21). ACM, New York, NY, USA, 11–20.https://doi.org/10.1145/3404835.3462875
- Zhang et al. (2021)↑張揚、馮富麗、何向南、韋天鑫、宋崇剛、凌國輝、張永東。2021年。推薦における人気バイアスを活用するための因果介入。第44回国際ACM SIGIR情報検索に関する会議の論文集（バーチャルイベント、カナダ）（SIGIR '21）。ACM、ニューヨーク、NY、USA、11–20。https://doi.org/10.1145/3404835.3462875

- Zhao etal.(2023)↑Haiyuan Zhao, Lei Zhang, Jun Xu, Guohao Cai, Zhenhua Dong, and Ji-Rong Wen. 2023.Uncovering User Interest from Biased and Noised Watch Time in Video Recommendation. InProceedings of the 17th ACM Conference on Recommender Systems(Singapore, Singapore)(RecSys ’23). Association for Computing Machinery, New York, NY, USA, 528–539.https://doi.org/10.1145/3604915.3608797
- Zhao et al. (2023)↑趙海源、張磊、徐俊、蔡國豪、董振華、文紀榮。2023年。ビデオ推薦におけるバイアスとノイズのある視聴時間からのユーザーの興味の発見。第17回ACM推薦システム会議の論文集（シンガポール）（RecSys '23）。ACM、ニューヨーク、NY、USA、528–539。https://doi.org/10.1145/3604915.3608797

- Zhao etal.(2019)↑Zhe Zhao, Lichan Hong, Li Wei, Jilin Chen, Aniruddh Nath, Shawn Andrews, Aditee Kumthekar, Maheswaran Sathiamoorthy, Xinyang Yi, and EdH. Chi. 2019.Recommending what video to watch next: a multitask ranking system. InProceedings of the 13th ACM Conference on Recommender Systems, RecSys 2019, Copenhagen, Denmark, September 16-20, 2019. ACM, 43–51.
- Zhao et al. (2019)↑趙哲、洪立燦、李偉、陳吉霖、阿尼魯德・納特、肖恩・アンドリュース、アディテ・クムテカール、マヘスワラン・サティアモーティ、イー・シンヤン、エド・H・チ。2019年。次に見るべきビデオの推薦：マルチタスクランキングシステム。第13回ACM推薦システム会議の論文集、RecSys 2019、デンマーク・コペンハーゲン、2019年9月16-20日。ACM、43–51。

- Zheng etal.(2022)↑Yu Zheng, Chen Gao, Jingtao Ding, Lingling Yi, Depeng Jin, Yong Li, and Meng Wang. 2022.DVR: Micro-Video Recommendation Optimizing Watch-Time-Gain under Duration Bias. InProceedings of the 30th ACM International Conference on Multimedia(Lisboa, Portugal)(MM ’22). Association for Computing Machinery, New York, NY, USA, 334–345.https://doi.org/10.1145/3503161.3548428
- Zheng et al. (2022)↑鄭宇、高晨、丁景濤、易玲玲、金德鵬、李勇、王萌。2022年。DVR：持続時間バイアスの下で視聴時間利益を最適化するマイクロビデオ推薦。第30回ACM国際マルチメディア会議の論文集（ポルトガル・リスボン）（MM '22）。ACM、ニューヨーク、NY、USA、334–345。https://doi.org/10.1145/3503161.3548428

- Zheng etal.(2021)↑Yu Zheng, Chen Gao, Xiang Li, Xiangnan He, Yong Li, and Depeng Jin. 2021.Disentangling User Interest and Conformity for Recommendation with Causal Embedding. InProceedings of the Web Conference 2021(Ljubljana, Slovenia)(WWW ’21). ACM, New York, NY, USA, 2980–2991.https://doi.org/10.1145/3442381.3449788
- Zheng et al. (2021)↑鄭宇、高晨、李翔、何向南、李勇、金德鵬。2021年。因果埋め込みを用いた推薦におけるユーザーの興味と適合性の分離。ウェブ会議2021の論文集（スロベニア・リュブリャナ）（WWW '21）。ACM、ニューヨーク、NY、USA、2980–2991。https://doi.org/10.1145/3442381.3449788

- Zhou etal.(2018)↑Tengfei Zhou, Hui Qian, Zebang Shen, Chao Zhang, Chengwei Wang, Shichen Liu, and Wenwu Ou. 2018.JUMP: a joint predictor for user click and dwell time. InProceedings of the 27th International Joint Conference on Artificial Intelligence. AAAI Press. 3704–3710.
- Zhou et al. (2018)↑周騰飛、錢輝、沈澤邦、張超、王成偉、劉士琛、歐文武。2018年。JUMP：ユーザーのクリックと滞在時間のための共同予測器。第27回国際共同人工知能会議の論文集。AAAIプレス。3704–3710。

(1)↑
Ai etal.(2018)↑
.
Qingyao Ai, Keping Bi, Cheng Luo, Jiafeng Guo, and W.Bruce Croft. 2018.
Unbiased Learning to Rank with Unbiased Propensity Estimation. InThe 41st International ACM SIGIR Conference on Research Development in Information Retrieval(Ann Arbor, MI, USA)(SIGIR ’18). ACM, New York, NY, USA, 385–394.
https://doi.org/10.1145/3209978.3209986
(1)↑
Ai et al. (2018)↑
.
アイ・チンヤオ、ビ・ケーピン、ルオ・チェン、グオ・ジャフェン、W・ブルース・クロフト。2018年。
バイアスのない傾向推定を用いたバイアスのないランキング学習。第41回国際ACM SIGIR情報検索に関する会議（アメリカ・ミシガン州アナーバー）（SIGIR '18）。ACM、ニューヨーク、NY、USA、385–394。
https://doi.org/10.1145/3209978.3209986

Aleskerov etal.(2007)↑
.
Fuad Aleskerov, Denis Bouyssou, and Bernard Monjardet. 2007.
Utility maximization, choice and preference. Vol.16.
Springer Science & Business Media.
Aleskerov et al. (2007)↑
.
フアド・アレスケロフ、ドニス・ブイッソー、ベルナール・モンジャルデ。2007年。
効用最大化、選択と嗜好。第16巻。
スプリンガー・サイエンス・ビジネス・メディア。

Amemiya (1984)↑
Takeshi Amemiya. 1984.
Tobit models: A survey.
Journal of econometrics24, 1-2 (1984), 3–61.
Amemiya (1984)↑
雨宮武。1984年。
トビットモデル：調査。
計量経済学ジャーナル 24, 1-2 (1984), 3–61。

Borisov etal.(2016)↑
.
Alexey Borisov, Ilya Markov, Maarten de Rijke, and Pavel Serdyukov. 2016.
A Neural Click Model for Web Search. InProceedings of the 25th International Conference on World Wide Web(Montréal, Québec, Canada)(WWW ’16). International World Wide Web Conferences Steering Committee, Republic and Canton of Geneva, CHE, 531–541.
https://doi.org/10.1145/2872427.2883033
Borisov et al. (2016)↑
.
アレクセイ・ボリソフ、イリヤ・マルコフ、マールテン・デ・ライケ、パベル・セルデュコフ。2016年。
ウェブ検索のためのニューラルクリックモデル。第25回国際ワールドワイドウェブ会議の論文集（カナダ・モントリオール）（WWW '16）。国際ワールドワイドウェブ会議運営委員会、ジュネーブ、スイス、531–541。
https://doi.org/10.1145/2872427.2883033

Cai etal.(2023)↑
.
Qingpeng Cai, Zhenghai Xue, Chi Zhang, Wanqi Xue, Shuchang Liu, Ruohan Zhan, Xueliang Wang, Tianyou Zuo, Wentao Xie, Dong Zheng, Peng Jiang, and Kun Gai. 2023.
Two-Stage Constrained Actor-Critic for Short Video Recommendation. InProceedings of the ACM Web Conference 2023, WWW 2023, Austin, TX, USA, 30 April 2023 - 4 May 2023. ACM, 865–875.
Cai et al. (2023)↑
.
蔡清鵬、薛正海、張琦、薛萬琦、劉書暢、詹若涵、王雪亮、左天佑、謝文韜、鄭東、姜鵬、蓋昆。2023年。
短編動画推薦のための二段階制約付きアクター・クリティック。ACMウェブ会議2023の論文集、WWW 2023、アメリカ・テキサス州オースティン、2023年4月30日 - 5月4日。ACM、865–875。

Chang etal.(2023)↑
.
Jianxin Chang, Chenbin Zhang, Yiqun Hui, Dewei Leng, Yanan Niu, Yang Song, and Kun Gai



. ACM, 865–875.
. ACM, 865–875.

Chang etal.(2023)↑
Chang etal.(2023)↑

Jianxin Chang, Chenbin Zhang, Yiqun Hui, Dewei Leng, Yanan Niu, Yang Song, and Kun Gai. 2023.
Jianxin Chang, Chenbin Zhang, Yiqun Hui, Dewei Leng, Yanan Niu, Yang Song, および Kun Gai. 2023.

PEPNet: Parameter and Embedding Personalized Network for Infusing with Personalized Prior Information.
PEPNet: パラメータと埋め込みの個人化ネットワークによる個人化された事前情報の注入。

CoRRabs/2302.01115 (2023).
CoRRabs/2302.01115 (2023).

Chapelle and Zhang (2009)↑
Chapelle and Zhang (2009)↑

Olivier Chapelle and Ya Zhang. 2009.
Olivier Chapelle と Ya Zhang. 2009.

A Dynamic Bayesian Network Click Model for Web Search Ranking. 
ウェブ検索ランキングのための動的ベイジアンネットワーククリックモデル。

InProceedings of the 18th International Conference on World Wide Web(Madrid, Spain)(WWW ’09). 
第18回国際ワールドワイドウェブ会議の議事録（スペイン、マドリード）（WWW ’09）。

Association for Computing Machinery, New York, NY, USA, 1–10.
コンピュータ機械学会、ニューヨーク、NY、USA、1–10。

https://doi.org/10.1145/1526709.1526711
https://doi.org/10.1145/1526709.1526711

Chen etal.(2020)↑
Chen etal.(2020)↑

Jia Chen, Jiaxin Mao, Yiqun Liu, Min Zhang, and Shaoping Ma. 2020.
Jia Chen、Jiaxin Mao、Yiqun Liu、Min Zhang、および Shaoping Ma. 2020.

A Context-Aware Click Model for Web Search. 
ウェブ検索のためのコンテキスト対応クリックモデル。

InProceedings of the 13th International Conference on Web Search and Data Mining(Houston, TX, USA)(WSDM ’20). 
第13回国際ウェブ検索およびデータマイニング会議の議事録（アメリカ、ヒューストン）（WSDM ’20）。

Association for Computing Machinery, New York, NY, USA, 88–96.
コンピュータ機械学会、ニューヨーク、NY、USA、88–96。

https://doi.org/10.1145/3336191.3371819
https://doi.org/10.1145/3336191.3371819

Chen etal.(2021)↑
Chen etal.(2021)↑

Mouxiang Chen, Chenghao Liu, Jianling Sun, and StevenC.H. Hoi. 2021.
Mouxiang Chen、Chenghao Liu、Jianling Sun、および StevenC.H. Hoi. 2021.

Adapting Interactional Observation Embedding for Counterfactual Learning to Rank. 
反事実的ランキング学習のための相互作用観察埋め込みの適応。

InProceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval(Virtual Event, Canada)(SIGIR ’21). 
第44回国際ACM SIGIR情報検索研究開発会議の議事録（バーチャルイベント、カナダ）（SIGIR ’21）。

Association for Computing Machinery, New York, NY, USA, 285–294.
コンピュータ機械学会、ニューヨーク、NY、USA、285–294。

https://doi.org/10.1145/3404835.3462901
https://doi.org/10.1145/3404835.3462901

Cho etal.(2019)↑
Cho etal.(2019)↑

Kyung-Jae Cho, Yeon-Chang Lee, Kyungsik Han, Jaeho Choi, and Sang-Wook Kim. 2019.
Kyung-Jae Cho、Yeon-Chang Lee、Kyungsik Han、Jaeho Choi、および Sang-Wook Kim. 2019.

No, that’s not my feedback: TV show recommendation using watchable interval. 
いいえ、それは私のフィードバックではありません：視聴可能なインターバルを使用したテレビ番組の推薦。

In2019 IEEE 35th International Conference on Data Engineering (ICDE). 
2019年IEEE第35回データ工学国際会議（ICDE）において。

IEEE, 316–327.
IEEE、316–327。

Chuklin etal.(2016)↑
Chuklin etal.(2016)↑

Aleksandr Chuklin, Ilya Markov, and Maarten de Rijke. 2016.
Aleksandr Chuklin、Ilya Markov、および Maarten de Rijke. 2016.

Click Models for Web Search and Their Applications to IR: WSDM 2016 Tutorial. 
ウェブ検索のためのクリックモデルとその情報検索への応用：WSDM 2016 チュートリアル。

InProceedings of the Ninth ACM International Conference on Web Search and Data Mining(San Francisco, California, USA)(WSDM ’16). 
第9回ACM国際ウェブ検索およびデータマイニング会議の議事録（アメリカ、サンフランシスコ）（WSDM ’16）。

Association for Computing Machinery, New York, NY, USA, 689–690.
コンピュータ機械学会、ニューヨーク、NY、USA、689–690。

https://doi.org/10.1145/2835776.2855113
https://doi.org/10.1145/2835776.2855113

Covington etal.(2016a)↑
Covington etal.(2016a)↑

Paul Covington, Jay Adams, and Emre Sargin. 2016a.
Paul Covington、Jay Adams、および Emre Sargin. 2016a.

Deep Neural Networks for YouTube Recommendations. 
YouTube推薦のための深層ニューラルネットワーク。

InProceedings of the 10th ACM Conference on Recommender Systems(Boston, Massachusetts, USA)(RecSys ’16). 
第10回ACM推薦システム会議の議事録（アメリカ、ボストン）（RecSys ’16）。

Association for Computing Machinery, New York, NY, USA, 191–198.
コンピュータ機械学会、ニューヨーク、NY、USA、191–198。

https://doi.org/10.1145/2959100.2959190
https://doi.org/10.1145/2959100.2959190

Covington etal.(2016b)↑
Covington etal.(2016b)↑

Paul Covington, Jay Adams, and Emre Sargin. 2016b.
Paul Covington、Jay Adams、および Emre Sargin. 2016b.

Deep Neural Networks for YouTube Recommendations. 
YouTube推薦のための深層ニューラルネットワーク。

InProceedings of the 10th ACM Conference on Recommender Systems, Boston, MA, USA, September 15-19, 2016. 
第10回ACM推薦システム会議の議事録、アメリカ、ボストン、2016年9月15-19日。

ACM, 191–198.
ACM、191–198。

Craswell etal.(2008)↑
Craswell etal.(2008)↑

Nick Craswell, Onno Zoeter, Michael Taylor, and Bill Ramsey. 2008.
Nick Craswell、Onno Zoeter、Michael Taylor、および Bill Ramsey. 2008.

An Experimental Comparison of Click Position-Bias Models. 
クリック位置バイアスモデルの実験的比較。

InProceedings of the 2008 International Conference on Web Search and Data Mining(Palo Alto, California, USA)(WSDM ’08). 
2008年国際ウェブ検索およびデータマイニング会議の議事録（アメリカ、パロアルト）（WSDM ’08）。

Association for Computing Machinery, New York, NY, USA, 87–94.
コンピュータ機械学会、ニューヨーク、NY、USA、87–94。

https://doi.org/10.1145/1341531.1341545
https://doi.org/10.1145/1341531.1341545

Davidson etal.(2010)↑
Davidson etal.(2010)↑

James Davidson, Benjamin Liebald, Junning Liu, Palash Nandy, Taylor VanVleet, Ullas Gargi, Sujoy Gupta, Yu He, Mike Lambert, Blake Livingston, and Dasarathi Sampath. 2010.
James Davidson、Benjamin Liebald、Junning Liu、Palash Nandy、Taylor VanVleet、Ullas Gargi、Sujoy Gupta、Yu He、Mike Lambert、Blake Livingston、および Dasarathi Sampath. 2010.

The YouTube Video Recommendation System. 
YouTube動画推薦システム。

InProceedings of the Fourth ACM Conference on Recommender Systems(Barcelona, Spain)(RecSys ’10). 
第4回ACM推薦システム会議の議事録（スペイン、バルセロナ）（RecSys ’10）。

Association for Computing Machinery, New York, NY, USA, 293–296.
コンピュータ機械学会、ニューヨーク、NY、USA、293–296。

https://doi.org/10.1145/1864708.1864770
https://doi.org/10.1145/1864708.1864770

Dupret and Piwowarski (2008)↑
Dupret and Piwowarski (2008)↑

GeorgesE. Dupret and Benjamin Piwowarski. 2008.
GeorgesE. Dupret と Benjamin Piwowarski. 2008.

A User Browsing Model to Predict Search Engine Click Data from Past Observations.. 
過去の観察から検索エンジンのクリックデータを予測するユーザーブラウジングモデル。

InProceedings of the 31st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval(Singapore, Singapore)(SIGIR ’08). 
第31回国際ACM SIGIR情報検索研究開発会議の議事録（シンガポール、シンガポール）（SIGIR ’08）。

Association for Computing Machinery, New York, NY, USA, 331–338.
コンピュータ機械学会、ニューヨーク、NY、USA、331–338。

https://doi.org/10.1145/1390334.1390392
https://doi.org/10.1145/1390334.1390392

Fu etal.(2023)↑
Fu etal.(2023)↑

Lingyue Fu, Jianghao Lin, Weiwen Liu, Ruiming Tang, Weinan Zhang, Rui Zhang, and Yong Yu. 2023.
Lingyue Fu、Jianghao Lin、Weiwen Liu、Ruiming Tang、Weinan Zhang、Rui Zhang、および Yong Yu. 2023.

An F-Shape Click Model for Information Retrieval on Multi-Block Mobile Pages. 
マルチブロックモバイルページにおける情報検索のためのF字型クリックモデル。

InProceedings of the Sixteenth ACM International Conference on Web Search and Data Mining(Singapore, Singapore)(WSDM ’23). 
第16回ACM国際ウェブ検索およびデータマイニング会議の議事録（シンガポール、シンガポール）（WSDM ’23）。

Association for Computing Machinery, New York, NY, USA, 1057–1065.
コンピュータ機械学会、ニューヨーク、NY、USA、1057–1065。

https://doi.org/10.1145/3539597.3570365
https://doi.org/10.1145/3539597.3570365

Gao etal.(2022b)↑
Gao etal.(2022b)↑

Chongming Gao, Shijun Li, Yuan Zhang, Jiawei Chen, Biao Li, Wenqiang Lei, Peng Jiang, and Xiangnan He. 2022b.
Chongming Gao、Shijun Li、Yuan Zhang、Jiawei Chen、Biao Li、Wenqiang Lei、Peng Jiang、および Xiangnan He. 2022b.

KuaiRand: An Unbiased Sequential Recommendation Dataset with Randomly Exposed Videos. 
KuaiRand: ランダムに露出された動画を持つバイアスのない逐次推薦データセット。

InProceedings of the 31st ACM International Conference on Information and Knowledge Management(Atlanta, GA, USA)(CIKM ’22). 
第31回ACM国際情報および知識管理会議の議事録（アメリカ、アトランタ）（CIKM ’22）。

5pages.
5ページ。

https://doi.org/10.1145/3511808.3557624
https://doi.org/10.1145/3511808.3557624

Gao etal.(2022a)↑
Gao etal.(2022a)↑

Yunjun Gao, Yuntao Du, Yujia Hu, Lu Chen, Xinjun Zhu, Ziquan Fang, and Baihua Zheng. 2022a.
Yunjun Gao、Yuntao Du、Yujia Hu、Lu Chen、Xinjun Zhu、Ziquan Fang、および Baihua Zheng. 2022a.

Self-Guided Learning to Denoise for Robust Recommendation. 
堅牢な推薦のための自己指導型学習によるノイズ除去。

InProceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval(Madrid, Spain)(SIGIR ’22). 
第45回国際ACM SIGIR情報検索研究開発会議の議事録（スペイン、マドリード）（SIGIR ’22）。

Association for Computing Machinery, New York, NY, USA, 1412–1422.
コンピュータ機械学会、ニューヨーク、NY、USA、1412–1422。

https://doi.org/10.1145/3477495.3532059
https://doi.org/10.1145/3477495.3532059

He etal.(2023)↑
He etal.(2023)↑

Xiangnan He, Yang Zhang, Fuli Feng, Chonggang Song, Lingling Yi, Guohui Ling, and Yongdong Zhang. 2023.
Xiangnan He、Yang Zhang、Fuli Feng、Chonggang Song、Lingling Yi、Guohui Ling、および Yongdong Zhang. 2023.

Addressing Confounding Feature Issue for Causal Recommendation.
因果推薦のための混乱特徴問題への対処。

ACM Trans. Inf. Syst.41, 3, Article 53 (feb 2023), 23pages.
ACM Trans. Inf. Syst.41, 3, Article 53 (2023年2月)、23ページ。

https://doi.org/10.1145/3559757
https://doi.org/10.1145/3559757

Jacobs etal.(1991)↑
Jacobs etal.(1991)↑

RobertA. Jacobs, MichaelI. Jordan, StevenJ. Nowlan, and GeoffreyE. Hinton. 1991.
RobertA. Jacobs、MichaelI. Jordan、StevenJ. Nowlan、および GeoffreyE. Hinton. 1991.

Adaptive Mixtures of Local Experts.
ローカルエキスパートの適応的混合。

Neural Comput.3, 1 (1991), 79–87.
Neural Comput.3, 1 (1991)、79–87。

Joachims etal.(2017)↑
Joachims etal.(2017)↑

Thorsten Joachims, Adith Swaminathan, and Tobias Schnabel. 2017.
Thorsten Joachims、Adith Swaminathan、および Tobias Schnabel. 2017.

Unbiased Learning-to-Rank with Biased Feedback. 
バイアスのあるフィードバックによるバイアスのないランキング学習。

InProceedings of the Tenth ACM International Conference on Web Search and Data Mining(Cambridge, United Kingdom)(WSDM ’17). 
第10回ACM国際ウェブ検索およびデータマイニング会議の議事録（イギリス、ケンブリッジ）（WSDM ’17）。

ACM, New York, NY, USA, 781–789.
ACM、ニューヨーク、NY、USA、781–789。

https://doi.org/10.1145/3018661.3018699
https://doi.org/10.1145/3018661.3018699

Li etal.(2016)↑
Li etal.(2016)↑

Yan Li, KevinS. Xu, and ChandanK. Reddy. 2016.
Yan Li、KevinS. Xu、および ChandanK. Reddy. 2016.

Regularized Parametric Regression for High-dimensional Survival Analysis. 
高次元生存分析のための正則化されたパラメトリック回帰。

InProceedings of the 2016 SIAM International Conference on Data Mining, Miami, Florida, USA, May 5-7, 2016, SanjayChawla Venkatasubramanian and WagnerMeira Jr. (Eds.). 
2016年SIAM国際データマイニング会議の議事録、アメリカ、マイアミ、2016年5月5-7日、SanjayChawla Venkatasubramanian および WagnerMeira Jr.（編）。

SIAM, 765–773.
SIAM、765–773。

https://doi.org/10.1137/1.9781611974348.86
https://doi.org/10.1137/1.9781611974348.86

Liu etal.(2019)↑
Liu etal.(2019)↑

Shang Liu, Zhenzhong Chen, Hongyi Liu, and Xinghai Hu. 2019.
Shang Liu、Zhenzhong Chen、Hongyi Liu、および Xinghai Hu. 2019.

User-Video Co-Attention Network for Personalized Micro-Video Recommendation. 
個人化されたマイクロビデオ推薦のためのユーザー-ビデオ共同注意ネットワーク。

InThe World Wide Web Conference(San Francisco, CA, USA)(WWW ’19). 
ワールドワイドウェブ会議（アメリカ、サンフランシスコ）（WWW ’19）。

Association for Computing Machinery, New York, NY, USA, 3020–3026.
コンピュータ機械学会、ニューヨーク、NY、USA、3020–3026。

https://doi.org/10.1145/3308558.3313513
https://doi.org/10.1145/3308558.3313513

Liu etal.(2021)↑
Liu etal.(2021)↑

Yiyu Liu, Qian Liu, Yu Tian, Changping Wang, Yanan Niu, Yang Song, and Chenliang Li. 2021.
Yiyu Liu、Qian Liu、Yu Tian、Changping Wang、Yanan Niu、Yang Song、および Chenliang Li. 2021.

Concept-Aware Denoising Graph Neural Network for Micro-Video Recommendation. 
マイクロビデオ推薦のための概念認識型ノイズ除去グラフニューラルネットワーク。

InProceedings of the 30th ACM International Conference on Information Knowledge Management(Virtual Event, Queensland, Australia)(CIKM ’21). 
第30回ACM国際情報知識管理会議の議事録（バーチャルイベント、オーストラリア、クイーンズランド）（CIKM ’21）。

Association for Computing Machinery, New York, NY, USA, 1099–1108.
コンピュータ機械学会、ニューヨーク、NY、USA、1099–1108。

https://doi.org/10.1145/3459637.3482417
https://doi.org/10.1145/3459637.3482417

Ma etal.(2018)↑
Ma etal.(2018)↑

Jiaqi Ma, Zhe Zhao, Xinyang Yi, Jilin Chen, Lichan Hong, and EdH. Chi. 2018.
Jiaqi Ma、Zhe Zhao、Xinyang Yi、Jilin Chen、Lichan Hong、および EdH. Chi. 2018.

Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts. 
マルチゲートエキスパートの混合を用いたマルチタスク学習におけるタスク関係のモデリング。

InProceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, KDD 2018, London, UK, August 19-23, 2018. 
第24回ACM SIGKDD国際知識発見およびデータマイニング会議の議事録、KDD 2018、イギリス、ロンドン、2018年8月19-23日。

ACM, 1930–1939.
ACM、1930–1939。

Mao etal.(2018)↑
Mao etal.(2018)↑

Jiaxin Mao, Cheng Luo, Min Zhang, and Shaoping Ma. 2018.
Jiaxin Mao、Cheng Luo、Min Zhang、および Shaoping Ma. 2018.

Constructing Click Models for Mobile Search. 
モバイル検索のためのクリックモデルの構築。

InThe 41st International ACM SIGIR Conference on Research & Development in Information Retrieval(Ann Arbor, MI, USA)(SIGIR ’18). 
第41回国際ACM SIGIR情報検索研究開発会議の議事録（アメリカ、アンアーバー）（SIGIR ’18）。

Association for Computing Machinery, New York, NY, USA, 775–784.
コンピュータ機械学会、ニューヨーク、NY、USA、775–784。

https://doi.org/10.1145/3209978.3210060
https://doi.org/10.1145/3209978.3210060

Park etal.(2017)↑
Park etal.(2017)↑

Yoojin Park, Jinoh Oh, and Hwanjo Yu. 2017.
Yoojin Park、Jinoh Oh、および Hwanjo Yu. 2017.

RecTime: Real-time recommender system for online broadcasting.
RecTime: オンライン放送のためのリアルタイム推薦システム。

Information Sciences409 (2017), 1–16.
Information Sciences409 (2017)、1–16。

Qin etal.(2023)↑
Qin etal.(2023)↑

Jiarui Qin, Jiachen Zhu, Yankai Liu, Junchao Gao, Jianjie Ying, Chaoxiong Liu, Ding Wang, Junlan Feng, Chao Deng, Xiaozheng Wang, etal.2023.
Jiarui Qin、Jiachen Zhu、Yankai Liu、Junchao Gao、Jianjie Ying、Chaoxiong Liu、Ding Wang、Junlan Feng、Chao Deng、Xiaozheng Wang、他。2023。

Learning to distinguish multi-user coupling behaviors for tv recommendation. 
テレビ推薦のためのマルチユーザー結合行動を区別する学習。

InProceedings of the Sixteenth ACM International Conference on Web Search and Data Mining. 
第16回ACM国際ウェブ検索およびデータマイニング会議の議事録。

204–212.
204–212。

Quan etal.(2023)↑
Quan etal.(2023)↑

Yuhan Quan, Jingtao Ding, Chen Gao, Nian Li, Lingling Yi, Depeng Jin, and Yong Li. 2023.
Yuhan Quan、Jingtao Ding、Chen Gao、Nian Li、Lingling Yi、Depeng Jin、および Yong Li. 2023.

Alleviating Video-length Effect for Micro-video Recommendation.
マイクロビデオ推薦のための動画長さ効果の緩和。

ACM Trans. Inf. Syst.42, 2, Article 44 (nov 2023), 24pages.
ACM Trans. Inf. Syst.42, 2, Article 44 (2023年11月)、24ページ。

https://doi.org/10.1145/3617826
https://doi.org/10.1145/3617826

Rendle (2012)↑
Rendle (2012)↑

Steffen Rendle. 2012.
Steffen Rendle. 2012.

Factorization Machines with LibFM.
LibFMによる因子分解マシン。

ACM Trans. Intell. Syst. Technol.3, 3, Article 57 (may 2012), 22pages.
ACM Trans. Intell. Syst. Technol.3, 3, Article 57 (2012年5月)、22ページ。

https://doi.org/10.1145/2168752.2168771
https://doi.org/10.1145/2168752.2168771

Saito etal.(2020)↑
Saito etal.(2020)↑

Yuta Saito, Suguru Yaginuma, Yuta Nishino, Hayato Sakata, and Kazuhide Nakata. 2020.
Yuta Saito、Suguru Yaginuma、Yuta Nishino、Hayato Sakata、および Kazuhide Nakata. 2020.

Unbiased Recommender Learning from Missing-Not-At-Random Implicit Feedback. 
ランダムでない欠落した暗黙のフィードバックからのバイアスのない推薦学習。

InProceedings of the 13th International Conference on Web Search and Data Mining(Houston, TX, USA)(WSDM ’20). 
第13回国際ウェブ検索およびデータマイニング会議の議事録（アメリカ、ヒューストン）（WSDM ’20）。

Association for Computing Machinery, New York, NY, USA, 501–509.
コンピュータ機械学会、ニューヨーク、NY、USA、501–509。

https://doi.org/10.1145/3336191.3371783
https://doi.org/10.1145/3336191.3371783

Schnabel etal.(2016)↑
Schnabel etal.(2016)↑

Tobias Schnabel, Adith Swaminathan, Ashudeep Singh, Navin Chandak, and Thorsten Joachims. 2016.
Tobias Schnabel、Adith Swaminathan、Ashudeep Singh、Navin Chandak、および Thorsten Joachims. 2016.

Recommendations as treatments: Debiasing learning and evaluation. 
推薦を治療として：学習と評価のバイアス除去。

Ininternational conference on machine learning. 
機械学習に関する国際会議において。

PMLR, 1670–1679.
PMLR、1670–1679。

Song etal.(2019)↑
Song etal.(2019)↑

Weiping Song, Chence Shi, Zhiping Xiao, Zhijian Duan, Yewen Xu, Ming Zhang, and Jian Tang. 2019.
Weiping Song、Chence Shi、Zhiping Xiao、Zhijian Duan、Yewen Xu、Ming Zhang、および Jian Tang. 2019.

AutoInt: Automatic Feature Interaction Learning via Self-Attentive Neural Networks. 
AutoInt: 自己注意型ニューラルネットワークによる自動特徴相互作用学習。

InProceedings of the 28th ACM International Conference on Information and Knowledge Management(Beijing, China)(CIKM ’19). 
第28回ACM国際情報および知識管理会議の議事録（中国、北京）（CIKM ’19）。

Association for Computing Machinery, New York, NY, USA, 1161–1170.
コンピュータ機械学会、ニューヨーク、NY、USA、1161–1170。

https://doi.org/10.1145/3357384.3357925
https://doi.org/10.1145/3357384.3357925

Tang etal.(2020)↑
Tang etal.(2020)↑

Hongyan Tang, Junning Liu, Ming Zhao, and Xudong Gong. 2020.
Hongyan Tang、Junning Liu、Ming Zhao、および Xudong Gong. 2020.

Progressive Layered Extraction (PLE): A Novel Multi-Task Learning (MTL) Model for Personalized Recommendations. 
プログレッシブラーヤード抽出（PLE）：個人化された推薦のための新しいマルチタスク学習（MTL）モデル。

InRecSys 2020: Fourteenth ACM Conference on Recommender Systems, Virtual Event, Brazil, September 22-26, 2020
RecSys 2020：第14回ACM推薦システム会議、バーチャルイベント、ブラジル、2020年9月22-26日。



. InRecSys 2020: Fourteenth ACM Conference on Recommender Systems, Virtual Event, Brazil, September 22-26, 2020. ACM, 269–278.
. InRecSys 2020: 第14回ACM推薦システム会議、バーチャルイベント、ブラジル、2020年9月22-26日。ACM、269–278。

Tang etal.(2023a)↑
Tang etal.(2023a)↑

. Shisong Tang, Qing Li, Dingmin Wang, Ci Gao, Wentao Xiao, Dan Zhao, Yong Jiang, Qian Ma, and Aoyang Zhang. 2023a.
Shisong Tang, Qing Li, Dingmin Wang, Ci Gao, Wentao Xiao, Dan Zhao, Yong Jiang, Qian Ma, および Aoyang Zhang. 2023a。

Counterfactual Video Recommendation for Duration Debiasing. 
「期間のバイアス除去のための反事実的ビデオ推薦」。

InProceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining(¡conf-loc¿, ¡city¿Long Beach¡/city¿, ¡state¿CA¡/state¿, ¡country¿USA¡/country¿, ¡/conf-loc¿)(KDD ’23). 
第29回ACM SIGKDD知識発見とデータマイニング会議の議事録（ロングビーチ、CA、USA）（KDD ’23）。

Association for Computing Machinery, New York, NY, USA, 4894–4903.
計算機科学協会、ニューヨーク、NY、USA、4894–4903。

https://doi.org/10.1145/3580305.3599797
https://doi.org/10.1145/3580305.3599797

Tang etal.(2023b)↑
Tang etal.(2023b)↑

. Shisong Tang, Qing Li, Dingmin Wang, Ci Gao, Wentao Xiao, Dan Zhao, Yong Jiang, Qian Ma, and Aoyang Zhang. 2023b.
Shisong Tang, Qing Li, Dingmin Wang, Ci Gao, Wentao Xiao, Dan Zhao, Yong Jiang, Qian Ma, および Aoyang Zhang. 2023b。

Counterfactual Video Recommendation for Duration Debiasing. 
「期間のバイアス除去のための反事実的ビデオ推薦」。

InProceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining(Long Beach, CA, USA)(KDD ’23). 
第29回ACM SIGKDD知識発見とデータマイニング会議の議事録（ロングビーチ、CA、USA）（KDD ’23）。

Association for Computing Machinery, New York, NY, USA, 4894–4903.
計算機科学協会、ニューヨーク、NY、USA、4894–4903。

https://doi.org/10.1145/3580305.3599797
https://doi.org/10.1145/3580305.3599797

Thompson and Spencer (1966)↑
Thompson and Spencer (1966)↑

RichardF Thompson and WilliamA Spencer. 1966.
Richard F. Thompson と William A. Spencer. 1966。

Habituation: a model phenomenon for the study of neuronal substrates of behavior.
「習慣化：行動の神経基盤の研究のためのモデル現象」。

Psychological review73, 1 (1966), 16.
心理学レビュー 73, 1 (1966), 16。

Vriend (1996)↑
Vriend (1996)↑

NicolaasJ Vriend. 1996.
Nicolaas J. Vriend. 1996。

Rational behavior and economic theory.
「合理的行動と経済理論」。

Journal of Economic Behavior & Organization29, 2 (1996), 263–285.
経済行動と組織のジャーナル 29, 2 (1996), 263–285。

Wang etal.(2019)↑
Wang etal.(2019)↑

. Ping Wang, Yan Li, and ChandanK Reddy. 2019.
Ping Wang, Yan Li, および Chandan K. Reddy. 2019。

Machine learning for survival analysis: A survey.
「生存分析のための機械学習：調査」。

ACM Computing Surveys (CSUR)51, 6 (2019), 1–36.
ACMコンピューティングサーベイ（CSUR）51, 6 (2019), 1–36。

Wang etal.(2017)↑
Wang etal.(2017)↑

. Ruoxi Wang, Bin Fu, Gang Fu, and Mingliang Wang. 2017.
Ruoxi Wang, Bin Fu, Gang Fu, および Mingliang Wang. 2017。

Deep & Cross Network for Ad Click Predictions. 
「広告クリック予測のためのDeep & Cross Network」。

InProceedings of the ADKDD’17(Halifax, NS, Canada)(ADKDD’17). 
ADKDD’17の議事録（ハリファックス、NS、カナダ）（ADKDD’17）。

Association for Computing Machinery, New York, NY, USA, Article 12, 7pages.
計算機科学協会、ニューヨーク、NY、USA、記事12、7ページ。

https://doi.org/10.1145/3124749.3124754
https://doi.org/10.1145/3124749.3124754

Wang etal.(2021)↑
Wang etal.(2021)↑

. Wenjie Wang, Fuli Feng, Xiangnan He, Liqiang Nie, and Tat-Seng Chua. 2021.
Wenjie Wang, Fuli Feng, Xiangnan He, Liqiang Nie, および Tat-Seng Chua. 2021。

Denoising Implicit Feedback for Recommendation. 
「推薦のための暗黙的フィードバックのノイズ除去」。

InProceedings of the 14th ACM International Conference on Web Search and Data Mining(Virtual Event, Israel)(WSDM ’21). 
第14回ACM国際ウェブ検索とデータマイニング会議の議事録（バーチャルイベント、イスラエル）（WSDM ’21）。

Association for Computing Machinery, New York, NY, USA, 373–381.
計算機科学協会、ニューヨーク、NY、USA、373–381。

https://doi.org/10.1145/3437963.3441800
https://doi.org/10.1145/3437963.3441800

Wang etal.(2016)↑
Wang etal.(2016)↑

. Xuanhui Wang, Michael Bendersky, Donald Metzler, and Marc Najork. 2016.
Xuanhui Wang, Michael Bendersky, Donald Metzler, および Marc Najork. 2016。

Learning to Rank with Selection Bias in Personal Search. 
「個人検索における選択バイアスを伴うランキング学習」。

InProceedings of the 39th International ACM SIGIR Conference on Research and Development in Information Retrieval(Pisa, Italy)(SIGIR ’16). 
第39回国際ACM SIGIR情報検索に関する研究開発会議の議事録（ピサ、イタリア）（SIGIR ’16）。

ACM, New York, NY, USA, 115–124.
ACM、ニューヨーク、NY、USA、115–124。

Wang etal.(2022)↑
Wang etal.(2022)↑

. Yu Wang, Xin Xin, Zaiqiao Meng, JoemonM Jose, Fuli Feng, and Xiangnan He. 2022.
Yu Wang, Xin Xin, Zaiqiao Meng, Joemon M. Jose, Fuli Feng, および Xiangnan He. 2022。

Learning Robust Recommenders through Cross-Model Agreement. 
「クロスモデル合意を通じた堅牢な推薦システムの学習」。

InProceedings of the ACM Web Conference 2022(Virtual Event, Lyon, France)(WWW ’22). 
ACMウェブ会議2022の議事録（バーチャルイベント、リヨン、フランス）（WWW ’22）。

Association for Computing Machinery, New York, NY, USA, 2015–2025.
計算機科学協会、ニューヨーク、NY、USA、2015–2025。

https://doi.org/10.1145/3485447.3512202
https://doi.org/10.1145/3485447.3512202

Wei etal.(2021)↑
Wei etal.(2021)↑

. Tianxin Wei, Fuli Feng, Jiawei Chen, Ziwei Wu, Jinfeng Yi, and Xiangnan He. 2021.
Tianxin Wei, Fuli Feng, Jiawei Chen, Ziwei Wu, Jinfeng Yi, および Xiangnan He. 2021。

Model-Agnostic Counterfactual Reasoning for Eliminating Popularity Bias in Recommender System. 
「推薦システムにおける人気バイアスを排除するためのモデル非依存の反事実的推論」。

InProceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery Data Mining(Virtual Event, Singapore)(KDD ’21). 
第27回ACM SIGKDD知識発見データマイニング会議の議事録（バーチャルイベント、シンガポール）（KDD ’21）。

Association for Computing Machinery, New York, NY, USA, 1791–1800.
計算機科学協会、ニューヨーク、NY、USA、1791–1800。

https://doi.org/10.1145/3447548.3467289
https://doi.org/10.1145/3447548.3467289

Wu etal.(2022)↑
Wu etal.(2022)↑

. Peng Wu, Haoxuan Li, Yuhao Deng, Wenjie Hu, Quanyu Dai, Zhenhua Dong, Jie Sun, Rui Zhang, and Xiao-Hua Zhou. 2022.
Peng Wu, Haoxuan Li, Yuhao Deng, Wenjie Hu, Quanyu Dai, Zhenhua Dong, Jie Sun, Rui Zhang, および Xiao-Hua Zhou. 2022。

On the Opportunity of Causal Learning in Recommendation Systems: Foundation, Estimation, Prediction and Challenges. 
「推薦システムにおける因果学習の機会：基礎、推定、予測と課題」。

InProceedings of the Thirty-First International Joint Conference on Artificial Intelligence, IJCAI-22. 
第31回国際共同人工知能会議の議事録、IJCAI-22。

5646–5653.
5646–5653。

Survey Track.
調査トラック。

Xie etal.(2023)↑
Xie etal.(2023)↑

. Ruobing Xie, Lin Ma, Shaoliang Zhang, Feng Xia, and Leyu Lin. 2023.
Ruobing Xie, Lin Ma, Shaoliang Zhang, Feng Xia, および Leyu Lin. 2023。

Reweighting Clicks with Dwell Time in Recommendation. 
「推薦における滞在時間を用いたクリックの再重み付け」。

InCompanion Proceedings of the ACM Web Conference 2023(Austin, TX, USA)(WWW ’23 Companion). 
ACMウェブ会議2023の補足議事録（オースティン、TX、USA）（WWW ’23 Companion）。

Association for Computing Machinery, New York, NY, USA, 341–345.
計算機科学協会、ニューヨーク、NY、USA、341–345。

https://doi.org/10.1145/3543873.3584624
https://doi.org/10.1145/3543873.3584624

Yuan etal.(2020)↑
Yuan etal.(2020)↑

. Bowen Yuan, Yaxu Liu, Jui-Yang Hsia, Zhenhua Dong, and Chih-Jen Lin. 2020.
Bowen Yuan, Yaxu Liu, Jui-Yang Hsia, Zhenhua Dong, および Chih-Jen Lin. 2020。

Unbiased Ad Click Prediction for Position-Aware Advertising Systems. 
「位置認識広告システムのためのバイアスのない広告クリック予測」。

InFourteenth ACM Conference on Recommender Systems(Virtual Event, Brazil)(RecSys ’20). 
第14回ACM推薦システム会議（バーチャルイベント、ブラジル）（RecSys ’20）。

ACM, New York, NY, USA, 368–377.
ACM、ニューヨーク、NY、USA、368–377。

https://doi.org/10.1145/3383313.3412241
https://doi.org/10.1145/3383313.3412241

Zhan etal.(2022)↑
Zhan etal.(2022)↑

. Ruohan Zhan, Changhua Pei, Qiang Su, Jianfeng Wen, Xueliang Wang, Guanyu Mu, Dong Zheng, Peng Jiang, and Kun Gai. 2022.
Ruohan Zhan, Changhua Pei, Qiang Su, Jianfeng Wen, Xueliang Wang, Guanyu Mu, Dong Zheng, Peng Jiang, および Kun Gai. 2022。

Deconfounding Duration Bias in Watch-Time Prediction for Video Recommendation. 
「ビデオ推薦のための視聴時間予測における期間バイアスの除去」。

InProceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining(Washington DC, USA)(KDD ’22). 
第28回ACM SIGKDD知識発見とデータマイニング会議の議事録（ワシントンDC、USA）（KDD ’22）。

Association for Computing Machinery, New York, NY, USA, 4472–4481.
計算機科学協会、ニューヨーク、NY、USA、4472–4481。

https://doi.org/10.1145/3534678.3539092
https://doi.org/10.1145/3534678.3539092

Zhang etal.(2021)↑
Zhang etal.(2021)↑

. Yang Zhang, Fuli Feng, Xiangnan He, Tianxin Wei, Chonggang Song, Guohui Ling, and Yongdong Zhang. 2021.
Yang Zhang, Fuli Feng, Xiangnan He, Tianxin Wei, Chonggang Song, Guohui Ling, および Yongdong Zhang. 2021。

Causal Intervention for Leveraging Popularity Bias in Recommendation. 
「推薦における人気バイアスを活用するための因果介入」。

InProceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval(Virtual Event, Canada)(SIGIR ’21). 
第44回国際ACM SIGIR情報検索に関する研究開発会議の議事録（バーチャルイベント、カナダ）（SIGIR ’21）。

ACM, New York, NY, USA, 11–20.
ACM、ニューヨーク、NY、USA、11–20。

https://doi.org/10.1145/3404835.3462875
https://doi.org/10.1145/3404835.3462875

Zhao etal.(2023)↑
Zhao etal.(2023)↑

. Haiyuan Zhao, Lei Zhang, Jun Xu, Guohao Cai, Zhenhua Dong, and Ji-Rong Wen. 2023.
Haiyuan Zhao, Lei Zhang, Jun Xu, Guohao Cai, Zhenhua Dong, および Ji-Rong Wen. 2023。

Uncovering User Interest from Biased and Noised Watch Time in Video Recommendation. 
「ビデオ推薦におけるバイアスとノイズのある視聴時間からのユーザー興味の発見」。

InProceedings of the 17th ACM Conference on Recommender Systems(Singapore, Singapore)(RecSys ’23). 
第17回ACM推薦システム会議の議事録（シンガポール、シンガポール）（RecSys ’23）。

Association for Computing Machinery, New York, NY, USA, 528–539.
計算機科学協会、ニューヨーク、NY、USA、528–539。

https://doi.org/10.1145/3604915.3608797
https://doi.org/10.1145/3604915.3608797

Zhao etal.(2019)↑
Zhao etal.(2019)↑

. Zhe Zhao, Lichan Hong, Li Wei, Jilin Chen, Aniruddh Nath, Shawn Andrews, Aditee Kumthekar, Maheswaran Sathiamoorthy, Xinyang Yi, and EdH. Chi. 2019.
Zhe Zhao, Lichan Hong, Li Wei, Jilin Chen, Aniruddh Nath, Shawn Andrews, Aditee Kumthekar, Maheswaran Sathiamoorthy, Xinyang Yi, および Ed H. Chi. 2019。

Recommending what video to watch next: a multitask ranking system. 
「次に見るべきビデオの推薦：マルチタスクランキングシステム」。

InProceedings of the 13th ACM Conference on Recommender Systems, RecSys 2019, Copenhagen, Denmark, September 16-20, 2019. 
第13回ACM推薦システム会議、RecSys 2019、デンマーク、コペンハーゲン、2019年9月16-20日。

ACM, 43–51.
ACM、43–51。

Zheng etal.(2022)↑
Zheng etal.(2022)↑

. Yu Zheng, Chen Gao, Jingtao Ding, Lingling Yi, Depeng Jin, Yong Li, and Meng Wang. 2022.
Yu Zheng, Chen Gao, Jingtao Ding, Lingling Yi, Depeng Jin, Yong Li, および Meng Wang. 2022。

DVR: Micro-Video Recommendation Optimizing Watch-Time-Gain under Duration Bias. 
「DVR：期間バイアス下での視聴時間利益を最適化するマイクロビデオ推薦」。

InProceedings of the 30th ACM International Conference on Multimedia(Lisboa, Portugal)(MM ’22). 
第30回ACM国際マルチメディア会議の議事録（リスボン、ポルトガル）（MM ’22）。

Association for Computing Machinery, New York, NY, USA, 334–345.
計算機科学協会、ニューヨーク、NY、USA、334–345。

https://doi.org/10.1145/3503161.3548428
https://doi.org/10.1145/3503161.3548428

Zheng etal.(2021)↑
Zheng etal.(2021)↑

. Yu Zheng, Chen Gao, Xiang Li, Xiangnan He, Yong Li, and Depeng Jin. 2021.
Yu Zheng, Chen Gao, Xiang Li, Xiangnan He, Yong Li, および Depeng Jin. 2021。

Disentangling User Interest and Conformity for Recommendation with Causal Embedding. 
「因果埋め込みを用いた推薦におけるユーザー興味と同調の分離」。

InProceedings of the Web Conference 2021(Ljubljana, Slovenia)(WWW ’21). 
ウェブ会議2021の議事録（リュブリャナ、スロベニア）（WWW ’21）。

ACM, New York, NY, USA, 2980–2991.
ACM、ニューヨーク、NY、USA、2980–2991。

https://doi.org/10.1145/3442381.3449788
https://doi.org/10.1145/3442381.3449788

Zhou etal.(2018)↑
Zhou etal.(2018)↑

. Tengfei Zhou, Hui Qian, Zebang Shen, Chao Zhang, Chengwei Wang, Shichen Liu, and Wenwu Ou. 2018.
Tengfei Zhou, Hui Qian, Zebang Shen, Chao Zhang, Chengwei Wang, Shichen Liu, および Wenwu Ou. 2018。

JUMP: a joint predictor for user click and dwell time. 
「JUMP：ユーザークリックと滞在時間のための共同予測器」。

InProceedings of the 27th International Joint Conference on Artificial Intelligence. AAAI Press. 3704–3710.
第27回国際共同人工知能会議の議事録。AAAIプレス。3704–3710。



## Appendix A Theorem 1の証明

Appendix A
As we have analyzed before, the CWTwu,vcsubscriptsuperscript𝑤𝑐𝑢𝑣w^{c}_{u,v}italic_w start_POSTSUPERSCRIPT italic_c end_POSTSUPERSCRIPT start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPTcorresponds to user interestsru,vsubscript𝑟𝑢𝑣r_{u,v}italic_r start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPT, i.e.,wu,vc=g(ru,v)subscriptsuperscript𝑤𝑐𝑢𝑣𝑔subscript𝑟𝑢𝑣w^{c}_{u,v}=g(r_{u,v})italic_w start_POSTSUPERSCRIPT italic_c end_POSTSUPERSCRIPT start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPT = italic_g ( italic_r start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPT ).
私たちが以前に分析したように、CWT $w^{c}_{u,v}$ はユーザの興味 $r_{u,v}$ に対応します。すなわち、$w^{c}_{u,v} = g(r_{u,v})$ です。

Based on Eq.(1), we can obtain the functions ofwu,vsubscript𝑤𝑢𝑣w_{u,v}italic_w start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPTonru,vsubscript𝑟𝑢𝑣r_{u,v}italic_r start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPT:
式(1)に基づいて、$w_{u,v}$ の関数を $r_{u,v}$ に関して得ることができます。

Next, we need to prove that the above function does not always have an inverse function, w.r.t anywu,vsubscript𝑤𝑢𝑣w_{u,v}italic_w start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPT.
次に、上記の関数が任意の $w_{u,v}$ に対して常に逆関数を持たないことを証明する必要があります。

Similar to Eq.(1), we rewrite the above function as a segmented function:
式(1)と同様に、上記の関数をセグメント化された関数として書き直します。

Note that whenwu,v=dvsubscript𝑤𝑢𝑣subscript𝑑𝑣w_{u,v}=d_{v}italic_w start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPT = italic_d start_POSTSUBSCRIPT italic_v end_POSTSUBSCRIPT(i.e., completely play a video), we can only obtain an inequality betweenwu,vsubscript𝑤𝑢𝑣w_{u,v}italic_w start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPTandru,vsubscript𝑟𝑢𝑣r_{u,v}italic_r start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPT, thus proving that there is no such an inverse functionru,v=g−1(wu,v)subscript𝑟𝑢𝑣superscript𝑔1subscript𝑤𝑢𝑣r_{u,v}=g^{-1}(w_{u,v})italic_r start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPT = italic_g start_POSTSUPERSCRIPT - 1 end_POSTSUPERSCRIPT ( italic_w start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPT )for allwu,v∈𝒲subscript𝑤𝑢𝑣𝒲w_{u,v}\in\mathcal{W}italic_w start_POSTSUBSCRIPT italic_u , italic_v end_POSTSUBSCRIPT ∈ caligraphic_W.
$w_{u,v} = d_{v}$（すなわち、ビデオを完全に再生する場合）であるとき、$w_{u,v}$ と $r_{u,v}$ の間に不等式しか得られないことに注意してください。これにより、すべての $w_{u,v} \in \mathcal{W}$ に対して逆関数 $r_{u,v} = g^{-1}(w_{u,v})$ が存在しないことが証明されます。
∎



## Appendix BDetailed Experimental Setting 付録B 詳細な実験設定

Appendix B  
付録B  

In our paper, we briefly described the dataset used in our papers and the baselines due to the limitation of pages.  
私たちの論文では、ページ数の制限のために、使用したデータセットとベースラインについて簡単に説明しました。  
Now, we put a more detailed experimental setting in this appendix.  
ここでは、この付録により詳細な実験設定を記載します。  

WeChat. This dataset is released by WeChat Big Data Challenge 2021, containing the WeChat Channels logs within two weeks.  
WeChat。このデータセットは、WeChat Big Data Challenge 2021によって公開され、2週間のWeChat Channelsのログを含んでいます。  
Following the practice in (Zheng et al., 2022), we split the data into the first 10 days, the middle 2 days, and the last 2 days as training, validation, and test set.  
(Zheng et al., 2022)の手法に従い、データを最初の10日間、中間の2日間、最後の2日間に分割し、トレーニング、バリデーション、テストセットとしました。  
We noticed that there is an unusually high proportion of 60s videos among the dataset (17.3%), so our experiments were conducted on a subset of 60s videos that were excluded (i.e., the duration range is [5s, 59s] in the subset).  
データセットの中に60秒の動画の割合が異常に高い（17.3%）ことに気づいたため、私たちの実験は除外された60秒の動画のサブセットで行われました（すなわち、サブセットの長さの範囲は[5s, 59s]です）。  
The adopted input features include user_id, feed_id, device, author_id, bgm_song_id, bgm_singer_id, user_type.  
採用された入力特徴には、user_id、feed_id、device、author_id、bgm_song_id、bgm_singer_id、user_typeが含まれます。  

KuaiRand (Gao et al., 2022b). KuaiRand is a newly released sequential recommendation dataset collected from KuaiShou.  
KuaiRand (Gao et al., 2022b)。KuaiRandは、KuaiShouから収集された新たに公開された逐次推薦データセットです。  
As suggested in (Gao et al., 2022b), we utilized one of the subsets KuaiRand-pure in this study.  
(Gao et al., 2022b)で提案されているように、私たちはこの研究でサブセットの一つであるKuaiRand-pureを利用しました。  
To mitigate the sparsity problem, we selected data from which the video duration is up to 400s.  
スパース性の問題を軽減するために、動画の長さが最大400秒のデータを選択しました。  
We split the data into the first 14 days, the middle 7 days, and the last 10 days as training, validation, and test set.  
データを最初の14日間、中間の7日間、最後の10日間に分割し、トレーニング、バリデーション、テストセットとしました。  
The adopted input features include user_id, video_id, author_id, music_id, follow_user_num_range, register_days_range, fans_user_num_range, friend_user_num_range, user_active_degree, most_popular_tag, video_type, upload_type, tab.  
採用された入力特徴には、user_id、video_id、author_id、music_id、follow_user_num_range、register_days_range、fans_user_num_range、friend_user_num_range、user_active_degree、most_popular_tag、video_type、upload_type、tabが含まれます。  

Product. We collect the product dataset from the server log of our video platform, which samples the log data from June 19, 2023 to June 25, 2023.  
Product。私たちは、2023年6月19日から2023年6月25日までのログデータをサンプリングした、私たちの動画プラットフォームのサーバーログから製品データセットを収集しました。  
Due to the data imbalance, we intercepted the records below 42 seconds as the final training set.  
データの不均衡のため、42秒未満のレコードを最終的なトレーニングセットとして切り取りました。  
We trained our model on this dataset and tested them in the last two hours of server log data.  
このデータセットでモデルをトレーニングし、サーバーログデータの最後の2時間でテストしました。  
The pretrained ID embedding and side information are used as feature inputs for all methods.  
すべての手法に対して、事前学習されたID埋め込みとサイド情報が特徴入力として使用されます。  

In this study, we implement WLR following the details in (Zhan et al., 2022).  
この研究では、(Zhan et al., 2022)の詳細に従ってWLRを実装します。  
For D2Q, the group number is set to 60 in KuaiRand, 30 in WeChat, and 10 in our Product dataset.  
D2Qについては、KuaiRandでグループ数を60、WeChatで30、私たちのProductデータセットで10に設定しました。  
For NDT, we set its hyper-parameters as the author suggested in their paper (Xie et al., 2023).  
NDTについては、著者が彼らの論文(Xie et al., 2023)で提案したようにハイパーパラメータを設定しました。  
For D2Co, the window size and sensitivity-controlled term are set as suggested in their paper (Zhao et al., 2023).  
D2Coについては、ウィンドウサイズと感度制御項を彼らの論文(Zhao et al., 2023)で提案されたように設定しました。  
We utilize Adam as the optimizer and set the initial learning rate as $5e^{-4}$ for all methods.  
すべての手法に対して、最適化手法としてAdamを使用し、初期学習率を$5e^{-4}$に設定しました。  
The batch size is set as 512.  
バッチサイズは512に設定されています。  
For all the backbone models, we set their latent embedding dimension to 10.  
すべてのバックボーンモデルについて、潜在埋め込み次元を10に設定しました。  
For all methods with neural networks, the hidden units are set to 64 while the dropout ratio is set to 0.2.  
すべてのニューラルネットワークを使用する手法について、隠れユニットを64に設定し、ドロップアウト比率を0.2に設定しました。  
The value of user cost $c$ and $\sigma$ in our CWM is set to $(1/40, 2)$ in the KuaiRand dataset, $(1/40, 20)$ in the WeChat dataset, and $(1/5, 5)$ in the Product dataset.  
私たちのCWMにおけるユーザーコスト$c$と$\sigma$の値は、KuaiRandデータセットで$(1/40, 2)$、WeChatデータセットで$(1/40, 20)$、Productデータセットで$(1/5, 5)$に設定されています。  
We tune our hyperparameters on the validation set while evaluating the performance on the test set.  
バリデーションセットでハイパーパラメータを調整し、テストセットでの性能を評価します。  

(a)  
(a)  

KuaiRand  
KuaiRand  

(b)  
(b)  

WeChat  
WeChat  

Figure 10.  
図10。  



## Appendix C The Unbiasedness of Interest Labels 付録C 興味ラベルの無偏性

To evaluate the performance of relevance ranking tasks in this study, we need an unbiased indicator of user interest first. 
この研究における関連性ランキングタスクのパフォーマンスを評価するためには、まずユーザの興味の無偏な指標が必要です。

However, the user interest labels are unobserved in real-world datasets. 
しかし、ユーザの興味ラベルは実世界のデータセットでは観測されません。

Although explicit feedback can reflect user interest and is not affected by duration bias, it suffers from severe selection bias and noise (Wang et al., 2022; Gao et al., 2022a; Wang et al., 2021): 
明示的なフィードバックはユーザの興味を反映でき、持続時間バイアスの影響を受けないものの、深刻な選択バイアスとノイズに悩まされます（Wang et al., 2022; Gao et al., 2022a; Wang et al., 2021）：

this indicates that users might not provide explicit feedback for videos they like and might mistakenly provide explicit feedback for videos they dislike. 
これは、ユーザが好きな動画に対して明示的なフィードバックを提供しない可能性があり、嫌いな動画に対して誤って明示的なフィードバックを提供する可能性があることを示しています。

Therefore, using explicit feedback as a label for evaluating relevance ranking tasks is inappropriate. 
したがって、関連性ランキングタスクを評価するためのラベルとして明示的なフィードバックを使用することは不適切です。

To this end, we defined user interests based on CWT in Eq. (8). 
この目的のために、私たちは式(8)に基づいてユーザの興味を定義しました。

However, the unbiasedness of this interest label still needs to be discussed. 
しかし、この興味ラベルの無偏性についてはまだ議論が必要です。

To achieve duration unbiased, the user interest indicator $r_{u,v}$ needs to fulfill two characteristics: 
持続時間の無偏性を達成するために、ユーザの興味指標 $r_{u,v}$ は2つの特性を満たす必要があります：

(1) it should be independent of video duration, and 
(1) それは動画の持続時間に依存しないべきです。

(2) when $r_{u,v} = 1$, user explicit feedback should be equivalent across all video duration (thus mitigating the issue described in Fig 1). 
(2) $r_{u,v} = 1$ のとき、ユーザの明示的なフィードバックはすべての動画の持続時間にわたって同等であるべきです（したがって、図1で説明されている問題を軽減します）。

To verify whether our interest indicator defined in Eq. (8) satisfies the above characteristics, we calculate the proportion of user interest labels $r_{u,v}$ and the proportion of explicit feedback when $r_{u,v} = 1$ grouped by video duration. 
式(8)で定義された私たちの興味指標が上記の特性を満たすかどうかを検証するために、ユーザの興味ラベル $r_{u,v}$ の割合と、動画の持続時間でグループ化したときの $r_{u,v} = 1$ の明示的フィードバックの割合を計算します。

Note that since videos shorter than $w_{0.7}$ cannot achieve a watch time of $w_{0.7}$, we exclude these videos from our analysis. 
$w_{0.7}$ より短い動画は $w_{0.7}$ の視聴時間を達成できないため、これらの動画は分析から除外します。

The results are presented in Fig 10. 
結果は図10に示されています。

It is evident that our defined $r_{u,v}$ roughly satisfies the above two characteristics on both the KuaiRand and WeChat datasets, thus indicating its unbiasedness. 
私たちが定義した $r_{u,v}$ は、KuaiRandデータセットとWeChatデータセットの両方で上記の2つの特性を大まかに満たしていることが明らかであり、したがってその無偏性を示しています。



## Appendix D 付録 D

### D.1. Parameter sensitivity パラメータ感度
There are two hyper-parameters in the proposed CWM: one is the user watch cost $c$ in the cost-based transform function (Eq.(3)). 
提案されたCWMには2つのハイパーパラメータがあります：1つはコストベースの変換関数（式(3)）におけるユーザの視聴コスト$c$です。

The larger the $c$, the more sensitive users are to watch time; 
$c$が大きいほど、ユーザは視聴時間に対してより敏感になります。

Another is the variance term $\sigma$ of user interest in counterfactual likelihood function (Eq(6)). 
もう1つは、反事実的尤度関数（式(6)）におけるユーザの興味の分散項$\sigma$です。

The larger the value of $\sigma$, the more dispersed the user’s interest distribution is. 
$\sigma$の値が大きいほど、ユーザの興味の分布はより分散します。

Fig.11 illustrates the performance changes of recommendation with different values of $c$ and $\sigma$. 
図11は、異なる$c$と$\sigma$の値に対する推薦のパフォーマンスの変化を示しています。

For watch time prediction (Fig.11(a)), the best hyper-parameter is $\sigma \in (1.0,2.0) \land c \in (1/40,1/20)$. 
視聴時間予測（図11(a)）の場合、最適なハイパーパラメータは$\sigma \in (1.0,2.0) \land c \in (1/40,1/20)$です。

For relevance ranking (Fig.11(b)), the best hyper-parameters is $\sigma \in (2.0,5.0) \land c \in (1/80,1/60)$. 
関連性ランキング（図11(b)）の場合、最適なハイパーパラメータは$\sigma \in (2.0,5.0) \land c \in (1/80,1/60)$です。

Note that the best hyper-parameters of two tasks may not be the same. 
2つのタスクの最適なハイパーパラメータは同じでない場合があることに注意してください。

In practice, it is necessary to adjust the hyper-parameters to make CWM perform best. 
実際には、CWMが最も良いパフォーマンスを発揮するようにハイパーパラメータを調整する必要があります。

### D.2. Better fit to the true watch time distribution 真の視聴時間分布へのより良い適合
We examine whether CWM can fit the true watch time distribution. 
CWMが真の視聴時間分布に適合できるかどうかを検討します。

As a comparison, we also present the estimated watch time distribution by PCR, which is representative of existing debiasing methods. 
比較のために、既存のデバイアス手法を代表するPCRによる推定視聴時間分布も示します。

Fig12(a) shows the true and estimated watch time distribution on videos with less than 100s duration on KuaiRand. 
図12(a)は、KuaiRandの100秒未満の動画における真の視聴時間分布と推定視聴時間分布を示しています。

We can find that the estimated watch time distribution by PCR is more flattening than the true distribution. 
PCRによる推定視聴時間分布は、真の分布よりも平坦化されていることがわかります。

It overestimates higher watch time (i.e., >10s). 
それは高い視聴時間（すなわち、>10秒）を過大評価します。

In contrast, our CWM can fit the true distribution even better. 
対照的に、私たちのCWMは真の分布にさらに良く適合します。

Fig12(b) shows the true and estimated watch time distribution on videos with 30s duration on KuaiRand. 
図12(b)は、KuaiRandの30秒の動画における真の視聴時間分布と推定視聴時間分布を示しています。

It can be found that PCR only estimates a single-peaked distribution which differs significantly from the true bimodal distribution. 
PCRは、真の二峰性分布とは大きく異なる単峰性分布のみを推定していることがわかります。

In comparison, CWM can estimate a similar bimodal distribution to the true distribution, demonstrating CWM’s effectiveness in watch time prediction. 
比較すると、CWMは真の分布に類似した二峰性分布を推定でき、視聴時間予測におけるCWMの効果を示しています。



## Instructions for reporting errors エラー報告の手順

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. 
私たちは論文のHTMLバージョンを改善し続けており、あなたのフィードバックはアクセシビリティとモバイルサポートの向上に役立ちます。 
To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:
HTMLのエラーを報告して、変換とレンダリングの改善に役立てるために、以下のいずれかの方法を選択してください：

- Click the "Report Issue" button.
- "Report Issue"ボタンをクリックしてください。
- Open a report feedback form via keyboard, use "Ctrl + ?".
- キーボードを使用して報告フィードバックフォームを開くには、「Ctrl + ?」を使用してください。
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
