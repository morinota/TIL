## link

- https://www.mdpi.com/2673-6470/4/1/3

## Abstract

News recommender systems (NRS) are crucial for helping users navigate the vast amount of content available online. However, traditional NRS often suffer from biases that lead to a narrow and unfair distribution of exposure across news items. In this paper, we propose a novel approach, the Contextual-Dual Bias Reduction Recommendation System (C-DBRRS), which leverages Long Short-Term Memory (LSTM) networks optimized with a multi-objective function to balance accuracy and diversity. We conducted experiments on two real-world news recommendation datasets and the results indicate that our approach outperforms the baseline methods, and achieves higher accuracy while promoting a fair and balanced distribution of recommendations. This work contributes to the development of a fair and responsible recommendation system.

# Introduction

The proliferation of digital media and information has led to an exponential increase in the availability of news content. However, this abundance of information poses challenges for users in selecting relevant and high-quality content. In response, news recommender systems (NRS) [1] have become vital components of online news platforms. These systems provide personalized recommendations to users based on their behavior, preferences, and interactions [2]. The primary goal of NRS is to enhance user engagement and retention by delivering tailored news consumption experiences [3].
We present an example of a NRS, in in Figure 1, which considers User A, who frequently reads news articles related to environmental issues and sustainability. An NRS that focuses solely on accuracy would continuously recommend articles related to the environment and sustainability, based on User A’s past behavior. This can lead to an ’echo chamber’ effect [1], where the user is exposed only to news and opinions that align with their existing beliefs and interests. Conversely, the NRS prioritizing fairness might recommend a broader range of topics, including politics, economics, technology, and social issues.

In this study, we define ’fairness’ in the context of NRS as a balance between personalized recommendations and promoting content “diversity”. This approach aims to broaden users’ exposure to a variety of ideas and perspectives, though it might sometimes lead to less tailored recommendations, potentially affecting user engagement and satisfaction [4]. NRS often exhibit bias by prioritizing content that aligns with a user’s existing preferences, thus reinforcing their current beliefs and interests [5,6]. To counter this, fairness in NRS is about offering a diverse and representative range of content. We introduce a novel method that seeks to strike a balance between personalization and diversity, with the goal of optimizing both the relevance of recommendations and the breadth of content exposure.
State-of-the-art NRS predominantly concentrate on enhancing recommendation accuracy [2,7], which is commendable. However, there is a growing recognition of the need to balance accuracy with fairness [7,8,9]. In NRS, a focus solely on accuracy may inadvertently lead to limited content exposure, potentially creating echo chambers [10]. Conversely, a system prioritizing fairness might offer a diverse range of content but with recommendations that are less aligned with individual user preferences [11]. Hence, there is an imperative need for strategies that simultaneously achieve both accuracy and fairness, aiming for a more inclusive news consumption experience.
This study introduces a novel approach to news recommendation that optimizes both accuracy and fairness. Fairness is a wide subject, encompassing various dimensions and interpretations depending on the context. In the realm of information systems and algorithms [4,12], fairness often involves considerations like equal representation, unbiased treatment of different groups, and equitable distribution of resources or opportunities. It is about ensuring that systems and decisions do not favor one group or individual over another unjustly and that they reflect a balanced and inclusive approach. This is particularly crucial in areas such as news recommendations, hiring practices, and financial services, where the impact of unfairness can be significant on both individuals and society at large.
In this work, we particularly refer to ’diversity’ for fairness, ensuring that the recommendations cater to a wide range of interests and perspectives [13]. We propose a multi-objective optimization strategy for an NRS. Our contributions include the development of an algorithm that balances multiple factors, such as user preferences, content diversity, and fairness in exposure to different news sources. This approach not only enhances the relevance of recommendations but also promotes a diverse and inclusive news consumption experience. Our aim is to create a more holistic and responsible NRS.
We introduce the “Contextual Dual Bias Reduction Recommendation System (C-DBRRS)”, which ensures fairness in item and exposure aspects of news recommendation. Built on LSTM networks and optimized with a multi-objective function, C-DBRRS harmonizes accuracy and diversity in news recommendations. The hyperparameter 𝜆
allows for a tunable balance between relevance (precision, recall, NDCG) and fairness (Gini coefficient). This is a novel approach, as it recognizes the trade-offs between providing relevant recommendations to users and ensuring a fair representation of items.

# Literature Overview

