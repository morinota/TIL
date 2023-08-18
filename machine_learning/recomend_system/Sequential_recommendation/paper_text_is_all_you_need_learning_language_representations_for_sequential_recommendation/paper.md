## link

https://arxiv.org/abs/2305.13731

## title

Text Is All You Need: Learning Language Representations for Sequential Recommendation

## abstract

Sequential recommendation aims to model dynamic user behavior from historical interactions. Existing methods rely on either explicit item IDs or general textual features for sequence modeling to understand user preferences. While promising, these approaches still struggle to model cold-start items or transfer knowledge to new datasets. In this paper, we propose to model user preferences and item features as language representations that can be generalized to new items and datasets. To this end, we present a novel framework, named Recformer, which effectively learns language representations for sequential recommendation. Specifically, we propose to formulate an item as a "sentence" (word sequence) by flattening item key-value attributes described by text so that an item sequence for a user becomes a sequence of sentences. For recommendation, Recformer is trained to understand the "sentence" sequence and retrieve the next "sentence". To encode item sequences, we design a bi-directional Transformer similar to the model Longformer but with different embedding layers for sequential recommendation. For effective representation learning, we propose novel pretraining and finetuning methods which combine language understanding and recommendation tasks. Therefore, Recformer can effectively recommend the next item based on language representations. Extensive experiments conducted on six datasets demonstrate the effectiveness of Recformer for sequential recommendation, especially in low-resource and cold-start settings.

# Introduction

Sequential recommender systems model historical user interactions as temporally-ordered sequences to recommend potential items that users are interested in. Sequential recommenders [11, 14, 25, 27] can capture both short-term and long-term preferences of users and hence are widely used in different recommendation scenarios. Various methods have been proposed to improve the performance of sequential recommendation, including Markov Chains [9, 25], RNN/CNN models [11, 17, 28, 34] and self-attentive models [14, 19, 27]. Traditional sequential recommendation models convert items into IDs and create item embedding tables for encoding. Item embeddings are learned from sequences of user interactions. To enrich item features, some approaches [4, 20, 37, 38] incorporate item contexts such as item textual information or categorical features into ID embeddings. While ID-based methods are promising, they struggle to understand cold-start items or conduct cross-domain recommendations where models are trained and then applied to different recommendation scenarios. Item-specific IDs prevent models from learning transferable knowledge from training data for cold-start items and new datasets. As a result, item IDs limit the performance of sequential recommenders on cold-start items and we have to re-train a sequential recommender for continually added new items. Therefore, transferable recommenders can benefit both cold-start items and new-domain datasets. To develop transferable recommender systems, previous studies usually assume shared information such as overlapping users/items [13, 26, 39] and common features [29] is available and then reduce the gap between source and target domains by learning either semantic mappings [39] or transferable components [16]. Such assumptions are rarely true in real applications because items in different domains (e.g., Laptops and T-shirts) usually contain different features for recommendation. Therefore, to have effective cross-domain transfer, recent works [7, 12] leverage the generality of natural language texts (e.g., titles, descriptions of items) for common knowledge in different domains. The basic idea is to employ pre-trained language models such as BERT [6] to obtain text representations and then learn the transformation from text representations to item representations. The knowledge of the transformation can be transferred across different domains and shows promising performance. However, such frameworks of learning transformation from language to items have several limitations: (1) Pre-trained language models are usually trained on a general language corpus (e.g., Wikipedia) serving natural language tasks that have a different language domain from item texts (e.g., concatenation of item attributes), hence text representations from pretrained language models for items are usually sub-optimal. (2) Text representations from pre-trained language models are not able to learn the importance of different item attributes and only provide coarse-grained (sentence-level) textual features but cannot learn fine-grained (word-level) user preferences for recommendations (e.g., find the same color in recent interactions for clothing recommendations). (3) Due to the independent training of pre-trained language models (by language understanding tasks, e.g., Masked Language Modeling) and transformation models (by recommendation tasks, e.g., next item prediction), the potential ability of models to understand language for recommendations has not been fully developed (by joint training). With the above limitations in mind, we aim to unify the frameworks of natural language understanding and recommendations in an ID-free sequential recommendation paradigm. The pre-trained language models [6, 15, 23, 24] benefit various downstream natural language processing tasks due to their transferable knowledge from pre-training. The basic idea of this paper is to use the generality of language models through joint training of language understanding and sequential recommendations. To this end, there are three major challenges to be solved. First, previous text-based methods [7, 12] usually have their specific item texts (e.g., item descriptions, concatenation of item attributes). Instead of specific data types, we need to find a universal input data format of items for language models that is flexible enough to different kinds of textual item information. Second, it is not clear how to model languages and sequential transitions of items in one framework. Existing language models are not able to incorporate sequential patterns of items and cannot learn the alignment between items and item texts. Third, a training and inference framework is necessary to bridge the gap between natural languages and recommendations like how to efficiently rank items based on language models without trained item embeddings. To address the above problems, we propose Recformer, a framework that can learn language representations for sequential recommendation. Overall, our approach takes a text sequence of historical items as input and predicts the next item based on language understanding. Specifically, as shown in Figure 1, we first formulate an item as key-value attribute pairs which can include any textual information such as the title, color, brand of an item. Different items can include different attributes as item texts. Then, to encode a sequence of key-value attribute pairs, we propose a novel bi-directional Transformer [30] based on Longformer structure [2] but with different embeddings for item texts to learn item sequential patterns. Finally, to effectively learn language representations for recommendation, we design the learning framework for the model including pre-training, finetuning and inference processes. Based on the above methods, Recformer can effectively recommend the next items based on item text representations. Furthermore, the knowledge learned from training can be transferred to cold-start items or a new recommendation scenario.

