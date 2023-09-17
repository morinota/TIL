## link

- https://medium.com/smartnews-inc/user-behavior-sequence-for-items-recommendation-in-smartnews-ads-2376622f6192

## title

User Behavior Sequence for Items Recommendation in SmartNews Ads

## NLP vs. Recommendation

User historical behavior sequences give us objective data about a user, regardless of his/her gender/age/income, which is ultimately reflected in what he/she has seen and purchased. Therefore, how to mine user preferences from behavioral sequences is a hot area in recommendation systems.

The traditional approach is to process these sequences statistically, e.g. collaborative filtering, which calculates the probability that a user who has bought item A will buy item B as a recommendation score. Or calculating the average number of times a user has viewed a category/store, the number of activities in a certain time interval for feature modeling, and so on. However, when it comes to sequences, natural language processing (NLP) is essentially solving this type of problem. A sentence is a sequence, and a conversation is a combination of sequences of sentences. So in the NLP domain, researchers have been thinking about how to effectively characterize sentences or even strings of conversations (paragraphs).

![](https://miro.medium.com/v2/resize:fit:1400/0*DslE4AF44bC9PnwX)

As shown above, around 2015, we can observe a series of model breakthroughs, from RNN -> LSTM/GRU -> Attention -> Transformer -> Bert -> Bert variants, and watch the SOTA list keep rotating and breaking, while the techniques of these models are also starting to ferment in other domains. For example, in the field of vision, the Transformer has been used for different tasks, e.g. DETR-based improvements in Object Detection have also yielded SOTA results. In the field of speech, the presence of Transformer can be seen in speech recognition, speech synthesis and text-to-speech. In the field of search and push, it is also following the evolution of NLP. From GRU4Rec -> NARM -> SASRec -> Bert4Rec, it has been in public testing and breakthroughs. The same is true for news recommendation, which is more relevant to NLP, and furthermore, finetune through PLM (Pretrained Language Model) has achieved very good results.

However, beyond academics, it is important to know whether it can really bring improvements in business scenarios. In particular, NLP features are simple, consisting mainly of sentences and words, with some scenarios adding keywords and lexical properties. However, in the case of recommendations, there are many other features that affect user clicks and purchases (e.g. super sales day/product prices/discount etc.). Imagine that we often buy things that we wouldn’t normally buy because of a discount on a Black Friday.

Today we’re going to take a look at how we’re using SmartNews user historical behavior data in an advertising scenario, and share our tips on how to do this in practice.

## SmartNews Ads Scenario

In SmartNews Ads, there are a lot of advertisers who want to advertise products that will be exposed to interested users and lead to purchases or app installs. For example, like e-commerce advertisers, there may be tens of millions of items, and our platform has to recommend the right items to different users to achieve the advertiser’s CPA/ROAS expectations based on different optimization goals.

![](https://miro.medium.com/v2/resize:fit:1400/0*eXQQUCRpjM5eOvJE)

It is necessary to use the user’s behavioral data on the SmartNews to better understand the user and achieve better recommendations. Basic recommendations, such as what users have seen recently, or recommending similar items based on CF, are already very effective in their own right. But now that we have the user behavioral sequence data, we try to incorporate the sequence recommendation modeling approach to see if it can lead to better recommendation results and user experience.

The diagram below shows the scenario we want to model. When we know the user’s historical behavior, can we guess what items the user will be most interested in next!

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*uJrnTI2Sm0VdVba0.png)

## Tech Detail / Trick

### Model Selection

As mentioned before, there are a range of models in the recommendation domain that also attempt to deal with sequences. Here we have chosen SASRec as the basis for our experiments, which is a Self-Attention based model architecture with the clear idea of using the past N product sequences to predict the N+1th product. The overall structure is shown in the figure below, using the Multi-head Attention mechanism to obtain a vector of the first N items, hoping that the inner product of the vector with the next item is greater than the other negative sample items. The inference is made by putting the user’s historical behavior into the model, obtaining the vector, and using the ANN to find the next most likely TopK item from a pool of 10 million items.

![](https://miro.medium.com/v2/resize:fit:1400/0*YGRlGEFLL1p_wNj3)

### Improve Training Speed

In order to use sequential modeling, a common training framework resembles a double tower (as shown in Fig. 5), with the left tower being the User Representation, i.e. the past historical behavior of the user. The right tower is the next item, which is finally compared to the label (positive or negative), using dot or cosine. If there are 10M users, and each user takes 50 different historical behavior sequences, and 3 negative samples, then there are 2 billion (10M _ 50 _ (1+3)) samples in total, which is a very high training time and iteration cost.

An optimization point here is that much of the historical behavior data of the same user is calculated repeatedly. For example, the first sample sequence is T0 to T50, the second sample sequence is T1 to T51, and the middle sequence (T2 to T50) is actually the same. SASRec’s training approach solves this problem considerably. For each user, we take a sequence of historical behaviors (e.g. T0 to T50, then T0 predicts T1, T0 to T1 predicts T2, and so on). Since Self Attention looks at the entire sequence, a Mask is introduced to mask the items to the right of the Target Item in order to avoid message traversal due to future click behaviors. Thus, by walking through Attention, we actually get a vector of N different sequences and train N samples. This way of training makes the overall training speed shorter, for a billion levels of click data, it only takes 3~4 hours to get a good convergence result, and it is also convenient for us to do parameter fine-tuning and model iteration.

![](https://miro.medium.com/v2/resize:fit:1400/0*aJHT3_bGIvERfhaY)

### K+1 Cross-entropy

The original Loss Function was trained to discriminate binary classification, assuming the target is whether the user clicks or not, and the label is click/no click. However, because in advertising, our scenario is first used in the recall phase, we do not need to consider the accuracy of the CTR value, but rather the accuracy of the recommended sequence. Therefore, in order to speed up the learning of the model, the loss function is also used in a way like DSSM, where each positive sample is combined with K negative samples, and then these K+1 scores are passed through a Softmax, which judges whether the prediction of the positive samples is correct. This approach allows for faster convergence and saves training time while ensuring the correctness of the sequence (hopefully maximizing the score of the positive samples). This training approach is often used in other scenarios as well. For example, in an NLP task, where we want to know what the next sentence in the sentence is most likely to follow, the same can be converted into a classification task and trained with great effect.

![](https://miro.medium.com/v2/resize:fit:1064/0*9xLTuBWZoGxXioHK)

### Integrate Other Features

SASRec only uses the item id as a feature. However, there is a lot of side information that can be used to help with training, such as title / description / image / category and other multimodal features that may be able to better characterize the items. The easiest way to do this is to concatenate these features and turn them into a fixed vector after an MLP. In this paper, FDSA introduces an attention mechanism, with the idea that attention is used to learn which features most influence user choice. In our experiments, however, most of the id features are quick to train and work well. However, in some verticals, such as real estate/used cars, the addition of some features can improve the conversion rate a lot. For example, the type of house/price/distance from the metro station, etc., and the mileage/brand/price of a used car are all important variables for conversion. Also in the cold start of an item, it is helpful to generalize the item’s features.

![](https://miro.medium.com/v2/resize:fit:1400/0*46i0gnC0EZWWZEhu)

### Auto Tuning

Although the overall training time can be compressed to 3–4 hours, it is particularly time-consuming to do tuning (e.g. dimension / dropout rate / learning rate / multi-head / blocks, etc.) if it cannot be done in parallel. Thanks to the SmartNews AI-Infra team, which has adopted Microsoft’s NNI to support fast Auto Tuning, the framework is able to automatically get the best parameters from a defined range of parameters, through a number of Search Algorithms, and supports parallel training. Experimental results also show that the appropriate parameters vary in different vertical domains and data sizes. With this training, the CTR can be increased by 5–10%. The user’s Reject Rate is also reduced by another 10%.

![](https://miro.medium.com/v2/resize:fit:1400/0*Z2KcvFq7M7K4vugw)

## Cold Start Scenario

We have two types of Cold Start, new items and new users. In fact, the retention rate is different for different items in different areas. For example, in the e-commerce scenario, the rate of new items is relatively low compared to old items. So even if we only use product ids for modeling, we can still get good results. However, in an auction scenario, such as eBay, where many items are auctioned off and gone, the ratio of new items is particularly high as new items are constantly being auctioned. This requires the use of multimodality to generalize the items to make recommendations for new items (e.g. FDSA with multimodal features).

For new users, it is relatively difficult, as they need to have a cold start period to collect user behavior to understand their interests. If you only look at advertising behavior, the data collection takes even longer. In the absence of sufficient user historical behavior sequences, the sequence model is not applicable. Another idea is to use the user’s news click sequence on the APP (which is easier to collect) to establish a relationship with the product, which is another interesting challenge.

## Performance

We trained individual models for different domains, such as e-commerce/property/automotive/auction, and were able to increase click-through rates by 10–20% compared to the original CF i2i model. Some small advertisers in some verticals were even able to increase their CVR by around 30%, which was very impressive, even though the models were not specifically optimized for CVR. However, in the case of large e-merchants with more than 10M products, the advantage is not so obvious. The click-through rate only increases by about 5%. But another significant improvement is the user reject rate, which can be reduced by about 10–20%. We interpret this as the model recommending products that are more in line with the user’s interests, so that the user does not feel annoyed by the ads, making the overall user experience better.

## Future work

### News to Ads

SmartNews is an information app and has a lot of user news reading sequences. If we could model the user’s news viewing behavior and transfer it to item recommendations, this could be very helpful for new users and be of greater value to advertisers. Intuitively, the correlation between news and purchase is weak most of the time, but it would be particularly valuable if user interests could be tapped from the news sequence and then transferred to merchandise to bring new users to advertisers.

### How to Add Any Features

More features are better. However, adding all of the features doesn’t necessarily pay off for the model results. Many statistical features in recommendations are also very effective. If you add them all to the attention, sometimes they tend to skew the model, and can’t get much effect. So for statistical features, it is possible to train them separately and finally fuse individual scores in an MLP to get better results. At the moment, there is no significant gain in all aspects through FDSA, but the cost of training is much higher.

### PLM Model

In the NLP domain, it is a common paradigm to use Bert to do large-scale training and then fine-tune for downstream tasks. In recommendation, if the amount of data is large enough, we can also try to train a base model by self-data and use self-supervised training to train the model as a pre-train model for downstream tasks, which can accelerate the convergence and also bring benefits to some small advertisers. For example, much new research in News Recommendation uses the NLP pre-train model to finetune, which can get better results.
