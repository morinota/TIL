## 0.1. link

- https://arxiv.org/abs/2102.09268

## 0.2. titile

Training Large-Scale News Recommenders with Pretrained Language Models in the Loop

## 0.3. abstract

News recommendation calls for deep insights of news articles' underlying semantics. Therefore, pretrained language models (PLMs), like BERT and RoBERTa, may substantially contribute to the recommendation quality. However, it's extremely challenging to have news recommenders trained together with such big models: the learning of news recommenders requires intensive news encoding operations, whose cost is prohibitive if PLMs are used as the news encoder. In this paper, we propose a novel framework, {SpeedyFeed}, which efficiently trains PLMs-based news recommenders of superior quality. SpeedyFeed is highlighted for its light-weighted encoding pipeline, which gives rise to three major advantages. Firstly, it makes the intermedia results fully reusable for the training workflow, which removes most of the repetitive but redundant encoding operations. Secondly, it improves the data efficiency of the training workflow, where non-informative data can be eliminated from encoding. Thirdly, it further saves the cost by leveraging simplified news encoding and compact news representation. Extensive experiments show that SpeedyFeed leads to more than 100× acceleration of the training process, which enables big models to be trained efficiently and effectively over massive user data. The well-trained PLMs-based model from SpeedyFeed demonstrates highly competitive performance, where it outperforms the state-of-the-art news recommenders with significant margins. SpeedyFeed is also a model-agnostic framework, which is potentially applicable to a wide spectrum of content-based recommender systems; therefore, the whole framework is open-sourced to facilitate the progress in related areas.

# 1. Introduction

Online news platforms have been important media of information acquisition. Given the huge volumes of online news articles, personalized news feed [1], [2], [3] become imperative, with which users may get the news articles they feel interested in. The high-quality news recommendation is built upon the precise understanding of news articles’ underlying semantics. Therefore, the pretrained language models (PLMs), e.g., BERT and RoBERTa [4], [5], which achieve remarkable performances on general text understanding tasks, are desirable of being applied as the news encoder. However, the PLMs are not quite friendly to the end-to-end training of news recommenders. On the one hand, it is expensive to work with PLMs: the encoding speed will be relatively slow and the GPU RAM consumption will be huge given the considerable sizes of PLMs. On the other hand, the training of news recommenders requires intensive news encoding operations: to learn from every click signal of a user, the user’s entire historical news clicks need to be encoded, whose computation cost will be prohibitive if PLMs are utilized. As a result, the development of PLMsbased news recommenders is severely limited by the efficiency bottleneck.

To overcome the above challenge, a novel framework SpeedyFeed is proposed in this work, which trains PMLsbased news recommenders with high efficiency and high quality. SpeedyFeed is highlighted for its light-weighted encoding pipeline, which leads to the following advantages.

- The intermedia results are made highly reusable. Instead of having training instances encoded for one-shot use and discard afterwards, our framework saves the cost by making the following intermedia results fully reusable. Firstly, there are a small fraction of “breaking news articles”, which are highly popular and widely exist in the majority of users’ histories. Such news articles may frequently appear throughout the training process, and need to be re-encoded everytime. Knowing that the news recommenders are trained with small learning rates, usually in the magnitude of 1e−5 (especially when PLMs are fine-tuned), the same news article’s embedding will merely be slightly changed in every training step. As such, a caching mechanism is developed, which enables freshly generated news embeddings to be reused for multiple steps. Secondly, it is also wasteful of simply having user history encoded for the prediction of one single click signal. In our framework, the autoregressive user modeling is proposed, where an encoded prefix of user history can be reused for the calculation of all its subsequent user embeddings.
- The data efficiency is significantly improved. The typical training workflow is prone to poor data efficiency: given that the lengths of news articles and user histories are highly diversified, plenty of padded elements have to be introduced so that raw data can be batched as input tensors. The padded data is not only non-informative, but also severely slows down the training speed. In our framework, a centralized news encoding workflow is designed, which completely eliminates the padded data in user history. Besides, the data loader is designed to adaptively group the training instances, so that less padded data is needed for the news articles.
- The news encoding cost is reduced with well preserved encoding quality. The PLMs are limited by their quadratic encoding complexity, which makes the news encoding cost grow dramatically when the news article’s length becomes longer. In our framework, two techniques are utilized to mitigate this problem. Firstly, the bus language modeling (BusLM) is introduced for news encoding: on the one hand, it partitions each news article into small segments, which results in the linear reduction of encoding complexity; on the other hand, it establishes the bus connection between the segments, which makes them jointly encoded for a highquality news embedding. Secondly, the content refinement is performed for each news article before it is encoded by PLMs: the useful part of a news article is identified from the raw content, based on which the news article is transformed into a more compact representation.