News recommender systems (NRS) have been a widely researched topic in recent years due to the increasing amount of online news content and the need for personalized recommendations [1]. Traditional NRS are designed to provide users with personalized news articles based on their past behavior, preferences, and interests [14]. Collaborative filtering and content-based filtering are two common approaches used in recommender systems [15]. Collaborative filtering recommends news articles to a user based on the preferences of similar users, whereas content-based filtering recommends articles based on the content of the articles and the user’s past behavior.
Accuracy is a critical factor in the performance of recommender systems [1]. The accuracy of a recommender system refers to its ability to recommend items that are relevant and of interest to the user [3]. Commonly used metrics for evaluating the accuracy of recommender systems include the Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and the F1-score [16]. Several approaches have been proposed to improve the accuracy of recommender systems, such as incorporating additional contextual information [17], or using hybrid recommendation algorithms that combine the strengths of both collaborative filtering and content-based filtering [18].
Bias in recommender systems can manifest in various ways [8,9,19,20], including popularity bias, where the system tends to recommend popular items, leading to a lack of exposure for less popular or niche items [1]. Additionally, there might be biases related to gender, race, or other demographic factors, leading to discriminatory recommendations [21]. Researchers have proposed various fairness metrics to evaluate the fairness of recommender systems. These include statistical parity, which requires that the recommendations are independent of a protected attribute (e.g., gender, race), and disparate impact, which measures the ratio of positive outcomes for the protected group to the positive outcomes for the non-protected group [22,23]. A related approach [24] proposed a fairness-aware ranking algorithm that considers both the utility of the recommendations to the user and the fairness towards the items. Another approach is to re-rank the recommendations generated by a standard recommender system to improve fairness [20,23].
Fairness in recommender systems has gained attention due to the potential biases that can arise from the recommendation algorithms. Studies have shown that recommender systems can inadvertently reinforce existing biases in the data, leading to unfair recommendations for certain groups of users [21]. For example, a study [25] showed that a music recommender system was biased towards popular artists, leading to less exposure for less popular or niche artists. Several approaches have been proposed to address fairness in recommender systems, such as re-ranking the recommendations [22] or modifying the recommendation algorithm to incorporate fairness constraints [20].
Recent advancements in NRS emphasize a balance between accuracy and fairness, particularly in terms of diversity [5]. A novel multi-objective optimization strategy has been proposed to refine recommender system models. For instance, ref. [26] discusses an innovative algorithm utilizing multi-objective optimization. Similarly, ref. [13] proposes a framework to optimize recommender systems, emphasizing fairness across multiple stakeholders. Moreover, the use of multi-objective optimization for recommending online learning resources is effectively demonstrated [27]. Finally, ref. [28] highlights the application of big data in enhancing recommendation systems through multi-objective optimization.
There is often a trade-off between fairness and accuracy in recommender systems [29]. Improving fairness in the recommendations may lead to a decrease in accuracy, and vice versa. For example, a study [24] showed that incorporating fairness constraints into the recommendation algorithm led to a decrease in recommendation accuracy. Similarly, a study [30] showed that re-ranking the recommendations to improve fairness led to a decrease in accuracy. Therefore, it is important to carefully consider the trade-off between fairness and accuracy when designing and evaluating recommender systems.

# Materials and Methods

## Data

In our study, we utilized two real-world news recommendation datasets, namely MIND-small and Outbrain Click Prediction, which offer a comprehensive view of user interactions and preferences in news consumption.
MIND-small [2]: Derived from the larger MIND dataset, the MIND-small dataset, curated by Microsoft team, captures the interactions of 50,000 users on Microsoft News over a one-month period. For our study, we focused on this subset, analyzing their interactions with news articles, and associated metadata such as titles, categories, and abstracts.
Outbrain Click Prediction [31]: Sourced from a Kaggle competition hosted by Outbrain, this dataset provides an extensive record of user page views and clicks across various publisher sites in the United States over a span of 14 days. It offers valuable insights into user behaviors regarding displayed and clicked ads.
Our data preparation methodology involves several key stages to ensure the datasets were optimally configured for our recommender system. We started with fundamental data-cleaning procedures to enhance the quality and reliability of our datasets. This involved the removal of duplicate records and the addressing of missing or incomplete data through exclusion criteria. To enrich our analysis, we extracted several critical features from the datasets:
Textual Embeddings (BERT): we converted the text content of news articles into numerical vector representations using the BERT (base-uncased) model to encapsulate their semantic content.
Topic Modeling (LDA): articles were categorized into specific genres or themes using Latent Dirichlet Allocation (LDA).
Sentiment Analysis (VADER): we employed the VADER [32] tool to analyze the emotional tone of articles, classifying them as positive, negative, or neutral.
Post feature extraction, we standardized the scale of numerical features to ensure uniformity. Subsequently, we integrated detailed user interaction data, including clicks, views, and duration of engagement with each article, with the article features. This integration facilitated the creation of comprehensive user–article interaction profiles.
For effective processing using Long Short-Term Memory (LSTM) networks, we structured our data in the following manner:
Unified Input Vectors: each user–article interaction was represented as a unified vector, consolidating user behavioral data with the extracted article content features.
Time Series Formation: we structured the data into time series to capture the temporal dynamics of user interactions, a crucial aspect of LSTM processing.
The final stage in our data preparation was the division of the dataset into distinct sets for training, validation, and testing, following the 80-10-10 scheme in chronological temporal order. We combined and structured data from the MIND-small and Outbrain Click Prediction datasets to capture the temporal dynamics of user interactions with news articles. The following elements constitute our data structure:
User and Article Identifiers: unique IDs for users and articles to track interactions.
Interaction Timestamps: capture the timing of each interaction, crucial for time series analysis.
Interaction Types: categorized as clicks, views, and engagement duration.
Content Features: textual embeddings, topic categories, and sentiment scores for articles from MIND-small.
Sequential Interaction History: chronological sequence of user interactions, vital for learning user behavior patterns over time.

