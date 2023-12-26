## link

- https://arxiv.org/abs/1907.05559

## title

NPA: Neural News Recommendation with Personalized Attention

## abstract

News recommendation is very important to help users find interested news and alleviate information overload. Different users usually have different interests and the same user may have various interests. Thus, different users may click the same news article with attention on different aspects. In this paper, we propose a neural news recommendation model with personalized attention (NPA). The core of our approach is a news representation model and a user representation model. In the news representation model we use a CNN network to learn hidden representations of news articles based on their titles. In the user representation model we learn the representations of users based on the representations of their clicked news articles. Since different words and different news articles may have different informativeness for representing news and users, we propose to apply both word- and news-level attention mechanism to help our model attend to important words and news articles. In addition, the same news article and the same word may have different informativeness for different users. Thus, we propose a personalized attention network which exploits the embedding of user ID to generate the query vector for the wordand news-level attentions. Extensive experiments are conducted on a real-world news recommendation dataset collected from MSN news, and the results validate the effectiveness of our approach on news recommendation.

# Introduction

Online news platforms such as MSN News and Google News have attracted a huge number of users to read digital news [7, 18]. However, massive news articles are emerged everyday, and it is impractical for users to seek for interested news from a huge volume of online news articles [26, 34]. Therefore, it is an important task for online news platforms to target user interests and make personalized news recommendation [1, 8, 14], which can help users to find their interested news articles and alleviate information overload [32, 35]. There are two common observations in the news recommendation scenario. First, not all news clicked by users can reflect the preferences of users. For example, as illustrated in Figure 1, user-1 clicked all the three news, but he/she was only interested in the first and the second news. In addition, the same news should also have different informativeness for modeling different users. For example, if user-1 is very interested in sports news but user-2 rarely reads, the news “Dolphins May Have Found A Head Coach” is very informative for characterizing user-1, but less informative for user-2. Second, different words in news titles usually have different informativeness for learning news representations. For example, the word “Crazy” in the first news title is informative, while the word “That” is uninformative. Moreover, the same words within a news title may also have different informativeness for revealing preferences of different users. For example, user-1 may be attracted by the word “Crazy”, and user-2 may pay more attention to the words “Actually Work”. Therefore, modeling the different informativeness of words and news for different users may be useful for learning better representations of users for accurate news recommendation.

Existing news recommendation methods are usually based on collaborative filtering (CF) techniques and news content[20–22, 24]. For example, Liu et al. [21] proposed a CF-based approach for news recommendation based on user interests. They use a Bayesian model to extract the interest features of users based on the click distributions on news articles in different categories. Okura et al. [24] proposed to first learn the distributed representations of news articles based on similarity and then use recurrent neural networks to learn user representations from browsing histories for click prediction. Lian et al. [20] proposed a deep fusion model (DMF) to learn representations of users and news using combinations of fully connected networks with different depth. They also used attention mechanism to select important user features. However, all these existing methods cannot model the different informativeness of news and their words for different users, which may be useful for improving the quality of personalized news recommendation.

In this paper, we propose a neural approach with personalized attention (NPA) for news recommendation. The core of our approach is a news representation model and a user representation model. In the news representation model we use a CNN network to learn the contextual representations of news titles, and in the user representation model we learn representations of users from their clicked news. Since different words and news articles usually have different informativeness for learning representations of news and users, we propose to apply attention mechanism at both word- and news-level to select and highlight informative words and news. In addition, since the informativeness of the same words and news may be different for different users, we propose a personalized attention network by using the embedding of user ID as the query vector of the word- and news-level attention networks to differentially attend to important words and news according to user preferences. Extensive experiments on a real-world dataset collected from MSN news validate the effectiveness of our approach on news recommendation.

# Related Work

## News Recommendation