To evaluate Recformer, we conduct extensive experiments on real-world datasets from different domains. Experimental results show that our method can achieve 15.83% and 39.78% (NDCG@10) performance improvements under fully-supervised and zero-shot sequential recommendation settings respectively.1 Our contributions in this paper can be summarized as follows:

- We formulate items as key-value attribute pairs for the IDfree sequential recommendation and propose a novel bidirectional Transformer structure to encode sequences of key-value pairs.
- We design the learning framework that helps the model learn users’ preferences and then recommend items based on language representations and transfer knowledge into different recommendation domains and cold-start items.
- Extensive experiments are conducted to show the effectiveness of our method. Results show that Recformer outperforms baselines for sequential recommendation and largely improves knowledge transfer as shown by zero-shot and cold-start settings.

# Methodology

In this section, we present Recformer which can learn language representations for sequential recommendation and effectively transfer and generalize to new recommendation scenarios.

## Problem Setup and Formulation

In the setting of sequential recommendation, we are given an item set I and a user’s interaction sequence 𝑠 = {𝑖1,𝑖2, . . . ,𝑖𝑛} in temporal order where 𝑛 is the length of𝑠 and 𝑖 ∈ I. Based on 𝑠, we seek to predict the next item. In previous sequential recommendation methods, each interacted item𝑖 is associated with a unique item ID. In this paper, each item 𝑖 has a corresponding attribute dictionary 𝐷𝑖 containing key-value attribute pairs {(𝑘1, 𝑣1), (𝑘2, 𝑣2), . . . , (𝑘𝑚, 𝑣𝑚)} where 𝑘 denotes an attribute name (e.g., Color) and 𝑣 is the corresponding value (e.g., Black). 𝑘 and 𝑣 are both described by natural languages and contain words (𝑘, 𝑣) = {𝑤 𝑘 1 , . . . ,𝑤𝑘 𝑐 ,𝑤𝑣 1 , . . . ,𝑤𝑣 𝑐 }, where 𝑤 𝑘 and 𝑤 𝑣 are words of 𝑘 and 𝑣 from a shared vocabulary in the language model and 𝑐 denotes the truncated length of text. An attribute dictionary 𝐷𝑖 can include all kinds of item textual information such as titles, descriptions, colors, etc. As shown in Figure 2, to feed the attribute dictionary 𝐷𝑖 into a language model, we flatten key-value attribute pairs into 𝑇𝑖 = {𝑘1, 𝑣1, 𝑘2, 𝑣2, . . . , 𝑘𝑚, 𝑣𝑚} to obtain an item “sentence” as the input data. Unlike previous sequential recommenders [12, 37] using both text and item IDs, in this study, we use only text for the sequential recommendation.

