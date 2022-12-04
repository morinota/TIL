### link

- https://dl.acm.org/doi/abs/10.1145/3097983.3098108?casa_token=E2V72vGAK60AAAAA:b1coQnhN8zeSe6KNZrv_2T3HC5NfMI5LtYH7Mrj9ckNTblQQuiP9FEvoPtpGYnIN5hbNA7zEwefO6qvo

### title

Embedding-based News Recommendation for Millions of Users

### ABSTRACT

It is necessary to understand the content of articles and user preferences to make effective news recommendations. While ID-based methods, such as collaborative filtering and low-rank factorization, are well known for making recommendations, they are not suitable for news recommendations because candidate articles expire quickly and are replaced with new ones within short spans of time. Word-based methods, which are often used in information retrieval settings, are good candidates in terms of system performance but have issues such as their ability to cope with synonyms and orthographical variants and define "queries" from users' historical activities. This paper proposes an embedding-based method to use distributed representations in a three step end-to-end manner: (i) start with distributed representations of articles based on a variant of a denoising autoencoder, (ii) generate user representations by using a recurrent neural network (RNN) with browsing histories as input sequences, and (iii) match and list articles for users based on inner-product operations by taking system performance into consideration. The proposed method performed well in an experimental offline evaluation using past access data on Yahoo! JAPAN's homepage. We implemented it on our actual news distribution system based on these experimental results and compared its online performance with a method that was conventionally incorporated into the system. As a result, the click-through rate (CTR) improved by 23% and the total duration improved by 10%, compared with the conventionally incorporated method. Services that incorporated the method we propose are already open to all users and provide recommendations to over ten million individual users per day who make billions of accesses per month.

## INTRODUCTION

It is impossible for users of news distributions to read all available articles due to limited amounts of time. Thus, users prefer news services that can selectively provide articles. Such selection is typically done manually by editors and a common set of selected stories are provided to all users in outmoded media such as television news programs and newspapers. However, we can identify users before they select articles that will be provided to them on the Internet by using information, such as that in user ID cookies, and personalize the articles for individual users [3, 22].

ID-based methods, such as collaborative filtering and low-rank factorization, are well known in making recommendations. However, Zhong et al. [22] suggested that such methods were not suitable for news recommendations because candidate articles expired too quickly and were replaced with new ones within short time spans. Thus, the three keys in news recommendations are: Understanding the content of articles, • Understanding user preferences, and • Listing selected articles for individual users based on content and preferences.

In addition, it is important to make recommendations in the real world [14] that respond to scalability and noise in learning data [14]. Applications also need to return responses within hundreds of milliseconds with every user access.

A baseline implementation to cover the three keys would be as follows. An article is regarded as a collection of words included in its text. A user is regarded as a collection of words included in articles he/she has browsed. The implementation learns click probability using co-occurrence of words between candidates of articles and browsing histories as features.

This method has some practical advantages. It can immediately reflect the latest trends because the model is very simple so that the model can be taught to learn and update in short periods of time. The estimation of priority can be quickly calculated using existing search engines with inverted indices on words.

The previous version of our implementation was based on this method for these reasons. However, it had some issues that may have had a negative impact on the quality of recommendations. The first regarded the representation of words. When a word was used as a feature, two words that had the same meaning were treated as completely different features if the notations were different. This problem tended to emerge in news articles when multiple providers separately submitted articles on the same event. The second regarded the handling of browsing histories. Browsing histories were handled as a set in this approach. However, they were actually a sequence, and the order of browsing should have represented the transition of user interests. We also had to note large variances in history lengths by users that ranged from private browsing to those who visited sites multiple times per hour. Deep-learning-based approaches have recently been reported to be effective in various domains. Distributed representations of words thoroughly capture semantic information [11, 16]. Recurrent neural networks (RNNs) have provided effective results as a method of handling input sequences of variable length [9, 15, 17].

If we build a model with a deep network using an RNN to estimate the degree of interest between users and articles, on the other hand, it is difficult to satisfy the response time constraints on accesses in real systems. This paper proposes an embedding-based method of using distributed representations in a three step endto-end manner from representing each article to listing articles for each user based on relevance and duplication: Start with distributed representations of articles based on a variant of the denoising autoencoder (which addresses the first issue in Section 3). • Generate user representations by using an RNN with browsing histories as input sequences (which addresses the second issue in Section 4). • Match and list articles for each user based on the inner product of article-user for relevance and article-article for de-duplication (outlined in Section 2).

The key to our method is using a simple inner product to estimate article-user relevance. We can calculate article representations and user representations before user visits in sufficient amounts of time. When a user accesses our service, we only select his/her representations and calculate the inner product of candidate articles and the representations. Our method therefore both expresses complex relations that are included in the user’s browsing history and satisfies the response time constraints of the real system.