News recommendation is an important task in the data mining field, and have been widely explored over years. Traditional news recommendation methods usually based on news relatedness [23], semantic similarities [3] and human editors’ demonstration [33]. However, the preferences of users cannot be effectively modeled. Therefore, most news recommendation methods are based on CF techniques. The earliest study on CF methods for news recommendation is the Grouplens project [17], which applied CF methods to aggregate news from Usenet. However, pure CF methods usually suffer from the sparsity and the cold-start problems, which are especially significant in news recommendation scenarios [19]. Thus, content-based techniques are usually complementary methods to CF [2, 20, 21, 24, 27, 29, 32, 39]. For example, Liu et al. [21] proposed to incorporate user interests for news recommendation. They use a Bayesian model to predict the interests of users based on the distributions of their clicked news articles in different categories. Okura et al. [24] proposed to learn news embeddings based on the similarities between news articles in the same and different categories. They use recurrent neural networks to learn user representations from the browsing histories through time to predict the score of news. Lian et al. [20] proposed a deep fusion model (DMF) to learn representations of users from various features extracted from their news reading, general web browsing and web searching histories. They used an inception network with attention mechanism to select important user features and combine the features learned by networks with different depths. Wang et al. [32] proposed to use the embeddings of the entities extracted from a knowledge graph as a separate channel of the CNN input. However, these existing methods cannot simultaneously model the informativeness of words and news. Different from all these methods, we propose to use personalized attention mechanism at both word- and new-level to dynamically recognize different informative words and news according to the preference of different users. Experimental results validate the effectiveness of our approach.

## Neural Recommender Systems

In recent years, deep learning techniques have been widely used in recommender systems [31]. For example, Xue et al. [37] proposed to use multi-layer neural networks to learn the latent factors of users and items in matrix factorization. However, the content of users and items cannot be exploited, which is usually important for recommender systems. Different from using neural networks within traditional matrix factorization frameworks, many methods apply neural networks to learn representations of users and items from raw features [5, 6, 9, 11–13]. For example, Huang et al. [13] proposed a deep structured semantic model (DSSM) for click-through rate (CTR) prediction. They first hashed the very sparse bag-of-words vectors into low-dimensional feature vectors based on character n-grams, then used multi-layer neural networks to learn the representations of query and documents, and jointly predicted the click score of multiple documents. Cheng et al. [5] proposed a Wide & Deep approach to combine a wide channel using a linear transformer with a deep channel using multi-layer neural networks. Guo et al. [11] proposed a DeepFM approach which combines factorization machines with deep neural networks. The two components share the same input features and the final predicted score is calculated from the combination of the output from both components. However, these methods usually rely on handcrafted features, and the dimension of feature vectors is usually huge. In addition, they cannot effectively recognize the important contexts when learning news and user representations. Different from the aforementioned methods, our approach can dynamically select important words and news for recommendation based on user preferences, which may be useful for learning more informative user representations for personalized news recommendation.

# Our Approach

In this section, we introduce our NPA approach with personalized attention for news recommendation. There are three major modules in our model. The first one is a news encoder, which aims to learn the representations of news. The second one is a user encoder, which aims to learn user representations based on the representations of his/her clicked news. The third one is a click predictor, which is used to predict the click score of a series of candidate news. In the news encoder and user encoder module, we apply personalized attention networks at both word- and new-level to differentially select informative words and news according to user preferences. The architecture of our approach is shown in Figure 2. We will introduce the details of our approach in the following sections.

## News Encoder

Since users’ click decisions on news platforms are usually made based on the titles of news articles, in our approach the news encoder module aims to learn news representations from news titles. As shown in Figure 2, there are three sub-modules in the news encoder module.

The first one is word embedding. It is used to convert a sequence of words within news title into a sequence of low-dimensional dense vectors. We denote the word sequence of the news Di as Di = [w1,w2, ...,wM ], where M is the number of words in the news title. The word sequence Di is transformed into a sequence of vector E w = [e1, e2, ..., eM ] using a word embedding matrix We ∈ RV ×D , where V denotes the vocabulary size and D denotes the dimension of word embedding vectors.

The second one is a convolutional neural network (CNN) [15]. CNN is an effective neural architecture for capturing local information [36]. Usually, local contexts within news are important for news recommendation. For example, in the news title “best Fiesta bowl moments”, the local combination of the words “Fiesta” and “bowl” is very important to infer the topic of this news. Thus, we apply a CNN network to the word sequences to learn contextual representations of words within news titles by capturing their local contexts. Denote the representation of the i-th word as ci , which is calculated as:

$$
\tag{1}
$$