It is worth noting that SpeedyFeed is not solely for training speedup. But because of the high training speed, it is now made feasible of training large-scale PLMs-based news recommenders over a huge amount of user data. The enlarged model scale, together with the enriched training data, ultimately make our recommender superior in generating high-quality news recommendation. SpeedyFeed is verified with the production data of Microsoft News, where it leads to more than 100× acceleration of the training speed, compared with its conventional workflow. Besides, our well trained PLMs-based recommender also demonstrates highly competitive performance, where it significantly outperforms the state-of-the-art approaches in comprehensive evaluations.

Finally, SpeedyFeed is a model-agnostic framework. In fact, it can be helpful to a wide variety of content-based recommender systems where user behaviors are associated with rich textual information, such as commodity and advertisement recommendation.

We summarize the major contributions of this work with the following points:

- We propose a novel framework SpeedyFeed to facilitate the training of large-scale PLMs-based news recommenders. With highly improved reusability, data efficiency and reduced news encoding complexity, our framework achieves significant acceleration for the training process.
- Our framework also fully preserves the PLMs’ expressiveness. The PLMs-based news recommender, trained via SpeedyFeed, significantly outperforms the stateof-the-art news recommendation baselines with even smaller training cost.
- We’ve made SpeedyFeed1 open to public, which can be adapted for a wide spectrum of content-based recommendation systems with rich textual information.

# 2. Related Works

In this section, we briefly review the related works from two perspectives: the deep news recommendation systems, and the pretrained language models.

## 2.1. Deep News Recommendation Systems

News recommendation systems are designed to identify users’ interested news articles with intensive exploitation of their historical news browsing behaviors [1], [3], [6]. As a result, two inherent problems need to be resolved within this process. One problem is the modeling of users’ behaviors. With the progress of deep learning based recommendation systems, plenty of techniques have been proposed for user modeling. In Youtube-DNN [7], users are represented as the averages of their interacted items’ embeddings; in GRU4Rec [8], users’ historical behaviors are aggregated with GRUs for sequential awareness; in DIN [9] and DEIN [10], users’ historical behaviors are attentively aggregated to establish candidate dependency; and in RUM [11], memory networks are utilized to capture the diversity about users’ behaviors. Such technical advancement also inspires the development of news recommenders. In DKN [12], users’ historical news clicks are attended by the candidate news for more precise modeling of user interest; and in LSTUR [13], recurrent neural networks are leveraged to capture users’ short-term interests.

The other problem, which is more specific to news recommendation, is the modeling of news content. In recent years, the prosperity of natural language processing pushes forward the progress of news modeling. For example, the hierarchical attention networks (HAN) [14], which was originally proposed for document classification, is adapted for the multi-view representation of news articles [15]; meanwhile, the Deep Attention Matching Networks (DAMN) [16], which was designed for response selection in chatbots, is applied to perform fine-grained matching between the news content and user history. The remarkable progress of the pretrained language models brings huge potentials for the further enhancement of news modeling. However, the efficiency issue becomes one of the major obstacles of applying PLMs for news recommendation: compared with the conventional small-scale text encoders, making use of PLMs in news recommenders is expensive in terms of both training time and computation resources. It usually requires the models to be trained on powerful GPU clusters, and still takes tremendously more running time. As a result, the research progress and real-world applications of PLMs-based news recommenders are comparatively limited for the current stage.