## Contextual Dual Bias Reduction Recommendation System

In this section, we introduce the Contextual Dual Bias Reduction Recommendation System (C-DBRRS) algorithm, which is an advanced LSTM-based algorithm tailored for news recommendation. C-DBRRS is designed to balance content relevance and fairness by mitigating item and exposure biases while adapting to dynamic user interactions and news features. The notations used in the equations of this section are in Table 1 and the algorithm is given in Algorithm 1.

The C-DBRRS employs a Long Short-Term Memory (LSTM) network to process sequences of input data 𝑥=(𝑥1,𝑥2,…,𝑥𝑡) , integrating user interactions with news content features. The LSTM updates its internal state at each time step t through the following mechanisms:

Input Gate controls how much new information flows into the cell state:

Forget Gate determines the information to be removed from the cell state:

Cell State Update generates new candidate values for updating the cell state:

Output Gate outputs the next hidden state reflecting the processed information:

To manage the trade-off between relevance and fairness in recommendations, the system employs a hyperparameter 𝜆 (described below). Relevance is assessed using metrics like Precision, Recall, and NDCG, whereas fairness is evaluated through the Gini coefficient. The optimization objective is formulated as:

In this optimization objective: 𝐿acc (Accuracy Loss) is typically the mean squared error (MSE) between the predicted and actual user interactions. It measures how accurately the system predicts user preferences based on their interaction history and content features. 𝐿item (Item Bias Loss) aims to reduce the bias towards frequently recommended items. It is computed by measuring the deviation of the item distribution in the recommendations from a desired distribution, such as a uniform distribution. 𝐿exp (Exposure Bias Loss) is designed to ensure that all items receive a fair amount of exposure in the recommendations. This is measured as the variance in the number of times different items are recommended, penalizing the model when certain items are consistently under-represented. The hyperparameters 𝛼,𝛽,𝛾 are used to balance these different aspects of the loss function. They are typically determined through experimentation and tuning, based on the specific characteristics of the data.

# Experimental Setup

## Baseline Methods

Our evaluation of the proposed C-DBRRS includes comparisons with a range of established recommendation methods, each offering unique strengths:
Popularity-based Recommendation (POP): this method ranks news articles based on their overall popularity, measured by the total number of user clicks.
Content-based Recommendation (CB): this method suggests articles to users by aligning the content of articles with their past preferences.
Collaborative Filtering (CF): this method utilizes user behavior patterns, recommending items favored by similar users.
Matrix Factorization (MF) [3]: this method decomposes the user–item interaction matrix into lower-dimensional latent factors for inferring user interests.
Neural Collaborative Filtering (NCF) [33]: this method combines neural network architectures with collaborative filtering to enhance recommendation accuracy.
BERT4Rec [34]: this model employs the Bidirectional Encoder Representations from Transformers (BERT) architecture, specifically designed for sequential recommendation. It captures complex item interaction patterns and user preferences from sequential data. We used the BERT-base-uncased model.

## Evaluation Metrics

To assess the performance of our model against the baselines, we employed several key metrics:

Precision@K measures the proportion of relevant articles in the top-K recommendations, reflecting accuracy.
Recall@K indicates the fraction of relevant articles captured in the top-K recommendations, highlighting the model’s retrieval ability.
Normalized Discounted Cumulative Gain (NDCG)@K assesses ranking quality, prioritizing the placement of relevant articles higher in the recommendation list.
Gini Index evaluates the fairness of recommendation distribution, with lower values indicating more equitable distribution across items.
We consider the value of top@ k as 5 (k = 5) following standard works in recommender systems theory [16].