where e(i−k):(i+k) denotes the concatenation of the word embeddings from the position (i − k) to (i + k). Fw ∈ RNf ×(2k+1)D and bw ∈ RNf denote the parameters of the CNN filters, where Nf is the number of CNN filters and 2k+1 is their window size. ReLU [10] is used as the non-linear function for activation. The output of the CNN layer is the sequence of contextual word representation vectors, denoted as [c1, c2, ..., cM ].

The third one is a word-level personalized attention network. Different words in a news title usually have different informativeness for characterizing the topics of news. For example, in the news entitled with “NBA games in this season” the word “NBA” is very informative for learning news representations, since it conveys important clues about the news topic, while the word “this” is less informative for recommendation. In addition, the same word may also have different informativeness for the recommendation of different users. For example, in the news title “Genesis G70 is the 2019 MotorTrend Car of the Year”, the words “Genesis” and “MotorTrend” are informative for the recommendation of users who are interested in cars, but may be less informative for users who are not interested. Thus, recognizing important words for different users is useful for news recommendation. However, in vanilla non-personalized attention networks [20], the attention weights are only calculated based on the input representation sequence via a fixed attention query vector, and the user preferences are not incorporated. To model the informativeness of each word for the recommendation of different users, we propose to use a personalized attention network to recognize and highlight important words within news titles according to user preferences. The architecture of our personalized attention module is shown in Figure 3. In order to obtain the representation of user preferences, we first embed the ID of users into a representation vector eu ∈ RDe , where De denotes the size of user embedding. Then we use a dense layer to learn the word-level user preference query qw as:

$$
\tag{2}
$$

where Vw ∈ RDe×Dq and vw ∈ RDq are parameters, Dq is the preference query size. In this module, the attention weight of each word is calculated based on the interactions between the preference query and word representations. We denote the attention weight of the i-th word as αi , which is formulated as:

$$
\tag{3}
$$

$$
\tag{4}
$$

where Wp ∈ RDq×Nf and bp ∈ RNf are projection parameters. The final contextual representation ri of the i-th news title is the summation of the contextual representations of words weighted by their attention weights:

$$
\tag{5}
$$

We apply the news encoder to all users’ clicked news and candidate news. The representations of clicked news of a user and candidate news are respectively denoted as [r1, r2, ..., rN ] and [r ′ 0 , r ′ 1 , ..., r ′ K ], where N is the number of clicked news and K + 1 is the number of candidate news.

## User Encoder

The user encoder module in our approach aims to learn the representations of users from the representations of their clicked news, as shown in Figure 2. In this module, a news-level personalized attention module is used to build informative user representations. Usually the news clicked by the same user have different informativeness for learning user representations. For example, the news “10 tips for cooking” is very informative for modeling user preferences, but the news “It will be Rainy next week” is less informative. In addition, the same news also has different informativeness for modeling different users. For example, the news “100 Greatest Golf Courses” is informative for characterizing users who are interested in golf, but is noisy for modeling users who are actually not interested in. To model the different informativeness of the same news for different users, we also apply personalized attention mechanism to the representations of news clicked by the same user. Similar with the word-level attention network, we first transform the user embedding vector into a news preference query qd , which is formulated as:

$$
\tag{6}
$$

where Vd ∈ RDe×Dd and vd ∈ RDd are parameters, Dd is the dimension of the news preference query.

We denote the attention weight of the i-th news as α ′ i , which is calculated by evaluating the importance of the interactions between the news preference query and news representations as follows:

$$
\tag{7}
$$

$$
\tag{8}
$$

where Wd ∈ RDd×Nf and bd ∈ RNf are projection parameters. The final user representation u is the summation of the news contextual representations weighted by their attention weights:

$$
\tag{9}
$$

## Click Predictor

The click predictor module is used to predict the click score of a user on each candidate news. A common observation in news recommendation is that most users usually only click a few news displayed in an impression. Thus, the number of positive and negative news samples is highly imbalanced. In many neural news recommendation methods [20, 32], the model only predicts the click score for a single piece of news (the sigmoid activation function is usually used in these methods). In these methods, positive and negative news samples are manually balanced by randomly sampling, and the rich information provided by negative samples is lost. In addition, since the total number of news samples is usually huge, the computational cost of these methods is usually heavy during model training. Thus, these methods are sub-optimal for simulating realworld news recommendation scenarios. Motivated by [13] and [38], we propose to apply negative sampling techniques by jointly predicting the click score for K +1 news during model training to solve the two problems above. The K + 1 news consist of one positive sample of a user, and K randomly selected negative samples of a user. The score yˆi of the candidate news D ′ i is calculated by the inner product of the news and user representation vector first, and then normalized by the softmax function, which is formulated as:

$$
\tag{10}
$$

$$
\tag{11}
$$

For model training, we formulate the click prediction problem as a pseudo K + 1 way classification task, i.e., the clicked news is the positive class and all the rest news are negative classes. We apply maximum likelihood method to minimize the log-likelihood on the positive class:

$$
\tag{12}
$$

where yj is the gold label, S is the set of the positive training samples. By optimizing the loss function L via gradient descend, all parameters can be tuned in our model. Compared with existing news recommendation methods, our approach can effectively exploit the useful information in negative samples, and further reduce the computational cost for model training (nearly divided by K). Thus, our model can be trained more easily on a large collection of news click logs.

# Experiments

## Datasets and Experimental Settings

Our experiments were conducted on a real-world dataset, which was constructed by randomly sampling user logs from MSN News1 in one month, i.e., from December 13rd, 2018 to January 12nd, 2019. The detailed statistics of the dataset is shown in Table 12 . We use the logs in the last week as the test set, and the rest logs are used for training. In addition, we randomly sampled 10% of samples for validation.

In our experiments, the dimension D of word embedding was set to 300. we used the pre-trained Glove embedding3 [25], which is trained on a corpus with 840 billion tokens, to initialize the embedding matrix. The number of CNN filters Nf was set to 400, and the window size was 3. The dimension of user embedding De was set to 50. The sizes of word and news preferences queries (Dq and Dd ) were both set to 200. The negative sampling ratio K was set to 4. We randomly sampled at most 50 browsed news articles to learn user representations. We applied dropout strategy [30] to each layer in our approach to mitigate overfitting. The dropout rate was set to 0.2. Adam [16] was used as the optimization algorithm for gradient descend. The batch size was set to 100. Due to the limitation of GPU memory, the maximum number of clicked news for learning user representations was set to 50 in neural network based methods, and the maximum length of news title was set to 30. These hyperparameters were selected according to the validation set. The metrics in our experiments include the average AUC, MRR, nDCG@5 and nDCG@10 scores over all impressions. We independently repeated each experiment for 10 times and reported the average performance.

## Performance Evaluation

First, we will evaluate the performance of our approach by comparing it with several baseline methods. The methods to be compared include:

- LibFM [28], which is a state-of-the-art feature-based matrix factorization and it is a widely used method for recommendation. In our experiments, we extract the TF-IDF features from users’ clicked news and candidate news, and concatenate both types of features as the input for LibFM.
- CNN [15], applying CNN to the word sequences in news titles and use max pooling technique to keep the most salient features, which is widely used in content-based recommendation [4, 40].
- DSSM [13], a deep structured semantic model with word hashing via character trigram and multiple dense layers. In our experiments, we concatenate all user’s clicked news as a long document as the query, and the candidate news are documents. The negative sampling ratio was set to 4.
- Wide & Deep [5], using the combination of a wide channel using a linear transformer and a deep channel with multiple dense layers. The features we used are the same with LibFM for both channels.
- DeepFM [11], which is also a widely used neural recommendation method, using a combination with factorization machines and deep neural networks. We use the same TF-IDF features to feed for both components.
- DFM [20], a deep fusion model by using combinations of dense layers with different depths. We use both TF-IDF features and word embeddings as the input for DFM.
- DKN [32], a deep news recommendation method with Kim CNN and news-level attention network. They also incorporated entity embeddings derived from knowledge graphs.
- NPA, our neural news recommendation approach with personalized attention.

The experimental results on news recommendation are summarized in Table 2. According to Table 2, We have several observations.

First, the methods based on neural networks (e.g., CNN, DSSM and NPA) outperform traditional matrix factorization methods such as LibFM. This is probably because neural networks can learn more sophisticated features than LibFM, which is beneficial for learning more informative latent factors of users and news.