## 2.2. Pretrained Language Models

The pretrained language models are proposed to learn universal representation/generation models with neural networks trained on large-scale corpus. The early works were started with some shallow structures, e.g, Skip-Gram [17] and GloVe [18]; in recent years, the network structures are being quickly scaled up: from EMLo [19], GPT [20], to BERT [5], RoBERTa [5], UniLM [21], till today’s GPT-3 [22]. The large-scale models, which get fully trained with massive corpus, demonstrate superior capabilities on general NLP tasks, e.g., semantic matching, question-answering, machine translation, and response generation.

The pretrained language models are also being intensively applied for the retrieval or information-filtering related scenarios [23], [24], [25]; e.g., in [26], PLMs are trained for knowledge retrieval, and in [27], PLMs are fine-tuned for advertisement keyword matching. In these scenarios, PLMs are required to represent a query and a keyword into their latent embeddings, where the query-keyword relationship can be reflected by their embedding similarity. Apparently, news recommenders turn out to be similar applications. However, the PLMs-based news recommenders can be relatively more expensive: to match a user towards a candidate news, it needs to encode all of the user’s historical news clicks with PLMs, which will lead to huge encoding costs.

# 3. Preliminaries

## 3.1. Typical Workflow of Training News Recommenders

The news recommender is to predict user’s future news preference given their news clicks in history. Therefore, a typical training workflow consists of three steps (shown on the left side of Figure 1), as implemented by Microsoft Recommenders [28].

- 1. Input Processing. The trainer needs to transfer the raw data, i.e., user’s historical interactions with news, into the required format, such that it can be loaded for training. Two operations are involved in this stage. On the one hand, the news articles are tokenized, and then padded/truncated into token sequences of a unified length. On the other hand, all users’ histories are padded/truncated into news sequences of a unified length.
- 2. News & User Encoding. The input tensors are encoded via two steps [1]. Firstly, the news encoding, which maps user’s historical news clicks and all of the candidate news into news embeddings. Secondly, the user encoding, which generates user embeddings based on the encoded historical news and other auxiliary features.
- 3. Learning from Prediction. Finally, the prediction is made about which candidate news is clicked given the user and news embeddings. The prediction loss (e.g., cross entropy or BPR) will be back-propagated for the model parameters’ update.

## 3.2. What’s wrong with the typical Workflow

One of the most notable things about training a news recommender is its huge text encoding cost: to make a prediction for one single user click, the trainer needs to encode 1) all of the news articles in user history and 2) the candidate news. Considering the large magnitudes of pretrained language models, the text encoding related computations will almost dominate the entire training cost. However, because of the following issues (shown in the middle of Figure 1), the typical training workflow becomes severely limited in efficiency, which makes it prohibitive to train a PLMs-based large-scale news recommender.

- High Encoding Cost. First of all, the PLMs are considerably larger in scale than the text encoders used in conventional text-related recommendations, e.g., bi-LSTM, CNN, and shallow transformers. What is worse, the PLMs are highly unfavorable to the processing of long texts. Particularly, the encoding cost is vulnerable to the length of input news (N), whose time complexity is O(N2 ), given that the mainstream PLMs are all based on transformer architectures [29]. Considering that many news articles require long textual descriptions to fully express their underlying information, it results in a huge computation overhead while encoding such news articles.
- Low Reusability. Secondly, the reusability is seldom emphasized before: every time a training instance is given, it is processed for the calculation of its own loss; once the loss is back-propagated, all related intermediate results, especially the news embeddings, will all be discarded after being used just one time. Considering that it is quite an expensive operation to encode a news article with PLMs, such a defect severely slows down the training progress.
- Low Data Efficiency. Lastly, due to the existence of substantial padded data (the padded elements in news article and user history), the meaningful computation throughput can be severely limited. Particularly, given that a token is the atomic data unit for both user tensor and candidate tensor, we define data efficiency as the ratio of valid (i.e.,non-padded) tokens within the input tensors:

$$
DE = \frac{|valid tokens|}{|\text{valid tokens}| + |\text{padded tokens}| \times 100}
\tag{1}
$$

Due to the highly diversified lengths of user histories and news articles, a huge amount of padded elements will probably be introduced. We empirically find that the data efficiency is usually lower than 50% in practice, which leads to a big waste of computation capacity and further jeopardizes the training efficiency.

# 4. Methodology

We develop an efficient training framework SpeedyFeed, which enables news recommenders built upon large-scale PLMs to be trained with both high speed and high quality. With SpeedyFeed, the news and user encoding are carried out through a light-weighted encoding pipeline, which is characterized by the following techniques: 1) the centralized news encoding for high data efficiency, 2) the cache acceleration and the autoregressive user modeling for high reusability, 3) the bus language modeling for economic encoding complexity (as the rightmost of Figure 1). Besides, two auxiliary techniques: content refinement and dynamic batching, are introduced, which give rise to a more compact representation of news content and further reduction of padded data, respectively.

## 4.1. Light-weighted Encoding Pipeline

Algorithm 1 presents the main logics of the light-weighted encoding pipeline. For each mini-batch, we apply centralized news encoding (Section 4.1.1) to gather all the involved news articles from both user tensor and news tensor into the merged set M. Then the lookup set M_L is sampled from the cached news embeddings M_C with the lookup rate pt, and the news articles within the lookup set directly use their cached embeddings, denoted by Θ_1. The news articles out of the lookup set are encoded with BusLM (Section 4.1.3), which gives Θ_2. The whole news embeddings Θ_1 ∪ Θ_2 are dispatched to their original positions (in either user history or candidate news); then, the cache is refreshed with the newly generated news embeddings Θ_2. Finally, the overall prediction loss is calculated with the autoregressive user modeling (Section 4.1.4), as in Eq. 5.

In the following sections, we elobrate the details of technical contributions in the light-weighted encoding pipeline.

### 4.1.1. Centralized News Encoding

The overall news encoding workflow is discussed in the first place. In the typical training workflow, the news encoder will directly work on the input tensors (i.e., user tensor, news tensor) for the news embeddings. During this process, the padded news articles are encoded together with the valid news, which results in low data efficiency.

Unlike the typical method, all of the news articles within a common mini-batch are jointly encoded in SpeedyFeed (as Figure 2). The centralized news encoding takes 3 steps: gathering, encoding and dispatching. Once a mini-batch is given, it gathers the news articles from all users and candidates into a merged set. The padded news and duplicated news are all removed. Then, the new embeddings are generated for all remaining news in the merged set. Finally, the news embeddings are dispatched to their original training instances. Note that the padded news articles also require their embeddings so as to infer the user embeddings; in this place, a dummy vector is plugged into the positions taken by the padded news, whereby no additional encoding cost is needed.

### 4.1.2. Cache-accelerated News Encoding

The cache mechanism is developed to fully reuse the intermedia news encoding results. Particularly, one notable observation about Microsoft News is its long-tail property of the news click distribution. As shown in Table 1, the top-1% popular news articles yield almost 60% of the overall news clicks. Therefore, such popular news articles may widely exist in the majority of users’ histories, making them frequently re-encoded across different training batches. Knowing that the model parameters are updated with a fairly small learning rate, usually in the magnitude of 1e^−5 , one news article’s recent embedding can be reused in the current mini-batch for approximation. Based on this intuition, we propose Cache-accelerated News Encoding, where a cache is maintained in memory for the storage of fresh news embeddings. The news encoding workflow is changed accordingly as Figure 3.