The proposed method was applied to our news distribution service for smartphones, which is described in the next section. We compared our method to a conventional approach, and the results (see Section 6) revealed that the proposed method outperformed the conventional approach with a real service as well as with static experimental data, even if disadvantages, such as increased learning time and large latency in model updates, are taken into consideration.

## OUR SERVICE AND PROCESS FLOW

The methods discussed in this paper were designed to be applied to the news distribution service on the homepage of Yahoo! JAPAN on smartphones. The online experiments described in Section 6 were also conducted on this page. This section introduces our service and process flow.

<img src="https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/2-Figure1-1.png">

Figure 1: Example of Yahoo! JAPAN’s homepage on smartphones. This paper discusses methods of providing articles in Personalized module.

Figure 1 has a mockup of our service that was renewed in May 2015. There is a search window and links to other services at the top as a header. The middle part, called the Topics module, provides six articles on major news selected by human professionals for a general readership. The bottom part, called the Personalized module, provides many articles and advertising that has been personalized for individual users. Users in the Personalized module can see as many articles as they want if they scroll down to the bottom. Typical users scroll down to browse the approximately top 20 articles. This paper describes optimization to provide articles in the Personalized module

Five processes are executed to select articles for millions of users for each user access.Identify: Obtain user features calculated from user history in advance. • Matching: Extract articles from all those available using user features. • Ranking: Rearrange list of articles on certain priorities. • De-duplication: Remove articles that contain the same information as others. • Advertising: Insert ads if necessary.

These processes have to be done within hundreds of milliseconds between user requests and when they are displayed because available articles are constantly changing. In fact, as all articles in our service expire within 24 hours from the viewpoint of information freshness, tens of thousands of new articles are posted every day, and the same number of old articles are removed due to expiration. Thus, each process adopts computationally light methods that leverage pre-computed distributed article representations (described in Section 3) and user representations (described in Section 4).

We use the inner product of distributed representations of a user and candidate articles in matching to quantify relevance and select promising candidates. We determine the order of priorities in ranking by considering additional factors, such as the expected number of page views and freshness of each article, in addition to the relevance used for matching. We skip similar articles in a greedy manner in de-duplication based on the cosine similarity of distributed representations. An article is skipped when the maximum value of its cosine similarity with articles with higher priorities is above a threshold. This is an important process in real news distribution services because similar articles tend to have similar scores in ranking. If similar articles are displayed close to one another, a real concern is that user satisfaction will decrease due to reduced diversity on the display. Details on comparison experiments in this process have been discussed in a report on our previous study [12]. Advertising is also important, but several studies [2, 10] have already reported on the relationship between advertising and user satisfaction, so such discussion has been omitted here.

## ARTICLE REPRESENTATIONS

Section 1 discussed a method of using words as features for an article that did not work well in certain cases of extracting and de-duplicating. This section describes a method of dealing with articles as a distributed representation. We proposed a method in our previous study [12], from which part of this section has been excerpted.

### Generating Method

Our method generates distributed representation vectors on the basis of a denoising autoencoder [19] with weak supervision. The conventional denoising autoencoder is formulated as:

$$
\tilde{x} \sim q(\tilde{x}|x) \\
h = f(W\tilde{x} + b) \\
y =f(W'h + b') \\
\theta = \argmin_{W, W', b, b'} \sum_{x \in X} L_R(y, x)
$$

where $x \in X$ is the original input vector and $q(·|·)$ is the corrupting distribution. The stochastically corrupted vector, $\tilde{x}$, is obtained from $q(·|x)$. The hidden representation, h, is mapped from $\tilde{x}$ through the network, which consists of an activation function, $f(·)$, parameter matrix W , and parameter vector b. In the same way, the reconstructed vector, y, is also mapped from h with parameters $W'$ and $b'$ . Using a loss function, $L_{R}(·, ·)$, we learn these parameters to minimize the reconstruction errors of y and x.

The h is usually used as a representation vector that corresponds to x. However, h only holds the information of x. We want to interpret that the inner product of two representation vectors $h_0^T h_1$ is larger if $x_0$ is more similar to $x_1$. To achieve that end, we use a triplet, $(x_0, x_1, x_2) \in X^3$ , as input for training and modify the objective function to preserve their categorical similarity as:

$$
\tilde{x}_n \sim q(\tilde{x}_n|x_n) \\
h_n = f(W\tilde{x}_n + b) - f(b) \\
y_n = f(W'h_n + b')
L_T(h_0, h_1, h_2) = \log (1+ \exp(h_0^T h_2 - h_0^T h_1)) \\
\theta = \argmin_{W,W',b, b'} \sum_{x_0,x_1,x_2 \in T}
\sum_{n=0}^2 L_R(y_n,x_n) + \alpha L_T(h_0, h_1, h_2) \\
\tag{1}
$$