Second, the methods using negative sampling (DSSM and NPA) outperform the methods without negative sampling (e.g., CNN, DFM and DKN). This is probably because the methods without negative sampling are usually trained on a balanced dataset with the same number of positive and negative samples, and cannot effectively exploit the rich information conveyed by negative samples. DSSM and our NPA approach can utilize the information from three more times of negative samples than other baseline methods, which is more suitable for real-world news recommendation scenarios.

Third, the deep learning methods using attention mechanism (DFM, DKN and NPA) outperform most of the methods without attention mechanism (CNN, Wide & Deep and DeepFM). This is probably because different news and their contexts usually have different informativeness for recommendation, and selecting the important features of news and users is useful for achieving better recommendation performance.

Fourth, our approach can consistently outperform all compared baseline methods. Although DSSM also use negative sampling techniques to incorporate more negative samples, it cannot effectively utilize the contextual information and word orders in news titles. Thus, our approach can outperform DSSM. In addition, although DFM uses attention mechanism to select important user features, it also cannot effectively model the contexts within news titles, and cannot select important words in the candidate news titles. Besides, although DKN uses a news-level attention network to select the news clicked by users, it cannot model the informativeness of different words. Different from all these methods, our approach can dynamically recognize important words and news according to user preferences. Thus, our approach can outperform these methods.

Next, we will compare the computational cost of our approach and the baseline methods. To summarize, the comparisons are shown in Table 34 . We assume that during the online test phase, the model can directly use the intermediate results produced by hidden layers. From Table 3, we have several observations.

First, comparing our NPA approach with feature-based methods, the computational cost on time and memory during training is lower if N is not large, since the dimension Df of the feature vector is usually huge due to the dependency on bag-of-words features.5 In addition, the computational cost in the test phase is only a little more expensive than these methods since De is not large.

Second, comparing our NPA approach with CNN, DFM and DKN, the training cost is actually divided by K with the help of negative sampling. In addition, the computational cost of NPA in the test phase much smaller than DKN and DFM, since DKN needs to use the representations of the candidate news as the query of the news-level attention network and the score needs to be predicted by encoding all news clicked by a user, which is very computationally expensive. DFM needs to take the sparse feature vector as input, which is also computationally expensive. Different from these baseline methods, our approach can be trained at a low computational cost, and can be applied to online services to handle massive users at a satisfactory computational cost.

Finally, we want to evaluate the performance of our approach in each day to explore the influence of user click behaviors over time. The performance of our approach in each day of the week for test (1/6/2019-1/12/2019) is shown in Figure 4. According to the results, the performance of our approach is best on the first day in the test week (1/6/2019). This is intuitive because the relevance of user preferences is usually strong between neighbor days. In addition, as time went by, the performance of our approach begins to decline. This is probably because news are usually highly timesensitive and most articles in common news services will be no longer recommended for users within several days (Usually two days for MSN news). Thus, more news will not appear in the training set over time, which leads to the performance decline. Fortunately, we also find the performance of our approach tends to be stable after three days. It shows that our model does not simply memorize the news appear in the training set and can make personalized recommendations based on user preferences and news topics. Thus, our model is robust to the news update over time.

## Effectiveness of Personalized Attention

In this section, we conducted several experiments to explore the effectiveness of the personalized attention mechanism in our NPA approach. First, we want to validate the advantage of personalized attention on vanilla non-personalized attention for news recommendation. The performance of NPA and its variant using vanilla attention and without attention is shown in Figure 5. According to Figure 5, we have several observations. First, the models with attention mechanism consistently outperform the model without attention. This is probably because different words and news usually have different informativeness for news recommendation. Therefore, using attention mechanism to recognize and highlight important words and news is useful for learning more informative news and user representations. In addition, our model with personalized attention outperforms its variant with vanilla attention. This is probably because the same words and news should have different informativeness for the recommendation of different users. However, vanilla attention networks usually use a fixed query vector, and cannot adjust to different user preferences. Different from vanilla attention, our personalized attention approach can dynamically attend to important words and news according to user characteristics, which can benefit news and user representation learning.