## Recformer

Figure 3 (a) shows the architecture of Recformer. The model has a similar structure as Longformer [2] which adopts a multi-layer bidirectional Transformer [30] with an attention mechanism that scales linearly with sequence length. We consider only computing efficiency for using Longformer but our method is open to other bidirectional Transformer structures such as BERT [6] and BigBird [36].

### Model Inputs.

As introduced in Section 2.1, for each item 𝑖 and corresponding attribute dictionary 𝐷𝑖 , we flatten the dictionary into an item “sentence”𝑇𝑖 = {𝑘1, 𝑣1, 𝑘2, 𝑣2, . . . , 𝑘𝑚, 𝑣𝑚} where 𝑘 and 𝑣 are described by words, formally (𝑘, 𝑣) = {𝑤 𝑘 1 , . . . ,𝑤𝑘 𝑐 ,𝑤𝑣 1 , . . . ,𝑤𝑣 𝑐 }. To encode a user’s interaction sequence 𝑠 = {𝑖1,𝑖2, . . . ,𝑖𝑛}, we first reverse items in a sequence to {𝑖𝑛,𝑖𝑛−1, . . . ,𝑖1} because intuitively recent items (i.e., 𝑖𝑛,𝑖𝑛−1, . . . ) are important for the next item prediction and reversed sequences can make sure recent items are included in the input data. Then, we use the item “sentences” to replace items and add a special token [CLS] at the beginning of sequences. Hence, model inputs are denoted as:

$$
\tag{1}
$$

where 𝑋 is a sequence of words containing all items and corresponding attributes the user interacted with in the historical interactions.

### Embedding Layer.

The target of Recformer is to understand the model input 𝑋 from both language understanding and sequential patterns in recommendations. The key idea in our work is to combine the embedding layers from language models [6, 21] and self-attentive sequential recommenders [14, 27]. Hence, Recformer contains four embeddings as follows:

- Token embedding represents the corresponding tokens. We denote the word token embedding by A ∈ R 𝑉𝑤 ×𝑑 , where 𝑉𝑤 is the number of words in our vocabulary and 𝑑 is the embedding dimension. Recformer does not have item embeddings as previous sequential recommenders and hence Recformer understands items in interaction sequences mainly based on these token embeddings. The size of token embeddings is a constant for different recommendation scenarios; hence, our model size is irrelevant to the number of items.
- Token position embedding represents the position of tokens in a sequence. A word appearing at the 𝑖-th position in the sequence 𝑋 is represented as B𝑖 ∈ R 𝑑 . Similar to language models, token position embedding is designed to help Transformer understand the sequential patterns of words.
- Token type embedding represents where a token comes from. Specifically, the token type embedding totally contains three vectors C[CLS], CKey, CValue ∈ R 𝑑 to represent if a token comes from [CLS], attribute keys, or attribute values respectively. Different types of tokens usually have different importance for the next item prediction. For example, because most items usually have the same attribute keys in a recommendation dataset, models with token type embedding will recognize repeated words from the same attribute keys.
- Item position embedding represents the position of items in a sequence. A word from attributes of the 𝑘-th item in the sequence 𝑋 is represented as D𝑘 ∈ R 𝑑 and D ∈ R 𝑛×𝑑 where 𝑛 is the maximum length of a user’s interaction sequence 𝑠. Same as previous self-attentive sequential recommenders [14, 27], the item position embedding is a key component for item sequential pattern learning. In Recformer, the item position embedding can also help the model learn the alignment between word tokens and items

Therefore, given a word 𝑤 from the input sequence 𝑋, the input embedding is calculated as the summation of four different embeddings followed by layer normalization [1]:

$$
\tag{2}
$$

where E𝑤 ∈ R 𝑑 . The embedding of model inputs 𝑋 is a sequence of E𝑤,

$$
\tag{3}
$$

where E𝑋 ∈ R (𝑙+1)×𝑑 and 𝑙 is the maximum length of tokens in a user’s interaction sequence.

### Item or Sequence Representations.