- News Encoding with Cache. For each news article in a mini-batch, the trainer will check the cache in the first place: if there is a copy of news embedding in cache, it will be directly reused without encoding; otherwise, the news article will be encoded from scratch.
- Cache Management Policy. The cache is managed with the following principles. Firstly, all of the embeddings in cache must be newly generated in the past few steps; otherwise, it will be incompatible with the current model. Secondly, the cache lookup should be dynamically scheduled: in the initial stage, the cached news embeddings should be used with a relatively low probability, because the step-wise change of model parameters is sharp; as the training goes on, the lookup rate should be gradually increased, because the change of model parameters becomes mild.

Based on the above principles, the cache management policy is made (as Figure 4), which is subject to two decisive variables: the stepwise lookup rate pt, and the expiration step γ. 1) An exponential scheduler is used to control the probability of whether to lookup the cache: the cache is looked up with probability 0 when the training gets started; the lookup probability will gradually grow to pt at the t-th step w.r.t. the following relationship:

$$
\tag{}
$$

β is the hyper parameter for growth rate, which lets pt grow to 1.0 after the initial stage of the training process. 2) A cached news embedding is expired after γ steps, and then it is removed from the cache.

Finally, instead of maintaining a private cache for each training thread, we establish a global cache in the master node. As a result, the newly generated news embeddings in one node can be shared across all devices, which accommodates the distributed training of news recommender. Besides, the cache is maintained in memory, instead of GPU RAM; therefore, it is almost free of cost, and the storage capacity can be large enough to host all needed embeddings.

Summary. We summarize the cache mechanism in Algorithm 2. In the training step t, we input a merged news set M by centralized news encoding. Firstly, the lookup probability pt is generated according to the current step t and hyper-parameter β (Lines 3). We use a random value to determine whether to read embeddings from the cache. If true, for all news embeddings in the cache, we only load the ones which are encoded less than γ training steps before the current step (Line 8). These loaded embeddings are denoted by Θ1, and the corresponding news are denoted by M_L. For news which are not cached, i.e., M \ M_L, we encode them into embeddings Θ2 with BusLM, which is introduced in the next subsetction, and write Θ2 into cache. Finally, Θ1 ∪ Θ2 is the whole new embeddings in step t.

### 4.1.3. Bus Language Modeling

We make further analysis of how we conduct news encoding in an economic way. The news encoding complexity is to the square of news length O(N2 ). A straightforward way of time reduction is to split the news into several subcomponents, e.g., the title, abstract, and body, as done in [15]; the text segments are processed independently, whose encoding results will be aggregated for the final news embedding. The operation may cut down the time complexity to O(N2/K), if the text can be partitioned into K “almost equal-length” segments. Yet, the naive split of text harms the news embedding quality, as the text segments cannot make reference to each other during the encoding process.

Inspired by recent progress on efficient transformers [30], we propose BusLM (Figure 5) to encode the news articles, where the acceleration is achieved with fully preserved embedding quality. In BusLM, the input news is uniformly partitioned into K text segments, such that the encoding complexity is reduced to O(N^2/K). The segments are still encoded by transformers; however, a layer-wise “bus connection” is established between the transformers, which enables information to be exchanged across the segments.

### 4.1.4. Autoregressive User Modeling

## 4.2. Further Enhancement

### 4.2.1. Content Refinement

### 4.2.2. Dynamic Batching

# 5. Experiment

## 5.1. Settings

### 5.1.1. Dataset description

### 5.1.2. SpeedyFeed Recommenders

### 5.1.3. Baselines

### 5.1.4. Evaluations

### 5.1.5. Training configurations

## 5.2. Experiment Analysis

### 5.2.1. Overall Performance

### 5.2.2. Further Analysis

# 6. Conclusion

# 7. Appendix

## 7.1. Appendix A

### 7.1.1. Bus Language Modeling

## 7.2. Appendix B

### 7.2.1. Details of Dataset

## 7.3. Appendix C

### 7.3.1. Details of Training Configurations