Then, we want to validate the effectiveness of the personalized attention at word-level and news-level. The performance of NPA and its variant with different combinations of personalized attention is shown in Figure 6. According to Figure 6, we have several observations. First, the word-level personalized attention can effectively improve the performance of our approach. This is probably because words are basic units to convey the meanings of news titles and selecting the important words according to user preferences is useful for learning more informative news representations for personalized recommendation. Second, the news-level personalized attention can also improve the performance of our approach. This is probably because news clicked by users usually have different informativeness for learning user representations, and recognizing the important news is useful for learning high quality user representations. Third, combining both word- and news-level personalized attention can further improve the performance of our approach. These results validate the effectiveness of the personalized attention mechanism in our approach.

## Influence of Negative Sampling

In this section, we will explore the influence of the negative sampling technique on the performance of our approach. To validate the effectiveness of negative sampling, we compare the performance of our approach with its variant without negative sampling. Following [20, 32], we choose to train this variant on a balanced training set by predicting the click scores of news articles one by one (the final activation function is changed to sigmoid). The experimental results are shown in Figure 7. According to Figure 7, the performance of our approach can be effectively improved via negative sampling. Since negative samples are dominant in the training set, they usually contain rich information for recommendation. However, the information provided by negative samples cannot be effectively utilized due to the limitation of balanced sampling. Therefore, the performance is usually sub-optimal. Different from this variant, our NPA approach can incorporate richer information in negative samples, which may be very useful for achieving better performance on news recommendation.

## Hyperparameter Analysis

In this section, we will explore the influence of an important hyperparameter in our approach, i.e., the negative sampling ratio K, which aims to control the number of negative samples to combine with a positive sample. The experimental results on K are shown in Figure 8. According to Figure 8, we find the performance of our approach first consistently improves when K increases. This is probably because when K is too small, the number of negative samples incorporated for training is also small, and the useful information provided by negative samples cannot be fully exploited, which will lead to sub-optimal performance. However, when K is too large, the performance will start to decline. This is probably because when too many negative samples are incorporated, they may become dominant and it is difficult for the model to correctly recognize the positive samples, which will also lead to sub-optimal performance. Thus, a moderate setting of K may be more appropriate (e.g., K = 4).

## Case Study

In this section, we will conduct several case studies to visually explore the effectiveness of the personalized attention mechanism in our approach. First, we want to explore the effectiveness of the word-level personalized attention. The visualization results of the clicked and candidate news from two sample users are shown in Figure 9(a). From Figure 9(a), we find the attention network can effectively recognize important words within news titles. For example, the word “nba” in the second news of user 1 is assigned high attention weight since it is very informative for modeling user preferences, while the word “survey” in the same title gains low attention weight since it is not very informative. In addition, our approach can calculate different attention weights for the words in the same news titles to adjust to the preferences of different users. For example, according to the clicked news, user 1 may be interested in sports news and user 2 may be interested in movie related news. The words “super bowl” are highlighted for user 1 and the words “superheroes” and “movies” are highlighted for user 2. These results show that our approach can learn personalized news representations by incorporating personalized attention.

Then, we want to explore the effectiveness of the news-level attention network. The visualization results of the clicked news are shown in Figure 9(b). From Figure 9(b), we find our approach can also effectively recognize important news of a user. For example, the news “nfl releases playoff schedule : cowboys-seahawks on saturday night” gains high attention weight because it is very informative for modeling the preferences of user 1, since he/she is very likely to be interested in sports according to the clicked news. The news “new year’s eve weather forecast” is assigned low attention weight, since it is uninformative for modeling user preferences. In addition, our approach can model the different informativeness of news for learning representations of different users. For example, the same sports news “10 nfl coaches who could be fired on black monday” is assigned high attention weight for user 1, but relatively low for user 2. According to the clicked news of both users, user 1 is more likely to be interested in sports than user 2 and this news may be noisy for user 2. These results show that our model can evaluate the different importance of the same news for different users according to their preferences.

# Conclusion

In this paper, we propose a neural news recommendation approach with personalized attention (NPA). In our NPA approach, we use a news representation model to learn news representations from titles using CNN, and use a user representation model to learn representations of users from their clicked news. Since different words and news articles usually have different informativeness for representing news and users, we proposed to apply attention mechanism at both word- and news to help our model to attend to important words and news articles. In addition, since the same words and news usually have different importance for different users, we propose a personalized attention network which exploits the embeddings of user ID as the queries of the word- and news-level attention networks. The experiments on the real-world dataset collected from MSN news validate the effectiveness of our approach.