To encode E𝑋 , we employ the bidirectional Transformer structure Longformer [2] as our encoder. Because 𝑋 is usually a long sequence, the local windowed attention in Longformer can help us efficiently encode E𝑋 . As the standard settings in Longformer for document understanding, the special token [CLS] has global attention but other tokens use the local windowed attention. Hence, Recformer computes 𝑑-dimensional word representations as follows:

$$
\tag{4}
$$

where h𝑤 ∈ R 𝑑 . Similar to the language models used for sentence representations, the representation of the first token h[CLS] is used as the sequence representation. In Recformer, we do not maintain an embedding table for items. Instead, we view the item as a special case of the interaction sequence with only one item. For each item 𝑖, we construct its item “sentence” 𝑇𝑖 and use 𝑋 = {[CLS],𝑇𝑖 } as the model input to get the sequence representation h[CLS] as the item representation h𝑖 .

### Prediction.

We predict the next item based on the cosine similarity between a user’s interaction sequence 𝑠 and item 𝑖. Formally, after obtaining the sequence representation h𝑠 and the item representation h𝑖 as introduced in Section 2.2.3, we calculate the scores between 𝑠 and 𝑖 as follows:

$$
\tag{5}
$$

where 𝑟𝑖,𝑠 ∈ R is the relevance of item 𝑖 being the next item given 𝑠. To predict the next item, we calculate 𝑟𝑖,𝑠 for all items 2 in the item set I and select item with the highest 𝑟𝑖,𝑠 as the next item:

$$
\tag{6}
$$

where ˆ𝑖𝑠 is the predicted item given user interaction sequence 𝑠.

## Learning Framework

To have an effective and efficient language model for the sequential recommendation, we propose our learning framework for Recformer including pre-training and two-stage finetuning.

### Pre-training.

The target of pre-training is to obtain a highquality parameter initialization for downstream tasks. Different from previous sequential recommendation pre-training methods which consider only recommendations, we need to consider both language understanding and recommendations. Hence, to pre-train Recformer, we adopt two tasks: (1) Masked Language Modeling (MLM) and (2) an item-item contrastive task. Masked Language Modeling (MLM) [6] is an effective pre-training method for language understanding and has been widely used for various NLP pre-training tasks such as sentence understanding [8], phrase understanding [18]. Adding MLM as an auxiliary task will prevent language models from forgetting the word semantics when models are jointly trained with other specific tasks. For recommendation tasks, MLM can also eliminate the language domain gap between a general language corpus and item texts. In particular, following BERT [6], the training data generator chooses 15% of the token positions at random for prediction. If the token is selected, we replace the token with (1) the [MASK] with probability 80%; (2) a random token with probability 10%; (3) the unchanged token with probability 10%. The MLM loss is calculated as:

$$
\tag{7}
$$

$$
\tag{8}
$$

$$
\tag{9}
$$

where Wℎ ∈ R 𝑑×𝑑 , bℎ ∈ R 𝑑 , W0 ∈ R |V |×𝑑 , b0 ∈ R |V | , GELU is the GELU activation function [10] and V is the vocabulary used in the language model.

Another pre-training task for Recformer is the item-item contrastive (IIC) task which is widely used in the next item prediction for recommendations. We use the ground-truth next items as positive instances following previous works [12, 14, 27]. However, for negative instances, we adopt in-batch next items as negative instances instead of negative sampling [14] or fully softmax [12, 27]. Previous recommenders maintain an item embedding table, hence they can easily retrieve item embeddings for training and update embeddings. In our case, item embeddings are from Recformer, so it is infeasible to re-encode items (from sampling or full set) per batch for training. In-batch negative instances [3] are using ground truth items of other instance sequences in the same batch as negative items. Although it is possible to provide false negatives, false negatives are less likely in the pre-training dataset with a large size. Furthermore, the target of pre-training is to provide high-quality initialized parameters and we have the finetuning with accurate supervision for downstream tasks. Therefore, we claim that inbatch negatives will not hurt the recommendation performance but have much higher training efficiency than accurate supervision. Formally, the item-item contrastive loss is calculated as:

$$
\tag{10}
$$