## Settings and Hyerparameters

We temporally split the datasets into training, validation, and testing sets with a ratio of 80:10:10. The hyperparameters of the models were tuned on the validation set. All experiments were conducted on a machine with an Intel Xeon processor, 32GB RAM, and an Nvidia GeForce GTX 1080 Ti GPU. The set of hyperparameters is given in Table 2.

In our C-DBRRS, various hyperparameters are carefully tuned for optimal performance, as shown in Table 2. Hyperparameters 𝛼,𝛽,𝛾 are crucial for weighting different components of the loss function, controlling how the model balances prediction accuracy, item bias, and exposure bias, respectively. In particular, 𝜆 serves as a key parameter for overall balancing between relevance and fairness in the recommendation output, in line with the system’s optimization objective.

## Overall Results

Table 3 illustrates the performance of various recommendation methods on the MIND-small and Outbrain datasets, respectively, including our proposed C-DBRRS and the state-of-the-art models. The performances reported are averaged over five runs to ensure statistical reliability, with the standard deviation included to indicate performance variability.

The Table 3 compares the performance of different recommendation methods on two datasets, MIND-small and Outbrain, using metrics such as Precision@5, Recall@5, NDCG@5, and the Gini Index. In both datasets, the C-DBRRS method demonstrates higher performance, achieving the highest scores in Precision@5, Recall@5, and NDCG@5, alongside the lowest Gini Index. In this study, we value a lower GINI index as it indicates a desirable level of diversity in recommendations. However, we aim to achieve this without resorting to entirely random recommendations. Our goal is to strike a balance between diversity and relevance, ensuring that the recommendations are diverse yet still meaningful and aligned with user interests.
Other methods like POP, CB, CF, MF, NCF, and BERT4Rec show lower performance compared to C-DBRRS. The improvement in performance metrics from simpler methods like POP to more advanced ones like C-DBRRS highlights the efficacy of sophisticated recommendation systems. Particularly, the lower Gini Index in methods like C-DBRRS highlights their capability in ensuring a more equitable distribution of recommendations (not too highly diverse).
Overall, these results suggest a clear advantage of advanced methods like C-DBRRS in enhancing both the accuracy and fairness of recommendations in News Recommendation Systems. Because of the comparable patterns found in both datasets and the superior performance of our model on the MIND dataset, we will present the results of our subsequent experiments using the MIND dataset.

## Recommendation Distribution across Different News Categories

To assess the fairness of the C-DBRRS’s recommendation distribution across different news categories on the MIND dataset, we employed the Gini coefficient as a measure of inequality—a Gini coefficient of 0 expresses perfect equality, and a Gini coefficient of 1 implies maximal inequality among values. We first calculated the Gini coefficients for each category in the baseline model, where no fairness constraints were applied. Subsequently, we integrated the fairness constraints into the C-DBRRS model and recalculated the Gini coefficients.
As evident from Table 4, all categories exhibit a significant reduction in the Gini coefficient, indicating a more equitable distribution of news recommendations. Specifically, the ‘Environment’ category showed the most considerable improvement, with a Gini coefficient reduction from 0.65 to 0.30, followed by the ‘Arts’ category, which reduced from 0.60 to 0.28. The ‘Politics’ and ‘Sports’ categories also observed notable improvements. The reduction in the Gini coefficients across all news categories indicates that the C-DBRRS model successfully addresses the challenges of item bias and exposure bias, leading to a more equitable and diverse set of recommendations.

## Analysis of Relevance and Fairness Trade-Off

The results presented in Figure 2 illustrate the trade-off between relevance and fairness for the C-DBRRS model. Specifically, as the value of 𝜆 increases from 0 to 1, the model places more emphasis on fairness, leading to a decrease in relevance as measured by Precision@5, Recall@5, and NDCG@5. For example, when 𝜆 is 0 (meaning the model only considers relevance), the Precision@5, Recall@5, and NDCG@5 are highest However, when 𝜆 is increased to 1 (meaning the model only considers fairness), these values decreases. This indicates that there is a trade-off between achieving high relevance and high fairness, as improving fairness leads to a decrease in relevance.

The Gini Index, a measure of inequality, improves (decreases) as 𝜆 increases, indicating that the recommendations are becoming more fair. For example, when 𝜆 is 0, the Gini Index is 0.10, whereas it decreases to 0.18 when 𝜆 is 0.5 and increases further when 𝜆 is 1. This shows that the C-DBRRS model is effective at improving the fairness of the recommendations while maintaining a reasonable level of relevance. Researchers and practitioners using this model will need to carefully select the value of 𝜆 to balance the trade-off between relevance and fairness based on their specific application and requirements.