where $T \subset X^3$ , such that $x_0$ and $x_1$ are in the same category/similar categories and $x_0$ and $x_2$ are in different categories. The h in Eq.1 satisfies the property, $x = 0 ⇒ h = 0$. This means that an article that has no available information is not similar to any other article. The notation, $L_T (·, ·, ·)$ is a penalty function for article similarity to correspond to categorical similarity, and α is a hyperparameter for balancing. Figure 2 provides an overview of this method.

<img src="https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/3-Figure2-1.png">

We use the elementwise sigmoid function, $\sigma(x)_i = 1/(1+exp(-x_i))$, as $f(·)$, elementwise cross entropy as $L_R(·, ·)$, and masking noise as $q(·|·)$. We train the model, $\theta = {W ,W′, b, b′}$, by using mini-batch stochastic gradient descent (SGD).

We construct x˜ in the application phase by using constant decay, instead of stochastic corruption in the training phase, as:

$$
\tilde{x} = (1-p)x \\
h = f(W\tilde{x} + b) - f(b)
$$

where $p$ is the corruption rate in the training phase. Thus, $h$ is uniquely determined at the time of application. Multiplying $1 − p$ has the effect of equalizing the input distribution to each neuron in the middle layer between learning with masking noise and that without the application of this noise.

We use the $h$ generated above in three applications as the representation of the article: (i) to input the user-state function described in Section 4, (ii) to measure the relevance of the user and the article in matching, and (iii) to measure the similarity between articles in de-duplication.

## USER REPRESENTATIONS

This section describes several variations of the method to calculate user preferences from the browsing history of the user. First, we formulate our problem and a simple word-based baseline method and discuss the issues that they have. We then describe some methods of using distributed representations of articles, as was explained in the previous section.

### Notation

Let $A$ be the entire set of articles. Representation of element $a \in A$ depends on the method. The $a$ is a sparse vector in the word-based method described in Section 4.2, and each element of a vector corresponds to each word in the vocabulary (i.e., $x$ in Section 3). However, $a$ is a distributed representation vector of the article (i.e., $h$ in Section 3) in the method using distributed representations described in Sections 4.3 and 4.4.

Browse means that the user visits the uniform resource locator (URL) of the page of an article. Let ${_t^u \in A}_{t=1,\cdots,T_u}$ be the browsing history of user $u \in U$.

Session means that the user visits our recommendation service and clicks one of the articles in the recommended list.

When $u$ clicks an article in our recommendation service (a session occurs), he/she will immediately visit the URL of the clicked article (a browse occurs). Thus, there is never more than one session between browses $a_t^u$ and $a^u_{t+1}$ ; therefore, this session is referred to as $s_t^u$ . However, $u$ can visit the URL of an article without our service, e.g., by using a Web search. Therefore, $s_t^u$ does not always exist.

Since a session corresponds to the list presented to $u$, we express a session, $s^u_t$, by a list of articles ${s^u_{t,p} \in A}_{p \in P}$. The notation, $P \subseteq N$, is the set of positions of the recommended list that is actually displayed on the screen in this session. Let $P_{+} \subseteq P$ be the clicked positions and $P_{-} = P \ P_{+}$ be non-clicked positions. Although $P$, $P_{+}$, and $P_{-}$ depend on $u$ and $t$, we omit these subscripts to simplify the notation. Figure 3 outlines the relationships between these notations.

<img src="https://d3i71xaburhd42.cloudfront.net/376953b2d70b30cfa9d56ae841b8c16f059e0867/4-Figure3-1.png">

Figure 3: Browsing history and session

Let $u_t$ be the user state depending on $a_1^u , \cdots, a_t^u$, i.e., $u_t$ represents the preference of $u$ immediately after browsing $a_t^u$. Let $R(u_t, a)$ be the relevance between the user state, $u_t$, and the article, $a$, which represents the strength of $u$’s interest in a in time t. Our main objective is to constitute user-state function $F(·, . . . , ·)$ and relevance function $R(·, ·)$ that satisfy the property:

$$
u_t = F(a_1^u, \cdots, a_t^u) \\
\forall{s_t^u} \forall{p_{+}} \in P_{+} \forall{p_{-}} 
\in P_{-} R(u_t, s_{t,p_{+}}^u) > R(u_t, s_{t, p_{-}}^u). \\
\tag{2}
$$

($\forall$は"任意の、全称記号"を表す論理記号。全称量化子とも呼ばれる。)

When considering the constrained response time of a real news distribution system with large traffic volumes, $R(·, ·)$ must be a simple function that can be quickly calculated. Because candidate articles are frequently replaced, it is impossible to pre-calculate the relevance score, $R(u_t, a)$, for all users ${u_t |u \in U }$ and all articles ${a \in A}$. Thus, it is necessary to calculate this in a very short time until the recommended list from visiting our service page is displayed. However, we have sufficient time to calculate the user state function, $F (·, \cdots, ·)$, until the next session occurs from browsing some article pages.