where sim is the similarity introduced in Equation (5); h + 𝑖 is the representation of the ground truth next item; B is the ground truth item set in one batch and 𝜏 is a temperature parameter. At the pre-training stage, we use a multi-task training strategy to jointly optimize Recformer:

$$
\tag{11}
$$

where 𝜆 is a hyper-parameter to control the weight of MLM task loss. The pre-trained model will be fine-tuned for new scenarios.

### Two-Stage Finetuning.

Similar to pre-training, we do not maintain an independent item embedding table. Instead, we encode items by Recformer. However, in-batch negatives cannot provide accurate supervision in a small dataset because it is likely to have false negatives which undermine recommendation performance. To solve this problem, we propose two-stage finetuning as shown in Algorithm 1. The key idea is to maintain an item feature matrix I ∈ R | I |×𝑑 . Different from the item embedding table, I is not learnable and all item features are encoded from Recformer. As shown in Algorithm 1, our proposed finetuning method has two stages. In stage 1, I is updated (line 4) per epoch,3 whereas, in stage 2 we freeze I and update only parameters in model 𝑀. The basic idea is that although the model is already pre-trained, item representations from the pre-trained model can still be improved by further training on downstream datasets. It is expensive to re-encode all items in every batch hence we re-encode all items in every epoch to update I (line 4) and use I as supervision for item-item contrastive learning (line 5). After obtaining the best item representations, we re-initialize the model with the corresponding parameters (line 12) and start stage 2. Since I keeps updating in stage 1, the supervision for finetuning is also changing. In this case, the model is hard to be optimized to have the best performance. Therefore, we freeze I and continue training the model until achieving the best performance on the validation dataset. The learning task used in finetuning is item-item contrastive learning which is the same as pre-training but with fully softmax instead of in-batch negatives. The finetuning loss is calculated as:

$$
\tag{12}
$$

where I𝑖 is the item feature of item 𝑖.

## Discussion

In this section, we briefly compare Recformer to other sequential recommendation methods to highlight the novelty of our method. Traditional sequential recommenders such as GRU4Rec [11], SASRec [14] and BERT4Rec [27] rely on item IDs and corresponding trainable item embeddings to train a sequential model for recommendations. These item embeddings are learned from sequential patterns of user interactions. However, as mentioned in [20], these approaches suffer from data sparsity and can not perform well with cold-start items. To reduce the dependence on item IDs, some context-aware sequential recommenders such as UniSRec [12], S3 -Rec [38], ZESRec [7] are proposed to incorporate side information (e.g., categories, titles) as prior knowledge for recommendations. All of these approaches rely on a feature extractor such as BERT [6] to obtain item feature vectors and then fuse these vectors into item representations with an independent sequential model. In this paper, we explore conducting sequential recommendations in a new paradigm that learns language representations for the next item recommendations. Instead of trainable item embeddings or fixed item features from language models, we bridge the gap between natural language understanding and sequential recommendation to directly learn representations of items and user sequences based on words. We expect the generality of natural language can improve the transferability of recommenders in order to benefit new domain adaptation and cold-start item understanding

# Experiments

In this section, we empirically show the effectiveness of our proposed model Recformer and learning framework.

## Experimental Setup

### Datasets.

To evaluate the performance of Recformer, we conduct pre-training and finetuning on different categories of Amazon review datasets [22]. The statistics of datasets after preprocessing are shown in Table 1. For pre-training, seven categories are selected as training data including “Automotive”, “Cell Phones and Accessories”, “Clothing Shoes and Jewelry”, “Electronics”, “Grocery and Gourmet Food”, “Home and Kitchen”, “Movies and TV”, and one category “CDs and Vinyl” is left out as validation data. Datasets from these categories are used as source domain datasets. For finetuning, we select six categories including “Industrial and Scientific”, “Musical Instruments”, “Arts, Crafts and Sewing”, “Office Products”, “Video Games”, “Pet Supplies”, as target domain datasets to evaluate Recformer. For pre-training and finetuning, we use the five-core datasets provided by the data source and filter items whose title is missing. Then we group the interactions by users and sort them by timestamp ascendingly. Following previous work [12], we select item attributes title, categories and brand as key-value pairs for items.

### Baselines.