# Discussion

## Practical and Theoratical Impact

In this paper, we presented a novel approach optimized with a multi-objective function to balance the accuracy and diversity aspects of fairness. The C-DBRRS model, which forms the foundation of our approach, leverages the capability of LSTM networks to capture temporal patterns in users’ interactions with items, thereby providing more accurate and personalized recommendations. By predicting the next items a user is likely to interact with and ranking them based on their predicted interaction probabilities, our model can recommend the top-ranked items to the user.
Our multi-objective optimization goal is a key contribution to this work. This approach integrates multiple bias-related objectives, namely item bias and exposure bias, in addition to accuracy. By formulating this as a multi-objective optimization problem and minimizing the Gini coefficients of the distribution of recommended items and exposure, we encourage a more equal and unbiased distribution of recommendations and exposure.

## Limitations

Our approach has some limitations. First, the computational complexity of the model may be high due to the use of LSTM networks and the need to compute Gini coefficients for user–item interactions. This may limit the scalability of our approach to very large datasets. Second, the performance of our approach may be sensitive to the choice of hyperparameters, and determining the optimal values may require extensive grid search. Furthermore, our approach assumes that the temporal dynamics of user–item interactions are important for making recommendations. This assumption may not hold for all types of items or users. Moreover, whereas our focus is on finding biases, it is essential to acknowledge that fairness in recommendation systems is beyond diversity. Future studies should delve into nuanced facets of fairness, including equitable item representation and user recommendations.
Future work could explore alternative optimization algorithms, different types of recurrent neural networks, and the applicability of our approach to other types of recommendation problems.

## Recommender Systems Fairness in the Era of Large Language Models

The emergence of Large Language Models (LLMs) has brought a new dimension to the fairness of recommender systems. A recent survey [35] highlights the importance of integrating fairness-aware strategies in these systems, focusing on countering potential biases and promoting equality. LLMs, with their advanced deep learning architectures and extensive training on diverse datasets, excel in identifying and predicting a wide array of user preferences and behaviors. This capability is important in counteracting the ‘echo chamber’ effect prevalent in recommender systems by offering a varied range of content. Such diversity in content exposes users to a broader spectrum of topics and perspectives, thereby promoting a more balanced consumption of information, whereas personalization is essential for user satisfaction, LLMs in recommender systems can aptly balance it with the need for recommendation diversity.
However, the utilization of LLMs in recommender systems is accompanied by challenges. Ensuring user privacy, managing biased training data, and maintaining transparency in the recommendation processes are critical considerations. Additionally, there is an ethical imperative to avoid manipulative practices in these systems. LLMs, with their extensive knowledge and understanding, are adept at delivering recommendations that are not only precise but also encompass a wide spectrum of content.
The integration of LLMs into recommender systems necessitates the development of advanced strategies to accommodate diverse user preferences and diminish biases [36]. The need for fairness testing in these systems to ensure equitable recommendations is emphasized in related research [37]. Moreover, various evaluation approaches and assurance strategies are proposed to uphold fairness in recommender systems [38]. The significance of privacy-preserving mechanisms in LLM-based recommender systems is also required, underlining the interplay between fairness and privacy [39]. All these approaches should align with the broader goal of fairness in recommender systems, ensuring that users are presented with a balanced mix of familiar and novel content, thus avoiding the creation of echo chambers.

# Conclusions

In this paper, we presented the C-DBRRS that formulates the optimization goal as a multi-objective problem to encourage a more equal and unbiased distribution of recommendations and exposure. Our experiments on two real-world datasets demonstrated that our approach outperforms state-of-the-art methods in terms of accuracy, fairness, and balance. Additionally, recommendation distribution across different news categories confirmed the effectiveness of our approach in addressing item bias and exposure bias, leading to a more equitable and diverse set of recommendations. This is a crucial step towards developing more fair and responsible recommendation systems. Future work could explore alternative optimization algorithms, different types of recurrent neural networks, LLMs and the applicability of our approach to other types of recommendation problems. Additionally, it would be interesting to investigate the impact of our approach on user satisfaction and engagement in a real-world setting.

### Abbreviations

The following abbreviations are used in this manuscript:
NRS News Recommender Systems
LSTM Long Short-Term Memory
C-DBRRS Contextual Dual Bias Reduction Recommendation System
BERT Bidirectional Encoder Representations from Transformers
POP Popularity-Based Recommendation
CB Content-Based Recommendation
CF Collaborative Filtering
MF Matrix Factorization
NCF Neural Collaborative Filtering
NDCG Normalized Discounted Cumulative Gain