We compare three groups of works as our baselines which include methods with only item IDs; methods using item IDs and treating item text as side information; and methods using only item texts as inputs.

- (1) ID-Only methods: • GRU4Rec [11] adopts RNNs to model user action sequences for session-based recommendations. We treat each user’s interaction sequence as a session. • SASRec [14] uses a directional self-attentive model to capture item correlations within a sequence. • BERT4Rec [27] employs a bi-directional self-attentive model with the cloze objective for modeling user behavior sequences. • RecGURU [16] proposes to pre-train sequence representations with an autoencoder in an adversarial learning paradigm. We do not consider overlapped users for this method in our setting. (2) ID-Text methods: • FDSA [37] uses a self-attentive model to capture item and feature transition patterns.• S 3 -Rec [38] pre-trains sequential models with mutual information maximization to learn the correlations among attributes, items, subsequences, and sequences. (3) Text-Only methods: • ZESRec [7] encodes item texts with a pre-trained language model as item features. We pre-train this method and finetune the model on six downstream datasets. • UniSRec [12] uses textual item representations from a pretrained language model and adapts to a new domain using an MoE-enhance adaptor. We initialize the model with the pre-trained parameters provided by the authors and finetune the model on target domains.

### Evaluation Settings.

To evaluate the performance of sequential recommendation, we adopt three widely used metrics NDCG@N, Recall@N and MRR, where N is set to 10. For data splitting of finetuning datasets, we apply the leave-one-out strategy [14] for evaluation: the most recent item in an interaction sequence is used for testing, the second most recent item for validation and the remaining data for training. We rank the ground-truth item of each sequence among all items for evaluation and report the average scores of all sequences in the test data.

### Implementation Details.

We build Recformer based on Longformer implemented by Huggingface 4 . For efficient computing, we set the size of the local attention windows in Longformer to 64. The maximum number of tokens is 32 for each attribute and 1,024 for each interaction sequence (i.e., 𝑋 in Equation (1)). The maximum number of items in a user sequence is 50 for all baselines and Recformer. The temperature parameter 𝜏 is 0.05 and the weight of MLM loss 𝜆 is 0.1. Other than token type embedding and item position embedding in Recformer, other parameters are initialized with pre-trained parameters of Longformer 5 before pre-training. The batch size is 64 for pre-training and 16 for finetuning. We optimize Recformer with Adam optimizer with learning rate 5e-5 and adopt early stop with the patience of 5 epochs to prevent overfitting. For baselines, we use the suggested settings introduced in [12].

## Overall Performance

We compare Recformer to baselines on six datasets across different recommendation domains. Results are shown in Table 2. For baselines, ID-Text methods (i.e., FDSA and S3 -Rec) achieve better results compared to ID-Only and Text-Only methods in general. Because ID-Text methods include item IDs and content features, they can learn both content-based information and sequential patterns from finetuning. Comparing Text-Only methods and ID-Only methods, we can find that on the Scientific, Instruments, and Pet datasets, Text-Only methods perform better than ID-Only methods. A possible reason is that the item transitions in these three datasets are highly related to item texts (i.e., title, brand) hence text-only methods can recommend the next item based on content similarity. Our proposed method Recformer, achieves the best overall performance on all datasets except the Recall@10 of Instruments. Recformer improves the NDCG@10 by 15.83% and MRR by 15.99% on average over the second best results. Different from baselines, Recformer learns language representations for sequential recommendation without pre-trained language models or item IDs. With two-stage finetuning, Recformer can be effectively adapted to downstream domains and transferred knowledge from pre-training can consistently benefit finetuning tasks. The results illustrate the effectiveness of the proposed Recformer.

## Low-Resource Performance

### Zero-Shot.

To show the effectiveness of pre-training, we evaluate the zero-shot recommendation performance of three TextOnly methods (i.e., UniSRec, ZESRec, Recformer) and compare results to the average scores of three ID-Only methods fully trained on downstream datasets. The zero-shot recommendation setting requires models to learn knowledge from pre-training datasets and directly test on downstream datasets without further training. Hence, traditional ID-based methods cannot be evaluated in this setting. We evaluate the knowledge transferability of Text-Only methods in different recommendation scenarios. All results in six downstream datasets are shown in Figure 4. Overall, Recformer improves the zero-shot recommendation performance compared to UniSRec and ZESRec on six datasets. On the Scientific dataset, Recformer performs better than the average performance of three ID-Only methods trained with full training sets. These results show that (1) natural language is promising as a general item representation across different recommendation scenarios; (2) Recformer can effectively learn knowledge from pre-training and transfer learned knowledge to downstream tasks based on language understanding.

### Low-Resource.

We conduct experiments with SASRec, UniSRec and Recformer in low-resource settings. In this setting, we train models on downstream datasets with different ratios of training data and results are shown in Figure 5. We can see that methods with item text (i.e., UniSRec and Recformer) outperform ID-only method SASRec especially when less training data is available. This indicates UniSRec and Recformer can incorporate prior knowledge and do recommendations based on item texts. In low-resource settings, most items in the test set are unseen during training for SASRec. Therefore, the embeddings of unseen items are randomly initialized and cannot provide high-quality representations for recommendations. After being trained with adequate data, SASRec could rapidly improve its performance. Recformer achieves the best performance over different ratios of training data. On the Scientific dataset, Recformer outperforms other methods by a large margin with 1% and 5% of training data.

## Further Analysis

### Performance w.r.t. Cold-Start Items.

In this section, we simulate this scenario by splitting a dataset into two parts, i.e., an in-set dataset and cold-start dataset. Specifically, for the in-set dataset, we make sure all test items appear in the training data and all other test items (never appearing in training data) will be sent to the cold-start dataset. We train models on in-set datasets and test on both in-set and cold-start datasets. In this case, models never see the cold-start items during training and item embedding tables do not contain cold-start items. We compare the ID-only method SASRec and the Text-only method UniSRec to Recformer. For ID-based SASRec, we substitute items appearing only once in the training set with a cold token and after training, we add this cold token embedding to cold-start item embeddings to provide prior knowledge 6 . For UniSRec, cold-start items are represented by item texts and encoded by BERT which is identical to seen items. Recformer directly encode item texts to represent cold-start items. Experimental results are shown in Table 3. We can see that Text-Only methods significantly outperform SASRec, especially on datasets with a large size (i.e., Arts, Pet). Because of randomly initialized cold-start item representations, the performance of SASRec is largely lower on cold-start items than in-set items. Hence, IDonly methods are not able to handle cold-start items and applying text is a promising direction. For Text-only methods, Recformer greatly improves performance on both in-set and cold-start datasets compared to UniSRec which indicates learning language representations is superior to obtaining text features for recommendations.

### Ablation Study.

We analyze how our proposed components influence the final sequential recommendation performance. The results are shown in Table 4. We introduce the variants and analyze their results respectively. We first test the effectiveness of our proposed two-stage finetuning. In variant (1) w/o two-stage finetuning, we do not update item feature matrix I and only conduct finetuning based on I from pre-trained parameters. We find that compared to (0) Recformer, (1) has similar results on Scientific but has a large margin on Instruments since the pre-trained model has better pre-trained item representations on Scientific compared to Instruments (shown in Figure 4). Hence, our proposed two-stage finetuning can effectively improve the sub-optimal item representations from pre-training and further improve performance on downstream datasets. Then, we investigate the effects of freezing/trainable word embeddings and item embeddings. In our default setting (1), we freeze the item feature matrix I and train word embeddings of Recformer. In variants (2)(3)(4), we try to train the item feature matrix or freeze word embeddings. Overall, on the Scientific dataset, the model with fixed item embeddings performs better than the model with trainable item embeddings, whereas on the Instruments dataset, our model performs well when item embeddings are trainable. The divergence can be eliminated by our two-stage finetuning strategy. Variant (5) w/o pre-training finetunes Recformer from scratch. We can see that (0) Recformer significantly outperforms Variant (5) in both datasets because without pre-training, the item feature matrix I is not trained and cannot provide informative supervision during finetuning even if we update I by two-stage finetuning. These results show the effectiveness of pre-training. Finally, we explore the effectiveness of our proposed model structure (i.e., item position embeddings and token type embeddings). Variant (6) removes the two embeddings and results show that the model in (6) causes performance decay on the instruments dataset which indicates the two embeddings are necessary when the gap between pre-training and finetuning is large.

### Pre-training Steps vs. Performance.

We investigate the zeroshot sequential recommendation performance on downstream tasks over different pre-training steps and results on four datasets are shown in Figure 6. The pre-training of natural language understanding usually requires a large number of training steps to achieve a promising result. However, we have a different situation in sequential recommendation. From Figure 6, we can see that most datasets already achieve their best performance after around 4,000 training steps and further pre-training may hurt the knowledge transferability on downstream tasks. We think there are two possible reasons: (1) We initialize most parameters from a Longformer model pre-trained by the MLM task. In this case, the model already has some essential knowledge of natural languages. The domain adaptation from a general language understanding to the item text understanding for recommendations should be fast. (2) Even if we include seven categories in the training data, there is still a language domain difference between pre-training data and downstream data since different item categories have their own specific vocabularies. For instance, the category Electronics has quite different words in item text compared to the Pets category.

# Related Work

## Sequential Recommendation

Sequential recommendation [11, 14, 27] aims to predict the next item based on historical user interactions. Proposed methods model user interactions as a sequence ordered by their timestamps. Due to the ability to capture the long-term preferences and short-term dynamics of users, sequential recommendation methods show their effectiveness for personalization and attract a lot of studies. Early works [9, 25] apply the Markov Chain to model item-item transition relations based on matrix factorization. For deep learning methods, Convolutional Sequence Embedding (Caser) [28] views the embedding matrix of previous items as an “image” and applies convolutional operations to extract transitions. GRU4Rec [11] introduces Gated Recurrent Units (GRU) [5] to model user sequential patterns. With the development of the Transformer [30], recent studies [14, 27] widely use self-attention model for sequential recommendation. Although these approaches achieve promising performance, they struggle to learn transferable knowledge or understand cold-start items due to the dependence on IDs and item embeddings which are specific to items and datasets. Recently, researchers attempt to employ textual features as transferable item representations [7, 12]. These methods first obtain item features by encoding item texts with language models and then learn transferable item representations with an independent sequential model. Independent language understanding and sequential pattern learning still limit the capacity of the model to learn user interactions based on languages. In this paper, we explore unifying the language understanding and sequential recommendations into one Transformer framework. We aim to have a sequential recommendation method that can effectively model cold-start items and learn transferable sequential patterns for different recommendation scenarios.

## Transfer Learning for Recommendation

Data sparsity and cold-start item understanding issues are challenging in recommender systems and recent studies [33, 39, 40] explore transferring knowledge across different domains to improve the recommendation at the target domain. Previous methods for knowledge transfer mainly rely on shared information between the source and target domains including common users [13, 31, 32, 35], items [26, 39] or attributes [29]. To learn common item features from different domains, pre-trained language models [6, 21] provide high-quality item features by encoding item texts (e.g., title, brand). Based on pre-trained item features, several methods [7, 12] are proposed to learn universal item representations by applying additional layers. In this work, we have the same target as previous transfer learning for recommendation (i.e., alleviate data sparsity and cold-start item issues). However, instead of relying on common users, items and attributes or encoding items with pre-trained language models, we directly learn language representations for sequential recommendation and hence transfer knowledge based on the generality of natural languages.

# Conclusion

In this paper, we propose Recformer, a framework that can effectively learn language representations for sequential recommendation. To recommend the next item based on languages, we first formulate items as key-value attribute pairs instead of item IDs. Then, we propose a novel bi-directional Transformer model for sequence and item representations. The proposed structure can learn both natural languages and sequential patterns for recommendations. Furthermore, we design a learning framework including pretraining and finetuning that helps the model learn to recommend based on languages and transfer knowledge into different recommendation scenarios. Finally, extensive experiments are conducted to evaluate the effectiveness of Recformer under full-supervised and low-resource settings. Results show that Recformer largely outperforms existing methods in different settings, especially for the zero-shot and cold-start items recommendation which indicates Recformer can effectively transfer knowledge from training. An ablation study is conducted to show the effectiveness of our proposed components.
